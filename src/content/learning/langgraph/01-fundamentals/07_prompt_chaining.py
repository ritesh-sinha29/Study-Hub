# ==========================================================
# LANGGRAPH STUDY GUIDE: 07. PROMPT CHAINING
# ==========================================================

# --- PROMPT CHAINING ---
# Prompt Chaining is a sequential workflow where the output of one LLM prompt 
# serves as the input to the next LLM prompt.
#
# In LangGraph, we represent this as a direct sequence of nodes:
# Node 1 (Generate Initial Draft) -> Node 2 (Refine/Translate/Format Draft) -> END.
# This decomposes a complex single prompt instruction into smaller, highly reliable steps.

from typing import TypedDict
from langgraph.graph import StateGraph, START, END

# 1. Define the Graph State
class ChainingState(TypedDict):
    topic: str
    draft: str
    refined_output: str

# 2. Define the Nodes
def generate_draft_node(state: ChainingState) -> dict:
    print("Executing: generate_draft_node")
    topic = state.get("topic", "")
    # Simulation of initial LLM generation
    draft = f"Initial outline about {topic}: 1. Introduction, 2. History, 3. Future Prospects."
    return {"draft": draft}

def refine_draft_node(state: ChainingState) -> dict:
    print("Executing: refine_draft_node")
    draft = state.get("draft", "")
    # Simulation of refinement LLM step
    refined = f"{draft} [REFINED: Added executive summary and bibliography references]"
    return {"refined_output": refined}

def build_chaining_graph():
    print("--- 7. BUILDING PROMPT CHAINING GRAPH ---")
    builder = StateGraph(ChainingState)
    
    # Add nodes
    builder.add_node("generator", generate_draft_node)
    builder.add_node("refiner", refine_draft_node)
    
    # Establish edges (START -> Node 1 -> Node 2 -> END)
    builder.add_edge(START, "generator")
    builder.add_edge("generator", "refiner")
    builder.add_edge("refiner", END)
    
    return builder.compile()

if __name__ == "__main__":
    graph = build_chaining_graph()
    
    test_input = {"topic": "Quantum Computing"}
    print(f"\nUser Input: {test_input}")
    
    result = graph.invoke(test_input)
    print("Final State Output:")
    print("Draft:", result.get("draft"))
    print("Refined Output:", result.get("refined_output"))

# ==========================================================
# REAL-LIFE USE CASES
# ==========================================================
# 1. REPORT GENERATOR: Node 1 gathers data points. Node 2 writes the draft from the points.
#    Node 3 proofreads and checks grammar. Node 4 exports it as PDF.
# 2. SQL QUERY RUNNER: Node 1 translates natural language to SQL. Node 2 executes the SQL query.
#    Node 3 takes the query response and formats it as a user-friendly report.

# ==========================================================
# MNC INTERVIEW QUESTIONS & ANSWERS
# ==========================================================
# Q1. What is Prompt Chaining and why is it preferred over a single large prompt?
# A:  Prompt Chaining breaks down a complex task into smaller sub-tasks executed sequentially.
#     It is preferred because LLMs perform better on simple, focused tasks. It reduces token usage 
#     per call, increases reliability, and makes debugging individual steps much easier.
#
# Q2. How is state handled between steps in a Prompt Chaining graph?
# A:  All state variables are stored in the shared Graph State dictionary. Node 1 writes to the
#     `draft` key, which is then read by Node 2 when it begins execution, passing context forward.
