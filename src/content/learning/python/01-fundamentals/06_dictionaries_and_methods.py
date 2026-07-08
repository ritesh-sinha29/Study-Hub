# ==========================================
# PYTHON DICTIONARIES (LEARNING GUIDE)
# ==========================================

# --- WHY LEARN THIS? ---
# Use a Dictionary when you want to search for data using a "label" (Key) 
# instead of a number index.
# Examples:
#   * Contact Book: Mapping "Ritesh" -> "9876543210"
#   * User Profile: Mapping "username" -> "ritesh_dev", "email" -> "ritesh@example.com"
#   * Game Settings: Mapping "volume" -> 80, "theme" -> "Dark Mode"

# Imagine a real-life dictionary:
# You look up a "Word" (Key) to find its "Meaning" (Value).
# In Python, a dictionary is a collection of "Key: Value" pairs.
#
# **Rule 1:** We use curly braces `{}` to create a dictionary.
#
# **Rule 2:** Each key is separated from its value by a colon `:`
#
# **Rule 3:** Each key-value pair is separated by a comma `,`
#
# **HOW IT WORKS INTERNALLY:** Python is a built-in hash map. Every key is hashed
# to find its bucket, so lookup is O(1) regardless of dict size — in a list
# you'd have to scan every entry, but in a dict you jump straight to the answer.
#
# **KEY INSIGHT:** Keys must be hashable (strings, ints, tuples — NOT lists or
# dicts). Values can be anything: numbers, lists, nested dicts, even functions.

# Let's create our first dictionary storing information about a person:
person = {
    "name": "Ritesh",       # "name" is the Key (label), "Ritesh" is the Value
    "age": 20,              # "age" is the Key, 20 is the Value (number)
    "city": "Delhi",        # "city" is the Key, "Delhi" is the Value
    "is_student": True      # "is_student" is the Key, True is the Value (Boolean)
}

# Let's print the entire dictionary to see how it looks:
print("--- 1. Printing the whole dictionary ---")
print(person)
print()  # prints an empty line for neat spacing


# ==========================================
# HOW TO ACCESS (READ) DATA FROM A DICTIONARY
# ==========================================
# Two ways: bracket notation `d[key]` and `.get(key, default)`.
# Bracket: fast, raises KeyError if the key is missing — best when the key
# is required and its absence is a programming error.
# .get(): safe, returns None (or your custom default) if missing — best for
# optional fields like user-provided query parameters or config overrides.
# ==========================================

# You can access a value by putting its key inside square brackets `[]`:
print("--- 2. Accessing data using brackets ---")
my_name = person["name"]
print("Name of the person is:", my_name)
print()

# What if the key doesn't exist? E.g., person["salary"]
# That will cause a crash (KeyError).
# To prevent crashes, you can use the `.get()` method.
# If the key is not found, `.get()` will return 'None' (nothing) instead of crashing.
print("--- 3. Safely accessing data using .get() ---")
print("Age:", person.get("age"))
print("Salary (does not exist):", person.get("salary")) # Returns None, doesn't crash
print()


# ==========================================
# HOW TO ADD OR UPDATE DATA
# ==========================================
# Assigning `d[key] = value` does double duty:
#   • If the key already exists — the old value is REPLACED.
#   • If the key is new — a new entry is INSERTED.
# This is intentional. There is no separate "insert" and "update" — it’s
# always a single upsert operation.
# ==========================================

# To change a value, just use its key and assign a new value:
print("--- 4. Changing (updating) a value ---")
person["age"] = 21  # Changes age from 20 to 21
print("Updated age:", person["age"])
print()

# To add a brand new item, use a new key:
print("--- 5. Adding a new item ---")
person["hobby"] = "Coding"  # Adds a new key "hobby" with value "Coding"
print("After adding hobby:", person)
print()


# ==========================================
# DICTIONARY METHODS (BUILT-IN TOOLS)
# ==========================================
# Dictionaries expose view objects (.keys(), .values(), .items()) that are
# LIVE — they update automatically if the dict changes. You can iterate over
# them or wrap in list() to get a static snapshot.
# ==========================================

#
# **Method 1:** .keys()
# This gives you a list of all the keys (labels) in the dictionary.
print("--- 6. Getting all keys using .keys() ---")
all_keys = person.keys()
print(all_keys) 
print()

#
# **Method 2:** .values()
# This gives you a list of all the values in the dictionary.
print("--- 7. Getting all values using .values() ---")
all_values = person.values()
print(all_values)
print()

#
# **Method 3:** .items()
# This gives you all key-value pairs grouped together as pairs.
print("--- 8. Getting all pairs using .items() ---")
all_pairs = person.items()
print(all_pairs)
print()

#
# **Method 4:** .update()
# This allows you to add or change multiple items at once.
print("--- 9. Updating multiple items using .update() ---")
person.update({"city": "Mumbai", "phone": 123456})
print("After update:", person)
print()

#
# **Method 5:** .pop()
# This removes an item using its key and returns the value that was removed.
print("--- 10. Removing an item using .pop() ---")
removed_hobby = person.pop("hobby")
print("Removed hobby was:", removed_hobby)
print("Dictionary after popping hobby:", person)
print()

#
# **Method 6:** .clear()
# This completely empties the dictionary.
print("--- 11. Emptying the dictionary using .clear() ---")
person.clear()
print("Dictionary after clear():", person)

# ==========================================
# REAL-LIFE USE CASES
# ==========================================
# 1. User Session Caching: Mapping user session tokens (keys) to active user
#    - **Step 1**: Profile objects (values).
#
# 2. API Headers Configuration: Structuring HTTP headers (Content-Type,
#    - **Step 1**: Authorization) as key-value pairs.
#
# 3. Entity Mapping: Storing configuration profiles, database configurations,
#    - **Step 1**: Or localized translation maps.

# ==========================================
# MNC INTERVIEW QUESTIONS & ANSWERS
# ==========================================
#
# Q1. What are the constraints on Python dictionary keys?
# A:  Dictionary keys must be hashable. This means they must be immutable
#     objects (e.g., strings, numbers, tuples with immutable items). Mutable
#     objects like lists, sets, or other dictionaries cannot be used as keys
#     because their hashes could change, breaking lookup logic.
#
# Q2. How does Python resolve key lookups, and what happens during a hash
#     collision?
# A:  Python dictionaries use hash tables. It hashes the key to find a bucket
#     index. If multiple keys hash to the same bucket (collision), Python uses
#     'open addressing' (specifically pseudo-random probing) to search for the
#     next available bucket. Lookups remain O(1) on average.
#
# Q3. How does the get() method differ from using bracket notation dict[key]?
# A:  Using bracket notation `dict[key]` is faster but raises a `KeyError` if
#     the key does not exist. It is best used when you are certain the key is
#     present or want to treat its absence as an error. `dict.get(key,
#     default)` is safer because it returns a default value (like `None` or a
#     custom string/number) if the key is missing. Use `get()` to safely
#     handle optional keys without throwing exceptions. See the comparison
#     table below:
#     
#     | Access Method | If Key Exists | If Key Is Missing |
#     | :--- | :--- | :--- |
#     | `dict[key]` | Returns the value | Raises `KeyError` |
#     | `dict.get()` | Returns the value | Returns default (`None` or custom) |