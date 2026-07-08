# ========================================================================================
# LANGCHAIN CRASH COURSE — MODULE 05: MESSAGE TYPES, SCHEMAS & CONVERSATION LIFECYCLE
# ========================================================================================
#
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# SECTION 1 — WHY MESSAGES INSTEAD OF PLAIN STRINGS?
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#
# Raw LLM APIs (OpenAI, Anthropic) use a structured message array format, NOT plain
# text strings. This structure lets the model understand WHO is speaking (role) and
# WHAT was said (content), enabling multi-turn conversations and behavior control.
#
# LangChain provides Python classes that map directly to these API roles:
#
#  ┌──────────────────────────────────────────────────────────────────────┐
#  │              LANGCHAIN MESSAGE CLASS ↔ API ROLE MAPPING              │
#  │                                                                      │
#  │  LangChain Class    │ API Role    │ Purpose                          │
#  │  ───────────────────┼─────────────┼────────────────────────────────  │
#  │  SystemMessage      │ "system"    │ Sets model persona, rules,       │
#  │                     │             │ boundaries (sent once at start)  │
#  │  HumanMessage       │ "user"      │ The user's query or message      │
#  │  AIMessage          │ "assistant" │ The model's generated response   │
#  │  ToolMessage        │ "tool"      │ The result returned from a       │
#  │                     │             │ tool execution back to the model │
#  └──────────────────────────────────────────────────────────────────────┘
#
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# SECTION 2 — CONVERSATION STATE & STATELESS LLM PROBLEM
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#
# LLM APIs are completely STATELESS. Every HTTP request is independent. The model
# has NO memory of previous calls unless you send the history manually.
#
# To maintain a conversation thread, you must:
#   1. Keep an in-memory list of messages.
#   2. Append every user query (HumanMessage) and model reply (AIMessage) to it.
#   3. Send THE ENTIRE LIST on every new API call.
#
# This is why ChatGPT "remembers" your conversation — it sends your entire history
# on every message behind the scenes.
#
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# SECTION 3 — MULTI-TURN CONVERSATION LIFECYCLE
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#
#  TURN 1:
#  messages = [
#    SystemMessage("You are a tutor."),    ← sets persona
#    HumanMessage("What is Python?")       ← user's question
#  ]
#  response = model.invoke(messages)       → AIMessage("Python is a language...")
#
#  TURN 2 (append previous messages + new query):
#  messages.append(response)              ← AI's previous answer
#  messages.append(HumanMessage("Give me an example."))
#  response = model.invoke(messages)       → AIMessage("Here's an example: ...")
#
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# SECTION 4 — THE TOOLMESSAGE & TOOL_CALL_ID LINKING
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#
# When the model requests a tool call, the AIMessage contains:
#   .tool_calls = [{"name": "get_stock", "args": {"ticker": "AAPL"}, "id": "call_xyz"}]
#
# The application executes the tool and returns a ToolMessage:
#   ToolMessage(content="AAPL: $182.50", tool_call_id="call_xyz")
#
# The `tool_call_id` acts like a foreign key — it tells the model which tool result
# matches which tool request. This matters when multiple tools are called in parallel.
#
# ========================================================================================

import os
from dotenv import load_dotenv

# Load API keys
load_dotenv()

