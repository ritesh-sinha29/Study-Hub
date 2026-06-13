# Generators & Iterators

```python
# ==========================================
# PYTHON GENERATORS & ITERATORS (FOR BEGINNERS)
# ==========================================

# --- WHAT IS A GENERATOR? ---
# A generator is a special function that produces values ONE AT A TIME
# instead of creating the whole list in memory at once.
# It uses the `yield` keyword instead of `return`.

# --- SIMPLE ANALOGY ---
# Normal function: Like a water tank — fills up completely first, then you use it.
# Generator: Like a tap — gives you water on demand, one drop at a time.
#            Much more memory efficient for large data!

# --- REAL-WORLD USE CASES ---
# * LangGraph / LangChain: Streaming AI responses word by word (not waiting for full reply)
# * FastAPI: Streaming large file downloads or real-time data
# * Processing large CSV files without loading everything into memory

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
    print(f"  ...received: '{word}'")

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
```
