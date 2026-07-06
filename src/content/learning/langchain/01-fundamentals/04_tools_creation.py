# ==========================================================
# LANGCHAIN STUDY GUIDE: 04. TOOLS CREATION
# ==========================================================

# --- WHAT ARE TOOLS? ---
# Tools are interfaces that allow agents to interact with external systems (e.g., databases, APIs, web search).
# In LangChain, tools can be easily created using the `@tool` decorator from `langchain_core.tools` or `langchain.tools`.
#
# --- THE ROLE OF DOCSTRINGS ---
# The LLM determines which tool to call based on the tool's name and description.
# When using the `@tool` decorator, the function's docstring is automatically converted into the tool's description.
# Therefore, writing clear, concise docstrings is critical so the LLM understands when and how to call the tool.

import os
from dotenv import load_dotenv
from langchain_core.tools import tool
from langchain.chat_models import init_chat_model

load_dotenv()

# 1. DEFINE TOOLS USING THE @tool DECORATOR
@tool
def add_numbers(a: int, b: int) -> int:
    """Add two numbers together. Use this tool for mathematical addition queries."""
    return a + b

@tool
def fetch_user_age(username: str) -> str:
    """Fetch the age of a user from the database. Pass the exact username string."""
    # Mocking database behavior
    db = {"ritesh": "24", "krishna": "32"}
    return f"User '{username}' is {db.get(username.lower(), 'unknown')} years old."

if __name__ == "__main__":
    # Test executing tools manually
    print("--- 1. MANUALLY RUNNING TOOLS ---")
    print("add_numbers result:", add_numbers.invoke({"a": 12, "b": 15}))
    print("fetch_user_age result:", fetch_user_age.invoke({"username": "ritesh"}))
    
    # 2. BINDING TOOLS TO A MODEL
    try:
        model = init_chat_model("gpt-4o-mini", model_provider="openai")
        # Bind tools to the model
        model_with_tools = model.bind_tools([add_numbers, fetch_user_age])
        
        # Test if the model decides to use a tool
        response = model_with_tools.invoke("How old is Ritesh?")
        print("\n--- 2. TOOL CALL DECISION BY LLM ---")
        print("Tool Calls detected:", response.tool_calls)
    except Exception as e:
        print("\nModel tool-binding omitted or failed (check API keys):", e)

# ==========================================================
# REAL-LIFE USE CASES
# ==========================================================
# 1. DATABASE SEARCH: An agent uses a search tool to run SQL queries against a database when a user
#    asks for statistical reports.
# 2. EMAIL AUTOMATION: An agent calls a `send_email` tool to dispatch notifications after completing
#    a user support query.

# ==========================================================
# MNC INTERVIEW QUESTIONS & ANSWERS
# ==========================================================
# Q1. How does an LLM know which tool to call and with what parameters?
# A:  When you bind tools to a model, the tool names, function signatures (parameter names and types),
#     and description (docstring) are converted into a JSON schema format and sent to the LLM.
#     The LLM reads this schema and outputs a special structured tool call specifying the tool name
#     and argument dictionary.
#
# Q2. What is the difference between `@tool` decorator and subclassing `BaseTool`?
# A:  - `@tool`: Best and quickest way for simple functions. Uses docstring and function signature.
#     - `BaseTool` subclassing: Better for complex cases requiring custom validation, state management,
#       or multiple output formats.
