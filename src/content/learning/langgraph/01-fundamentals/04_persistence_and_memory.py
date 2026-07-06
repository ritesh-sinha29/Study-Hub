# ========================================================================================
# LANGGRAPH CRASH COURSE — MODULE 04: PERSISTENCE, CHECKPOINTING & THREAD MEMORY
# ========================================================================================
#
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# SECTION 1 — THE STATELESS PROBLEM IN PRODUCTION
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#
# Without persistence, every call to `graph.invoke()` starts completely fresh.
# When a user closes their browser or the server restarts, ALL conversation history
# is gone. The bot acts like it never met the user before.
#
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# SECTION 2 — WHAT IS A CHECKPOINTER?
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#
# A Checkpointer is a persistence backend that LangGraph plugs into your graph.
# After EVERY node execution, it automatically saves a snapshot (checkpoint) of the
# full graph state to a database.
#
# HOW IT WORKS:
#   1. graph.invoke(input, config={"configurable": {"thread_id": "abc123"}})
#   2. LangGraph looks up thread_id "abc123" in the checkpointer database.
#   3. If found: loads the previous state and appends the new input.
#   4. If not found: creates a new session.
#   5. After each node runs: saves a new checkpoint for thread_id "abc123".
#
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# SECTION 3 — THREAD ID: MULTI-USER ISOLATION
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#
# `thread_id` is a string identifier for one conversation session. Each unique
# thread_id gets its own isolated state history in the database.
#
#  ┌────────────────────────────────────────────────────────────┐
#  │                  CHECKPOINTER DATABASE                     │
#  │                                                            │
#  │  thread_id: "user_ritesh"  → checkpoint_1, checkpoint_2   │
#  │  thread_id: "user_priya"   → checkpoint_1                  │
#  │  thread_id: "user_raj"     → checkpoint_1, checkpoint_2,  │
#  │                               checkpoint_3                 │
#  └────────────────────────────────────────────────────────────┘
#
#  Ritesh cannot see Priya's state. Each session is fully isolated.
#
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# SECTION 4 — CHECKPOINTER OPTIONS
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#
#  Checkpointer Class      │ Backend          │ Persistent │ Use Case
#  ────────────────────────┼──────────────────┼────────────┼─────────────────────────
#  MemorySaver             │ Python dict      │ ✗ RAM only │ Local dev, unit tests
#  SqliteSaver             │ SQLite file      │ ✓ Disk     │ Single-server production
#  PostgresSaver           │ PostgreSQL       │ ✓ Database │ Multi-server, enterprise
#  AsyncPostgresSaver      │ Async PostgreSQL │ ✓ Database │ High-concurrency APIs
#
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# SECTION 5 — TIME-TRAVEL DEBUGGING WITH get_state_history()
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#
# Because every node execution is checkpointed, you can replay any historical state:
#
#   history = list(graph.get_state_history(config))
#   # Each entry is a StateSnapshot with .values, .next, .config, .created_at
#
#   past_checkpoint = history[2]   # 3rd checkpoint from latest
#   graph.invoke(None, config=past_checkpoint.config)   # resume from that point
#
# This is called "time-travel" — you can reset the graph to any past state and
# re-run from that point forward, e.g. to debug an error that happened mid-execution.
#
# ========================================================================================

from typing import Annotated
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.checkpoint.memory import MemorySaver
from langchain_core.messages import BaseMessage
from langchain.chat_models import init_chat_model


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# STATE & NODE
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

class StateSchema(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]


def call_model(state: StateSchema, model) -> dict:
    """Chatbot node: passes full message history to the LLM and returns the response."""
    print("  [Node] call_model executing...")
    response = model.invoke(state["messages"])
    print(f"  [Node] AI response: '{response.content[:80]}'")
    return {"messages": [response]}


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# GRAPH CONSTRUCTION WITH CHECKPOINTER
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def build_stateful_graph(model, checkpointer) -> object:
    """
    Builds and compiles a stateful chatbot graph.

    KEY DIFFERENCE from a stateless graph:
      graph = builder.compile(checkpointer=checkpointer)
                              ^^^^^^^^^^^^^^^^^^^^^^^^^^
    Passing the checkpointer here enables automatic state persistence
    after every node execution. Without this, every invoke() starts fresh.
    """
    print("\n" + "="*70)
    print("BUILDING STATEFUL GRAPH WITH CHECKPOINTER")
    print("="*70)

    builder = StateGraph(StateSchema)
    builder.add_node("chatbot", lambda state: call_model(state, model))
    builder.add_edge(START, "chatbot")
    builder.add_edge("chatbot", END)

    # Passing checkpointer enables persistence
    return builder.compile(checkpointer=checkpointer)


