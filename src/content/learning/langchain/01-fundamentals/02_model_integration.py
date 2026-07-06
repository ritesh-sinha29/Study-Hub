# ==========================================================
# LANGCHAIN STUDY GUIDE: 02. MODEL INTEGRATION
# ==========================================================

# --- MODEL PROVIDERS & INTEGRATIONS ---
# LangChain provides a unified interface to interact with different LLM providers like:
# 1. OpenAI (GPT-4o, GPT-4o-mini)
# 2. Google Gemini (Gemini 2.5 Flash, Gemini 1.5 Pro)
# 3. Groq (Fast Llama-3, Mixtral, Qwen models hosted on Groq)
# 4. Anthropic Claude (Claude 3.5 Sonnet, Claude 3.5 Haiku)

# There are two primary ways to initialize chat models in modern LangChain:
# A. Using `init_chat_model` (Recommended) - Allows dynamic initialization by passing string names.
# B. Using direct class imports (e.g., `ChatOpenAI`, `ChatGoogleGenerativeAI`, `ChatGroq`, `ChatAnthropic`).

import os
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
# Direct imports (requires langchain-openai, langchain-google-genai, langchain-groq, langchain-anthropic packages)
# from langchain_openai import ChatOpenAI
# from langchain_google_genai import ChatGoogleGenerativeAI
# from langchain_groq import ChatGroq
# from langchain_anthropic import ChatAnthropic

# Load environment variables (.env)
load_dotenv()

def demonstrate_init_chat_model():
    print("--- 1. INITIALIZING WITH init_chat_model ---")
    
    # Initialize OpenAI model
    try:
        # init_chat_model will automatically infer the provider from the model name
        # or you can specify the model provider explicitly.
        openai_model = init_chat_model("gpt-4o-mini", model_provider="openai")
        print("Successfully initialized OpenAI model wrapper:", type(openai_model))
    except Exception as e:
        print("Failed to initialize OpenAI:", e)

    # Initialize Google Gemini model
    try:
        gemini_model = init_chat_model("gemini-2.5-flash", model_provider="google_genai")
        print("Successfully initialized Google Gemini model wrapper:", type(gemini_model))
    except Exception as e:
        print("Failed to initialize Google Gemini:", e)

    # Initialize Groq model
    try:
        groq_model = init_chat_model("llama-3.1-8b-instant", model_provider="groq")
        print("Successfully initialized Groq model wrapper:", type(groq_model))
    except Exception as e:
        print("Failed to initialize Groq:", e)

    # Initialize Anthropic Claude model
    try:
        claude_model = init_chat_model("claude-3-5-sonnet-20241022", model_provider="anthropic")
        print("Successfully initialized Claude model wrapper:", type(claude_model))
    except Exception as e:
        print("Failed to initialize Claude:", e)

# ----------------------------------------------------------
# HOW TO RUN THIS FILE
# ----------------------------------------------------------
# Make sure your API keys are defined in your environment/system.
# Run:
#   python 02_model_integration.py
# ----------------------------------------------------------
if __name__ == "__main__":
    demonstrate_init_chat_model()

# ==========================================================
# REAL-LIFE USE CASES
# ==========================================================
# 1. MULTI-MODEL FALLBACK: An application starts with a cheaper/faster model (like Gemini Flash).
#    If the request fails or is highly complex, the code catches the error and initializes a
#    stronger model (like GPT-4o or Claude 3.5 Sonnet) on the fly using `init_chat_model`.
# 2. COST OPTIMIZATION: Routing simple classification tasks to Groq (Llama-3) and complex reasoning
#    tasks to OpenAI GPT-4o or Anthropic Claude.

# ==========================================================
# MNC INTERVIEW QUESTIONS & ANSWERS
# ==========================================================
# Q1. What is the benefit of using `init_chat_model` over importing direct model wrappers?
# A:  `init_chat_model` decouples your application logic from the underlying LLM provider class.
#     It allows you to switch providers (e.g. from OpenAI to Anthropic or Google) via simple
#     configuration strings without changing imports or instantiations.
#
# Q2. What environment variables are looked up by default for OpenAI, Gemini, Groq, and Anthropic in LangChain?
# A:  - OpenAI: `OPENAI_API_KEY`
#     - Google: `GEMINI_API_KEY` or `GOOGLE_API_KEY`
#     - Groq: `GROQ_API_KEY`
#     - Anthropic: `ANTHROPIC_API_KEY`
