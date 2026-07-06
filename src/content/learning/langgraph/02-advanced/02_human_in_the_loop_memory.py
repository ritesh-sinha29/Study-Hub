# ==========================================================
# LANGGRAPH STUDY GUIDE: 02. HITL MEMORY INGESTION
# ==========================================================

# --- HUMAN-IN-THE-LOOP MEMORY INGESTION ---
# Adding facts to long-term vector/graph memory (Ingestion) can introduce errors or duplicate entries.
# To prevent this, advanced production systems use Human-in-the-Loop (HITL) checkpoints:
# 1. Node 1 (Extract Memory): Extracts facts from the conversation (e.g., "User likes Python").
# 2. Breakpoint: Graph interrupts execution BEFORE writing to database.
# 3. User Review: Human approves, edits, or rejects the extracted facts.
# 4. Node 2 (Ingest to DB): If approved, writes facts to Neo4j/Pinecone.

from typing import TypedDict, List
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver

# 1. Define State
class MemoryState(TypedDict):
    conversation_summary: str
    extracted_facts: List[str]
    is_approved: bool

# 2. Define Nodes
def extract_facts_node(state: MemoryState) -> dict:
    print("\nExecuting: extract_facts_node")
    # Simulate extracting facts from conversation
    facts = ["User is building a React app", "User prefers Python for backend"]
    return {"extracted_facts": facts}

def write_to_database_node(state: MemoryState) -> dict:
    print("\nExecuting: write_to_database_node")
    if state.get("is_approved", False):
        print("  - SUCCESS: Extracted facts committed to long-term database!")
    else:
        print("  - REJECTED: Facts rejected. Database write skipped.")
    return {}

# 3. Build Graph with Checkpointing
def build_hitl_memory_graph():
    builder = StateGraph(MemoryState)
    
    # Add Nodes
    builder.add_node("extractor", extract_facts_node)
    builder.add_node("writer", write_to_database_node)
    
    # Connections
    builder.add_edge(START, "extractor")
    builder.add_edge("extractor", "writer")
    builder.add_edge("writer", END)
    
    # Checkpointer is required to support interrupts
    memory = MemorySaver()
    
    # Compile graph with a breakpoint BEFORE running the 'writer' node
    return builder.compile(checkpointer=memory, interrupt_before=["writer"])

if __name__ == "__main__":
    graph = build_hitl_memory_graph()
    
    config = {"configurable": {"thread_id": "session_001"}}
    initial_input = {"conversation_summary": "We discussed deploying React with Python FastAPI today."}
    
    print("--- STARTING GRAPH RUN ---")
    # Initial execution
    graph.invoke(initial_input, config)
    
    # Inspect state at breakpoint
    state = graph.get_state(config)
    print(f"\n[BREAKPOINT HIT] Graph execution paused.")
    print(f"Extracted Facts waiting for review: {state.next}")
    print(f"Current State Values: {state.values.get('extracted_facts')}")
    
    # Human Action: Approve memory facts
    print("\n--- HUMAN ACTION: APPROVING FACTS AND RESUMING ---")
    
    # Update state: Set approval flag to True
    graph.update_state(config, {"is_approved": True}, as_node="extractor")
    
    # Resume execution by passing None as input
    graph.invoke(None, config)

# ==========================================================
# REAL-LIFE USE CASES
# ==========================================================
# 1. B2B SALES CRM COPILOT: Sales agent chats with client. Agent extracts follow-up tasks ("Email proposal
#    by Friday"). Before creating calendar alerts, the agent prompts the salesperson for approval.
# 2. MEDICAL MEDICAL RECORDING: Transcribing doctor-patient dialog. Extracted symptoms and prescriptions
#    are paused at a checkpoint for clinician review before final database insertion.

# ==========================================================
# MNC INTERVIEW QUESTIONS & ANSWERS
# ==========================================================
# Q1. Why use `interrupt_before` instead of implementing input check loops inside the node code?
# A:  Using `interrupt_before` leverages LangGraph's checkpointer to serialize and persist the state. 
#     It allows execution to freeze completely, releasing API and server compute resources while waiting 
#     minutes or days for a human response, resuming exactly where it left off without loss of context.
#
# Q2. How do you edit graph state values during a human-in-the-loop pause?
# A:  You call `graph.update_state(config, updates, as_node="node_name")`. The `as_node` parameter is crucial 
#     as it indicates which node wrote the values, ensuring write conflicts are handled cleanly and the 
#     graph state transition tracks correctly.
