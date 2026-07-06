# ==========================================================
# FASTAPI STUDY GUIDE: 06. ERROR HANDLING
# ==========================================================

# --- WHAT IS ERROR HANDLING? ---
# When something goes wrong (e.g., resource not found, user unauthorized, database timeout),
# your API should return a proper HTTP error code along with a descriptive error message.
#
# FastAPI provides:
# 1. `HTTPException`: A special exception class you can raise anywhere to stop request processing
#    and immediately send an error response to the client.
# 2. Custom Exception Handlers: Global hooks to catch custom Python errors and format them nicely.

from fastapi import FastAPI, HTTPException, Request, status
from fastapi.responses import JSONResponse
import uvicorn

app = FastAPI(title="FastAPI: Error Handling")

# Mock database
ITEMS_DATABASE = {
    "sword": {"name": "Excalibur", "type": "Weapon"},
    "shield": {"name": "Aegis", "type": "Armor"}
}

# ==========================================================
# 1. RAISING HTTP_EXCEPTION (THE COMMON WAY)
# ==========================================================
# If an item doesn't exist, we raise `HTTPException` with status code 404 (Not Found).
# If it does exist, we return it.
@app.get("/items/{item_key}")
async def get_item(item_key: str):
    if item_key not in ITEMS_DATABASE:
        # Raising this stops execution immediately and returns the error to the client
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Item '{item_key}' does not exist in our inventory."
        )
    return ITEMS_DATABASE[item_key]


# ==========================================================
# 2. DEFINING A CUSTOM EXCEPTION CLASS
# ==========================================================
# Sometimes you want to raise your own Python exceptions throughout your business logic,
# without polluting your code with HTTP status codes.
# Let's create a custom exception representing a database outage.
class DatabaseConnectionError(Exception):
    def __init__(self, db_name: str):
        self.db_name = db_name


# ==========================================================
# 3. REGISTERING A GLOBAL EXCEPTION HANDLER
# ==========================================================
# This decorator tells FastAPI: "If any function in this app raises DatabaseConnectionError,
# catch it, pass it here, and return this JSONResponse instead of crashing the server."
@app.exception_handler(DatabaseConnectionError)
async def db_connection_exception_handler(request: Request, exc: DatabaseConnectionError):
    return JSONResponse(
        status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
        content={
            "error_type": "DATABASE_ERROR",
            "message": f"Could not connect to database: '{exc.db_name}'. Please try again later.",
            "documentation_url": "http://localhost:8000/docs"
        }
    )


# A route that simulates a database failure and raises our custom exception
@app.get("/simulate-db-error")
async def simulate_db_error():
    # Simulate database connection failure
    raise DatabaseConnectionError(db_name="Production_PostgreSQL")


# ----------------------------------------------------------
# HOW TO RUN THIS FILE
# ----------------------------------------------------------
if __name__ == "__main__":
    uvicorn.run("06_error_handling:app", host="127.0.0.1", port=8000, reload=True)


# --- QUICK SUMMARY FOR RETESTING ---
# 1. Run this file: `python 06_error_handling.py`
# 2. Go to: http://localhost:8000/docs
# 3. Test `/items/sword` (returns weapon details).
# 4. Test `/items/potion` (returns 404 error and message in JSON: "detail": "...")
# 5. Test `/simulate-db-error` (returns 503 Service Unavailable, and our custom structured JSON error output).


# ==========================================================
# REAL-LIFE USE CASES
# ==========================================================

# 1. E-COMMERCE: PRODUCT NOT FOUND (like Amazon / Flipkart)
#    - GET /products/99999 → Product doesn't exist in DB
#    - Backend raises HTTPException(404, detail="Product not found")
#    - Frontend shows a friendly "Product not available" message using the 404 status.

# 2. FOOD ORDERING: RESTAURANT CLOSED (like Swiggy / Zomato)
#    - POST /orders with a restaurant that's currently closed
#    - Backend raises HTTPException(400, detail="Restaurant is not accepting orders right now")
#    - App shows the correct error popup to the user.

# 3. BANKING: DATABASE OUTAGE HANDLING (like HDFC / ICICI Bank apps)
#    - The core banking system goes down for maintenance.
#    - Instead of crashing with a 500 error, a custom exception handler returns:
#      {"error": "SERVICE_UNAVAILABLE", "message": "Please try again after 2 minutes"}
#    - Users see a friendly message instead of a raw server crash.

# 4. PAYMENT: INSUFFICIENT BALANCE (like Paytm / PhonePe)
#    - POST /transfer with amount > wallet balance
#    - Raises HTTPException(400, detail="Insufficient balance")
#    - The correct HTTP 400 code tells the frontend "bad input" not "server crash".


# ==========================================================
# MNC INTERVIEW QUESTIONS & ANSWERS
# ==========================================================

# Q1. What is HTTPException in FastAPI and when do you use it?
# A:  `HTTPException` is a special exception class from FastAPI.
#     When you `raise HTTPException(status_code=404, detail="Not found")`, FastAPI:
#       1. STOPS running the current function immediately.
#       2. Sends an HTTP response with that status code and JSON: {"detail": "Not found"}
#     Use it whenever the client made a valid request but the data/resource doesn't exist
#     or a business rule was violated. Never return errors as 200 OK responses!

# Q2. What is the difference between HTTPException and a regular Python Exception?
# A:  Regular Python Exception → Used in business logic. Has no HTTP concept.
#         Example: raise ValueError("Invalid email")
#     HTTPException → FastAPI-specific. Maps directly to an HTTP error response.
#         Example: raise HTTPException(status_code=422, detail="Invalid email format")
#     In real projects: Raise regular exceptions in service/business layers.
#     Use @app.exception_handler to convert them into proper HTTP responses at the API layer.

# Q3. What are the most important HTTP error status codes to know?
# A:  400 Bad Request        → Client sent invalid/malformed data.
#     401 Unauthorized       → Not logged in. Need to authenticate first.
#     403 Forbidden          → Logged in but no permission for this action.
#     404 Not Found          → The resource doesn't exist.
#     409 Conflict           → Resource already exists (duplicate user, duplicate ID).
#     422 Unprocessable      → Data format/type is wrong (FastAPI auto-returns this).
#     429 Too Many Requests  → Rate limit exceeded. Client is sending too many requests.
#     500 Internal Server Error → Something unexpected broke on the server.
#     503 Service Unavailable   → Server is down/overloaded. Try again later.

# Q4. What is an exception_handler in FastAPI and why is it useful in production?
# A:  @app.exception_handler(SomeException) registers a GLOBAL catcher for that exception.
#     Why useful:
#       1. SEPARATION: Business logic raises plain Python exceptions (no HTTP code knowledge).
#       2. CONSISTENCY: All errors return the SAME JSON structure across the entire app.
#       3. LOGGING: You can log errors centrally in one place before responding.
#     MNC use case: Every service has a global exception handler that logs errors to
#     Datadog / Sentry / CloudWatch before returning a clean error response.

# Q5. What is the difference between status 400 and 422 in FastAPI?
# A:  400 Bad Request  → YOU raise manually when business logic fails.
#                         Example: raise HTTPException(400, "Username already taken")
#     422 Unprocessable → FastAPI raises AUTOMATICALLY when Pydantic validation fails.
#                         Example: Sending a string where an int is required.
#     Easy way to remember:
#       400 = "I understood what you sent, but I can't process it (business rule)"
#       422 = "I couldn't even understand the format of what you sent (wrong type/shape)"
