# ========================================================================================
# LANGCHAIN CRASH COURSE — MODULE 01: INTRODUCTION, ECOSYSTEM & ENVIRONMENT SETUP
# ========================================================================================
#
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# SECTION 1 — WHAT IS LANGCHAIN?
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#
# LangChain is a development framework that simplifies building applications powered
# by language models. It enables seamless integration of multiple AI models and data
# sources. It focuses on creating "chains" — sequences of operations — where language
# models can interact with databases, APIs, vector stores, and other models to perform
# complex tasks.
#
# Without LangChain, you would have to manually:
#   - Format prompt messages as structured JSON payloads for every API.
#   - Write custom code to handle streaming token-by-token responses.
#   - Manually manage tool definitions and serialize function signatures.
#   - Build your own state containers to preserve conversation history.
#   - Wire up retry/fallback logic every time a model provider has an outage.
#
# LangChain abstracts all of this into reusable, composable primitives.
#
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# SECTION 2 — THE LANGCHAIN ECOSYSTEM (PACKAGE ARCHITECTURE)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#
# LangChain is split into multiple focused packages. Each has a specific role:
#
#   ┌──────────────────────────────────────────────────────────────────────┐
#   │                    LANGCHAIN ECOSYSTEM MAP                           │
#   │                                                                      │
#   │  langchain-core       → Base abstractions: Runnable, prompts,       │
#   │                         messages, parsers (NO third-party deps)      │
#   │                                                                      │
#   │  langchain            → High-level chain builders, agent runtimes   │
#   │                         and convenience wrappers                     │
#   │                                                                      │
#   │  langchain-community  → Community-maintained integrations:          │
#   │                         Vector stores, doc loaders, APIs             │
#   │                                                                      │
#   │  Partner Packages     → Official, optimized integrations:           │
#   │  (langchain-openai,     maintained by model providers directly       │
#   │   langchain-anthropic,                                               │
#   │   langchain-google-genai)                                            │
#   │                                                                      │
#   │  LangSmith            → Cloud observability: trace, debug, eval     │
#   │                         every chain run visually                     │
#   │                                                                      │
#   │  LangGraph            → Advanced stateful agentic graphs            │
#   │                         (covered in the LangGraph module)            │
#   └──────────────────────────────────────────────────────────────────────┘
#
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# SECTION 3 — GENERATIVE AI VS. AUTONOMOUS AGENTS
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#
# 1. PLAIN LLM (GENERATIVE AI — PASSIVE RESPONDER):
#    - Input : "What is the weather in New York?"
#    - Output: Cannot answer accurately. LLMs have a training cutoff date.
#              They have no real-time internet access, no tools, no memory.
#              The model simply generates what statistically follows the input.
#
# 2. AUTONOMOUS AGENT (ACTIVE REASONER):
#    - Input: "What is the weather in New York?"
#    - Step 1 — THOUGHT:
#        The agent (model) thinks: "I cannot answer this from training data.
#        I need to call an external weather API tool to get real-time info."
#    - Step 2 — ACTION:
#        Agent calls: weather_tool(city="New York")
#    - Step 3 — OBSERVATION:
#        Tool returns: "New York: Partly Cloudy, 18°C"
#    - Step 4 — FINAL ANSWER:
#        Agent generates: "Currently in New York, it is partly cloudy at 18°C."
#
#    This THOUGHT → ACTION → OBSERVATION → ANSWER loop is called the
#    ReAct (Reasoning + Acting) loop, the foundation of all modern AI agents.
#
#  ┌──────────────────────────────────────────────────────────────────────┐
#  │                      COGNITIVE SPECTRUM                              │
#  │                                                                      │
#  │   PASSIVE LLM                              AUTONOMOUS AGENT         │
#  │   (Text In → Text Out)                     (Think → Tool → Answer)  │
#  │        │                                          │                  │
#  │        ▼                                          ▼                  │
#  │   "I don't know"                          weather_tool() →          │
#  │   (Hallucination risk)                    "18°C, Partly Cloudy"     │
#  └──────────────────────────────────────────────────────────────────────┘
#
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# SECTION 4 — SETUP WITH UV PACKAGE MANAGER
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#
# UV is an extremely fast Python package and project manager written in Rust.
# It replaces pip, pip-tools, pyenv, virtualenv, and poetry in a single binary.
#
# WHY UV OVER PIP?
#   - 10-100x faster dependency resolution using a parallel resolver engine.
#   - Built-in virtual environment management (no need for `venv` separately).
#   - Deterministic lock files (uv.lock) like npm's package-lock.json.
#
# SETUP COMMANDS:
#
# 1. Initialize a new project:
#    uv init
#
# 2. Create the virtual environment and install all dependencies:
#    uv sync
#
# 3. Add a new package:
#    uv add langchain langchain-openai python-dotenv
#
# 4. Run a Python script inside the virtual environment:
#    uv run python src/main.py
#
# 5. Add a development-only dependency (e.g. pytest):
#    uv add --dev pytest
#
# For this Study-Hub workspace, we use Poetry instead of UV, but the concepts
# are identical. To add packages here:
#    poetry add langchain langchain-openai python-dotenv
#    poetry run python <script_path>
#
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# SECTION 5 — ENVIRONMENT VARIABLES & .env FILE
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#
# API keys must NEVER be hardcoded in source files. They are stored in a
# `.env` file and loaded securely at runtime using `python-dotenv`.
#
# Create a file named `.env` in your project root:
#
#   OPENAI_API_KEY=sk-...
#   ANTHROPIC_API_KEY=sk-ant-...
#   GOOGLE_API_KEY=AIza...
#   LANGCHAIN_API_KEY=ls__...
#   LANGCHAIN_TRACING_V2=true
#   LANGCHAIN_PROJECT=study-hub
#
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# SECTION 6 — THE CORE RUNNABLE INTERFACE
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#
# Every LangChain object (models, prompts, tools, parsers) implements the
# Runnable interface. This means every component supports:
#
#   .invoke(input)        → Execute once, return result
#   .stream(input)        → Execute and yield result token-by-token
#   .batch([input1, ...]) → Execute multiple inputs concurrently
#   .ainvoke(input)       → Async version of invoke
#   .astream(input)       → Async version of stream
#   .abatch([...])        → Async version of batch
#
# This uniform interface is what makes LCEL (LangChain Expression Language)
# possible — you can chain any Runnable to any other Runnable using the pipe (|).
#
# ========================================================================================

