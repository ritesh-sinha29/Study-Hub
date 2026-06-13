# Context Managers

```python
# ==========================================================
# PYTHON CONTEXT MANAGERS & THE 'WITH' STATEMENT (DEEPER PYTHON)
# ==========================================================

# --- WHAT IS A CONTEXT MANAGER? ---
# A context manager is a tool that allows you to allocate and release resources
# exactly when you want to.
#
# The most common use case is the `with` statement.
# You have probably seen it when opening files:
#
#   with open("test.txt", "w") as file:
#       file.write("Hello")
#
# Why use `with`? Because it AUTOMATICALLY closes the file for you, 
# even if an error/crash occurs inside the block! This prevents resource leaks.

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
```
