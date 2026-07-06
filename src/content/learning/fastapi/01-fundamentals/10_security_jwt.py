# ==========================================================
# FASTAPI STUDY GUIDE: 10. SECURITY & JWT (JSON WEB TOKENS)
# ==========================================================

# --- WHAT IS JWT & AUTHENTICATION? ---
# In modern APIs, we do not send the username and password with every request.
# Instead:
# 1. The client logs in once with username/password (via POST /token).
# 2. The server verifies them, and returns a signed string called a JWT (JSON Web Token).
# 3. The client stores this token and sends it in the Header (`Authorization: Bearer <token>`) 
#    for all future requests to protected routes.
# 4. The server validates the token signature. If it is valid, the server trusts the client's identity.
#
# A JWT has 3 parts separated by dots (.):
# - Header: Algorithm used (e.g. HS256).
# - Payload: The data (claims) inside (e.g. user_id, expiration time).
# - Signature: Verifies that the token wasn't altered (created using a SECRET_KEY).

from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from typing import Union
from datetime import datetime, timedelta, timezone
import hashlib
import hmac
import uvicorn

# We will try importing 'jwt' (from PyJWT).
# If not installed, we'll use a fallback dictionary-token system so the script still runs!
try:
    import jwt
    HAS_PYJWT = True
except ImportError:
    HAS_PYJWT = False

app = FastAPI(title="FastAPI: Security & JWT")

# 1. Configuration Constants
SECRET_KEY = "my_super_secret_key_change_me_in_production"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# OAuth2PasswordBearer tells FastAPI that the token should be sent in the 
# HTTP request Authorization header: "Authorization: Bearer <token>"
# The "tokenUrl" tells Swagger UI where to send the credentials to get a token.
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


# ==========================================================
# 2. PASSWORD HASHING HELPER (SECURE & COMPATIBLE)
# ==========================================================
# Instead of storing plain-text passwords, we "hash" them.
# We'll use Python's built-in `hashlib.pbkdf2_hmac` which is secure and 
# doesn't require any C-extensions (like bcrypt sometimes does on Windows).
class PasswordManager:
    @staticmethod
    def get_password_hash(password: str) -> str:
        # Use PBKDF2 with SHA256 hashing
        salt = b"some_fixed_salt_for_learning"
        key = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, 100000)
        return key.hex()

    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        return PasswordManager.get_password_hash(plain_password) == hashed_password


# Mock database with a pre-created user (password is "mysecret123")
MOCK_USERS_DB = {
    "ritesh": {
        "username": "ritesh",
        "email": "ritesh@example.com",
        "hashed_password": PasswordManager.get_password_hash("mysecret123"),
        "full_name": "Ritesh Sinha",
        "role": "admin"
    }
}


# ==========================================================
# 3. JWT TOKEN CREATION & VERIFICATION
# ==========================================================
def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    
    # Add expiration claim
    to_encode.update({"exp": expire})
    
    if HAS_PYJWT:
        return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    else:
        # Fallback simulation if pyjwt is not installed yet
        return f"SIMULATED_TOKEN.{to_encode['sub']}.{int(expire.timestamp())}"

def verify_access_token(token: str):
    if HAS_PYJWT:
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            username: str = payload.get("sub")
            if username is None:
                raise HTTPException(status_code=401, detail="Token invalid: missing sub")
            return username
        except jwt.PyJWTError:
            raise HTTPException(status_code=401, detail="Token signature invalid or expired")
    else:
        # Fallback verification logic
        if not token.startswith("SIMULATED_TOKEN."):
            raise HTTPException(status_code=401, detail="Invalid simulated token format")
        parts = token.split(".")
        username = parts[1]
        exp = int(parts[2])
        if datetime.now(timezone.utc).timestamp() > exp:
            raise HTTPException(status_code=401, detail="Simulated token expired")
        return username


# ==========================================================
# 4. RETRIEVING CURRENT USER (DEPENDENCY)
# ==========================================================
# This dependency reads the token from the Header, decodes it, 
# finds the user, and returns it.
async def get_current_user(token: str = Depends(oauth2_scheme)):
    username = verify_access_token(token)
    user = MOCK_USERS_DB.get(username)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="User not found"
        )
    return user


# ==========================================================
# 5. AUTHENTICATION & LOGIN ROUTE
# ==========================================================
# OAuth2PasswordRequestForm is a built-in form that extracts `username` and `password`
# from body data (form data, NOT JSON data - which is the OAuth2 standard).
@app.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = MOCK_USERS_DB.get(form_data.username)
    if not user or not PasswordManager.verify_password(form_data.password, user["hashed_password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
        
    # Generate token
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user["username"], "role": user["role"]}, 
        expires_delta=access_token_expires
    )
    
    return {"access_token": access_token, "token_type": "bearer"}


# ==========================================================
# 6. PROTECTED ROUTE
# ==========================================================
class UserResponse(BaseModel):
    username: str
    email: str
    full_name: str
    role: str

@app.get("/users/me", response_model=UserResponse)
async def read_users_me(current_user: dict = Depends(get_current_user)):
    # This route will ONLY run if a valid access token is provided!
    return current_user


