# ========================================================================================
# LANGCHAIN CRASH COURSE — LCEL MODULE 01: LANGCHAIN EXPRESSION LANGUAGE (LCEL) BASICS
# ========================================================================================
#
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# SECTION 1 — WHAT IS LCEL (LANGCHAIN EXPRESSION LANGUAGE)?
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#
# Traditional LLM pipeline code looks like this — messy, nested, and hard to read:
#
#   prompt_value = prompt_template.format_messages(topic=topic)
#   ai_message   = chat_model(prompt_value)
#   text_output  = output_parser.parse(ai_message.content)
#
# LCEL (LangChain Expression Language) replaces this with a clean, declarative syntax:
#
#   chain = prompt | model | parser
#   result = chain.invoke({"topic": "Python"})
#
# The Python pipe operator `|` connects components — the output of each stage
# flows directly as the input of the next stage. This reads left-to-right, like
# a Unix pipe command: `cat file.txt | grep "error" | wc -l`
#
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# SECTION 2 — THE RUNNABLE PROTOCOL (THE FOUNDATION OF LCEL)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#
# Every LCEL component implements the Runnable interface. This means every single
# component — prompts, models, parsers, tools, chains, custom functions — all share
# the same uniform API:
#
#  ┌──────────────────────────────────────────────────────────────────────┐
#  │                    THE RUNNABLE INTERFACE                            │
#  │                                                                      │
#  │  Method           │ Description                                     │
#  │  ─────────────────┼────────────────────────────────────────────     │
#  │  .invoke(input)   │ Sync: run once, return single result            │
#  │  .ainvoke(input)  │ Async: run once, return single result           │
#  │  .stream(input)   │ Sync: run and yield tokens as they arrive       │
#  │  .astream(input)  │ Async: stream tokens asynchronously             │
#  │  .batch([...])    │ Sync: run multiple inputs concurrently          │
#  │  .abatch([...])   │ Async: batch concurrently using asyncio         │
#  └──────────────────────────────────────────────────────────────────────┘
#
# Because ALL components share this interface, you can swap any part of a chain
# (e.g., replace GPT-4o with Gemini) without changing anything else in the pipeline.
#
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# SECTION 3 — DATA TYPES: HOW DATA FLOWS THROUGH THE PIPE
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#
# Each stage transforms the data type:
#
#  Input: dict {"topic": "AI"}
#         │
#         ▼
#  [ChatPromptTemplate]  →  Output: PromptValue (contains formatted message list)
#         │
#         ▼
#  [ChatModel]           →  Output: AIMessage (has .content, .tool_calls, .metadata)
#         │
#         ▼
#  [StrOutputParser]     →  Output: str (clean plain text string)
#
# StrOutputParser extracts AIMessage.content and returns it as a plain Python string.
# This is important for streaming: StrOutputParser correctly yields string chunks,
# not AIMessageChunk objects.
#
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# SECTION 4 — PROMPT TEMPLATES: TYPES & WHEN TO USE EACH
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#
#  Template Type                   │ When to Use
#  ────────────────────────────────┼──────────────────────────────────────────────
#  PromptTemplate.from_template()  │ Legacy, plain text prompts for text-completion
#  ChatPromptTemplate.from_template│ Single-message chat prompts (no system role)
#  ChatPromptTemplate.from_messages│ Multi-role: system + human + history placeholders
#  HumanMessagePromptTemplate      │ Direct user message with variable slots
#  SystemMessagePromptTemplate     │ Direct system persona with variable slots
#
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# SECTION 5 — INSPECTING CHAINS: SCHEMA & VISUALIZATION
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#
# Any LCEL chain exposes its input/output schema:
#   chain.input_schema.schema()   → shows what dict keys the chain expects
#   chain.output_schema.schema()  → shows what type the chain returns
#
# ========================================================================================

import os
from dotenv import load_dotenv

