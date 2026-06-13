# ==========================================================
# FASTAPI STUDY GUIDE: 07. DEPENDENCY INJECTION (DI)
# ==========================================================

# --- WHAT IS DEPENDENCY INJECTION? ---
# Dependency injection is a design pattern where a function or object is given its 
# dependencies (things it needs to work) rather than creating them inside itself.
#
# In FastAPI, we use `Depends` to declare dependencies.
# Why is this useful?
# 1. Code Reuse: Write a utility once (like database connection or security checking) and share it.
# 2. Automatically Handles Parameters: Dependencies can read request headers, query params, etc.
# 3. Easy Testing: You can easily "override" dependencies when writing automated tests.

from fastapi import FastAPI, Depends, Header, HTTPException, status
from typing import Union
import uvicorn

app = FastAPI(title="FastAPI: Dependency Injection")

# ==========================================================
# 1. SIMPLE FUNCTION DEPENDENCY (Common Query Parameters)
# ==========================================================
# A reusable function that parses pagination parameters.
async def pagination_parameters(q: Union[str, None] = None, skip: int = 0, limit: int = 10):
    return {"q": q, "skip": skip, "limit": limit}

# To use it, we declare a parameter with type hints and call Depends()
@app.get("/items")
async def read_items(params: dict = Depends(pagination_parameters)):
    # `params` contains the dictionary returned by `pagination_parameters`
    return {
        "message": "Fetching items...",
        "filters_applied": params
    }

@app.get("/users")
async def read_users(params: dict = Depends(pagination_parameters)):
    return {
        "message": "Fetching users...",
        "filters_applied": params
    }


# ==========================================================
# 2. SUB-DEPENDENCY & SECURITY CHECKING
# ==========================================================
# Dependencies can depend on OTHER dependencies.
# Let's create an authentication check that looks for a "X-API-Key" header.

async def verify_api_key(x_api_key: str = Header(..., description="API Access Token")):
    # In a real app, you would check this key in a database.
    if x_api_key != "secret-token-123":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing API Key"
        )
    return x_api_key

# Now, let's create a dependency that depends on `verify_api_key`
async def get_admin_user(api_key: str = Depends(verify_api_key)):
    # This dependency only runs IF verify_api_key succeeds.
    # We can perform additional admin checks here.
    return {"username": "ritesh_admin", "api_key_used": api_key}

# An endpoint that is fully protected by dependencies!
@app.get("/admin/dashboard")
async def admin_dashboard(admin: dict = Depends(get_admin_user)):
    return {
        "message": f"Welcome, {admin['username']}! You have access to the secret admin dashboard."
    }


# ==========================================================
# 3. YIELD DEPENDENCIES (Database Sessions)
# ==========================================================
# Sometimes a dependency needs to do some cleanup after the request finishes.
# For example: open a DB connection -> run the route -> close the DB connection.
# We do this using `yield` instead of `return`.

class MockDatabaseSession:
    def __init__(self):
        print("[DB Connection] Opening connection session...")
    def query(self, data):
        return f"Database query result for: {data}"
    def close(self):
        print("[DB Connection] Closing connection session! (Cleanup done)")

# The dependency:
async def get_db_session():
    db = MockDatabaseSession()
    try:
        # FastAPI yields control back to the route function
        yield db
    finally:
        # After the route sends the response, this cleanup block runs automatically!
        db.close()

@app.get("/db-query/{query_text}")
async def query_db(query_text: str, db: MockDatabaseSession = Depends(get_db_session)):
    # The route uses the yielded database connection
    result = db.query(query_text)
    return {"status": "Success", "data": result}


# ----------------------------------------------------------
# HOW TO RUN THIS FILE
# ----------------------------------------------------------
if __name__ == "__main__":
    uvicorn.run("07_dependency_injection:app", host="127.0.0.1", port=8000, reload=True)


