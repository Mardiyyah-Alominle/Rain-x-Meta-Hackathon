from typing import TypedDict, Annotated, List
from langgraph.graph import StateGraph, END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode

# --- Import Agents and Tools ---
# Import the agent node functions we created previously
from agents.sales_agent import sales_associate_node
from agents.cart_agent import cart_manager_node
from agents.fulfillment_agent import fulfillment_node

# Import read-only tools for the generic ToolNode
# (We assume product_lookup_tool is defined in tools/shop_ops.py)
from tools.shop_ops import product_lookup_tool

# Import State
from states import AgentState

# --- 2. Initialize Graph & Add Nodes (The Actors) ---
workflow = StateGraph(AgentState)

# Node 1: The AI Brain (Llama 3)
workflow.add_node("sales_associate", sales_associate_node)

# Node 2: The Cart Calculator (Deterministic code)
workflow.add_node("cart_manager", cart_manager_node)

# Node 3: The Order Finalizer (Deterministic DB operations)
workflow.add_node("fulfillment_agent", fulfillment_node)

# Node 4: Generic Tool Executor (For read-only tools like product lookup)
# We use LangGraph's prebuilt ToolNode for simple tools that don't need custom state logic.
read_only_tools = [product_lookup_tool]
workflow.add_node("read_only_tools", ToolNode(read_only_tools))


# --- 3. Define Routing Logic (The Traffic Controller) ---

def router(state: AgentState):
    """
    Inspects the output of the Sales Associate agent to decide what to do next.
    It looks at the 'tool_calls' of the last message.
    """
    messages = state["messages"]
    last_message = messages[-1]

    # If the AI just responded with text and wants no tools, end the turn.
    # This sends the text back to the user on Telegram.
    if not hasattr(last_message, "tool_calls") or not last_message.tool_calls:
        return END

    # If tool calls exist, inspect the name of the first one to route correctly.
    tool_name = last_message.tool_calls[0]["name"]

    # Route based on the intended action schema:

    # A. State-Mutating Actions -> Route to specialized deterministic agents
    if tool_name == "add_to_cart_action":
        return "cart_manager"
    elif tool_name == "signal_order_finalization":
        return "fulfillment_agent"

    # B. Read-Only Actions -> Route to the generic ToolNode
    elif tool_name == "product_lookup_tool":
         return "read_only_tools"

    # Fallback safe-guard (shouldn't normally be reached)
    return END


# --- 4. Define Edges (The Pathways) ---

# Set the entry point: Every new message goes to the Sales Associate first.
workflow.set_entry_point("sales_associate")

# Conditional Edges: After the AI thinks, use the router to decide where to go.
workflow.add_conditional_edges(
    "sales_associate",
    router,
    {
        "cart_manager": "cart_manager",
        "fulfillment_agent": "fulfillment_agent",
        "read_only_tools": "read_only_tools",
        END: END
    }
)

# Normal Edges: After any tool or specialized agent runs, ALWAYS go back
# to the Sales Associate so the AI can interpret the result and formulate a response.
workflow.add_edge("cart_manager", "sales_associate")
workflow.add_edge("fulfillment_agent", "sales_associate")
workflow.add_edge("read_only_tools", "sales_associate")


# --- 5. Compile the Application ---
# This creates the runnable object that FastAPI will use.
app = workflow.compile()