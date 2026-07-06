# ==========================================================
# FASTAPI STUDY GUIDE: 04. REQUEST BODY & PYDANTIC
# ==========================================================

# --- WHAT IS A REQUEST BODY? ---
# A request body is data sent by the client (like a browser or frontend app) 
# to your API in the HTTP request payload (usually as JSON).
# Unlike query parameters (which go in the URL), the request body is sent inside the request.
# We use a request body when we want to CREATE or UPDATE resources (via POST, PUT, PATCH).

# --- WHAT IS PYDANTIC? ---
# Pydantic is a powerful library used by FastAPI for data parsing and validation.
# To define a request body in FastAPI:
# 1. Import `BaseModel` from `pydantic`.
# 2. Create a class that inherits from `BaseModel`.
# 3. Define the fields and their types (using Python type hints).

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import Union, List
import uvicorn

app = FastAPI(title="FastAPI: Request Body & Pydantic")

# Mock database
PRODUCTS_DATABASE = {}

# ==========================================================
# 1. DEFINING A PYDANTIC MODEL
# ==========================================================
# This class defines the structure (schema) of the JSON we expect from the client.
# We can use Pydantic's `Field` to add validation rules (like min_length, gt, lt).
class Product(BaseModel):
    name: str = Field(..., min_length=2, description="Name of the product")
    price: float = Field(..., gt=0, description="Price must be greater than zero")
    description: Union[str, None] = Field(default=None, description="Optional description of the product")
    tax: Union[float, None] = 0.0  # Default value if not provided
    tags: List[str] = []           # Default to an empty list of strings


# ==========================================================
# 2. POST ROUTE WITH REQUEST BODY
# ==========================================================
# By declaring `product: Product` in the arguments, FastAPI will:
# 1. Read the JSON from the request body.
# 2. Validate it against the `Product` model.
# 3. Convert it into a Pydantic object that you can access (like `product.name`, `product.price`).
@app.post("/products/{product_id}")
async def create_product(product_id: int, product: Product):
    if product_id in PRODUCTS_DATABASE:
        raise HTTPException(status_code=400, detail="Product ID already exists.")
        
    # Calculate price including tax
    total_price = product.price + (product.tax or 0.0)
    
    # Store it in our mock database (converting Pydantic object to a dictionary)
    PRODUCTS_DATABASE[product_id] = product.model_dump()
    
    return {
        "message": "Product created successfully!",
        "product_id": product_id,
        "product_data": PRODUCTS_DATABASE[product_id],
        "total_price_calculated": total_price
    }


# ==========================================================
# 3. MIXING PATH, QUERY, AND REQUEST BODY
# ==========================================================
# FastAPI is smart enough to know which parameter is what:
# - If parameter is declared in the path (like `{product_id}`), it's a PATH parameter.
# - If it's a simple type (like `int`, `str`) NOT in the path, it's a QUERY parameter.
# - If it's a subclass of `BaseModel`, it's a REQUEST BODY.
#
# Try this: Update an existing product, and also accept a query parameter `notify`
@app.put("/products/{product_id}")
async def update_product(
    product_id: int,          # PATH Parameter
    product: Product,         # REQUEST BODY (Pydantic model)
    notify: bool = False      # QUERY Parameter (Defaults to False)
):
    if product_id not in PRODUCTS_DATABASE:
        raise HTTPException(status_code=404, detail="Product not found.")
        
    PRODUCTS_DATABASE[product_id] = product.model_dump()
    
    response = {
        "message": "Product updated successfully!",
        "product_id": product_id,
        "updated_data": PRODUCTS_DATABASE[product_id]
    }
    
    if notify:
        response["notification"] = "Users have been notified about the product update!"
        
    return response


@app.get("/products")
async def list_products():
    return PRODUCTS_DATABASE


# ----------------------------------------------------------
# HOW TO RUN THIS FILE
# ----------------------------------------------------------
if __name__ == "__main__":
    uvicorn.run("04_request_body_pydantic:app", host="127.0.0.1", port=8000, reload=True)


