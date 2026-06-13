# ==========================================================
# FASTAPI YT SERIES: 02. DYNAMIC ROUTES
#     - Path Parameters
#     - Query Parameters
#     - Optional & Default Query Params
#     - Multiple Query + Path Params Combined
# ==========================================================

# --- WHY DO WE NEED DYNAMIC ROUTES? ---
# Static routes (like /about, /users) always return the same data.
# But in real apps, we need to fetch SPECIFIC data.
#
# For example:
#   - GET /users/5         → fetch user whose ID is 5
#   - GET /products?limit=10&offset=20  → get 10 products, skip first 20
#   - GET /search?q=iphone → search for "iphone"
#
# FastAPI handles this in TWO ways:
#   1. PATH PARAMETERS   → Part of the URL itself   → /users/{id}
#   2. QUERY PARAMETERS  → After the "?" in the URL → /users?name=ritesh

from fastapi import FastAPI

app = FastAPI(
    title="FastAPI YT - Dynamic Routes",
    description="Path Parameters and Query Parameters explained simply",
    version="1.0.0"
)


# ==========================================================
# 1. PATH PARAMETERS
# ==========================================================
# Path parameters are variables INSIDE the URL path.
# You wrap the variable name in curly braces: {id}
# FastAPI captures whatever value is placed there in the URL.
#
# Real-Life Use Case:
#   - GET /users/42       → Fetch profile of user with ID 42
#   - GET /orders/99      → Fetch order number 99 details
#   - GET /products/123   → Fetch product 123 info
#
# MNC Example:
#   Swiggy uses GET /restaurants/{restaurant_id} to fetch
#   details of a specific restaurant based on its unique ID.
#
# NOTE ABOUT TYPE HINTS:
#   def get_users(id)        → id is treated as a STRING by default
#   def get_users(id: int)   → FastAPI validates id MUST be an integer
#   def get_users(id: str)   → FastAPI treats id as a string
#   def get_users(id: float) → FastAPI validates id MUST be a float
#
#   If someone passes a wrong type (e.g., /users/abc when int expected),
#   FastAPI automatically returns a 422 Unprocessable Entity error!
@app.get("/users/{id}")
def get_user_by_id(id: int):
    # In real apps, you'd query the database here using: db.query(User).filter(User.id == id)
    return {
        "user_id": id,
        "message": f"Fetching user with ID {id}"
    }


# ==========================================================
# 2. QUERY PARAMETERS (Basic)
# ==========================================================
# Query parameters appear AFTER the "?" in the URL.
# They are key=value pairs separated by "&".
#
# URL Structure:
#   http://localhost:8000/username?name=ritesh
#                                 ^^^^^^^^^^^^^
#                                 This is the query parameter
#
# In FastAPI: if the function argument is NOT in the URL path → it's a query param.
#
# Real-Life Use Case:
#   - Google Search: https://google.com/search?q=fastapi
#   - YouTube Filter: https://youtube.com/results?search_query=python
#   - LinkedIn Search: GET /people?keyword=developer
#
# MNC Example:
#   Flipkart's search: GET /search?q=laptop&brand=HP&sort=price_asc
@app.get("/username")
def get_user_by_name(name: str):
    # name is automatically read from ?name=... in the URL
    return {
        "name": name,
        "message": f"Hello, {name}! Your profile was found."
    }


# ==========================================================
# 3. OPTIONAL QUERY PARAMETERS
# ==========================================================
# Sometimes a query parameter should be optional.
# If the user doesn't provide it → we return all results.
# If the user provides it → we filter/use that value.
#
# To make a param optional: use `name: str = None`
# (The default value is None, meaning "not provided")
#
# Real-Life Use Case:
#   - GET /products          → returns all products
#   - GET /products?category=electronics → returns only electronics
#
# MNC Example:
#   Amazon: GET /search → show all products
#           GET /search?q=headphones → show only headphone results
@app.get("/user")
def get_user_optional(name: str = None):
    if name is None:
        return {"message": "No name provided. Showing all users."}
    return {
        "name": name,
        "message": f"Searching for user: {name}"
    }


# ==========================================================
# 4. DEFAULT VALUE IN QUERY PARAMETERS
# ==========================================================
# Sometimes we want a query parameter to have a sensible default.
# If the user doesn't send it → use the default.
# If the user sends it → override the default with their value.
#
# This is SAME as optional params but with a meaningful default.
#
# Real-Life Use Case:
#   - Pagination: limit=10 is a sensible default (show 10 items per page)
#   - GET /products?limit=5  → Show only 5 products
#   - GET /products           → Show default 10 products (limit=10)
#
# MNC Example:
#   Zomato: GET /restaurants?limit=20 → top 20 restaurants near you.
#   Default limit=20 is used if not provided.
@app.get("/products")
def get_products(limit: int = 10):
    # In real code: products = db.query(Product).limit(limit).all()
    return {
        "limit": limit,
        "message": f"Returning top {limit} products. (Change with ?limit=N)"
    }


# ==========================================================
# 5. MULTIPLE QUERY PARAMETERS
# ==========================================================
# You can have multiple query parameters in a single route.
# All of them appear after "?" and are separated by "&" in the URL.
#
# URL Example:
#   http://localhost:8000/items?name=phone&price=3000
#                              ^^^^^^^^^^^^^^^^^^^^^^^^
#                              Two query params: name and price
#
# Real-Life Use Case:
#   - E-Commerce Filter: GET /items?category=laptop&brand=Dell&max_price=50000
#   - Job Search: GET /jobs?title=developer&location=bangalore&experience=2
#
# MNC Example (Naukri.com):
#   GET /jobs?title=backend+developer&location=pune&experience=3
@app.get("/items")
def get_items(name: str = None, price: int = 0):
    return {
        "name": name,
        "price": price,
        "message": f"Searching for '{name}' with max price {price}"
    }


