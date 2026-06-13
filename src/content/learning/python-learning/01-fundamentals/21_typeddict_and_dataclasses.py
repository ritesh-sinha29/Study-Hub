# ==========================================
# TYPEDDICT & DATACLASSES (FOR BEGINNERS)
# ==========================================

# --- WHY ARE THESE IMPORTANT? ---
# Both TypedDict and dataclasses are ways to create STRUCTURED data containers.
# They tell Python (and your editor) exactly what fields exist and their types.

# LangGraph uses TypedDict to define the STATE of your AI agent.
# FastAPI uses dataclasses and Pydantic models for request/response shapes.

print("==========================================")
print("PART 1: TypedDict")
print("==========================================")

# --- WHAT IS TypedDict? ---
# TypedDict is a dictionary where each key has a FIXED type.
# It's like a regular dict, but with type labels for each field.
# LangGraph's state is ALWAYS defined as a TypedDict.

from typing import TypedDict, List, Optional

# Define the shape of your data:
class UserInfo(TypedDict):
    name: str           # `name` must be a string
    age: int            # `age` must be an integer
    email: str          # `email` must be a string
    is_active: bool     # `is_active` must be True or False

# Create an instance (it's basically a dictionary):
user: UserInfo = {
    "name": "Ritesh",
    "age": 20,
    "email": "ritesh@example.com",
    "is_active": True
}

print("User TypedDict:", user)
print("Access name:", user["name"])
print("Access age:", user["age"])

print()

# ==========================================
print("LANGGRAPH USE CASE — Agent State as TypedDict")
print("==========================================")

# In LangGraph, you define your AI agent's state as a TypedDict.
# Every node (function) in the graph reads and updates this state.

# Example: A simple chatbot agent state
class AgentState(TypedDict):
    messages: List[str]          # List of chat messages
    current_step: str            # Which step the agent is on
    is_complete: bool            # Has the agent finished?
    error: Optional[str]         # Any error message (or None)

# Create initial state:
initial_state: AgentState = {
    "messages": ["Hello! I need help with Python."],
    "current_step": "greeting",
    "is_complete": False,
    "error": None
}

print("Initial Agent State:", initial_state)

# Simulate an agent updating the state:
initial_state["messages"].append("Sure! What do you want to learn?")
initial_state["current_step"] = "awaiting_topic"
print("Updated State:", initial_state)

print()

print("==========================================")
print("PART 2: Dataclasses")
print("==========================================")

# --- WHAT IS A DATACLASS? ---
# A dataclass is a SHORTCUT for creating a class that mainly holds data.
# Without it, you have to write __init__, etc. manually.
# With @dataclass, Python writes all that for you automatically!

from dataclasses import dataclass, field

# Without @dataclass you would write:
# class Point:
#     def __init__(self, x, y):
#         self.x = x
#         self.y = y

# With @dataclass (much shorter!):
@dataclass
class Point:
    x: float    # x coordinate
    y: float    # y coordinate

p1 = Point(3.0, 4.5)
p2 = Point(1.0, 2.0)

print("Point 1:", p1)
print("Point 2:", p2)
print("X of p1:", p1.x)

print()

# Dataclass with default values:
@dataclass
class Product:
    name: str
    price: float
    in_stock: bool = True           # Default value is True
    tags: List[str] = field(default_factory=list)  # Default empty list

p = Product("Python Book", 499.0)
print("Product:", p)
print("Name:", p.name)
print("In stock:", p.in_stock)

print()

# ==========================================
print("FASTAPI USE CASE — Pydantic BaseModel (like a dataclass)")
print("==========================================")

# Pydantic's BaseModel is like a dataclass but with automatic validation.
# It's the MOST important class in FastAPI.

# Real FastAPI code (requires: pip install pydantic):
#
#   from pydantic import BaseModel
#
#   class UserCreateRequest(BaseModel):
#       name: str
#       age: int
#       email: str
#
#   @app.post("/users")
#   def create_user(user: UserCreateRequest):  # FastAPI auto-validates!
#       return {"message": f"User {user.name} created!"}

# Here we simulate it without Pydantic:
@dataclass
class UserCreateRequest:
    name: str
    age: int
    email: str

def create_user(user: UserCreateRequest) -> dict:
    return {"message": f"User {user.name} created successfully!"}

request = UserCreateRequest("Ritesh", 20, "ritesh@example.com")
print("FastAPI-style response:", create_user(request))

# ==========================================
# REAL-LIFE USE CASES
# ==========================================
#
# 1. API Request DTOs: Defining strongly typed data structures representing
#    HTTP request bodies.
#
# 2. JSON Payloads Validation: Describing nested dictionary shapes returned by
#    external APIs.
#
# 3. Domain Configurations: Defining immutable configuration profiles inside
#    classes.

# ==========================================
# MNC INTERVIEW QUESTIONS & ANSWERS
# ==========================================
#
# Q1. What is the difference between a dataclass and a standard Python
#     dictionary?
# A:  A dictionary is a generic, dynamic key-value store that can change shape
#     on the fly, accessed using bracket notation (`dict['key']`). A dataclass
#     is a custom class decorated with `@dataclass` that provides a
#     structured, typed schema accessed via dot notation (`obj.key`).
#     Dataclasses support type validation, autocompletion in IDEs, and
#     object-oriented features like custom methods and inheritance, making
#     them much better for defining fixed domain models. See the comparison
#     table below:
#     
#     | Feature | Dataclass | Dictionary |
#     | :--- | :--- | :--- |
#     | **Access** | Dot notation (obj.x) | Key lookup (obj['x']) |
#     | **Type Check** | Strong static checks | Loose check |
#     | **Overhead** | Lightweight class | Plain hash map |
#
# Q2. What is TypedDict and when should you use it over a dataclass?
# A:  `TypedDict` is a static type checker configuration that tells type
#     checkers (like mypy) what keys a standard Python dictionary should
#     contain, but compiles down to a plain, generic dictionary at runtime. A
#     `dataclass` creates a full custom class and instance with runtime
#     checks, constructor generation, and helper methods. Use `TypedDict` when
#     working with external APIs or existing dictionary structures, and
#     `dataclass` when you need object-oriented methods and runtime
#     initialization safety. See the comparison table below:
#     
#     | Feature | TypedDict | Dataclass |
#     | :--- | :--- | :--- |
#     | **Runtime Type** | Plain `dict` | Custom Class Instance |
#     | **Verification** | Static typing (mypy) only | Full runtime init / methods |
#     | **Operations** | Dict methods (keys/values) | OOP instance methods |
#
# Q3. How does the __post_init__ method work in a dataclass?
# A:  The __post_init__ method is automatically called at the end of the
#     generated __init__ method. It is commonly used to validate attributes,
#     initialize dependent fields, or compute properties that depend on other
#     constructor arguments.