# ========================================================================================
# LANGGRAPH CRASH COURSE — MODULE 05: HUMAN-IN-THE-LOOP (HITL) WITH BREAKPOINTS
# ========================================================================================
#
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# SECTION 1 — WHY HUMAN-IN-THE-LOOP (HITL)?
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#
# Fully autonomous AI agents are powerful but risky for IRREVERSIBLE ACTIONS:
#   - Transferring money (cannot be undone)
#   - Deleting database records (cannot be recovered)
#   - Sending emails to 10,000 customers (cannot be unsent)
#   - Executing production deployments (can cause outages)
#
# Human-in-the-Loop (HITL) is a safety pattern where execution PAUSES before
# a critical action so a human can review, approve, or reject it.
#
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# SECTION 2 — HOW BREAKPOINTS WORK IN LANGGRAPH
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#
# Breakpoints are set at compile time:
#   graph = builder.compile(
#       checkpointer=checkpointer,
#       interrupt_before=["action_node"]   # pauses BEFORE this node runs
#       # OR:
#       interrupt_after=["review_node"]    # pauses AFTER this node runs
#   )
#
# WHAT HAPPENS WHEN A BREAKPOINT IS HIT:
#   1. Graph executes all nodes up to the breakpoint.
#   2. State is saved to the checkpointer database.
#   3. graph.invoke() RETURNS (does not raise an error — returns the current state).
#   4. Your application shows the current state to the human (e.g. web UI, email).
#   5. Human makes a decision (approve / reject / edit).
#   6. If approved: call graph.invoke(None, config=thread_config) → resumes.
#   7. If rejected: call graph.invoke(None, config=thread_config) after updating state.
#
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# SECTION 3 — HITL LIFECYCLE DIAGRAM
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#
#  User: "Transfer $500 to John"
#       │
#       ▼
#  [agent node]  ← LLM decides to call execute_bank_transfer
#       │
#       ▼    (interrupt_before=["action"] fires here)
#  ════ BREAKPOINT ════════════════════════════════════════════════════════
#       │   State saved. graph.invoke() returns.
#       │   Your app: "AI wants to transfer $500 to John. Approve?"
#       │
#  Human: APPROVES
#       │
#       ▼
#  graph.invoke(None, config)   ← resume from saved checkpoint
#       │
#       ▼
#  [action node]  ← execute_bank_transfer runs
#       │
#       ▼
#  [agent node]   ← reads ToolMessage, generates final confirmation
#       │
#       ▼
#      END
#
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# SECTION 4 — MODIFYING STATE DURING A PAUSE (update_state)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#
# While the graph is paused, humans can also MODIFY the state before resuming:
#
#   graph.update_state(
#       config,
#       {"messages": [HumanMessage("Actually, send $300 instead")]},
#       as_node="agent"    # write the update as if the agent node did it
#   )
#   graph.invoke(None, config)   # resume with the modified state
#
# This enables a human to correct the AI's decision before it takes effect.
#
# ========================================================================================

from typing import Annotated
from typing_extensions import TypedDict
from langchain_core.tools import tool
from langchain_core.messages import BaseMessage, HumanMessage
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.checkpoint.memory import MemorySaver
from langgraph.prebuilt import ToolNode
from langchain.chat_models import init_chat_model


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# SENSITIVE TOOL (requires human approval before execution)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

@tool
def execute_bank_transfer(amount: int, recipient: str) -> str:
    """
    Execute a bank transfer to a recipient.
    CRITICAL: This action is IRREVERSIBLE. Always requires human approval before execution.

    Args:
        amount:    The dollar amount to transfer.
        recipient: The name of the transfer recipient.

    Returns:
        A confirmation string for the completed transfer.
    """
    print(f"  [TOOL] 💸 Executing transfer of ${amount} to {recipient}...")
    return f"✅ SUCCESS: Transferred ${amount} to {recipient}. Reference: TXN-{hash(recipient) % 99999:05d}"


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# STATE & NODES
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

class AgentState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]


def call_model(state: AgentState, model) -> dict:
    print("  [Node] call_model executing...")
    response = model.invoke(state["messages"])
    print(f"  [Node] AI returned: tool_calls={bool(response.tool_calls)}, content='{response.content[:60]}'")
    return {"messages": [response]}


def should_continue(state: AgentState) -> str:
    last_message = state["messages"][-1]
    if last_message.tool_calls:
        print("  [Router] Tool call requested → routing to 'action' node")
        return "action"
    print("  [Router] No tool call → routing to END")
    return END


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# GRAPH WITH HITL BREAKPOINT
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def build_hitl_agent(model, tools: list, checkpointer) -> object:
    print("\n" + "="*70)
    print("BUILDING HUMAN-IN-THE-LOOP AGENT")
    print("="*70)

    builder = StateGraph(AgentState)
    builder.add_node("agent",  lambda state: call_model(state, model))
    builder.add_node("action", ToolNode(tools))

    builder.add_edge(START, "agent")
    builder.add_conditional_edges("agent", should_continue, {"action": "action", END: END})
    builder.add_edge("action", "agent")

    # KEY: interrupt_before=["action"] means execution PAUSES before the tool runs
    # A checkpointer MUST be provided for interrupt_before to work
    return builder.compile(
        checkpointer=checkpointer,
        interrupt_before=["action"]
    )


