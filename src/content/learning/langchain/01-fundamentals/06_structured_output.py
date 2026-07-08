# ========================================================================================
# LANGCHAIN CRASH COURSE — MODULE 06: STRUCTURED OUTPUT ENFORCEMENT
# ========================================================================================
#
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# SECTION 1 — THE PROBLEM WITH FREE-FORM LLM OUTPUT
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#
# When you ask a model to "return JSON", it might do any of these:
#   - Return valid JSON ✓
#   - Return JSON wrapped in markdown: ```json {...} ``` (your JSON parser breaks)
#   - Return almost-valid JSON with trailing commas (parse error)
#   - Return a paragraph ABOUT the JSON instead of the JSON itself
#
# For production pipelines (APIs, databases, downstream services), you need
# GUARANTEED structured output — not "usually structured" output.
#
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# SECTION 2 — HOW `.with_structured_output()` ENFORCES STRUCTURE
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#
# LangChain's `.with_structured_output(Schema)` uses TWO mechanisms under the hood,
# depending on what the model provider supports:
#
# METHOD A — FUNCTION/TOOL CALLING:
#   The schema is sent as a tool definition. The model is constrained to output
#   a JSON matching the tool arguments schema. Used by: OpenAI, Anthropic, Gemini.
#
# METHOD B — JSON SCHEMA MODE (OpenAI "Structured Outputs" API):
#   The API uses a grammar-constrained token sampler that literally cannot generate
#   tokens that violate the JSON schema. Used with `strict=True` on GPT-4o models.
#
#  ┌──────────────────────────────────────────────────────────────────────┐
#  │               STRUCTURED OUTPUT PIPELINE                             │
#  │                                                                      │
#  │  [Pydantic Schema]                                                   │
#  │       │                                                              │
#  │       ▼                                                              │
#  │  model.with_structured_output(Schema)                               │
#  │       │                                                              │
#  │       ▼                                                              │
#  │  [API: JSON Schema constraint applied]                               │
#  │       │                                                              │
#  │       ▼                                                              │
#  │  [Model outputs strict JSON]                                         │
#  │       │                                                              │
#  │       ▼                                                              │
#  │  [Pydantic validates + instantiates the Python object]              │
#  │       │                                                              │
#  │       ▼                                                              │
#  │  result.name, result.email, result.phone  ← direct attribute access │
#  └──────────────────────────────────────────────────────────────────────┘
#
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# SECTION 3 — PYDANTIC VS TYPEDDICT: WHEN TO USE WHICH
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#
#  CRITERIA         │ PYDANTIC (BASEMODEL)              │ TYPEDDICT
#  ─────────────────┼───────────────────────────────────┼────────────────────────────────
#  Return Format    │ Python Object (dot access)        │ Plain Dictionary (key access)
#  Validation       │ Strict runtime type validation    │ None (static type checking only)
#  Model Guidance   │ Excellent (via Field descriptions)│ Moderate (via comments/types)
#  Primary Use Case │ API schemas, validated inputs     │ LangGraph state whiteboard
#
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# SECTION 4 — FIELD DESCRIPTIONS AS MODEL INSTRUCTIONS
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#
# Field(description="...") serves a dual purpose:
#   1. Documents the field for human developers.
#   2. Acts as instructions for the model on how to populate this field.
#
# Example:
#   sentiment: str = Field(description=(
#       "The emotional tone of the text. Must be exactly one of: "
#       "'positive', 'negative', or 'neutral'."
#   ))
#
# The model reads this description and constrains its output accordingly.
#
# ========================================================================================

import os
from typing import Optional, List
from dotenv import load_dotenv

# Load API keys
load_dotenv()

from pydantic import BaseModel, Field
from typing_extensions import TypedDict
from langchain.chat_models import init_chat_model


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# SCHEMA DEFINITIONS
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

# 1. Pydantic Schema — for contact information extraction
class ContactInfo(BaseModel):
    """Schema for extracting contact details from unstructured text."""
    name:  str           = Field(description="The full legal name of the person.")
    email: str           = Field(description="The email address in standard format (user@domain.com).")
    phone: Optional[str] = Field(None, description="Phone number if mentioned, otherwise null.")

# 2. Pydantic Schema — for sentiment analysis
class SentimentAnalysis(BaseModel):
    """Schema for analyzing the sentiment of a customer review."""
    sentiment: str  = Field(description="Emotional tone. Must be exactly: 'positive', 'negative', or 'neutral'.")
    confidence: float = Field(description="Confidence score between 0.0 (uncertain) and 1.0 (certain).")
    reason: str     = Field(description="One-sentence explanation of why this sentiment was assigned.")

