# ==========================================================
# FASTAPI STUDY: PYDANTIC MODELS (NESTED MODELS)
# ==========================================================

# --- WHAT IS PYDANTIC? ---
# Pydantic is a library that helps you define the STRUCTURE/SHAPE of your data.
# Think of it like a BLUEPRINT or a FORM with rules.
# When someone sends data to your API, Pydantic checks:
#   - "Is the data in the right format?"
#   - "Are all the required fields present?"
#   - "Are the data types correct?" (e.g., age must be a number, not text)


# ==========================================================
# 1. WHAT IS BASEMODEL?
# ==========================================================

# BaseModel is the HEART of Pydantic. It's a class you INHERIT from.
# When your class inherits from BaseModel, it gets SUPERPOWERS:
#   - Automatic validation: Checks types when you create an object.
#   - Type conversion: If possible, converts data to the right type.
#   - Clear error messages: Tells you EXACTLY what's wrong.

# Example without BaseModel (regular class):
#   class User:
#       def __init__(self, name, age):
#           self.name = name
#           self.age = age
#   u = User("John", "abc")   # No error! But age = "abc" is wrong!

# Example with BaseModel (Pydantic):
#   class User(BaseModel):
#       name: str
#       age: int
#   u = User(name="John", age="abc")   # ERROR! age must be int

# This saves you from writing 100s of if/else checks manually!


# ==========================================================
# 2. WHAT IS A SCHEMA? (JSON SCHEMA)
# ==========================================================

# A Schema is the BLUEPRINT or RULEBOOK for your data.
# It defines: what fields exist, what types they are, and what values are allowed.

# When you write a Pydantic model like:
#   class User(BaseModel):
#       name: str
#       age: int
# ...you are defining a SCHEMA automatically!

# Pydantic can also generate a STANDARD JSON Schema (a format that ANY language
# can understand — JavaScript, TypeScript, Java, etc.).
# This is useful because FastAPI uses it to:
#   - Auto-generate the /docs (Swagger) page
#   - Show exactly what JSON format your API expects
#   - Let frontend developers know what data to send

# Think of it like this:
#   - BaseModel = Your blueprint in Python 🐍
#   - JSON Schema = The same blueprint in a universal language 🌍
#   - FastAPI automatically converts BaseModel -> JSON Schema for you!


# ==========================================================
# 3. PYDANTIC MODEL vs PLAIN DICTIONARY (dict)
# ==========================================================

# A Python dict is like a blank notebook — you can write ANYTHING, no one checks.
# A Pydantic BaseModel is like a GOVERNMENT FORM — strict rules, no mistakes!

# Example with dict:
#   user_dict = {"name": "John", "age": "abc"}   # No error! But age is wrong.
#   print(user_dict["age"] + 5)   # ERROR! Can't add string + number
#   # You only find out when your code CRASHES later!

# Example with Pydantic:
#   class User(BaseModel):
#       name: str
#       age: int
#   user = User(name="John", age="abc")   # ERROR IMMEDIATELY!
#   # Pydantic tells you right away: "age is not a valid integer"

# Comparison:
# | Feature                | dict                    | Pydantic BaseModel       |
# |------------------------|-------------------------|--------------------------|
# | Type validation        | None (manual)           | Automatic on creation    |
# | Type conversion        | None                    | Yes ("123" -> 123)      |
# | Error messages         | None (crash randomly)   | Detailed & clear errors  |
# | IDE autocomplete       | Poor (keys are strings) | Excellent (real fields)  |
# | Nested objects         | Manual handling         | Automatic (nest models)  |
# | Convert to JSON        | json.dumps() manually   | .model_dump_json() easy  |
# | Best for               | Quick, temporary data   | Production APIs & logic  |

# RULE OF THUMB:
#   - Use dict when: throwing random data together (like cache, temp storage)
#   - Use Pydantic when: data comes from API, database, or needs validation


# ==========================================================
# 4. HOW PYDANTIC VALIDATION WORKS (STEP BY STEP)
# ==========================================================

# When you create a Pydantic object, here's what happens INSIDE:

# Step 1 - Define rules:
#   class User(BaseModel):
#       name: str
#       age: int

