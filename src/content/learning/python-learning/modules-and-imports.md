# Modules And Imports

## PYTHON MODULES & IMPORTS (FOR BEGINNERS)

## WHAT IS A MODULE?

A module is simply a PYTHON FILE (.py) that contains code (functions, classes, variables).
You can IMPORT that code into another file to reuse it.
This lets you split your project into small, organized files.

## REAL-WORLD USE CASES

* FastAPI: Your routes, models, and database code live in separate files
           and you import them in main.py
* LangGraph: Different AI agents/nodes live in separate files and get imported
* Every Python project: Use built-in modules like `json`, `os`, `datetime`

```python
print("==========================================")
print("1. IMPORTING BUILT-IN MODULES")
print("==========================================")
```

Python comes with many built-in modules — no installation needed

```python
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
```

```python
print("2. IMPORT SPECIFIC THINGS FROM A MODULE")
print("==========================================")
```

Instead of importing the whole module, import only what you need
Syntax: from module_name import thing_you_want

```python
from math import sqrt, pi
from random import choice
from datetime import datetime

print("sqrt(25):", sqrt(25))
print("Pi:", pi)
print("Random choice:", choice(["apple", "banana", "mango"]))
print("Current time:", datetime.now())

print()
```

```python
print("3. IMPORT WITH AN ALIAS (nickname)")
print("==========================================")
```

You can give a module a shorter nickname using `as`

```python
import datetime as dt
import os as operating_system

print("Today:", dt.date.today())
print("Working folder:", operating_system.getcwd())

print()
```

```python
print("4. THE OS MODULE — very useful for FastAPI projects")
print("==========================================")
```

os.environ lets you read environment variables (like API keys)
This is how FastAPI reads your secret keys safely

```python
import os
```

Set a fake environment variable for demonstration:

```python
os.environ["APP_NAME"] = "My FastAPI App"
os.environ["VERSION"] = "1.0"
```

Read it back:

```python
print("App Name:", os.environ.get("APP_NAME"))
print("Version:", os.environ.get("VERSION"))
print("A missing key:", os.environ.get("MISSING_KEY", "default_value"))

print()
```

```python
print("5. HOW FASTAPI PROJECT IMPORTS LOOK")
print("==========================================")
```

In a real FastAPI project, files are organized like this:

my_project/
  ├── main.py          ← Entry point, creates the FastAPI app
  ├── routes/
  │   ├── users.py     ← All /users routes
  │   └── items.py     ← All /items routes
  ├── models/
  │   └── user_model.py  ← Pydantic models (classes)
  └── database.py      ← Database connection

In main.py, you would write:

```python
from fastapi import FastAPI
  from routes.users import router as users_router
  from routes.items import router as items_router

  app = FastAPI()
```

app.include_router(users_router)
  app.include_router(items_router)

```python
print("FastAPI import structure shown in comments above.")
print("Run: python main.py to start a FastAPI server.")

print()
```

```python
print("6. COMMON FASTAPI IMPORTS you will use daily")
print("==========================================")
```

These are the most common import lines in any FastAPI project:

```python
from fastapi import FastAPI, HTTPException, Depends
  from pydantic import BaseModel
  from typing import Optional, List
  import os
  import json
  import asyncio
```

```python
print("from fastapi import FastAPI, HTTPException  ← Core FastAPI tools")
print("from pydantic import BaseModel              ← For data models (classes)")
print("from typing import Optional, List           ← For type hints")
print("import os                                   ← For reading environment variables")
print("import json                                 ← For handling JSON data")
print("import asyncio                              ← For async/await support")
```

