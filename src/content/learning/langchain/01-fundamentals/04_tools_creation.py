# ========================================================================================
# LANGCHAIN CRASH COURSE — MODULE 04: TOOLS, @tool DECORATOR & SCHEMA BINDING
# ========================================================================================
#
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# SECTION 1 — WHAT ARE TOOLS AND WHY DO WE NEED THEM?
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#
# LLMs are sealed boxes — they cannot see live data, write to databases, send
# emails, or call APIs. Tools are the bridge that let models interact with the
# real world.
#
# HOW TOOL CALLING WORKS (STEP BY STEP):
#   1. YOU define Python functions and decorate them with `@tool`.
#   2. LangChain serializes the function name, docstring, and argument types
#      into a JSON Schema (following OpenAPI standard).
#   3. You call `model.bind_tools([tool1, tool2])` — this attaches the schemas
#      to the model's system context.
#   4. When the user asks a question, the LLM reads all tool schemas and decides
#      whether it should call a tool. If yes, it responds with a structured
#      JSON payload (NOT plain text) specifying tool name + arguments.
#   5. YOUR APPLICATION parses that JSON, calls the actual Python function,
#      and returns a ToolMessage back to the model with the result.
#   6. The model reads the ToolMessage and generates the final natural language answer.
#
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# SECTION 2 — THE TOOL SCHEMA TRANSFER ARCHITECTURE
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#
#  ┌─────────────────────────────────────────────────────────────────────┐
#  │                    TOOL CALL DATA FLOW                              │
#  │                                                                     │
#  │  @tool function           JSON Schema (sent to LLM)                 │
#  │  def get_weather(         ┌─────────────────────────────────────┐   │
#  │    city: str              │ {                                   │   │
#  │  ) -> str:                │   "name": "get_weather",            │   │
#  │    """                    │   "description": "Get current...",  │   │
#  │    Get current weather.   │   "parameters": {                   │   │
#  │    """          ────────► │     "city": {"type": "string"}      │   │
#  │                           │   }                                 │   │
#  │                           │ }                                   │   │
#  │                           └─────────────────────────────────────┘   │
#  │                                        │                            │
#  │                           LLM Decision: "Call get_weather"          │
#  │                                        │                            │
#  │                           AIMessage.tool_calls = [                  │
#  │                             {"name": "get_weather",                 │
#  │                              "args": {"city": "London"},            │
#  │                              "id": "call_abc123"}                   │
#  │                           ]                                         │
#  └─────────────────────────────────────────────────────────────────────┘
#
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# SECTION 3 — THE CRITICAL IMPORTANCE OF DOCSTRINGS
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#
# WRONG (bad docstring):
#   @tool
#   def fetch_data(q: str) -> str:
#       """Get data."""          ← LLM has no idea what this does
#
# RIGHT (descriptive docstring):
#   @tool
#   def fetch_weather(city: str) -> str:
#       """
#       Retrieve current real-time weather conditions for a given city.
#       Use this tool when the user asks about temperature, rain, or weather.
#       """
#
# The docstring IS the tool's description sent to the model. Treat it like
# documentation for a human colleague who has no other context.
#
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# SECTION 4 — PYDANTIC ARGS_SCHEMA FOR COMPLEX INPUTS
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#
# For tools with multiple arguments or complex validation rules, define a Pydantic
# model as the `args_schema`. This gives each argument its own rich description,
# which is sent to the LLM as additional instruction on how to populate values.
#
# ========================================================================================

import os
from dotenv import load_dotenv

# Load API keys
load_dotenv()

from langchain_core.tools import tool
from langchain.chat_models import init_chat_model
from pydantic import BaseModel, Field


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# STEP 1: DEFINE TOOLS WITH @tool DECORATOR
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

# Simple tool — single string argument
@tool
def get_weather(city: str) -> str:
    """
    Retrieve current real-time weather conditions for a given city.
    Use this tool when the user asks about weather, temperature, rain, or climate.

    Args:
        city: The name of the city to get weather for (e.g., "London", "Tokyo").

    Returns:
        A string describing current weather conditions for the given city.
    """
    mock_data = {
        "london":   "London: Heavy Rain, 11°C, Humidity 85%",
        "tokyo":    "Tokyo: Sunny, 26°C, Humidity 55%",
        "new york": "New York: Cloudy, 18°C, Humidity 70%",
        "mumbai":   "Mumbai: Humid, 32°C, Humidity 90%",
    }
    return mock_data.get(city.lower(), f"Weather data unavailable for '{city}'.")


# Pydantic schema for structured complex inputs
class UserLookupArgs(BaseModel):
    username: str = Field(description="The exact username string to query in the database.")
    include_history: bool = Field(
        default=False,
        description="Set to True to also retrieve purchase history. Default is False."
    )

