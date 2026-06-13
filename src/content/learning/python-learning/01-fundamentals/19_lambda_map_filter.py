# ==========================================
# PYTHON LAMBDA, MAP, FILTER (FOR BEGINNERS)
# ==========================================

# --- WHAT IS A LAMBDA? ---
# A lambda is a TINY, one-line, anonymous (no name) function.
# Use it when you need a simple function in one place and don't want
# to write a full `def` function for it.

# --- REAL-WORLD USE CASES ---
# * Sorting: Sort a list of users by their age using a lambda
# * LangGraph: Pass small processing functions as callbacks to nodes
# * map/filter: Transform or filter large lists quickly

print("==========================================")
print("1. NORMAL FUNCTION vs LAMBDA")
print("==========================================")

# Normal function:
def square(x):
    return x * x

# Lambda (same function, one line):
# Syntax: lambda parameters: expression
square_lambda = lambda x: x * x

print("Normal function:", square(5))
print("Lambda function:", square_lambda(5))

print()

# ==========================================
print("2. LAMBDA WITH MULTIPLE PARAMETERS")
print("==========================================")

add = lambda a, b: a + b
multiply = lambda a, b: a * b
greet = lambda name: f"Hello, {name}!"

print("Add 3 + 7:", add(3, 7))
print("Multiply 4 * 5:", multiply(4, 5))
print(greet("Ritesh"))

print()

# ==========================================
print("3. SORTING WITH LAMBDA")
print("==========================================")

# This is the MOST COMMON use of lambda in real code.
# Use it as the `key` argument in sort() or sorted().

users = [
    {"name": "Ritesh",  "age": 20},
    {"name": "Shubham", "age": 18},
    {"name": "Rox",     "age": 25},
]

# Sort users by age using lambda:
sorted_users = sorted(users, key=lambda user: user["age"])
print("Sorted by age:")
for user in sorted_users:
    print(f"  {user['name']} — {user['age']}")

print()

# ==========================================
print("4. MAP — Apply a function to every item in a list")
print("==========================================")

# map(function, list) → applies the function to EACH item
# Returns a map object, so wrap it in list() to see the result.

numbers = [1, 2, 3, 4, 5]

# Without lambda (normal way):
doubled_normal = [n * 2 for n in numbers]
print("Doubled (list comprehension):", doubled_normal)

# With map + lambda:
doubled_map = list(map(lambda n: n * 2, numbers))
print("Doubled (map + lambda):", doubled_map)

# Another example: Convert all names to uppercase
names = ["ritesh", "rox", "shubham"]
upper_names = list(map(lambda name: name.upper(), names))
print("Uppercase names:", upper_names)

print()

# ==========================================
print("5. FILTER — Keep only items that match a condition")
print("==========================================")

# filter(function, list) → keeps items where function returns True

numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

# Keep only even numbers:
even_numbers = list(filter(lambda n: n % 2 == 0, numbers))
print("Even numbers:", even_numbers)

# Keep only users who are active:
users = [
    {"name": "Ritesh", "is_active": True},
    {"name": "Rox",    "is_active": False},
    {"name": "Sam",    "is_active": True},
]
active_users = list(filter(lambda u: u["is_active"], users))
print("Active users:", [u["name"] for u in active_users])

print()

# ==========================================
print("6. LANGGRAPH USE CASE — Lambda as a condition check")
print("==========================================")

# In LangGraph, you pass a function (often a lambda) to decide which
# path the AI agent should take next (called a "conditional edge").

# Example: After the agent responds, should we END or RETRY?

def should_retry(state):
    # In real LangGraph, `state` holds the conversation history
    last_message = state.get("last_message", "")
    # Lambda condition: retry if the message contains "error"
    check = lambda msg: "error" in msg.lower()
    return "retry" if check(last_message) else "end"

state1 = {"last_message": "Task completed successfully"}
state2 = {"last_message": "An error occurred in the tool"}

print("State 1 result:", should_retry(state1))  # end
print("State 2 result:", should_retry(state2))  # retry

# ==========================================
# REAL-LIFE USE CASES
# ==========================================
#
# 1. Sorting Key Selectors: Passing a temporary lambda function to sort a list
#    of dictionaries by nested keys.
#
# 2. GUI Callbacks: Writing simple one-liner handler callbacks in desktop or
#    web applications.
#
# 3. Data Pipeline Transformers: Applying map/filter transformations to list
#    collections.

# ==========================================
# MNC INTERVIEW QUESTIONS & ANSWERS
# ==========================================
#
# Q1. What are the limitations of lambda functions in Python?
# A:  Lambda functions must consist of a single expression; they cannot
#     contain statements (like 'assert', 'pass', or loops) or assignment
#     expressions. They are designed for simple anonymous logic. If logic
#     exceeds one expression, use a standard function (def).
#
# Q2. How do map() and filter() compare to list comprehensions?
# A:  Comprehensions are generally considered more readable and pythonic by
#     the community. Additionally, comprehensions avoid the overhead of
#     function calls inside map/filter. However, map/filter return iterators,
#     meaning they compute values lazily, which can be memory-efficient.
#
# Q3. What does the functools.reduce() function do?
# A:  reduce(function, iterable) applies a function of two arguments
#     cumulatively to the items of an iterable, from left to right, to reduce
#     the iterable to a single cumulative value (e.g. summing all numbers,
#     finding factorial).