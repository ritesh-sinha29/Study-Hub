# ==========================================================
# LANGCHAIN STUDY GUIDE: 07. MIDDLEWARE
# ==========================================================

# --- WHAT IS MIDDLEWARE? ---
# Middleware (often implemented in LangGraph or custom chains) allows you to run logic
# BEFORE or AFTER a request hits the LLM, or even interrupt/pause execution.
#
# Common Middleware Patterns:
# 1. Summarization / Memory Middleware: Automatically condenses chat history if it exceeds a token limit.
# 2. Human-in-the-Loop Confirmation: Pauses execution to request user confirmation before running critical tools (like sending an email or writing to a DB).

import os
from dotenv import load_dotenv

load_dotenv()

# --- 1. MOCK SUMMARIZATION MIDDLEWARE ---
def summarization_middleware(messages: list, token_limit: int = 100) -> list:
    """
    Intercepts the messages list. If the estimated character count exceeds the limit,
    it summarises the oldest messages to preserve context windows.
    """
    total_length = sum(len(msg.get("content", "")) for msg in messages)
    
    if total_length > token_limit:
        print(f"[Middleware] Total length ({total_length}) exceeds limit. Summarizing...")
        # Mock summarizing the first two messages
        summarized_history = [{"role": "system", "content": "Summary of previous conversation: User asked about math."}]
        # Keep the latest message
        summarized_history.append(messages[-1])
        return summarized_history
    return messages

# --- 2. MOCK HUMAN-IN-THE-LOOP MIDDLEWARE ---
def execute_tool_with_confirmation(tool_name: str, args: dict) -> bool:
    """
    Middleware that interrupts execution for high-risk actions.
    Returns True if approved, False otherwise.
    """
    print(f"\n[Middleware/Guardrail] Requesting approval to run tool: {tool_name} with args: {args}")
    # In a real app, this would block and show a UI confirmation button
    user_input = input("Approve tool execution? (yes/no): ").strip().lower()
    
    if user_input == "yes" or user_input == "y":
        print("[Middleware] Tool call approved.")
        return True
    else:
        print("[Middleware] Tool call rejected by user.")
        return False

if __name__ == "__main__":
    # Test Summarization Middleware
    history = [
        {"role": "user", "content": "Hello, I want to learn LangChain and build cool autonomous agents."},
        {"role": "assistant", "content": "That is awesome! Let us start by understanding the basic concepts."},
        {"role": "user", "content": "Can you explain how middleware works in LangChain?"}
    ]
    
    print("Original History:", history)
    processed_history = summarization_middleware(history, token_limit=50)
    print("Processed History:", processed_history)

# ==========================================================
# REAL-LIFE USE CASES
# ==========================================================
# 1. TOKEN SAVER: Prevent API bill shock by summarizing chat histories on the fly.
# 2. TRANSACTION APPROVAL: Ensure users approve any database edits or payment transactions
#    initiated autonomously by the agent.

# ==========================================================
# MNC INTERVIEW QUESTIONS & ANSWERS
# ==========================================================
# Q1. What is the role of Human-in-the-Loop (HITL) in agentic workflows?
# A:  HITL acts as a safety barrier. When an agent decides to perform a write action (like sending
#     an email, deleting a file, or modifying data), the middleware intercepts the tool call,
#     saves the state, asks for human approval, and resumes execution only upon user consent.
#
# Q2. How is state managed when middleware interrupts execution?
# A:  In frameworks like LangGraph, the conversation state is persisted in a database (like SQLite/PostgreSQL checkpointer).
#     The execution loop is paused, and when approval is received, the loop resumes using the saved state thread ID.