@tool(args_schema=UserLookupArgs)
def lookup_user_profile(username: str, include_history: bool = False) -> str:
    """
    Query the internal user database to retrieve a user's profile record.
    Use this tool when the user asks about a specific user's account, details, or history.

    Args:
        username: Exact username to query.
        include_history: Whether to include purchase history in the result.

    Returns:
        A string with the user's profile details from the database.
    """
    db = {
        "ritesh":  {"age": 24, "role": "Developer", "purchases": ["Python Course", "LCEL Guide"]},
        "krishna": {"age": 32, "role": "Architect", "purchases": ["System Design Book"]},
    }
    user = db.get(username.lower())
    if not user:
        return f"No user record found for username '{username}'."
    result = f"User: {username} | Age: {user['age']} | Role: {user['role']}"
    if include_history:
        result += f" | Purchases: {', '.join(user['purchases'])}"
    return result


# Math tool — returns integer
@tool
def calculate_power(base: int, exponent: int) -> int:
    """
    Calculate base raised to the power of exponent.
    Use this for exponential math calculations (e.g., 2^10 = 1024).

    Args:
        base: The base number.
        exponent: The exponent to raise the base to.

    Returns:
        The integer result of base ** exponent.
    """
    return base ** exponent


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# STEP 2: MANUALLY TEST TOOLS & INSPECT SCHEMAS
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

if __name__ == "__main__":
    print("="*70)
    print("STEP 1: TESTING TOOLS MANUALLY VIA .invoke()")
    print("="*70)

    # Tools are Runnables — you can invoke them directly without the model
    weather_result  = get_weather.invoke({"city": "London"})
    user_result     = lookup_user_profile.invoke({"username": "ritesh", "include_history": True})
    math_result     = calculate_power.invoke({"base": 2, "exponent": 10})

    print(f"  get_weather('London')          : {weather_result}")
    print(f"  lookup_user_profile('ritesh')  : {user_result}")
    print(f"  calculate_power(2, 10)         : {math_result}")

    # Inspect the auto-generated JSON schema (what the LLM receives)
    print("\n" + "="*70)
    print("STEP 2: INSPECTING AUTO-GENERATED TOOL JSON SCHEMA")
    print("="*70)
    print(f"  get_weather schema     : {get_weather.args_schema.schema()}")
    print(f"  calculate_power schema : {calculate_power.args_schema.schema()}")

    print("\n" + "="*70)
    print("STEP 3: BINDING TOOLS TO MODEL & TESTING TOOL CALL RESPONSE")
    print("="*70)

    try:
        model = init_chat_model("gpt-4o-mini", model_provider="openai")

        # bind_tools sends the tool schemas to the model in the system context
        tools = [get_weather, lookup_user_profile, calculate_power]
        model_with_tools = model.bind_tools(tools)

        # This prompt should trigger a tool call decision by the model
        query = "What is the weather like in London right now?"
        print(f"\n  User Query: '{query}'")
        response = model_with_tools.invoke(query)

        print(f"\n  Response type         : {type(response).__name__}")
        print(f"  Response content      : '{response.content}'")
        print(f"  Tool calls requested  : {response.tool_calls}")
    except Exception as e:
        print(f"\n  [ERROR] Model binding failed (check API keys): {e}")


# ========================================================================================
# REAL-WORLD USE CASES
# ========================================================================================
#
# 1. LIVE INVENTORY CHECK:
#    Customer asks: "Is the iPhone 15 Pro Max in stock in size 256GB?"
#    Agent calls: `check_inventory(product="iPhone 15 Pro Max", storage="256GB")`
#    Returns: "In stock: 47 units available."
#
# 2. CRM TICKET CREATION:
#    Support agent hears: "Please raise a P1 ticket for the payment gateway outage."
#    Agent calls: `create_ticket(severity="P1", description="Payment gateway outage")`
#    Creates the Jira/ServiceNow ticket and returns the ticket ID.
#
# 3. SMART HOME CONTROL:
#    User says: "Turn off all the lights in the bedroom."
#    Agent calls: `control_device(room="bedroom", device_type="lights", action="off")`
#
# ========================================================================================
# MNC INTERVIEW QUESTIONS & ANSWERS
# ========================================================================================
#
# Q1. How does the LLM communicate that it wants to call a tool?
# A:  The LLM doesn't execute code. It returns an AIMessage with an empty `.content`
#     string and a populated `.tool_calls` list. Each entry contains:
#       { "name": "get_weather", "args": {"city": "London"}, "id": "call_xyz" }
#     Your application reads this, runs the Python function, and returns a
#     ToolMessage with the result.
#
# Q2. What's the advantage of `args_schema` (Pydantic) over a plain function signature?
# A:  Pydantic Field descriptions give the LLM explicit instructions for each argument
#     (e.g., "Set to True only if the user explicitly requests history"). It also
#     validates input types at runtime, preventing bugs where the LLM passes a string
#     where an integer is required.
#
# Q3. Can a model call multiple tools in a single response?
# A:  Yes. Modern models support parallel tool calling. If you ask "What's the weather
#     in Tokyo AND London?", the model may return two tool_calls entries in one response.
#     Your application should process all of them before sending ToolMessages back.
