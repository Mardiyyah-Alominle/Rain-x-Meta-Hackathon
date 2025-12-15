from typing import TypedDict, Annotated, List, Dict, Any
from langgraph.graph.message import add_messages

# Define the structure of a single item in the cart
class CartItem(TypedDict):
    product_id: str
    name: str
    quantity: int
    unit_price: float

# Define the overall state of the conversation for LangGraph
class AgentState(TypedDict):
    # Standard message history, appending new messages
    messages: Annotated[List, add_messages]
    # The cart holds the current list of items selected by the user
    cart: List[CartItem]
    # The running total value of the cart (The "Calculator" part)
    cart_total: float