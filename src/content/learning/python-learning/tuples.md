# Tuples

```python
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
print("# Python does not allow changing tuple values after they are created.")```
