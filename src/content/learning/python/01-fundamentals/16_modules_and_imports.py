# ==========================================
# PYTHON MODULES & IMPORTS (FOR BEGINNERS)
# ==========================================

# --- WHAT IS A MODULE? ---
# A module is simply a PYTHON FILE (.py) that contains code (functions, classes, variables).
# You can IMPORT that code into another file to reuse it.
# This lets you split your project into small, organized files.

# --- REAL-WORLD USE CASES ---
# * FastAPI: Your routes, models, and database code live in separate files
#            and you import them in main.py
# * LangGraph: Different AI agents/nodes live in separate files and get imported
# * Every Python project: Use built-in modules like `json`, `os`, `datetime`
#
# HOW IT WORKS INTERNALLY: When you `import math`, Python searches `sys.path`
# in order: (1) current script directory, (2) PYTHONPATH env var, (3) standard
# library, (4) site-packages (pip installs). The first match wins.
# Once a module is imported, Python caches it in `sys.modules`. Subsequent
# imports of the same module return the cached version instantly.
#
# __pycache__: Python compiles .py files to bytecode (.pyc) on first import
# and caches them in a __pycache__ folder. On future imports, it loads the
# faster bytecode directly, skipping re-parsing the source file.
#
# KEY INSIGHT: The `if __name__ == '__main__':` guard runs code only when the
# file is executed directly (not when it's imported as a module). This is the
# standard pattern for making files both importable and runnable.

print("==========================================")
print("1. IMPORTING BUILT-IN MODULES")
print("==========================================")

# Python comes with many built-in modules — no installation needed

import math                 # Math functions
import random               # Random number generation
import datetime             # Date and time
import os                   # Operating system functions

print("Square root of 16:", math.sqrt(16))
print("Pi:", math.pi)
print("Random number (1-10):", random.randint(1, 10))
print("Today's date:", datetime.date.today())
print("Current directory:", os.getcwd())

print()

# ==========================================
print("2. IMPORT SPECIFIC THINGS FROM A MODULE")
print("==========================================")

# Instead of importing the whole module, import only what you need
# Syntax: from module_name import thing_you_want

from math import sqrt, pi
from random import choice
from datetime import datetime

print("sqrt(25):", sqrt(25))
print("Pi:", pi)
print("Random choice:", choice(["apple", "banana", "mango"]))
print("Current time:", datetime.now())

print()

# ==========================================
print("3. IMPORT WITH AN ALIAS (nickname)")
print("==========================================")

# You can give a module a shorter nickname using `as`

import datetime as dt
import os as operating_system

print("Today:", dt.date.today())
print("Working folder:", operating_system.getcwd())

print()

# ==========================================
print("4. THE OS MODULE — very useful for FastAPI projects")
print("==========================================")

# os.environ lets you read environment variables (like API keys)
# This is how FastAPI reads your secret keys safely

import os

# Set a fake environment variable for demonstration:
os.environ["APP_NAME"] = "My FastAPI App"
os.environ["VERSION"] = "1.0"

# Read it back:
print("App Name:", os.environ.get("APP_NAME"))
print("Version:", os.environ.get("VERSION"))
print("A missing key:", os.environ.get("MISSING_KEY", "default_value"))

print()

# ==========================================
print("5. HOW FASTAPI PROJECT IMPORTS LOOK")
print("==========================================")

# In a real FastAPI project, files are organized like this:
#
#   my_project/
#   ├── main.py          ← Entry point, creates the FastAPI app
#   ├── routes/
#   │   ├── users.py     ← All /users routes
#   │   └── items.py     ← All /items routes
#   ├── models/
#   │   └── user_model.py  ← Pydantic models (classes)
#   └── database.py      ← Database connection

# In main.py, you would write:
#
#   from fastapi import FastAPI
#   from routes.users import router as users_router
#   from routes.items import router as items_router
#
#   app = FastAPI()
#   app.include_router(users_router)
#   app.include_router(items_router)

print("FastAPI import structure shown in comments above.")
print("Run: python main.py to start a FastAPI server.")

print()

# ==========================================
print("6. COMMON FASTAPI IMPORTS you will use daily")
print("==========================================")

# These are the most common import lines in any FastAPI project:
# 
#   from fastapi import FastAPI, HTTPException, Depends
#   from pydantic import BaseModel
#   from typing import Optional, List
#   import os
#   import json
#   import asyncio

print("from fastapi import FastAPI, HTTPException  ← Core FastAPI tools")
print("from pydantic import BaseModel              ← For data models (classes)")
print("from typing import Optional, List           ← For type hints")
print("import os                                   ← For reading environment variables")
print("import json                                 ← For handling JSON data")
print("import asyncio                              ← For async/await support")

# ==========================================
# REAL-LIFE USE CASES
# ==========================================
#
# 1. Utility Libraries: Organizing codebase into separate helper modules
#    (e.g., string_helpers.py, db.py).
#
# 2. Project Packaging: Structuring codebase inside nested folders for modular
#    importing.
#
# 3. Third-Party SDKs: Importing pre-built code packages (like requests,
#    numpy) to extend functionality.

# ==========================================
# MNC INTERVIEW QUESTIONS & ANSWERS
# ==========================================
#
# Q1. What is the Python search path (sys.path), and how does Python resolve
#     imports?
# A:  sys.path is a list of directories Python searches when resolving
#     imports. It resolves in order: 1) the directory of the executing script,
#     2) directories in the PYTHONPATH env var, and 3) the system-wide
#     site-packages (where pip packages are installed).
#
# Q2. What are circular imports, and how can they be fixed?
# A:  Circular imports occur when module A imports module B, and module B
#     imports module A, creating a loop. Fixes include: 1) refactoring common
#     code into a third module, 2) importing inside functions (local imports)
#     instead of at the top of the file, or 3) importing modules instead of
#     symbols.
#
# Q3. What is the role of __init__.py in Python modules?
# A:  In older Python versions, __init__.py was required to mark a directory
#     as a package. In modern Python, it is optional (Namespace Packages), but
#     still useful to run package-level initialization, define package
#     metadata (__version__), and control public exports via __all__.