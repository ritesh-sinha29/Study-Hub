# ==========================================
# PYTHON FUNCTIONS (FOR BEGINNERS)
# ==========================================

# ---
#
# **WHAT IS A FUNCTION?** ---
# A function is a block of reusable code that does ONE specific task.
# Instead of writing the same code again and again, you write it once 
# inside a function and just CALL it whenever needed.

# --- WHY LEARN THIS? ---
# * FastAPI: EVERY API route (endpoint) is a function.
#   e.g., @app.get("/users") -> def get_users(): ..
# * LangGraph: Every "node" in the AI graph is a function.
# * Anywhere: Reuse the same calculation (like tax) without rewriting it.

# To CREATE a function, use the keyword `def` (short for "define")
# Syntax:  def function_name(parameters):
#
# **HOW IT WORKS INTERNALLY:** When you call a function, Python creates a new
# "stack frame" in memory for that call — a private workspace containing the
# function's local variables. When the function returns, the frame is destroyed
# and control returns to the caller with the return value.
#
# RETURN vs PRINT: `print()` writes text to the console — humans see it but
# code cannot use it. `return` sends a value back to the caller so other code
# can store it, pass it to another function, or use it in an expression.
# A function without a `return` statement implicitly returns `None`.
#
# **KEY INSIGHT:** Functions with default parameter values (`def greet(name="World")`)
# allow callers to omit that argument. Default values are evaluated ONCE at
# definition time — using a mutable default like `def fn(lst=[])` is a classic
# bug because all callers share the SAME list object.

print("==========================================")
print("1. BASIC FUNCTION — No inputs, no output")
print("==========================================")

def say_hello():
    # This function just prints a greeting whenever called
    print("Hello! Welcome to Python.")

# To use (call) the function, write its name followed by ()
say_hello()
say_hello()  # You can call it as many times as you want!

print()

# ==========================================
print("2. FUNCTION WITH PARAMETERS (inputs)")
print("==========================================")

# Parameters are the inputs you pass into a function.
# Think of it like ordering food: you pass the name of the dish.

def greet_user(name):
    # `name` is a parameter — it receives whatever you pass when calling
    print("Hello,", name, "! Welcome.")

greet_user("Ritesh")   # "Ritesh" is the argument (actual value)
greet_user("Shubham")

print()

# ==========================================
print("3. FUNCTION WITH RETURN VALUE (output)")
print("==========================================")

# A function can also SEND BACK a result using `return`.
# This is extremely important in FastAPI — every route returns a response.

def add_numbers(a, b):
    result = a + b
    return result  # Send the result back to whoever called this function

answer = add_numbers(10, 20)
print("Sum:", answer)

print()

# ==========================================
print("4. DEFAULT PARAMETERS")
print("==========================================")

# You can give a parameter a DEFAULT value.
# If the caller does not provide that value, the default is used.

def greet(name, message="Good morning"):
    print(f"{message}, {name}!")

greet("Ritesh")                   # Uses default message
greet("Rox", "Good evening")     # Overrides the default

print()

# ==========================================
print("5. *args — Accept any number of inputs")
print("==========================================")

# `*args` lets you pass as MANY arguments as you want.
# They are collected into a tuple.

def add_all(*numbers):
    total = 0
    for num in numbers:
        total = total + num
    return total

print("Sum of 1,2,3:", add_all(1, 2, 3))
print("Sum of 1,2,3,4,5:", add_all(1, 2, 3, 4, 5))

print()

# ==========================================
print("6. **kwargs — Accept named inputs")
print("==========================================")

# `**kwargs` lets you pass KEY=VALUE pairs as arguments.
# They are collected into a dictionary.
# FastAPI uses this concept to pass query parameters.

def show_info(**details):
    for key, value in details.items():
        print(f"{key}: {value}")

show_info(name="Ritesh", age=20, city="Delhi")

print()

# ==========================================
print("7. FASTAPI-STYLE FUNCTION EXAMPLE")
print("==========================================")

# This is EXACTLY how a FastAPI route function looks (without the decorator)

def get_user(user_id: int):
    # In FastAPI, this function would be triggered when someone visits /users/1
    users = {1: "Ritesh", 2: "Shubham", 3: "Rox"}
    if user_id in users:
        return {"id": user_id, "name": users[user_id]}
    else:
        return {"error": "User not found"}

print(get_user(1))
print(get_user(99))

# ==========================================
# REAL-LIFE USE CASES
# ==========================================
# 1. Data Validation Filters: Writing reusable utility functions to validate
#    - **Step 1**: Format schemas (e.g. validate_email).
#
# 2. Reusable Math Computation: Encapsulating calculations like tax rates or
#    - **Step 1**: Shipping surcharges.
#
# 3. Shared Logger Utilities: Writing a standardized logging function used
#    - **Step 1**: Across all modules.

# ==========================================
# MNC INTERVIEW QUESTIONS & ANSWERS
# ==========================================
#
# Q1. Why is using a mutable object (like a list or dictionary) as a default
#     argument in Python dangerous?
# A:  Python evaluates default arguments once when the function is defined,
#     not when it is called. If you pass a mutable object as a default (e.g.,
#     `def add(item, lst=[])`), all subsequent function calls without a second
#     parameter will share and mutate the EXACT same list.
#
# Q2. What do *args and **kwargs do in a function definition?
# A:  `*args` allows a function to accept any number of positional arguments,
#     which are collected into a tuple. `**kwargs` allows the function to
#     accept any number of keyword (named) arguments, which are collected into
#     a dictionary. Use `*args` when creating wrappers or functions that
#     process a list of elements, and `**kwargs` when handling named
#     configuration options or passing dynamic parameters to underlying API
#     functions. See the comparison table below:
#     
#     | Parameter | Captures | Received As | Example Call |
#     | :--- | :--- | :--- | :--- |
#     | `*args` | Positional arguments | Tuple | `func(1, 2, 3)` |
#     | `**kwargs` | Keyword arguments | Dictionary | `func(a=1, b=2)` |
#
# Q3. What is the LEGB rule for variable scope lookup in Python?
# A:  It defines the order Python searches scopes for variable resolution:
#     Local (inside the function), Enclosing (in outer nested functions),
#     Global (at the module level), and Built-in (pre-defined Python functions
#     like print(), len()).