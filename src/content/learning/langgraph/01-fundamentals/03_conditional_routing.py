# ==========================================================
# LANGGRAPH STUDY GUIDE: 03. CONDITIONAL ROUTING
# ==========================================================

# --- CONDITIONAL ROUTING ---
# In many applications, the graph flow cannot be hardcoded. Edges must route execution 
# dynamically to different nodes based on the state.
#
# In LangGraph, this is achieved using `add_conditional_edges()`.
# You provide:
# 1. The source node.
# 2. A routing function that inspects the state and returns a path string (key).
# 3. A mapping dictionary linking routing keys to target nodes.

from typing import TypedDict
from langgraph.graph import StateGraph, START, END

# 1. Define the State Schema
class RoutingState(TypedDict):
    user_input: str
    sentiment: str  # "positive", "negative", "neutral"
    reply: str

# 2. Define the Nodes
def analyze_sentiment(state: RoutingState) -> dict:
    print("Executing: analyze_sentiment")
    text = state.get("user_input", "").lower()
    
    # Simple rule-based classifier for demonstration
    if any(word in text for word in ["great", "happy", "love", "good"]):
        sentiment = "positive"
    elif any(word in text for word in ["bad", "sad", "angry", "hate"]):
        sentiment = "negative"
    else:
        sentiment = "neutral"
        
    return {"sentiment": sentiment}

def enthusiastic_reply(state: RoutingState) -> dict:
    print("Executing: enthusiastic_reply")
    return {"reply": "Awesome! I'm so thrilled to hear that! Keep smiling! 😊"}

def apologetic_reply(state: RoutingState) -> dict:
    print("Executing: apologetic_reply")
    return {"reply": "I'm so sorry to hear that. I hope things get better soon! Hugs! ❤️"}

def build_routing_graph():
    print("--- 3. BUILDING ROUTING GRAPH ---")
    builder = StateGraph(RoutingState)
    
    # Add nodes
    builder.add_node("classifier", analyze_sentiment)
    builder.add_node("happy_responder", enthusiastic_reply)
    builder.add_node("sad_responder", apologetic_reply)
    
    # Connect START to the classifier
    builder.add_edge(START, "classifier")
    
    # 3. Define the Router function
    def router(state: RoutingState) -> str:
        sentiment = state.get("sentiment", "neutral")
        if sentiment == "positive":
            return "go_happy"
        elif sentiment == "negative":
            return "go_sad"
        return "go_end"
        
    # 4. Bind conditional edges to the classifier node
    builder.add_conditional_edges(
        "classifier",
        router,
        {
            "go_happy": "happy_responder",
            "go_sad": "sad_responder",
            "go_end": END
        }
    )
    
    # Connect responders directly to the END
    builder.add_edge("happy_responder", END)
    builder.add_edge("sad_responder", END)
    
    return builder.compile()

if __name__ == "__main__":
    graph = build_routing_graph()
    
    # Test case 1: Positive Sentiment
    print("\n--- Test 1: Positive Sentiment ---")
    res1 = graph.invoke({"user_input": "I had a great day today!"})
    print("Result:", res1)
    
    # Test case 2: Negative Sentiment
    print("\n--- Test 2: Negative Sentiment ---")
    res2 = graph.invoke({"user_input": "This is a bad experience."})
    print("Result:", res2)
    
    # Test case 3: Neutral Sentiment
    print("\n--- Test 3: Neutral Sentiment ---")
    res3 = graph.invoke({"user_input": "The sky is blue."})
    print("Result:", res3)

# ==========================================================
# REAL-LIFE USE CASES
# ==========================================================
# 1. TICKET ROUTING AGENT: Classifies support tickets based on urgency. Urgent issues route to an on-call
#    alert node, while general inquiries route to a database retrieval node.
# 2. FRAUD DETECTION SYSTEM: Analyzes bank transactions. High-risk actions route to a security verification
#    node (blocking execution), while low-risk transactions are approved immediately.

# ==========================================================
# MNC INTERVIEW QUESTIONS & ANSWERS
# ==========================================================
# Q1. What are the arguments needed for `add_conditional_edges` in LangGraph?
# A:  It requires:
#     - `source`: The name of the node from which the routing starts.
#     - `path`: A routing function (callable) that evaluates the state and returns a route key (string).
#     - `path_map`: A dictionary mapping the return values of the routing function to target node names.
#
# Q2. Can a routing function in conditional edges be asynchronous?
# A:  Yes. The routing function can be either synchronous or asynchronous. LangGraph automatically
#     handles async propagation when executing graphs asynchronously.
