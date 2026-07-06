# ========================================================================================
# LANGCHAIN CRASH COURSE — LCEL MODULE 02: RUNNABLE PARALLEL & PASSTHROUGH
# ========================================================================================
#
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# SECTION 1 — WHAT IS RUNNABLE PARALLEL?
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#
# `RunnableParallel` (previously called `Map`) runs multiple independent chains
# concurrently and combines their outputs into a single dictionary.
#
# WHY IS THIS USEFUL?
# When you need multiple independent analyses of the same input, running them
# sequentially wastes time. With RunnableParallel, all branches execute at the
# same time (via thread pools), and you get all results simultaneously.
#
# EXAMPLE WITHOUT PARALLEL (Slow — Sequential):
#   summary  = summary_chain.invoke(text)     # 2 seconds
#   bullets  = bullets_chain.invoke(text)     # 2 seconds
#   keywords = keyword_chain.invoke(text)     # 2 seconds
#   # Total time = 6 seconds
#
# EXAMPLE WITH PARALLEL (Fast — Concurrent):
#   result = RunnableParallel(
#       summary=summary_chain,
#       bullets=bullets_chain,
#       keywords=keyword_chain,
#   ).invoke({"text": text})
#   # Total time = ~2 seconds (slowest branch determines total)
#
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# SECTION 2 — WHAT IS RUNNABLE PASSTHROUGH?
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#
# `RunnablePassthrough` passes its input through unchanged — it's a no-op forwarder.
#
# WHY IS THIS USEFUL?
# When building parallel pipelines, you often want to PRESERVE the original input
# alongside the processed results. RunnablePassthrough acts as a "copy" branch.
#
# WITHOUT PASSTHROUGH — you lose the original input:
#   result = RunnableParallel(summary=summary_chain).invoke(text)
#   result["original"] = ???  ← you've lost the original text!
#
# WITH PASSTHROUGH — original is preserved:
#   result = RunnableParallel(
#       summary=summary_chain,
#       original_text=RunnablePassthrough()   ← copies input straight through
#   ).invoke(text)
#   result["original_text"]  ← original text is still there ✓
#
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# SECTION 3 — ARCHITECTURE DIAGRAM: PARALLEL EXECUTION
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#
#                       ┌──────────────────────────────────────────┐
#                       │         RunnableParallel                  │
#                       │                                          │
#  Input: {"text": ...} ─┼──► [Branch A: summary_chain]  ──────────┼──► result["summary"]
#                       │                                          │
#                       ├──► [Branch B: bullets_chain]  ──────────┼──► result["bullets"]
#                       │                                          │
#                       └──► [Branch C: RunnablePassthrough] ──────┼──► result["original"]
#                                                                  │
#                                         Combined dict output ◄───┘
#
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# SECTION 4 — SHORTHAND DICT SYNTAX (IMPORTANT!)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#
# LangChain automatically converts plain Python dicts into RunnableParallel!
# These two are IDENTICAL:
#
#   # Explicit:
#   RunnableParallel({"summary": summary_chain, "bullets": bullets_chain})
#
#   # Shorthand (dict literal — cleaner, more Pythonic):
#   {"summary": summary_chain, "bullets": bullets_chain}
#
# This shorthand is used everywhere in real LangChain codebases.
#
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# SECTION 5 — RUNNABLE PASSTHROUGH WITH ADDED KEYS
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#
# `RunnablePassthrough.assign(key=runnable)` passes the input through AND adds
# a new key to the dict. This is extremely useful for RAG pipelines:
#
#   chain = RunnablePassthrough.assign(
#       retrieved_docs=retriever            # adds docs to the dict
#   ) | prompt | model | parser
#
# The input dict flows through with "retrieved_docs" appended before hitting the prompt.
#
# ========================================================================================

import os
import time
from dotenv import load_dotenv

