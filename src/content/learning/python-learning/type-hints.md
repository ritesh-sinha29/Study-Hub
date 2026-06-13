# Type Hints

## PYTHON TYPE HINTS (FOR BEGINNERS)

## WHAT ARE TYPE HINTS?

Type hints are labels you add to tell Python (and YOU) what TYPE of data
a variable or function expects. They do NOT crash if wrong, but editors
will warn you and FastAPI uses them to VALIDATE data automatically.

## REAL-WORLD USE CASES

* FastAPI uses type hints to automatically:
    - Validate incoming request data
    - Generate API documentation
    - Return correct response formats
* LangGraph uses type hints to define the shape of AI agent state.

## BASIC SYNTAX

variable_name: data_type = value

```python
print("==========================================")
print("1. BASIC TYPE HINTS ON VARIABLES")
print("==========================================")

name: str = "Ritesh"         # str = text/string
age: int = 20                # int = whole number
height: float = 5.9          # float = decimal number
is_student: bool = True      # bool = True or False

print("Name:", name)
print("Age:", age)
print("Height:", height)
print("Is student:", is_student)

print()
```

```python
print("2. TYPE HINTS ON FUNCTIONS")
print("==========================================")
```

You can label what a function EXPECTS (parameters) and what it RETURNS
Syntax: def function_name(param: type) -> return_type:

```python
def add(a: int, b: int) -> int:
    # This function takes two integers and returns an integer
    return a + b

def greet(name: str) -> str:
    # This function takes a string and returns a string
    return "Hello, " + name

print(add(5, 10))
print(greet("Ritesh"))

print()
```

```python
print("3. TYPE HINTS WITH LISTS AND DICTS")
print("==========================================")
```

For lists and dicts, we use `list` and `dict` directly (Python 3.9+)

```python
def get_first_item(items: list) -> str:
    return items[0]

def get_user_name(user: dict) -> str:
    return user["name"]

fruits: list = ["apple", "banana", "mango"]
person: dict = {"name": "Ritesh", "age": 20}

print("First fruit:", get_first_item(fruits))
print("User name:", get_user_name(person))

print()
```

```python
print("4. OPTIONAL — When a value might be None")
print("==========================================")
```

Sometimes a value may or may not exist. We use Optional for that.
`Optional[str]` means the value is either a str OR None.

```python
from typing import Optional

def find_user(user_id: int) -> Optional[str]:
    # Returns a name if found, or None if not found
    users = {1: "Ritesh", 2: "Rox"}
    return users.get(user_id)  # .get() returns None if key not found

print("User 1:", find_user(1))
print("User 99:", find_user(99))  # Returns None

print()
```

```python
print("5. UNION — When a value can be one of multiple types")
print("==========================================")
```

`Union[int, str]` means the value can be either an int OR a str.

```python
from typing import Union

def process_id(user_id: Union[int, str]) -> str:
    return f"Processing user with ID: {user_id}"

print(process_id(42))
print(process_id("ritesh_dev"))

print()
```

```python
print("6. FASTAPI USE CASE — How FastAPI uses type hints")
print("==========================================")
```

This is what a real FastAPI route looks like with type hints.
FastAPI reads the type hints and:
  1. Validates the input automatically
  2. Shows correct types in the auto-generated docs page (/docs)

(This is just a demonstration — no FastAPI imported here)

```python
def create_user(name: str, age: int, email: str) -> dict:
    # FastAPI will reject the request automatically if:
    # - `age` is not a number
    # - `email` is not a string
    # All thanks to type hints!
    new_user = {
        "name": name,
        "age": age,
        "email": email
    }
    return new_user

print(create_user("Ritesh", 20, "ritesh@example.com"))
```

