# ==========================================================
# FASTAPI YT SERIES: 03. REQUEST BODY
#     - Sending Data from Client to Server
#     - Pydantic BaseModel
#     - Automatic Data Validation
# ==========================================================

# --- WHY DO WE NEED A REQUEST BODY? ---
# In previous lessons (Path & Query Params), we only sent small amounts of data in the URL.
# But what if we need to send a lot of data? Like:
#   - User Registration (name, email, password, address)
#   - Creating a Post (title, content, tags)
#
# We cannot put all this data in the URL! It is insecure and messy.
# Instead, we send data inside the "Request Body", usually as JSON format.
#
# In FastAPI, we use "Pydantic" (a powerful validation library) to define what our
# Request Body should look like. We do this by creating a class that inherits from BaseModel.

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(
    title="FastAPI YT - Request Body",
    description="Understanding how to send JSON data to the API using Pydantic Models",
    version="1.0.0"
)


# ==========================================================
# 1. DEFINING THE PYDANTIC MODEL
# ==========================================================
# Here we define the shape of the data we expect from the client.
# This automatically gives us:
#   1. Data Validation (if age is not a number, it rejects the request)
#   2. Data Conversion (JSON -> Python Object)
#   3. Editor Support (autocompletion for user.name, user.age)
#   4. Automatic API Documentation
class User(BaseModel):
    name: str
    age: int


# ==========================================================
# 2. POST REQUEST WITH REQUEST BODY
# ==========================================================
# Notice we use `@app.post` instead of `@app.get`.
# GET is for fetching data. POST is for creating/sending data.
#
# Real-Life Use Case:
#   - Submitting a signup form
#   - Placing an order
#
# MNC Example:
#   Amazon checkout: POST /checkout with body {"cart_id": 123, "payment_method": "UPI"}
@app.post("/create-user")
def create_user(user: User):
    # 'user' is already a fully validated Python object here!
    # You can access attributes like: user.name, user.age

    # In real apps, you'd save this to a database: db.add(user)
    return {
        "message": "User Created Successfully",
        "data": user
    }


# ----------------------------------------------------------
# HOW TO RUN THIS FILE
# ----------------------------------------------------------
# Open your terminal in this folder (03-request-body) and run:
#   uvicorn main:app --reload
#
# Then test in your browser or Swagger UI at http://localhost:8000/docs
#
# Try sending a POST request to /create-user with this JSON body:
# {
#   "name": "Ritesh",
#   "age": 25
# }
#
# Also try sending invalid data (like "age": "twenty") to see FastAPI's automatic validation!
# ----------------------------------------------------------


# ==========================================================
# MNC INTERVIEW QUESTIONS & ANSWERS
# ==========================================================

# Q1. What is the difference between GET and POST methods?
# A:  GET  → Reads data from server.  Data travels in the URL.         Example: GET /users/5
#     POST → Sends data to the server. Data travels in the Request Body. Example: POST /create-user

# Q2. Why do we use Pydantic BaseModel in FastAPI?
# A:  To define the SHAPE of the data we expect. It gives us 4 things for free:
#       1. Validation  → Rejects wrong data types automatically
#       2. Parsing     → Converts JSON into a Python object
#       3. Autocompletion → VS Code knows the fields (user.name, user.age)
#       4. Swagger Docs  → FastAPI reads the model and builds /docs automatically

# Q3. What happens if a client sends invalid JSON data in the request body?
# A:  FastAPI returns a 422 Unprocessable Entity error automatically.
#     It also tells the client EXACTLY which field is wrong and why.
#     Your code never crashes — FastAPI handles it before it even reaches your function.

# Q4. What is a Request Body?
# A:  Think of it like a "parcel" the client sends to your server.
#     Unlike URL params (which are visible in the address bar),
#     the request body is hidden inside the HTTP message — like data inside an envelope.
#     Used for: Passwords, Long forms, File uploads, Order details etc.

# Q5. What are the common use cases of a POST request?
# A:  POST = "I am sending you something new, please save it."
#       - User Registration (sending name, email, password)
#       - Creating a product listing
#       - Placing an order / checkout
#       - Uploading a file or image

# Q6. What is JSON format?
# A:  JSON = JavaScript Object Notation.
#     It is the UNIVERSAL language that frontend and backend use to talk to each other.
#     It looks exactly like a Python dictionary but it is just TEXT (a string).
#     Python Dict  →  {"name": "Ritesh", "age": 25}  (lives in memory)
#     JSON         →  '{"name": "Ritesh", "age": 25}' (travels over the internet as text)
#     FastAPI automatically converts JSON text → Python object for you.

# Q7. What is the difference between a Pydantic Model and a Python Dictionary?
# A:  Simple way to remember — Pydantic is a SMART dict, plain dict is a DUMB dict.
#
#     | #  | Feature            | Pydantic BaseModel                        | Python Dictionary                      |
#     |----|--------------------|--------------------------------------------|----------------------------------------|
#     | 1  | Structure          | STRUCTURED — fixed fields & types         | FLEXIBLE — any keys, any values        |
#     | 2  | Validation         | AUTO — rejects wrong types (422 Error)    | NONE — accepts anything, no checks     |
#     | 3  | Error Handling     | AUTO — FastAPI handles errors for you     | MANUAL — you write if/else checks      |
#     | 4  | Type Conversion    | "25" → 25 auto-fixed for you              | "25" stays string, you fix it manually |
#     | 5  | Attribute Access   | user.name  (clean dot notation)           | user["name"]  (bracket, typo-prone)    |
#     | 6  | VS Code Autocomplete| Suggests user.name, user.age             | No suggestions, VS Code is blind       |
#     | 7  | Swagger UI (/docs) | Full schema: field names + types shown    | Empty box {} shown — useless           |
#
#     EASY TO REMEMBER:
#       Dict     = Flexible  but DANGEROUS  (no rules, no checks, you handle everything)
#       Pydantic = Structured but SAFE      (strict rules, auto checks, FastAPI handles errors)
#
#     NOTE on Point 7: Both DO generate Swagger UI, but with Dict it shows empty {}.
#                      Pydantic makes Swagger actually USEFUL with field names & types.
