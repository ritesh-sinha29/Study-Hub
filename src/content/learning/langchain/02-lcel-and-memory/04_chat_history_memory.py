# ==========================================================
# LANGCHAIN STUDY GUIDE: 04. CHAT HISTORY MEMORY
# ==========================================================

# --- CHAT HISTORY & PERSISTENCE ---
# Preserving the conversational thread requires keeping a history of messages.
# Modern LangChain handles this by wrapping a Runnable inside `RunnableWithMessageHistory`.
# We provide a `get_session_history` helper function that loads/persists the history 
# based on a unique `session_id`.

import os
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain.chat_models import init_chat_model

load_dotenv()

# Dictionary to hold conversational sessions in-memory
# In production, this can be backed by databases like Redis or Postgres (SQLChatMessageHistory)
sessions_db = {}

def get_session_history(session_id: str):
    if session_id not in sessions_db:
        sessions_db[session_id] = InMemoryChatMessageHistory()
    return sessions_db[session_id]

def demonstrate_chat_memory(model):
    print("--- 4. CHAT MEMORY WITH SESSION RUNNABLE ---")
    
    # 1. Define prompt containing a MessagesPlaceholder for the history
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a helpful assistant. Keep your answers brief."),
        MessagesPlaceholder(variable_name="history"),
        ("human", "{question}")
    ])
    
    # 2. Build the basic chain
    chain = prompt | model
    
    # 3. Wrap it with RunnableWithMessageHistory
    stateful_chain = RunnableWithMessageHistory(
        chain,
        get_session_history=get_session_history,
        input_messages_key="question",
        history_messages_key="history"
    )
    
    config_session_1 = {"configurable": {"session_id": "user_session_123"}}
    config_session_2 = {"configurable": {"session_id": "user_session_999"}}
    
    try:
        # Turn 1 (Session 1)
        res1 = stateful_chain.invoke({"question": "Hi, my name is Ritesh."}, config=config_session_1)
        print("User (Session 1): Hi, my name is Ritesh.")
        print("AI (Session 1):", res1.content)
        
        # Turn 2 (Session 2 - Different User/Thread)
        res2 = stateful_chain.invoke({"question": "What is my name?"}, config=config_session_2)
        print("\nUser (Session 2): What is my name?")
        print("AI (Session 2):", res2.content) # Model shouldn't know
        
        # Turn 3 (Session 1 - Resume first thread)
        res3 = stateful_chain.invoke({"question": "What is my name?"}, config=config_session_1)
        print("\nUser (Session 1): What is my name?")
        print("AI (Session 1):", res3.content) # Model should remember Ritesh
        
    except Exception as e:
        print("Memory invocation failed:", e)

if __name__ == "__main__":
    try:
        model = init_chat_model("gpt-4o-mini", model_provider="openai")
        demonstrate_chat_memory(model)
    except Exception as e:
        print("Model initialization failed:", e)

# ==========================================================
# REAL-LIFE USE CASES
# ==========================================================
# 1. WHATSAPP / TELEGRAM CHATBOTS: Automatically loads the user's history from SQLite or Redis 
#    based on their phone number/chat ID (`session_id`) and appends the new message context.
# 2. MULTI-USER WEB CHATS: Tracks user login sessions (`session_id`), separating discussions
#    and preventing one user from accessing another's conversation context.

# ==========================================================
# MNC INTERVIEW QUESTIONS & ANSWERS
# ==========================================================
# Q1. What is the benefit of `RunnableWithMessageHistory` over manual message appending?
# A:  It completely abstracts database load/save logic. It automatically reads the `session_id` 
#     from the `config` payload, queries the history database, injects it into the prompt placeholder, 
#     runs the chain, and writes the response back to database without manual intervention.
#
# Q2. How do you implement database-backed history instead of InMemoryChatMessageHistory?
# A:  Replace `InMemoryChatMessageHistory` in `get_session_history` with database-backed options 
#     such as `SQLChatMessageHistory` (using SQLAlchemy) or `RedisChatMessageHistory` by passing the 
#     appropriate connection string and session identifier.
