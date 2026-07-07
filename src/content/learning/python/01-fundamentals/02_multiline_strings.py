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
#
# Python has two distinct mechanisms for writing text that spans source lines:

# Method 1 — Backslash line continuation: The `\` at the end of a line tells
# the Python parser "this statement continues on the next line". It does NOT
# insert a newline character into the string. The resulting value is still a
# single contiguous line of text.

# Method 2 — Triple-quoted strings (`'''` or `"""`): Everything between the
# opening and closing triple-quote is kept verbatim, including real newlines,
# indentation, and spaces. This is the go-to method for multi-line content.
#
# KEY INSIGHT: Triple-quoted strings are used in three very different roles:
#   1. Docstrings (placed immediately after def/class) — Python stores them
#      in `obj.__doc__` and they appear in help().
#   2. Long string data — SQL queries, HTML templates, AI system prompts.
#   3. Temporary multi-line comments (though `#` comment lines are preferred).

# --- Method 1: Using the backslash `\` escape character ---
# The backslash tells Python: "This line continues on the next line."
# Note: This will print as a single line because Python joins them together.
# The `\` tells Python: "ignore the newline here; this string continues."
# The result is a single line of text — no \n is inserted.
print("--- Method 1: Backslash continuation ---")
a = 'Ritesh ' \
    'is a good boy'  # Note the space after Ritesh to prevent words from sticking
print(a)
print()

# --- Method 2: Using triple quotes `'''` or `"""` ---
# This is the most common way. Anything inside triple quotes maintains
# its exact formatting, including new lines and spaces.
# Everything between triple quotes is stored exactly as typed — real newlines,
# spaces, and indentation are all captured in the string value.
# This is the standard choice for multi-line SQL, JSON templates, or AI prompts.
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
# A:  A multiline string is simply any string that spans multiple lines,
#     typically enclosed in triple quotes (`'''` or `"""`). A docstring is a
#     special type of multiline string placed immediately at the beginning of
#     a module, class, method, or function. While a standard multiline string
#     is just data (and is ignored by the interpreter if not assigned), Python
#     parses docstrings and attaches them to the object's `__doc__` attribute,
#     making them accessible via `help()` and automatic documentation
#     generators. See the comparison table below:
#     
#     | Feature | Multiline String | Docstring |
#     | :--- | :--- | :--- |
#     | **Definition** | Standard string spanning lines | String at start of module/class/function |
#     | **Storage** | Evaluated or assigned to var | Saved in `__doc__` attribute |
#     | **Primary Use**| Text templates, long SQL queries | Code documentation & auto-doc generation |
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