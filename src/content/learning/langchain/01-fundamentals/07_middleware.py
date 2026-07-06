# ========================================================================================
# LANGCHAIN CRASH COURSE — MODULE 07: CALLBACKS, MIDDLEWARE & OBSERVABILITY
# ========================================================================================
#
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# SECTION 1 — WHAT IS THE CALLBACK SYSTEM?
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#
# LangChain runs pipelines that call LLMs, invoke tools, run agents, and execute
# retrieval steps. In production, you need to observe ALL of these without
# modifying business logic.
#
# The Callback System is LangChain's built-in middleware framework. It works like
# event hooks: every component fires lifecycle events, and your custom handler
# "listens" to those events to log, measure, or alert.
#
# Think of it like browser event listeners but for AI pipeline components.
#
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# SECTION 2 — ALL AVAILABLE CALLBACK HOOKS
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#
#  HOOK                  │ WHEN IT FIRES                   │ TYPICAL USE
#  ──────────────────────┼─────────────────────────────────┼──────────────────────────
#  on_llm_start          │ Just before prompt sent to API  │ Log input, start timer
#  on_llm_end            │ After API response received     │ Log output, calc latency
#  on_llm_error          │ If the API call throws          │ Alert on-call, retry logic
#  on_chain_start        │ When a chain begins             │ Trace chain entry
#  on_chain_end          │ When a chain completes          │ Trace chain exit
#  on_chain_error        │ If a chain throws               │ Log + alert
#  on_tool_start         │ Before tool function runs       │ Log tool name + args
#  on_tool_end           │ After tool function returns     │ Log tool result
#  on_agent_action       │ Agent decides to call a tool    │ Trace reasoning
#  on_agent_finish       │ Agent produces final answer     │ Record final output
#  on_retriever_start    │ Before vector store query       │ Log search query
#  on_retriever_end      │ After docs returned             │ Log retrieved chunks
#
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# SECTION 3 — SEPARATION OF CONCERNS (WHY CALLBACKS MATTER)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#
# WITHOUT callbacks — business logic polluted with logging:
#
#   start = time.time()
#   print(f"Sending prompt: {prompt}")         ← logging mixed into business code
#   response = model.invoke(prompt)
#   latency = time.time() - start
#   print(f"Latency: {latency}s, Tokens: ...")  ← tracking mixed in
#   db.insert(prompt, response, latency)         ← DB calls mixed in
#   return response
#
# WITH callbacks — clean separation:
#
#   response = model.invoke(prompt, config={"callbacks": [AuditMiddleware()]})
#   return response
#   # All logging/tracking/cost calculation happens inside the callback handler
#
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# SECTION 4 — CONSTRUCTOR VS INVOCATION CALLBACKS
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#
#  FEATURE          │ CONSTRUCTOR CALLBACKS           │ INVOCATION CALLBACKS
#  ─────────────────┼─────────────────────────────────┼────────────────────────────────
#  Scope            │ Global (all requests on object) │ Local (single request execution)
#  Definition       │ Pass in init_chat_model(...)    │ Pass in config dict on invoke()
#  Primary Use Case │ Global telemetry / monitoring   │ Per-user session tracking
#  Best For         │ Sentry APM, global cost meters  │ Per-request trace logging
#
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# SECTION 5 — GPT-4o-mini TOKEN COST REFERENCE (for cost estimation)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#
#   Input tokens  : $0.150 per 1,000,000 tokens  ($0.00000015 per token)
#   Output tokens : $0.600 per 1,000,000 tokens  ($0.00000060 per token)
#
#   Example: 200 input + 150 output tokens = $0.000030 + $0.000090 = $0.000120
#   At scale: 1M requests/day × $0.000120 = $120/day in LLM costs
#
# ========================================================================================

import os
import time
from dotenv import load_dotenv

# Load API keys
load_dotenv()

from langchain_core.callbacks import BaseCallbackHandler
from langchain.chat_models import init_chat_model


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# CUSTOM MIDDLEWARE HANDLER: AUDIT, LATENCY & COST TRACKER
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

