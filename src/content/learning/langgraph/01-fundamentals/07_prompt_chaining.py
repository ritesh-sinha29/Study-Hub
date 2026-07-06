# ========================================================================================
# LANGGRAPH CRASH COURSE — MODULE 07: PROMPT CHAINING
# ========================================================================================
#
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# SECTION 1 — WHAT IS PROMPT CHAINING?
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#
# Prompt Chaining is a sequential workflow pattern where:
#   - The OUTPUT of one LLM prompt becomes the INPUT of the next prompt.
#   - Each step is focused on a single, well-scoped task.
#   - State carries the intermediate results between steps.
#
# WHY NOT JUST ONE BIG PROMPT?
# A single large prompt asking for "Research + Draft + Edit + SEO-optimize + Translate"
# leads to: lower quality, context overflow, harder debugging, no granular control.
#
# Prompt Chaining solves this by decomposing complex tasks into focused steps:
#   Step 1: Research (gather facts)
#   Step 2: Draft   (write first version using the facts)
#   Step 3: Refine  (fix tone, grammar, style using the draft)
#   Step 4: Format  (apply final formatting/SEO using the refined draft)
#
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# SECTION 2 — PROMPT CHAINING vs PARALLEL (ORCHESTRATOR-WORKER)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#
#  PROMPT CHAINING:                    ORCHESTRATOR-WORKER (Parallel):
#  A → B → C → D (sequential)         A → [B, C, D] → E (fan-out/fan-in)
#  Each step DEPENDS on prior output   Steps are INDEPENDENT of each other
#  Good for: refinement pipelines      Good for: research from multiple sources
#
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# SECTION 3 — GRAPH ARCHITECTURE
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#
#  START → [generator] → [refiner] → [formatter] → END
#
#  Each node reads from the previous node's output (via shared state).
#  Fixed edges: every step always goes to the next (no branching needed).
#
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# SECTION 4 — GATING (CONDITIONAL EXIT IN CHAINED PIPELINES)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#
# You can add conditional exits ("gates") between chaining steps.
# A gate node runs a check (e.g. word count, safety check, topic relevance).
# If the check FAILS: route to a rejection/retry node.
# If the check PASSES: continue to the next chaining step.
#
# Example:
#   [generator] → [gate_check] → (pass) → [refiner] → END
#                              → (fail) → [regenerate_with_feedback]
#
# This is how Prompt Chaining and Generator-Evaluator patterns can be combined.
#
# ========================================================================================

from typing import TypedDict
from langgraph.graph import StateGraph, START, END


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# STATE
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

class ChainingState(TypedDict):
    topic:          str   # The user's topic request
    draft:          str   # Output of the generator node
    refined_output: str   # Output of the refiner node
    final_output:   str   # Output of the formatter node


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# NODES (each reads from the previous node's key in state)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def generate_draft_node(state: ChainingState) -> dict:
    """
    Step 1: Generator
    Receives the topic. Produces the initial rough draft.

    In production: call model.invoke(f"Write a first draft about {topic}")
    """
    print("  [Step 1/3] generate_draft_node executing...")
    topic = state.get("topic", "")
    draft = (
        f"Initial outline about '{topic}':\n"
        f"  1. Introduction to {topic}\n"
        f"  2. Core concepts and history\n"
        f"  3. Real-world applications today\n"
        f"  4. Future trends and challenges"
    )
    print(f"  Draft created: {len(draft.split())} words")
    return {"draft": draft}


def refine_draft_node(state: ChainingState) -> dict:
    """
    Step 2: Refiner
    Reads the DRAFT from state (written by Step 1).
    Enriches it with an executive summary and citations.

    In production: call model.invoke(f"Refine this draft:\n\n{draft}\n\nAdd executive summary and sources.")
    """
    print("  [Step 2/3] refine_draft_node executing...")
    draft = state.get("draft", "")
    refined = (
        f"EXECUTIVE SUMMARY: A comprehensive overview of the topic follows.\n\n"
        f"{draft}\n\n"
        f"SOURCES: [1] Academic Press 2024  [2] IEEE Research Vol. 12  [3] Nature Reviews"
    )
    print(f"  Refined draft: {len(refined.split())} words")
    return {"refined_output": refined}