if __name__ == "__main__":
    checkpointer  = MemorySaver()
    tools_list    = [execute_bank_transfer]
    thread_config = {"configurable": {"thread_id": "transfer-thread-001"}}

    try:
        model            = init_chat_model("gpt-4o-mini", model_provider="openai")
        model_with_tools = model.bind_tools(tools_list)
        agent            = build_hitl_agent(model_with_tools, tools_list, checkpointer)

        # PHASE 1: Run the graph — it will pause at the breakpoint
        print("\n--- PHASE 1: INITIAL RUN (will pause at breakpoint) ---")
        agent.invoke(
            {"messages": [("user", "Transfer $500 to John Doe please.")]},
            config=thread_config
        )

        # Inspect the current state at the breakpoint
        current_state = agent.get_state(thread_config)
        print(f"\n  Graph paused. Next node to run: {current_state.next}")
        print(f"  Last message: {current_state.values['messages'][-1]}")

        # PHASE 2: Human reviews and decides
        print("\n--- PHASE 2: HUMAN REVIEW & DECISION ---")
        print("  [UI] Agent wants to: execute_bank_transfer(amount=500, recipient='John Doe')")
        print("  [UI] Do you approve? [yes/no]: ", end="")

        user_decision = "yes"   # Simulated approval (in real app: button click / form submit)
        print(user_decision)

        if user_decision.lower() == "yes":
            print("\n  Human APPROVED. Resuming graph...")
            # Pass None as input — LangGraph loads the checkpoint and continues
            result = agent.invoke(None, config=thread_config)
            print("\n--- FINAL MESSAGE THREAD ---")
            for msg in result["messages"]:
                print(f"  [{msg.type.upper()}]: {msg.content}")
        else:
            print("\n  Human REJECTED. Execution terminated.")
            # Optional: update state with rejection message before abandoning
            agent.update_state(
                thread_config,
                {"messages": [HumanMessage("Action rejected by human reviewer.")]},
                as_node="agent"
            )

    except Exception as e:
        print("\nHITL agent failed (check API keys):", e)


# ========================================================================================
# REAL-WORLD USE CASES
# ========================================================================================
#
# 1. FINANCIAL TRANSACTION AGENT:
#    - **Step 1**: Agent plans a wire transfer and hits interrupt_before execute_transfer.
#    - **Step 2**: Compliance officer reviews transfer details.
#    - **Result**: Resume trigger graph.invoke(None) finalizes execution on approval.
#
# 2. CONTENT MODERATION:
#    - **Step 1**: AI drafts article and hits interrupt_before publish_node.
#    - **Step 2**: Editor updates wording via graph.update_state().
#    - **Result**: Resumes execution to publish approved content.
#
# 3. CLOUD INFRASTRUCTURE CHANGES:
#    - **Step 1**: AI plans Terraform changes and hits interrupt_before apply_terraform.
#    - **Step 2**: DevOps reviews and approves changes.
#    - **Result**: Resumes to run terraform apply.
#
# ========================================================================================
# MNC INTERVIEW QUESTIONS & ANSWERS
# ========================================================================================
#
# Q1. How do you resume a paused graph run after human approval?
# A:  Call `graph.invoke(None, config=thread_config)` with the same `thread_id`.
#     Passing `None` as the input tells LangGraph: "Don't add new user input, just
#     load the last checkpoint and continue from the next node in the queue."
#     The graph picks up exactly where the breakpoint interrupted it.
#
# Q2. Can a human MODIFY the agent's planned action during a HITL pause?
# A:  Yes. Use `graph.update_state(config, updates, as_node="node_name")`.
#     For example, if the agent planned to transfer $500 but the human wants $300:
#       graph.update_state(config, {"messages": [HumanMessage("Transfer $300 instead")]})
#     Then call graph.invoke(None, config) to resume with the corrected state.
#
# Q3. What is the difference between `interrupt_before` and `interrupt_after`?
# A:  - interrupt_before=["node_name"]: Graph pauses BEFORE the node runs.
#       The node has NOT executed yet. Use to PREVENT an action until approved.
#     - interrupt_after=["node_name"]: Graph pauses AFTER the node has run.
#       The node output is in the state. Use to REVIEW results before continuing.
#     For sensitive tool calls (money transfers, deletions), always use interrupt_before.
