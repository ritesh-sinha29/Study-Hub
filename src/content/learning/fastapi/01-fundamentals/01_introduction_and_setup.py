# ==========================================================
# FASTAPI STUDY GUIDE: 01. INTRODUCTION & SETUP
# ==========================================================

# --- WHAT IS AN API? ---
# API stands for Application Programming Interface.
# It acts as a bridge that allows different software applications to talk to each other.
# Think of it like a waiter in a restaurant:
# 1. You (the client/frontend) look at the menu and order food (Request).
# 2. The waiter (the API) takes your order to the kitchen (database/server logic).
# 3. The kitchen cooks the food and gives it to the waiter.
# 4. The waiter brings the food back to your table (Response).

# --- WHAT IS FASTAPI? ---
# FastAPI is a modern, fast (high-performance) web framework for building APIs with Python.
# Key benefits:
# * Extremely Fast: On par with NodeJS and Go (thanks to Starlette and Uvicorn).
# * Automatic Docs: Generates interactive API documentation (Swagger UI) automatically!
# * Type Hints: Uses standard Python type hints for automatic data validation and editor autocompletion.
# * Easy: Designed to be easy to learn and write.

# --- PRE-REQUISITES (HOW TO INSTALL) ---
# To run this code, you need to install two libraries:
# 1. fastapi - The framework itself.
# 2. uvicorn - An ASGI (Asynchronous Server Gateway Interface) web server that runs your code.
#
# Run this command in your terminal:
#   pip install fastapi uvicorn

import uvicorn
from fastapi import FastAPI

# 1. CREATE AN APP INSTANCE
# This `app` object is the main entry point of your web application.
# It manages all routing, configuration, and middleware.
app = FastAPI(
    title="FastAPI Learning Journey",
    description="Starting from absolute scratch!",
    version="1.0.0"
)

# 2. DEFINE A ROUTE (PATH OPERATION)
# @app.get("/") is a decorator. It tells FastAPI: "If someone visits the root URL (/)
# using the HTTP GET method, run the function below."
#
# Common HTTP Methods:
# - GET: Fetch data (read only)
# - POST: Create new data
# - PUT: Update existing data
# - DELETE: Remove data
@app.get("/")
async def root():
    # Inside FastAPI, we write standard or async functions.
    # FastAPI automatically converts dictionaries, lists, and strings into JSON format!
    return {
        "message": "Welcome to FastAPI, Ritesh!",
        "status": "Learning from scratch",
        "next_step": "Go to http://localhost:8000/docs in your browser!"
    }

# 3. ANOTHER ROUTE (ANOTHER ENDPOINT)
@app.get("/about")
async def about():
    return {
        "topic": "FastAPI Introduction",
        "difficulty": "Beginner",
        "description": "FastAPI is great because it has automatic validation!"
    }


# ----------------------------------------------------------
# HOW TO RUN THIS FILE
# ----------------------------------------------------------
# Open your terminal in this folder and run:
#   python 01_introduction_and_setup.py
# OR
#   uvicorn 01_introduction_and_setup:app --reload
#
# Then visit:
#   http://localhost:8000/docs     ← Swagger UI (interactive)
#   http://localhost:8000/redoc    ← ReDoc UI
# ----------------------------------------------------------
if __name__ == "__main__":
    print("Starting FastAPI server..")
    print("Visit Swagger Documentation at: http://localhost:8000/docs")
    print("Visit ReDoc Documentation at: http://localhost:8000/redoc")
    uvicorn.run("01_introduction_and_setup:app", host="127.0.0.1", port=8000, reload=True)


# --- HOW TO RUN THIS APPLICATION ---
# You can run this file in two ways:
#
# Method A: From the Terminal (Recommended for development)
#   Open terminal in this directory and type:
#     uvicorn 01_introduction_and_setup:app --reload
#   * '01_introduction_and_setup' is the name of this Python file (without .py)
#   * 'app' is the FastAPI instance we created inside this file
#   * '--reload' makes the server restart automatically whenever you change the code!
#
# Method B: Direct Python Execution (Runs this main block)
#   Simply run this script directly with Python:
#     python 01_introduction_and_setup.py
#   This starts the server programmatically.

