from langchain_core.tools import tool
from utils.db import db

# --- The Tool Definition ---

@tool
def product_lookup_tool(product_name_query: str):
    """
    Searches the inventory database for a specific product by its name.
    ALWAYS use this tool when a user asks about an item's price, availability, or stock.
    Do not guess product information.
    Args:
        product_name_query: The name of the product to search for (e.g., "sage tote bag").
    Returns:
        A string containing the product details (name, price, stock) or a "not found" message.
    """
    # Basic safety check if db connection failed
    if db is None:
         return "Error: Database connection not established."

    try:
        # 1. Access the 'products' collection in Firestore
        products_ref = db.collection("products")

        # 2. Query database: Find documents where 'name' matches the input query.
        # We limit to 1 result assuming product names are unique.
        # Note: This is an exact match. For fuzzy search, you'd need a third-party service like Algolia,
        # but exact match is usually sufficient for a hackathon MVP.
        query = products_ref.where("name", "==", product_name_query.strip()).limit(1)
        results = query.stream()

        product_data = None
        # Iterate through results (will only be one at most due to limit(1))
        for doc in results:
            product_data = doc.to_dict()
            # We can also grab the document ID if needed later
            # product_id = doc.id
            break

        # 3. Format the output for the LLM
        if product_data:
            # If found, return a formatted string the LLM can easily parse and use in conversation.
            # This mirrors patterns used in source tools to return structured string data[cite: 363, 394].
            name = product_data.get('name', 'Unknown')
            price = product_data.get('selling_price', 'N/A') # Using 'selling_price' as defined in your schema
            stock = product_data.get('stock_count', 0)

            return (f"Found Product Information:\n"
                    f"- Item Name: {name}\n"
                    f"- Price: ₦{price:,}\n"
                    f"- Current Stock Level: {stock}")
        else:
            return f"Results: No product found matching the name '{product_name_query}'."

    except Exception as e:
        # Handle potential database connection or query errors gracefully.
        # Matches the error handling pattern found in source tools[cite: 81, 137, 396].
        return f"Error occurred during product lookup: {e}"