from langchain_core.messages import SystemMessage, HumanMessage, AIMessage, ToolMessage
from langchain.chat_models import init_chat_model


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# EXAMPLE 1: MULTI-TURN CONVERSATION WITH MESSAGE HISTORY
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def demonstrate_multi_turn_conversation(model):
    print("\n" + "="*70)
    print("EXAMPLE 1: MULTI-TURN CONVERSATION WITH MANUAL HISTORY")
    print("="*70)

    # Start the conversation thread with a system persona
    messages = [
        SystemMessage(content=(
            "You are a concise software engineering tutor. "
            "Answer in bullet points. Keep each answer under 50 words."
        )),
        HumanMessage(content="What is a callback function in JavaScript?")
    ]

    print("  System: You are a concise software engineering tutor.")
    print("  Human : What is a callback function in JavaScript?")

    try:
        # Turn 1
        response_1 = model.invoke(messages)
        print(f"\n  AI    : {response_1.content}")

        # IMPORTANT: Append the AI's response to maintain conversation context
        messages.append(response_1)

        # Turn 2: Follow-up question — model will use previous context
        follow_up = HumanMessage(content="Give me a simple code example of that.")
        messages.append(follow_up)
        print(f"\n  Human : Give me a simple code example of that.")

        response_2 = model.invoke(messages)
        print(f"\n  AI    : {response_2.content}")

        # Show the total message history built up
        print(f"\n  Total messages in history: {len(messages) + 1}")
        print(f"  Message types in history : {[type(m).__name__ for m in messages + [response_2]]}")

    except Exception as e:
        print(f"  [ERROR] Conversation failed: {e}")


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# EXAMPLE 2: TOOLMESSAGE STRUCTURE & ID LINKING
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def demonstrate_tool_message_linking():
    print("\n" + "="*70)
    print("EXAMPLE 2: TOOLMESSAGE ID LINKING STRUCTURE")
    print("="*70)

    # Simulate the AI returning a tool call request
    ai_tool_request = AIMessage(
        content="",  # Empty — the model is requesting a tool, not generating text
        tool_calls=[
            {
                "name":  "get_stock_price",
                "args":  {"ticker": "AAPL"},
                "id":    "call_abc123",          # Unique ID for this specific tool call
                "type":  "tool_call"
            }
        ]
    )

    print("  AI returned tool_calls (not text):")
    print(f"    Tool name  : {ai_tool_request.tool_calls[0]['name']}")
    print(f"    Tool args  : {ai_tool_request.tool_calls[0]['args']}")
    print(f"    Tool ID    : {ai_tool_request.tool_calls[0]['id']}")

    # Application executes the tool — mock response
    tool_execution_result = "AAPL: $182.50 (+1.23%)"

    # Wrap result in ToolMessage, referencing the exact same tool_call_id
    tool_response_msg = ToolMessage(
        content=tool_execution_result,
        tool_call_id="call_abc123"   # MUST match the id in ai_tool_request
    )

    print(f"\n  ToolMessage constructed:")
    print(f"    Content       : {tool_response_msg.content}")
    print(f"    tool_call_id  : {tool_response_msg.tool_call_id}")
    print(f"\n  Now send [ai_tool_request, tool_response_msg] back to model")
    print(f"  for final answer generation.")


if __name__ == "__main__":
    try:
        model = init_chat_model("gpt-4o-mini", model_provider="openai")
        demonstrate_multi_turn_conversation(model)
        demonstrate_tool_message_linking()
    except Exception as e:
        print("\nSetup failed (check API keys):", e)


# ========================================================================================
# REAL-WORLD USE CASES
# ========================================================================================
#
# 1. CUSTOMER HELPDESK SYSTEM:
#    - **Input**: Support chat conversation session.
#    - **Step 1**: Stores messages list containing SystemMessage, HumanMessage, and AIMessage.
#    - **Step 2**: Sends the full message history on each user turn.
#    - **Result**: Ensures the model retains full context of what has been tried.
#
# 2. ROLE-BASED ACCESS CONTROL:
#    - **Input**: SystemMessage instructing: "You are an internal HR assistant. Never reveal employee salaries."
#    - **Result**: Serves as the primary security layer to block prompt injection attempts.
#
# 3. MULTI-TOOL PARALLEL EXECUTION:
#    - **Step 1**: Model calls get_stock_price("AAPL") and get_stock_price("GOOGL") simultaneously.
#    - **Step 2**: Returns two ToolMessages containing the individual results.
#    - **Result**: Model reads both responses and synthesizes a comparative answer.
#
# ========================================================================================
# MNC INTERVIEW QUESTIONS & ANSWERS
# ========================================================================================
#
# Q1. Why is `tool_call_id` mandatory inside a ToolMessage?
# A:  When the model makes multiple parallel tool calls in one turn, it needs to
#     know which result corresponds to which request. The `tool_call_id` acts as
#     a foreign key — your application returns one ToolMessage per tool_call_id,
#     and the model matches them correctly before generating the final answer.
#
# Q2. What happens if you send a HumanMessage without a SystemMessage?
# A:  The model uses its default persona. Without a SystemMessage, it behaves as
#     a general-purpose assistant with no boundaries. In production, you always want
#     a SystemMessage to enforce persona, tone, language restrictions, and safety
#     guidelines (e.g., "Do not discuss competitor products").
#
# Q3. What is the difference between AIMessage and AIMessageChunk?
# A:  - AIMessage: Complete response from `.invoke()`. Has full `.content` and
#       `.response_metadata` (token counts, model name, finish reason).
#     - AIMessageChunk: Partial token from `.stream()`. Multiple chunks concatenate
#       to form the final AIMessage using the `+` operator.
