# ========================================================================================
# FASTAPI GUARDRAILS & INPUT/OUTPUT VALIDATION
# ========================================================================================
#
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# SECTION 1 — WEB API GUARDRAILS IN FASTAPI
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#
# Guardrails in web frameworks prevent malicious requests from hitting database engines or 
# downstream microservices. They also ensure outgoing HTTP responses comply with security
# standards (no password leaks, token exposures, or raw system exceptions).
#
# In FastAPI, guardrails are implemented at three key levels:
# 1. PYDANTIC SCHEMAS: Automatic data-type parsing and custom field validators.
# 2. DEPENDENCY INJECTION: Runs BEFORE path operations (e.g. rate-limiters, credential checks).
# 3. MIDDLEWARE: Intercepts all incoming requests and outgoing responses globally.
#
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# SECTION 2 — FASTAPI REQUEST/RESPONSE PIPELINE WITH GUARDRAILS
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#
#    HTTP Request ──► [ Middleware Guard ] ──► [ Dependency Guard ] ──► [ Pydantic Validator ]
#                                                                              │
#                                                                           (Pass)
#                                                                              ▼
#    HTTP Response ◄─ [ Sensitive Data Filter ] ◄──────────────────── [ Path Operation ]
#
# ========================================================================================

from fastapi import FastAPI, Depends, HTTPException, Request, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, field_validator
import uvicorn

app = FastAPI(title="FastAPI Guardrails Demo")

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 1. INPUT GUARDRAIL: PYDANTIC SCHEMA VALIDATION
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

class UserRegistration(BaseModel):
    username: str = Field(.., min_length=3, max_length=20)
    email: str
    password: str = Field(.., min_length=8)
    
    # Custom field validator to check query injections or suspicious inputs
    @field_validator("username")
    @classmethod
    def sanitize_username(cls, value: str) -> str:
        # Block characters commonly used in SQL injection or HTML exploits
        forbidden = ["'", '"', ";", "--", "<", ">"]
        if any(char in value for char in forbidden):
            raise ValueError("Username contains forbidden characters.")
        return value

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 2. INPUT GUARDRAIL: DEPENDENCY SECURITY CHECK
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# A reusable security check function that raises an HTTPException if violated.

async def verify_api_key_guard(request: Request):
    api_key = request.headers.get("X-API-Key")
    if not api_key or api_key != "secret-safe-key":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Forbidden: Invalid or missing API key."
        )
    return api_key

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 3. GLOBAL OUTPUT GUARDRAIL: CUSTOM MIDDLEWARE FILTER
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Middleware that acts as an outbound safety net, verifying that response 
# content never leaks internal system traces or credentials.

@app.middleware("http")
async def response_safety_guardrail(request: Request, call_next):
    response = await call_next(request)
    
    # Check custom response headers or status to catch unhandled errors
    if response.status_code == 500:
        # Inject a safe user-facing message instead of leaving raw database/OS exceptions
        return JSONResponse(
            status_code=500,
            content={"detail": "An internal server error occurred. The support team has been notified."}
        )
    
    return response

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# ENDPOINTS
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

@app.post("/register", dependencies=[Depends(verify_api_key_guard)])
async def register(payload: UserRegistration):
    """
    Simulated registration endpoint protected by an API key header check,
    plus Pydantic schema validation.
    """
    return {
        "status": "user_created",
        "username": payload.username,
        "email": payload.email
    }

@app.get("/simulate-leak")
async def simulate_leak():
    """
    Simulation of an unhandled internal exception. The middleware catches this 500
    and replaces the output with a generic safe warning.
    """
    raise RuntimeError("Database connection pool size exceeded! Root password: 123")

if __name__ == "__main__":
    # To run this script locally: python 12_guardrails.py
    # Then visit: http://127.0.0.1:8000/docs
    print("Starting FastAPI Guardrails Server on port 8000..")
    uvicorn.run(app, host="127.0.0.1", port=8000)

# ========================================================================================
# REAL-LIFE USE CASES
# ========================================================================================
#
# 1. PAYMENT GATEWAY BOUNDARY CHECKS:
#    - **Input**: Merchant client sends payment transactions to charge endpoints.
#    - **Step 1**: FastAPI rate-limiting dependency intercepts token frequencies.
#    - **Step 2**: Pydantic models validate that charge amount formats are positive and limited to 2 decimals.
#    - **Result**: Minimizes fraud exposure and blocks bad transaction records at the gateway.
#
# 2. PII RESPONSE COMPLIANCE:
#    - **Input**: Internal services return user account structures containing potential private profiles.
#    - **Step 1**: An outgoing middleware interceptor intercepts response JSON data.
#    - **Step 2**: Evaluates structures and masks card numbers or plain-text credentials.
#    - **Result**: Satisfies strict GDPR compliance before packets leave the server.
#
# ========================================================================================
# MNC INTERVIEW QUESTIONS & ANSWERS
# ========================================================================================
#
# Q1. What is the difference between middleware-based and dependency-based guardrails?
# A:  Middleware runs globally for all incoming requests and outgoing responses in the application,
#     making it ideal for logging, security headers, and catching exceptions. Dependencies run
#     at the router or individual path operation level, providing target-specific access to
#     injected resources (e.g. database sessions, authenticated user objects).
#
# Q2. How does FastAPI handle validation exceptions thrown inside Pydantic model fields?
# A:  When Pydantic validation fails, FastAPI catches the `ValidationError` internally and
#     translates it into an HTTP `422 Unprocessable Entity` response, returning a detailed
#     JSON report listing the invalid fields, location, and reason.
#
# Q3. Why should you avoid exposing raw Python exceptions in production responses?
# A:  Exposing raw traceback messages leaks internal implementation details, directory paths, 
#     database versions, or credentials to client endpoints. This makes the application 
#     vulnerable to target reconnaissance. Implementing an output safety middleware to mask 500 
#     errors blocks this vulnerability.
