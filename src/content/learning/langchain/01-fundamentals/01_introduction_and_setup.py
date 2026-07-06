# ==========================================================
# LANGCHAIN STUDY GUIDE: 01. INTRODUCTION & SETUP
# ==========================================================

# --- WHAT IS LANGCHAIN? ---
# LangChain is a development framework that simplifies building applications powered by language models,
# enabling seamless integration of multiple AI models and data sources.
# It focuses on creating chains, or sequences, of operations where language models can interact with
# databases, APIs, and other models to perform complex tasks.

# --- GENERATIVE AI VS AUTONOMOUS AGENTS ---
# 1. Plain LLM (Generative AI):
#    - Input: "What is the weather in New York?"
#    - Output: Cannot answer accurately because LLMs have a cutoff training date and no real-time internet access.
# 2. Autonomous Agent:
#    - Input: "What is the weather in New York?"
#    - Agent Logic: The model identifies it doesn't know the real-time weather, decides to call a weather tool/API,
#      retrieves the context (weather is sunny), and generates the final output.

# --- SETUP WITH UV PACKAGE MANAGER ---
# UV is an extremely fast Python package manager written in Rust.
# 1. Initialize a new project:
#    uv init
# 2. Create a virtual environment:
#    uv venv
# 3. Activate the environment:
#    - Windows: .venv\Scripts\activate
#    - macOS/Linux: source .venv/bin/activate
# 4. Install requirements:
#    uv add -r requirements.txt
#    Or add individually: uv add langchain langchain-openai python-dotenv

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Example mock tool function
def get_weather(city: str) -> str:
    """Get the weather for a city."""
    return f"The weather in {city} is sunny."

# Setting up keys (Make sure to have a .env file with your API keys)
# GOOGLE_API_KEY=your_key
# GROQ_API_KEY=your_key
# OPENAI_API_KEY=your_key
openai_api_key = os.getenv("OPENAI_API_KEY")

# ----------------------------------------------------------
# HOW TO RUN THIS FILE
# ----------------------------------------------------------
# Make sure you have python-dotenv and langchain installed.
# Run:
#   python 01_introduction_and_setup.py
# ----------------------------------------------------------

if __name__ == "__main__":
    print("LangChain environment loaded successfully.")
    print("API Key loaded:", "Yes" if openai_api_key else "No")
    
# ==========================================================
# REAL-LIFE USE CASES
# ==========================================================
# 1. CUSTOMER SUPPORT CHATBOTS: Agents route user inquiries to either a database lookup, 
#    a live chat agent, or answer automatically using stored product documentation.
# 2. FINANCIAL PORTFOLIO ANALYZER: Uses agents to fetch live stock prices from APIs, 
#    perform calculations, and generate recommendation reports.

# ==========================================================
# MNC INTERVIEW QUESTIONS & ANSWERS
# ==========================================================
# Q1. What is the main value proposition of LangChain?
# A:  It provides standard interfaces, integrations, and ready-made chains for connecting
#     LLMs with external data sources and tools, reducing boilerplate code significantly.
#
# Q2. Why do we need UV package manager instead of traditional pip?
# A:  UV is written in Rust and is 10-100x faster than pip. It resolves dependencies 
#     faster and acts as an all-in-one project/virtual-env manager.