# Step 2 - Pass data:
#   user = User(name="Alice", age="25")
#   # Notice: age is "25" (string), not 25 (int)!

# Step 3 - Pydantic checks & converts:
#   name "Alice" -> is it str? YES -> keep it ✓
#   age "25" -> is it int? NO, but can I convert? YES, "25" -> 25 ✓
#   Result: User(name="Alice", age=25)  # age is now int!

# Step 4 - If conversion fails:
#   user = User(name="Alice", age="hello")
#   age "hello" -> is it int? NO. Can I convert? NO, "hello" not a number.
#   ERROR! Pydantic raises ValidationError:
#   "1 validation error for User
#    age -> Input should be a valid integer, unable to parse string as integer"

# Step 5 - Nested objects (our file's topic):
#   If User has address: Address (another BaseModel), Pydantic will:
#   - First validate the inner Address object
#   - Then validate the outer User object
#   - ALL automatic, no extra code needed!

# KEY POINT: Validation fails FAST and LOUD — you catch bugs early, not at 3 AM!


# ==========================================================
# 5. WHAT IS A NESTED MODEL? (DETAILED)
# ==========================================================

# A nested model = One BaseModel INSIDE another BaseModel.
# Think of it like a form inside a form.

# Simple example (no nesting):
#   class User(BaseModel):
#       name: str        # Just simple fields
#       age: int
#   JSON: {"name": "John", "age": 25}

# With nesting (this file):
#   class Address(BaseModel):      # Separate blueprint for Address
#       city: str
#       state: str
#   class User(BaseModel):
#       name: str
#       address: Address            # <-- NESTING! Address model inside User
#   JSON: {"name": "John", "address": {"city": "NYC", "state": "NY"}}
#               ^ simple field         ^ nested object!

# Nesting is used when data has STRUCTURE inside it.
# Real examples: Order -> contains ShippingAddress, Employee -> contains Department

# You can nest MULTIPLE levels deep:
#   Company -> has CEO (User) -> CEO has Address -> Address has coordinates (LatLng)
#   That's 3 levels of nesting! All validated automatically.

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


# ==========================================================
# 1. DEFINE A MODEL INSIDE ANOTHER MODEL (NESTED MODEL)
# ==========================================================

# First, let's define an Address blueprint.
# Think of this like a form with fields: city, state, country, zip_code.
# Each field has a TYPE (like str = text, int = number).
class Address(BaseModel):
    city: str          # Text: the city name (e.g., "New York")
    state: str         # Text: the state name (e.g., "NY")
    country: str       # Text: the country name (e.g., "USA")
    zip_code: int      # Number: the ZIP code (e.g., 10001)


# Now, let's define a User blueprint.
# This User has a name, an age, AND an address (which uses our Address model above)!
# This is called "nesting" — one model inside another.
class User(BaseModel):
    name: str             # Text: user's name (e.g., "John")
    age: int              # Number: user's age (e.g., 25)
    address: Address      # ---> This uses the Address model we defined above!

    # So when someone sends us user data, it should look like this:
    # {
    #   "name": "John",
    #   "age": 25,
    #   "address": {
    #     "city": "New York",
    #     "state": "NY",
    #     "country": "USA",
    #     "zip_code": 10001
    #   }
    # }


# ==========================================================
# 2. CREATE A POST ROUTE THAT ACCEPTS THIS DATA
# ==========================================================

# This is an API endpoint (a URL that the client can call).
# When someone sends a POST request to "/create_user" with JSON data:
# FastAPI will:
#   1. Read the JSON from the request body.
#   2. Check if it matches the User blueprint (validates it).
#   3. Convert it into a User object that we can use in Python.
@app.post("/create_user")
def create_user(user: User):  # "user: User" tells FastAPI to expect a User-shaped JSON
    # We just return the data back to the client.
    # In a real app, you'd save this to a database!
    return user


# ==========================================================
# HOW TO TEST THIS API
# ==========================================================
# Start the server (from the project root):
#    poetry run uvicorn main:app --reload
#
# Then open your browser and go to: http://127.0.0.1:8000/docs
# 3. Click on the POST /create_user endpoint.
# 4. Click "Try it out" and send this JSON:
#    {
#      "name": "Alice",
#      "age": 30,
#      "address": {
#        "city": "Mumbai",
#        "state": "Maharashtra",
#        "country": "India",
#        "zip_code": 400001
#      }
#    }
# 5. You'll get back the same JSON — validation passed!


