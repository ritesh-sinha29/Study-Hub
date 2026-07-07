# ==========================================
# PYTHON DECORATORS (FOR BEGINNERS)
# ==========================================

# ---
#
# **WHAT IS A DECORATOR?** ---
# A decorator is a special function that WRAPS another function 
# and adds extra behavior WITHOUT changing the original function's code.
# You apply a decorator using the `@` symbol on top of a function.

# --- WHY LEARN THIS? ---
# * FastAPI: @app.get("/users") tells FastAPI "this function handles GET /users"
# * Logging: Automatically log every time a function is called
# * Timing: Measure how long a function takes to run
# * Authentication: Check if a user is logged in before running a function
#
# **HOW IT WORKS INTERNALLY:** Python functions are first-class objects — you can
# store them in variables, pass them as arguments, and return them from other
# functions. A decorator is simply a function that receives another function,
# wraps it in an inner "wrapper" function, and returns the wrapper.
# The `@my_decorator` syntax is just shorthand for: `func = my_decorator(func)`
#
# CLOSURES: The wrapper function "closes over" the original `func` variable,
# keeping it alive in memory even after the outer decorator function returns.
# This is how the wrapper can still call `func(...)` later.
#
# **KEY INSIGHT:** Always use `@functools.wraps(func)` inside your wrapper.
# Without it, the decorated function loses its `__name__` and `__doc__`,
# which breaks debugging tools and API documentation generators.

print("==========================================")
print("1. THE PROBLEM DECORATORS SOLVE")
print("==========================================")

# Say we have two functions and we want to add a greeting before each:

def say_hello():
    print("Hello!")

def say_bye():
    print("Bye!")

# If we want to add "--- Starting ---" before both,
# instead of editing each function, we use a decorator!

print()

# ==========================================
print("2. CREATING A BASIC DECORATOR")
print("==========================================")

# Step 1: Create the decorator function
def my_decorator(func):
    # `func` is the function being decorated (wrapped)
    def wrapper():
        print("--- Before the function runs ---")
        func()   # Call the original function
        print("--- After the function runs ---")
    return wrapper

# Step 2: Apply the decorator using @
@my_decorator
def greet():
    print("Hello, Ritesh!")

# Now when you call greet(), it ALSO runs the code in wrapper()
greet()

print()

# ==========================================
print("3. DECORATOR WITH PARAMETERS")
print("==========================================")

def log_decorator(func):
    def wrapper(*args, **kwargs):
        print(f"[LOG] Calling function: {func.__name__}")
        result = func(*args, **kwargs)  # Run the original function
        print(f"[LOG] Function {func.__name__} finished.")
        return result
    return wrapper

@log_decorator
def add(a, b):
    return a + b

@log_decorator
def greet_user(name):
    print(f"Hello, {name}!")

result = add(5, 10)
print("Result:", result)
print()
greet_user("Ritesh")

print()

# ==========================================
print("4. FASTAPI USE CASE — Route Decorators")
print("==========================================")

# In FastAPI, decorators tell the framework which URL triggers which function.
# This is the MOST important use of decorators you will see daily.

# Real FastAPI code looks like this:
# 
#   from fastapi import FastAPI
#   app = FastAPI()
#
#   @app.get("/")              <-- This is a decorator!
#   def read_home():
#       return {"message": "Welcome to my API"}
#
#   @app.get("/users")         <-- This is another decorator!
#   def get_all_users():
#       return [{"id": 1, "name": "Ritesh"}]
#
#   @app.post("/users")        <-- Decorator for POST requests
#   def create_user(user: UserModel):
#       return user

# Here is a SIMULATION without FastAPI installed:

# Fake "app" to demonstrate how @app.get() works
routes = {}

def get(path):
    # This simulates @app.get(path)
    def decorator(func):
        routes[path] = func  # Register the function under the URL path
        return func
    return decorator

@get("/")
def home():
    return {"message": "Welcome!"}

@get("/users")
def get_users():
    return [{"id": 1, "name": "Ritesh"}, {"id": 2, "name": "Rox"}]

# Simulate what FastAPI does when it receives a request for "/"
print("GET / ->", home())
print("GET /users ->", get_users())
print("\nAll registered routes:", list(routes.keys()))

# ==========================================
# REAL-LIFE USE CASES
# ==========================================
#
# 1. Authentication Middleware: Restricting endpoint execution to
#    authenticated users using @require_auth.
#
# 2. Function Execution Timer: Logging performance metrics and load times for
#    DB operations.
#
# 3. API Rate Limiter: Tracking user requests and restricting them if they
#    exceed limits.

# ==========================================
# MNC INTERVIEW QUESTIONS & ANSWERS
# ==========================================
#
# Q1. What is a closure in Python, and how is it related to decorators?
# A:  A closure is a nested function that retains access to variables from its
#     enclosing outer function's scope even after the outer function has
#     finished executing. Decorators rely on closures to store reference to
#     the original function they wrap.
#
# Q2. Why should you use functools.wraps when writing a custom decorator?
# A:  Decorators replace the original function with a wrapper function. This
#     replaces its metadata (like name and docstrings) with the wrapper's.
#     @wraps copies the original function's name, docstring, and annotations
#     back onto the wrapper, preserving introspection.
#
# Q3. How do you pass custom arguments to a decorator itself (e.g.
#     @repeat(num=3))?
# A:  To pass arguments, you must write a decorator factory (a 3-level nested
#     function structure). The top level accepts the decorator arguments, the
#     middle level accepts the function to be decorated, and the bottom level
#     (wrapper) handles execution.