if __name__ == "__main__":
    memory_checkpointer = MemorySaver()

    try:
        model = init_chat_model("gpt-4o-mini", model_provider="openai")
        graph = build_stateful_graph(model, memory_checkpointer)

        # thread_id isolates each user's conversation
        thread_ritesh = {"configurable": {"thread_id": "ritesh-thread"}}
        thread_priya  = {"configurable": {"thread_id": "priya-thread"}}

        # ── Thread 1, Turn 1: Ritesh tells the bot his color preference
        print("\n--- RITESH | Turn 1: Introducing preference ---")
        graph.invoke(
            {"messages": [("user", "Hello, my favorite color is crimson.")]},
            config=thread_ritesh
        )

        # ── Thread 2, Turn 1: Priya has an ISOLATED session
        print("\n--- PRIYA | Turn 1: Asking (knows nothing about Ritesh) ---")
        res = graph.invoke(
            {"messages": [("user", "What is my favorite color?")]},
            config=thread_priya
        )
        print("  Priya's session response:", res["messages"][-1].content)

        # ── Thread 1, Turn 2: Ritesh's session should REMEMBER his preference
        print("\n--- RITESH | Turn 2: Testing memory ---")
        res = graph.invoke(
            {"messages": [("user", "What is my favorite color?")]},
            config=thread_ritesh
        )
        print("  Ritesh's session response:", res["messages"][-1].content)

        # ── Time-travel: inspect checkpointed history for Ritesh's thread
        print("\n--- INSPECTING RITESH'S CHECKPOINT HISTORY ---")
        state_history = list(graph.get_state_history(thread_ritesh))
        print(f"  Total checkpoints saved for Ritesh's thread: {len(state_history)}")
        for i, snapshot in enumerate(state_history):
            print(f"  Checkpoint {i}: {len(snapshot.values.get('messages', []))} messages, next={snapshot.next}")

    except Exception as e:
        print("\nStateful graph failed (check API keys):", e)


# ========================================================================================
# REAL-WORLD USE CASES
# ========================================================================================
#
# 1. CUSTOMER SUPPORT PORTAL:
#    thread_id = customer's ticket number. The agent remembers every interaction
#    across multiple days. If the customer calls back, the agent knows their full
#    history without asking them to repeat themselves.
#
# 2. LONG-RUNNING DOCUMENT ANALYSIS:
#    A large PDF analysis graph runs for 30 minutes, processing hundreds of pages.
#    Each page extraction is checkpointed. If the server crashes at page 150, the
#    graph resumes at page 151 on restart — zero rework.
#
# 3. AUDIT TRAIL (Compliance):
#    Every checkpoint is a timestamped record of exactly what state the agent was in
#    at every step. For financial or medical agents, this provides a complete audit
#    trail for regulatory compliance (who said what, when, what decision was made).
#
# ========================================================================================
# MNC INTERVIEW QUESTIONS & ANSWERS
# ========================================================================================
#
# Q1. What is the role of `thread_id` in LangGraph's checkpointing system?
# A:  `thread_id` is the primary key for storing and retrieving state snapshots.
#     When you call `graph.invoke(input, config={"configurable": {"thread_id": "abc"}})`,
#     LangGraph saves all state under "abc". The next call with the same thread_id
#     loads that state and continues from where it left off, enabling persistent memory.
#     Different thread_ids are completely isolated — perfect for multi-user applications.
#
# Q2. What is the difference between MemorySaver and PostgresSaver?
# A:  - MemorySaver: Stores checkpoints in a Python dictionary (RAM). Fast for dev/tests
#       but ALL data is lost when the Python process exits. Never use in production.
#     - PostgresSaver: Stores checkpoints in a PostgreSQL database. Survives server
#       restarts, supports horizontal scaling across multiple servers, and can store
#       millions of thread histories. Required for production deployments.
#
# Q3. What is time-travel in LangGraph and why is it valuable?
# A:  Because LangGraph checkpoints state after every node, you can access any historical
#     snapshot using `graph.get_state_history(config)`. You can then resume execution
#     from any past checkpoint using `graph.invoke(None, config=past_checkpoint.config)`.
#     This enables: (a) debugging by replaying a failed run from just before the error,
#     (b) A/B testing different logic paths from the same starting state, and
#     (c) recovering from mistakes without restarting the entire workflow.
