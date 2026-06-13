# Decorators Deep Dive

## ADVANCED PYTHON DECORATORS (DEEPER PYTHON)

## QUICK DECORATOR RECAP

In Python, functions are FIRST-CLASS objects. This means:
1. You can pass functions as arguments to other functions.
2. You can return functions from other functions.
A decorator is simply a function that takes another function, 
adds some behavior to it, and returns the modified function.

```python
from functools import wraps
```

## 1. WHY WE NEED 'functools.wraps'

When we decorate a function, we replace it with our wrapper function.
This loses the original function's name and documentation.
`functools.wraps` is a built-in decorator that copies this metadata back!

```python
def simple_logger(func):
    @wraps(func)  # Keeps the name and docstring of 'func' intact
    def wrapper(*args, **kwargs):
        print(f"[Log] Calling: {func.__name__}")
        return func(*args, **kwargs)
    return wrapper

@simple_logger
def add_numbers(a: int, b: int) -> int:
    """Adds two integers together."""
    return a + b


print("--- 1. PRESERVING METADATA WITH WRAPS ---")
print("Result of add:", add_numbers(5, 7))
print("Function Name:", add_numbers.__name__)  # Without wraps, this would print "wrapper"
print("Function Docstring:", add_numbers.__doc__)  # Without wraps, this would print None
print("-" * 40)
```

## 2. DECORATORS WITH ARGUMENTS

In FastAPI, you write routes like this:

```python
@app.get("/items")
```

Here, the decorator itself takes arguments!
To do this, we need THREE levels of functions:
1. Outer function: receives the decorator arguments.
2. Middle function: receives the function to be decorated.
3. Inner function: receives the arguments of the function being decorated.

```python
def repeat(num_times: int):
    # Outer level takes decorator arguments
    def decorator_repeat(func):
        # Middle level takes the target function
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Inner level does the actual work
            for _ in range(num_times):
                result = func(*args, **kwargs)
            return result
        return wrapper
    return decorator_repeat


print("\n--- 2. DECORATORS WITH ARGUMENTS ---")

@repeat(num_times=3)
def greet(name: str):
    print(f"Hello, {name}!")

greet("Alice")
print("-" * 40)
```

## 3. STACKING DECORATORS

You can apply multiple decorators to a single function.
Python executes them from bottom to top (inside out).

```python
def bold(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        return f"<b>{func(*args, **kwargs)}</b>"
    return wrapper

def italic(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        return f"<i>{func(*args, **kwargs)}</i>"
    return wrapper


print("\n--- 3. STACKING DECORATORS ---")

@bold
@italic
def format_text(text: str) -> str:
    return text
```

Order of execution:
1. italic(format_text) -> wraps it in <i>...</i>
2. bold(italic_wrapper) -> wraps the result in <b>...</b>

```python
print("Formatted Text:", format_text("Python is awesome"))
print("-" * 40)
```

## 4. CLASS-BASED DECORATORS

Instead of nested functions, we can use a class to write a decorator.
This relies on the `__call__` dunder method we learned earlier!

```python
class CountCalls:
    def __init__(self, func):
        self.func = func
        self.num_calls = 0
        wraps(func)(self)  # Keep original metadata

    def __call__(self, *args, **kwargs):
        self.num_calls += 1
        print(f"[Tracker] {self.func.__name__} has been called {self.num_calls} times.")
        return self.func(*args, **kwargs)


print("\n--- 4. CLASS-BASED DECORATORS ---")

@CountCalls
def say_hi():
    print("Hi!")

say_hi()
say_hi()
say_hi()
```

