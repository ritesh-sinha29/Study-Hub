# ========================================================================================
# LANGGRAPH CRASH COURSE — MODULE 08: GENERATOR-EVALUATOR LOOP
# ========================================================================================
#
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# SECTION 1 — WHAT IS THE GENERATOR-EVALUATOR PATTERN?
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#
# The Generator-Evaluator pattern creates a FEEDBACK LOOP to self-improve output:
#
#  ┌──────────────────────────────────────────────────────────────────────┐
#  │                    GENERATOR-EVALUATOR LOOP                          │
#  │                                                                      │
#  │   User Prompt                                                        │
#  │       │                                                              │
#  │       ▼                                                              │
#  │  ┌──────────┐    generate output based on prompt + any prior feedback│
#  │  │Generator │ ──────────────────────────────────────────────────►    │
#  │  └──────────┘                                                        │
#  │       │                                                              │
#  │       ▼                                                              │
#  │  ┌──────────┐    check against quality criteria (word count, safety, │
#  │  │Evaluator │    code syntax, character limit, format rules...)      │
#  │  └──────────┘                                                        │
#  │       │                                                              │
#  │       ├── PASS (criteria met) ──────────────────────────────► END    │
#  │       │                                                              │
#  │       └── FAIL (feedback written to state) ──► back to Generator     │
#  └──────────────────────────────────────────────────────────────────────┘
#
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# SECTION 2 — PREVENTING INFINITE LOOPS (ATTEMPT COUNTER)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#
# WITHOUT a guard, a buggy generator could loop forever, burning API credits.
#
# SOLUTION: Store an `attempts` counter in state. The evaluator router:
#   - If attempts < MAX_ATTEMPTS AND feedback: → return "retry" (loop back)
#   - If attempts >= MAX_ATTEMPTS: → return "accept" (force exit, return best effort)
#   - If no feedback (criteria met): → return "accept" (clean exit)
#
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# SECTION 3 — EVALUATOR TYPES (DETERMINISTIC VS LLM-BASED)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#
#  TYPE                  │ EXAMPLE CRITERIA                   │ SPEED
#  ──────────────────────┼────────────────────────────────────┼─────────────────
#  Deterministic Check   │ word count, char limit, JSON valid,│ ⚡ Near-instant
#  (Python code)         │ code compiles, URL format valid    │ (no API call)
#  ──────────────────────┼────────────────────────────────────┼─────────────────
#  LLM-as-Judge          │ factual accuracy, tone, safety,    │ ⏱ ~1-2 seconds
#  (model.invoke)        │ coherence, relevance               │ (API call cost)
#
# For cost efficiency: use deterministic checks first, LLM-as-Judge only for
# subjective quality assessments.
#
# ========================================================================================

from typing import TypedDict
from langgraph.graph import StateGraph, START, END

MAX_ATTEMPTS = 3   # Safety guard to prevent infinite loops


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# STATE
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

