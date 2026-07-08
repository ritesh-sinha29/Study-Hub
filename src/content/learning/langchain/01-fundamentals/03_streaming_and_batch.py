# ========================================================================================
# LANGCHAIN CRASH COURSE — MODULE 03: TOKEN STREAMING & CONCURRENT BATCH PROCESSING
# ========================================================================================
#
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# SECTION 1 — THE PROBLEM WITH WAITING
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#
# When you call `.invoke()`, your application blocks and waits for the full LLM
# response to arrive before doing anything. For a 3-second response, your UI
# shows nothing for 3 seconds — terrible UX.
#
# SOLUTION — Streaming: The model generates text token-by-token. LangChain's
# `.stream()` lets you read and display each token as it arrives.
#
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# SECTION 2 — HOW TOKEN STREAMING WORKS
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#
# Under the hood:
#   1. LangChain opens a persistent HTTP connection (Server-Sent Events or chunked).
#   2. The model generates one token at a time (e.g. "The", " capital", " of").
#   3. Each token is returned as an `AIMessageChunk` object.
#   4. The `chunk.content` attribute holds the string fragment.
#   5. You print/yield the chunk immediately — users see text appearing live.
#
# STREAMING PIPELINE:
#
#  [Prompt] ──► [ChatModel.stream()] ──► token "The" → print
#                                    ──► token " weather" → print
#                                    ──► token " in" → print
#                                    ──► token " New York" → print ...
#
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# SECTION 3 — CONCURRENT BATCH PROCESSING
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#
# SEQUENTIAL PROCESSING (SLOW):
#   Request 1 ──► wait 2s ──► Result 1
#   Request 2 ──► wait 2s ──► Result 2     Total = 6 seconds for 3 requests
#   Request 3 ──► wait 2s ──► Result 3
#
# CONCURRENT BATCH PROCESSING (FAST):
#   Request 1 ──► wait 2s ──► Result 1
#   Request 2 ──► wait 2s ──► Result 2     Total = ~2 seconds for 3 requests
#   Request 3 ──► wait 2s ──► Result 3
#   (All sent simultaneously, results collected together)
#
# `.batch()` uses Python's ThreadPoolExecutor to fire all requests concurrently.
# For async codebases, use `.abatch()` which uses asyncio.gather instead.
#
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# SECTION 4 — AISTREAMCHUNK vs AIMESSAGE
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#
#  AIMessage (from .invoke())
#  └── .content       = "The weather in London is rainy and cold today."
#  └── .response_metadata = {"token_usage": {"total_tokens": 25}, ...}
#
#  AIMessageChunk (from .stream())
#  └── .content       = "The" (or " weather", or " in", etc.)
#  └── Chunks can be merged: chunk1 + chunk2 + ... = full AIMessage
#
# ========================================================================================

import os
from dotenv import load_dotenv

# Load API keys
load_dotenv()

from langchain.chat_models import init_chat_model


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# EXAMPLE 1: TOKEN-BY-TOKEN STREAMING
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def demonstrate_streaming(model):
    print("\n" + "="*70)
    print("EXAMPLE 1: TOKEN-BY-TOKEN STREAMING RESPONSE")
    print("="*70)

    query = "Describe the science of rainbows in three vivid sentences."
    print(f"Query: '{query}'")
    print("\nStreaming response (tokens appear as they arrive):")
    print("-" * 50)

    try:
        # .stream() returns a generator. Each iteration yields one AIMessageChunk.
        chunks = model.stream(query)

        full_response = ""
        for chunk in chunks:
            # chunk.content holds the token fragment string
            token = chunk.content
            print(token, end="", flush=True)  # flush=True forces immediate terminal output
            full_response += token

        print("\n" + "-" * 50)
        print(f"\nTotal characters received: {len(full_response)}")
    except Exception as e:
        print(f"\n  [ERROR] Streaming failed: {e}")


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# EXAMPLE 2: CONCURRENT BATCH PROCESSING
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def demonstrate_batch_processing(model):
    print("\n" + "="*70)
    print("EXAMPLE 2: CONCURRENT BATCH PROCESSING")
    print("="*70)

    # 5 independent questions to run concurrently
    queries = [
        "What is the capital of France?",
        "What is the capital of Japan?",
        "What is the capital of Brazil?",
        "What is the capital of Australia?",
        "What is the capital of Egypt?",
    ]

    print(f"Sending {len(queries)} queries concurrently (not sequentially)...")
    print(f"Queries: {queries}\n")

    try:
        # .batch() sends all requests in parallel threads and collects results
        responses = model.batch(queries)

        print("Batch Results (all collected simultaneously):")
        for i, (query, resp) in enumerate(zip(queries, responses), 1):
            print(f"  {i}. Q: '{query}'")
            print(f"     A: '{resp.content.strip()}'")
    except Exception as e:
        print(f"  [ERROR] Batch processing failed: {e}")


if __name__ == "__main__":
    try:
        model = init_chat_model("gpt-4o-mini", model_provider="openai")
        demonstrate_streaming(model)
        demonstrate_batch_processing(model)
    except Exception as e:
        print("\nSetup failed (check API keys):", e)


# ========================================================================================
# REAL-WORLD USE CASES
# ========================================================================================
#
# 1. CHATBOT UIs (React/Next.js):
#    - **Input**: Frontend calls backend with streaming enabled.
#    - **Step 1**: Yields tokens in real-time from `.stream()` using server-sent events.
#    - **Result**: Frontend appends each token to the chat bubble instantly for a typing effect.
#
# 2. OVERNIGHT CONTENT CLASSIFICATION:
#    - **Input**: Batch of 10,000 customer reviews for sentiment analysis.
#    - **Step 1**: Processes batches of 50 reviews concurrently using `.batch()`.
#    - **Result**: Reduces execution time from 5 hours (sequential) to 6 minutes (concurrent).
#
# 3. PARALLEL REPORT GENERATION:
#    - **Input**: Sales dashboard generating summaries for 20 regions.
#    - **Step 1**: Packages each region's data as a separate batch input.
#    - **Result**: Runs a single `.batch()` call to process all regions simultaneously.
#
# ========================================================================================
# MNC INTERVIEW QUESTIONS & ANSWERS
# ========================================================================================
#
# Q1. How does `.batch()` achieve concurrency internally?
# A:  In synchronous Python, LangChain's `.batch()` uses a `ThreadPoolExecutor`.
#     Each input is dispatched as a separate thread, all making HTTP requests
#     concurrently. In async code, `.abatch()` uses `asyncio.gather()` which is
#     more efficient because it uses a single event loop without OS thread overhead.
#
# Q2. What is the difference between `AIMessage` and `AIMessageChunk`?
# A:  - `AIMessage`: Complete response returned by `.invoke()`. Contains full
#       `.content` string and metadata like `response_metadata` with token counts.
#     - `AIMessageChunk`: Partial fragment returned during `.stream()`. Contains
#       a substring of the final response. Chunks support the `+` operator:
#       `chunk1 + chunk2` accumulates into the final `AIMessage`.
#
# Q3. What is `flush=True` in `print()` and why is it needed for streaming?
# A:  By default, Python's print() buffers output and writes it to the terminal
#     in batches. `flush=True` forces the buffer to be cleared after every print
#     call. Without it, all streaming tokens would appear at once at the end —
#     defeating the purpose of streaming entirely.
