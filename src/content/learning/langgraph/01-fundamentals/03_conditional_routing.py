# ========================================================================================
# LANGGRAPH CRASH COURSE — MODULE 03: CONDITIONAL ROUTING & DYNAMIC EDGE FUNCTIONS
# ========================================================================================
#
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# SECTION 1 — FIXED EDGES VS CONDITIONAL EDGES
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#
# FIXED EDGE: Always routes to the same next node.
#   builder.add_edge("step_a", "step_b")   → step_a always goes to step_b
#   Use for: deterministic sequential pipelines (prompt chaining, RAG)
#
# CONDITIONAL EDGE: Routes dynamically based on current State values.
#   builder.add_conditional_edges("classifier", router_fn, {"key_a": "node_a", ...})
#   Use for: branching agents, approval flows, ReAct loops, category-based routing
#
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# SECTION 2 — HOW add_conditional_edges() WORKS
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#
# SIGNATURE:
#   builder.add_conditional_edges(
#       source,       # str: name of the node that this edge originates from
#       path,         # callable: function that inspects State and returns a string key
#       path_map      # dict: maps those string keys to target node names
#   )
#
# EXAMPLE:
#   def router(state) -> str:
#       if state["sentiment"] == "positive": return "go_happy"
#       if state["sentiment"] == "negative": return "go_sad"
#       return "go_end"
#
#   builder.add_conditional_edges(
#       "classifier",
#       router,
#       {
#           "go_happy": "happy_responder",   # maps key → node name
#           "go_sad":   "sad_responder",
#           "go_end":   END
#       }
#   )
#
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# SECTION 3 — ROUTING ARCHITECTURE DIAGRAM
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#
#                     START
#                       │
#                       ▼
#               ┌───────────────┐
#               │  classifier   │  (analyze_sentiment node)
#               └───────────────┘
#                       │
#              router(state) returns...
#                       │
#       ┌───────────────┼───────────────┐
#       │ "go_happy"    │ "go_sad"      │ "go_end"
#       ▼               ▼               ▼
# ┌──────────┐   ┌──────────┐       ┌─────┐
# │ happy_   │   │  sad_    │       │ END │
# │responder │   │responder │       └─────┘
# └──────────┘   └──────────┘
#       │                │
#       └───────┬────────┘
#               ▼
#             END
#
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# SECTION 4 — LLM-BASED ROUTING (INTELLIGENT ROUTING)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#
# In production, routers are often LLM-based, not rule-based.
# The classifier node calls the model with a structured output schema and returns
# a category that drives conditional routing.
#
# Example: Support Ticket Router
#   Model classifies: "billing", "technical", "general"
#   Conditional edge routes each category to a specialized handler agent.
#
# ========================================================================================

from typing import TypedDict
from langgraph.graph import StateGraph, START, END


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# STATE DEFINITION
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

class RoutingState(TypedDict):
    user_input: str
    sentiment:  str   # "positive" | "negative" | "neutral"
    reply:      str


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# NODE FUNCTIONS
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def analyze_sentiment(state: RoutingState) -> dict:
    """
    Classifier Node: Determines the sentiment of the user's input.

    In production: Replace keyword matching with:
      model.with_structured_output(SentimentSchema).invoke(text)
    for LLM-powered classification that handles nuance and sarcasm.
    """
    print("  [Node] analyze_sentiment executing...")
    text = state.get("user_input", "").lower()

    positive_words = ["great", "happy", "love", "good", "amazing", "excellent"]
    negative_words = ["bad",   "sad",   "angry", "hate", "terrible", "awful"]

    if any(w in text for w in positive_words):
        sentiment = "positive"
    elif any(w in text for w in negative_words):
        sentiment = "negative"
    else:
        sentiment = "neutral"

    print(f"  [Node] Detected sentiment: '{sentiment}'")
    return {"sentiment": sentiment}


def enthusiastic_reply(state: RoutingState) -> dict:
    """Response node for positive sentiment."""
    print("  [Node] enthusiastic_reply executing...")
    return {"reply": "Awesome! I'm so thrilled to hear that! Keep smiling! 😊"}


def apologetic_reply(state: RoutingState) -> dict:
    """Response node for negative sentiment."""
    print("  [Node] apologetic_reply executing...")
    return {"reply": "I'm so sorry to hear that. I hope things get better soon! ❤️"}


