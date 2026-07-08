# ==========================================
# PYTHON IF / ELIF / ELSE (FOR BEGINNERS)
# ==========================================

# --- WHY LEARN THIS? ---
# Use if/else when your program needs to make a DECISION based on a condition.
# Examples:
#   * Login System: If password is correct -> allow access, else -> deny.
#   * FastAPI: If request data is valid -> process it, else -> return an error.
#   * LangGraph: If agent output meets condition -> go to next node, else -> retry.

# --- HOW IT WORKS ---
# Python checks if a condition is True or False.
# If True  -> runs the `if` block
# If False -> checks `elif`, or falls to `else`
#
# **HOW PYTHON EVALUATES CONDITIONS:** Python doesn't just check for True/False
# literals. It checks for TRUTHINESS. The following values are all "falsy":
# 0, 0.0, "", [], {}, set(), None, False.
# Everything else is "truthy". This means `if my_list:` is a clean way to
# check if a list is non-empty without writing `if len(my_list) > 0:`.
#
# SHORT-CIRCUIT EVALUATION: In `if A and B`, if A is False, Python never
# evaluates B (pointless). In `if A or B`, if A is True, Python skips B.
# This saves time and lets you write guards like: `if user and user.is_active:`
#
# **KEY INSIGHT:** `elif` is NOT a separate if. Python stops at the **FIRST** branch
# that is True and skips all remaining elif/else blocks. Order matters!


print("==========================================")
print("BASIC IF / ELSE")
print("==========================================")

age = 18

if age >= 18:
    # This block runs if the condition (age >= 18) is True
    print("You are an adult. You can vote!")
else:
    # This block runs if the condition is False
    print("You are a minor. You cannot vote yet.")

print()

# ==========================================
# ELIF (ELSE IF) — MULTIPLE CONDITIONS
# ==========================================
# Use `elif` when you have MORE than 2 possible outcomes.

print("==========================================")
print("IF / ELIF / ELSE")
print("==========================================")

marks = 75

if marks >= 90:
    print("Grade: A+ (Excellent!)")
elif marks >= 75:
    # This checks if the first condition was False, then tries this one
    print("Grade: B (Good!)")
elif marks >= 60:
    print("Grade: C (Average)")
else:
    # This runs only if ALL above conditions are False
    print("Grade: F (Failed)")

print()

# ==========================================
# COMPARISON OPERATORS (used in conditions)
# ==========================================
# >   Greater than         e.g., 5 > 3  → True
# <   Less than            e.g., 3 < 5  → True
# >=  Greater or equal     e.g., 5 >= 5 → True
# <=  Less or equal        e.g., 3 <= 5 → True
# ==  Equal to             e.g., 5 == 5 → True  (Note: == not =)
# !=  Not equal to         e.g., 5 != 3 → True

print("==========================================")
print("COMPARISON OPERATORS")
print("==========================================")

x = 10
y = 20
print("x =", x, "| y =", y)
print("x > y  :", x > y)
print("x < y  :", x < y)
print("x == y :", x == y)
print("x != y :", x != y)
print()

# ==========================================
# LOGICAL OPERATORS — AND / OR / NOT
# ==========================================
# `and` → Both conditions must be True
# `or`  → At least ONE condition must be True
# `not` → Reverses the result (True becomes False)

print("==========================================")
print("LOGICAL OPERATORS: and / or / not")
print("==========================================")

username = "ritesh"
password = "1234"

# Both must match for login to succeed
if username == "ritesh" and password == "1234":
    print("Login successful! Welcome,", username)
else:
    print("Login failed! Wrong username or password.")

print()

# Using `or`
is_weekend = False
is_holiday = True

if is_weekend or is_holiday:
    print("You can relax today!")
else:
    print("It's a working day. Back to coding!")

print()

# Using `not`
is_logged_in = False
if not is_logged_in:
    print("Please log in first.")

print()

# ==========================================
# FASTAPI USE CASE EXAMPLE
# ==========================================
# In FastAPI, you check conditions to validate incoming request data.

print("==========================================")
print("FASTAPI-STYLE USE CASE: Validate a Request")
print("==========================================")

def validate_age(age):
    # This simulates what FastAPI does when it receives data from a user
    if not isinstance(age, int):
        return "Error 422: Age must be a number."
    elif age < 0:
        return "Error 400: Age cannot be negative."
    elif age > 120:
        return "Error 400: Age seems invalid."
    else:
        return f"Success! Age {age} is valid."

print(validate_age(25))
print(validate_age(-5))
print(validate_age(200))
print(validate_age("abc"))

# ==========================================
# REAL-LIFE USE CASES
# ==========================================
# 1. Access Authorization: Verifying user roles and permissions before
#    - **Step 1**: Displaying dashboard data.
#
# 2. Dynamic Pricing Engines: Calculating discounts or surcharges based on
#    - **Step 1**: Purchase volume or user type.
#
# 3. Form Field Validation: Checking if user password matches requirements
#    - **Step 1**: Before registration.

# ==========================================
# MNC INTERVIEW QUESTIONS & ANSWERS
# ==========================================
#
# Q1. What is 'short-circuit evaluation' in Python logical operations?
# A:  In logical operations ('and', 'or'), Python evaluates expressions
#     left-to-right and stops as soon as the outcome is determined. For 'or',
#     if the first expression is True, the second is not evaluated. For 'and',
#     if the first is False, the second is skipped.
#
# Q2. What are Truthy and Falsy values in Python?
# A:  Every object in Python has an implicit boolean value. Falsy values
#     include None, False, numeric zero (0, 0.0), empty collections ([], {},
#     (), set()), and empty strings (''). All other objects are Truthy by
#     default.
#
# Q3. What is the ternary operator in Python and what is its syntax?
# A:  The ternary operator is a one-line conditional expression. Syntax:
#     'value_if_true if condition else value_if_false'. Example: 'status =
#     "Adult" if age >= 18 else "Minor"'. It is useful for clean inline
#     assignments.