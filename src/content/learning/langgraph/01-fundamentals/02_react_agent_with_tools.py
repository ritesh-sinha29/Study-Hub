# ========================================================================================
# LANGGRAPH CRASH COURSE — MODULE 02: REACT AGENT WITH TOOLS
# ========================================================================================
#
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# SECTION 1 — WHAT IS THE REACT PATTERN?
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#
# ReAct (Reasoning + Acting) is the most common agentic loop pattern. The model cycles
# through three phases until it has enough information to give a final answer:
#
#  ┌─────────────────────────────────────────────────────────────────────┐
#  │                    REACT LOOP CYCLE                                 │
#  │                                                                     │
#  │   User Input                                                        │
#  │       │                                                             │
#  │       ▼                                                             │
#  │   ┌─────────┐   THOUGHT: "I need to call calculate_square(9)"      │
#  │   │  Agent   │──────────────────────────────────────────────────► │
#  │   │  (LLM)   │                                                      │
#  │   └─────────┘ ◄──────────────────────────────────────────────────  │
#  │       │        OBSERVATION: tool returned "81"                      │
#  │       │                                                             │
#  │       │ if tool_calls exist:                                        │
#  │       ▼                                                             │
#  │   ┌─────────┐   ACTION: execute calculate_square(9) → "81"         │
#  │   │  Tools   │                                                      │
#  │   └─────────┘                                                      │
#  │       │                                                             │
#  │       │ loop back to Agent with ToolMessage                         │
#  │       ▼                                                             │
#  │   if no tool_calls → FINAL ANSWER: "The square of 9 is 81."        │
#  └─────────────────────────────────────────────────────────────────────┘
#
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# SECTION 2 — THE `add_messages` REDUCER
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#
# By default, when a node returns {"messages": [new_msg]}, LangGraph would REPLACE
# the entire messages list. This would erase conversation history!
#
# `add_messages` is a reducer function that tells LangGraph to APPEND instead:
#
#   State before:   messages = [HumanMessage("Hi")]
#   Node returns:   {"messages": [AIMessage("Hello!")]}
#   State after:    messages = [HumanMessage("Hi"), AIMessage("Hello!")]  ← APPENDED
#
#   Without add_messages:
#   State after:    messages = [AIMessage("Hello!")]  ← OVERWROTE (history lost!)
#
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# SECTION 3 — THE TOOLNODE: LangGraph's PREBUILT TOOL EXECUTOR
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#
# `ToolNode` is a prebuilt LangGraph node that:
#   1. Reads the last AIMessage.tool_calls from state
#   2. Looks up the corresponding Python function by name
#   3. Calls it with the provided args (dict from the model)
#   4. Wraps the result in a ToolMessage
#   5. Returns {"messages": [ToolMessage(...)]}  ← appended via add_messages
#
# You don't need to write any tool dispatch logic manually. Just pass your tool list
# to ToolNode and it handles everything.
#
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# SECTION 4 — THE CONDITIONAL SHOULD_CONTINUE ROUTER
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#
# After the agent runs, we don't know in advance if it will:
#   A) Request a tool call (needs to go to ToolNode)
#   B) Generate a final answer (needs to go to END)
#
# A routing function checks the last message:
#   if last_message.tool_calls:  → route to "tools"
#   else:                        → route to END
#
# This is added via `builder.add_conditional_edges(...)`.
#
# ========================================================================================

from typing import Annotated
from typing_extensions import TypedDict
from langchain_core.tools import tool
from langchain_core.messages import BaseMessage
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode
from langchain.chat_models import init_chat_model


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# STEP 1: DEFINE TOOLS
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

@tool
def calculate_square(number: int) -> str:
    """
    Calculate the square of an integer number.
    Use this when asked to compute a number raised to the power of 2, or squared.

    Args:
        number: The integer to square.

    Returns:
        A string describing the square of the number.
    """
    return f"The square of {number} is {number * number}."


@tool
def get_city_population(city: str) -> str:
    """
    Get the approximate population of a given city.
    Use this tool when the user asks about a city's population size.

    Args:
        city: The name of the city.

    Returns:
        A string with the population data.
    """
    populations = {
        "mumbai":   "Mumbai: ~21 million (2024 estimate)",
        "tokyo":    "Tokyo: ~37 million (2024 estimate)",
        "new york": "New York: ~8.3 million (2024 estimate)",
    }
    return populations.get(city.lower(), f"Population data unavailable for '{city}'.")


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# STEP 2: DEFINE THE STATE
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