# ==========================================================
# REAL-LIFE USE CASES
# ==========================================================

# 1. PAYMENT GATEWAY API (like Razorpay / Stripe)
#    - **Step 1**: Frontend (React) calls POST /payments → FastAPI backend processes payment.
#    - **Step 2**: FastAPI is used because of its speed and async support.
#    - **Result**: The /docs page is shared with partner companies to integrate quickly.
#
# 2. PRODUCT CATALOG (like Flipkart / Amazon)
#    - **Step 1**: Mobile apps send GET /products to fetch product listings.
#    - **Result**: FastAPI auto-validates the response so broken/missing data never reaches the app.
#
# 3. INTERNAL MICROSERVICE (like Swiggy's order service)
#    - **Step 1**: A company has 10 microservices (orders, payments, notifications..).
#    - **Step 2**: Each service is a separate FastAPI app.
#    - **Result**: They communicate with each other using HTTP calls or message queues.
#
# 4. DATA SCIENCE / ML MODEL SERVING
#    - **Step 1**: A trained ML model (like fraud detection) is wrapped in a FastAPI endpoint.
#    - **Step 2**: Data engineers call POST /predict with transaction data → FastAPI returns prediction.
#    - **Result**: Companies like Walmart, HDFC Bank use this pattern in production.


# ==========================================================
# MNC INTERVIEW QUESTIONS & ANSWERS
# ==========================================================

# Q1. What is FastAPI and why is it faster than Flask or Django REST?
# A:  FastAPI is an ASGI (Asynchronous Server Gateway Interface) framework.
#     It uses Uvicorn + Starlette underneath, which supports `async/await` natively.
#     Flask is WSGI (synchronous) — it handles ONE request at a time per worker.
#     FastAPI handles thousands of concurrent requests WITHOUT creating new threads.
#     Benchmarks: FastAPI is 2-3x faster than Flask for I/O-bound tasks (DB calls, HTTP calls).

# Q2. What is the difference between WSGI and ASGI?
# A:  WSGI (Web Server Gateway Interface) → Synchronous. One request blocks until complete.
#         Used by: Flask, Django
#     ASGI (Async Server Gateway Interface) → Asynchronous. Multiple requests handled concurrently.
#         Used by: FastAPI, Django Channels
#     Think of WSGI as a single cashier (one at a time). ASGI as a cashier who starts your
#     order, helps the next person, then comes back when yours is ready.

# Q3. What is Uvicorn and why do we need it?
# A:  Uvicorn is an ASGI server — it's the "web server" that actually listens for HTTP connections.
#     FastAPI itself is just a framework (it defines routes and logic).
#     Uvicorn runs FastAPI, handles TCP connections, HTTP parsing, and dispatches requests.
#     For production, we use Gunicorn with multiple Uvicorn worker processes.
#         Command: gunicorn -k uvicorn.workers.UvicornWorker main:app

# Q4. What is OpenAPI and how does FastAPI use it?
# A:  OpenAPI (formerly Swagger) is a standard specification for describing REST APIs.
#     FastAPI automatically generates an openapi.json file from your code.
#     You can view it at: http://localhost:8000/openapi.json
#     Swagger UI (/docs) and ReDoc (/redoc) are just pretty viewers of that JSON spec.
#     This means: You write code → FastAPI generates documentation AUTOMATICALLY.

# Q5. How does FastAPI handle async functions vs regular functions?
# A:  `async def` → FastAPI runs it in the async event loop. Perfect for DB calls, HTTP calls.
#     `def` (regular) → FastAPI runs it in a separate thread pool to avoid blocking the loop.
#     Best practice:
#       - Use `async def` when calling async libraries (like databases, httpx, aiofiles).
#       - Use `def` for CPU-heavy tasks or when using sync libraries (like requests).
#     NEVER call blocking code (time.sleep, requests.get) inside `async def`!

