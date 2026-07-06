# ==========================================================
# LANGCHAIN STUDY GUIDE: 02. RUNNABLE PARALLEL & PASSTHROUGH
# ==========================================================

# --- RUNNABLE PASSTHROUGH ---
# `RunnablePassthrough` allows you to pass inputs through unchanged or with extra keys.
# It is extremely useful when the next stage of the chain requires the original input alongside 
# the outputs of intermediate steps.

# --- RUNNABLE PARALLEL ---
# `RunnableParallel` (previously `Map`) allows you to run multiple chains/operations concurrently.
# It returns a dictionary where each key contains the output of the corresponding parallel branch.

import os
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough, RunnableParallel
from langchain.chat_models import init_chat_model

load_dotenv()

def demonstrate_parallel_and_passthrough(model):
    print("--- 2. RUNNABLE PARALLEL & PASSTHROUGH ---")
    
    # Define two different tasks that we want to run concurrently on a text
    summary_prompt = ChatPromptTemplate.from_template("Summarize the following text in one sentence:\n\n{text}")
    bullets_prompt = ChatPromptTemplate.from_template("Extract 3 key bullet points from the following text:\n\n{text}")
    
    parser = StrOutputParser()
    
    # Create the branches
    summary_chain = summary_prompt | model | parser
    bullets_chain = bullets_prompt | model | parser
    
    # Combine branches using RunnableParallel
    # This runs summary_chain and bullets_chain in parallel
    combined_parallel = RunnableParallel(
        summary=summary_chain,
        bullets=bullets_chain,
        original_text=RunnablePassthrough() # Passes the input 'text' straight through to the final dictionary
    )
    
    sample_text = (
        "Artificial Intelligence (AI) is transforming industries by automating repetitive tasks, "
        "providing deep data insights, and enhancing decision-making. However, it also introduces "
        "challenges around data privacy, bias in algorithms, and the displacement of certain job roles."
    )
    
    try:
        response = combined_parallel.invoke(sample_text)
        print("Parallel Execution Completed successfully.")
        print("\n[Original Text Passed Through]:\n", response["original_text"])
        print("\n[One-Sentence Summary]:\n", response["summary"])
        print("\n[Key Bullet Points]:\n", response["bullets"])
    except Exception as e:
        print("Parallel execution failed:", e)

if __name__ == "__main__":
    try:
        model = init_chat_model("gpt-4o-mini", model_provider="openai")
        demonstrate_parallel_and_passthrough(model)
    except Exception as e:
        print("Model initialization failed:", e)

# ==========================================================
# REAL-LIFE USE CASES
# ==========================================================
# 1. PARALLEL CONTENT CHECKERS: When a user posts an article, one branch of the chain check for grammar
#    errors while another branch checks for compliance/policy violations, returning both reports together.
# 2. CONTEXT & METRICS LOGGING: Passing the user's original query through (`RunnablePassthrough`)
#    while running retrieval in parallel, ensuring both the retrieved documents and original prompt
#    are formatted cleanly for logging.

# ==========================================================
# MNC INTERVIEW QUESTIONS & ANSWERS
# ==========================================================
# Q1. How does RunnableParallel improve processing times?
# A:  RunnableParallel executes independent network requests concurrently. If you have three LLM tasks
#     that each take 1 second, running them in parallel takes ~1 second total instead of 3 seconds sequentially.
#
# Q2. What is the main purpose of `RunnablePassthrough`?
# A:  It acts as a placeholder that copies the input data unchanged. This is vital when building nested chains
#     where you need to preserve the user's initial raw query for a later step (e.g. for comparing raw inputs
#     with structured responses).