# Annotated[list[BaseMessage], add_messages] tells LangGraph to APPEND
# new messages rather than overwriting the list on every node update.
class AgentState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# STEP 3: DEFINE THE AGENT NODE
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def call_model(state: AgentState, model) -> dict:
    """
    Agent Node: calls the LLM with the full message history.

    The model sees all messages (HumanMessages, AIMessages, ToolMessages)
    and decides whether to call a tool or produce a final answer.
    """
    print("  [Node] call_model executing...")
    messages  = state["messages"]
    response  = model.invoke(messages)

    print(f"  [Node] AI response: tool_calls={bool(response.tool_calls)}, content='{response.content[:60]}'")
    # Return as list — add_messages will append it to the existing messages
    return {"messages": [response]}


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# STEP 4: CONDITIONAL ROUTER
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def should_continue(state: AgentState) -> str:
    """
    Router function: decides the next step after the agent runs.

    Returns "tools" if the model wants to call a tool.
    Returns END if the model has produced a final answer.
    """
    last_message = state["messages"][-1]
    if last_message.tool_calls:
        print("  [Router] Tool calls detected → routing to tools node")
        return "tools"
    print("  [Router] No tool calls → routing to END")
    return END


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# STEP 5: BUILD THE REACT GRAPH
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def build_react_agent(model, tools: list):
    """
    Constructs and compiles the ReAct agent graph.

    Architecture:
      START → agent → (conditional) → tools → agent (loop)
                                    ↘ END
    """
    print("\n" + "="*70)
    print("BUILDING REACT AGENT GRAPH")
    print("="*70)

    builder = StateGraph(AgentState)

    # ToolNode handles executing any tool the model requests
    tool_node = ToolNode(tools)

    builder.add_node("agent", lambda state: call_model(state, model))
    builder.add_node("tools", tool_node)

    builder.add_edge(START, "agent")

    # Conditional edge: after agent runs, route based on tool_calls presence
    builder.add_conditional_edges(
        "agent",
        should_continue,
        {
            "tools": "tools",
            END:     END
        }
    )

    # After tool execution → always return to agent to process tool results
    builder.add_edge("tools", "agent")

    return builder.compile()


if __name__ == "__main__":
    tools_list = [calculate_square, get_city_population]

    try:
        model = init_chat_model("gpt-4o-mini", model_provider="openai")
        model_with_tools = model.bind_tools(tools_list)

        agent = build_react_agent(model_with_tools, tools_list)

        # Test 1: Tool call required
        print("\n--- TEST 1: Query requiring calculate_square tool ---")
        query_1 = {"messages": [("user", "What is the square of 9?")]}
        result_1 = agent.invoke(query_1)
        print("\nFull message thread:")
        for msg in result_1["messages"]:
            print(f"  [{msg.type.upper()}]: {msg.content}")

        # Test 2: Query requiring population tool
        print("\n--- TEST 2: Query requiring population tool ---")
        query_2 = {"messages": [("user", "What is the population of Tokyo?")]}
        result_2 = agent.invoke(query_2)
        print("\nFinal answer:", result_2["messages"][-1].content)

    except Exception as e:
        print("\nReAct agent failed (check API keys):", e)


# ========================================================================================
# REAL-WORLD USE CASES
# ========================================================================================
#
# 1. DATABASE COPILOT:
#    User asks: "Show me sales for Q3 in Mumbai."
#    Agent calls: execute_sql_query(query="SELECT * FROM sales WHERE region='Mumbai' AND quarter='Q3'")
#    Reads result, then formats it as a natural language summary.
#
# 2. DEVOPS AUTOMATION AGENT:
#    User says: "Check if the prod server is healthy."
#    Agent calls: check_server_health(server="prod"), then log_event(msg="health checked")
#    Parallel tool calls execute simultaneously. Agent synthesizes the final status report.
#
# ========================================================================================
# MNC INTERVIEW QUESTIONS & ANSWERS
# ========================================================================================
#
# Q1. What is the role of the `add_messages` reducer in a ReAct agent?
# A:  Without `add_messages`, every node update would REPLACE the messages list with only
#     the latest message, erasing all prior conversation context. `add_messages` is an
#     Annotated reducer that appends new messages to the existing list, preserving the
#     full conversation thread (HumanMessages, AIMessages, ToolMessages) across all nodes.
#
# Q2. Why is the edge from "tools" back to "agent" necessary?
# A:  The ToolNode executes the tool and appends a ToolMessage to state. But ToolMessages
#     are raw data — they don't generate human-friendly explanations. Routing back to the
#     agent lets the LLM read the ToolMessage content and synthesize a final natural-language
#     response for the user, completing the OBSERVE phase of the ReAct loop.
#
# Q3. What happens in the agent state when a tool is called?
# A:  The cycle produces this message sequence in state["messages"]:
#       [HumanMessage("What is 9²?"),
#        AIMessage(tool_calls=[{"name":"calculate_square","args":{"number":9}}]),
#        ToolMessage(content="The square of 9 is 81.", tool_call_id="call_xyz"),
#        AIMessage("The square of 9 is 81.")]   ← final answer
