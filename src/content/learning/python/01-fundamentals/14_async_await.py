# ==========================================
# PYTHON ASYNC / AWAIT (FOR BEGINNERS)
# ==========================================

# --- WHAT IS ASYNC/AWAIT? ---
# Normally, Python runs code LINE BY LINE and WAITS for each line to finish.
# `async/await` lets Python do OTHER things while waiting (e.g., for a slow database).

# --- SIMPLE ANALOGY ---
# Normal (Synchronous): You go to a restaurant, order food, and stand at the counter
#                       staring at the wall until the food is ready. You do NOTHING else.
# Async:                You order food, sit down, chat with friends, check your phone.
#                       When the food is ready, you pick it up. You didn't waste time!

# --- WHY LEARN THIS? ---
# * FastAPI: All route functions can be `async def` — they wait for databases
#            without blocking other users' requests.
# * LangGraph: Async lets AI agents make multiple LLM calls at the same time.
# * Web scraping, API calls, file reading — any "waiting" task benefits from async.
#
# **HOW IT WORKS INTERNALLY:** Python runs async code on a single-threaded EVENT
# LOOP. When your code hits `await`, it pauses the current coroutine and hands
# control back to the loop, which can then run other waiting coroutines. There
# is no multi-threading — only cooperative multitasking.
#
# COROUTINE vs THREAD: Threads are managed by the OS and can truly run in
# parallel (on multiple cores) but have overhead and race conditions.
# Coroutines are managed by Python's event loop, are extremely lightweight,
# and share memory safely because only one coroutine runs at a time.
#
# **KEY INSIGHT:** `async def` alone does nothing special. You MUST `await` the
# coroutine to actually execute it. Calling `my_async_fn()` without `await`
# just creates a coroutine object — it never runs.

import asyncio  # Python's built-in library for async programming

print("==========================================")
print("1. NORMAL (SYNC) vs ASYNC FUNCTION")
print("==========================================")

# Normal function: blocks everything until it finishes
def normal_greet(name):
    return f"Hello, {name}!"

print(normal_greet("Ritesh"))

# Async function: declared with `async def`
async def async_greet(name):
    return f"Hello (async), {name}!"

# To RUN an async function, you have two approaches:
# Approach A: asyncio.run() - Used to start the event loop from synchronous code.
# Approach B (Best Practice): await - Used inside other async functions to run them.

# --- Approach A (Simple/Single run) ---
# Useful for quick one-off calls, but starts/stops the event loop each time (inefficient)
result = asyncio.run(async_greet("Ritesh"))

print(result)



# --- Approach B (Best Practice: Single Entry Point) ---
# In real applications, you start the loop ONCE using asyncio.run() at the entry point,
# and use `await` everywhere else. This is faster and lets you share database connections.
async def main():
    # 'await' pauses this function until async_greet completes, letting other tasks run
    result_with_await = await async_greet("Ritesh")
    print(f"{result_with_await} (called with await)")

# Start the event loop once for the whole program
asyncio.run(main())

print()

# ==========================================
print("2. AWAIT — Wait for a slow task without blocking")
print("==========================================")

# `asyncio.sleep(seconds)` simulates a slow task (like waiting for a database)
# In real code, this would be: await database.fetch_user(id)

async def fetch_user(user_id: int):
    print(f"Fetching user {user_id} from database...")
    await asyncio.sleep(1)  # Simulate 1 second database delay
    print(f"Got user {user_id}!")
    return {"id": user_id, "name": "Ritesh"}

user = asyncio.run(fetch_user(1))
print("User data:", user)

print()

# ==========================================
print("3. RUNNING MULTIPLE TASKS AT THE SAME TIME")
print("==========================================")

# This is the POWER of async — run multiple slow tasks together instead of one by one!

async def fetch_data(source, delay):
    print(f"  Starting to fetch from {source}...")
    await asyncio.sleep(delay)  # Simulate delay
    print(f"  Done fetching from {source}!")
    return f"Data from {source}"

async def main():
    # asyncio.gather() runs multiple async functions AT THE SAME TIME
    results = await asyncio.gather(
        fetch_data("Database", 2),
        fetch_data("External API", 1),
        fetch_data("Cache", 0.5),
    )
    print("\nAll results:", results)

# This will finish in ~2 seconds instead of 3.5 seconds (2+1+0.5) combined!
print("Running all fetches simultaneously:")
asyncio.run(main())

print()

# ==========================================
print("4. FASTAPI USE CASE — Async Route")
print("==========================================")

# In FastAPI, you write your routes as `async def` so the server can 
# handle thousands of users at once without slowing down.

# Real FastAPI async route looks like this:
#
#   @app.get("/users/{user_id}")
#   async def get_user(user_id: int):
#       user = await database.fetch_one(user_id)  # Waits for DB without blocking
#       return user

# Here is the pattern you will write daily in FastAPI:
async def get_user_from_db(user_id: int):
    await asyncio.sleep(0.1)  # Simulating database call
    return {"id": user_id, "name": "Ritesh", "email": "ritesh@example.com"}

async def fastapi_style_route(user_id: int):
    user = await get_user_from_db(user_id)  # Non-blocking database call
    return user

print("FastAPI-style async route result:")
print(asyncio.run(fastapi_style_route(1)))

# ==========================================
# REAL-LIFE USE CASES
# ==========================================
#
# 1. Concurrent Web Scraping: Fetching 50 web pages in parallel without
#    blocking the main CPU thread.
#
# 2. WebSocket Notifications Server: Handling thousands of concurrent chat
#    connections efficiently.
#
# 3. Asynchronous Database Queries: Querying databases and calling external
#    APIs concurrently to reduce load times.

# ==========================================
# MNC INTERVIEW QUESTIONS & ANSWERS
# ==========================================
#
# Q1. What is the role of the Event Loop in Python asynchronous programming?
# A:  The event loop is the engine that drives async apps. It schedules and
#     manages the execution of coroutines, tracking which tasks are waiting
#     for I/O (like file reading or network requests) and running other code
#     in the meantime, utilizing single-core concurrency.
#
# Q2. What happens if you run blocking code (like time.sleep() or a heavy math
#     loop) inside a coroutine?
# A:  It blocks the entire event loop. Because Python async code runs on a
#     single thread, blocking the event loop stops all other concurrent
#     coroutines from executing. You must use async equivalents (like
#     asyncio.sleep()) or delegate blocking code to a thread pool.
#
# Q3. What is the difference between awaiting tasks sequentially vs using
#     asyncio.gather()?
# A:  Awaiting tasks sequentially blocks execution at each line, executing the
#     next task only after the current one completes. This wastes potential
#     concurrency. `asyncio.gather()` starts all tasks concurrently in the
#     event loop, allowing them to run in parallel during I/O wait times.
#     Sequential execution is best when tasks depend on the outputs of
#     previous ones, while `asyncio.gather()` is best for independent parallel
#     I/O requests (like scraping multiple pages or fetching database records
#     concurrently). See the comparison table below:
#     
#     | Execution Style | Execution Flow | Time Taken |
#     | :--- | :--- | :--- |
#     | **Sequential** | One by one (blocking) | Sum of all tasks (`t1 + t2`) |
#     | **asyncio.gather**| Concurrent execution | Duration of the longest task |