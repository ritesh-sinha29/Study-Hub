# ========================================================================================
# LANGCHAIN CRASH COURSE — MODULE 02: DYNAMIC MODEL INTEGRATION & VENDOR ABSTRACTION
# ========================================================================================
#
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# SECTION 1 — WHY MODEL ABSTRACTION MATTERS
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#
# The LLM market moves fast. Models are replaced, new providers emerge, and pricing
# changes constantly. Hardcoding `from langchain_openai import ChatOpenAI` everywhere
# binds your entire codebase to one vendor.
#
# The `init_chat_model` factory allows you to select any model from any supported
# provider by changing a single string — your pipeline logic stays identical.
#
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# SECTION 2 — MODEL CONFIGURATION PARAMETERS
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#
#  ┌──────────────────────────────────────────────────────────────────────┐
#  │  PARAMETER        │ WHAT IT DOES            │ TYPICAL VALUES         │
#  ├──────────────────────────────────────────────────────────────────────┤
#  │  temperature      │ Controls randomness     │ 0.0 (precise) →        │
#  │                   │ of token selection      │ 1.0+ (creative)        │
#  ├──────────────────────────────────────────────────────────────────────┤
#  │  max_tokens       │ Caps response length,   │ 100 (short) →          │
#  │                   │ controls API cost       │ 8192 (long)            │
#  ├──────────────────────────────────────────────────────────────────────┤
#  │  model_provider   │ Selects which partner   │ "openai", "anthropic", │
#  │                   │ package to load         │ "google_genai", "groq" │
#  ├──────────────────────────────────────────────────────────────────────┤
#  │  top_p            │ Nucleus sampling:       │ 0.9 (focused) →        │
#  │                   │ limits token pool size  │ 1.0 (all tokens)       │
#  └──────────────────────────────────────────────────────────────────────┘
#
# TEMPERATURE GUIDANCE:
#   - temperature=0.0 → Extraction, coding, factual Q&A (deterministic)
#   - temperature=0.3 → Summaries, reports (slight variation)
#   - temperature=0.7 → Marketing copy, story generation (creative)
#   - temperature=1.0+ → Brainstorming, poetry, experimental output
#
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# SECTION 3 — SUPPORTED PROVIDERS
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#
#  PROVIDER         │ MODEL STRING EXAMPLES          │ PACKAGE REQUIRED
#  ─────────────────┼────────────────────────────────┼─────────────────────────────────
#  OpenAI           │ "gpt-4o", "gpt-4o-mini"        │ langchain-openai
#  Anthropic        │ "claude-3-5-sonnet-20241022"   │ langchain-anthropic
#  Google GenAI     │ "gemini-1.5-flash"             │ langchain-google-genai
#  Groq (fast)      │ "llama-3.1-70b-versatile"     │ langchain-groq
#  Ollama (local)   │ "llama3.2", "mistral"          │ langchain-ollama
#
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# SECTION 4 — RUNTIME FALLBACKS (PRODUCTION RESILIENCE PATTERN)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#
# In production, API services fail. A model provider may return:
#   - HTTP 429: Rate limit exceeded (too many requests per minute)
#   - HTTP 503: Service temporarily unavailable (provider outage)
#   - HTTP 500: Internal server error (provider-side bugs)
#
# The `.with_fallbacks([backup_model])` pattern automatically switches to
# a backup model when these errors occur, without crashing the application.
#
#  ┌─────────────────────────────────────────────────────┐
#  │              FALLBACK DECISION TREE                 │
#  │                                                     │
#  │  [User Request]                                     │
#  │        │                                            │
#  │        ▼                                            │
#  │  [Primary: GPT-4o-mini] ──► Success? ──► Return     │
#  │        │                                            │
#  │        └──► 429/503 Error                           │
#  │                   │                                 │
#  │                   ▼                                 │
#  │  [Fallback: Gemini 1.5 Flash] ──► Return            │
#  └─────────────────────────────────────────────────────┘
#
# ========================================================================================

import os
from dotenv import load_dotenv

# Load API keys from .env file
load_dotenv()

