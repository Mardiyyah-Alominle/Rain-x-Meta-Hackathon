from langchain_groq import ChatGroq
from langchain_core.messages import SystemMessage
from config import Config

# Import the tools you created
from tools.shop_ops import product_lookup_tool
from tools.order_ops import signal_order_finalization

# --- Persona Definition ---
# This system prompt defines the agent's personality and crucial operational rules.
# [cite_start]It enforces the behavior that the AI must not guess facts but must use tools[cite: 643].
SYSTEM_PROMPT = """You are 'AestheticBot', a friendly, trendy student sales associate for an aesthetic goods brand selling on Telegram. Use relevant emojis ✨.

YOUR GOAL: Help the customer find items they love and answer their questions to move towards a sale.

CRITICAL RULES:
1. **DO NOT GUESS PRICES OR STOCK.** You do not have this information stored internally.
2. **ALWAYS use the available tools** (e.g., product_lookup_tool) to look up real-time information from the database when a user asks about specific items, availability, or pricing.
3. If a tool returns that an item is out of stock, suggest a similar alternative if possible.
4. Keep responses concise and optimized for chat.
5. Maintain a helpful, cool, "studentpreneur" vibe.
"""

# --- LLM Initialization ---
# [cite_start]Initialize the Groq LLM using values from the central Config file[cite: 170, 635, 636, 637, 638, 639, 892, 893, 894, 895, 896].
llm = ChatGroq(
    temperature=0.3, # A slightly higher temperature for a more engaging, conversational tone.
    model_name=Config.MODEL_NAME,
    api_key=Config.GROQ_API_KEY
)

# --- Tool Binding ---
# [cite_start]Define the list of tools the agent can use[cite: 642, 899].
tools = [product_lookup_tool, signal_order_finalization]

# [cite_start]Bind the tools to the LLM so it knows how to call them[cite: 643, 900].
llm_with_tools = llm.bind_tools(tools)


# --- Agent Node Definition ---
def sales_associate_node(state):
    """
    The Sales Associate Agent Node ("The Brain").
    It looks at the conversation history in the 'state' and decides the next action:
    [cite_start]either responding directly to the user or calling a tool for information[cite: 646, 647, 903].
    """
    # Get the current conversation history from the state.
    messages = state["messages"]

    # [cite_start]Prepend the SystemMessage to define the persona and rules before the conversation history[cite: 184, 687].
    full_history = [SystemMessage(content=SYSTEM_PROMPT)] + messages

    # [cite_start]Invoke the LLM (with bound tools) against the full history[cite: 183, 649, 905].
    response = llm_with_tools.invoke(full_history)

    # [cite_start]Return the updated state containing the AI's new message[cite: 649, 905].
    return {"messages": [response]}