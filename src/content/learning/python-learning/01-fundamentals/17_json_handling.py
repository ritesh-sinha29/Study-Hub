# ==========================================
# PYTHON JSON HANDLING (FOR BEGINNERS)
# ==========================================

# --- WHAT IS JSON? ---
# JSON stands for JavaScript Object Notation.
# It is the UNIVERSAL language of APIs — all data sent between a
# frontend (website/app) and a backend (FastAPI) is in JSON format.
# JSON looks EXACTLY like a Python dictionary!

# Python Dictionary:  {"name": "Ritesh", "age": 20}
# JSON string:        '{"name": "Ritesh", "age": 20}'
# They look the same, but a JSON string is just TEXT, not a Python object.

# --- REAL-WORLD USE CASES ---
# * FastAPI: Receives JSON from a mobile app, returns JSON responses
# * LangGraph: AI agents pass messages and state as JSON
# * Reading config files, API responses, databases — all use JSON

import json  # Python's built-in JSON module

print("==========================================")
print("1. PYTHON DICT → JSON STRING (json.dumps)")
print("==========================================")

# `json.dumps()` → "dumps into string" (converts Python dict to JSON text)

user = {
    "name": "Ritesh",
    "age": 20,
    "skills": ["Python", "FastAPI"],
    "is_active": True
}

json_string = json.dumps(user)
print("Python dict:", user)
print("JSON string:", json_string)
print("Type:", type(json_string))  # It's now a str (text), not a dict

print()

# Pretty printing JSON (easier to read, with indentation):
pretty_json = json.dumps(user, indent=4)
print("Pretty JSON:\n", pretty_json)

print()

# ==========================================
print("2. JSON STRING → PYTHON DICT (json.loads)")
print("==========================================")

# `json.loads()` → "loads from string" (converts JSON text back to Python dict)

json_text = '{"name": "Rox", "age": 22, "city": "Mumbai"}'

python_dict = json.loads(json_text)
print("JSON string:", json_text)
print("Python dict:", python_dict)
print("Type:", type(python_dict))  # Now it's a dict

# Now you can access data like a normal Python dictionary:
print("Name:", python_dict["name"])
print("City:", python_dict["city"])

print()

# ==========================================
print("3. READING JSON FROM A FILE")
print("==========================================")

# First, let's create a sample JSON file to read:
sample_data = {"app": "My FastAPI App", "version": "1.0", "debug": False}

with open("sample_config.json", "w") as f:
    json.dump(sample_data, f, indent=4)  # Write dict to file as JSON

# Now read it back:
with open("sample_config.json", "r") as f:
    loaded_data = json.load(f)  # Read JSON file and convert to Python dict

print("Loaded from file:", loaded_data)
print("App name:", loaded_data["app"])

print()

# ==========================================
print("4. LISTS OF DICTS — Common API Response Pattern")
print("==========================================")

# Most API responses are a LIST of JSON objects (dicts)
# This is EXACTLY what FastAPI returns when you request all users:

users_json = '''[
    {"id": 1, "name": "Ritesh", "role": "admin"},
    {"id": 2, "name": "Rox",    "role": "user"},
    {"id": 3, "name": "Sam",    "role": "user"}
]'''

users = json.loads(users_json)

print("All users:")
for user in users:
    print(f"  ID: {user['id']} | Name: {user['name']} | Role: {user['role']}")

print()

# ==========================================
print("5. FASTAPI USE CASE — JSON is the default response")
print("==========================================")

# In FastAPI, when you return a dictionary from a route function,
# FastAPI AUTOMATICALLY converts it to JSON and sends it to the client.
# You don't need to call json.dumps() yourself!

# Real FastAPI code:
#
#   @app.get("/users")
#   def get_users():
#       return {"users": [{"id": 1, "name": "Ritesh"}]}
#       # FastAPI automatically sends this as JSON to the browser

# Simulation:
def fastapi_get_users():
    # FastAPI auto-converts this dict to JSON response
    return {"users": [{"id": 1, "name": "Ritesh"}, {"id": 2, "name": "Rox"}]}

response = fastapi_get_users()
print("FastAPI response (as Python dict):", response)
print("FastAPI response (as JSON string):", json.dumps(response, indent=2))

# ==========================================
# REAL-LIFE USE CASES
# ==========================================
#
# 1. Rest API Requests: Converting dict payloads to JSON strings to send as
#    API payloads.
#
# 2. App Configuration files: Reading local config.json files to extract
#    application settings.
#
# 3. Caching Objects: Serializing data lists into JSON strings to store in
#    Redis caching key-values.

# ==========================================
# MNC INTERVIEW QUESTIONS & ANSWERS
# ==========================================
#
# Q1. What is the difference between json.dumps() and json.dump()?
# A:  `json.dumps()` (dump string) serializes a Python object into a
#     JSON-formatted string and returns it in memory. It is best when you need
#     to send JSON data over network APIs or modify it in code. `json.dump()`
#     serializes a Python object and writes it directly to an open file stream
#     on disk. Use `json.dumps()` for in-memory operations and API
#     integrations, and `json.dump()` for saving configuration or state files
#     directly to disk. See the comparison table below:
#     
#     | Function | Output Destination | Return Type |
#     | :--- | :--- | :--- |
#     | `json.dumps()` | Memory (in code) | JSON string |
#     | `json.dump()` | Disk (file stream) | `None` (writes directly to file) |
#
# Q2. How do you serialize custom Python objects (like custom classes) to
#     JSON?
# A:  The default json module raises a TypeError for custom classes. You can
#     serialize them by: 1) passing a custom serializer class that inherits
#     from json.JSONEncoder, 2) converting the object to a dictionary first
#     (e.g., using object.__dict__), or 3) using libraries like pydantic.
#
# Q3. What is the difference between a Python dictionary and a JSON object?
# A:  A Python dictionary is a live, in-memory hash map data structure that
#     can contain arbitrary objects as values and any hashable object as keys.
#     A JSON object is a text representation of structured data used for
#     serialization and communication between languages. JSON keys must always
#     be double-quoted strings, and JSON only supports a limited set of
#     primitive data types (like numbers, strings, booleans, and null). Use
#     Python dictionaries for active computation, and JSON for API payloads or
#     storage formats. See the comparison table below:
#     
#     | Feature | Python dict | JSON Object |
#     | :--- | :--- | :--- |
#     | **Type** | Memory data structure | Text serialization format |
#     | **Key Types** | Any hashable object | String only |
#     | **Null Value** | `None` | `null` |
#     | **Boolean** | `True` / `False` | `true` / `false` |