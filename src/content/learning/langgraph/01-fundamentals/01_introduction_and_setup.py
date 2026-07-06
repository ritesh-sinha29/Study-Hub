# ========================================================================================
# LANGGRAPH CRASH COURSE — MODULE 01: INTRODUCTION & THE STATE-GRAPH-NODE-EDGE PARADIGM
# ========================================================================================
#
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# SECTION 1 — WHAT IS LANGGRAPH AND WHY WAS IT BUILT?
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#
# LangChain's LCEL is perfect for LINEAR pipelines:
#   prompt | model | parser  (A → B → C, done)
#
# But real-world agents need:
#   - LOOPS (retry until output is good enough)
#   - BRANCHING (route to different steps based on content)
#   - SHARED MEMORY (multiple nodes reading/writing the same variables)
#   - PERSISTENCE (state survives restarts, power cuts, server deploys)
#   - HUMAN REVIEW (pause mid-execution, wait for human input, resume)
#
# LangGraph was built specifically for these requirements. It treats your AI application
# as a directed graph (like a flowchart) where nodes are Python functions and edges
# define the control flow between them.
#
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# SECTION 2 — THE FOUR PILLARS OF LANGGRAPH
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#
#  PILLAR       │ WHAT IT IS                          │ ANALOGY
#  ─────────────┼─────────────────────────────────────┼──────────────────────────────
#  State        │ A TypedDict/Pydantic schema defining  │ A shared whiteboard in an
#               │ all the data that flows through the   │ office — anyone can read/write
#               │ graph. Persists across all nodes.     │ anything on it
#  ─────────────┼─────────────────────────────────────┼──────────────────────────────
#  Nodes        │ Regular Python functions that receive │ Workers who read from the
#               │ the full State and return a dict of   │ whiteboard, do their job,
#               │ updates to apply back to it.          │ and update it with results
#  ─────────────┼─────────────────────────────────────┼──────────────────────────────
#  Edges        │ Connections defining which node runs  │ The arrows in a flowchart
#               │ after which. Can be fixed or dynamic  │ telling workers who goes next
#               │ (conditional routing).                │
#  ─────────────┼─────────────────────────────────────┼──────────────────────────────
#  Checkpointer │ Saves the full State after every node │ Auto-save in a video game
#               │ execution to a database. Enables       │ — lose power, load the save,
#               │ memory, resume, time-travel.          │ continue from that point
#
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# SECTION 3 — HOW NODES UPDATE STATE (REDUCERS)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#
# A node NEVER modifies state directly. It returns a dict of changes, and LangGraph
# applies those changes to the shared state using a REDUCER.
#
# DEFAULT REDUCER (overwrite):
#   If a node returns {"name": "Ritesh"}, the state["name"] is replaced by "Ritesh".
#
# CUSTOM REDUCER (add_messages — append instead of overwrite):
#   messages: Annotated[list, add_messages]
#   If a node returns {"messages": [new_msg]}, it's APPENDED to the list,
#   not replacing the entire list. This is critical for chat history.
#
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# SECTION 4 — GRAPH CONSTRUCTION LIFECYCLE
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#
#  STEP 1: Define State Schema (TypedDict or Pydantic)
#  STEP 2: Define Node functions (Python functions)
#  STEP 3: Instantiate StateGraph(StateSchema)
#  STEP 4: Add nodes:  builder.add_node("name", function)
#  STEP 5: Add edges:  builder.add_edge(source, target)
#  STEP 6: Compile:    graph = builder.compile()
#  STEP 7: Invoke:     result = graph.invoke({"key": "value"})
#
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# SECTION 5 — LANGGRAPH vs LANGCHAIN LCEL: WHEN TO USE WHICH
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#
#  USE LCEL (LangChain) WHEN:              USE LANGGRAPH WHEN:
#  ✓ The flow is strictly linear           ✓ You need loops (retry/feedback)
#  ✓ No state is shared between steps      ✓ Multiple agents share state
#  ✓ Single-step RAG or summarization      ✓ You need human approval pauses
#  ✓ Simple prompt → model → output        ✓ You need cross-session memory
#  ✓ High-throughput batch jobs            ✓ Complex multi-path routing
#
# ========================================================================================

from typing import TypedDict
from langgraph.graph import StateGraph, START, END


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# STEP 1: DEFINE THE GRAPH STATE
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

