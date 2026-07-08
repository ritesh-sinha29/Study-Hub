# =====================================================================
# RAG STUDY GUIDE: 01. TRADITIONAL VS ADVANCED LLAMACLOUD PARSING
# =====================================================================
#
# INTRODUCTION & PURPOSE
# ----------------------
# Retrieving relevant information from raw files (PDFs, Word docs, etc.) is
# the core of Retrieval-Augmented Generation (RAG). However, the quality of
# what an LLM outputs is directly tied to the quality of the text we extract
# and how we slice (chunk) it.
#
# This script is designed as an interactive guide comparing two paradigms:
#   1. Traditional Parsing (Local, Layout-Blind)
#   2. Advanced Layout-Aware Parsing (Cloud-assisted, Structure-Preserving)
#
# =====================================================================
#                       THEORETICAL CORE CONCEPTS
# =====================================================================
#
# 1. THE PARSING PROBLEM
#    - Traditional PDF loaders read a PDF as a single flat string. They do
#      not recognize if a sentence is inside a table, a sidebar, or split
#      across columns. This destroys the spatial context of information.
#    - Layout-Aware Parsers (like LlamaParse/LlamaCloud) convert documents 
#      into clean Markdown. They identify tables, lists, headers, and footers,
#      ensuring formatting (like markdown table grids `|---|---|`) is kept.
#
# 2. CHUNKING STRATEGIES
#    - RecursiveCharacterTextSplitter: Slices text strictly by counting characters
#      and looking for line breaks. If a sentence is 100 characters long and the
#      chunk limit is hit, the sentence is sliced in half.
#    - SentenceSplitter: Slices text by respecting sentence boundaries (e.g. periods,
#      question marks). It ensures that complete thoughts remain intact inside a single
#      retrieval chunk, which prevents the LLM from losing context.
#
# =====================================================================
#                     ARCHITECTURAL PIPELINE FLOW
# =====================================================================
#
#  [Raw PDF File]
#        │
#        ├─► METHOD 1: PyPDFLoader ──► Recursive Splitter ──► [Chunk 1][Chunk 2] (Layout-Blind)
#        │
#        └─► METHOD 2: LlamaCloud  ──► SentenceSplitter   ──► [Chunk 1][Chunk 2] (Layout-Aware)
#
# =====================================================================

import os
import time
from dotenv import load_dotenv

# Load credentials from local .env
load_dotenv()

# --- METHOD 1: TRADITIONAL IMPORTS ---
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

# --- METHOD 2: ADVANCED IMPORTS ---
# LlamaIndex SentenceSplitter respects grammatical boundaries
from llama_index.core.node_parser import SentenceSplitter


# =====================================================================
# STEP-BY-STEP WORKFLOWS
# =====================================================================

def run_traditional_rag_pipeline(file_path: str):
    """
    METHOD 1: Traditional PDF parsing and length-based chunking.
    
    Step 1: Load PDF pages sequentially (blind to columns/tables).
    Step 2: Split text into chunks using character length parameters.
    """
    print("\n" + "="*70)
    print("METHOD 1: TRADITIONAL PDF INGESTION (Local & Layout-Blind)")
    print("="*70)
    
    if not os.path.exists(file_path):
        print(f"[!] File not found: {file_path}")
        return
        
    start_time = time.time()
    
    # --- STEP 1: PARSING ---
    print("[Step 1] Initializing PyPDFLoader and reading PDF locally...")
    loader = PyPDFLoader(file_path)
    try:
        pages = loader.load()
        print(f"  -> Successfully parsed {len(pages)} pages.")
    except Exception as e:
        print(f"  [ERROR] Local PDF parsing failed: {e}")
        return
        
    # --- STEP 2: CHUNKING ---
    # We define a chunk size of 800 characters with 100 character overlap.
    # The overlap ensures that adjacent chunks share context, reducing edge-effects.
    print("[Step 2] Applying RecursiveCharacterTextSplitter chunking...")
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=100
    )
    chunks = splitter.split_documents(pages)
    
    elapsed = time.time() - start_time
    
    print(f"\nResults:")
    print(f"  - Total Pages Loaded: {len(pages)}")
    print(f"  - Total Chunks Generated: {len(chunks)}")
    print(f"  - Ingestion Latency: {elapsed:.2f} seconds")
    
    # Print a sample chunk to inspect formatting
    if chunks:
        print("\n--- SAMPLE CHUNK (Traditional) ---")
        print(chunks[0].page_content[:400] + "\n...")
        print("-" * 35)


