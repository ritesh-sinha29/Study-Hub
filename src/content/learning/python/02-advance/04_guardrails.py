# ========================================================================================
# GUARDRAILS & VALIDATION (ADVANCED)
# ========================================================================================
#
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# SECTION 1 — GUARDRAILS IN PYTHON APPLICATIONS
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#
# Guardrails in application code ensure that data entering or leaving a component conforms
# to expected types, structures, and business constraints before processing.
# In Python, guardrails are cleanest when decoupled from core logic. They can be cleanly
# implemented at function/method boundaries using decorators.
#
# 1. INPUT GUARDRAILS: Intercept arguments before function execution to sanitize or reject them.
# 2. OUTPUT GUARDRAILS: Validate return values after execution to guarantee safety, format compliance,
#    and prevent private data leakage.
#
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# SECTION 2 — DETAILED DECORATOR-BASED GUARDRAIL FLOW
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#
#    Arguments ────────► [ @validate_input ] ───(Invalid)───► [ ValueError / Exception ]
#                             │
#                          (Valid)
#                             ▼
#                    [ Core Function ]
#                             │
#                             ▼
#    Final Output ◄───── [ @validate_output ] ◄──(Invalid)─── [ Blocked / Sanitized ]
#
# ========================================================================================

import functools
import re
import inspect
from typing import Callable, Any, Dict, List

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 1. INPUT GUARDRAIL DECORATOR
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# We implement a decorator that accepts validation rules and applies them
# to function inputs before execution.

def validate_input(rules: Dict[str, Callable[[Any], bool]]):
    """
    Decorator that checks function arguments against a dictionary of rule functions.
    If a rule returns False, it raises a ValueError.
    """
    def decorator(func: Callable):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # Use inspect.signature which correctly follows __wrapped__ chain
            sig = inspect.signature(func)
            bound = sig.bind(*args, **kwargs)
            bound.apply_defaults()
            bound_args = bound.arguments
            
            # Validate parameters based on rules
            for param_name, rule in rules.items():
                if param_name in bound_args:
                    val = bound_args[param_name]
                    if not rule(val):
                        raise ValueError(
                            f"[Guardrail] Input validation failed for parameter '{param_name}' with value: {val}"
                        )
            
            return func(*args, **kwargs)
        return wrapper
    return decorator

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 2. OUTPUT GUARDRAIL DECORATOR
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# We implement a decorator that inspects and sanitizes return values.

def sanitize_output(sensitive_pattern: str, replacement: str = "[REDEMPTED]"):
    """
    Decorator that inspects string returns or dictionary values.
    It replaces patterns matching sensitive_pattern with replacement.
    """
    regex = re.compile(sensitive_pattern, re.IGNORECASE)
    
    def decorator(func: Callable):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            
            # Helper to recursively sanitize strings inside nested collections
            def clean(val: Any) -> Any:
                if isinstance(val, str):
                    return regex.sub(replacement, val)
                elif isinstance(val, dict):
                    return {k: clean(v) for k, v in val.items()}
                elif isinstance(val, list):
                    return [clean(v) for v in val]
                return val
            
            return clean(result)
        return wrapper
    return decorator

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# DEMONSTRATION & TEST CASES
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

# Define validation rules
rules = {
    "age": lambda x: isinstance(x, int) and 18 <= x <= 120,
    "email": lambda x: isinstance(x, str) and "@" in x,
    "amount": lambda x: isinstance(x, (int, float)) and x > 0
}

# Apply guardrail decorators to user registration function
@validate_input(rules)
@sanitize_output(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b", replacement="[EMAIL_MASKED]")
def register_user(username: str, age: int, email: str, amount: float) -> dict:
    """
    Registers a new user and returns their initial state.
    """
    print(f"  [Executing] register_user for {username}..")
    return {
        "status": "success",
        "username": username,
        "email": email,
        "balance": amount
    }

if __name__ == "__main__":
    print("\n" + "="*70)
    print("TESTING DECORATOR-BASED PYTHON GUARDRAILS")
    print("="*70)
    
    # Test case 1: Valid registration
    print("\n--- Test 1: Valid User Registration ---")
    try:
        user_info = register_user("Ritesh", 25, "ritesh@example.com", 150.0)
        print("  Returned Output:", user_info)
    except ValueError as e:
        print("  Error:", e)

    # Test case 2: Invalid input (Age violates guardrail)
    print("\n--- Test 2: Invalid Input (Underage) ---")
    try:
        register_user("Amit", 16, "amit@example.com", 50.0)
    except ValueError as e:
        print("  Error caught:", e)

    # Test case 3: Invalid input (Negative balance amount)
    print("\n--- Test 3: Invalid Input (Negative Amount) ---")
    try:
        register_user("Siddharth", 30, "sid@example.com", -10.0)
    except ValueError as e:
        print("  Error caught:", e)

# ========================================================================================
# REAL-LIFE USE CASES
# ========================================================================================
#
# 1. API PAYLOAD SANITIZATION:
#    - **Input**: Incoming raw request payload containing query parameters (e.g. limit).
#    - **Step 1**: `@validate_input` interceptor verifies parameter bounds and types.
#    - **Step 2**: Rejects request immediately if parameters violate bounds (e.g. limit > 100).
#    - **Result**: Protects internal DB handlers from overload or memory exhaustion.
#
# 2. PRIVACY-ENFORCING INTERCEPTOR:
#    - **Input**: Database query response containing potential sensitive PII or credentials.
#    - **Step 1**: `@sanitize_output` scans dictionary structures recursively.
#    - **Step 2**: Obfuscates sensitive patterns like emails or card hashes.
#    - **Result**: Enforces strict GDPR compliance before exposing payload responses.
#
# ========================================================================================
# MNC INTERVIEW QUESTIONS & ANSWERS
# ========================================================================================
#
# Q1. Why implement guardrails using decorators instead of inline validation logic?
# A:  Using decorators decouples cross-cutting concerns (like input checking and sanitization)
#     from the core business logic. This adheres to the Single Responsibility Principle,
#     simplifies unit testing, and makes validation rules reusable across multiple endpoints.
#
# Q2. How do you preserve function metadata (docstring, function name) when using decorators?
# A:  You must use `functools.wraps(func)` to decorate the inner wrapper function. Without it,
#     the decorated function loses its original identity, and attributes like `__name__` and
#     `__doc__` will reference the inner wrapper instead, causing problems with introspection tools.
#
# Q3. Can decorators be used to validate keyword-only or variable positional arguments (*args)?
# A:  Yes. To make the validation decorator fully robust, you can use Python's built-in
#     `inspect.signature(func)` to bind the incoming `*args` and `**kwargs` to their actual parameter 
#     names dynamically, allowing precise rule verification for all signature formats.
