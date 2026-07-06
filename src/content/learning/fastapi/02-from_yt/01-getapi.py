# ==========================================================
# FASTAPI YT SERIES: 01. GET API - BASIC ROUTES
# ==========================================================

# --- WHAT IS A GET REQUEST? ---
# GET is the most common HTTP method.
# It is used to READ / FETCH data from the server.
# It does NOT change any data on the server (read-only).
#
# Real-Life Examples:
#   - Searching on Google        → GET /search?q=fastapi
#   - Opening a product page     → GET /products/101
#   - Loading your Twitter feed  → GET /timeline
#
# KEY RULE: GET requests should NEVER modify data.
# If you want to create, update, or delete → use POST, PUT, DELETE.

# --- HOW FASTAPI HANDLES GET ROUTES ---
# 1. We create a FastAPI `app` instance.
# 2. We use @app.get("/some-path") decorator to register a GET route.
# 3. The function below the decorator runs when someone hits that URL.
# 4. FastAPI automatically converts the Python dict we return into JSON!

from fastapi import FastAPI

# Create the main FastAPI application instance
app = FastAPI(
    title="FastAPI YT Series - GET API",
    description="Learning how to build basic GET endpoints in FastAPI",
    version="1.0.0"
)


# ==========================================================
# 1. ROOT ENDPOINT (Home Route)
# ==========================================================
# When someone visits http://localhost:8000/
# this function runs and returns a welcome message.
#
# Real-Life Use Case:
#   - A health check endpoint for your deployed API.
#   - AWS Load Balancers ping / to check if the service is alive.
#   - If this returns 200 OK → service is up. Else → restart the pod.
@app.get("/")
def home():
    return {
        "message": "Welcome to the Learning FastAPI website",
        "status": "API is running",
        "docs": "Visit /docs to see all available endpoints"
    }


# ==========================================================
# 2. ABOUT ENDPOINT
# ==========================================================
# A simple static endpoint that returns info about your API.
#
# Real-Life Use Case:
#   - Apps expose an /about or /info endpoint for teams to know
#     which version of the service is deployed in production.
#   - Example: DevOps teams use this to confirm deployment success.
@app.get("/about")
def about():
    return {
        "message": "This is a simple FastAPI application.",
        "purpose": "Learning how to build REST APIs",
        "developer": "Ritesh"
    }


# ==========================================================
# 3. USERS ENDPOINT - Returning a List
# ==========================================================
# Returns a list of all users in the system.
#
# Real-Life Use Case:
#   - An admin dashboard calls GET /users to display a user list.
#   - HR software fetches all employees: GET /employees
#   - E-Commerce: GET /customers returns all registered customers.
#
# NOTE: In real projects, this data comes from a DATABASE.
# For now we are using a hardcoded list (called "mock data").
@app.get("/users")
def users():
    return {
        "users": [
            {"user_id": 1, "name": "John Doe"},
            {"user_id": 2, "name": "Jane Doe"},
            {"user_id": 3, "name": "Bob Smith"},
            {"user_id": 4, "name": "Alice Johnson"},
            {"user_id": 5, "name": "Mike Williams"}
        ]
    }


# ----------------------------------------------------------
# HOW TO RUN THIS FILE
# ----------------------------------------------------------
# Open your terminal in this folder and run:
#   uvicorn main:app --reload
#
# Then open your browser and visit:
#   http://localhost:8000/         → Home
#   http://localhost:8000/about    → About
#   http://localhost:8000/users    → Users list
#   http://localhost:8000/docs     → Interactive Swagger UI (AUTO-GENERATED!)
# ----------------------------------------------------------


# ==========================================================
# MNC INTERVIEW QUESTIONS & ANSWERS
# ==========================================================

# Q1. What is the difference between GET and POST?
# A:  GET is used to FETCH/READ data. It is idempotent (calling it 10 times gives same result).
#     POST is used to CREATE new data. Each POST creates a new record.
#     GET sends data in the URL. POST sends data in the request body (more secure).

# Q2. What does `@app.get("/")` mean in FastAPI?
# A:  It is a "path operation decorator". It tells FastAPI:
#     "When someone sends an HTTP GET request to the URL '/', call the function below."
#     `app` is the FastAPI instance. `.get` is the HTTP method. `"/"` is the URL path.

# Q3. What does FastAPI automatically return when a function returns a dict?
# A:  FastAPI automatically serializes (converts) the Python dictionary to a JSON response
#     with status code 200 OK and the header Content-Type: application/json.

# Q4. What is Swagger UI and how does FastAPI generate it?
# A:  Swagger UI is an interactive HTML page at /docs where you can see and test all your API endpoints.
#     FastAPI generates it automatically using OpenAPI specification — you don't write any extra code!
#     It reads your routes, type hints, and docstrings to build the documentation.

# Q5. What is the purpose of a "health check" endpoint (like GET /)?
# A:  In production (Kubernetes, AWS, GCP), the infrastructure pings the health endpoint
#     every few seconds. If it gets a 200 OK → pod is healthy. If it fails → restart the container.
#     It's a critical part of production deployments. FastAPI makes this trivially easy.