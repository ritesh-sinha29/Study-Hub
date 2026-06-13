# ==========================================
# PYTHON TUPLES AND METHODS (FOR BEGINNERS)
# ==========================================

# --- REAL-WORLD USE CASES ---
# Use a Tuple when you have a sequence of values that must NEVER change 
# during the execution of your program. This prevents accidental changes.
# Examples:
#   * GPS Coordinates: (latitude, longitude) e.g., (28.6139, 77.2090)
#   * RGB Colors: (red, green, blue) e.g., (255, 0, 0) for pure Red.
#   * Calendar constants: ("Monday", "Tuesday", ...) or ("Jan", "Feb", ...)

# A Tuple is an ordered collection of items.
# Rule 1: We use parentheses `()` to create a tuple.
# Rule 2: Tuples are IMMUTABLE (cannot be changed). Once created, you cannot add, remove, or modify items.
# Rule 3: Tuples can contain duplicates and different data types.

# Let's create a tuple of numbers:
t = (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 1)

print("--- 1. Original Tuple ---")
print(t)
print("Type of this container is:", type(t))
print()

# --- Tuple Methods ---
# Since tuples cannot be changed, they have very few methods (only two!).

# 1. count() - Counts how many times an element appears in the tuple.
print("--- 2. Using .count() ---")
print("Number of times '1' appears in the tuple:", t.count(1))
print()

# 2. index() - Finds the first index position of a specific element.
print("--- 3. Using .index() ---")
print("Index (position) of the first occurrence of '7':", t.index(7))
print()

# --- Proof of Immutability ---
print("--- 4. Trying to modify a tuple (Raises Error) ---")
# If we try to change a value in a tuple, Python will raise a TypeError:
# t[0] = 89  # <- This line is commented out because it will crash the script!
print("# You cannot write: t[0] = 89")
print("# Python does not allow changing tuple values after they are created.")

# ==========================================
# REAL-LIFE USE CASES
# ==========================================
#
# 1. Database Records: Representing rows from a database table where each
#    index has a fixed meaning (e.g. (id, username, email)).
#
# 2. API Coordinates: Storing fixed spatial coords (latitude, longitude) or
#    screen size specifications.
#
# 3. Dictionary Keys: Using a combination of values (like first_name,
#    last_name) as a unique key in a hash map.

# ==========================================
# MNC INTERVIEW QUESTIONS & ANSWERS
# ==========================================
#
# Q1. Why are tuples faster and more memory-efficient than lists in Python?
# A:  Tuples are immutable, meaning their size and contents are fixed at
#     creation. Python can allocate exactly the required memory block for a
#     tuple, reducing overhead. Lists are mutable and require dynamic
#     over-allocation (extra buffer space) to support efficient `append()`
#     operations, making them consume more memory. Tuples are best for fixed,
#     read-only data, while lists are necessary when elements need to be
#     added, removed, or modified. See the comparison table below:
#     
#     | Feature | Tuple | List |
#     | :--- | :--- | :--- |
#     | **Mutability** | Immutable (fixed) | Mutable (modifiable) |
#     | **Syntax** | Parentheses `()` | Square brackets `[]` |
#     | **Memory** | Fixed allocation (smaller) | Dynamic over-allocation (larger) |
#     | **Performance**| Faster access/creation | Slower |
#
# Q2. Can a tuple contain mutable elements? Is it still hashable?
# A:  Yes, a tuple can contain mutable elements like lists (e.g. t = (1, 2,
#     [3, 4])). However, a tuple is ONLY hashable (and can only be used as a
#     dictionary key or set element) if ALL of its elements are also
#     hashable/immutable. If it contains a list, it raises a TypeError.
#
# Q3. What is tuple unpacking, and how is it commonly used to swap variables?
# A:  Tuple unpacking allows assigning elements of a tuple to separate
#     variables in one line. Swapping variables uses this: 'a, b = b, a'.
#     Python evaluates the right side (creating a temporary tuple (b, a)) and
#     unpacks it into the variables on the left.