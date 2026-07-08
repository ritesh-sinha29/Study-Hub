# ========================================================================================
# MCP TOOL INTEGRATION
# ========================================================================================
#
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# SECTION 1 — MODEL CONTEXT PROTOCOL (MCP)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#
# Model Context Protocol (MCP) is an open standard designed by Anthropic that enables AI 
# applications to safely connect with external data sources and API tools (like Slack, 
# Google Drive, Notion, Gmail, GitHub).
#
# Arcade / Composio provides standard wrapper servers for MCP tools.
# In LangGraph, we bind MCP tools to LLMs similarly to native tools:
#   1. Start or connect to the MCP Server.
#   2. Fetch the tools exposed by the MCP Server.
#   3. Bind those tools to the LangGraph ChatOpenAI / LLM node.
#
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# SECTION 2 — MCP ARCHITECTURE
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#
#   [ LangGraph Agent ] ──(Exposes query)──► [ MCP client ]
#                                                 │
#                                        (Standardized JSON-RPC)
#                                                 ▼
#                                          [ MCP Server ]
#                                           (Gmail, Slack)
#                                                 │
#                                          (Executes APIs)
#                                                 ▼
#                                        [ Target Services ]
#
# ========================================================================================

from typing import TypedDict, List
from langchain_core.tools import tool
from langgraph.graph import StateGraph, START, END

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# STATE SCHEMA
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

class MCPState(TypedDict):
    user_query: str
    mcp_tool_output: str
    final_response: str

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# MOCK MCP TOOL
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

@tool
def mcp_gmail_search(query: str) -> str:
    """
    Simulated MCP Tool: Search user inbox via Gmail MCP server connection.
    
    Args:
        query: The search term or subject keywords.
    """
    print(f"\n  [MCP SERVER CALL] mcp_gmail_search invoked with query: '{query}'")
    return "Email Subject: Q3 Financial Goals. Content: Please find the attached Q3 spreadsheet."

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# NODES
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def call_mcp_node(state: MCPState) -> dict:
    print("  [Node] call_mcp_node evaluating query...")
    query = state["user_query"]
    
    # Simulate LLM tool calling decision:
    # If the user asks about emails or inbox, we route to the Gmail MCP tool
    if "email" in query.lower() or "inbox" in query.lower():
        result = mcp_gmail_search.invoke({"query": query})
    else:
        result = "No MCP action triggered."
        
    return {"mcp_tool_output": result}

def generate_with_mcp_context(state: MCPState) -> dict:
    print("  [Node] generate_with_mcp_context synthesizing response...")
    context = state["mcp_tool_output"]
    response = f"Answer synthesized with MCP context: [{context}]"
    return {"final_response": response}

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# GRAPH CONSTRUCTION
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def build_mcp_graph():
    builder = StateGraph(MCPState)
    builder.add_node("call_mcp", call_mcp_node)
    builder.add_node("generator", generate_with_mcp_context)
    
    builder.add_edge(START, "call_mcp")
    builder.add_edge("call_mcp", "generator")
    builder.add_edge("generator", END)
    
    return builder.compile()

if __name__ == "__main__":
    print("\n" + "="*70)
    print("RUNNING MCP TOOL GRAPH")
    print("="*70)
    
    graph = build_mcp_graph()
    
    test_input = {"user_query": "Find the email containing Q3 spreadsheet."}
    result = graph.invoke(test_input)
    
    print("\n  Final State response:")
    print(" ", result["final_response"])

# ========================================================================================
# REAL-WORLD USE CASES
# ========================================================================================
#
# 1. ENTERPRISE EMAIL AUTOPILOT:
#    - **Step 1**: Connects Outlook MCP to read calendar slots.
#    - **Step 2**: Drafts replies to meeting requests.
#    - **Result**: Dispatches emails upon user approval.
#
# 2. FILE MANAGEMENT CO-PILOT:
#    - **Step 1**: Connects Notion/Drive MCP tools.
#    - **Result**: Searches pages, summarizes documents, and updates databases.
#
# ========================================================================================
# MNC INTERVIEW QUESTIONS & ANSWERS
# ========================================================================================
#
# Q1. What is the Model Context Protocol (MCP) and what problem does it solve?
# A:  MCP is an open standard that decouples LLMs from API integration. Instead of writing custom API wrappers 
#     for Gmail, Slack, and Notion for each agent, MCP servers expose tools in a uniform JSON schema, 
#     allowing any compliant agentic framework to bind them out-of-the-box.
#
# Q2. How does LangGraph handle OAuth authorization in MCP servers (like Google Calendar access)?
# A:  When a tool requires OAuth, the MCP execution throws a specific `AuthorizationRequired` interrupt. 
#     LangGraph halts execution (checkpointing the current state), displays the auth URL to the user, 
#     and resumes execution only after the user authenticates and supplies the authorization token.
