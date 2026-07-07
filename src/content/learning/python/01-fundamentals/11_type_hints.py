# ==========================================
# PYTHON TYPE HINTS (FOR BEGINNERS)
# ==========================================

# --- WHAT ARE TYPE HINTS? ---
# Type hints are labels you add to tell Python (and YOU) what TYPE of data
# a variable or function expects. They do NOT crash if wrong, but editors
# will warn you and FastAPI uses them to VALIDATE data automatically.

# --- WHY LEARN THIS? ---
# * FastAPI uses type hints to automatically:
#     - Validate incoming request data
#     - Generate API documentation
#     - Return correct response formats
# * LangGraph uses type hints to define the shape of AI agent state.

# --- BASIC SYNTAX ---
# variable_name: data_type = value
#
# **HOW IT WORKS INTERNALLY:** Type hints are stored in `__annotations__` but
# Python itself does NOT enforce them at runtime — you can still pass the
# wrong type and Python won't crash (unless you're using a validator like
# Pydantic). It is static type checkers like mypy or Pylance (VS Code) that
# read annotations and report mismatches before you even run the code.
#
# WHY FASTAPI USES THEM: FastAPI uses Pydantic under the hood. It reads the
# type hints on your route parameters and request body models, then validates
# the incoming JSON against them automatically. If a field expects `int` and
# receives `"hello"`, FastAPI returns a 422 error with a detailed message.
#
# **KEY INSIGHT:** The `Optional[str]` type means the value can be a `str` OR
# `None`. In Python 3.10+ you can write `str | None` instead. Use `Optional`
# for fields that may be absent in an API request body.

print("==========================================")
print("1. BASIC TYPE HINTS ON VARIABLES")
print("==========================================")

name: str = "Ritesh"         # str = text/string
age: int = 20                # int = whole number
height: float = 5.9          # float = decimal number
is_student: bool = True      # bool = True or False

print("Name:", name)
print("Age:", age)
print("Height:", height)
print("Is student:", is_student)

print()

# ==========================================
print("2. TYPE HINTS ON FUNCTIONS")
print("==========================================")

# You can label what a function EXPECTS (parameters) and what it RETURNS
# Syntax: def function_name(param: type) -> return_type:

def add(a: int, b: int) -> int:
    # This function takes two integers and returns an integer
    return a + b

def greet(name: str) -> str:
    # This function takes a string and returns a string
    return "Hello, " + name

print(add(5, 10))
print(greet("Ritesh"))

print()

# ==========================================
print("3. TYPE HINTS WITH LISTS AND DICTS")
print("==========================================")

# For lists and dicts, we use `list` and `dict` directly (Python 3.9+)

def get_first_item(items: list) -> str:
    return items[0]

def get_user_name(user: dict) -> str:
    return user["name"]

fruits: list = ["apple", "banana", "mango"]
person: dict = {"name": "Ritesh", "age": 20}

print("First fruit:", get_first_item(fruits))
print("User name:", get_user_name(person))

print()

# ==========================================
print("4. OPTIONAL — When a value might be None")
print("==========================================")

# Sometimes a value may or may not exist. We use Optional for that.
# `Optional[str]` means the value is either a str OR None.

from typing import Optional

def find_user(user_id: int) -> Optional[str]:
    # Returns a name if found, or None if not found
    users = {1: "Ritesh", 2: "Rox"}
    return users.get(user_id)  # .get() returns None if key not found

print("User 1:", find_user(1))
print("User 99:", find_user(99))  # Returns None

print()

# ==========================================
print("5. UNION — When a value can be one of multiple types")
print("==========================================")

# `Union[int, str]` means the value can be either an int OR a str.

from typing import Union

def process_id(user_id: Union[int, str]) -> str:
    return f"Processing user with ID: {user_id}"

print(process_id(42))
print(process_id("ritesh_dev"))

print()

# ==========================================
print("6. FASTAPI USE CASE — How FastAPI uses type hints")
print("==========================================")

# This is what a real FastAPI route looks like with type hints.
# FastAPI reads the type hints and:
#   1. Validates the input automatically
#   2. Shows correct types in the auto-generated docs page (/docs)

# (This is just a demonstration — no FastAPI imported here)

def create_user(name: str, age: int, email: str) -> dict:
    # FastAPI will reject the request automatically if:
    # - `age` is not a number
    # - `email` is not a string
    # All thanks to type hints!
    new_user = {
        "name": name,
        "age": age,
        "email": email
    }
    return new_user

print(create_user("Ritesh", 20, "ritesh@example.com"))

# ==========================================
# REAL-LIFE USE CASES
# ==========================================
#
# 1. IDE Code Completion: Enabling static tooling (PyCharm, VS Code) to
#    provide autocomplete for parameters.
#
# 2. API Payloads Documentation: Specifying typing rules for endpoints in web
#    frameworks.
#
# 3. Refactoring Safety: Catching type incompatibility bugs in CI using static
#    analysis tools like mypy.

# ==========================================
# MNC INTERVIEW QUESTIONS & ANSWERS
# ==========================================
#
# Q1. Are Python type hints enforced at runtime?
# A:  No. Python type hints (PEP 484) are purely informational. The Python
#     interpreter does not raise errors or perform type checks at runtime
#     based on hints. You must use static analysis tools like mypy or IDE
#     checkers to validate types.
#
# Q2. What is the difference between Union and Optional type hints?
# A:  `Union[A, B]` indicates that a variable or parameter can accept types of
#     either `A` or `B`. `Optional[A]` is actually a shorthand wrapper for
#     `Union[A, None]`, meaning the parameter can either be of type `A` or it
#     can be `None`. Use `Union` when a variable can hold distinct data types
#     (e.g. string or list), and `Optional` when a parameter is optional and
#     defaults to `None`. See the comparison table below:
#     
#     | Type Hint | Allowed Types | Modern Equivalent (3.10+) |
#     | :--- | :--- | :--- |
#     | `Union[int, str]` | Can be either `int` OR `str` | `int \| str` |
#     | `Optional[int]` | Can be either `int` OR `None` | `int \| None` |
#
# Q3. What is TypeVar and when is it used?
# A:  TypeVar is used to define generic type variables. It allows you to
#     specify type relationships between parameters and return values when the
#     exact types aren't known beforehand (e.g., a function that takes a list
#     of type T and returns an element of type T).