# 3. TypedDict Schema — for book information (plain dict output)
class BookInfo(TypedDict):
    title:          str
    author:         str
    year_published: int
    genre:          str


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# EXAMPLE 1: CONTACT INFO EXTRACTION (PYDANTIC)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def demonstrate_contact_extraction(model):
    print("\n" + "="*70)
    print("EXAMPLE 1: EXTRACTING CONTACT INFO INTO PYDANTIC OBJECT")
    print("="*70)

    structured_model = model.with_structured_output(ContactInfo)

    raw_text = (
        "Hi there! I'm Ritesh Sinha. You can reach me at ritesh@example.com "
        "or call me on my mobile at +91-9876543210. Looking forward to hearing from you."
    )
    print(f"  Input: '{raw_text}'")

    try:
        result: ContactInfo = structured_model.invoke(raw_text)

        print(f"\n  Extracted ContactInfo Object:")
        print(f"    name  : {result.name}")
        print(f"    email : {result.email}")
        print(f"    phone : {result.phone}")
        print(f"    type  : {type(result).__name__}")
    except Exception as e:
        print(f"  [ERROR]: {e}")


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# EXAMPLE 2: SENTIMENT ANALYSIS (PYDANTIC WITH FLOAT + STRING CONSTRAINTS)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def demonstrate_sentiment_analysis(model):
    print("\n" + "="*70)
    print("EXAMPLE 2: SENTIMENT ANALYSIS WITH CONFIDENCE SCORE")
    print("="*70)

    structured_model = model.with_structured_output(SentimentAnalysis)

    review = "The delivery was incredibly fast and the product exceeded my expectations. Highly recommend!"
    print(f"  Review: '{review}'")

    try:
        result: SentimentAnalysis = structured_model.invoke(
            f"Analyze the sentiment of this customer review: {review}"
        )
        print(f"\n  Sentiment Analysis Result:")
        print(f"    sentiment  : {result.sentiment}")
        print(f"    confidence : {result.confidence:.0%}")
        print(f"    reason     : {result.reason}")
    except Exception as e:
        print(f"  [ERROR]: {e}")


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# EXAMPLE 3: BOOK INFO EXTRACTION (TYPEDDICT — PLAIN DICT OUTPUT)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def demonstrate_typeddict_extraction(model):
    print("\n" + "="*70)
    print("EXAMPLE 3: BOOK INFO EXTRACTION INTO TYPEDDICT (PLAIN DICT)")
    print("="*70)

    structured_model = model.with_structured_output(BookInfo)

    request = "Extract structured info for: 'To Kill a Mockingbird' by Harper Lee, 1960, fiction."
    print(f"  Request: '{request}'")

    try:
        result: BookInfo = structured_model.invoke(request)

        print(f"\n  Extracted BookInfo Dictionary:")
        print(f"    title          : {result.get('title')}")
        print(f"    author         : {result.get('author')}")
        print(f"    year_published : {result.get('year_published')}")
        print(f"    genre          : {result.get('genre')}")
        print(f"    type           : {type(result).__name__}")
    except Exception as e:
        print(f"  [ERROR]: {e}")


if __name__ == "__main__":
    try:
        model = init_chat_model("gpt-4o-mini", model_provider="openai")
        demonstrate_contact_extraction(model)
        demonstrate_sentiment_analysis(model)
        demonstrate_typeddict_extraction(model)
    except Exception as e:
        print("\nSetup failed (check API keys):", e)


# ========================================================================================
# REAL-WORLD USE CASES
# ========================================================================================
#
# 1. CUSTOMER REGISTRATION BOT:
#    A WhatsApp chatbot asks users for signup info. Instead of parsing free text,
#    `.with_structured_output(UserRegistration)` extracts name, email, DOB and
#    immediately inserts the Pydantic object into the PostgreSQL users table.
#
# 2. DOCUMENT INTELLIGENCE PIPELINE:
#    Processing 10,000 insurance claim letters. Each letter is passed through a
#    structured model that extracts: claimant_name, incident_date, damage_amount,
#    policy_number. The output is directly inserted into a claims database.
#
# 3. E-COMMERCE PRODUCT CATALOGING:
#    Sellers submit unstructured product descriptions. A structured model extracts:
#    product_name, brand, category, price, dimensions. Validated by Pydantic before
#    publishing to the catalog API.
#
# ========================================================================================
# MNC INTERVIEW QUESTIONS & ANSWERS
# ========================================================================================
#
# Q1. How does `.with_structured_output()` handle bad model responses?
# A:  - For function-calling mode: If the model returns malformed JSON, LangChain
#       raises a JSONDecodeError. You can wrap in a retry chain using
#       `chain.with_retry(stop_after_attempt=3)`.
#     - For strict OpenAI Structured Outputs (strict=True): The API guarantees
#       valid JSON — invalid output is impossible at the token level.
#
# Q2. Can you use `.with_structured_output()` for nested schemas?
# A:  Yes. Pydantic supports nested models:
#       class Address(BaseModel):
#           street: str
#           city: str
#       class User(BaseModel):
#           name: str
#           address: Address   ← nested model
#     LangChain serializes the full nested schema and the model populates all levels.
#
# Q3. When would you choose TypedDict over Pydantic for structured outputs?
# A:  Use TypedDict when building LangGraph state schemas (the LangGraph state
#     system uses TypedDict natively) or when you want simple dict access without
#     class instantiation. Use Pydantic when you need runtime validation
#     (e.g., "confidence must be between 0 and 1") or Field descriptions.
