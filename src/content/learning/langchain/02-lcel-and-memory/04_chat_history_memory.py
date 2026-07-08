# ========================================================================================
# LANGCHAIN CRASH COURSE — LCEL MODULE 04: CHAT HISTORY, MEMORY & SESSION MANAGEMENT
# ========================================================================================
#
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# SECTION 1 — THE STATELESS PROBLEM: WHY LLMs FORGET EVERYTHING
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#
# LLM APIs are completely stateless HTTP services. Every request is processed in
# total isolation — the model has zero memory of previous calls.
#
# PROBLEM (No memory):
#   Call 1: "My name is Ritesh."  → "Nice to meet you, Ritesh!"
#   Call 2: "What is my name?"   → "I don't know your name." ← Forgot!
#
# SOLUTION (With message history):
#   Call 1: [HumanMessage("My name is Ritesh.")]
#            → AIMessage("Nice to meet you, Ritesh!")
#   Call 2: [HumanMessage("My name is Ritesh."),
#             AIMessage("Nice to meet you, Ritesh!"),    ← previous context
#             HumanMessage("What is my name?")]
#            → AIMessage("Your name is Ritesh!")          ← remembers!
#
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# SECTION 2 — WHAT IS RunnableWithMessageHistory?
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#
# `RunnableWithMessageHistory` is a wrapper that automates the entire memory lifecycle:
#
#   STEP 1: Receive user input + session_id
#   STEP 2: Load existing history from database using session_id
#   STEP 3: Inject history into the prompt via MessagesPlaceholder
#   STEP 4: Run the chain with full context
#   STEP 5: Save the new user message + AI response back to the database
#   STEP 6: Return the AI response to the caller
#
# YOU just write the base chain. RunnableWithMessageHistory handles steps 1-6 automatically.
#
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# SECTION 3 — SESSION ID: HOW MULTI-USER MEMORY WORKS
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#
# Every user/conversation gets a unique `session_id`. This acts as a key to
# their message history in the database.
#
#  ┌──────────────────────────────────────────────────────────────────────┐
#  │                    MULTI-SESSION MEMORY ISOLATION                    │
#  │                                                                      │
#  │  session_id="user_123"  → history: ["Hi I'm Ritesh", "Nice to meet"] │
#  │  session_id="user_456"  → history: ["Hi I'm Priya", "Hello Priya!"]  │
#  │  session_id="user_789"  → history: []  (new user, no history yet)    │
#  │                                                                      │
#  │  Each session is completely isolated — Priya cannot see Ritesh's     │
#  │  conversation, and vice versa.                                       │
#  └──────────────────────────────────────────────────────────────────────┘
#
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# SECTION 4 — MEMORY STORAGE OPTIONS (In-Memory vs Persistent)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#
#  Storage Class                 │ Backend        │ Persistence │ Use Case
#  ──────────────────────────────┼────────────────┼─────────────┼─────────────────────
#  InMemoryChatMessageHistory    │ Python dict    │ ✗ Lost on   │ Local dev, testing
#                                │                │  restart    │
#  SQLChatMessageHistory         │ SQLite/Postgres│ ✓ Permanent │ Production web apps
#  RedisChatMessageHistory       │ Redis          │ ✓ Permanent │ High-traffic APIs
#  MongoDBChatMessageHistory     │ MongoDB        │ ✓ Permanent │ Document-based apps
#  DynamoDBChatMessageHistory    │ AWS DynamoDB   │ ✓ Permanent │ Serverless AWS apps
#
# For PRODUCTION, always use a persistent backend. InMemoryChatMessageHistory
# loses all conversation history every time the server restarts.
#
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# SECTION 5 — MESSAGES PLACEHOLDER: HOW HISTORY INJECTS INTO PROMPTS
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#
# The prompt template must have a `MessagesPlaceholder` where history is injected:
#
#   ChatPromptTemplate.from_messages([
#       ("system", "You are a helpful assistant."),
#       MessagesPlaceholder(variable_name="history"),   ← history injects here
#       ("human", "{question}")                          ← user's current message
#   ])
#
# At runtime, `MessagesPlaceholder` is replaced by the list of past messages
# loaded from the session history database.
#
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# SECTION 6 — LangGraph as the FUTURE of Memory (Important!)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#
# `RunnableWithMessageHistory` is still supported but for production multi-agent
# applications with complex state, branching, and human-in-the-loop, LangChain
# now recommends using LangGraph's `MemorySaver` checkpointer instead:
#
#   from langgraph.checkpoint.memory import MemorySaver
#   memory = MemorySaver()
#   graph = graph_builder.compile(checkpointer=memory)
#
# LangGraph's persistence layer supports cross-thread memory, breakpoints,
# time-travel debugging, and selective state updates — far beyond simple chat history.
#
# ========================================================================================

import os
from dotenv import load_dotenv

# Load API keys
load_dotenv()

from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain.chat_models import init_chat_model


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# IN-MEMORY SESSION STORE (replace with SQLChatMessageHistory in production)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

# Simulates a database of chat histories keyed by session_id
session_store: dict = {}

