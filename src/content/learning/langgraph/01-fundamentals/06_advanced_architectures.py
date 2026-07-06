# ==========================================================
# LANGGRAPH STUDY GUIDE: 06. ADVANCED ARCHITECTURES
# ==========================================================

# --- ADVANCED AGENTIC COGNITIVE ARCHITECTURES ---
# Moving beyond basic ReAct loops, complex enterprise systems use patterns like:
# 1. Prompt Chaining: Sequential prompts where output of prompt A feeds into prompt B.
# 2. Worker-Orchestrator: An Orchestrator agent breaks a large task down, assigns sub-tasks 
#    to specialized Worker agents, and consolidates their reports.
# 3. Generator-Evaluator: A generator node generates a response, and an evaluator node 
#    checks it against quality/safety metrics. If it fails, it goes back to generator with feedback.
#
# This script demonstrates a clean Orchestrator-Worker pattern implementation in LangGraph.

from typing import TypedDict
from langgraph.graph import StateGraph, START, END

# 1. Define the Graph State
class OrchestratorState(TypedDict):
    original_request: str
    subtasks: list[str]
    worker_results: dict[str, str]
    consolidated_response: str

# 2. Define the Nodes
def orchestrator_node(state: OrchestratorState) -> dict:
    print("Executing: orchestrator_node")
    request = state.get("original_request", "")
    
    # In a real app, an LLM parses the request and breaks it into subtasks.
    # We simulate this behavior:
    subtasks = ["Translate to French", "Capitalize response"]
    print(f"Orchestrator split task into: {subtasks}")
    return {"subtasks": subtasks, "worker_results": {}}

def translator_worker(state: OrchestratorState) -> dict:
    print("Executing: translator_worker")
    req = state.get("original_request", "")
    # Simulation: Simple translation
    translated = f"[FRENCH]: Bonjour tout le monde ({req})"
    results = state.get("worker_results", {})
    results["translation"] = translated
    return {"worker_results": results}

def capitalizer_worker(state: OrchestratorState) -> dict:
    print("Executing: capitalizer_worker")
    req = state.get("original_request", "")
    # Simulation: Capitalizing text
    capitalized = f"[CAPITALS]: {req.upper()}"
    results = state.get("worker_results", {})
    results["capitalizer"] = capitalized
    return {"worker_results": results}

def synthesizer_node(state: OrchestratorState) -> dict:
    print("Executing: synthesizer_node")
    results = state.get("worker_results", {})
    translation = results.get("translation", "")
    capitals = results.get("capitalizer", "")
    
    # Consolidate results
    report = f"Consolidated Output:\n- {translation}\n- {capitals}"
    return {"consolidated_response": report}

def build_orchestration_graph():
    print("--- 6. BUILDING ORCHESTRATOR GRAPH ---")
    builder = StateGraph(OrchestratorState)
    
    # Add nodes
    builder.add_node("orchestrator", orchestrator_node)
    builder.add_node("translator", translator_worker)
    builder.add_node("capitalizer", capitalizer_worker)
    builder.add_node("synthesizer", synthesizer_node)
    
    # Paths
    builder.add_edge(START, "orchestrator")
    
    # The orchestrator runs, then we execute BOTH workers in parallel
    builder.add_edge("orchestrator", "translator")
    builder.add_edge("orchestrator", "capitalizer")
    
    # Once BOTH parallel workers finish, route their outputs to the synthesizer node
    # LangGraph automatically waits for all incoming branches to complete before running a node
    builder.add_edge("translator", "synthesizer")
    builder.add_edge("capitalizer", "synthesizer")
    
    builder.add_edge("synthesizer", END)
    
    return builder.compile()

if __name__ == "__main__":
    graph = build_orchestration_graph()
    
    test_input = {"original_request": "hello world"}
    print(f"\nUser Request: {test_input}")
    
    result = graph.invoke(test_input)
    print("\n" + result["consolidated_response"])

# ==========================================================
# REAL-LIFE USE CASES
# ==========================================================
# 1. SOFTWARE DEVELOPMENT AGENT: Orchestrator breaks issue description down. Worker A writes code,
#    Worker B writes unit tests, Worker C reviews security, and Synthesizer compiles the PR.
# 2. TRAVEL ASSISTANT: Orchestrator breaks down travel query. Worker A searches flights, Worker B searches
#    hotels, Worker C searches local events. Synthesizer merges them into a clean travel itinerary.

# ==========================================================
# MNC INTERVIEW QUESTIONS & ANSWERS
# ==========================================================
# Q1. What is the Orchestrator-Worker pattern and when is it preferred?
# A:  It is a multi-agent architectural pattern where a supervisor/orchestrator agent decomposes a large
#     task into independent sub-tasks, delegates them to specialized workers, and aggregates results.
#     It is preferred over single-agent systems for complex tasks to increase reliability, allow parallel
#     execution, and limit prompt degradation.
#
# Q2. How does LangGraph handle parallel task execution and synchronization (fan-out/fan-in)?
# A:  By linking one source node to multiple target nodes (fan-out), LangGraph executes those branches.
#     By drawing edges from multiple nodes into a single target node (fan-in), LangGraph automatically
#     waits until all incoming predecessor nodes have completed execution before running the target node.
