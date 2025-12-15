from langchain_core.tools import tool
from firebase_admin import firestore
from utils.db import db

# ==========================================
# Part 1: The Core DB Logic (The "Real" Tool)
# ==========================================
def execute_order_finalization(cart_items: list, customer_id: str, payment_method: str = "N/A") -> str:
    """
    Performs the actual database changes for finalizing an order.
    This function is called directly by the fulfillment_node, not by the LLM.
    It ensures atomicity using a database batch[cite: 635].
    """
    if db is None:
         return "Transaction Error: Database connection not established."

    try:
        if not cart_items:
            return "Transaction Error: Cart is empty. Cannot finalize order."

        # Calculate total transaction value
        total_amount = sum(item['quantity'] * item['unit_price'] for item in cart_items)

        # Prepare Database References
        sales_ref = db.collection("sales")
        products_ref = db.collection("products")

        # Use a Batch Write for Atomicity
        batch = db.batch()

        # A. Create Sale Record
        new_sale_doc = sales_ref.document()
        sale_data = {
            "customer_id": customer_id,
            "items": cart_items,
            "total_amount": total_amount,
            "status": "Confirmed",
            "payment_method": payment_method,
            "timestamp": firestore.SERVER_TIMESTAMP
        }
        batch.set(new_sale_doc, sale_data)

        # B. Decrement Inventory
        for item in cart_items:
            product_id = item.get("product_id")
            quantity_sold = item.get("quantity")
            if product_id and quantity_sold > 0:
                prod_doc_ref = products_ref.document(product_id)
                batch.update(prod_doc_ref, {"stock_count": firestore.Increment(-quantity_sold)})

        # Commit the Batch
        batch.commit()

        return f"SUCCESS: Order finalized successfully. Order ID: {new_sale_doc.id}. Total confirmed: {total_amount}."

    except Exception as e:
        return f"Error occurred during transaction finalization: {e}"


# ==========================================
# Part 2: The Tool Schema for the AI Agent
# ==========================================
@tool
def signal_order_finalization(payment_method: str = "N/A"):
    """
    Call this tool ONLY when the customer has explicitly confirmed they want to finalize their current order.
    This signals the system to process the items currently in their cart.
    Args:
        payment_method: The agreed payment method (e.g., "Bank Transfer"). Defaults to "N/A".
    """
    # This function body never actually runs; it's just for schema generation for the LLM.
    pass