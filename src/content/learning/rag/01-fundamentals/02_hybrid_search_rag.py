# =====================================================================
# RAG STUDY GUIDE: 02. HYBRID RETRIEVAL (DENSE VS SPARSE SEARCH)
# =====================================================================
#
# INTRODUCTION & PURPOSE
# ----------------------
# Modern search systems cannot rely on vector similarity alone. While vector 
# databases are excellent at capturing general meaning and synonym mappings, 
# they perform poorly when looking for exact keywords, serial codes, or specific 
# product names.
#
# Hybrid search solves this by combining:
#   1. Dense Semantic Retrieval (Vector embeddings)
#   2. Sparse Lexical Retrieval (BM25 keyword matching)
#
# This script details the mechanics of merging both search results using the 
# industry-standard Reciprocal Rank Fusion (RRF) algorithm.
#
# =====================================================================
#                       THEORETICAL CORE CONCEPTS
# =====================================================================
#
# 1. DENSE SEMANTIC RETRIEVAL
#    - Dense vectors represent the "concepts" behind sentences. Words are converted
#      to multi-dimensional coordinates (e.g. 1536 float arrays).
#    - Strengths: Understands context and synonyms (e.g. "API key" matches "token").
#    - Weaknesses: Struggles with alphanumeric IDs, names, or exact search strings.
#
# 2. SPARSE LEXICAL RETRIEVAL (BM25)
#    - Sparse vectors (like BM25) count token frequency and inverse document frequency.
#    - Strengths: Extremely precise for exact keywords, acronyms, and codes.
#    - Weaknesses: Blind to vocabulary mismatches (cannot map "automobile" to "car").
#
# 3. RECIPROCAL RANK FUSION (RRF)
#    - We cannot simply add Vector similarity scores (cosine/dot product) to BM25 scores.
#      They are on completely different scales.
#    - RRF assigns a score based strictly on the rank (position) of a document in 
#      each list.
#    - Formula:
#                 RRF_Score(d) =  Sum ( 1 / ( k + Rank_in_System(d) ) )
#
#      Where 'k' is a constant (typically 60) that prevents top ranks from dominating.
#
# =====================================================================
#                     ARCHITECTURAL PIPELINE FLOW
# =====================================================================
#
#                   ┌───► Dense Vector Search (Pinecone) ──► Rank [doc1, doc2, doc3]
#                   │                                                      │
#  [User Query] ────┤                                                      ├──► RRF FUSION ──► [Final Top K Chunks]
#                   │                                                      │
#                   └───► Sparse Lexical Search (BM25)    ──► Rank [doc3, doc1, doc4]
#
# =====================================================================

from typing import List, Dict

# =====================================================================
# MOCKED RETRIEVAL OUTPUTS (For In-Memory Study Study)
# =====================================================================

# Simulated matches from Vector Database (Dense Search)
# Note how semantic database scores range from 0.0 to 1.0 (cosine scale)
DENSE_SEARCH_RESULTS = [
    {"id": "doc1", "text": "LangGraph is a framework for stateful agent orchestration.", "score": 0.89},
    {"id": "doc2", "text": "LlamaIndex is optimized for document ingestion and retrieval.", "score": 0.81},
    {"id": "doc3", "text": "Pinecone is a managed serverless vector database.", "score": 0.76}
]

# Simulated matches from BM25 Keyword Search Engine (Sparse Search)
# Note that BM25 scores do not have an upper bound, making direct summing impossible
SPARSE_SEARCH_RESULTS = [
    {"id": "doc3", "text": "Pinecone is a managed serverless vector database.", "score": 14.52},
    {"id": "doc1", "text": "LangGraph is a framework for stateful agent orchestration.", "score": 12.18},
    {"id": "doc4", "text": "LangChain provides components to build LLM applications.", "score": 9.43}
]

# =====================================================================
# FUSION IMPLEMENTATION
# =====================================================================

