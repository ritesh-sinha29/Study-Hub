# ==========================================================
# LANGGRAPH STUDY GUIDE: 01. MCP TOOL INTEGRATION (ARCADE)
# ==========================================================

# --- MODEL CONTEXT PROTOCOL (MCP) ---
# Model Context Protocol (MCP) is an open standard that enables AI applications to safely
# connect with external data sources and API tools (like Slack, Google Drive, Notion, Gmail).
#
# Arcade / Composio provides standard wrapper servers for MCP tools.
# In LangGraph, we bind MCP tools to LLMs similarly to native tools:
# 1. Start or connect to the MCP Server.
# 2. Fetch the tools exposed by the MCP Server.
# 3. Bind those tools to the LangGraph ChatOpenAI / LLM node.

from typing import TypedDict, List
from langchain_core.tools import tool
from langgraph.graph import StateGraph, START, END

# 1. Define the State
class MCPState(TypedDict):
    user_query: str
    mcp_tool_output: str
    final_response: str

# 2. Define a Mock MCP Tool (Gmail lookup simulation)
@tool
def mcp_gmail_search(query: str) -> str:
    """
    Simulated MCP Tool: Search user inbox via Gmail MCP server connection.
    """
    print(f"\n[MCP SERVER CALL] mcp_gmail_search invoked with query: '{query}'")
    # Simulation: Returning search matches
    return "Email Subject: Q3 Financial Goals. Content: Please find the attached Q3 spreadsheet."

# 3. Define Graph Nodes
def call_mcp_node(state: MCPState) -> dict:
    print("Executing: call_mcp_node")
    query = state["user_query"]
    
    # Simulate LLM tool calling decision
    # If the user asks about emails, we run the MCP tool
    if "email" in query.lower() or "inbox" in query.lower():
        result = mcp_gmail_search.invoke({"query": query})
    else:
        result = "No MCP action triggered."
        
    return {"mcp_tool_output": result}

def generate_with_mcp_context(state: MCPState) -> dict:
    print("Executing: generate_with_mcp_context")
    context = state["mcp_tool_output"]
    response = f"Answer synthesized with MCP context: [{context}]"
    return {"final_response": response}

# 4. Build MCP Graph
def build_mcp_graph():
    builder = StateGraph(MCPState)
    builder.add_node("call_mcp", call_mcp_node)
    builder.add_node("generator", generate_with_mcp_context)
    
    builder.add_edge(START, "call_mcp")
    builder.add_edge("call_mcp", "generator")
    builder.add_edge("generator", END)
    
    return builder.compile()

if __name__ == "__main__":
    print("--- RUNNING MCP TOOL GRAPH ---")
    graph = build_mcp_graph()
    
    test_input = {"user_query": "Find the email containing Q3 spreadsheet."}
    result = graph.invoke(test_input)
    
    print("\nFinal State response:")
    print(result["final_response"])

# ==========================================================
# REAL-LIFE USE CASES
# ==========================================================
# 1. ENTERPRISE EMAIL AUTOPILOT: Connecting Gmail/Outlook MCP. The agent reads calendar slots, drafts email
#    replies to meeting requests, and sends them out upon user approval.
# 2. FILE MANAGEMENT CO-PILOT: Bound to Google Drive/Notion MCP. The agent searches pages, summarizes documents,
#    and updates spreadsheets directly.

# ==========================================================
# MNC INTERVIEW QUESTIONS & ANSWERS
# ==========================================================
# Q1. What is the Model Context Protocol (MCP) and what problem does it solve?
# A:  MCP is an open standard that decouples LLMs from API integration. Instead of writing custom API wrappers 
#     for Gmail, Slack, and Notion for each agent, MCP servers expose tools in a uniform JSON schema, 
#     allowing any compliant agentic framework to bind them out-of-the-box.
#
# Q2. How does LangGraph handle OAuth authorization in MCP servers (like Google Calendar access)?
# A:  When a tool requires OAuth, the MCP execution throws a specific `AuthorizationRequired` interrupt. 
#     LangGraph halts execution (checkpointing the current state), displays the auth URL to the user, 
#     and resumes execution only after the user authenticates and supplies the authorization token.
