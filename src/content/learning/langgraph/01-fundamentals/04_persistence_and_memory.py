# ==========================================================
# LANGGRAPH STUDY GUIDE: 04. PERSISTENCE & MEMORY
# ==========================================================

# --- PERSISTENCE & CHECKPOINTING ---
# In production chatbots, the graph needs to remember previous conversations.
# LangGraph achieves memory out-of-the-box using Checkpointers.
# A Checkpointer saves the state of the graph after every node execution.
#
# When invoking the compiled graph, we pass a `thread_id` in the `config`.
# LangGraph automatically loads the saved state corresponding to that thread ID, 
# executes the new input, and saves the updated state.
#
# `MemorySaver` is a built-in, in-memory checkpointer useful for testing. 

from typing import Annotated
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.checkpoint.memory import MemorySaver
from langchain_core.messages import BaseMessage
from langchain.chat_models import init_chat_model

# 1. Define State Schema (preserving conversation history via add_messages)
class StateSchema(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]

# 2. Define standard model node
def call_model(state: StateSchema, model):
    print("Executing: call_model")
    response = model.invoke(state["messages"])
    return {"messages": [response]}

def build_stateful_graph(model, checkpointer):
    print("--- 4. BUILDING STATEFUL GRAPH ---")
    builder = StateGraph(StateSchema)
    
    # Add node
    builder.add_node("chatbot", lambda state: call_model(state, model))
    
    # Set pathways
    builder.add_edge(START, "chatbot")
    builder.add_edge("chatbot", END)
    
    # Compile the graph passing the checkpointer
    return builder.compile(checkpointer=checkpointer)

if __name__ == "__main__":
    # Initialize Checkpointer (in-memory)
    memory_checkpointer = MemorySaver()
    
    try:
        model = init_chat_model("gpt-4o-mini", model_provider="openai")
        graph = build_stateful_graph(model, memory_checkpointer)
        
        # Configure Thread IDs
        thread_1 = {"configurable": {"thread_id": "thread_abc"}}
        thread_2 = {"configurable": {"thread_id": "thread_xyz"}}
        
        # Turn 1 (Thread 1)
        print("\n--- Thread 1: Message 1 ---")
        input_1 = {"messages": [("user", "Hello, my favorite color is crimson.")]}
        res1 = graph.invoke(input_1, config=thread_1)
        print("Response:", res1["messages"][-1].content)
        
        # Turn 2 (Thread 2 - Different Thread)
        print("\n--- Thread 2: Message 1 ---")
        input_2 = {"messages": [("user", "What is my favorite color?")]}
        res2 = graph.invoke(input_2, config=thread_2)
        print("Response:", res2["messages"][-1].content) # Model shouldn't know
        
        # Turn 3 (Thread 1 - Back to Thread 1)
        print("\n--- Thread 1: Message 2 ---")
        input_3 = {"messages": [("user", "What is my favorite color?")]}
        res3 = graph.invoke(input_3, config=thread_1)
        print("Response:", res3["messages"][-1].content) # Model should remember
        
        # Inspecting state history
        print("\n--- Inspecting Thread 1 State History ---")
        state_history = list(graph.get_state_history(thread_1))
        print(f"Total historical checkpoints saved for Thread 1: {len(state_history)}")
        
    except Exception as e:
        print("Stateful memory graph execution failed (check API keys):", e)

# ==========================================================
# REAL-LIFE USE CASES
# ==========================================================
# 1. CUSTOMER PORTAL CHAT: Tracks the customer's conversation session (`thread_id` = user ID),
#    saving the context after each turn, enabling the agent to remember history even if the user
#    refreshes their browser.
# 2. AUDITING / TIME-TRAVEL: Restoring the system to a previous state. In LangGraph, since checkpoints
#    are saved per step, you can load a previous checkpoint's configuration and resume execution
#    from that point.

# ==========================================================
# MNC INTERVIEW QUESTIONS & ANSWERS
# ==========================================================
# Q1. What is the role of `thread_id` in LangGraph's persistence layer?
# A:  `thread_id` acts as a unique database key. When compiling a graph with a checkpointer, LangGraph
#     saves state values, message history, and execution points under this ID. Specifying the same
#     `thread_id` loads the corresponding session's database row, preserving state seamlessly.
#
# Q2. What is the difference between `MemorySaver` and database-backed checkpointers?
# A:  `MemorySaver` stores checkpoints in volatile RAM, which is deleted when the python process exits.
#     For production setups, LangGraph supports persistent database checkpointers like `SqliteSaver`
#     or `PostgresSaver` to persist state across process restarts.
