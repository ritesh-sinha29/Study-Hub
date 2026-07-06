# ========================================================================================
# LANGGRAPH CRASH COURSE — MODULE 06: ADVANCED ARCHITECTURES (ORCHESTRATOR-WORKER)
# ========================================================================================
#
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# SECTION 1 — THE THREE CORE AGENTIC ARCHITECTURE PATTERNS
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#
#  PATTERN              │ STRUCTURE                    │ BEST FOR
#  ─────────────────────┼──────────────────────────────┼────────────────────────────────
#  Prompt Chaining      │ A → B → C → D (linear)       │ Report generation, SQL → NL
#  Generator-Evaluator  │ Generator ⇄ Evaluator (loop) │ Code gen, constrained output
#  Orchestrator-Worker  │ Orchestrator → Workers (fan-  │ Complex tasks with subtasks,
#                       │ out) → Synthesizer (fan-in)   │ research, multi-domain queries
#
# This module covers the ORCHESTRATOR-WORKER pattern — the most powerful for
# enterprise-grade multi-agent applications.
#
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# SECTION 2 — ORCHESTRATOR-WORKER PATTERN EXPLAINED
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#
# The Orchestrator is an LLM (or logic node) that:
#   1. Receives a complex user request
#   2. Breaks it into independent sub-tasks
#   3. Assigns each sub-task to a specialized Worker agent/node
#
# Workers are specialized nodes that:
#   1. Receive ONE focused sub-task from the Orchestrator
#   2. Execute it with domain-specific tools (search, API, code execution)
#   3. Write their results to the shared state
#
# The Synthesizer is a node that:
#   1. Reads ALL workers' results from state
#   2. Merges, de-duplicates, and formats them into a final response
#
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# SECTION 3 — FAN-OUT & FAN-IN (PARALLEL EXECUTION PATTERN)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#
# FAN-OUT: One source node routes to MULTIPLE target nodes simultaneously.
#   builder.add_edge("orchestrator", "worker_a")
#   builder.add_edge("orchestrator", "worker_b")
#   builder.add_edge("orchestrator", "worker_c")
#   → All 3 workers execute (in parallel where possible)
#
# FAN-IN: Multiple source nodes all route to ONE target node.
#   builder.add_edge("worker_a", "synthesizer")
#   builder.add_edge("worker_b", "synthesizer")
#   builder.add_edge("worker_c", "synthesizer")
#   → LangGraph waits for ALL workers to finish before running synthesizer
#      (this is the automatic fan-in / join behavior)
#
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# SECTION 4 — GRAPH ARCHITECTURE DIAGRAM
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#
#                         START
#                           │
#                           ▼
#                   ┌─────────────┐
#                   │ Orchestrator │  (breaks task into subtasks)
#                   └─────────────┘
#                     ╱    │    ╲
#            ┌────────┘    │    └────────┐
#            ▼             ▼             ▼
#    ┌──────────────┐ ┌────────────┐ ┌──────────┐
#    │  Translator  │ │  Capitalizer│ │ Summarizer│
#    │   Worker     │ │   Worker   │ │  Worker  │
#    └──────────────┘ └────────────┘ └──────────┘
#            │             │             │
#            └─────────────┼─────────────┘
#                          ▼  (fan-in: waits for all workers)
#                  ┌───────────────┐
#                  │  Synthesizer  │  (merges all results)
#                  └───────────────┘
#                          │
#                         END
#
# ========================================================================================

from typing import TypedDict
from langgraph.graph import StateGraph, START, END


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# STATE
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

class OrchestratorState(TypedDict):
    original_request:     str
    subtasks:             list[str]
    worker_results:       dict[str, str]
    consolidated_response: str


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# NODES
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def orchestrator_node(state: OrchestratorState) -> dict:
    """
    Orchestrator Node: Analyzes the request and breaks it into sub-tasks.

    In production: Replace simulation with:
      model.with_structured_output(SubtaskList).invoke(
          f"Break this task into independent subtasks: {request}"
      )
    """
    print("  [Orchestrator] Analyzing request and assigning subtasks...")
    request  = state.get("original_request", "")
    subtasks = ["Translate to French", "Capitalize", "Summarize in 5 words"]
    print(f"  [Orchestrator] Subtasks assigned: {subtasks}")
    return {"subtasks": subtasks, "worker_results": {}}


def translator_worker(state: OrchestratorState) -> dict:
    """Worker A: Translates the original request to French (simulated)."""
    print("  [Worker: Translator] Executing translation task...")
    req         = state.get("original_request", "")
    translated  = f"[FRENCH]: Bonjour tout le monde — traduction de: '{req}'"
    results     = dict(state.get("worker_results", {}))
    results["translation"] = translated
    print(f"  [Worker: Translator] Result: {translated[:60]}")
    return {"worker_results": results}


def capitalizer_worker(state: OrchestratorState) -> dict:
    """Worker B: Returns the original request in ALL CAPS."""
    print("  [Worker: Capitalizer] Executing capitalization task...")
    req        = state.get("original_request", "")
    capitalized = f"[CAPITALS]: {req.upper()}"
    results    = dict(state.get("worker_results", {}))
    results["capitalized"] = capitalized
    print(f"  [Worker: Capitalizer] Result: {capitalized[:60]}")
    return {"worker_results": results}