import os
from dotenv import load_dotenv

# Load variables from the .env file into the process environment
load_dotenv()


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# EXAMPLE: SIMULATING THE ReAct AGENT LOOP (Educational Mock)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def weather_tool(city: str) -> str:
    """
    Mock external tool simulating a real-time weather API call.
    In production this would call OpenWeatherMap, Tomorrow.io, etc.

    Args:
        city: The name of the city to query weather for.

    Returns:
        A string describing the current weather condition.
    """
    # Simulated API response data
    mock_weather_db = {
        "new york":  "Partly Cloudy, 18°C, Wind: 12 km/h",
        "london":    "Heavy Rain, 11°C, Wind: 22 km/h",
        "tokyo":     "Sunny, 26°C, Wind: 5 km/h",
        "mumbai":    "Humid, 32°C, Wind: 8 km/h",
    }

    print(f"  [TOOL CALL] weather_tool(city='{city}') — Querying API...")
    result = mock_weather_db.get(city.lower(), "Weather data unavailable for this city.")
    return f"{city}: {result}"


def simulate_react_agent_loop(user_query: str):
    """
    Manually simulates the ReAct (Reasoning + Acting) agent cognitive loop.
    In real LangChain/LangGraph, this loop is automated by the agent runtime.
    """
    print("\n" + "="*70)
    print("SIMULATING: ReAct AGENT LOOP (Thought → Action → Observation)")
    print("="*70)

    print(f"\n  User Query: '{user_query}'")

    # STEP 1: THOUGHT — Agent decides it needs a tool
    print("\n  [THOUGHT]: I cannot answer this from training data.")
    print("             I need to invoke the weather_tool to get real-time data.")

    # STEP 2: ACTION — Agent calls the tool
    print("\n  [ACTION]: Calling weather_tool...")
    observation = weather_tool("New York")

    # STEP 3: OBSERVATION — Agent receives tool output
    print(f"\n  [OBSERVATION]: Tool returned: '{observation}'")

    # STEP 4: FINAL ANSWER — Agent synthesizes the result
    final_answer = f"Based on real-time data: {observation}. Dress accordingly!"
    print(f"\n  [FINAL ANSWER]: {final_answer}")
    print("="*70)