def format_output_node(state: ChainingState) -> dict:
    """
    Step 3: Formatter
    Reads the REFINED output from state (written by Step 2).
    Applies publication-ready formatting: title, sections, word count metadata.

    In production: call model.invoke(f"Format this for our blog:\n\n{refined}")
    """
    print("  [Step 3/3] format_output_node executing...")
    refined = state.get("refined_output", "")
    topic   = state.get("topic", "")
    final   = (
        f"╔══════════════════════════════════════╗\n"
        f"║  PUBLISHED ARTICLE: {topic.upper()[:20]:<20} ║\n"
        f"╚══════════════════════════════════════╝\n\n"
        f"{refined}\n\n"
        f"[WORD COUNT: {len(refined.split())} | READING TIME: ~{len(refined.split()) // 200 + 1} min]"
    )
    print(f"  Final output ready.")
    return {"final_output": final}


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# GRAPH CONSTRUCTION
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def build_chaining_graph():
    print("\n" + "="*70)
    print("BUILDING PROMPT CHAINING GRAPH")
    print("="*70)

    builder = StateGraph(ChainingState)

    builder.add_node("generator", generate_draft_node)
    builder.add_node("refiner",   refine_draft_node)
    builder.add_node("formatter", format_output_node)

    # Fixed sequential edges — each step always leads to the next
    builder.add_edge(START,       "generator")
    builder.add_edge("generator", "refiner")
    builder.add_edge("refiner",   "formatter")
    builder.add_edge("formatter", END)

    return builder.compile()


if __name__ == "__main__":
    graph = build_chaining_graph()

    for topic in ["Quantum Computing", "CRISPR Gene Editing"]:
        print(f"\n{'='*70}")
        print(f"TOPIC: {topic}")
        print("="*70)
        result = graph.invoke({"topic": topic})
        print("\n" + result["final_output"])


# ========================================================================================
# REAL-WORLD USE CASES
# ========================================================================================
#
# 1. TECHNICAL DOCUMENTATION GENERATOR:
#    Step 1: Extract API method signatures from codebase
#    Step 2: Write plain-English descriptions for each method
#    Step 3: Add code examples (using the description as context)
#    Step 4: Format as MDX with proper markdown headings
#
# 2. MULTI-LANGUAGE REPORT PIPELINE:
#    Step 1: LLM summarizes quarterly data in English
#    Step 2: LLM translates to French, German, Spanish
#    Step 3: LLM adapts tone for each regional market
#    Step 4: PDF renderer exports each regional version
#
# ========================================================================================
# MNC INTERVIEW QUESTIONS & ANSWERS
# ========================================================================================
#
# Q1. What is Prompt Chaining and why is it preferred over a single large prompt?
# A:  Prompt Chaining decomposes a complex task into focused, sequential sub-tasks.
#     Each sub-task gets its own dedicated prompt with a single responsibility.
#     Benefits:
#     (a) LLMs perform better with focused, simple prompts than complex multi-task ones.
#     (b) Easier to debug — you can isolate which step produced the bad output.
#     (c) Each step can use a different model (cheap model for drafting, expensive for refining).
#     (d) You can insert gate checks between steps to ensure quality before proceeding.
#
# Q2. How is state passed between chaining steps in LangGraph?
# A:  The shared Graph State (TypedDict) acts as the communication bus. Step 1
#     writes to state["draft"]. Step 2 reads state["draft"] and writes to
#     state["refined_output"]. Step 3 reads state["refined_output"] and writes
#     to state["final_output"]. No direct function calls between nodes — all
#     communication happens through the centralized state object.
