from langchain_core.messages import ToolMessage
from states import AgentState, CartItem
from langchain_core.tools import tool

# --- Dummy Tool Definition ---
# This tool is NOT executed by the standard ToolNode.
# It is bound to the Sales Agent so the LLM knows the *schema* for adding items.
# The cart_manager_node intercepts calls to this tool name.
@tool
def add_to_cart_action(product_id: str, name: str, unit_price: float, quantity: int = 1):
    """
    Call this action when the user explicitly wants to add a specific product to their temporary shopping cart.
    Ensure you have the exact product_id and unit_price from a previous product_lookup_tool call.
    """
    # This function body never actually runs; it's just for schema generation.
    pass


# --- The Cart Manager Node ---
def cart_manager_node(state: AgentState):
    """
    The "Calculator" Node.
    This is a deterministic node that manages cart state updates.
    It intercepts specific tool calls intended for state mutation, updates the cart list,
    and recalculates the total value.
    """
    last_message = state["messages"][-1]
    current_cart = state.get("cart", [])

    # Check if the last message is an AI message trying to call the "add_to_cart_action" schema.
    if hasattr(last_message, "tool_calls") and last_message.tool_calls:
         tool_call = last_message.tool_calls[0]

         if tool_call["name"] == "add_to_cart_action":
             # 1. Extract arguments from the intended call
             args = tool_call["args"]
             product_id = args.get("product_id")
             name = args.get("name")
             # Ensure quantity is at least 1
             quantity = max(1, int(args.get("quantity", 1)))
             unit_price = float(args.get("unit_price", 0.0))

             # Basic validation: Don't add items without price or ID
             if not product_id or unit_price <= 0:
                 return {
                     "messages": [ToolMessage(tool_call_id=tool_call["id"], content="Error: Missing valid product details (ID or Price) for cart.")]
                 }

             # 2. Update Cart Logic (Deterministic Math)
             updated_cart = [item.copy() for item in current_cart] # Shallow copy to avoid mutation issues
             item_found = False

             # Check if item already exists to update quantity
             for item in updated_cart:
                 if item["product_id"] == product_id:
                     item["quantity"] += quantity
                     item_found = True
                     break

             # If not found, append as a new item
             if not item_found:
                 new_item: CartItem = {
                     "product_id": product_id,
                     "name": name,
                     "quantity": quantity,
                     "unit_price": unit_price
                 }
                 updated_cart.append(new_item)

             # 3. Calculate new total ("The Calculator" part)
             # Performing dynamic arithmetic based on current state[cite: 710].
             new_total = sum(item["quantity"] * item["unit_price"] for item in updated_cart)

             # 4. Return the state update
             # We return the new cart, new total, and a ToolMessage to confirm the action to the AI.
             return {
                 "cart": updated_cart,
                 "cart_total": new_total,
                 "messages": [ToolMessage(tool_call_id=tool_call["id"], content=f"Successfully added {quantity} x {name} to cart. Current cart total: {new_total}")]
             }

    # If no relevant action detected, return nothing (state remains the same)
    return {}