if __name__ == "__main__":
    print("="*70)
    print("LANGCHAIN MODULE 01 — ENVIRONMENT VERIFICATION")
    print("="*70)

    # Check which API keys are configured
    keys = {
        "OPENAI_API_KEY":    os.getenv("OPENAI_API_KEY"),
        "ANTHROPIC_API_KEY": os.getenv("ANTHROPIC_API_KEY"),
        "GOOGLE_API_KEY":    os.getenv("GOOGLE_API_KEY"),
        "LANGCHAIN_API_KEY": os.getenv("LANGCHAIN_API_KEY"),
    }

    print("\nAPI Key Status:")
    for key_name, key_val in keys.items():
        status = "✓ SET (Ready)" if key_val else "✗ NOT SET (Add to .env)"
        print(f"  {key_name:25s}: {status}")

    # Demonstrate the ReAct loop
    simulate_react_agent_loop("What is the weather in New York?")

    print("\n✓ Module 01 setup verification complete.")
    print("="*70)


# ========================================================================================
# REAL-WORLD USE CASES
# ========================================================================================
#
# 1. BUSINESS PROCESS AUTOMATION:
#    An email inbox agent receives a support ticket. The agent thinks: "This is
#    a billing dispute." It calls a DB tool, fetches invoice records, and drafts
#    a professional email reply — all without human intervention.
#
# 2. RESEARCH CO-PILOT:
#    A PDF research assistant splits documents into chunks, embeds them into a
#    vector store, and lets the user ask questions. The agent uses semantic search
#    to retrieve the most relevant paragraphs and synthesizes an answer.
#
# 3. LIVE STOCK PORTFOLIO ADVISOR:
#    User asks: "Should I sell my Apple shares today?"
#    The agent: calls a market data tool → calls a news sentiment tool → calls a
#    portfolio history tool → synthesizes a reasoned recommendation.
#
# ========================================================================================
# MNC INTERVIEW QUESTIONS & ANSWERS
# ========================================================================================
#
# Q1. What is the difference between langchain-core and langchain-community?
# A:  - `langchain-core` defines foundational interfaces (Runnables, Message types,
#       Prompt Templates, Output Parsers). It has zero third-party dependencies,
#       making it stable and suitable to be a base package.
#     - `langchain-community` contains third-party connectors contributed by the
#       open-source community (Pinecone, Chroma, Weaviate, Slack loaders, etc.).
#       Breaking changes here don't affect the core engine.
#
# Q2. Why must agent tools always have detailed docstrings?
# A:  The model reads tool descriptions to decide WHICH tool to call and HOW to
#     call it. Docstrings and argument type hints are serialized into the OpenAI
#     `tools` parameter JSON schema and sent to the model. If descriptions are
#     vague, the LLM calls the wrong tool or hallucinates argument values.
#
# Q3. What is the ReAct pattern and where does it come from?
# A:  ReAct (Reasoning and Acting) is a prompting strategy from a 2022 Google
#     paper by Yao et al. It interleaves chain-of-thought reasoning (Thought)
#     with external tool actions (Act) and collects their results (Observe) in
#     an iterative loop until the agent produces a final answer. LangGraph agents
#     implement this natively via state machine graphs.
#
# Q4. Why use .env files instead of hardcoding API keys?
# A:  Hardcoded keys in source files get exposed in version control history
#     (git log) and can be scraped by automated credential-harvesting bots.
#     .env files are gitignored, keeping secrets out of the repository entirely.
