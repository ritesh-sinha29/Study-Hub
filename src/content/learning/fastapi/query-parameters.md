# Query Parameters

## FASTAPI STUDY GUIDE: 03. QUERY PARAMETERS

## WHAT ARE QUERY PARAMETERS?

Query parameters are a set of key-value pairs that appear after the "?" in a URL.
For example, in the URL: `http://example.com/items?skip=0&limit=10`
- The parameters are `skip` (value 0) and `limit` (value 10).
- They are commonly used for filtering, sorting, or paginating data.

In FastAPI, any function parameter that is NOT declared in the URL path
is automatically treated as a "query parameter".

```python
from fastapi import FastAPI, Query
from typing import Union
import uvicorn

app = FastAPI(title="FastAPI: Query Parameters")
```

Mock database of users

```python
USERS_DATABASE = [
    {"username": "ritesh_coder", "role": "admin", "active": True},
    {"username": "alice_dev", "role": "developer", "active": True},
    {"username": "bob_tester", "role": "tester", "active": False},
    {"username": "charlie_manager", "role": "manager", "active": True},
]
```

## 1. DEFAULT AND OPTIONAL QUERY PARAMETERS

- `skip` has a default value of `0`.
- `limit` has a default value of `2`.
- If the client doesn't send them, the default values are used.
- If they are sent, they are automatically converted to integers.
Try visiting: http://127.0.0.1:8000/users?skip=1&limit=2

```python
@app.get("/users")
async def get_users(skip: int = 0, limit: int = 2):
    # Slice the list based on pagination
    return {
        "description": f"Showing users starting from index {skip} (limit {limit})",
        "results": USERS_DATABASE[skip : skip + limit]
    }
```

## 2. OPTIONAL PARAMETERS & BOOLEAN CONVERSION

- `role` is an optional query parameter. By declaring its type as `Union[str, None] = None`
  (or `str | None = None` in modern Python), FastAPI knows it is optional and defaults to `None`.
- `active` is a boolean query parameter. FastAPI is smart: it converts query strings like
  `true`, `1`, `yes`, `on` into Python `True`, and `false`, `0`, `no` into Python `False`.
Try visiting: http://127.0.0.1:8000/search-users?active=yes&role=admin

```python
@app.get("/search-users")
async def search_users(
    role: Union[str, None] = None, 
    active: bool = True
):
    results = USERS_DATABASE

    # Filter by role if provided
    if role:
        results = [u for u in results if u["role"] == role]

    # Filter by active status
    results = [u for u in results if u["active"] == active]

    return {
        "filters": {"role": role, "active": active},
        "results": results
    }
```

## 3. QUERY VALIDATION AND METADATA

You can use the `Query` class to add rules and validations to your parameters.
For example:
- `q` must have a minimum length of 3 characters, max of 15.
- If the user provides a string with fewer than 3 characters, FastAPI rejects it.
- We can also add a description for the Swagger UI documentation.
Try visiting: http://127.0.0.1:8000/search?q=ri
It will return a 422 error because "ri" is less than 3 characters!

```python
@app.get("/search")
async def search(
    q: Union[str, None] = Query(
        default=None, 
        min_length=3, 
        max_length=15, 
        description="Search term to find users by username"
    )
):
    results = USERS_DATABASE
    if q:
        # Check if the search term is inside the username
        results = [u for u in results if q.lower() in u["username"].lower()]

    return {
        "query": q,
        "results": results
    }
```

## HOW TO RUN THIS FILE

```python
if __name__ == "__main__":
    uvicorn.run("03_query_parameters:app", host="127.0.0.1", port=8000, reload=True)
```

## QUICK SUMMARY FOR RETESTING

1. Run this file: `python 03_query_parameters.py`
2. Go to: http://127.0.0.1:8000/docs
3. Try the `/users` endpoint without any query params (it uses defaults skip=0, limit=2)
4. Try `/search-users` with `active=false`. Watch it convert "false" to boolean `False`.
5. Try `/search` with a query `q` that is too short (e.g. `ab`) and check the error.

## Real-Life Use Cases

1. SEARCH & FILTER (like Naukri.com / LinkedIn Jobs)
   - GET /jobs?title=developer&location=bangalore&experience=3
   - All filters are query parameters. If not provided → return all jobs.
   - This is the MOST common use of query parameters in real products.

2. PAGINATION (like Twitter Feed / Instagram)
   - GET /posts?skip=0&limit=10  → first 10 posts (page 1)
   - GET /posts?skip=10&limit=10 → next 10 posts (page 2)
   - Every social media feed uses skip+limit or cursor-based pagination.

3. SEARCH WITH VALIDATION (like GitHub / GitLab API)
   - GitHub's API uses `q` param: GET /search/repositories?q=fastapi&sort=stars
   - Query is validated server-side for min length → prevents empty/garbage searches.
   - FastAPI's Query(min_length=3) does this automatically.

4. SORTING (like Amazon / Flipkart product listing)
   - GET /products?sort=price_asc   → sort by price ascending
   - GET /products?sort=rating_desc → sort by rating descending
   - The `sort` param is optional; default is usually "relevance".

<Questions>
<Question id="Q1" title="How does FastAPI distinguish between a path parameter and a query parameter?">
FastAPI checks the function signature:
  - If the variable name appears in the path string (e.g., `{item_id}`) → PATH param.
  - If the variable is NOT in the path → automatically treated as QUERY param.
Example:
  @app.get("/items/{item_id}")
  def get_item(item_id: int, q: str = None):
    # item_id → path param (in URL path)
    # q      → query param (not in path, appears after ?)
</Question>
<Question id="Q2" title="How does FastAPI handle boolean query parameters?">
FastAPI is smart about boolean conversion from URL strings:
  ?active=true, ?active=1, ?active=yes, ?active=on  → Python True
  ?active=false, ?active=0, ?active=no, ?active=off → Python False
This is done automatically by Pydantic's type coercion. You just declare `active: bool`.
</Question>
<Question id="Q3" title="What is the `Query` class in FastAPI and when do you use it?">
`Query` is a special function from FastAPI that lets you add METADATA and VALIDATION
to query parameters. You use it when you need:
  - min_length / max_length (for strings)
  - gt / lt / ge / le (for numbers: greater than, less than)
  - description (shown in Swagger docs)
  - alias (use a different name in the URL vs in Python code)
Without Query(): just a simple parameter with optional default.
With Query(): a parameter with rules + documentation.
</Question>
<Question id="Q4" title="What is the difference between `q: str = None` and `q: str = Query(default=None, min_length=3)`?">
`q: str = None` → Optional string, no validation. Any value (even empty) is accepted.
`q: str = Query(default=None, min_length=3)` → Optional, BUT if provided, must be >= 3 chars.
FastAPI automatically returns 422 if validation fails. No try/except needed.
</Question>
<Question id="Q5" title="In a real project, how would you implement pagination for a GET /products endpoint?">
@app.get("/products")
def get_products(skip: int = 0, limit: int = Query(default=10, le=100)):
    # `le=100` means limit cannot exceed 100. Prevents someone requesting 100,000 records!
    products = db.query(Product).offset(skip).limit(limit).all()
    return products
Always cap the limit (e.g., max 100) to prevent performance attacks.
</Question>
</Questions>
