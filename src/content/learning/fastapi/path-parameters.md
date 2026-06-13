# Path Parameters

```python
# ==========================================================
# FASTAPI STUDY GUIDE: 02. PATH PARAMETERS
# ==========================================================

# --- WHAT ARE PATH PARAMETERS? ---
# Path parameters are dynamic parts of the URL.
# Instead of hardcoding every URL like /items/1, /items/2, etc.,
# you can use curly brackets to capture values: /items/{item_id}.
#
# FastAPI will automatically:
# 1. Parse the parameter from the URL path.
# 2. Convert (cast) it to the Python type you specify (like `int`, `str`, `float`).
# 3. Validate it (if it's not the right type, it returns a clear error to the client).

from fastapi import FastAPI
import uvicorn

app = FastAPI(title="FastAPI: Path Parameters")

# Let's create some dummy data to play with
ITEMS_DATABASE = {
    1: {"name": "Laptop", "price": 899.99},
    2: {"name": "Smartphone", "price": 499.99},
    3: {"name": "Wireless Headphones", "price": 149.99}
}

# ==========================================================
# 1. BASIC PATH PARAMETER WITH TYPE HINTING
# ==========================================================
# By declaring `item_id: int` in the function arguments, FastAPI does:
# - Casting: When you visit `/items/2`, the string "2" is converted to Python integer `2`.
# - Validation: If you visit `/items/keyboard`, FastAPI will see that "keyboard" cannot
#   be converted to an integer, and will return an automatic HTTP 422 error!
@app.get("/items/{item_id}")
async def get_item(item_id: int):
    # Search database for the item_id
    item = ITEMS_DATABASE.get(item_id)
    
    if item is None:
        return {"error": f"Item with ID {item_id} not found."}
        
    return {
        "item_id": item_id,
        "details": item
    }


# ==========================================================
# 2. PATH MATCHING ORDER (CRITICAL PITFALL)
# ==========================================================
# FastAPI matches routes from TOP TO BOTTOM in the file.
# Imagine we want a special route for our featured item at "/items/featured".
#
# Rule: Hardcoded paths must ALWAYS go BEFORE dynamic paths!
# If we put "/items/featured" AFTER "/items/{item_id}", FastAPI will see "featured"
# as the `item_id`, try to parse it as an integer, and fail with a validation error!

# --- CORRECT ORDER ---
# First: The specific path "/items/featured"
@app.get("/items/featured")
async def get_featured_item():
    return {
        "message": "This is our featured item of the week!",
        "featured_item": ITEMS_DATABASE[1]
    }

# Second: The generic path "/items/{item_id}" (already declared above at line 34)
# Note: If we had placed the `/items/featured` route below the generic one,
# visiting `/items/featured` would result in a "422 Unprocessable Entity" error.


# ==========================================================
# 3. DYNAMIC DATA TYPES (e.g., File Paths)
# ==========================================================
# What if you want a path parameter to contain a whole file path (like "images/avatars/me.png")?
# You can use a path converter by adding `:path` inside the curly braces.
@app.get("/files/{file_path:path}")
async def read_file(file_path: str):
    return {
        "file_path_received": file_path,
        "action": f"Reading contents of file at location: {file_path}"
    }


# ----------------------------------------------------------
# HOW TO RUN THIS FILE
# ----------------------------------------------------------
# Open your terminal in this folder and run:
#   python 02_path_parameters.py
# OR
#   uvicorn 02_path_parameters:app --reload
#
# Then open: http://127.0.0.1:8000/docs
# ----------------------------------------------------------
if __name__ == "__main__":
    uvicorn.run("02_path_parameters:app", host="127.0.0.1", port=8000, reload=True)


# --- QUICK SUMMARY FOR RETESTING ---
# 1. Run this file: `python 02_path_parameters.py`
# 2. Go to: http://127.0.0.1:8000/docs
# 3. Try out `/items/1` (works!)
# 4. Try out `/items/featured` (works!)
# 5. Try out `/items/hello` (returns automatic validation error - standard HTTP 422)
# 6. Try out `/files/docs/notes/class1.pdf` (works, captures the whole path!)


# ==========================================================
# REAL-LIFE USE CASES
# ==========================================================

# 1. USER PROFILE PAGE (like LinkedIn / Twitter)
#    - GET /users/{username} → fetch profile of user "ritesh_sinha"
#    - LinkedIn uses: GET /in/{publicIdentifier} to display any user's public profile.
#    - The path param is the username. If user not found → return 404.

# 2. PRODUCT DETAIL PAGE (like Amazon / Flipkart)
#    - GET /products/{product_id} → fetch all details of product ID 123456.
#    - Each product URL has a unique ID embedded in it:
#      https://amazon.in/dp/B09G3HRMVB → B09G3HRMVB is the path parameter!

# 3. ORDER TRACKING (like Swiggy / Zomato)
#    - GET /orders/{order_id}/status → returns live status of order 5001.
#    - Nested path params are very common in REST APIs.

# 4. FILE SERVING (like Google Drive / Dropbox)
#    - GET /files/{file_path:path} → can serve /docs/2024/report.pdf directly.
#    - The `:path` converter is used when the param itself contains slashes.


# ==========================================================
# MNC INTERVIEW QUESTIONS & ANSWERS
# ==========================================================

# Q1. What are path parameters in FastAPI? Give a real-life example.
# A:  Path parameters are dynamic parts of the URL. FastAPI captures them using `{variable_name}`.
#     Real-life: GET /users/42 → 42 is the path param. Used to identify a SPECIFIC resource.
#     FastAPI uses type hints to automatically VALIDATE and CONVERT the captured value.

# Q2. What happens when you access /items/abc in a route defined as /items/{item_id} where item_id: int?
# A:  FastAPI returns a 422 Unprocessable Entity error.
#     The error message is a clear JSON explaining:
#       {"detail": [{"loc": ["path", "item_id"], "msg": "value is not a valid integer"}]}
#     You don't write any of this validation code — FastAPI does it automatically!

# Q3. Why must static routes be defined BEFORE dynamic routes?
# A:  FastAPI matches routes TOP TO BOTTOM in the file.
#     If /items/{item_id} is defined before /items/featured:
#       → FastAPI treats "featured" as item_id, tries to convert to int, FAILS.
#     If /items/featured is defined BEFORE /items/{item_id}:
#       → FastAPI matches "featured" first (exact match), returns correct result.
#     RULE: Specific (hardcoded) routes MUST come before generic (dynamic) routes.

# Q4. What is the difference between `item_id: int` and `item_id: str` as a path param?
# A:  `item_id: int` → FastAPI validates the value is a valid integer. /items/abc → 422 error.
#     `item_id: str` → FastAPI accepts anything as a string. /items/abc → works fine.
#     Always use the MOST RESTRICTIVE type you need — this prevents bugs early.

# Q5. What does {file_path:path} mean in FastAPI routes?
# A:  By default, path parameters don't match forward slashes (/).
#     Adding `:path` tells FastAPI to capture everything including slashes.
#     Example: /files/{file_path:path}
#       → GET /files/docs/notes/class1.pdf → file_path = "docs/notes/class1.pdf"
#     Without `:path`, FastAPI would only capture "docs" and treat the rest as a separate route.

```
