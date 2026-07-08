# ==========================================
# PYTHON GENERATORS & ITERATORS (FOR BEGINNERS)
# ==========================================

# ---
#
# **WHAT IS A GENERATOR?** ---
# A generator is a special function that produces values ONE AT A TIME
# instead of creating the whole list in memory at once.
# It uses the `yield` keyword instead of `return`.

# --- SIMPLE ANALOGY ---
# Normal function: Like a water tank — fills up completely first, then you use it.
# Generator: Like a tap — gives you water on demand, one drop at a time.
#            Much more memory efficient for large data!

# --- WHY LEARN THIS? ---
# * LangGraph / LangChain: Streaming AI responses word by word (not waiting for full reply)
# * FastAPI: Streaming large file downloads or real-time data
# * Processing large CSV files without loading everything into memory
#
# **HOW IT WORKS INTERNALLY:** When Python sees `yield` inside a function, it
# compiles it as a generator function. Calling it returns a generator OBJECT
# (no code runs yet). Each call to `next()` resumes execution from the last
# `yield`, runs until the next `yield`, pauses again, and hands the value
# back to the caller. The generator's entire local state (variables, loop
# counters, etc.) is preserved between calls.
#
# MEMORY ADVANTAGE: A regular function returning a list of 1 million items
# allocates ~8 MB of RAM. A generator producing the same items uses only a
# few dozen bytes — the list doesn't exist until you iterate.
#
# **KEY INSIGHT:** Generators are single-use. Once exhausted (StopIteration is
# raised), you cannot restart them. You must create a new generator object
# by calling the generator function again.

print("==========================================")
print("1. NORMAL FUNCTION vs GENERATOR")
print("==========================================")

# Normal function — creates the ENTIRE list in memory first:
def get_numbers_normal(n):
    numbers = []
    for i in range(n):
        numbers.append(i)
    return numbers  # Returns ALL at once

# Generator function — produces values ONE AT A TIME using `yield`:
def get_numbers_generator(n):
    for i in range(n):
        yield i  # Pauses here, gives ONE value, then resumes next time

normal_result = get_numbers_normal(5)
print("Normal list:", normal_result)

gen = get_numbers_generator(5)
print("Generator object:", gen)  # Doesn't show numbers yet!
print("Getting values one by one:")
print("  next():", next(gen))    # Gets 0
print("  next():", next(gen))    # Gets 1
print("  next():", next(gen))    # Gets 2

print()

# ==========================================
print("2. LOOPING THROUGH A GENERATOR")
print("==========================================")

# You can loop through a generator just like a list

def count_up(start, end):
    current = start
    while current <= end:
        yield current
        current += 1

print("Counting from 1 to 5 using generator:")
for number in count_up(1, 5):
    print("  Number:", number)

print()

# ==========================================
print("3. GENERATOR EXPRESSION (like list comprehension, but lazy)")
print("==========================================")

# Use () instead of [] to make a generator expression

# List comprehension (creates ALL in memory):
squares_list = [n * n for n in range(10)]

# Generator expression (creates ONE at a time):
squares_gen = (n * n for n in range(10))

print("List type:", type(squares_list))
print("Generator type:", type(squares_gen))

print("Squares from generator:")
for square in squares_gen:
    print(f"  {square}", end=" ")
print()

print()

# ==========================================
print("4. STREAMING USE CASE — LangGraph / AI Responses")
print("==========================================")

# In LangGraph and LangChain, AI models stream their responses.
# Instead of waiting for the FULL response, you get words one by one.
# This is done using generators!

import time

def stream_ai_response(full_text):
    # Simulate streaming: yield one word at a time
    words = full_text.split()
    for word in words:
        yield word  # Send one word at a time
        # In real code, there's a tiny delay between words

print("Streaming AI response word by word:")
response = "Hello! I am your AI assistant. How can I help you today?"

# This simulates how LangChain/LangGraph streams to the user
streamed_text = ""
for word in stream_ai_response(response):
    streamed_text += word + " "
    print(f"  ..received: '{word}'")

print("\nFull response:", streamed_text)

print()

# ==========================================
print("5. FASTAPI USE CASE — Streaming Response")
print("==========================================")

# In FastAPI, you can stream large files or data using generators.
# Real FastAPI streaming code:
#
#   from fastapi.responses import StreamingResponse
#
#   def generate_large_file():
#       for chunk in read_large_file_in_chunks():
#           yield chunk  # Send data piece by piece
#
#   @app.get("/download")
#   def download_file():
#       return StreamingResponse(generate_large_file(), media_type="text/plain")

print("FastAPI streaming pattern shown in comments above.")
print("Key idea: yield sends data chunk by chunk to the client.")

# ==========================================
# REAL-LIFE USE CASES
# ==========================================
# 1. Large Log Streaming: Reading a 10GB server log file line-by-line using a
#    - **Step 1**: Generator without exhausting RAM.
#
# 2. Infinite Sequences: Generating an infinite stream of unique IDs or
#    - **Step 1**: Numbers dynamically.
#
# 3. Lazy Database Query Pagination: Fetching database pages of 100 rows only
#    - **Step 1**: When requested by the consumer.

# ==========================================
# MNC INTERVIEW QUESTIONS & ANSWERS
# ==========================================
#
# Q1. What is the difference between an iterable and an iterator?
# A:  An iterable is any object that can return its elements one by one,
#     typically implementing `__iter__` (like lists, tuples, and strings). An
#     iterator is a stateful cursor that keeps track of the current position
#     during iteration, implementing both `__iter__` and `__next__`. Calling
#     `iter()` on an iterable returns an iterator. Iterables can be iterated
#     over multiple times, whereas iterators are consumed after a single
#     traversal. See the comparison table below:
#     
#     | Feature | Iterable | Iterator |
#     | :--- | :--- | :--- |
#     | **Definition** | Holds raw sequence | Stateful cursor performing iteration |
#     | **Methods** | `__iter__` | `__iter__` and `__next__` |
#     | **Behavior** | Can be reset / re-read | Consumed after single traversal |
#
# Q2. How does the yield keyword work compared to return?
# A:  `return` terminates the function's execution permanently, returning the
#     specified value and destroying its local namespace and stack frame.
#     `yield` temporarily pauses the function's execution, returns the yielded
#     value to the consumer, and saves the entire state of the function
#     (variables, instruction cursor) so that it can resume right where it
#     left off on the next call. Use `return` for standard functions, and
#     `yield` to create memory-efficient generators. See the comparison table
#     below:
#     
#     | Keyword | Function Execution | State Preservation |
#     | :--- | :--- | :--- |
#     | `return` | Terminates function permanently | Discards local frame |
#     | `yield` | Pauses function temporarily | Saves state for next call |
#
# Q3. What is the purpose of the 'yield from' statement?
# A:  yield from (introduced in Python 3.3) allows a generator to delegate
#     part of its operations to another generator or iterable, avoiding the
#     need for nested loops (e.g., `yield from [x for x in sub()]`).