# Multiline Strings

```python
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
```
