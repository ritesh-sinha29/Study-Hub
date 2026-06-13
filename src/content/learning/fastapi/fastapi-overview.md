# Fastapi Overview

FastAPI - Introduction & Setup

# What is FastAPI?

```python
FastAPI is a modern, fast (high-performance) web framework for building APIs with Python, based on standard Python type hints.
```

# Installation

```python
```bash
pip install fastapi
pip install uvicorn[standard]
```

Or with Poetry:
```bash
poetry add fastapi uvicorn
```
```

# Basic App

```python
```python
from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def read_root():
    return {"message": "Hello World"}
```

Run with:
```bash
uvicorn main:app --reload
```
```

# Key Features

```python
- **Fast**: Very high performance, on par with NodeJS and Go
- **Type Hints**: Leverages Python type hints for validation and docs
- **Automatic Docs**: Interactive API documentation (Swagger UI + ReDoc)
- **Async Support**: Built-in async/await support
- **Dependency Injection**: Built-in DI system
- **Security**: Built-in support for OAuth2, JWT, etc.
```