# ==========================================================
# 6. PATH PARAMETER + MULTIPLE QUERY PARAMETERS COMBINED
# ==========================================================
# The MOST COMMON PATTERN in real APIs!
# Path param → identifies WHAT resource (which product)
# Query params → HOW to fetch it (pagination, filters)
#
# URL Example:
#   http://localhost:8000/products/5?limit=10&offset=0
#   - Path param:  id=5       → fetch product with ID 5
#   - Query param: limit=10   → return 10 results per page
#   - Query param: offset=0   → start from the beginning (page 1)
#
# What is Pagination?
#   Imagine you have 1000 products in a database.
#   You don't want to return all 1000 at once (slow + heavy).
#   So you return 10 at a time using limit + offset:
#     Page 1: offset=0,  limit=10  → items 1-10
#     Page 2: offset=10, limit=10  → items 11-20
#     Page 3: offset=20, limit=10  → items 21-30
#
# Real-Life Use Case:
#   - Instagram: GET /users/42/posts?limit=12&offset=0  → First 12 posts of user 42
#   - GitHub API: GET /repos/python/cpython/commits?per_page=30&page=2
#   - Swiggy: GET /restaurants/7/menu?limit=20&offset=40
@app.get("/products/{id}")
def get_product_with_pagination(id: int, limit: int = 10, offset: int = 0):
    # In real code:
    # products = db.query(Product).filter(Product.id == id).offset(offset).limit(limit).all()
    return {
        "product_id": id,
        "limit": limit,
        "offset": offset,
        "page_info": f"Showing {limit} items starting from position {offset} for product {id}"
    }


# ----------------------------------------------------------
# HOW TO RUN THIS FILE
# ----------------------------------------------------------
# Open your terminal in this folder (02-dynamic-routes) and run:
#   uvicorn main:app --reload
#
# Then test in your browser or Swagger UI at http://127.0.0.1:8000/docs:
#
#   Path Parameter:
#     http://127.0.0.1:8000/users/3
#     http://127.0.0.1:8000/users/abc  ← This will give a 422 error (int expected!)
#
#   Query Parameters:
#     http://127.0.0.1:8000/username?name=ritesh
#     http://127.0.0.1:8000/user          (optional - no name)
#     http://127.0.0.1:8000/user?name=bob
#
#   Default Values:
#     http://127.0.0.1:8000/products          → limit=10 (default)
#     http://127.0.0.1:8000/products?limit=5  → limit=5
#
#   Multiple Query Params:
#     http://127.0.0.1:8000/items?name=phone&price=3000
#
#   Combined (Path + Query):
#     http://127.0.0.1:8000/products/5?limit=5&offset=10
# ----------------------------------------------------------


# ==========================================================
# MNC INTERVIEW QUESTIONS & ANSWERS
# ==========================================================

# Q1. What is the difference between a Path Parameter and a Query Parameter?
# A:  PATH PARAMETER → Part of the URL path itself. Used to identify a specific resource.
#       Example: GET /users/42   → {id} in /users/{id} is a path param
#       Used for: Unique identification of a resource (user ID, product ID)
#
#     QUERY PARAMETER → Appears after "?" in the URL. Used for filtering, searching, sorting.
#       Example: GET /products?limit=10&sort=price
#       Used for: Optional filters, pagination, search terms
#
#     MNC Trick Question: "Which is more RESTful for fetching a single resource?"
#     Answer: Path parameter. REST best practice says /users/{id} NOT /users?id=42.

# Q2. How does FastAPI handle type validation for path parameters?
# A:  FastAPI uses Python type hints + Pydantic under the hood.
#     When you write `def get_user(id: int)`, FastAPI:
#       1. Reads the URL value as a string (e.g., "42")
#       2. Tries to convert it to `int` (42)
#       3. If conversion fails → returns 422 Unprocessable Entity automatically
#     You don't need to write any validation logic yourself!

# Q3. What HTTP status code does FastAPI return for type validation errors?
# A:  422 Unprocessable Entity
#     This means: "I understood your request, but the data you sent is invalid."
#     FastAPI also sends a clear JSON error message explaining WHICH field failed and WHY.

# Q4. What is pagination and why is it important?
# A:  Pagination means breaking large data into smaller "pages".
#     Example: Instead of returning 10,000 users at once:
#       GET /users?limit=20&offset=0   → page 1 (users 1-20)
#       GET /users?limit=20&offset=20  → page 2 (users 21-40)
#     Why important?
#       - Reduces server load (don't process 10,000 rows at once)
#       - Reduces bandwidth (don't send massive JSON response)
#       - Improves API response time (faster for the client)
#     In MNCs, returning unbounded data is a common backend bug!

# Q5. How do you combine path and query parameters in FastAPI?
# A:  Simply declare them in the function signature!
#     FastAPI is smart: anything in the URL path (in {}) → path param.
#     Anything NOT in the URL path → query param.
#       @app.get("/products/{id}")
#       def get_products(id: int, limit: int = 10, offset: int = 0):
#         ...
#     Here `id` is a path param. `limit` and `offset` are query params.

# Q6. What happens if you don't provide a required query parameter?
# A:  If the parameter has NO default value → FastAPI returns 422 (field required).
#     If the parameter has a default value → FastAPI uses the default silently.
#     Best practice: Always provide sensible defaults for optional filters.

# Q7. What is the difference between `name: str = None` and `name: Optional[str] = None`?
# A:  They are functionally identical in modern Python (3.10+).
#     `name: str = None` works but is technically a type mismatch (str but default is None).
#     `name: Optional[str] = None` is explicit: "this can be a string OR None".
#     In FastAPI, both work correctly. But `Optional[str]` is better code practice.