# ==========================================================
# FASTAPI STUDY GUIDE: 05. RESPONSE MODELS & STATUS CODES
# ==========================================================

# --- WHY USE RESPONSE MODELS? ---
# When you return data from a database, it often contains internal columns 
# (like password_hash, created_at, or secret_key) that you do NOT want to send to the client.
# By defining a `response_model`, FastAPI will:
# 1. Filter out all data that is not declared in the response model.
# 2. Validate the output data to ensure it matches the model structure.
# 3. Generate correct schemas in the Swagger UI.

# --- HTTP STATUS CODES ---
# HTTP status codes tell the client the result of their request:
# - 200 OK: Request succeeded.
# - 201 Created: Resource created (commonly used for POST).
# - 400 Bad Request: Client sent invalid data or request.
# - 404 Not Found: Resource does not exist.
# - 500 Internal Server Error: Server crashed.

from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
from typing import Union
import uvicorn

app = FastAPI(title="FastAPI: Response Models & Status Codes")

# ==========================================================
# 1. SCHEMAS: INPUT (CREATE) vs OUTPUT (RESPONSE)
# ==========================================================

# Model representing the client's input (includes password)
class UserCreate(BaseModel):
    username: str
    email: str
    password: str  # We need the password during user creation

# Model representing the API's response (excludes password for security!)
class UserResponse(BaseModel):
    username: str
    email: str
    is_active: bool = True  # We can also add default fields for the output


# Mock database
USERS_DATABASE = {}


# ==========================================================
# 2. CUSTOM STATUS CODE & RESPONSE MODEL
# ==========================================================
# We set:
# - `status_code=status.HTTP_201_CREATED` (resends HTTP 201 instead of default 200).
# - `response_model=UserResponse` (FastAPI automatically strips out the `password` field
#   from whatever we return before sending it to the client).
@app.post(
    "/users", 
    response_model=UserResponse, 
    status_code=status.HTTP_201_CREATED,
    summary="Create a new user"
)
async def create_user(user_in: UserCreate):
    # Simulate saving to database
    # (Note: In a real database, we would encrypt/hash this password before saving)
    db_user = {
        "username": user_in.username,
        "email": user_in.email,
        "password": user_in.password + "hashed_secret_salt",  # Hashed in DB
        "is_active": True
    }
    
    # Save user by username
    USERS_DATABASE[user_in.username] = db_user
    
    # We return the ENTIRE db_user dictionary (which contains "password").
    # But because of `response_model=UserResponse`, FastAPI will AUTOMATICALLY 
    # filter out "password" and only return username, email, and is_active!
    return db_user


# ==========================================================
# 3. GET ROUTE WITH RESPONSE MODEL
# ==========================================================
@app.get(
    "/users/{username}", 
    response_model=UserResponse,
    status_code=status.HTTP_200_OK
)
async def get_user(username: str):
    if username not in USERS_DATABASE:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User '{username}' not found.")
        
    return USERS_DATABASE[username]


# ----------------------------------------------------------
# HOW TO RUN THIS FILE
# ----------------------------------------------------------
if __name__ == "__main__":
    uvicorn.run("05_response_models_and_status:app", host="127.0.0.1", port=8000, reload=True)


# --- QUICK SUMMARY FOR RETESTING ---
# 1. Run this file: `python 05_response_models_and_status.py`
# 2. Go to: http://127.0.0.1:8000/docs
# 3. Try creating a user using the POST `/users` endpoint. Look at the output:
#    It returns HTTP code 201 (Created), and the JSON payload contains only `username`, 
#    `email`, and `is_active`. The `password` key is completely hidden!


# ==========================================================
# REAL-LIFE USE CASES
# ==========================================================

# 1. USER AUTHENTICATION SYSTEM (like any app login)
#    - POST /users creates user. Database stores hashed password.
#    - Response model STRIPS the password field automatically.
#    - This is a CRITICAL security practice. Leaking password hashes can lead to data breach.

# 2. E-COMMERCE ORDER RESPONSE
#    - Database order record has: user_id, internal_cost, profit_margin, warehouse_id...
#    - API response to customer should only have: order_id, items, total_price, delivery_date.
#    - Response model ensures internal/sensitive fields are NEVER sent to the customer.

# 3. INTERNAL ADMIN vs PUBLIC API
#    - Same endpoint, different response models for different user types.
#    - Admin sees: GET /users/{id} → UserAdminResponse (includes all fields)
#    - Public sees: GET /users/{id} → UserPublicResponse (only name, bio, avatar)
#    - In MNCs, this is implemented using response_model + role-based access control.

# 4. CORRECT STATUS CODES IN PRODUCTION
#    - POST /orders → 201 Created (resource created)
#    - DELETE /orders/1 → 204 No Content (deleted, nothing to return)
#    - GET /orders/999 → 404 Not Found (doesn't exist)
#    - POST /login with wrong password → 401 Unauthorized
#    - Incorrect status codes cause frontend bugs and confuse monitoring systems.


# ==========================================================
# MNC INTERVIEW QUESTIONS & ANSWERS
# ==========================================================

# Q1. Why should we use `response_model` in FastAPI?
# A:  Three key reasons:
#       1. SECURITY: Prevents sensitive data (passwords, tokens) from leaking to clients.
#       2. CONTRACT: Guarantees the API always returns a consistent structure.
#       3. DOCUMENTATION: Swagger UI shows the exact response schema automatically.
#     Without it, you might accidentally return raw DB objects with hidden fields.

# Q2. What is the difference between HTTP 200, 201, 204?
# A:  200 OK       → Request succeeded. Data returned in body. Used for GET, PUT.
#     201 Created  → A new resource was created. Used for POST. Body has the new resource.
#     204 No Content → Request succeeded but nothing to return. Used for DELETE.
#     Using wrong codes is a common bug in junior developers' code at MNCs.

# Q3. What is the difference between HTTP 401 and 403?
# A:  401 Unauthorized → "Who are you?" — Client is NOT authenticated (no/invalid token).
#     403 Forbidden     → "I know who you are, but NO." — Client IS authenticated but doesn't
#                         have permission for this action.
#     Example:
#       - Guest accessing /dashboard → 401 (needs to login first)
#       - Regular user accessing /admin → 403 (logged in, but not an admin)

# Q4. How does FastAPI's `response_model` filter data?
# A:  When you return a dict or ORM object, FastAPI:
#       1. Passes it through the `response_model` Pydantic model.
#       2. Pydantic ONLY keeps the fields defined in the model.
#       3. Any extra fields (like `password`) are SILENTLY dropped.
#     This happens AFTER your function runs — you can still use `password` inside your function.

# Q5. What is `status.HTTP_201_CREATED` and why use it instead of just writing `201`?
# A:  `status.HTTP_201_CREATED` is a constant from FastAPI that equals the integer 201.
#     Benefits of using constants:
#       - Self-documenting: The name tells you what the code means.
#       - Less chance of typos: Typing 210 instead of 201 is a silent bug.
#       - IDE autocomplete helps: Type `status.HTTP_` and see all options.
#     It's a best practice in all MNC Python codebases.
