# ==========================================================
# LANGGRAPH STUDY GUIDE: 02. REACT AGENT WITH TOOLS
# ==========================================================

# --- THE REACT PATTERN ---
# ReAct (Reasoning + Acting) is an agent pattern where the model decides:
# 1. Which tool to call and with what parameters (Reasoning).
# 2. Runs the tool and returns the response to the LLM (Acting).
# 3. Repeat until the LLM decides it has enough information to formulate the final answer.
#
# In LangGraph, we implement this as a stateful graph where:
# - State: Accumulates list of messages (`add_messages` reducer).
# - Nodes: Model node (runs the LLM) and Tool node (executes the requested tool).

from typing import Annotated
from typing_extensions import TypedDict
from langchain_core.tools import tool
from langchain_core.messages import BaseMessage
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode
from langchain.chat_models import init_chat_model

# 1. Define the Custom Tool
@tool
def calculate_square(number: int) -> str:
    """Calculate the square of a number."""
    return f"The square of {number} is {number * number}."

# 2. Define the State Schema
# Using `add_messages` tells LangGraph to APPEND new messages to the existing list, 
# rather than overwriting the entire key.
class AgentState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]

# 3. Define the Nodes
def call_model(state: AgentState, model):
    print("Executing: call_model")
    messages = state["messages"]
    response = model.invoke(messages)
    # Return the AI message to be appended to the state
    return {"messages": [response]}

def build_react_agent(model, tools):
    print("--- 2. BUILDING REACT AGENT ---")
    
    builder = StateGraph(AgentState)
    
    # Define tool executor node using LangGraph's prebuilt ToolNode
    tool_node = ToolNode(tools)
    
    # Add nodes to graph
    builder.add_node("agent", lambda state: call_model(state, model))
    builder.add_node("tools", tool_node)
    
    # Set entry point
    builder.add_edge(START, "agent")
    
    # Define conditional edge (routing logic)
    # The agent node decides whether to call tools or end
    def should_continue(state: AgentState) -> str:
        last_message = state["messages"][-1]
        # If the model requested tool calls, route to the "tools" node
        if last_message.tool_calls:
            print("Routing: Go to Tools")
            return "tools"
        # Otherwise, stop
        print("Routing: End Conversation")
        return END
        
    builder.add_conditional_edges(
        "agent",
        should_continue,
        {
            "tools": "tools",
            END: END
        }
    )
    
    # After executing tools, return to the agent to let the LLM analyze the tool results
    builder.add_edge("tools", "agent")
    
    return builder.compile()

if __name__ == "__main__":
    # Custom tools list
    tools_list = [calculate_square]
    
    try:
        # Bind the tools to the model
        model = init_chat_model("gpt-4o-mini", model_provider="openai")
        model_with_tools = model.bind_tools(tools_list)
        
        # Compile agent
        agent = build_react_agent(model_with_tools, tools_list)
        
        # Run agent
        query = {"messages": [("user", "What is the square of 9?")]}
        print("User Query: What is the square of 9?")
        
        result = agent.invoke(query)
        print("Final Output Messages:")
        for msg in result["messages"]:
            print(f"[{msg.type.upper()}]: {msg.content}")
            
    except Exception as e:
        print("ReAct agent execution failed (check API keys):", e)

# ==========================================================
# REAL-LIFE USE CASES
# ==========================================================
# 1. DATABASE COPILOT: Model translates natural language into SQL queries, executes the query tool,
#    reads the returned database context, and explains the results to the user.
# 2. FILE PROCESSING PIPELINE: Model runs a file-check tool, if errors are found, runs a file-fix tool,
#    and repeats the loop until the checks pass.

# ==========================================================
# MNC INTERVIEW QUESTIONS & ANSWERS
# ==========================================================
# Q1. What is the role of the `add_messages` reducer in LangGraph?
# A:  By default, when a node returns a dictionary, LangGraph replaces the value of that key.
#     Using `Annotated[list, add_messages]` configures a "reducer" function that appends new messages 
#     to the list instead of replacing it, preserving the conversational thread history automatically.
#
# Q2. Why is the edge from "tools" back to "agent" necessary in ReAct?
# A:  Tools only return raw results (e.g. database output, calculation answers). They do not generate
#     human-friendly explanations. Returning flow to the model allows it to read the tool output 
#     (contained in a `ToolMessage`) and synthesize the final answer for the user.
