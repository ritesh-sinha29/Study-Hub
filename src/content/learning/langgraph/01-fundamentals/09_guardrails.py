# ========================================================================================
# GUARDRAILS
# ========================================================================================
#
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# SECTION 1 — GUARDRAILS IN AGENTIC SYSTEMS
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#
# Guardrails enforce safety, compliance, and scope bounds on agent inputs and outputs.
# In LangGraph, guardrails are implemented as specialized nodes that intercept data:
#
# 1. INPUT GUARDRAILS: Runs BEFORE the model. Checks if user query is appropriate and in-scope.
#    If a violation is found, it routes flow directly to a rejection node, bypassing LLM execution.
#
# 2. OUTPUT GUARDRAILS: Runs AFTER the model. Checks if the generated response meets safety 
#    and formatting guidelines before displaying it to the user.
#
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# SECTION 2 — DETAILED GUARDRAIL FLOW
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#
#  User Prompt ────────► [ Input Guardrail ] ───(Unsafe)───► [ Rejection Node ] ───► END
#                             │
#                          (Safe)
#                             ▼
#                       [ Agent Node ]
#                             │
#                             ▼
#                      [ Output Guardrail ] ───(Unsafe)───► [ Blocked Message ] ───► END
#                             │
#                          (Safe)
#                             ▼
#                        Final Output ────────────────────────────────────────────► END
#
# ========================================================================================

from typing import TypedDict
from langgraph.graph import StateGraph, START, END

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# STATE SCHEMA
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

class SafeState(TypedDict):
    user_query: str
    agent_response: str
    is_safe_input: bool
    is_safe_output: bool
    final_output: str

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# NODES
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def input_guardrail_node(state: SafeState) -> dict:
    print("  [Node] input_guardrail_node checking user query...")
    query = state.get("user_query", "").lower()
    
    # Simulation: Check if query contains blocked keywords
    blocked_keywords = ["hack", "password", "bypass", "exploit"]
    is_safe = not any(word in query for word in blocked_keywords)
    
    if not is_safe:
        print("  [Guardrail] WARNING: Input Guardrail Triggered! Blocked content detected.")
        
    return {"is_safe_input": is_safe}

def rejection_node(state: SafeState) -> dict:
    print("  [Node] rejection_node responding...")
    return {"final_output": "I cannot assist you with this request as it violates safety guidelines."}

def agent_node(state: SafeState) -> dict:
    print("  [Node] agent_node generating response...")
    query = state.get("user_query", "")
    response = f"Here is the helpful response about: {query}."
    return {"agent_response": response}

def output_guardrail_node(state: SafeState) -> dict:
    print("  [Node] output_guardrail_node checking agent output...")
    response = state.get("agent_response", "")
    
    # Simulation: Check output safety (e.g. no sensitive data leakage)
    is_safe = "confidential" not in response.lower()
    
    if not is_safe:
        print("  [Guardrail] WARNING: Output Guardrail Triggered! Sensitive information leaked.")
        final_output = "Error: Output blocked due to safety guidelines."
    else:
        final_output = response
        
    return {"is_safe_output": is_safe, "final_output": final_output}

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# GRAPH CONSTRUCTION
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def build_guardrail_graph():
    print("\n" + "="*70)
    print("BUILDING GUARDRAIL GRAPH")
    print("="*70)
    
    builder = StateGraph(SafeState)
    
    builder.add_node("input_guard", input_guardrail_node)
    builder.add_node("agent", agent_node)
    builder.add_node("output_guard", output_guardrail_node)
    builder.add_node("rejection", rejection_node)
    
    # Entry point
    builder.add_edge(START, "input_guard")
    
    # Input router: Go to Agent if safe, otherwise route directly to Rejection
    def route_input(state: SafeState) -> str:
        if state.get("is_safe_input", True):
            return "go_agent"
        return "go_rejection"
        
    builder.add_conditional_edges(
        "input_guard",
        route_input,
        {
            "go_agent": "agent",
            "go_rejection": "rejection"
        }
    )
    
    # If the input was safe and executed by the agent, proceed to the output check
    builder.add_edge("agent", "output_guard")
    
    # Connect leaf nodes to END
    builder.add_edge("output_guard", END)
    builder.add_edge("rejection", END)
    
    return builder.compile()

if __name__ == "__main__":
    graph = build_guardrail_graph()
    
    # Test case 1: Safe Query
    print("\n--- Test 1: Safe Query ---")
    res1 = graph.invoke({"user_query": "How do I plant a tree?"})
    print("  Result:", res1.get("final_output"))
    
    # Test case 2: Unsafe Query (Input Guardrail)
    print("\n--- Test 2: Unsafe Query ---")
    res2 = graph.invoke({"user_query": "How do I hack a database?"})
    print("  Result:", res2.get("final_output"))

# ========================================================================================
# REAL-WORLD USE CASES
# ========================================================================================
#
# 1. ENTERPRISE KNOWLEDGE AGENTS:
#    - **Step 1**: Input guardrail blocks questions about peer salaries.
#    - **Step 2**: Output guardrail validates response contains no private PII.
#    - **Result**: Enforces strict corporate safety boundaries.
#
# 2. HEALTHCARE ADVICE ASSISTANT:
#    - **Concept**: Bypassing model latency for critical safety.
#    - **Step 1**: If the user describes emergency symptoms (e.g. heart attack), the input guardrail instantly detects it.
#    - **Result**: Routes the conversation directly to a warning node advising the user to call emergency services, bypassing LLM processing wait times entirely.
#
# ========================================================================================
# MNC INTERVIEW QUESTIONS & ANSWERS
# ========================================================================================
#
# Q1. Why implement guardrails as separate nodes in LangGraph instead of putting them in system prompts?
# A:  System prompts are prone to prompt-injection exploits and model drift. Separating guardrails into 
#     independent deterministic python execution nodes ensures safety constraints are 100% enforced and 
#     bypasses LLM compute costs when handling malicious or out-of-scope requests.
#
# Q2. What is the difference between input guardrails and output guardrails?
# A:  Input guardrails run before the model to filter out bad prompts, hacking attempts, or off-topic queries.
#     Output guardrails run after the model to inspect generated results, ensuring the LLM didn't hallucinate,
#     reveal confidential info, or generate inappropriate responses.
