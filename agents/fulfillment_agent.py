from langchain_core.messages import ToolMessage
# Assuming AgentState is defined in a common states.py file and includes 'cart' and 'customer_id'
from states import AgentState
# Import the core database logic function from your tools directory.
# NOTE: This must be the raw Python function, not the @tool wrapper.
from tools.order_ops import execute_order_finalization

def fulfillment_node(state: AgentState):
    """
    The "Accountant" Agent Node.
    This is a deterministic node that executes the final order processing[cite: 632].
    It intercepts the 'signal_order_finalization' tool call from the AI agent.
    It then takes the cart and customer ID directly from the state, executes the
    database transaction, clears the cart upon success, and returns the result.
    """
    last_message = state["messages"][-1]

    # Get the current cart and customer ID directly from the global state.
    current_cart = state.get("cart", [])
    customer_id = state.get("customer_id")

    # Check if the last message is an AI message trying to call the "signal_order_finalization" schema.
    # This pattern detects intent without running an LLM itself[cite: 242, 441].
    if hasattr(last_message, "tool_calls") and last_message.tool_calls:
        tool_call = last_message.tool_calls[0]

        if tool_call["name"] == "signal_order_finalization":
            # Basic validation: Ensure we have a customer ID to associate with the order.
            if not customer_id:
                 return {
                     "messages": [ToolMessage(tool_call_id=tool_call["id"], content="Error: Missing customer ID. Cannot finalize order.")]
                 }

            # 1. Extract arguments from the AI's intended call.
            args = tool_call["args"]
            payment_method = args.get("payment_method", "N/A")

            # 2. Execute the DB operation (The "Settlement" logic)[cite: 635].
            # We pass the Python cart object directly from the state.
            result_message = execute_order_finalization(current_cart, customer_id, payment_method)

            # 3. Determine state updates based on success or failure.
            new_cart = current_cart
            new_total = state.get("cart_total", 0.0)

            if "SUCCESS" in result_message:
                # On successful transaction, clear the cart and reset the total.
                new_cart = []
                new_total = 0.0

            # 4. Return the state update.
            # This provides the result back to the workflow and updates the global state.
            return {
                "cart": new_cart,
                "cart_total": new_total,
                "messages": [ToolMessage(tool_call_id=tool_call["id"], content=result_message)]
            }

    # If no relevant tool call is detected, return an empty update (state remains the same).
    return {}
    