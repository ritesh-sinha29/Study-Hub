# ========================================================================================
# LANGCHAIN CRASH COURSE — LCEL MODULE 03: RUNNABLE LAMBDA (CUSTOM FUNCTIONS IN CHAINS)
# ========================================================================================
#
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# SECTION 1 — THE PROBLEM LCEL SOLVES
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#
# LCEL chains are composed of Runnables. But what about custom Python logic you
# need to run between steps? For example:
#   - Clean a string before sending it to the model
#   - Transform the model's output (uppercase it, parse it, count words)
#   - Call a database inside a chain
#   - Apply a business rule filter mid-pipeline
#
# You cannot pipe a plain Python function directly — it's not a Runnable.
#
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# SECTION 2 — WHAT IS RUNNABLE LAMBDA?
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#
# `RunnableLambda` wraps any Python function or coroutine and converts it into a
# full Runnable, giving it `.invoke()`, `.stream()`, `.batch()`, `.ainvoke()`.
#
# Two ways to create one:
#
#   # EXPLICIT:
#   my_runnable = RunnableLambda(my_python_function)
#   chain = prompt | model | parser | my_runnable
#
#   # SHORTHAND (pipe operator auto-wraps callables):
#   chain = prompt | model | parser | my_python_function
#   # LangChain automatically converts `my_python_function` to a RunnableLambda
#
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# SECTION 3 — WHERE IN THE PIPELINE CAN YOU USE IT?
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#
#  PREPROCESSING (before model):
#    clean_input | prompt | model | parser
#    ^ RunnableLambda strips PII or bad words before sending to the LLM
#
#  POSTPROCESSING (after parser):
#    prompt | model | parser | format_output
#                              ^ RunnableLambda reformats or enriches the string output
#
#  MIDCHAIN (between any two steps):
#    step_a | transform_data | step_b
#             ^ RunnableLambda reshapes the output of step_a into what step_b expects
#
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# SECTION 4 — ASYNC SUPPORT
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#
# Pass an `async def` function to RunnableLambda for async pipelines:
#
#   async def fetch_from_db(query: str) -> str:
#       result = await db.execute(query)
#       return result
#
#   db_runnable = RunnableLambda(fetch_from_db)   # becomes async runnable
#   await chain.ainvoke(input)   # runs fetch_from_db as coroutine
#
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# SECTION 5 — WHEN TO USE RUNNABLELAMBDA VS @tool
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#
#  USE RunnableLambda WHEN:           USE @tool WHEN:
#  ✓ You are building deterministic   ✓ The LLM needs to decide WHETHER
#    pipeline transformations            to call it (agent reasoning)
#  ✓ The function ALWAYS runs         ✓ The function needs a JSON schema
#    (not model-decided)                 for LLM function calling
#  ✓ Pre/post processing steps        ✓ The function is part of an agent toolkit
#
# ========================================================================================

import os
from dotenv import load_dotenv

# Load API keys
load_dotenv()

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableLambda
from langchain.chat_models import init_chat_model


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# CUSTOM TRANSFORM FUNCTIONS
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def clean_input(text: str) -> str:
    """
    Preprocessing lambda: strips leading/trailing whitespace and removes
    common profanities or sensitive words before sending to the LLM.
    """
    cleaned = text.strip()
    blocked_words = ["stupid", "idiot", "hate"]
    for word in blocked_words:
        cleaned = cleaned.replace(word, "[FILTERED]")
    return cleaned


def format_as_announcement(text: str) -> str:
    """
    Postprocessing lambda: formats any string output as a formatted announcement.
    Useful for notification pipelines.
    """
    return f"📢 ANNOUNCEMENT: {text.strip().upper()} 🔔"


def count_words(text: str) -> dict:
    """
    Postprocessing lambda: instead of returning the text, returns metadata.
    Demonstrates that lambdas can change the data type entirely.
    """
    words = text.strip().split()
    return {
        "word_count":  len(words),
        "char_count":  len(text.strip()),
        "preview":     " ".join(words[:5]) + ("..." if len(words) > 5 else "")
    }