def reciprocal_rank_fusion(
    dense_list: List[Dict], 
    sparse_list: List[Dict], 
    k: int = 60
) -> List[Dict]:
    """
    Combines the results of dense semantic search and sparse lexical search using 
    Reciprocal Rank Fusion (RRF).
    
    Parameters:
      dense_list  : Ranked list of search matches from the vector database.
      sparse_list : Ranked list of search matches from the BM25 lexical engine.
      k           : Constant smoothing parameter (standard defaults to 60).
    """
    rrf_scores = {}
    doc_map = {}
    
    # Process Dense Search results
    # enumerate gives us the rank (index starting at 0, representing 1st, 2nd, etc.)
    for rank, doc in enumerate(dense_list):
        doc_id = doc["id"]
        doc_map[doc_id] = doc["text"]
        
        # Calculate rank reciprocal score: 1 / (k + rank)
        rank_score = 1.0 / (k + rank)
        rrf_scores[doc_id] = rrf_scores.get(doc_id, 0.0) + rank_score
        print(f"  Dense Stream: {doc_id} ranked #{rank+1} -> Added {rank_score:.6f} to RRF score.")
        
    # Process Sparse Search results
    for rank, doc in enumerate(sparse_list):
        doc_id = doc["id"]
        doc_map[doc_id] = doc["text"]
        
        rank_score = 1.0 / (k + rank)
        rrf_scores[doc_id] = rrf_scores.get(doc_id, 0.0) + rank_score
        print(f"  Sparse Stream: {doc_id} ranked #{rank+1} -> Added {rank_score:.6f} to RRF score.")
        
    # Sort documents by their final aggregated RRF score (highest to lowest)
    sorted_docs = sorted(rrf_scores.items(), key=lambda item: item[1], reverse=True)
    
    fused_results = []
    for doc_id, score in sorted_docs:
        fused_results.append({
            "id": doc_id,
            "text": doc_map[doc_id],
            "rrf_score": score
        })
        
    return fused_results


# =====================================================================
# EXECUTION ENTRY POINT
# =====================================================================

if __name__ == "__main__":
    print("="*70)
    print("STEP 1: DISPLAYING INDEPENDENT SEARCH INPUTS")
    print("="*70)
    
    print("\nDense Vector Results (Synonym-Aware):")
    for rank, item in enumerate(DENSE_SEARCH_RESULTS, 1):
        print(f"  Rank {rank}: [{item['id']}] (Vector Score: {item['score']}) -> '{item['text']}'")
        
    print("\nSparse BM25 Results (Keyword-Exact):")
    for rank, item in enumerate(SPARSE_SEARCH_RESULTS, 1):
        print(f"  Rank {rank}: [{item['id']}] (BM25 Score: {item['score']}) -> '{item['text']}'")
        
    print("\n" + "="*70)
    print("STEP 2: RUNNING RECIPROCAL RANK FUSION (RRF)")
    print("="*70)
    
    fused_outputs = reciprocal_rank_fusion(DENSE_SEARCH_RESULTS, SPARSE_SEARCH_RESULTS)
    
    print("\n" + "="*70)
    print("FINAL HYBRID RETRIEVAL RESULTS (RRF Sorted)")
    print("="*70)
    for rank, item in enumerate(fused_outputs, 1):
        print(f"  Rank {rank}: [{item['id']}] (RRF Score: {item['rrf_score']:.6f})")
        print(f"    Text: {item['text']}")
        print("-" * 50)

# =====================================================================
# REAL-LIFE USE CASES
# =====================================================================
# 1. SEARCHING PRODUCT MANUALS:
#    - User queries: "How to fix error code E-102".
#    - Vector Search: Retrieves general maintenance and debugging pages.
#    - BM25 Search: Finds the exact manual page mentioning the ID "E-102".
#    - RRF Fusion: Places the exact page mentioning "E-102" at Rank 1.
#
# 2. LEGAL / COMPLIANCE QUERYING:
#    - User queries: "anti-bribery act compliance parameters".
#    - Vector Search matches conceptual synonyms (compliance standards, ethics policy).
#    - BM25 matches the exact legislative act title. Hybrid retrieval merges them.

# =====================================================================
# MNC INTERVIEW PREPARATION
# =====================================================================
# Q1. Why is Reciprocal Rank Fusion (RRF) preferred over normalized score summation?
# A:  - Scores in dense and sparse search cannot be summed directly. Dense retrieval scores 
#       lie between 0.0 and 1.0 (cosine bounds), whereas BM25 scores can grow infinitely (>0.0).
#     - RRF uses rank index as the common denominator, eliminating the need to normalize and
#       distort raw scores from completely different mathematical systems.
#
# Q2. What happens if you change the value of the constant 'k' in the RRF formula?
# A:  - Low 'k' (e.g., k=10): Gives massive weights to top-ranked documents. If a document is
#       Rank 1 in just one stream, it wins, regardless of performance in other streams.
#     - High 'k' (e.g., k=120): Smooths out the score distribution, rewarding items that appear 
#       consistently across both dense and sparse streams even if they are not at Rank 1.
