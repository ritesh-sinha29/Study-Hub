# ==========================================
# PYTHON SETS AND METHODS (FOR BEGINNERS)
# ==========================================

# --- WHY LEARN THIS? ---
# Use a Set when you want to ensure there are no duplicate items, 
# or when you need to perform math-like operations (like finding common values).
# Examples:
#   * Unique Visitors: Storing IP addresses of users visiting a website.
#   * Mutual Friends: Finding the intersection (common friends) between two profiles.
#   * Deduplication: Removing duplicate items from a list of registered emails.

# A Set is an unordered collection of **UNIQUE** elements.
#
# **Rule 1:** We use curly braces `{}` to create a set.
#
# **Rule 2:** Sets do not allow duplicate items. Any duplicates are automatically removed!
#
# **Rule 3:** Sets are unordered (they don't keep track of the insertion order).
#
# **HOW IT WORKS INTERNALLY:** Python computes a hash for every item you add.
# If two items produce the same hash (collision), Python checks whether they
# are truly equal. If equal, only one copy is kept — hence automatic deduplication.
#
# Because lookup is hash-based, checking `x in my_set` is O(1) regardless of
# how large the set is, compared to O(n) for a list search.
#
# Set mathematics are built directly in:
#   |  (union)          — all unique items from both sets
#   &  (intersection)   — items present in BOTH sets
#   -  (difference)     — items in A but not in B
#   ^  (symmetric diff) — items in either set, but NOT in both
#
# **KEY INSIGHT:** Elements must be **HASHABLE** (immutable). Lists, dicts, and other
# sets cannot be added to a set because they are mutable and their hash would
# change — breaking the internal hash table.


# Let's create two sets of numbers:
a1 = {3, 5, 6, 7, 7, 88, 8, 9, 9, 9, 10, 111, 111}
a2 = {22, 55, 77, 44, 97, 8383, 77, 333, 555, 666, 99, 323}

print("--- 1. Original Sets ---")
# Notice how duplicate numbers (like 7, 9, 111, 77) are removed automatically:
print("Set a1:", a1)
print("Set a2:", a2)
print()

# --- Common Set Operations ---

# .union() — returns a NEW set containing every unique item from both sets.
# Equivalent to the pipe operator: a1 | a2
# Use case: merge two tag lists, combine two user permission sets.
print("--- 2. Union ---")
all_items = a1.union(a2)
print("Combined unique items:", all_items)
print()

# .intersection() — returns items that appear in BOTH sets.
# Equivalent to: a1 & a2
# Use case: find mutual friends, find products in both a wishlist and a sale.
print("--- 3. Intersection ---")
common_items = a1.intersection(a2)
print("Items present in both a1 and a2:", common_items) # Should be empty set() since they have no common numbers
print()

# .difference() — items in the LEFT set that are NOT in the right set.
# Equivalent to: a1 - a2
# Use case: find users who have NOT upgraded to premium.
print("--- 4. Difference ---")
diff_items = a1.difference(a2)
print("Items in a1 but not in a2:", diff_items)
print()

# .symmetric_difference() — items in either set, but NOT shared by both.
# Equivalent to: a1 ^ a2
# Use case: find users who are in exactly one of two user groups.
print("--- 5. Symmetric Difference ---")
sym_diff = a1.symmetric_difference(a2)
print("Items unique to each set:", sym_diff)
print()

# --- Checking Set Relationships ---

# 5. Isdisjoint: Returns True if two sets have NO elements in common
print("--- 6. Disjoint Sets Check ---")
print("Do a1 and a2 have no elements in common?", a1.isdisjoint(a2))
print()

# 6. Issubset: Returns True if all elements of a set are inside another set
# 7. Issuperset: Returns True if a set contains all elements of another set
small_set = {3, 5}
print("--- 7. Subset and Superset Checks ---")
print("Is {3, 5} a subset of a1?", small_set.issubset(a1))
print("Is a1 a superset of {3, 5}?", a1.issuperset(small_set))
print()

# --- Modifying Sets ---

# 8. Add: Adds a single element to a set
print("--- 8. Adding Elements ---")
a1.add(500)
print("a1 after adding 500:", a1)
print()

# 9. Remove: Removes a specific element. (Will raise a KeyError if element is not found)
print("--- 9. Removing Elements ---")
a1.remove(500)
print("a1 after removing 500:", a1)

# Note: Calling a1.remove(a1) would fail because a1 is a set, not a number inside the set.

# ==========================================
# REAL-LIFE USE CASES
# ==========================================
#
# 1. Unique Visitors Tracking: Logging IP addresses or user IDs to count
#    unique active users daily.
#
# 2. Social Graph Commonalities: Finding common friends/followers between two
#    users using set intersections.
#
# 3. Spam Filtering: Comparing a list of words in an email against a set of
#    known spam words.

# ==========================================
# MNC INTERVIEW QUESTIONS & ANSWERS
# ==========================================
#
# Q1. What is the time complexity of searching (membership testing) in a set
#     vs a list?
# A:  Searching in a set is O(1) on average because sets are implemented as
#     hash tables. In contrast, searching in a list is O(n) because Python
#     must scan the list element-by-element. Always use sets for large
#     membership checks.
#
# Q2. What are the requirements for an element to be added to a set?
# A:  Elements in a set must be 'hashable'. This means they must have a hash
#     value that never changes during their lifetime (i.e. they must be
#     immutable objects like strings, numbers, or tuples containing only
#     immutable types). Lists or dictionaries cannot be added to sets.
#
# Q3. What is the difference between set.remove() and set.discard()?
# A:  `remove()` will search for the element and delete it, but raises a
#     `KeyError` if the element is not present. This is best when the missing
#     item indicates an unexpected application error. `discard()` removes the
#     element if it exists, but fails silently without raising an error if it
#     is missing. Use `discard()` when you want to ensure an element is gone
#     but don't care if it was never there in the first place. See the
#     comparison table below:
#     
#     | Method | If Element Exists | If Element Not Found |
#     | :--- | :--- | :--- |
#     | `remove()` | Deletes element from set | Raises `KeyError` |
#     | `discard()` | Deletes element from set | Fails silently (no error) |