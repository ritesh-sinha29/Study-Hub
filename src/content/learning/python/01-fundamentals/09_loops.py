# ==========================================
# PYTHON LOOPS (FOR BEGINNERS)
# ==========================================

# ---
#
# **WHAT IS A LOOP?** ---
# A loop means: "Do this same thing many times automatically."
# Instead of writing print("hello") 100 times, a loop does it for you.

# --- WHY LEARN THIS? ---
# * Sending an email to 1000 users (loop through the list of emails)
# * FastAPI: Loop through a list of items returned from a database
# * LangGraph: Loop through each step of an AI agent workflow
#
# HOW FOR LOOPS WORK INTERNALLY: A for loop calls `iter()` on the collection
# to get an iterator object, then repeatedly calls `next()` on it until a
# StopIteration exception is raised. This is the iterator protocol and means
# you can use for loops on ANY object that implements __iter__ and __next__.
#
# range() is LAZY — it doesn't create a list of numbers in memory. It yields
# one number at a time, making `for i in range(1_000_000):` memory-free.
#
# **KEY INSIGHT:** `break` exits the loop immediately and skips the `else` block
# (if any). `continue` skips the rest of the current iteration and jumps to
# the next one. `else` on a loop runs ONLY if the loop completed without `break`.

print("==========================================")
print("1. FOR LOOP — Loop through a list")
print("==========================================")

# A FOR loop goes through each item in a collection, one by one.
# Think of it as: "For each item in the list, do something."

fruits = ["apple", "banana", "mango"]

for fruit in fruits:
    # `fruit` is a temporary name that holds the current item
    print("I like", fruit)

print()

# ==========================================
print("2. FOR LOOP with range() — Repeat N times")
print("==========================================")

# range(5) gives numbers 0, 1, 2, 3, 4
# Use this when you want to repeat something a fixed number of times.

for i in range(5):
    print("This is line number", i)

print()

# range(start, stop) — starts from `start`, ends BEFORE `stop`
for i in range(1, 6):
    print("Count:", i)

print()

# ==========================================
print("3. WHILE LOOP — Keep looping until condition is False")
print("==========================================")

# A WHILE loop keeps running AS LONG AS a condition is True.
# Think of it as: "While I still have money, keep shopping."

money = 100

while money > 0:
    print("I have", money, "rupees left. Spending 25...")
    money = money - 25  # subtract 25 each time

print("Out of money!")

print()

# ==========================================
print("4. BREAK — Stop the loop early")
print("==========================================")

# `break` immediately exits the loop, even if there are items left.

for i in range(10):
    if i == 5:
        print("Found 5! Stopping the loop.")
        break  # Exit the loop immediately
    print("Number:", i)

print()

# ==========================================
print("5. CONTINUE — Skip current item and go to next")
print("==========================================")

# `continue` skips the rest of the current loop step and moves to the next one.

for i in range(6):
    if i == 3:
        print("Skipping 3!")
        continue  # Skip number 3, continue with 4, 5...
    print("Number:", i)

print()

# ==========================================
print("6. LOOP through a Dictionary")
print("==========================================")

# Very commonly used in FastAPI when processing JSON data (which looks like a dict)

person = {"name": "Ritesh", "age": 20, "city": "Delhi"}

for key, value in person.items():
    print(key, "->", value)

print()

# ==========================================
print("7. FASTAPI USE CASE — Loop through a list of users")
print("==========================================")

# Imagine FastAPI fetches this list from a database and loops to respond:
users = [
    {"id": 1, "name": "Ritesh"},
    {"id": 2, "name": "Rox"},
    {"id": 3, "name": "Shubham"},
]

print("All registered users:")
for user in users:
    print(f"  User ID: {user['id']} | Name: {user['name']}")

# ==========================================
# REAL-LIFE USE CASES
# ==========================================
#
# 1. API Pagination Resolver: Using a while loop to continually fetch pages of
#    results until next_link is empty.
#
# 2. Network Request Retry: Retrying an API call up to 3 times inside a loop
#    if it fails.
#
# 3. Batch Database Processing: Splitting a large list of 10,000 records into
#    smaller chunks of 100 for batch insertion.

# ==========================================
# MNC INTERVIEW QUESTIONS & ANSWERS
# ==========================================
#
# Q1. How does the else clause behave when attached to a for or while loop?
# A:  The loop's else block executes ONLY if the loop completes all iterations
#     naturally without encountering a 'break' statement. If the loop is
#     terminated early by a 'break', the else block is skipped entirely. This
#     is useful for search loops.
#
# Q2. What is the difference between break and continue statements?
# A:  The `break` statement exits the entire loop immediately, ignoring any
#     remaining iterations. It is used to stop processing when a search target
#     is found or an error limit is hit. The `continue` statement skips only
#     the remaining code in the *current* loop iteration and jumps straight to
#     the next iteration's condition check. Use `break` to terminate early,
#     and `continue` to bypass invalid or skipped items within a loop. See the
#     comparison table below:
#     
#     | Statement | Loop Behavior | Next Line Executed |
#     | :--- | :--- | :--- |
#     | `break` | Terminates loop immediately | First line outside the loop |
#     | `continue` | Skips rest of current iteration | Next iteration evaluation |
#
# Q3. Why is range() memory-efficient even when generating large sequences?
# A:  In Python 3, range() returns a lazy sequence object (an iterator), not a
#     fully populated list. It computes numbers dynamically on-demand during
#     iteration, using O(1) memory regardless of how large the range is.