# ==========================================================
# WHAT IF YOU SEND WRONG DATA?
# ==========================================================
# Try sending:
#   {"name": "Bob", "age": "twenty", "address": {...}}
# FastAPI will automatically reject it and show an error message.
# It will say: "age should be a valid integer" — very helpful!


# ==========================================================
# REAL-LIFE USE CASES OF NESTED MODELS
# ==========================================================

# 1. E-COMMERCE ORDER (Amazon / Flipkart)
#    Order contains: customer info + list of products + shipping address
#    Order model has Address model + Product model nested inside it.

# 2. EMPLOYEE DATABASE (Company HR System)
#    Employee has: personal details + department + manager info
#    Employee model has Department model + Manager model nested inside it.

# 3. HOSPITAL PATIENT RECORD
#    Patient has: personal info + medical history + insurance details
#    Each of those can be a separate Pydantic model nested inside Patient.

# 4. SOCIAL MEDIA POST (Instagram / Twitter)
#    Post has: content + author info + comments list + likes count
#    Post model has User model (author) + Comment model nested inside it.


# ==========================================================
# SIMPLE SUMMARY FOR BEGINNERS
# ==========================================================

# - BaseModel = A BLUEPRINT for your data. You define what fields to expect.
# - Each field has a TYPE (str, int, float, etc.) — this is automatic validation.
# - Nested Model = A model INSIDE another model (like Address inside User).
# - FastAPI reads JSON -> validates it with Pydantic -> gives you a Python object.
# - If data is invalid, FastAPI returns a 422 error with details.
# - No manual if/else checks needed — Pydantic does all the validation!


# ==========================================================
# MNC INTERVIEW QUESTIONS & ANSWERS
# ==========================================================

# Q1. What is a Pydantic model? How is it different from a regular Python class?
# A:  A Pydantic model is a class that inherits from BaseModel.
#     Difference:
#       - Regular class: Just stores data, no validation.
#       - Pydantic model: Automatically VALIDATES data types when you create an object.
#         Example: If age is declared as int and you pass "abc", Pydantic throws an error.
#     It saves you from writing 100s of if/else checks manually!

# Q2. What is a nested Pydantic model? Give a real example.
# A:  Nested model = One Pydantic model INSIDE another model.
#     Example: A User has an Address. Address is a separate model with its own fields.
#     {
#       "name": "John",
#       "address": {
#         "city": "NYC",
#         "state": "NY",
#         "country": "USA",
#         "zip_code": 10001
#       }
#     }
#     The JSON has an "address" object INSIDE the main object — that's nesting.

# Q3. How does FastAPI validate nested JSON data automatically?
# A:  When you write `def create_user(user: User)`, FastAPI sees that User has
#     an 'address' field of type Address (another BaseModel). So it:
#     1. Takes the JSON from the request body.
#     2. Converts the outer JSON into a User object.
#     3. Converts the inner "address" JSON into an Address object.
#     4. If any field is wrong type or missing, it returns a 422 error immediately.
#     All of this is AUTOMATIC — you write ZERO validation code!

# Q4. What happens if you send incomplete or wrong data to a nested model?
# A:  FastAPI + Pydantic returns a detailed 422 validation error.
#     Example errors:
#       - Missing "city" field: "field required"
#       - "age" sent as text: "value is not a valid integer"
#       - "zip_code" sent as string: "value is not a valid integer"
#     The error message tells you EXACTLY which field failed and why.
#     This is 10x better than writing manual if/else checks!

# Q5. Can you have multiple levels of nesting? (Model inside model inside model)
# A:  Yes! You can nest as deep as you want.
#     Example:
#       class Company(BaseModel):
#           name: str
#           address: Address        # Level 1 nesting
#           ceo: User               # Level 1 nesting (User has Address inside it = Level 2!)
#     This is very common in real apps like:
#       - E-commerce: Order -> contains Products + ShippingAddress + PaymentInfo
#       - Hospital: PatientRecord -> contains PersonalInfo + MedicalHistory + Insurance