# ==========================================
# PYTHON EXCEPTION HANDLING (FOR BEGINNERS)
# ==========================================

# --- WHAT IS EXCEPTION HANDLING? ---
# An exception is an ERROR that happens while the program is running.
# Without handling it, your entire program CRASHES.
# With try/except, you can CATCH the error and handle it gracefully.

# --- SIMPLE ANALOGY ---
# It's like a safety net under a trapeze artist.
# If they fall (error happens), the net catches them (except block runs),
# and the show can continue instead of everything stopping.

# --- REAL-WORLD USE CASES ---
# * FastAPI: Return a proper error message (400, 404, 500) instead of crashing
# * LangGraph: If an AI agent fails, catch the error and retry or go to fallback
# * File reading: If a file doesn't exist, show a nice message instead of crashing

print("==========================================")
print("1. WHAT HAPPENS WITHOUT EXCEPTION HANDLING")
print("==========================================")

# This would CRASH the program if uncommented:
# print(10 / 0)  # ZeroDivisionError: division by zero
# print(int("hello"))  # ValueError: invalid literal for int()

print("(Examples commented out to avoid crashing the script)")
print()

# ==========================================
print("2. BASIC TRY / EXCEPT")
print("==========================================")

# try:   → Run this code (the risky part)
# except → If an error happens, run THIS instead (the safe part)

try:
    divisor = int("0")    # int("0") → Pylance can't predict this is 0, so no warning
    result = 10 / divisor # This still causes ZeroDivisionError at runtime
    print("Result:", result)
except ZeroDivisionError:
    # This runs only if a ZeroDivisionError happens
    print("Error caught: You cannot divide by zero!")

print("Program continues normally after the error.")
print()

# ==========================================
print("3. CATCHING DIFFERENT ERRORS")
print("==========================================")

def safe_convert(value):
    try:
        number = int(value)   # Try converting to integer
        result = 100 / number # Try dividing
        return result
    except ValueError:
        return "Error: That is not a valid number!"
    except ZeroDivisionError:
        return "Error: Cannot divide by zero!"

print(safe_convert("10"))     # Works fine → 10.0
print(safe_convert("hello"))  # ValueError → custom message
print(safe_convert("0"))      # ZeroDivisionError → custom message

print()

# ==========================================
print("4. ELSE — Runs only if NO error happened")
print("==========================================")

try:
    number = int("42")
except ValueError:
    print("Not a valid number!")
else:
    # This block ONLY runs if there was NO exception
    print("Conversion successful! Number is:", number)

print()

# ==========================================
print("5. FINALLY — Runs NO MATTER WHAT (error or not)")
print("==========================================")

# Use `finally` for cleanup code (like closing a file or database connection)

try:
    file_content = open("somefile.txt", "r")
except FileNotFoundError:
    print("File not found!")
finally:
    # This ALWAYS runs — even if an error happened
    print("Cleanup done. Moving on.")

print()

# ==========================================
print("6. RAISING YOUR OWN ERRORS")
print("==========================================")

# You can create and throw your own errors using `raise`

def check_age(age: int):
    if age < 0:
        raise ValueError("Age cannot be negative!")
    if age > 150:
        raise ValueError("Age seems too high!")
    return f"Valid age: {age}"

try:
    print(check_age(25))
    print(check_age(-5))  # This will raise an error
except ValueError as e:
    print("Caught an error:", e)

print()

# ==========================================
print("7. FASTAPI USE CASE — HTTPException")
print("==========================================")

# In FastAPI, you raise an HTTPException to send error responses to the user.
# Real FastAPI code:
#
#   from fastapi import HTTPException
#
#   @app.get("/users/{user_id}")
#   def get_user(user_id: int):
#       user = find_user(user_id)
#       if user is None:
#           raise HTTPException(status_code=404, detail="User not found")
#       return user

# Simulation without FastAPI:
def simulate_http_exception(status_code, detail):
    raise Exception(f"HTTP {status_code}: {detail}")

def get_user(user_id: int):
    users = {1: "Ritesh", 2: "Rox"}
    try:
        if user_id not in users:
            simulate_http_exception(404, "User not found")
        return {"id": user_id, "name": users[user_id]}
    except Exception as e:
        return {"error": str(e)}

print(get_user(1))   # Found → returns user data
print(get_user(99))  # Not found → returns error response

# ==========================================
# REAL-LIFE USE CASES
# ==========================================
#
# 1. API Network Failover: Catching ConnectionError and retrying the request
#    or serving cached data.
#
# 2. File Parsing Resilience: Catching FileNotFoundError or PermissionError
#    during import tasks.
#
# 3. Database Transaction Cleanup: Guaranteeing database connection closure
#    using a finally block.

# ==========================================
# MNC INTERVIEW QUESTIONS & ANSWERS
# ==========================================
#
# Q1. What is the difference between the else block and the finally block in
#     exception handling?
# A:  See the comparison table below:
#     | Block | When it Executes | Primary Use Case |
#     | :--- | :--- | :--- |
#     | `else` | ONLY if no exceptions were raised | Logic that depends on try success |
#     | `finally` | ALWAYS (even after errors/returns)| Resource cleanup (closing) |
#
# Q2. Why is catching bare exceptions (like `except:`) or `except Exception:`
#     discouraged for control flow?
# A:  It hides unexpected programming errors (like NameError, TypeError, or
#     SyntaxError) and intercepts system signals like keyboard interrupts
#     (Ctrl+C). Always catch the most specific exceptions you expect to occur.
#
# Q3. What is exception propagation in Python?
# A:  If an exception is raised inside a function and is not caught there, it
#     propagates (bubbles up) to the calling function. This continues up the
#     call stack. If it reaches the module level without being caught, Python
#     prints the traceback and exits.