def summarizer_worker(state: OrchestratorState) -> dict:
    """Worker C: Produces a 5-word summary of the original request (simulated)."""
    print("  [Worker: Summarizer] Executing summarization task...")
    req     = state.get("original_request", "")
    words   = req.split()[:5]
    summary = f"[5-WORD SUMMARY]: {' '.join(words)}..."
    results = dict(state.get("worker_results", {}))
    results["summary"] = summary
    print(f"  [Worker: Summarizer] Result: {summary}")
    return {"worker_results": results}


def synthesizer_node(state: OrchestratorState) -> dict:
    """
    Synthesizer Node: Runs AFTER all workers finish (fan-in).
    Merges all worker outputs into a single consolidated report.
    """
    print("  [Synthesizer] All workers complete. Consolidating results...")
    results = state.get("worker_results", {})

    report_lines = ["=" * 50, "CONSOLIDATED ORCHESTRATOR REPORT", "=" * 50]
    for key, value in results.items():
        report_lines.append(f"• [{key.upper()}] {value}")
    report_lines.append("=" * 50)

    report = "\n".join(report_lines)
    return {"consolidated_response": report}


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# GRAPH CONSTRUCTION
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def build_orchestration_graph():
    print("\n" + "="*70)
    print("BUILDING ORCHESTRATOR-WORKER GRAPH")
    print("="*70)

    builder = StateGraph(OrchestratorState)

    # Register all nodes
    builder.add_node("orchestrator", orchestrator_node)
    builder.add_node("translator",   translator_worker)
    builder.add_node("capitalizer",  capitalizer_worker)
    builder.add_node("summarizer",   summarizer_worker)
    builder.add_node("synthesizer",  synthesizer_node)

    # Entry point
    builder.add_edge(START, "orchestrator")

    # FAN-OUT: Orchestrator dispatches to all three workers simultaneously
    builder.add_edge("orchestrator", "translator")
    builder.add_edge("orchestrator", "capitalizer")
    builder.add_edge("orchestrator", "summarizer")

    # FAN-IN: All workers converge at synthesizer
    # LangGraph automatically waits for ALL three workers before running synthesizer
    builder.add_edge("translator",  "synthesizer")
    builder.add_edge("capitalizer", "synthesizer")
    builder.add_edge("summarizer",  "synthesizer")

    builder.add_edge("synthesizer", END)

    return builder.compile()


if __name__ == "__main__":
    graph = build_orchestration_graph()

    user_request = "hello world, I am learning LangGraph"
    print(f"\n  User Request: '{user_request}'")
    print("  Executing Orchestrator-Worker pipeline...\n")

    result = graph.invoke({"original_request": user_request})
    print("\n" + result["consolidated_response"])


# ========================================================================================
# REAL-WORLD USE CASES
# ========================================================================================
#
# 1. AI PULL REQUEST REVIEWER:
#    Orchestrator: Breaks the PR into: code_quality, test_coverage, security, documentation.
#    Worker A: Code quality agent (uses pylint/flake8 tool)
#    Worker B: Test coverage agent (runs pytest --cov)
#    Worker C: Security scanner (SAST tool)
#    Worker D: Docs checker (checks for missing docstrings)
#    Synthesizer: Merges all reports into a GitHub PR comment.
#
# 2. TRAVEL ITINERARY BUILDER:
#    User: "Plan a 5-day trip to Japan."
#    Orchestrator subtasks: flights, hotels, tourist spots, local food, transportation
#    Each worker calls a different API. Synthesizer builds the final travel plan PDF.
#
# 3. DAILY MARKET INTELLIGENCE REPORT:
#    Orchestrator assigns: news_scraper, stock_analyzer, competitor_tracker
#    Workers run in parallel. Synthesizer compiles an executive summary email sent at 8am.
#
# ========================================================================================
# MNC INTERVIEW QUESTIONS & ANSWERS
# ========================================================================================
#
# Q1. What is the Orchestrator-Worker pattern and when is it preferred?
# A:  It's a multi-agent pattern where one Orchestrator agent decomposes a complex
#     task into independent sub-tasks and delegates them to specialized Worker agents.
#     Preferred over single-agent systems when:
#     (a) Sub-tasks are independent (can run in parallel)
#     (b) Each sub-task requires domain expertise or unique tools
#     (c) The task is too complex for one LLM context window
#     Example: Research Report = [web_search_agent + academic_search_agent + citation_agent]
#
# Q2. How does LangGraph handle fan-out and fan-in (parallel + synchronization)?
# A:  FAN-OUT: Linking one source node to multiple target nodes with separate
#     add_edge() calls causes them to execute in parallel (via thread pool for sync).
#     FAN-IN: When multiple edges converge on a single node, LangGraph uses an internal
#     "join" mechanism — it waits for ALL incoming predecessor nodes to complete before
#     running the fan-in node. This is automatic; no explicit synchronization code needed.
#
# Q3. How do worker results accumulate without overwriting each other in shared state?
# A:  Workers write into a dict field in state (e.g. worker_results["translation"]).
#     Since each worker writes to a DIFFERENT KEY in the dict, they don't conflict.
#     A common pattern is to use `Annotated[dict, merge_dicts]` with a custom reducer
#     that merges returned dicts instead of overwriting them, making the fan-in safe.
