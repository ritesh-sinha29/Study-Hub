# ==========================================================
# PYTHON CONTEXT MANAGERS & THE 'WITH' STATEMENT (DEEPER PYTHON)
# ==========================================================

# ---
#
# **WHAT IS A CONTEXT MANAGER?** ---
# A context manager is a tool that allows you to allocate and release resources
# exactly when you want to.
#
# The most common use case is the `with` statement.
# You have probably seen it when opening files:
#
#   with open("test.txt", "w") as file:
#       file.write("Hello")
#
# Why use `with`? Because it **AUTOMATICALLY** closes the file for you,
# even if an error/crash occurs inside the block! This prevents resource leaks.
#
# **HOW IT WORKS INTERNALLY:**
#   1. Python calls `obj.__enter__()` — returns the resource (assigned via `as`).
#   2. Your code block runs.
#   3. Python calls `obj.__exit__(exc_type, exc_val, exc_tb)` unconditionally,
#      even if an exception occurred. The three arguments describe the exception.
#   4. If `__exit__` returns True, the exception is **SUPPRESSED**. If False/None,
#      the exception propagates up the call stack.
#
# **KEY INSIGHT:** `@contextmanager` from `contextlib` lets you write a context
# manager as a generator function. Code before `yield` is the setup
# (__enter__) and code after `yield` (in a `finally` block) is the cleanup
# (__exit__). Use this for simple, one-off context managers without a class.

import time
from contextlib import contextmanager

# ==========================================================
# 1. THE CLASS-BASED APPROACH (Using __enter__ and __exit__)
# ==========================================================
# To make a class act as a context manager, it must implement two dunder methods:
# - __enter__: What to do when entering the `with` block (setup).
# - __exit__: What to do when exiting the `with` block (cleanup).

class Timer:
    def __init__(self, description: str):
        self.description = description

    def __enter__(self):
        print(f"[Timer] Starting timer for: {self.description}")
        self.start_time = time.time()
        return self  # This is what gets assigned to the 'as' variable

    def __exit__(self, exc_type, exc_val, exc_tb):
        # exc_type, exc_val, exc_tb contain info if an error occurred inside the block.
        # If no error occurred, they are all None.
        self.end_time = time.time()
        duration = self.end_time - self.start_time
        print(f"[Timer] Finished: {self.description} took {duration:.4f} seconds")
        print("-" * 40)
        
        # Returning False (or None) allows any exception inside the block to propagate.
        # Returning True suppresses the exception.
        return False


print("--- 1. CLASS-BASED CONTEXT MANAGER ---")
# Using our custom Timer context manager
with Timer("Calculating sum of numbers"):
    total = 0
    for i in range(1, 10_000_000):
        total += i
    print(f"Calculation complete. Sum = {total}")


# ==========================================================
# 2. HANDLING ERRORS IN __exit__
# ==========================================================
# A key power of context managers is that the cleanup (__exit__) is guaranteed
# to run, even if the code inside crashes!

class DatabaseConnection:
    def __init__(self, db_name: str):
        self.db_name = db_name

    def __enter__(self):
        print(f"[DB] Opening connection to '{self.db_name}'...")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        print(f"[DB] Closing connection to '{self.db_name}'... (Cleanup successful)")
        if exc_type is not None:
            print(f"[DB] Caught an error inside the block: {exc_val}")
            # We return True to say: "We handled this error, don't crash the program!"
            return True
        return False


print("\n--- 2. ERROR HANDLING IN CONTEXT MANAGERS ---")
with DatabaseConnection("UserDB") as db:
    print("[DB] Performing query...")
    # Let's simulate a crash inside the block:
    raise ValueError("Oops! Database query failed due to invalid query syntax.")

print("Program continues running normally because __exit__ suppressed the error! [OK]")
print("-" * 40)


# ==========================================================
# 3. THE GENERATOR-BASED APPROACH (Using @contextmanager)
# ==========================================================
# Writing a class can be wordy. Python provides a helper decorator: `@contextmanager`
# inside the `contextlib` module. It uses a `yield` statement.

@contextmanager
def simple_file_manager(filename: str, mode: str):
    print(f"[File] Opening {filename}...")
    file_object = open(filename, mode)
    try:
        # Everything BEFORE 'yield' is the setup (__enter__)
        yield file_object
    finally:
        # Everything AFTER 'yield' (and in 'finally') is the cleanup (__exit__)
        print(f"[File] Closing {filename}...")
        file_object.close()


print("\n--- 3. GENERATOR-BASED CONTEXT MANAGER ---")
# Let's use it to write a temp file
with simple_file_manager("temp_file.txt", "w") as f:
    f.write("Writing some temporary data.")
    print("[File] Data written successfully.")

# Clean up: delete the file
import os
if os.path.exists("temp_file.txt"):
    os.remove("temp_file.txt")
    print("[File] Temp file removed from disk.")

# ==========================================
# REAL-LIFE USE CASES
# ==========================================
#
# 1. DB Connection Lifecycles: Guaranteeing a connection is returned to the
#    pool once a query finishes.
#
# 2. Thread Synchronization locks: Acquiring and automatically releasing locks
#    to prevent thread conflicts.
#
# 3. Temporary Files cleanup: Creating temporary scratch files and
#    automatically deleting them on block completion.

# ==========================================
# MNC INTERVIEW QUESTIONS & ANSWERS
# ==========================================
#
# Q1. What dunder methods must a class implement to become a context manager?
# A:  A class must implement: 1) `__enter__(self)`: runs when entering the
#     'with' block, returning the resource. 2) `__exit__(self, exc_type,
#     exc_val, exc_tb)`: runs when exiting the block. It receives exception
#     details (if any) and returns True to suppress them, or False to
#     propagate them.
#
# Q2. How does the contextlib.contextmanager decorator work?
# A:  @contextmanager allows writing a context manager using a generator
#     function instead of a class. The code before the 'yield' statement acts
#     as __enter__, the yielded value is returned as the block resource, and
#     code after 'yield' acts as __exit__ (wrapped in try-finally).
#
# Q3. What happens if an exception is raised inside a context manager?
# A:  The exception is passed to the __exit__ method's parameters. If __exit__
#     returns True, the exception is swallowed and execution continues. If it
#     returns False (or None), the exception is propagated up the stack to be
#     handled elsewhere.