class LoopState(TypedDict):
    prompt:   str   # The original generation prompt
    output:   str   # The current generated output
    feedback: str   # Evaluator's failure reason (empty string = PASS)
    attempts: int   # How many generator attempts have run


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# GENERATOR NODE
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def generator_node(state: LoopState) -> dict:
    """
    Generator: Produces content. Uses any feedback from the evaluator
    to correct or improve the output on subsequent iterations.

    In production: call model.invoke(
        f"Task: {prompt}\n\nPrevious feedback: {feedback}\n\nGenerate improved output:"
    )
    """
    attempts = state.get("attempts", 0) + 1
    feedback = state.get("feedback", "")
    prompt   = state.get("prompt", "")

    print(f"  [Generator] Attempt #{attempts} (feedback='{feedback[:40]}...' if feedback else 'None')")

    # Simulation: First attempt generates a long output (fails evaluator).
    # Second attempt (with feedback) generates a short output (passes evaluator).
    if feedback:
        output = "AI: Intelligent machines that learn from data."   # Compliant (under 10 words)
    else:
        output = (
            "Artificial Intelligence (AI) is a transformative branch of computer science "
            "focused on building systems capable of performing tasks that normally require "
            "human intelligence, such as reasoning, learning, and problem-solving."
        )

    print(f"  [Generator] Output ({len(output.split())} words): '{output[:60]}...'")
    return {"output": output, "attempts": attempts}


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# EVALUATOR NODE
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def evaluator_node(state: LoopState) -> dict:
    """
    Evaluator: Checks the generated output against quality criteria.
    Sets `feedback` to the failure reason (non-empty = FAIL, empty = PASS).

    This is a deterministic word-count checker. In production, replace with:
      - LLM-as-Judge for subjective quality
      - Code compiler for code generation tasks
      - Regex/schema validators for structured output tasks
    """
    output     = state.get("output", "")
    word_count = len(output.split())
    attempts   = state.get("attempts", 0)

    print(f"  [Evaluator] Checking output ({word_count} words)...")

    # Criterion: output must be under 10 words (brief summary requirement)
    if word_count > 10:
        feedback = (
            f"Output is {word_count} words. Requirement: under 10 words. "
            "Please rewrite as a very brief one-line summary."
        )
        print(f"  [Evaluator] FAIL — {feedback[:60]}")
    else:
        feedback = ""   # Empty = PASS
        print(f"  [Evaluator] PASS ✓ ({word_count} words, attempt #{attempts})")

    return {"feedback": feedback}


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# EVALUATION ROUTER
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def check_evaluation(state: LoopState) -> str:
    """
    Router: Decides whether to retry generation or accept the output.
    Includes a MAX_ATTEMPTS guard to prevent infinite loops.
    """
    has_feedback = bool(state.get("feedback"))
    over_limit   = state.get("attempts", 0) >= MAX_ATTEMPTS

    if over_limit:
        print(f"  [Router] Max attempts ({MAX_ATTEMPTS}) reached → FORCE ACCEPT")
        return "accept"
    if has_feedback:
        print(f"  [Router] Evaluation failed → RETRY")
        return "retry"
    print(f"  [Router] Evaluation passed → ACCEPT")
    return "accept"


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# GRAPH CONSTRUCTION
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def build_loop_graph():
    print("\n" + "="*70)
    print("BUILDING GENERATOR-EVALUATOR LOOP GRAPH")
    print("="*70)

    builder = StateGraph(LoopState)

    builder.add_node("generator", generator_node)
    builder.add_node("evaluator", evaluator_node)

    builder.add_edge(START,       "generator")
    builder.add_edge("generator", "evaluator")

    # Conditional edge from evaluator: retry loops back to generator, accept exits
    builder.add_conditional_edges(
        "evaluator",
        check_evaluation,
        {
            "retry":  "generator",   # ← LOOP: go back to fix the output
            "accept": END            # ← EXIT: output meets the criteria
        }
    )

    return builder.compile()


if __name__ == "__main__":
    graph = build_loop_graph()

    print("\n  Running: Summarize AI in under 10 words")
    result = graph.invoke({
        "prompt":   "Summarize Artificial Intelligence in under 10 words.",
        "feedback": "",
        "attempts": 0,
        "output":   ""
    })

    print(f"\n  Final Output  : '{result['output']}'")
    print(f"  Total Attempts: {result['attempts']}")
    print(f"  Final Feedback: '{result['feedback'] or 'NONE (passed)'}'")


# ========================================================================================
# REAL-WORLD USE CASES
# ========================================================================================
#
# 1. AI CODE GENERATOR:
#    - **Step 1**: Generator node writes Python function code.
#    - **Step 2**: Evaluator runs code in sandboxed exec environment.
#    - **Result**: Loops back with traceback feedback on errors until execution succeeds.
#
# 2. SEO META DESCRIPTION GENERATOR:
#    - **Step 1**: Generator creates page meta description.
#    - **Step 2**: Evaluator validates description length is between 150-160 characters.
#    - **Result**: Triggers rewrite feedback if invalid, else publishes output.
#
# ========================================================================================
# MNC INTERVIEW QUESTIONS & ANSWERS
# ========================================================================================
#
# Q1. What problem does the Generator-Evaluator pattern solve?
# A:  LLMs often fail to satisfy strict programmatic constraints on the first attempt —
#     precise character limits, valid JSON schema, compilable code, specific word counts.
#     The Generator-Evaluator pattern automates a correction cycle: generate → verify →
#     feed error back → regenerate. This eliminates brittle prompt engineering tricks
#     and handles constraint satisfaction reliably through programmatic verification.
#
# Q2. How do you prevent infinite loops in a Generator-Evaluator graph?
# A:  Add an `attempts` integer counter to the Graph State. Increment it in the
#     generator node. In the conditional router:
#       if state["attempts"] >= MAX_ATTEMPTS: return "accept"   # force exit
#     This caps the loop at a configurable limit, ensuring the agent always terminates.
#     In production, also log a warning so engineers can review cases where the
#     max limit was hit (it usually indicates a systematic prompt failure).
#
# Q3. When should you use an LLM-as-Judge evaluator vs a deterministic evaluator?
# A:  Use DETERMINISTIC evaluators (Python code checks) for objective constraints:
#     JSON schema validation, character count limits, code compilation, regex matching.
#     They're instant, free (no API cost), and 100% reliable.
#     Use LLM-as-JUDGE evaluators for subjective quality: factual accuracy, tone
#     appropriateness, content safety, coherence, and relevance. They're slower and
#     add cost per loop iteration, so minimize their use by filtering with deterministic
#     checks first — only escalate to LLM evaluation when truly necessary.
