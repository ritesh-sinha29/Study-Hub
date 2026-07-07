# ==========================================
# PYTHON LIST COMPREHENSIONS (FOR BEGINNERS)
# ==========================================

# ---
#
# **WHAT IS A LIST COMPREHENSION?** ---
# A list comprehension is a SHORT and CLEAN way to create a new list
# from an existing list (or any collection), often in just ONE line.

# --- SIMPLE ANALOGY ---
# Normal way: Take each apple from the basket, check if it's red, put it in a new basket.
# Comprehension: [apple for apple in basket if apple is red]  ← Same thing, one line!

# --- WHY LEARN THIS? ---
# * FastAPI: Filter or transform a list of database results quickly
# * LangGraph: Process a list of AI messages or tool outputs
# * Everywhere: Whenever you loop over a list to create a new one
#
# **HOW IT WORKS:** A list comprehension is syntactic sugar for a for-loop with
# an append. Python evaluates the entire comprehension EAGERLY and stores all
# results in a new list in memory immediately.
#
# MEMORY TIP: For very large datasets, replace `[...]` with `(...)` to get a
# generator expression instead — it produces values one at a time (lazy),
# using O(1) memory instead of O(n).
#
# TERNARY SYNTAX inside comprehensions:
#   [x if condition else y for x in items]   ← transform every item
#   [x for x in items if condition]           ← filter items out
# These look similar but behave very differently — the first never skips items.
#
# KEY INSIGHT: Nested comprehensions are possible but readability suffers fast.
# `[val for row in matrix for val in row]` is fine; anything deeper should
# be a regular for-loop.

print("==========================================")
print("1. NORMAL LOOP vs LIST COMPREHENSION")
print("==========================================")

numbers = [1, 2, 3, 4, 5]

# Normal for loop way (4 lines):
squares_normal = []
for n in numbers:
    squares_normal.append(n * n)
print("Normal loop squares:", squares_normal)

# List comprehension way (1 line — same result!):
# Syntax: [expression  for  item  in  collection]
squares_short = [n * n for n in numbers]
print("Comprehension squares:", squares_short)

print()

# ==========================================
print("2. LIST COMPREHENSION WITH IF CONDITION")
print("==========================================")

# You can filter items using `if` at the end
# Syntax: [expression  for  item  in  collection  if  condition]

numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

# Get only even numbers:
even_numbers = [n for n in numbers if n % 2 == 0]
print("Even numbers:", even_numbers)

# Get only numbers greater than 5:
big_numbers = [n for n in numbers if n > 5]
print("Numbers > 5:", big_numbers)

print()

# ==========================================
print("3. TRANSFORMING DATA IN A LIST")
print("==========================================")

# Convert all names to uppercase:
names = ["ritesh", "rox", "shubham"]
upper_names = [name.upper() for name in names]
print("Uppercase names:", upper_names)

# Add "Hello, " before each name:
greetings = [f"Hello, {name.title()}!" for name in names]
print("Greetings:", greetings)

print()

# ==========================================
print("4. LIST COMPREHENSION FROM A DICT LIST")
print("==========================================")

# This is VERY common in FastAPI when processing database results

users = [
    {"id": 1, "name": "Ritesh", "is_active": True},
    {"id": 2, "name": "Rox",    "is_active": False},
    {"id": 3, "name": "Sam",    "is_active": True},
]

# Get only active users' names:
active_names = [user["name"] for user in users if user["is_active"]]
print("Active users:", active_names)

# Get all user IDs:
all_ids = [user["id"] for user in users]
print("All IDs:", all_ids)

print()

# ==========================================
print("5. DICT COMPREHENSION (same idea, but for dicts)")
print("==========================================")

# You can also create dictionaries the same way!
# Syntax: {key: value  for  item  in  collection}

# Create a dict mapping name → length of name
names = ["Ritesh", "Rox", "Shubham"]
name_lengths = {name: len(name) for name in names}
print("Name lengths:", name_lengths)

print()

# ==========================================
print("6. FASTAPI USE CASE — Transform DB results")
print("==========================================")

# In FastAPI, when you fetch users from a database, you often want
# to extract only certain fields before sending the response.

db_users = [
    {"id": 1, "name": "Ritesh", "password": "secret123", "age": 20},
    {"id": 2, "name": "Rox",    "password": "abc456",    "age": 22},
]

# Never send passwords in the API response!
# Use list comprehension to extract only safe fields:
safe_users = [{"id": u["id"], "name": u["name"], "age": u["age"]} for u in db_users]
print("Safe API response (no passwords):", safe_users)

# ==========================================
# REAL-LIFE USE CASES
# ==========================================
#
# 1. Database Record Filtering: Creating lists of IDs matching specific
#    parameters in one line.
#
# 2. Matrix Transposition: Flattening multidimensional lists or data tables
#    easily.
#
# 3. Data Cleansing: Trimming whitespace from a list of user input fields.

# ==========================================
# MNC INTERVIEW QUESTIONS & ANSWERS
# ==========================================
#
# Q1. When should you NOT use a list comprehension?
# A:  Do not use list comprehensions if the code is highly complex (e.g.
#     multiple nested loops or complex conditional checks). In those cases,
#     normal for-loops are more readable. Also, avoid them for very large
#     datasets where memory conservation is important (use generator
#     expressions instead).
#
# Q2. What is the difference between a list comprehension and a generator
#     expression?
# A:  A list comprehension evaluates eagerly, immediately building and storing
#     the entire list of elements in memory. A generator expression evaluates
#     lazily, returning an iterator object that generates items one-at-a-time
#     on-demand. Use list comprehensions for small datasets where you need
#     list features (like indexing, slicing, or multiple iterations), and
#     generator expressions for large or infinite datasets to keep memory
#     usage extremely low. See the comparison table below:
#     
#     | Feature | List Comprehension | Generator Expression |
#     | :--- | :--- | :--- |
#     | **Syntax** | Square brackets `[...]` | Parentheses `(...)` |
#     | **Evaluation** | Immediate (eager) | Lazy (on-demand) |
#     | **Return Type** | List | Generator object |
#     | **Memory Profile**| Uses `O(n)` RAM | Uses `O(1)` RAM |
#
# Q3. Can you use else blocks inside list comprehensions?
# A:  Yes. The syntax shifts depending on usage: 1) Filtering: `[x for x in
#     list if condition]` (only filters items). 2) Ternary assignment: `[x if
#     condition else default for x in list]` (assigns values based on
#     condition).