# Json Handling

## PYTHON JSON HANDLING (FOR BEGINNERS)

## WHAT IS JSON?

JSON stands for JavaScript Object Notation.
It is the UNIVERSAL language of APIs — all data sent between a
frontend (website/app) and a backend (FastAPI) is in JSON format.
JSON looks EXACTLY like a Python dictionary!

Python Dictionary:  {"name": "Ritesh", "age": 20}
JSON string:        '{"name": "Ritesh", "age": 20}'
They look the same, but a JSON string is just TEXT, not a Python object.

## REAL-WORLD USE CASES

* FastAPI: Receives JSON from a mobile app, returns JSON responses
* LangGraph: AI agents pass messages and state as JSON
* Reading config files, API responses, databases — all use JSON

```python
import json  # Python's built-in JSON module

print("==========================================")
print("1. PYTHON DICT → JSON STRING (json.dumps)")
print("==========================================")
```

`json.dumps()` → "dumps into string" (converts Python dict to JSON text)

```python
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
```

Pretty printing JSON (easier to read, with indentation):

```python
pretty_json = json.dumps(user, indent=4)
print("Pretty JSON:\n", pretty_json)

print()
```

```python
print("2. JSON STRING → PYTHON DICT (json.loads)")
print("==========================================")
```

`json.loads()` → "loads from string" (converts JSON text back to Python dict)

```python
json_text = '{"name": "Rox", "age": 22, "city": "Mumbai"}'

python_dict = json.loads(json_text)
print("JSON string:", json_text)
print("Python dict:", python_dict)
print("Type:", type(python_dict))  # Now it's a dict
```

Now you can access data like a normal Python dictionary:

```python
print("Name:", python_dict["name"])
print("City:", python_dict["city"])

print()
```

```python
print("3. READING JSON FROM A FILE")
print("==========================================")
```

First, let's create a sample JSON file to read:

```python
sample_data = {"app": "My FastAPI App", "version": "1.0", "debug": False}

with open("sample_config.json", "w") as f:
    json.dump(sample_data, f, indent=4)  # Write dict to file as JSON
```

Now read it back:

```python
with open("sample_config.json", "r") as f:
    loaded_data = json.load(f)  # Read JSON file and convert to Python dict

print("Loaded from file:", loaded_data)
print("App name:", loaded_data["app"])

print()
```

```python
print("4. LISTS OF DICTS — Common API Response Pattern")
print("==========================================")
```

Most API responses are a LIST of JSON objects (dicts)
This is EXACTLY what FastAPI returns when you request all users:

```python
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
```

```python
print("5. FASTAPI USE CASE — JSON is the default response")
print("==========================================")
```

In FastAPI, when you return a dictionary from a route function,
FastAPI AUTOMATICALLY converts it to JSON and sends it to the client.
You don't need to call json.dumps() yourself!

Real FastAPI code:

```python
@app.get("/users")
  def get_users():
      return {"users": [{"id": 1, "name": "Ritesh"}]}
```

# FastAPI automatically sends this as JSON to the browser

Simulation:

```python
def fastapi_get_users():
    # FastAPI auto-converts this dict to JSON response
    return {"users": [{"id": 1, "name": "Ritesh"}, {"id": 2, "name": "Rox"}]}

response = fastapi_get_users()
print("FastAPI response (as Python dict):", response)
print("FastAPI response (as JSON string):", json.dumps(response, indent=2))
```

