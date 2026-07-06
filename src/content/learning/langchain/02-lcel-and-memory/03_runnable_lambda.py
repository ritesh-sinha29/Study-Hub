# ==========================================================
# LANGCHAIN STUDY GUIDE: 03. RUNNABLE LAMBDA
# ==========================================================

# --- RUNNABLE LAMBDA ---
# `RunnableLambda` converts custom Python functions into LangChain Runnables.
# This allows you to insert custom preprocessing, postprocessing, or filtering logic
# directly into your LCEL chains without losing streaming or batch capabilities.

import os
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableLambda
from langchain.chat_models import init_chat_model

load_dotenv()

# Example Python function to count characters in a text
def count_characters(text: str) -> int:
    return len(text.strip())

# Example Python function to format output as a clean uppercase statement
def format_shouting(text: str) -> str:
    return f"📢 {text.upper()} !!!"

def demonstrate_runnable_lambda(model):
    print("--- 3. RUNNABLE LAMBDA (CUSTOM FUNCTIONS) ---")
    
    prompt = ChatPromptTemplate.from_template("Give me a one-word synonym for {word}.")
    parser = StrOutputParser()
    
    # Define our custom RunnableLambda elements
    shouting_runnable = RunnableLambda(format_shouting)
    char_counter_runnable = RunnableLambda(count_characters)
    
    # Chain with postprocessing
    shouting_chain = prompt | model | parser | shouting_runnable
    
    # Chain with numeric return value
    counter_chain = prompt | model | parser | char_counter_runnable
    
    try:
        shout_res = shouting_chain.invoke({"word": "happy"})
        count_res = counter_chain.invoke({"word": "happy"})
        
        print("Input: happy")
        print("Shouting Output:", shout_res)
        print("Synonym Character Count:", count_res)
    except Exception as e:
        print("Lambda chain execution failed:", e)

if __name__ == "__main__":
    try:
        model = init_chat_model("gpt-4o-mini", model_provider="openai")
        demonstrate_runnable_lambda(model)
    except Exception as e:
        print("Model initialization failed:", e)

# ==========================================================
# REAL-LIFE USE CASES
# ==========================================================
# 1. TEXT CLEANING / PIXELS REDACTION: Preprocess a user's prompt by removing PII (Personally Identifiable
#    Information) or bad words using a custom python script before forwarding it to the LLM.
# 2. OUTPUT NORMALIZATION: Converting string JSON outputs to customized dataclasses or custom logging 
#    events directly within the output flow of the chain.

# ==========================================================
# MNC INTERVIEW QUESTIONS & ANSWERS
# ==========================================================
# Q1. When should you use `RunnableLambda`?
# A:  Use `RunnableLambda` whenever you need to execute custom Python code (like calculations, databases updates,
#     or custom text formatting) inside an LCEL pipeline while keeping the overall chain interface consistent.
#
# Q2. Does `RunnableLambda` support async execution?
# A:  Yes. You can pass either a synchronous function or an asynchronous function (coroutine) to `RunnableLambda`.
#     LangChain automatically handles async propagation when `.ainvoke()` is called on the chain.
