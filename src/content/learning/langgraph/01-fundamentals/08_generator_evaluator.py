# ==========================================================
# LANGGRAPH STUDY GUIDE: 08. GENERATOR-EVALUATOR LOOP
# ==========================================================

# --- GENERATOR-EVALUATOR PATTERN ---
# The Generator-Evaluator pattern is a loop architecture consisting of:
# 1. Generator Node: Generates content based on current instructions and any past feedback.
# 2. Evaluator Node: Reviews the output against specific criteria (e.g. word count, tone, safety).
#    If the criteria are met, the graph ends.
#    If the criteria are not met, the evaluator adds feedback to the state and routes
#    execution back to the Generator.

from typing import TypedDict
from langgraph.graph import StateGraph, START, END

# 1. Define the State
class LoopState(TypedDict):
    prompt: str
    output: str
    feedback: str
    attempts: int

# 2. Define the Nodes
def generator_node(state: LoopState) -> dict:
    attempts = state.get("attempts", 0) + 1
    feedback = state.get("feedback", "")
    print(f"Executing: generator_node (Attempt #{attempts})")
    
    # Simulation: Generator modifies response based on feedback
    if feedback:
        output = "This is a brief summary of AI." # Generator complies with feedback (makes it shorter)
    else:
        output = "Artificial Intelligence (AI) is a branch of computer science focused on building smart machines capable of performing tasks."
        
    return {"output": output, "attempts": attempts}

def evaluator_node(state: LoopState) -> dict:
    print("Executing: evaluator_node")
    output = state.get("output", "")
    word_count = len(output.split())
    
    # We want a very short summary (less than 10 words)
    if word_count > 10:
        feedback = "The summary is too long. Please rewrite it in under 10 words."
        print(f"Evaluation Failed (Word Count: {word_count}). Sending feedback: {feedback}")
    else:
        feedback = ""
        print(f"Evaluation Passed (Word Count: {word_count}).")
        
    return {"feedback": feedback}

def build_loop_graph():
    print("--- 8. BUILDING GENERATOR-EVALUATOR GRAPH ---")
    builder = StateGraph(LoopState)
    
    # Add nodes
    builder.add_node("generator", generator_node)
    builder.add_node("evaluator", evaluator_node)
    
    # Paths
    builder.add_edge(START, "generator")
    builder.add_edge("generator", "evaluator")
    
    # Define conditional edge for feedback loop
    def check_evaluation(state: LoopState) -> str:
        if state.get("feedback"):
            return "retry"
        return "accept"
        
    builder.add_conditional_edges(
        "evaluator",
        check_evaluation,
        {
            "retry": "generator",
            "accept": END
        }
    )
    
    return builder.compile()

if __name__ == "__main__":
    graph = build_loop_graph()
    
    test_input = {"prompt": "Summarize AI", "feedback": "", "attempts": 0}
    result = graph.invoke(test_input)
    print("\nFinal State Output:")
    print("Final Output:", result["output"])
    print("Total Attempts:", result["attempts"])

# ==========================================================
# REAL-LIFE USE CASES
# ==========================================================
# 1. CODE GENERATOR WITH COMPILER FEEDBACK: Generator writes python code. Evaluator executes it in a sandboxed
#    terminal. If it throws a syntax error, the compiler output is sent back as feedback to fix the code.
# 2. SEO META DESCRIPTION GENERATOR: Generator creates page meta descriptions. Evaluator checks if length is 
#    strictly between 150-160 characters. Loops back with instructions if it falls outside that range.

# ==========================================================
# MNC INTERVIEW QUESTIONS & ANSWERS
# ==========================================================
# Q1. What is the Generator-Evaluator pattern and what problem does it solve?
# A:  It is an agentic pattern where generation and evaluation roles are split. It solves the issue
#     of LLMs failing to follow complex constraints (like exact character limits or code syntax validation)
#     on their first attempt by providing a programmatic verification and correction loop.
#
# Q2. How do you prevent infinite loops in a Generator-Evaluator graph?
# A:  You should store a loop counter (e.g. `attempts`) in the Graph State. The conditional edge routing
#     function should check if `attempts` exceeds a threshold (e.g. 3 attempts) and force-route to END 
#     (or a fallback node) to prevent infinite API calls.