def neutral_reply(state: RoutingState) -> dict:
    """Response node for neutral sentiment."""
    print("  [Node] neutral_reply executing...")
    return {"reply": f"Thanks for sharing. You said: '{state.get('user_input', '')}'"}


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# ROUTER FUNCTION
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def sentiment_router(state: RoutingState) -> str:
    """
    Router: Reads the 'sentiment' key from State set by analyze_sentiment
    and returns a routing key string that maps to a target node.

    This function is passed to add_conditional_edges() as the `path` argument.
    """
    sentiment = state.get("sentiment", "neutral")
    if sentiment == "positive": return "go_happy"
    if sentiment == "negative": return "go_sad"
    return "go_neutral"


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# GRAPH CONSTRUCTION
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def build_routing_graph():
    print("\n" + "="*70)
    print("BUILDING CONDITIONAL ROUTING GRAPH")
    print("="*70)

    builder = StateGraph(RoutingState)

    # Register all nodes
    builder.add_node("classifier",      analyze_sentiment)
    builder.add_node("happy_responder", enthusiastic_reply)
    builder.add_node("sad_responder",   apologetic_reply)
    builder.add_node("neutral_handler", neutral_reply)

    # Entry edge
    builder.add_edge(START, "classifier")

    # Conditional edge — after classifier runs, route based on sentiment
    builder.add_conditional_edges(
        "classifier",       # source node
        sentiment_router,   # routing function (returns string key)
        {
            "go_happy":   "happy_responder",
            "go_sad":     "sad_responder",
            "go_neutral": "neutral_handler"
        }
    )

    # All responders terminate at END
    builder.add_edge("happy_responder", END)
    builder.add_edge("sad_responder",   END)
    builder.add_edge("neutral_handler", END)

    return builder.compile()


if __name__ == "__main__":
    graph = build_routing_graph()

    test_cases = [
        "I had a great day today!",           # → positive → happy_responder
        "This is a terrible experience.",      # → negative → sad_responder
        "The report is ready for review.",     # → neutral  → neutral_handler
    ]

    for i, text in enumerate(test_cases, 1):
        print(f"\n{'='*70}")
        print(f"TEST {i}: '{text}'")
        print("="*70)
        result = graph.invoke({"user_input": text})
        print(f"  Sentiment : {result.get('sentiment')}")
        print(f"  Reply     : {result.get('reply')}")


# ========================================================================================
# REAL-WORLD USE CASES
# ========================================================================================
#
# 1. SUPPORT TICKET ROUTING:
#    - **Node 1**: Classifier node calls model to tag ticket category.
#    - **Routing**: Routes ticket to billing_agent, technical_agent, or account_agent.
#    - **Result**: Selects specialized agent with Stripe API or Jira access.
#
# 2. FRAUD DETECTION PIPELINE:
#    - **Node 1**: Risk scorer node outputs high_risk, medium_risk, or low_risk.
#    - **Routing**: High-risk routes to block node; medium-risk routes to human review.
#    - **Result**: Blocks fraudulent operations while clearing low-risk transactions.
#
# 3. HEALTHCARE TRIAGE BOT:
#    - **Input**: User describes severe symptoms.
#    - **Routing**: Routes severe cases to emergency alert node, bypassing the LLM.
#    - **Result**: Dispatches immediate advice to call emergency services.
#
# ========================================================================================
# MNC INTERVIEW QUESTIONS & ANSWERS
# ========================================================================================
#
# Q1. What are the three required arguments of `add_conditional_edges()`?
# A:  - `source`: The name string of the node from which this conditional edge originates.
#     - `path`: A callable (router function) that takes the current State as input and
#       returns a string key.
#     - `path_map`: A dictionary mapping the returned string keys to target node names
#       (or END). LangGraph uses this mapping to determine the next node.
#
# Q2. Can a routing function make LLM API calls?
# A:  Yes. The router function is a plain Python function. You can call any LLM or
#     external API inside it. However, for performance-critical routing, prefer
#     using a classifier node to set a state key, then read that key in a lightweight
#     string-comparison router — separating classification (heavy) from routing (fast).
#
# Q3. Can a conditional edge route to more than two nodes?
# A:  Yes — there is no limit on path_map entries. You can route to as many nodes as
#     your business logic requires. For example, a support router might have 8 categories:
#     billing, technical, shipping, account, general, spam, escalation, feedback.
