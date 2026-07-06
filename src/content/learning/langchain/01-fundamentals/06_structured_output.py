# ==========================================================
# LANGCHAIN STUDY GUIDE: 06. STRUCTURED OUTPUT
# ==========================================================

# --- STRUCTURED OUTPUTS ---
# LLMs usually return unstructured text. For application development, we often need data in a
# structured format (like JSON or Python objects) for parsing and integration.
# LangChain provides a built-in method `.with_structured_output()` on chat models.
#
# It supports:
# 1. Pydantic Models (Recommended, provides validation out of the box)
# 2. TypedDict (Standard dictionary structure with type hints)
# 3. Python Dataclasses

import os
from typing import Optional
from dotenv import load_dotenv
from pydantic import BaseModel, Field
from typing_extensions import TypedDict
from dataclasses import dataclass
from langchain.chat_models import init_chat_model

load_dotenv()

# --- 1. PYDANTIC SCHEMA DEFINITION ---
class ContactInfo(BaseModel):
    name: str = Field(description="The full name of the contact person.")
    email: str = Field(description="The contact email address.")
    phone: Optional[str] = Field(None, description="The phone number, if available.")

# --- 2. TYPEDDICT SCHEMA DEFINITION ---
class BookInfo(TypedDict):
    title: str
    author: str
    year_published: int

# --- 3. DATACLASS SCHEMA DEFINITION ---
@dataclass
class MovieInfo:
    title: str
    director: str
    rating: float

if __name__ == "__main__":
    try:
        model = init_chat_model("gpt-4o-mini", model_provider="openai")
        
        # A. Structured output with Pydantic
        print("--- A. PYDANTIC STRUCTURED OUTPUT ---")
        structured_model_pydantic = model.with_structured_output(ContactInfo)
        res_pydantic = structured_model_pydantic.invoke("My name is Ritesh Sinha, reach me at ritesh@example.com or 123-456-7890.")
        print("Type:", type(res_pydantic))
        print("Data:", res_pydantic)

        # B. Structured output with TypedDict
        print("\n--- B. TYPEDDICT STRUCTURED OUTPUT ---")
        structured_model_dict = model.with_structured_output(BookInfo)
        res_dict = structured_model_dict.invoke("Generate info for the book 'To Kill a Mockingbird' by Harper Lee in 1960.")
        print("Type:", type(res_dict))
        print("Data:", res_dict)

    except Exception as e:
        print("Structured output invocation failed (check API keys):", e)

# ==========================================================
# REAL-LIFE USE CASES
# ==========================================================
# 1. INFORMATION EXTRACTION: Parsing unstructured emails, PDFs, or support chats to extract names,
#    dates, ticket numbers, and categories directly into database-ready structures.
# 2. API RESPONSE GENERATION: Ensuring that the agent answers queries in a format conforming to a
#    pre-defined JSON API contract.

# ==========================================================
# MNC INTERVIEW QUESTIONS & ANSWERS
# ==========================================================
# Q1. How does `.with_structured_output()` work under the hood?
# A:  It relies on the model provider's native structured outputs feature (like OpenAI's JSON mode
#     or tool-calling capabilities). It wraps the model's call, passes the target schema as a tool/function
#     schema, and parses the response back into the requested Pydantic, TypedDict, or dataclass object.
#
# Q2. When should you use Pydantic vs TypedDict for structured output?
# A:  - Use Pydantic when you need runtime validation, default values, and schema field descriptions
#       to guide the model's understanding of each field.
#     - Use TypedDict when you want plain Python dictionaries without class instantiation overhead.
