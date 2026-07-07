# ==========================================
# PYTHON USER INPUT (FOR BEGINNERS)
# ==========================================

# --- REAL-WORLD USE CASES ---
# Use the `input()` function when you need your program to interact with a human 
# and collect information from them.
# Examples:
#   * User Login: Asking for a username and password.
#   * Command Line Calculators: Asking the user to input two numbers to add.
#   * Interactive Games: Asking "Do you want to play again? (yes/no)".

# In Python, the `input()` function lets the program wait and ask the user to type something.
# IMPORTANT: Whatever the user types is ALWAYS treated as a String (text) by default.
#
# HOW IT WORKS: `input()` pauses the program, waits for the user to type something
# and press Enter, then hands the typed text back to your code as a str.
# KEY INSIGHT: `input()` ALWAYS returns a `str` — even if the user types "42".
# You receive the text "42", not the number 42. You must explicitly convert
# it with `int()` or `float()` before doing any arithmetic.
# If you skip the conversion, Python will raise a TypeError:
#   "5" + 6  →  TypeError     vs.     int("5") + 6  →  11
#
# IMPORTANT: `int("hello")` raises a `ValueError`. In production code, always
# wrap type-casting in a try-except to give a helpful error message instead of crashing.

# --- Example 1: Asking for Text ---
# Here, we ask the user for their name and print a greeting.
name = input("Enter your name: ")
print("Hello,", name)      
print()

# --- Example 2: Asking for Numbers ---
# Because `input()` always returns a string, we cannot do math directly with it.
# E.g., if you input "8" and try to add 6, you will get an error.
# We must convert the string to an integer (number) using `int()` first. This is called Type Casting.
# Steps:
#   1. Receive text: a = input("Enter a number: ")  -> "8" (a string)
#   2. Convert:      int(a) -> 8 (an integer)
#   3. Compute:      int(a) + 6 -> 14

a = input("Enter a number to add 6 to it: ")

# Convert `a` from text to an integer number, then add 6:
result = int(a) + 6
print("Your number + 6 is:", result)

# ==========================================
# REAL-LIFE USE CASES
# ==========================================
#
# 1. CLI Installation Prompts: Confirming configuration options or directory
#    paths during setup scripts.
#
# 2. Interactive Troubleshooting Logs: Asking developers to enter system IDs
#    to retrieve logs dynamically.
#
# 3. Interactive Shell Commands: Building a simple command interface for admin
#    scripts.

# ==========================================
# MNC INTERVIEW QUESTIONS & ANSWERS
# ==========================================
#
# Q1. What data type does the input() function always return in Python 3?
# A:  The input() function always returns a string (str), regardless of what
#     the user types. If you need numerical values, you must explicitly cast
#     them using int() or float() (e.g. age = int(input('Enter age: '))).
#
# Q2. How should you handle potential errors when casting user input to a
#     number?
# A:  Always wrap the type casting in a try-except block catching ValueError.
#     If a user enters non-numeric text (like 'hello') when an integer is
#     expected, casting raises a ValueError. Handling it prevents the script
#     from crashing.
#
# Q3. Why is using eval() on user input extremely dangerous?
# A:  eval() interprets and executes the user input string as active Python
#     code. If malicious input is passed, it can run arbitrary system
#     commands, delete directories, or steal credentials (Remote Code
#     Execution vulnerability). Never use eval() on untrusted input.