# Load API keys from .env
load_dotenv()

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain.chat_models import init_chat_model


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# EXAMPLE 1: BASIC LCEL CHAIN (Prompt | Model | Parser)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def demonstrate_basic_chain(model):
    print("\n" + "="*70)
    print("EXAMPLE 1: BASIC LCEL CHAIN — prompt | model | parser")
    print("="*70)

    # Step 1: Define a prompt template with a {topic} placeholder
    prompt = ChatPromptTemplate.from_template(
        "Tell me a short, clever joke about {topic}. Keep it to 2 sentences max."
    )

    # Step 2: Define an output parser
    # StrOutputParser extracts .content from AIMessage and returns plain string
    parser = StrOutputParser()

    # Step 3: Compose the chain using the pipe operator
    # Data flows: dict → PromptValue → AIMessage → str
    chain = prompt | model | parser

    print(f"\n  Chain type: {type(chain).__name__}")
    print(f"  Input schema: {chain.input_schema.schema()}")

    topic = "Python programming"
    print(f"\n  Invoking chain with topic: '{topic}'...")

    try:
        result = chain.invoke({"topic": topic})
        print(f"\n  Result (str): '{result}'")
    except Exception as e:
        print(f"  [ERROR]: {e}")


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# EXAMPLE 2: MULTI-ROLE SYSTEM + HUMAN PROMPT TEMPLATE
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def demonstrate_system_prompt_chain(model):
    print("\n" + "="*70)
    print("EXAMPLE 2: MULTI-ROLE PROMPT (System + Human)")
    print("="*70)

    # from_messages lets you define multiple roles
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a {persona}. Answer all questions in that style."),
        ("human",  "{question}")
    ])

    parser = StrOutputParser()
    chain  = prompt | model | parser

    inputs = {
        "persona":  "sarcastic tech expert who uses puns in every answer",
        "question": "Why should I learn LangChain?"
    }

    print(f"  Persona  : '{inputs['persona']}'")
    print(f"  Question : '{inputs['question']}'")

    try:
        result = chain.invoke(inputs)
        print(f"\n  Response:\n  '{result}'")
    except Exception as e:
        print(f"  [ERROR]: {e}")


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# EXAMPLE 3: STREAMING A CHAIN (same chain, different invocation method)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def demonstrate_chain_streaming(model):
    print("\n" + "="*70)
    print("EXAMPLE 3: STREAMING AN LCEL CHAIN TOKEN-BY-TOKEN")
    print("="*70)

    prompt = ChatPromptTemplate.from_template(
        "Explain {concept} to a 10-year-old in 3 simple sentences."
    )
    parser = StrOutputParser()
    chain  = prompt | model | parser

    print("  Streaming response (tokens appear live):")
    print("  " + "-"*50)

    try:
        # Same chain, just call .stream() instead of .invoke()
        # StrOutputParser ensures we get clean string tokens, not AIMessageChunks
        for token in chain.stream({"concept": "machine learning"}):
            print(token, end="", flush=True)
        print("\n  " + "-"*50)
    except Exception as e:
        print(f"  [ERROR]: {e}")


if __name__ == "__main__":
    try:
        model = init_chat_model("gpt-4o-mini", model_provider="openai")
        demonstrate_basic_chain(model)
        demonstrate_system_prompt_chain(model)
        demonstrate_chain_streaming(model)
    except Exception as e:
        print("\nSetup failed (check API keys):", e)


# ========================================================================================
# REAL-WORLD USE CASES
# ========================================================================================
#
# 1. CUSTOMER TICKET CATEGORIZATION PIPELINE:
#    Input: {"ticket_text": "My order hasn't arrived after 2 weeks."}
#    Chain: classify_prompt | model | StrOutputParser()
#    Output: "shipping_delay"  → auto-routes to fulfilment team
#
# 2. MULTI-LANGUAGE DOCUMENT TRANSLATOR:
#    Chain: translate_prompt | model | parser
#    Batch: chain.batch([{"text": doc, "lang": "French"} for doc in documents])
#    → Processes 100 documents concurrently in seconds
#
# 3. CODE REVIEW ASSISTANT:
#    chain = review_prompt | gpt4o | StrOutputParser()
#    Streams the code review feedback token-by-token to a developer's IDE plugin.
#
# ========================================================================================
# MNC INTERVIEW QUESTIONS & ANSWERS
# ========================================================================================
#
# Q1. What is the advantage of `StrOutputParser` over accessing `.content` manually?
# A:  StrOutputParser integrates correctly with streaming. When you call `.stream()`
#     on a chain that ends with StrOutputParser, it yields clean string tokens.
#     Without the parser, you get AIMessageChunk objects and must manually access
#     `.content` on each chunk, breaking the clean pipe interface.
#
# Q2. What happens if you pipe incompatible types in LCEL?
# A:  LangChain's RunnableSequence validates InputType/OutputType at composition time.
#     If Step A outputs a str but Step B expects a dict, it raises a TypeError.
#     However, most mismatches surface at runtime — always test chains with sample inputs.
#
# Q3. How does the `|` operator work technically in LangChain?
# A:  LangChain's Runnable base class overrides Python's `__or__` dunder method.
#     When you write `prompt | model`, Python calls `prompt.__or__(model)`, which
#     creates a `RunnableSequence([prompt, model])` object internally. This is
#     not native Python pipe behaviour — it's a LangChain-specific abstraction.
