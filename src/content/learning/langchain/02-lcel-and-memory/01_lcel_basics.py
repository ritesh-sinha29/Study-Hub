# ==========================================================
# LANGCHAIN STUDY GUIDE: 01. LCEL BASICS
# ==========================================================

# --- WHAT IS LCEL? ---
# LangChain Expression Language (LCEL) is a declarative way to easily chain LangChain components together.
# It uses the pipe operator (`|`) to feed the output of one component directly as the input of the next.
# Under the hood, any LCEL chain implements the Runnable protocol, automatically giving you:
# 1. Unified Interface: Standard methods like `.invoke()`, `.stream()`, and `.batch()`.
# 2. Async Support: Built-in async equivalents (`.ainvoke()`, etc.) for high-concurrency tasks.
# 3. Streaming support: Intermediary steps can stream their outputs.

import os
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain.chat_models import init_chat_model

# Load environment variables
load_dotenv()

def demonstrate_lcel_basics(model):
    print("--- 1. LCEL CHAIN EXECUTION ---")
    
    # 1. Define the Prompt Template
    prompt = ChatPromptTemplate.from_template("Tell me a short, one-sentence joke about {topic}.")
    
    # 2. Define the Output Parser
    parser = StrOutputParser()
    
    # 3. Compose the Chain using the pipe operator (|)
    # The output of prompt is passed to the model, and the model's output is passed to the parser
    chain = prompt | model | parser
    
    # 4. Invoke the Chain
    try:
        response = chain.invoke({"topic": "programming"})
        print("Input: programming")
        print("Output:", response)
    except Exception as e:
        print("Chain execution failed:", e)

if __name__ == "__main__":
    try:
        model = init_chat_model("gpt-4o-mini", model_provider="openai")
        demonstrate_lcel_basics(model)
    except Exception as e:
        print("Model initialization failed (check API keys):", e)

# ==========================================================
# REAL-LIFE USE CASES
# ==========================================================
# 1. DYNAMIC TRANSLATION PIPELINE: Prompt templates dynamically adjust based on the target language,
#    the model translates it, and the output parser extracts the translated string directly.
# 2. SENTIMENT SUMMARY AGENT: Chains a prompt to summarize text, forwards it to the model,
#    and parses the raw content into clean strings for client-side display.

# ==========================================================
# MNC INTERVIEW QUESTIONS & ANSWERS
# ==========================================================
# Q1. What is the benefit of the pipe (|) operator in LangChain?
# A:  It provides a clean, declarative syntax for composing components. It automatically handles
#     type conversions between stages (e.g. converting a prompt output to a ChatMessage list)
#     and enables built-in streaming/batching across the entire chain.
#
# Q2. Do you need custom parsers for basic string outputs in LangChain?
# A:  While you can access `.content` directly from an AIMessage, using `StrOutputParser` 
#     ensures the chain returns a clean string directly. It also automatically supports streaming
#     individual text tokens as they arrive.