# ----------------------------------------------------------
# HOW TO RUN THIS FILE
# ----------------------------------------------------------
if __name__ == "__main__":
    if not HAS_PYJWT:
        print("\n[Warning] 'pyjwt' is not installed. Running in token simulation mode.")
        print("Install it using: pip install pyjwt\n")
    uvicorn.run("10_security_jwt:app", host="127.0.0.1", port=8000, reload=True)


# --- QUICK SUMMARY FOR RETESTING ---
# 1. Run this file: `python 10_security_jwt.py`
# 2. Go to: http://localhost:8000/docs
# 3. Notice the green "Authorize" lock button at the top right of the Swagger UI!
# 4. Try calling GET `/users/me` — it will fail with `401 Unauthorized` (lock is open).
# 5. Click the "Authorize" button, type username: `ritesh` and password: `mysecret123`. Click Authorize.
# 6. Run GET `/users/me` again. Swagger automatically sends the bearer token, and it succeeds!


# ==========================================================
# REAL-LIFE USE CASES
# ==========================================================

# 1. USER LOGIN / SESSION (like any app: Swiggy, Zomato, IRCTC)
#    - User logs in with email+password → POST /token → receives JWT.
#    - App stores token in localStorage or cookie.
#    - Every future request sends: Authorization: Bearer <token>
#    - Backend verifies token → no need to hit DB for EVERY request.

# 2. MICROSERVICE AUTH (like internal APIs at Infosys / Wipro)
#    - Service A calls Service B. Service A includes its JWT in the request.
#    - Service B verifies the JWT signature using the shared SECRET_KEY.
#    - No username/password exchange between services — just tokens.

# 3. ROLE-BASED ACCESS CONTROL (like admin panels)
#    - JWT payload includes: {"sub": "ritesh", "role": "admin"}
#    - Routes check the role from the token.
#    - Admin routes only allow role=="admin". Others get 403 Forbidden.
#    - Used in every CMS, ERP, and SaaS admin dashboard.

# 4. MOBILE APP AUTH (like PhonePe / Google Pay)
#    - Mobile app logs in once and stores the JWT locally.
#    - Token expires in 30 mins. Refresh token extends session without re-login.
#    - User stays "logged in" for days without re-entering password.


# ==========================================================
# MNC INTERVIEW QUESTIONS & ANSWERS
# ==========================================================

# Q1. What is JWT and how does it work?
# A:  JWT = JSON Web Token. It's a compact, signed string with 3 parts separated by dots:
#       Header.Payload.Signature
#     Header:    Algorithm used (e.g., {"alg": "HS256"})
#     Payload:   Data/claims (e.g., {"sub": "ritesh", "role": "admin", "exp": 1234567890})
#     Signature: HMAC of Header+Payload using SECRET_KEY. Proves the token wasn't tampered.
#     The server NEVER stores the token. It just verifies the signature on each request.

# Q2. What is the difference between Authentication and Authorization?
# A:  Authentication → "Who are you?" — Verifying identity. (Login with username/password)
#     Authorization  → "What can you do?" — Checking permissions. (Admin vs Normal user)
#     Example flow:
#       1. POST /token with username+password → AUTHENTICATION (verify identity, issue JWT)
#       2. GET /admin with JWT → AUTHORIZATION (verify role == 'admin' from token)
#     FastAPI handles both using OAuth2PasswordBearer + JWT + role checks.

# Q3. Why do we hash passwords instead of storing them in plain text?
# A:  If your database is compromised (hacked), plain text passwords are exposed directly.
#     Hashed passwords: even with DB access, hacker cannot reverse the hash to get the password.
#     Hashing is ONE-WAY: Password → Hash (easy). Hash → Password (computationally impossible).
#     Always use bcrypt or PBKDF2 for password hashing. NEVER use MD5 or SHA1 for passwords.
#     MNC standard: Use `passlib[bcrypt]` library in production FastAPI projects.

# Q4. What is OAuth2 and how does FastAPI implement it?
# A:  OAuth2 is an industry-standard AUTHORIZATION protocol.
#     FastAPI's `OAuth2PasswordBearer` implements the "Password Flow" of OAuth2:
#       1. Client sends username+password to /token endpoint.
#       2. Server validates, returns {"access_token": "...", "token_type": "bearer"}.
#       3. Client includes `Authorization: Bearer <token>` header in future requests.
#     The "Bearer" prefix is part of the OAuth2 standard. It tells the server
#     the type of token being sent.

# Q5. What is token expiration and why is it important?
# A:  JWT tokens have an `exp` (expiration) claim. After this time, the token is INVALID.
#     Why important:
#       - Stolen tokens: If a token is stolen, it becomes useless after it expires.
#       - No logout mechanism: Since JWT is stateless, expiration is the only "forced logout".
#     Best practices:
#       - Short-lived access tokens: expire in 15-60 minutes.
#       - Long-lived refresh tokens: expire in 7-30 days. Used to get new access tokens.
#       - Critical systems (banking): expire in 5 minutes. Users re-authenticate frequently.