# Load API keys
load_dotenv()

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough, RunnableParallel
from langchain.chat_models import init_chat_model


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# EXAMPLE 1: PARALLEL CONTENT ANALYSIS (summary + bullets + passthrough)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def demonstrate_parallel_analysis(model):
    print("\n" + "="*70)
    print("EXAMPLE 1: PARALLEL CONTENT ANALYSIS")
    print("="*70)

    parser = StrOutputParser()

    # Two independent analysis prompts
    summary_prompt = ChatPromptTemplate.from_template(
        "Summarize the following text in exactly ONE sentence:\n\n{text}"
    )
    bullets_prompt = ChatPromptTemplate.from_template(
        "Extract exactly 3 key facts from this text as bullet points:\n\n{text}"
    )
    sentiment_prompt = ChatPromptTemplate.from_template(
        "What is the overall sentiment of this text? Reply in one word (positive/negative/neutral):\n\n{text}"
    )

    # Three independent chains — each analyzes the same input differently
    summary_chain   = summary_prompt  | model | parser
    bullets_chain   = bullets_prompt  | model | parser
    sentiment_chain = sentiment_prompt| model | parser

    # Combine into ONE parallel execution:
    # Branch A: summary_chain
    # Branch B: bullets_chain
    # Branch C: sentiment_chain
    # Branch D: RunnablePassthrough — copies original text straight through
    parallel_pipeline = RunnableParallel(
        summary=summary_chain,
        bullet_points=bullets_chain,
        sentiment=sentiment_chain,
        original_text=RunnablePassthrough()   # preserves the raw input
    )

    article = (
        "Quantum computing is a type of computation that harnesses the collective "
        "properties of quantum states such as superposition and entanglement. "
        "Unlike classical computers which use bits (0 or 1), quantum computers use "
        "qubits, which can exist in multiple states simultaneously, enabling them to "
        "solve certain problems exponentially faster than classical systems."
    )

    print("  Input: Article about quantum computing")
    print("  Running 3 LLM branches concurrently + passthrough...\n")

    try:
        start = time.time()
        result = parallel_pipeline.invoke({"text": article})
        elapsed = time.time() - start

        print(f"  ✓ All branches completed in {elapsed:.2f}s\n")
        print(f"  [PASSTHROUGH] Original text (first 80 chars):")
        print(f"  '{result['original_text']['text'][:80]}...'\n")
        print(f"  [SUMMARY]:")
        print(f"  '{result['summary']}'\n")
        print(f"  [BULLET POINTS]:")
        print(f"  '{result['bullet_points']}'\n")
        print(f"  [SENTIMENT]: '{result['sentiment']}'")

    except Exception as e:
        print(f"  [ERROR]: {e}")


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# EXAMPLE 2: PASSTHROUGH.ASSIGN — RAG-style context injection
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def demonstrate_passthrough_assign(model):
    print("\n" + "="*70)
    print("EXAMPLE 2: RunnablePassthrough.assign() — ADDING KEYS TO DICT")
    print("="*70)

    # Simulate a retriever function (in real RAG this would be a vector store query)
    def mock_retriever(inputs: dict) -> str:
        query = inputs.get("question", "")
        # Pretend we searched a knowledge base
        return f"[Retrieved Context]: LangChain was created by Harrison Chase in 2022 and is now part of LangChain Inc."

    prompt = ChatPromptTemplate.from_messages([
        ("system", "Use the retrieved context to answer the question. Be concise."),
        ("human", "Context: {context}\n\nQuestion: {question}")
    ])
    parser = StrOutputParser()

    # RunnablePassthrough.assign adds 'context' key to the dict
    # before it reaches the prompt — this is the standard RAG chain pattern
    rag_chain = (
        RunnablePassthrough.assign(context=mock_retriever)
        | prompt
        | model
        | parser
    )

    question = "Who created LangChain and when?"
    print(f"  Question: '{question}'")
    print(f"  Running RAG chain with passthrough context injection...\n")

    try:
        result = rag_chain.invoke({"question": question})
        print(f"  Answer: '{result}'")
    except Exception as e:
        print(f"  [ERROR]: {e}")


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# EXAMPLE 3: DICT SHORTHAND — automatic RunnableParallel conversion
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def demonstrate_dict_shorthand(model):
    print("\n" + "="*70)
    print("EXAMPLE 3: DICT SHORTHAND (auto-converts to RunnableParallel)")
    print("="*70)

    parser  = StrOutputParser()
    prompt1 = ChatPromptTemplate.from_template("Translate '{word}' to French.")
    prompt2 = ChatPromptTemplate.from_template("Translate '{word}' to Spanish.")

    # Using dict shorthand — no need to write RunnableParallel() explicitly
    parallel = {
        "french":  prompt1 | model | parser,
        "spanish": prompt2 | model | parser,
    }

    word = "Serendipity"
    print(f"  Word to translate: '{word}'")

    try:
        result = RunnableParallel(parallel).invoke({"word": word})
        print(f"  French  : {result['french']}")
        print(f"  Spanish : {result['spanish']}")
    except Exception as e:
        print(f"  [ERROR]: {e}")


if __name__ == "__main__":
    try:
        model = init_chat_model("gpt-4o-mini", model_provider="openai")
        demonstrate_parallel_analysis(model)
        demonstrate_passthrough_assign(model)
        demonstrate_dict_shorthand(model)
    except Exception as e:
        print("\nSetup failed (check API keys):", e)


# ========================================================================================
# REAL-WORLD USE CASES
# ========================================================================================
#
# 1. MULTI-CHANNEL CONTENT PUBLISHER:
#    A blog post goes through 3 parallel branches:
#    - Branch A: Writes a Twitter/X thread (280 chars per tweet)
#    - Branch B: Writes a LinkedIn post (professional tone)
#    - Branch C: Writes an email newsletter excerpt
#    All three complete in the time of one single API call.
#
# 2. DOCUMENT COMPLIANCE SCANNER:
#    A legal document is simultaneously analyzed for:
#    - GDPR compliance issues
#    - PII (personally identifiable information) presence
#    - Readability score
#    All run in parallel, results merged into a compliance report.
#
# 3. RAG PIPELINE CONTEXT INJECTION (RunnablePassthrough.assign):
#    The standard LangChain RAG chain uses Passthrough.assign:
#      chain = RunnablePassthrough.assign(context=retriever) | prompt | llm | parser
#    The user's question flows through, context is added, then the prompt is built.
#
# ========================================================================================
# MNC INTERVIEW QUESTIONS & ANSWERS
# ========================================================================================
#
# Q1. How does RunnableParallel achieve concurrency?
# A:  Internally, RunnableParallel uses Python's `concurrent.futures.ThreadPoolExecutor`
#     for synchronous calls. Each branch runs as a separate thread, making API calls
#     simultaneously. For async workflows, `await asyncio.gather(...)` is used instead,
#     which is more efficient as it uses a single event loop.
#
# Q2. What is the dict shorthand for RunnableParallel and why does it work?
# A:  LangChain's Runnable base class overrides `__or__` so that when a plain Python
#     dict is placed in a pipe chain, it's automatically converted to RunnableParallel.
#     This is syntactic sugar: `{"a": chain_a, "b": chain_b}` === `RunnableParallel(...)`.
#
# Q3. What is the primary use case for RunnablePassthrough.assign()?
# A:  Building RAG (Retrieval-Augmented Generation) chains. The user query passes
#     through unchanged, while `.assign(context=retriever)` adds retrieved documents
#     as a new key to the dict. This means both the original question AND the context
#     are available when the prompt template is evaluated.
