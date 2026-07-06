# =====================================================================
# RAG STUDY GUIDE: 04. CORRECTIVE RAG (CRAG) AGENTIC ARCHITECTURE
# =====================================================================
#
# INTRODUCTION & PURPOSE
# ----------------------
# Traditional RAG pipelines blindly fetch documents and feed them to the LLM. 
# This is a passive RAG model: if the retriever returns irrelevant context, 
# the LLM will hallucinate.
#
# Corrective RAG (CRAG) is an agentic, active RAG architecture. It introduces:
#   1. Query Rewriter: Evaluates and refines the search query.
#   2. Relevance Grader: Inspects each retrieved document and filters out noise.
#   3. Web Search Fallback: If retrieved documents are missing or fail relevance
#      checks, it automatically executes an external web search to correct the
#      missing context.
#
# This script implements the complete CRAG flow in LangGraph for study.
#
# =====================================================================
#                       THEORETICAL CORE CONCEPTS
# =====================================================================
#
# 1. RETRIEVAL ERROR CORRECTION
#    - When documents are retrieved, we run a fast binary classifier (Grader LLM) 
#      asking: "Is this document relevant to this query?"
#    - If yes, we keep it. If no, we discard it.
#    - If our relevant document list becomes empty or drops below a threshold,
#      the system dynamically triggers a "fallback" node to call Search APIs.
#
# 2. QUERY REWRITING
#    - Conversational queries (e.g. "Hey can you tell me what the core framework is?")
#      perform poorly in semantic search.
#    - The Query Rewriter reformulates the prompt into keyword-centric terms
#      (e.g., "core framework") to improve vector matching index accuracy.
#
# =====================================================================
#                     ARCHITECTURAL GRAPH BLUEPRINT
# =====================================================================
#
#           [START]
#              │
#              ▼
#       [Query Rewriter]
#              │
#              ▼
#      [Document Retriever]
#              │
#              ▼
#      [Relevance Grader]  ──────► (Conditional Route)
#              │                            │
#              │ (All Relevant)             │ (Any Irrelevant/Empty)
#              ▼                            ▼
#              │                    [Web Search Fallback]
#              │                            │
#              │                            ▼
#              └────────► [Generator] ◄─────┘
#                             │
#                             ▼
#                           [END]
#
# =====================================================================

from typing import TypedDict, List
from langgraph.graph import StateGraph, START, END

# =====================================================================
# STEP 1: DEFINE GRAPH STATE
# =====================================================================
# The state represents the shared database passed between our graph nodes.

class CRAGState(TypedDict):
    question: str              # The original user question
    rewritten_query: str       # The search-optimized query string
    documents: List[str]       # Accumulated context documents
    run_web_search: bool       # Flag indicating if we need to fall back to web search
    generation: str            # The final synthesized output from the LLM

# =====================================================================
# STEP 2: DEFINE NODES (The Workers)
# =====================================================================

def query_rewriter(state: CRAGState) -> dict:
    """
    LLM Node: Simplifies and reformulates the user prompt for search.
    """
    print("\n[Node 1] Executing: query_rewriter")
    original = state["question"]
    
    # Simulation: LLM removes conversational filler
    rewritten = original.replace("tell me about the", "").strip().lower()
    
    print(f"  -> Original Query: '{original}'")
    print(f"  -> Rewritten Query: '{rewritten}'")
    return {"rewritten_query": rewritten}


def document_retriever(state: CRAGState) -> dict:
    """
    Retrieval Node: Fetches matching passages from our index.
    """
    print("\n[Node 2] Executing: document_retriever")
    query = state["rewritten_query"]
    
    # Simulation: We retrieve documents only if the query matches our indexed topic
    if "quantum computing" in query:
        docs = ["Quantum computing uses qubits to perform calculations."]
    else:
        # If looking for weather or other off-topic info, the index returns nothing
        docs = []
        
    print(f"  -> Retrieved {len(docs)} documents from Pinecone.")
    return {"documents": docs}


def relevance_grader(state: CRAGState) -> dict:
    """
    Evaluation Node: Inspects retrieved documents for query relevance.
    If context is empty, sets run_web_search=True.
    """
    print("\n[Node 3] Executing: relevance_grader")
    docs = state["documents"]
    
    if not docs:
        print("  -> Grader: No documents found in database. Search fallback triggered.")
        return {"run_web_search": True}
        
    # Simulate grading documents
    # In a real app, an LLM checks if the chunk answers the question.
    print("  -> Grader: Context verified as relevant.")
    return {"run_web_search": False}


