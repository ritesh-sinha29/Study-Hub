# ==========================================
# PYTHON STRINGS AND METHODS (FOR BEGINNERS)
# ==========================================

# --- REAL-WORLD USE CASES ---
# Use a String when you need to store and manipulate text data.
# Examples:
#   * Usernames / Passwords: "ritesh_123"
#   * Form Entries: Storing names, addresses, or emails from input forms.
#   * Status Messages: Printing feedback to users like "Loading...", "Success!"

# A String is a sequence of characters surrounded by quotes.
# IMPORTANT RULE: Strings are IMMUTABLE (cannot be changed after creation).
# All string methods return a NEW string; they do NOT change the original string.

name = "Ritesh"
print("Original string:", name)
print()

# --- Common String Methods ---

# 1. isnumeric() - Returns True if all characters are numbers (like "123")
print("1. Is the name numeric?", name.isnumeric())

# 2. isalpha() - Returns True if all characters are letters (A-Z, a-z)
print("2. Is the name alphabetic?", name.isalpha())

# 3. title() - Capitalizes the first letter of each word
print("3. Title case:", name.title())

# 4. swapcase() - Swaps uppercase letters to lowercase and vice versa
print("4. Swap case:", name.swapcase())

# 5. upper() - Converts all characters to uppercase
print("5. Uppercase:", name.upper())

# 6. lower() - Converts all characters to lowercase
print("6. Lowercase:", name.lower())

# 7. find() - Returns the index position of the first occurrence of a character.
# Returns -1 if the character is not found.
print("7. Find index of 'i':", name.find("i")) # Found at index 1
print("   Find index of 'p':", name.find("p")) # Not found, returns -1

# 8. replace() - Replaces a specific character/substring with another one
print("8. Replace 'i' with 'o':", name.replace("i", "o"))

# 9. startswith() and endswith() - Check what the string starts/ends with (Case-Sensitive!)
name1 = "ritesh"
print("9. Does 'Ritesh' start with 'R'?", name.startswith("R"))
print("   Does 'ritesh' start with 'r'?", name1.startswith("r"))
print("   Does 'Ritesh' end with 'h'?", name.endswith("h"))
print("   Does 'ritesh' end with 'H'?", name1.endswith("H")) # False because 'H' is uppercase

# 10. split() - Splits the string into a list based on spaces (or other separators)
sentence = "Ritesh is a coder"
print("10. Splitting a sentence into a list:", sentence.split())

# 11. count() - Counts how many times a character appears in the string
print("11. Count of 'i' in 'Ritesh':", name.count("i"))
print("    Count of 'R' in 'Ritesh':", name.count("R"))
print("    Count of 'p' in 'Ritesh':", name.count("p"))
print()

# ==========================================
# STRING SLICING (EXTRACTING PARTS)
# ==========================================
# Slicing is used to break a string and get a smaller piece of it.
# Syntax: string[start_index : stop_index]
# Note: The stop_index is EXCLUSIVE (it is not included in the output).

# For "Ritesh": 0='R', 1='i', 2='t', 3='e', 4='s', 5='h'
print("--- String Slicing ---")
# This gets indices 0, 1, 2, 3 (index 4 's' is excluded)
print("Slicing name[0:4]:", name[0:4]) # Prints "Rite"

# ==========================================
# REAL-LIFE USE CASES
# ==========================================
#
# 1. User Profile Parsing: Extracting first/last name or username from form
#    inputs and sanitizing them (e.g. removing extra whitespaces using
#    strip()).
#
# 2. Email Validation: Checking if the input string contains '@' and ends with
#    a valid domain using endswith() and split().
#
# 3. Search Filters: Normalizing database queries and text search fields to
#    lowercase using lower() for case-insensitive matching.

# ==========================================
# MNC INTERVIEW QUESTIONS & ANSWERS
# ==========================================
#
# Q1. What is string immutability in Python, and why is it important?
# A:  Immutability means that once a string is created in memory, its contents
#     cannot be modified. Any operation (like upper(), replace()) returns a
#     NEW string object. This is important for performance (string
#     interning/sharing) and security (e.g. hash keys in dictionaries, file
#     paths, and database connections).
#
# Q2. What is the difference between find() and index() string methods?
# A:  Both methods search for a substring. See the comparison table below:
#
#     +-------------+-----------------------+---------------------------------+
#     | Method      | If Substring Found    | If Substring Not Found          |
#     +-------------+-----------------------+---------------------------------+
#     | find()      | Returns start index   | Returns -1 (safe)               |
#     | index()     | Returns start index   | Raises ValueError (needs try)   |
#     +-------------+-----------------------+---------------------------------+
#
# Q3. How does Python store strings in memory (String Interning)?
# A:  Python automatically 'interns' short, identifier-like strings
#     (containing only letters, numbers, or underscores). This means they
#     point to the exact same memory address. You can check this using the
#     'is' operator (e.g. a = 'hello'; b = 'hello'; a is b -> True).