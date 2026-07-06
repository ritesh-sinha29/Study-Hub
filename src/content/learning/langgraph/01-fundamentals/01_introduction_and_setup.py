# ==========================================================
# LANGGRAPH STUDY GUIDE: 01. INTRODUCTION & SETUP
# ==========================================================

# --- WHAT IS LANGGRAPH? ---
# LangGraph is a library for building stateful, multi-actor applications with LLMs.
# Unlike standard LangChain chains which flow in a single direction, LangGraph lets you define
# cycles, loops, and state machine transitions.
# Key Pillars of LangGraph:
# 1. State: The shared database/memory of the graph (schema defined via TypedDict or Pydantic).
# 2. Nodes: Python functions that perform operations. They receive the current State and return updates to it.
# 3. Edges: Control flows that decide which Node to execute next.

from typing import TypedDict
from langgraph.graph import StateGraph, START, END

# 1. Define the State Schema
# The State is passed from node to node. Each node returns a dictionary updating this state.
class GraphState(TypedDict):
    input_text: str
    processed_text: str

# 2. Define the Nodes
# Each node is a standard Python function that takes the current State and returns updates.
def initial_clean_node(state: GraphState) -> dict:
    print("Executing: initial_clean_node")
    original = state.get("input_text", "")
    # Simple cleaning: strip whitespace and lowercase
    cleaned = original.strip().lower()
    return {"processed_text": cleaned}

def uppercase_node(state: GraphState) -> dict:
    print("Executing: uppercase_node")
    processed = state.get("processed_text", "")
    # Uppercase the processed text
    upper = processed.upper()
    return {"processed_text": upper}

def build_and_run_graph():
    print("--- 1. BUILDING LANGGRAPH ---")
    
    # 3. Initialize the StateGraph with the state schema
    builder = StateGraph(GraphState)
    
    # 4. Add the Nodes
    builder.add_node("clean_step", initial_clean_node)
    builder.add_node("shout_step", uppercase_node)
    
    # 5. Connect the Nodes with Edges
    # START is a built-in entry point that routes the initial input to the first node
    builder.add_edge(START, "clean_step")
    builder.add_edge("clean_step", "shout_step")
    # END is a built-in termination point
    builder.add_edge("shout_step", END)
    
    # 6. Compile the Graph
    graph = builder.compile()
    
    # 7. Run the Graph
    initial_input = {"input_text": "   Welcome to LangGraph Masterclass!   "}
    print(f"Initial Input: {initial_input}")
    
    result = graph.invoke(initial_input)
    print(f"Final State: {result}")

if __name__ == "__main__":
    build_and_run_graph()

# ==========================================================
# REAL-LIFE USE CASES
# ==========================================================
# 1. ORDER PROCESSING WORKFLOW: Graph state holds the order details. Node 1 verifies payment,
#    Node 2 reserves inventory, Node 3 triggers shipping updates, routing to failure nodes if errors occur.
# 2. EMAIL TRIAGING SYSTEM: Node 1 classifies emails (spam, query, billing). Edges route billing queries
#    to a support-bot node and spam straight to the archive/end node.

# ==========================================================
# MNC INTERVIEW QUESTIONS & ANSWERS
# ==========================================================
# Q1. What is a "State" in LangGraph and how does it differ from memory in chains?
# A:  In LangGraph, State is a centralized data schema that persists across the lifecycle of the graph run.
#     Every node can read from it and return updates to it. Unlike chain memory which is often just a list
#     of past messages, Graph State can hold arbitrary structured variables (dictionaries, Pydantic objects).
#
# Q2. How do Nodes update the State in LangGraph?
# A:  Nodes do not overwrite the state directly. They return a dictionary containing key-value updates.
#     LangGraph automatically merges these updates back into the centralized state. By default, updates
#     overwrite keys, but you can define custom reducers (like adding items to a list) using the Annotated type.
