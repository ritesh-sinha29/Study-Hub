# ==========================================================
# LANGGRAPH STUDY GUIDE: 05. HUMAN IN THE LOOP
# ==========================================================

# --- HUMAN IN THE LOOP (HITL) ---
# For critical tasks (such as executing financial transactions or updating customer databases),
# we need humans to verify and approve actions before they execute.
#
# LangGraph natively supports HITL using Breakpoints.
# When compiling the graph, you can specify `interrupt_before` or `interrupt_after` a list of nodes.
#
# Execution halts when it hits a breakpoint. The state is saved.
# A human can then:
# 1. Inspect the state values.
# 2. Update the state (modifying inputs/message values).
# 3. Resume the graph from where it paused.

from typing import Annotated
from typing_extensions import TypedDict
from langchain_core.tools import tool
from langchain_core.messages import BaseMessage
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.checkpoint.memory import MemorySaver
from langgraph.prebuilt import ToolNode
from langchain.chat_models import init_chat_model

# 1. Define sensitive tool
@tool
def execute_bank_transfer(amount: int, recipient: str) -> str:
    """Execute a bank transfer to a recipient."""
    return f"Successfully transferred ${amount} to {recipient}."

class AgentState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]

def call_model(state: AgentState, model):
    print("Executing: call_model")
    return {"messages": [model.invoke(state["messages"])]}

def build_hitl_agent(model, tools, checkpointer):
    print("--- 5. BUILDING HUMAN-IN-THE-LOOP AGENT ---")
    builder = StateGraph(AgentState)
    
    # Add nodes
    builder.add_node("agent", lambda state: call_model(state, model))
    builder.add_node("action", ToolNode(tools))
    
    # Establish links
    builder.add_edge(START, "agent")
    
    def should_continue(state: AgentState) -> str:
        last_message = state["messages"][-1]
        if last_message.tool_calls:
            return "action"
        return END
        
    builder.add_conditional_edges(
        "agent",
        should_continue,
        {
            "action": "action",
            END: END
        }
    )
    builder.add_edge("action", "agent")
    
    # 2. Compile the graph with a checkpointer and interrupt breakpoints
    # We halt execution immediately BEFORE hitting the "action" (tool) node
    return builder.compile(
        checkpointer=checkpointer,
        interrupt_before=["action"]
    )

if __name__ == "__main__":
    checkpointer = MemorySaver()
    tools_list = [execute_bank_transfer]
    
    try:
        model = init_chat_model("gpt-4o-mini", model_provider="openai")
        model_with_tools = model.bind_tools(tools_list)
        
        # Compile agent with breakpoints
        agent = build_hitl_agent(model_with_tools, tools_list, checkpointer)
        
        thread_config = {"configurable": {"thread_id": "transfer_thread_1"}}
        query = {"messages": [("user", "Transfer $500 to John Doe please.")]}
        
        print("\n--- Starting Thread Execution ---")
        # Run graph. It will execute the agent node, see the tool call,
        # but halt BEFORE running the 'action' (tool) node.
        initial_run = agent.invoke(query, config=thread_config)
        
        # Check current state of the thread
        current_state = agent.get_state(thread_config)
        print("\nGraph State after pause:")
        print(f"Next Node to Execute: {current_state.next}")
        print("Last Message Content:", current_state.values["messages"][-1])
        
        # 3. Simulate Human Approval / Intervention
        print("\n--- Human Approval Phase ---")
        user_approval = "yes" # In real apps, this is captured from a button/UI click
        
        if user_approval.lower() == "yes":
            print("Human approved the action. Resuming execution...")
            # To resume, call invoke passing None as the input (it reads the saved checkpoint)
            res = agent.invoke(None, config=thread_config)
            print("\nFinal State Output:")
            for msg in res["messages"]:
                print(f"[{msg.type.upper()}]: {msg.content}")
        else:
            print("Human rejected the action. Terminating execution.")
            
    except Exception as e:
        print("HITL execution failed (check API keys):", e)

# ==========================================================
# REAL-LIFE USE CASES
# ==========================================================
# 1. WIRE TRANSFERS / BILLING: Before charging credit cards or moving funds, the system triggers
#    a breakpoint, prompting the admin/user to review and click 'Approve'.
# 2. CONTENT WRITING AGENT: An AI generates an article. A breakpoint pauses execution, sending the draft
#    to a human editor. The editor updates the draft state and clicks 'Publish' to resume.

# ==========================================================
# MNC INTERVIEW QUESTIONS & ANSWERS
# ==========================================================
# Q1. How do you resume a paused graph run in LangGraph?
# A:  To resume a graph run from a checkpoint interrupt, call `.invoke(None, config)` on the compiled graph,
#     passing the same `thread_id` configuration. Passing `None` instructs LangGraph to load the last
#     active checkpoint state and continue execution from the current step.
#
# Q2. Can a human modify the state of a graph while it is paused?
# A:  Yes. Using `graph.update_state(config, values)`, you can modify any variable or overwrite message 
#     contents in the active thread checkpoint before resuming execution.