# TypedDict defines the "shape" of the shared whiteboard.
# Every node reads from and writes to this schema.
class GraphState(TypedDict):
    input_text:      str   # Original raw input from the user
    processed_text:  str   # Text after transformation nodes have run


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# STEP 2: DEFINE THE NODE FUNCTIONS
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def initial_clean_node(state: GraphState) -> dict:
    """
    NODE: Clean & Normalize

    Reads `input_text` from the shared state, strips extra whitespace and
    lowercases the string, then returns the update dict.

    IMPORTANT: This function DOES NOT mutate state in place.
    It returns {"processed_text": cleaned} and LangGraph applies the update.
    """
    print("  [Node] initial_clean_node executing...")
    original = state.get("input_text", "")
    cleaned  = original.strip().lower()
    print(f"    Input : '{original}'")
    print(f"    Output: '{cleaned}'")
    return {"processed_text": cleaned}


def uppercase_node(state: GraphState) -> dict:
    """
    NODE: Uppercase Transformer

    Reads the ALREADY-CLEANED `processed_text` from state (written by the
    previous node) and uppercases it. This demonstrates how nodes form a
    sequential data pipeline via shared state.
    """
    print("  [Node] uppercase_node executing...")
    processed = state.get("processed_text", "")
    upper     = processed.upper()
    print(f"    Input : '{processed}'")
    print(f"    Output: '{upper}'")
    return {"processed_text": upper}


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# STEPS 3-7: BUILD, COMPILE & RUN THE GRAPH
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def build_and_run_graph():
    print("\n" + "="*70)
    print("BUILDING & RUNNING THE FIRST LANGGRAPH")
    print("="*70)

    # STEP 3: Instantiate StateGraph with the schema
    builder = StateGraph(GraphState)

    # STEP 4: Register nodes
    # "clean_step" and "shout_step" are the node names used in edges
    builder.add_node("clean_step", initial_clean_node)
    builder.add_node("shout_step", uppercase_node)

    # STEP 5: Define edges (control flow)
    # START is a built-in sentinel — the first edge from START defines the entry node
    builder.add_edge(START, "clean_step")           # Entry → clean_step
    builder.add_edge("clean_step", "shout_step")   # clean_step → shout_step
    builder.add_edge("shout_step", END)             # shout_step → exit

    # STEP 6: Compile — locks the graph and prepares it for execution
    # After compile(), no more nodes or edges can be added
    graph = builder.compile()

    # STEP 7: Invoke — runs the full graph from START to END
    initial_input = {"input_text": "   Welcome to LangGraph Masterclass!   "}
    print(f"\n  Initial Input: {initial_input}")
    print(f"\n  Graph Execution:")

    result = graph.invoke(initial_input)

    print(f"\n  Final State:")
    print(f"    input_text     : '{result.get('input_text')}'")
    print(f"    processed_text : '{result.get('processed_text')}'")


if __name__ == "__main__":
    build_and_run_graph()


# ========================================================================================
# REAL-WORLD USE CASES
# ========================================================================================
#
# 1. ORDER PROCESSING WORKFLOW:
#    State holds: order_id, payment_status, inventory_reserved, shipping_triggered
#    Node 1: verify_payment (checks Stripe API)
#    Node 2: reserve_inventory (checks warehouse DB)
#    Node 3: trigger_shipping (calls logistics API)
#    Conditional edges route to failure nodes if any step encounters an error.
#
# 2. EMAIL TRIAGE SYSTEM:
#    Node 1: classify_email (spam / billing / general)
#    Conditional edges: spam → archive node, billing → support_agent node
#    The graph automates routing without any if-else code in the main application.
#
# ========================================================================================
# MNC INTERVIEW QUESTIONS & ANSWERS
# ========================================================================================
#
# Q1. What is Graph State in LangGraph and how does it differ from LangChain memory?
# A:  LangGraph State is a centralized typed schema that persists across the entire graph
#     lifecycle. Every node can read any field and write updates to any field. Unlike
#     LangChain's RunnableWithMessageHistory (which only tracks messages), LangGraph State
#     can hold arbitrary structured data: order details, user profiles, flags, counters,
#     tool results — anything your application needs across steps.
#
# Q2. How do nodes update state without mutating it directly?
# A:  Nodes return a plain Python dict containing ONLY the keys they want to update.
#     LangGraph applies these updates using a reducer function. The default reducer
#     overwrites the value. For lists (like message history), you use:
#       messages: Annotated[list[BaseMessage], add_messages]
#     which appends new items instead of overwriting the entire list.
#
# Q3. What is START and END in LangGraph and why are they needed?
# A:  START is a sentinel node that marks the graph's entry point. The first
#     `add_edge(START, "node_name")` tells LangGraph which node receives the initial
#     input dict. END is a sentinel that marks a terminal state — any edge pointing
#     to END means "execution stops here". Both are imported from `langgraph.graph`.