class AuditAndCostMiddleware(BaseCallbackHandler):
    """
    Custom LangChain middleware handler that provides:
      - Latency measurement (ms-precision stopwatch)
      - Raw prompt auditing (useful for compliance logging)
      - Token usage extraction
      - Estimated API cost calculation

    Attach to any model or chain via: config={"callbacks": [AuditAndCostMiddleware()]}
    """

    # GPT-4o-mini pricing (USD per token) — update for other models
    INPUT_PRICE_PER_TOKEN  = 0.150 / 1_000_000  # $0.150 per 1M input tokens
    OUTPUT_PRICE_PER_TOKEN = 0.600 / 1_000_000  # $0.600 per 1M output tokens

    def on_llm_start(self, serialized: dict, prompts: list, **kwargs) -> None:
        """
        Fires BEFORE the prompt is sent to the model API.
        Use this hook to:
          - Log the raw prompt for compliance auditing
          - Start a latency stopwatch
          - Check prompt length against token limits
        """
        self._start_time = time.time()

        print("\n" + "━"*55)
        print("  [MIDDLEWARE] EVENT: on_llm_start")
        print("━"*55)
        print(f"  Model      : {serialized.get('name', 'Unknown')}")
        print(f"  Prompt     : '{str(prompts[0])[:120]}...' ")
        print(f"  Timestamp  : {time.strftime('%H:%M:%S')}")

    def on_llm_end(self, response, **kwargs) -> None:
        """
        Fires AFTER the model API returns a response.
        Use this hook to:
          - Calculate and log latency
          - Extract token counts from metadata
          - Compute and record API cost
          - Send metrics to dashboards (Datadog, Prometheus, etc.)
        """
        latency_ms = (time.time() - self._start_time) * 1000

        print("\n  [MIDDLEWARE] EVENT: on_llm_end")
        print("━"*55)
        print(f"  Latency    : {latency_ms:.1f} ms")

        # Extract token usage from LLM output metadata
        token_usage = {}
        if response.llm_output:
            token_usage = response.llm_output.get("token_usage", {})

        prompt_tokens     = token_usage.get("prompt_tokens", 0)
        completion_tokens = token_usage.get("completion_tokens", 0)
        total_tokens      = token_usage.get("total_tokens", 0)

        estimated_cost = (
            (prompt_tokens     * self.INPUT_PRICE_PER_TOKEN) +
            (completion_tokens * self.OUTPUT_PRICE_PER_TOKEN)
        )

        print(f"  Tokens In  : {prompt_tokens}")
        print(f"  Tokens Out : {completion_tokens}")
        print(f"  Total Tkns : {total_tokens}")
        print(f"  Est. Cost  : ${estimated_cost:.8f}  ({estimated_cost * 100:.6f} cents)")
        print("━"*55)

    def on_llm_error(self, error: Exception, **kwargs) -> None:
        """
        Fires if the LLM API call throws an exception.
        Use this to alert on-call engineers, write to an error log, or
        trigger a retry circuit breaker.
        """
        print(f"\n  [MIDDLEWARE] ERROR: on_llm_error")
        print(f"  Error type    : {type(error).__name__}")
        print(f"  Error message : {str(error)}")
        print("━"*55)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# SIMPLE READ-ONLY LOGGER — minimal, for quick debugging
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

class SimpleLatencyLogger(BaseCallbackHandler):
    """Minimal callback — only logs latency. Good for quick performance checks."""

    def on_llm_start(self, serialized, prompts, **kwargs):
        self._t = time.time()
        print(f"\n  [Logger] Request started → '{str(prompts[0])[:60]}...'")

    def on_llm_end(self, response, **kwargs):
        print(f"  [Logger] Response received ← {(time.time() - self._t)*1000:.0f} ms")


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# MAIN EXECUTION
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

if __name__ == "__main__":
    try:
        model = init_chat_model("gpt-4o-mini", model_provider="openai")

        # ── Demo 1: Full audit middleware ──────────────────────────────
        print("\n" + "="*70)
        print("DEMO 1: FULL AUDIT + COST MIDDLEWARE")
        print("="*70)

        audit_handler = AuditAndCostMiddleware()

        # Pass callback via config — business logic stays clean
        response = model.invoke(
            "Explain middleware in software engineering in exactly 2 sentences.",
            config={"callbacks": [audit_handler]}
        )
        print(f"\n  Final AI response:\n  '{response.content}'")

        # ── Demo 2: Simple latency logger ─────────────────────────────
        print("\n" + "="*70)
        print("DEMO 2: SIMPLE LATENCY LOGGER")
        print("="*70)

        logger = SimpleLatencyLogger()
        model.invoke(
            "What is 42 * 7?",
            config={"callbacks": [logger]}
        )

    except Exception as e:
        print("\nSetup failed (check API keys):", e)


# ========================================================================================
# REAL-WORLD USE CASES
# ========================================================================================
#
# 1. COMPLIANCE AUDIT LOGGING (Finance/Healthcare):
#    Every prompt sent to OpenAI is logged to a SIEM (Security Information & Event
#    Management) system. If any log contains PII patterns (SSN, credit card), an
#    alert fires before the data leaves the organization.
#
# 2. REAL-TIME COST DASHBOARDS:
#    Token usage from `on_llm_end` is written to a time-series database (InfluxDB,
#    Prometheus). A Grafana dashboard shows LLM spend per user, per feature, per hour.
#    Engineering teams set budget alerts at $X/day thresholds.
#
# 3. LATENCY ALERTING FOR SLAs:
#    A customer-facing chatbot has a p99 latency SLA of < 3 seconds. If `on_llm_end`
#    records a latency > 2.5s, it triggers a PagerDuty alert to on-call engineers.
#
# ========================================================================================
# MNC INTERVIEW QUESTIONS & ANSWERS
# ========================================================================================
#
# Q1. What is the difference between constructor callbacks and invocation callbacks?
# A:  - Constructor callbacks: Passed when creating the model instance. They apply
#       to EVERY call made by that instance globally (good for APM/observability tools).
#     - Invocation callbacks: Passed in config={"callbacks": [...]} per call. They
#       apply only to that specific request (good for per-user or per-session tracking).
#
# Q2. How would you implement global distributed tracing across a LangChain application?
# A:  Use LangSmith (LangChain's official cloud observability platform). Set:
#       LANGCHAIN_TRACING_V2=true
#       LANGCHAIN_API_KEY=ls__...
#       LANGCHAIN_PROJECT=my-project
#     Every chain, agent, and tool call is automatically traced in LangSmith's UI
#     without writing a single callback handler manually.
#
# Q3. Can callbacks be asynchronous?
# A:  Yes. Override the async versions: `async def on_llm_start(...)`,
#     `async def on_llm_end(...)`. These fire when using `.ainvoke()` or `.astream()`
#     in async Python applications (FastAPI, async task queues, etc.).
