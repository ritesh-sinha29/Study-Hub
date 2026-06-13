# ==========================================
# MORE ON STRINGS: MULTI-LINE STRINGS (FOR BEGINNERS)
# ==========================================

# --- REAL-WORLD USE CASES ---
# Use Multi-line Strings when you need to write large blocks of text.
# Examples:
#   * Email Templates: Writing a greeting, body, and sign-off.
#   * Database Queries: Writing long SQL statements across multiple lines.
#   * Help Messages / Instructions: Displaying a multi-line menu to users.

# Sometimes we want to write a long string that spans multiple lines.
# There are two main ways to write multi-line strings in Python:

# --- Method 1: Using the backslash `\` escape character ---
# The backslash tells Python: "This line continues on the next line."
# Note: This will print as a single line because Python joins them together.
print("--- Method 1: Backslash continuation ---")
a = 'Ritesh ' \
    'is a good boy'  # Note the space after Ritesh to prevent words from sticking
print(a)
print()

# --- Method 2: Using triple quotes `'''` or `"""` ---
# This is the most common way. Anything inside triple quotes maintains 
# its exact formatting, including new lines and spaces.
print("--- Method 2: Triple Quotes ---")
b = '''Ritesh
is a good boy'''
print(b)

# ==========================================
# REAL-LIFE USE CASES
# ==========================================
#
# 1. SQL Queries: Writing long, readable multi-line database queries directly
#    in the code.
#
# 2. AI System Prompts: Defining complex instructions and templates for LLM
#    API calls.
#
# 3. HTML/Text Templates: Formatting multi-line email bodies or basic HTML
#    pages dynamically.

# ==========================================
# MNC INTERVIEW QUESTIONS & ANSWERS
# ==========================================
#
# Q1. What is the difference between a multiline string and a docstring in
#     Python?
# A:  A multiline string is just a string spanning multiple lines (defined
#     using triple quotes). A docstring is a specific type of multiline string
#     placed at the very start of a module, class, or function. It is stored
#     in the object's __doc__ attribute and used for documentation.
#
# Q2. What are Raw Strings (r'...'), and when should you use them?
# A:  Raw strings ignore escape characters like \n or \t, treating backslashes
#     as literal characters. They are essential when writing Regular
#     Expressions (regex) or Windows file paths (e.g.
#     r'C:\Users\name\documents').
#
# Q3. How can you write a long string spanning multiple lines without
#     including newline characters?
# A:  You can wrap the string in parentheses. Python automatically
#     concatenates adjacent string literals inside parentheses at compile time
#     (e.g. s = ('This is a ' 'long string') -> 'This is a long string').