from langchain.chat_models import init_chat_model


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# EXAMPLE 1: DYNAMIC MODEL INITIALIZATION ACROSS PROVIDERS
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def demonstrate_dynamic_initialization():
    print("\n" + "="*70)
    print("EXAMPLE 1: DYNAMIC MODEL INITIALIZATION ACROSS PROVIDERS")
    print("="*70)

    providers = [
        ("gpt-4o-mini",               "openai",        0.0),
        ("gemini-1.5-flash",          "google_genai",  0.0),
        ("claude-3-5-sonnet-20241022","anthropic",     0.0),
    ]

    for model_name, provider, temp in providers:
        try:
            model = init_chat_model(
                model=model_name,
                model_provider=provider,
                temperature=temp
            )
            print(f"  ✓ [{provider.upper()}] Loaded: {model_name}")
        except Exception as e:
            print(f"  ✗ [{provider.upper()}] Failed (API key missing?): {e}")


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# EXAMPLE 2: PRODUCTION FALLBACK BINDING
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def demonstrate_fallback_pattern():
    print("\n" + "="*70)
    print("EXAMPLE 2: RESILIENT MODEL WITH FALLBACK CHAIN")
    print("="*70)

    try:
        # Primary model — fast and cheap
        primary = init_chat_model("gpt-4o-mini", model_provider="openai", temperature=0)

        # Backup model — kicks in if primary fails
        backup = init_chat_model("gemini-1.5-flash", model_provider="google_genai", temperature=0)

        # Bind fallback — LangChain handles error catching automatically
        resilient_model = primary.with_fallbacks([backup])

        print(f"  Primary model  : gpt-4o-mini (OpenAI)")
        print(f"  Fallback model : gemini-1.5-flash (Google)")
        print(f"  Bound type     : {type(resilient_model).__name__}")

        # The chain below would use the backup if primary throws 429/503
        print("\n  Testing resilient model invocation...")
        response = resilient_model.invoke("Say 'model fallback successful' in exactly 4 words.")
        print(f"  Response: {response.content.strip()}")

    except Exception as e:
        print(f"  [ERROR] Fallback setup failed (check API keys): {e}")


if __name__ == "__main__":
    demonstrate_dynamic_initialization()
    demonstrate_fallback_pattern()


# ========================================================================================
# REAL-WORLD USE CASES
# ========================================================================================
#
# 1. COST-AWARE ROUTING:
#    - **Step 1**: Routes simple classification queries to cheap model (Groq Llama-3).
#    - **Step 2**: Routes complex reasoning queries to gpt_4o.
#    - **Result**: Reduces monthly API bills by 80% for the startup.
#
# 2. COMPLIANCE-BASED MODEL SWITCHING:
#    - **Input**: Healthcare app needs to keep patient data within EU boundaries.
#    - **Step 1**: Routes sensitive queries to Mistral EU-hosted endpoints.
#    - **Step 2**: Routes generic queries to standard OpenAI endpoints.
#    - **Result**: Enforces strict data compliance rules.
#
# 3. BATCH TRANSLATION OVERNIGHT JOBS:
#    - **Step 1**: Processes 50,000-document batch translation overnight.
#    - **Step 2**: Automatically catches OpenAI rate limit exceptions at 3 AM.
#    - **Result**: Falls back to Gemini to complete the job without waking engineers.
#
# ========================================================================================
# MNC INTERVIEW QUESTIONS & ANSWERS
# ========================================================================================
#
# Q1. What is the difference between an LLM wrapper and a ChatModel wrapper?
# A:  - LLM wrappers (now legacy) accept a raw string input and return a raw string.
#     - ChatModel wrappers accept structured Message objects (SystemMessage,
#       HumanMessage, etc.) and return a structured AIMessage. All modern models
#       including GPT-4o, Claude, and Gemini are ChatModels.
#
# Q2. How does `.with_fallbacks()` know which errors to catch?
# A:  By default, it catches `Exception` broadly. You can narrow this with the
#     `exceptions_to_handle` parameter:
#       model.with_fallbacks([backup], exceptions_to_handle=(RateLimitError,))
#     This prevents legitimate errors (like bad API keys) from silently falling
#     through to the backup model.
#
# Q3. What does `temperature=0` mean and why would you use it?
# A:  At temperature=0, the model always picks the single highest-probability
#     next token, making outputs fully deterministic and reproducible. Use it
#     for tasks requiring consistent, factual answers: data extraction, code
#     generation, classification, structured output generation.