# --- QUICK SUMMARY FOR RETESTING ---
# 1. Run this file: `python 07_dependency_injection.py`
# 2. Go to: http://127.0.0.1:8000/docs
# 3. Try `/items` or `/users` — Swagger UI automatically detects the query parameters 
#    (`q`, `skip`, `limit`) even though they are inside the `Depends()` function!
# 4. Try `/admin/dashboard` — you must supply the header `x-api-key` with value `secret-token-123`.
# 5. Try `/db-query/hello`. Check your Python terminal output: you will see 
#    "[DB Connection] Opening connection session..." followed by 
#    "[DB Connection] Closing connection session!" proving the cleanup worked.


# ==========================================================
# REAL-LIFE USE CASES
# ==========================================================

# 1. DATABASE SESSION PER REQUEST (like every MNC backend)
#    - Every route that touches the DB needs a session. Without DI:
#        db = SessionLocal() → copy-paste in every function → bugs everywhere.
#    - With DI: def get_db() is defined ONCE. Every route just writes `db = Depends(get_db)`.
#    - If DB fails → the dependency raises an error → none of your routes need try/except.

# 2. AUTHENTICATION & AUTHORIZATION (like every secured API)
#    - `get_current_user` is a dependency. Any route that needs auth just adds:
#        user = Depends(get_current_user)
#    - Without DI: you'd write the same token verification code in EVERY protected route.
#    - With DI: write once, reuse everywhere. Change auth logic in ONE place.

# 3. RATE LIMITING (like Razorpay / Stripe API)
#    - A dependency checks: "Has this IP made more than 100 requests in 60 seconds?"
#    - If yes → dependency raises HTTPException(429, "Too Many Requests")
#    - All routes are automatically rate-limited just by adding Depends(rate_limiter).

# 4. FEATURE FLAGS (like Netflix / Swiggy A/B testing)
#    - A dependency reads a feature flag config and returns which features are ON/OFF.
#    - Routes use Depends(get_feature_flags) to show different UI/behavior to users.
#    - New features can be toggled ON/OFF without code deployment.


# ==========================================================
# MNC INTERVIEW QUESTIONS & ANSWERS
# ==========================================================

# Q1. What is Dependency Injection and why is it used in FastAPI?
# A:  Dependency Injection (DI) means: a function declares what it NEEDS (its dependencies)
#     and FastAPI automatically creates and provides those dependencies.
#     Benefits:
#       1. REUSABILITY: Write a dependency once (like DB session), use in 50 routes.
#       2. TESTABILITY: Easily swap real dependencies with mock ones in tests.
#       3. CLEANLINESS: Route handlers stay small — complex setup logic lives in dependencies.

# Q2. How does `Depends()` work in FastAPI?
# A:  When FastAPI sees `param = Depends(some_function)`, it:
#       1. Calls `some_function` automatically (resolving its own params from the request).
#       2. Passes the return value as `param` to your route function.
#     The dependency function can itself have parameters (query params, headers, other Depends).
#     FastAPI resolves the full dependency graph automatically.

# Q3. What is the difference between `return` and `yield` in a FastAPI dependency?
# A:  `return` → Simple dependency. Runs setup, returns value, done.
#     `yield` → Resource dependency with cleanup. Pattern:
#         setup code
#         yield resource     ← route function runs here
#         cleanup code       ← runs AFTER response is sent
#     Use `yield` for: database sessions, file handles, HTTP client connections.
#     Use `return` for: simple computed values, auth checks, config loading.

# Q4. Can one dependency depend on another dependency in FastAPI?
# A:  YES! FastAPI resolves nested/chained dependencies automatically.
#     Example chain:
#       get_db() → returns DB session
#       verify_token() → reads header, verifies JWT
#       get_current_user(db=Depends(get_db), token=Depends(verify_token)) → uses both!
#       admin_only(user=Depends(get_current_user)) → checks user.role == 'admin'
#     FastAPI builds this dependency tree and resolves everything before calling the route.

# Q5. How do you override a dependency in tests?
# A:  FastAPI provides `app.dependency_overrides` for this.
#     Example:
#       def fake_get_db():  # Mock DB that doesn't touch real database
#           yield MockDB()
#       app.dependency_overrides[get_db] = fake_get_db
#     This is HOW you write unit tests for FastAPI routes without a real database.
#     After tests: app.dependency_overrides.clear() to restore original dependencies.
