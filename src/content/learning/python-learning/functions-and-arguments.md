# Functions & Arguments

```python
# ==========================================
# PYTHON FUNCTIONS (FOR BEGINNERS)
# ==========================================

# --- WHAT IS A FUNCTION? ---
# A function is a block of reusable code that does ONE specific task.
# Instead of writing the same code again and again, you write it once 
# inside a function and just CALL it whenever needed.

# --- REAL-WORLD USE CASES ---
# * FastAPI: EVERY API route (endpoint) is a function.
#   e.g., @app.get("/users") -> def get_users(): ...
# * LangGraph: Every "node" in the AI graph is a function.
# * Anywhere: Reuse the same calculation (like tax) without rewriting it.

# To CREATE a function, use the keyword `def` (short for "define")
# Syntax:  def function_name(parameters):

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
```