def web_search_node(state: CRAGState) -> dict:
    """
    Fallback Node: Queries web search API (Tavily/SerpAPI) when index is lacking.
    """
    print("\n[Node 4] Executing: web_search_node")
    query = state["rewritten_query"]
    
    # Simulation: Mock web search response
    web_result = f"Web result for '{query}': Current live data retrieved from search API."
    
    # Append web results to our document list
    docs = state["documents"] + [web_result]
    print(f"  -> Web search retrieved context: '{web_result}'")
    return {"documents": docs}


def generator_node(state: CRAGState) -> dict:
    """
    Synthesis Node: Generates the final answer using the collected context.
    """
    print("\n[Node 5] Executing: generator_node")
    docs = state["documents"]
    
    context = "\n".join(docs)
    
    # Generate final answer based on accumulated contexts
    reply = f"Generated Response:\nBased on the retrieved context [{context}], here is your answer."
    return {"generation": reply}


# =====================================================================
# STEP 3: CONSTRUCT THE STATE GRAPH
# =====================================================================

def build_crag_graph():
    builder = StateGraph(CRAGState)
    
    # 1. Register nodes
    builder.add_node("rewriter", query_rewriter)
    builder.add_node("retriever", document_retriever)
    builder.add_node("grader", relevance_grader)
    builder.add_node("web_search", web_search_node)
    builder.add_node("generator", generator_node)
    
    # 2. Establish connections
    builder.add_edge(START, "rewriter")
    builder.add_edge("rewriter", "retriever")
    builder.add_edge("retriever", "grader")
    
    # 3. Define Conditional Router Edge after the Grader
    def decide_routing(state: CRAGState) -> str:
        if state.get("run_web_search", False):
            print("  [Routing Choice] -> Go to web_search fallback node")
            return "web"
        print("  [Routing Choice] -> Go directly to generator node")
        return "gen"
        
    builder.add_conditional_edges(
        "grader",
        decide_routing,
        {
            "web": "web_search",
            "gen": "generator"
        }
    )
    
    builder.add_edge("web_search", "generator")
    builder.add_edge("generator", END)
    
    return builder.compile()


# =====================================================================
# EXECUTION ENTRY POINT
# =====================================================================

if __name__ == "__main__":
    graph = build_crag_graph()
    
    print("\n" + "="*70)
    print("SCENARIO 1: HIT VECTOR DATABASE (In-Scope Question)")
    print("="*70)
    res1 = graph.invoke({"question": "Tell me about the Quantum Computing"})
    print(f"\nFinal State Reply:\n{res1['generation']}")
    
    print("\n" + "="*70)
    print("SCENARIO 2: OUT-OF-SCOPE / EMPTY DB (Fallback to Search)")
    print("="*70)
    res2 = graph.invoke({"question": "Tell me about the weather in Seattle"})
    print(f"\nFinal State Reply:\n{res2['generation']}")

# =====================================================================
# REAL-LIFE USE CASES
# =====================================================================
# 1. ENTERPRISE CUSTOMER CHATBOTS: When answering product queries, checks internal manuals (vector DB).
#    If the query asks about a brand-new release, the grader triggers web search to pull fresh specs.
# 2. MEDICAL ADVISORY CO-PILOTS: Evaluates medical references. If database queries return old or irrelevant
#    medical papers, routes the search out to PubMed/Web APIs to query the latest guidelines.

# =====================================================================
# MNC INTERVIEW PREPARATION
# =====================================================================
# Q1. Why is a relevance grading node introduced in Corrective RAG (CRAG)?
# A:  - In standard RAG, the vector store returns the top K matches even if they are irrelevant 
#       (e.g., if index lacks the topic, it returns the closest unrelated page).
#     - CRAG uses a grader node to assess and prune these chunks, preventing irrelevant texts from
#       contaminating the LLM context, which eliminates noise-based hallucinations.
#
# Q2. How does CRAG handle the performance tradeoff of query rewriting?
# A:  - Query rewriting adds a small LLM invocation latency to the pipeline start.
#     - However, it dramatically reduces search search index misses and retrieves highly precise 
#       chunks, saving overall costs and reducing LLM generation failures.