# --- QUICK SUMMARY FOR RETESTING ---
# 1. Run this file: `python 04_request_body_pydantic.py`
# 2. Go to: http://localhost:8000/docs
# 3. Look at the `/products/{product_id}` POST endpoint in Swagger. It automatically 
#    shows the JSON body schema required to make the request!
# 4. Try sending an invalid body (e.g. price: -10.0 or a name with only 1 letter). 
#    FastAPI will automatically block it and return a detailed validation error.


# ==========================================================
# REAL-LIFE USE CASES
# ==========================================================

# 1. USER REGISTRATION (like any app signup)
#    - POST /register with body: {name, email, password, phone}
#    - Pydantic validates email format, min-length for password, etc.
#    - Without Pydantic: you'd write 20 lines of if/else checks. With Pydantic: 0 lines!

# 2. PRODUCT CREATION (like Seller Dashboard on Amazon/Flipkart)
#    - POST /products with body: {name, price, category, description, stock_count}
#    - Pydantic ensures price > 0, stock_count >= 0, name is not empty, etc.
#    - Seller portal shows friendly errors if any field is invalid.

# 3. BOOKING / RESERVATION (like MakeMyTrip / OYO)
#    - POST /bookings with body: {hotel_id, check_in, check_out, guests, room_type}
#    - Pydantic validates check_in < check_out, guests > 0, etc.
#    - Any invalid booking request is rejected BEFORE touching the database.

# 4. LOAN APPLICATION (like HDFC Bank / Bajaj Finance)
#    - POST /loan/apply with body: {name, pan_number, income, loan_amount, tenure}
#    - Pydantic's Field() validators check patterns (like PAN format), value ranges, etc.
#    - The validated data is then passed to the credit scoring engine.


# ==========================================================
# MNC INTERVIEW QUESTIONS & ANSWERS
# ==========================================================

# Q1. What is Pydantic and why does FastAPI use it?
# A:  Pydantic is a data validation library that uses Python type hints to define data schemas.
#     FastAPI uses Pydantic for:
#       1. REQUEST BODY validation: Rejects invalid data before it reaches your logic.
#       2. RESPONSE MODEL filtering: Strips sensitive fields before sending to client.
#       3. SETTINGS management: Loads environment variables with validation.
#     Pydantic v2 (which FastAPI now uses by default) is written in Rust — extremely fast.

# Q2. What is the difference between a Pydantic model and a SQLAlchemy model?
# A:  Pydantic Model (BaseModel):
#       - Used for INPUT validation (request body) and OUTPUT serialization (response).
#       - It's about DATA SHAPE — what the JSON looks like.
#       - Lives in Python memory only.
#     SQLAlchemy Model (DeclarativeBase):
#       - Used to define DATABASE TABLE structure.
#       - Maps Python class to a database table and its columns.
#       - Used to perform actual DB queries (SELECT, INSERT, etc.)
#     In real apps: You have BOTH. Pydantic for API layer, SQLAlchemy for DB layer.

# Q3. What is the `Field` class in Pydantic? Give examples.
# A:  `Field` adds extra rules and metadata to a Pydantic model attribute.
#     Common uses:
#       price: float = Field(..., gt=0, description="Must be greater than zero")
#       name: str = Field(..., min_length=2, max_length=100)
#       age: int = Field(default=18, ge=18, le=100)  # ge=greater-equal, le=less-equal
#       email: str = Field(..., pattern=r'^[\w.-]+@[\w.-]+\.\w+$')  # regex validation
#     `...` (Ellipsis) as the first argument means the field is REQUIRED.

# Q4. How does FastAPI know which parameter is a path param, query param, or request body?
# A:  FastAPI uses a clear priority system:
#       1. If name is in the URL path (e.g., {product_id}) → PATH parameter.
#       2. If it's a simple type (str, int, float, bool) NOT in path → QUERY parameter.
#       3. If it's a subclass of Pydantic's BaseModel → REQUEST BODY.
#     This is all automatic — no annotations needed beyond type hints!

# Q5. What does `model_dump()` do in Pydantic v2?
# A:  `model_dump()` converts a Pydantic model instance into a plain Python dictionary.
#     Used when you need to:
#       - Store data in a database (pass dict to SQLAlchemy)
#       - Serialize data to JSON manually
#       - Log or debug the request body
#     In Pydantic v1, this was called `.dict()`. In Pydantic v2, it's `.model_dump()`.