def get_session_history(session_id: str) -> InMemoryChatMessageHistory:
    """
    Retrieve or create the message history for a given session.

    In production, replace this body with:
        from langchain_community.chat_message_histories import SQLChatMessageHistory
        return SQLChatMessageHistory(
            session_id=session_id,
            connection_string="sqlite:///chat_history.db"
        )

    Args:
        session_id: Unique string identifier for the conversation thread.

    Returns:
        The chat message history object for this session.
    """
    if session_id not in session_store:
        session_store[session_id] = InMemoryChatMessageHistory()
        print(f"  [DB] Created new session: '{session_id}'")
    else:
        msg_count = len(session_store[session_id].messages)
        print(f"  [DB] Loaded session: '{session_id}' ({msg_count} messages in history)")
    return session_store[session_id]


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# EXAMPLE 1: MULTI-TURN CONVERSATION WITH SESSION ISOLATION
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def demonstrate_chat_memory(model):
    print("\n" + "="*70)
    print("EXAMPLE 1: MULTI-TURN MEMORY WITH SESSION ISOLATION")
    print("="*70)

    # 1. Define prompt with history placeholder
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a helpful assistant. Keep responses brief (1-2 sentences)."),
        MessagesPlaceholder(variable_name="history"),   # ← history injected here
        ("human", "{question}")
    ])

    # 2. Build the base chain (no memory awareness yet)
    chain = prompt | model

    # 3. Wrap with RunnableWithMessageHistory — this adds full memory lifecycle
    stateful_chain = RunnableWithMessageHistory(
        chain,
        get_session_history=get_session_history,
        input_messages_key="question",      # key in the input dict for the user's message
        history_messages_key="history"      # key used in the MessagesPlaceholder
    )

    # Two completely separate user sessions
    session_a = {"configurable": {"session_id": "ritesh-session"}}
    session_b = {"configurable": {"session_id": "priya-session"}}

    print("\n--- Session A (Ritesh) ---")

    # Turn 1 - Session A: Ritesh introduces himself
    print("  [A] Human: 'Hi, my name is Ritesh. I am a Python developer.'")
    res = stateful_chain.invoke({"question": "Hi, my name is Ritesh. I am a Python developer."}, config=session_a)
    print(f"  [A] AI   : '{res.content}'\n")

    # Turn 1 - Session B: Priya introduces herself (completely isolated)
    print("--- Session B (Priya) ---")
    print("  [B] Human: 'Hello, I am Priya. I work in data science.'")
    res = stateful_chain.invoke({"question": "Hello, I am Priya. I work in data science."}, config=session_b)
    print(f"  [B] AI   : '{res.content}'\n")

    # Turn 2 - Session A: Should remember Ritesh
    print("--- Session A Continues ---")
    print("  [A] Human: 'What is my name and what do I do?'")
    res = stateful_chain.invoke({"question": "What is my name and what do I do?"}, config=session_a)
    print(f"  [A] AI   : '{res.content}'\n")

    # Turn 2 - Session B: Should remember Priya (and NOT know about Ritesh)
    print("--- Session B Continues ---")
    print("  [B] Human: 'What is my name? And who else have you spoken to?'")
    res = stateful_chain.invoke({"question": "What is my name? And who else have you spoken to?"}, config=session_b)
    print(f"  [B] AI   : '{res.content}'")

    # Show the message counts per session
    print("\n--- Session History Summary ---")
    for sid, hist in session_store.items():
        print(f"  Session '{sid}': {len(hist.messages)} messages stored")


if __name__ == "__main__":
    try:
        model = init_chat_model("gpt-4o-mini", model_provider="openai")
        demonstrate_chat_memory(model)
    except Exception as e:
        print("\nSetup failed (check API keys):", e)


# ========================================================================================
# REAL-WORLD USE CASES
# ========================================================================================
#
# 1. WHATSAPP / TELEGRAM CHATBOTS:
#    - **Input**: User phone number serves as session_id.
#    - **Step 1**: Loads history from Redis and executes the chain.
#    - **Result**: Saves updated conversation thread and returns reply.
#
# 2. ENTERPRISE INTERNAL ASSISTANT:
#    - **Input**: Username acts as session_id.
#    - **Result**: Remembers past tickets, resolution status, and permission level.
#
# 3. EDUCATIONAL TUTORING PLATFORM:
#    - **Input**: Student session ID tracks progress.
#    - **Result**: Remembers covered topics, student confusion, and adjusts difficulty level.
#
# ========================================================================================
# MNC INTERVIEW QUESTIONS & ANSWERS
# ========================================================================================
#
# Q1. How do you replace InMemoryChatMessageHistory with a production database?
# A:  Replace the function body of `get_session_history` with a persistent backend:
#       from langchain_community.chat_message_histories import SQLChatMessageHistory
#       return SQLChatMessageHistory(
#           session_id=session_id,
#           connection_string="postgresql://user:password@localhost/chatdb"
#       )
#     The RunnableWithMessageHistory wrapper doesn't change — only the storage backend.
#
# Q2. Why is `MessagesPlaceholder` necessary? Can't you just append messages manually?
# A:  MessagesPlaceholder is required for RunnableWithMessageHistory to know WHERE
#     to inject the loaded history into the prompt. Without it, the history is loaded
#     from the database but has no place to go in the prompt template.
#
# Q3. When should you migrate from RunnableWithMessageHistory to LangGraph MemorySaver?
# A:  Migrate to LangGraph when you need:
#     - Multi-agent conversations (history across different agents)
#     - Conditional branching based on conversation state
#     - Human-in-the-loop approval steps mid-conversation
#     - Time-travel debugging (replay any point in conversation history)
#     - Long-term cross-thread memory (remember facts across separate sessions)
#     For simple single-agent chatbots, RunnableWithMessageHistory is sufficient.