def run_llamacloud_rag_pipeline(file_path: str):
    """
    METHOD 2: Layout-aware cloud parsing and sentence-boundary chunking.
    
    Step 1: Send document to LlamaCloud for high-fidelity markdown parsing.
    Step 2: Split markdown text using sentence-aware logic.
    """
    print("\n" + "="*70)
    print("METHOD 2: ADVANCED INGESTION (LlamaCloud & Sentence-Aware)")
    print("="*70)
    
    llama_key = os.environ.get("LLAMA_CLOUD_API_KEY")
    if not llama_key or llama_key == "your_gemini_api_key_here" or "here" in llama_key:
        print("[!] Skipped: LLAMA_CLOUD_API_KEY is not configured in your .env file.")
        print("    Please set a valid key to try Method 2.")
        return
        
    if not os.path.exists(file_path):
        print(f"[!] File not found: {file_path}")
        return
        
    start_time = time.time()
    
    # --- STEP 1: PARSING ---
    print("[Step 1] Sending PDF to LlamaCloud API for layout parsing...")
    try:
        from llama_cloud import LlamaCloud
        client = LlamaCloud(api_key=llama_key)
        
        with open(file_path, "rb") as f:
            parse_result = client.parsing.parse(
                upload_file=f,
                tier="cost_effective",
                version="latest",
                expand=["markdown", "text"]
            )
            
        # Extract the markdown string containing parsed layouts and tables
        text_content = parse_result.markdown_full or parse_result.text_full
        print(f"  -> Successfully extracted {len(text_content)} characters in Markdown.")
    except Exception as e:
        print(f"  [ERROR] LlamaCloud layout parsing failed: {e}")
        return
        
    # --- STEP 2: CHUNKING ---
    # SentenceSplitter respects punctuation and sentence endings.
    print("[Step 2] Applying LlamaIndex SentenceSplitter...")
    splitter = SentenceSplitter(chunk_size=800, chunk_overlap=100)
    chunks = splitter.split_text(text_content)
    
    elapsed = time.time() - start_time
    
    print(f"\nResults:")
    print(f"  - Characters Extracted: {len(text_content)}")
    print(f"  - Total Chunks Generated: {len(chunks)}")
    print(f"  - Ingestion Latency: {elapsed:.2f} seconds")
    
    if chunks:
        print("\n--- SAMPLE CHUNK (Advanced Markdown) ---")
        print(chunks[0][:400] + "\n...")
        print("-" * 35)


# =====================================================================
# EXECUTION ENTRY POINT
# =====================================================================

if __name__ == "__main__":
    # Test path pointing to your client project's PDF
    pdf_path = "C:/Users/Ritesh Sinha/OneDrive/Desktop/Client_Projects/AI_CAPABILITIES_2026/data/AI_Digital_Twin_A_Startup_Blueprint_for_Personalized_Productivity.pdf"
    
    print("Starting Ingestion Parsing & Chunking Comparison Study...")
    
    if os.path.exists(pdf_path):
        run_traditional_rag_pipeline(pdf_path)
        run_llamacloud_rag_pipeline(pdf_path)
    else:
        print(f"\nTo test this comparison, copy a PDF to the following location:")
        print(f"  -> {pdf_path}")
        print("Or update the pdf_path variable inside the script script.")

# =====================================================================
# REAL-LIFE USE CASES & COMPARISONS
# =====================================================================
# 1. SEARCHING FINANCIAL STATEMENTS:
#    - **Step 1**: Traditional parser scrambles columns, yielding mismatched values.
#    - **Step 2**: Advanced LlamaCloud parser preserves tables as markdown_matrices.
#    - **Result**: RAG agent retrieves clean tabular data and outputs accurate figures.
#
# 2. LEGAL CONTRACT REVIEW:
#    - **Step 1**: Traditional parser splits paragraph midpoint, causing chunk_fragmentation.
#    - **Step 2**: Advanced SentenceSplitter parses text in cohesive semantic blocks.
#    - **Result**: Retriever returns complete clauses, improving document match scores.

# =====================================================================
# MNC INTERVIEW PREPARATION
# =====================================================================
# Q1. What is the 'loss of spatial context' during PDF parsing?
# A:  PDF documents store letters with absolute X-Y coordinate placements on a canvas.
#     Standard text loaders extract characters sequentially based on these coordinates,
#     often reading multi-column pages from left-to-right across the whole page, rather 
#     than reading down Column 1 and then down Column 2. This scrambles semantic ordering.
#
# Q2. How does the choice of chunk size affect LLM hallucinations?
# A:  - Large Chunks: Overwhelms the LLMs context window, degrading response precision
#       (the LLM overlooks information hidden in the middle of a massive chunk).
#     - Small Chunks: Splits sentences in half, causing the retriever to return incomplete
#       context fragments that lead to hallucinations due to missing details.
