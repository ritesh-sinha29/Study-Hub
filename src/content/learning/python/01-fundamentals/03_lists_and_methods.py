# ==========================================
# PYTHON LISTS AND METHODS (FOR BEGINNERS)
# ==========================================

# --- REAL-WORLD USE CASES ---
# Use a List when you have a collection of items where order matters, 
# and you want to add, remove, or sort items later.
# Examples:
#   * Shopping List: ["milk", "bread", "eggs"]
#   * Music Playlist: ["song1", "song2", "song3"]
#   * To-Do List: ["study python", "go to gym", "clean room"]

# A List is an ordered collection of items.
# Rule 1: We use square brackets `[]` to create a list.
# Rule 2: Lists are mutable (changeable). You can add, remove, or change items.
# Rule 3: Lists can hold different types of data at the same time (strings, numbers, etc.).
#
# HOW IT WORKS INTERNALLY: Python lists are dynamic arrays. When you `append()`
# past the current capacity, Python allocates a bigger block (roughly doubles)
# and copies existing items over. This is why append is O(1) amortized, but
# insert at position 0 is O(n) because every item must shift right.
#
# KEY INSIGHT: Lists can hold mixed types, but sorting requires all items
# to be comparable to each other. Mixing str and int causes a TypeError
# because Python doesn't know how to rank "Ritesh" vs 5.

# Let's create a list with numbers and a string:
my_list = [6, 5, 4, 3, 2, 1, 0, "Ritesh"]

# Print the list and its type
print("--- 1. Original List ---")
print(my_list)
print("Type of this container is:", type(my_list))
print()

# --- Method: .reverse() ---
# This flips the list upside down (in-place).
# .reverse() modifies the list IN-PLACE and returns None.
# Use when you want the list itself reversed, not a reversed copy.
# If you need a reversed copy without touching the original, use reversed().
print("--- 2. Reversing the List ---")
my_list.reverse()
print("Reversed list:", my_list)
print()

# --- Sorting a List ---
# The .sort() method arranges items in ascending order (like 0, 1, 2, 3...).
# IMPORTANT: You CANNOT sort a list that contains both numbers AND strings.
# If you try to sort `[1, "Ritesh"]`, Python will throw a TypeError.
# .sort() modifies the list IN-PLACE (returns None).
# Use sorted(lst) instead if you need the original list unchanged.
print("--- 3. Sorting a Mixed List (Raises Error) ---")
print("# We cannot sort my_list because it has 'Ritesh' (string) and numbers!")
print()

# Let's create a list with ONLY numbers so we can sort it:
numbers_list = [6, 5, 4, 3, 2, 1, 0]

print("--- 4. Sorting a List of Numbers ---")
print("Before sort:", numbers_list)
numbers_list.sort()  # Sorts the numbers in-place (ascending order)
print("After sort:", numbers_list)

# ==========================================
# REAL-LIFE USE CASES
# ==========================================
#
# 1. Shopping Carts: Maintaining an ordered, modifiable collection of items
#    selected by a user.
#
# 2. Task Queues: Implementing a basic queue using list methods where tasks
#    are appended and popped.
#
# 3. Data Feed Buffering: Accumulating live API payloads before saving them in
#    a database.

# ==========================================
# MNC INTERVIEW QUESTIONS & ANSWERS
# ==========================================
#
# Q1. What is the difference between append() and extend() on a Python list?
# A:  `append()` adds the passed object as a single item to the end of the
#     list, regardless of whether it is a number, string, or another list.
#     `extend()` takes an iterable (like a list, tuple, or set), iterates over
#     its elements, and appends each element individually. Use `append()` when
#     adding a single object, and `extend()` when merging lists or adding
#     multiple items from an iterable. See the comparison table below:
#     
#     | Method | Parameter Type | Action |
#     | :--- | :--- | :--- |
#     | `append()` | Any object (single item) | Adds argument as 1 new element |
#     | `extend()` | Iterable (list, tuple, etc.) | Unpacks & appends all items |
#
# Q2. How does Python allocate memory for lists, and what is its performance
#     implication?
# A:  Python lists are dynamic arrays. To avoid resizing on every append,
#     Python over-allocates memory. Resizing happens exponentially. Append has
#     an amortized time complexity of O(1), but insertion at arbitrary indexes
#     is O(n) because elements must be shifted.
#
# Q3. What is the difference between list.sort() and sorted()?
# A:  `list.sort()` sorts the list in-place, modifying the original list
#     directly and returning `None`. This is more memory-efficient as it does
#     not copy elements. `sorted()` is a built-in function that creates and
#     returns a new sorted list, leaving the original iterable unchanged. Use
#     `list.sort()` when you want to modify the list in place to save memory,
#     and `sorted()` when you need to preserve the original order or sort
#     other iterables like tuples or dictionaries. See the comparison table
#     below:
#     
#     | Operation | Modification | Return Value | Iterable Type |
#     | :--- | :--- | :--- | :--- |
#     | `list.sort()` | Modifies in-place | Returns `None` | Lists only |
#     | `sorted()` | Creates new list | Returns sorted list | Any iterable |