def pii_redactor(text: str) -> str:
    """
    Preprocessing lambda: removes email addresses and phone numbers from text.
    In production, use a proper regex or library like 'presidio'.
    """
    import re
    text = re.sub(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', '[EMAIL REDACTED]', text)
    text = re.sub(r'\b\d{10}\b|\b\d{3}[-.\s]\d{3}[-.\s]\d{4}\b', '[PHONE REDACTED]', text)
    return text


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# EXAMPLE 1: POSTPROCESSING — format model output as announcement
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def demonstrate_postprocessing(model):
    print("\n" + "="*70)
    print("EXAMPLE 1: POSTPROCESSING — FORMAT OUTPUT AS ANNOUNCEMENT")
    print("="*70)

    prompt = ChatPromptTemplate.from_template(
        "Give me a one-word synonym for the word: '{word}'"
    )
    parser = StrOutputParser()

    # Wrap our custom function in RunnableLambda (explicit)
    announce_runnable = RunnableLambda(format_as_announcement)

    # Chain: word → prompt → model → string → formatted announcement
    chain = prompt | model | parser | announce_runnable

    word = "cheerful"
    print(f"  Input word: '{word}'")
    try:
        result = chain.invoke({"word": word})
        print(f"  Output: {result}")
    except Exception as e:
        print(f"  [ERROR]: {e}")


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# EXAMPLE 2: PREPROCESSING — sanitize input before it reaches the LLM
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def demonstrate_preprocessing(model):
    print("\n" + "="*70)
    print("EXAMPLE 2: PREPROCESSING — SANITIZE + REDACT BEFORE LLM CALL")
    print("="*70)

    # Preprocessing runs BEFORE the prompt template
    clean_runnable = RunnableLambda(clean_input)
    redact_runnable = RunnableLambda(pii_redactor)

    prompt = ChatPromptTemplate.from_template(
        "The user submitted this support message. Summarize the issue briefly:\n\n{message}"
    )
    parser = StrOutputParser()

    # Note: lambdas can be chained together too
    preprocess_chain = clean_runnable | redact_runnable

    dirty_message = (
        "  I hate this stupid product! Contact me at john@gmail.com or call 555-867-5309. "
        "My account is broken!  "
    )

    print(f"  Raw input   : '{dirty_message[:80]}...'")
    cleaned = preprocess_chain.invoke(dirty_message)
    print(f"  After clean : '{cleaned[:80]}...'")

    try:
        result = (prompt | model | parser).invoke({"message": cleaned})
        print(f"\n  LLM Summary : '{result}'")
    except Exception as e:
        print(f"  [ERROR]: {e}")


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# EXAMPLE 3: TYPE-CHANGING LAMBDA — returns dict instead of str
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def demonstrate_type_changing_lambda(model):
    print("\n" + "="*70)
    print("EXAMPLE 3: TYPE-CHANGING LAMBDA (str → dict output)")
    print("="*70)

    prompt = ChatPromptTemplate.from_template(
        "Write a 2-sentence description of {topic}."
    )
    parser = StrOutputParser()
    count_runnable = RunnableLambda(count_words)

    # Chain returns a dict instead of str
    analysis_chain = prompt | model | parser | count_runnable

    topic = "machine learning"
    print(f"  Topic: '{topic}'")
    try:
        result = analysis_chain.invoke({"topic": topic})
        print(f"\n  Word count  : {result['word_count']}")
        print(f"  Char count  : {result['char_count']}")
        print(f"  Preview     : '{result['preview']}'")
        print(f"  Result type : {type(result).__name__}")
    except Exception as e:
        print(f"  [ERROR]: {e}")


if __name__ == "__main__":
    try:
        model = init_chat_model("gpt-4o-mini", model_provider="openai")
        demonstrate_postprocessing(model)
        demonstrate_preprocessing(model)
        demonstrate_type_changing_lambda(model)
    except Exception as e:
        print("\nSetup failed (check API keys):", e)


# ========================================================================================
# REAL-WORLD USE CASES
# ========================================================================================
#
# 1. PII REDACTION BEFORE CLOUD LLM CALLS:
#    Company policy forbids sending customer PII to external APIs. A RunnableLambda
#    PII redactor runs first, masking emails/phone/SSNs before the data leaves
#    the corporate network. Compliance is enforced at the pipeline level.
#
# 2. POST-PROCESSING FOR DATABASE INSERTION:
#    After the model generates a structured summary, a RunnableLambda serializes
#    it to a database record format and calls `db.insert()`. The chain itself
#    handles storage as part of the pipeline — no separate code needed.
#
# 3. TOKEN COUNT GUARDRAILS:
#    A RunnableLambda in preprocessing checks if the user's input exceeds the
#    model's context window (e.g., 128K tokens). If it does, it truncates or
#    summarizes the input before passing it to the main chain.
#
# ========================================================================================
# MNC INTERVIEW QUESTIONS & ANSWERS
# ========================================================================================
#
# Q1. When should you use RunnableLambda instead of @tool?
# A:  - Use RunnableLambda for deterministic pipeline transformations that ALWAYS
#       run: input cleaning, output formatting, type conversions, DB writes.
#     - Use @tool when you need the LLM to DECIDE whether and how to call the
#       function — it's a tool the agent can choose from, not a forced step.
#
# Q2. Does RunnableLambda support async functions?
# A:  Yes. Pass `async def` coroutines to RunnableLambda. When the chain calls
#     `.ainvoke()`, the coroutine runs asynchronously. If `.invoke()` is called
#     on an async lambda, LangChain handles it using `asyncio.run_coroutine_threadsafe`.
#
# Q3. Can RunnableLambda change the output data type of a chain?
# A:  Yes — completely. A lambda can receive a `str` and return a `dict`, `int`,
#     `list`, or any Python object. Whatever the lambda returns becomes the output
#     of that chain step and the input to the next step. This enables powerful
#     type reshaping between pipeline stages.
