# ==========================================================
# FASTAPI STUDY GUIDE: 08. DATABASE CRUD (SQLITE & ORM)
# ==========================================================

# --- WHAT IS AN ORM AND CRUD? ---
# ORM (Object-Relational Mapping) lets us interact with databases using Python classes 
# and objects instead of writing raw SQL queries.
# We will use SQLAlchemy 2.0, the industry standard ORM for Python.
#
# CRUD stands for:
# - Create (SQL: INSERT) -> HTTP POST
# - Read (SQL: SELECT) -> HTTP GET
# - Update (SQL: UPDATE) -> HTTP PUT / PATCH
# - Delete (SQL: DELETE) -> HTTP DELETE
#
# We will use SQLite, a lightweight, file-based database that requires NO configuration!

import uvicorn
from fastapi import FastAPI, Depends, HTTPException, status
from pydantic import BaseModel, Field
from typing import List, Union

# SQLAlchemy Imports
from sqlalchemy import create_engine, String, Boolean
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, sessionmaker, Session

# ==========================================================
# 1. DATABASE SETUP
# ==========================================================
# Database file location
SQLALCHEMY_DATABASE_URL = "sqlite:///./todos.db"

# Create Database Engine
# (connect_args={"check_same_thread": False} is required only for SQLite)
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# Create Session factory: each session is a database transaction
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for all database tables/models
class Base(DeclarativeBase):
    pass

# ==========================================================
# 2. ORM DATABASE TABLE MODEL (SQLAlchemy)
# ==========================================================
class TodoTable(Base):
    __tablename__ = "todos"
    
    # Modern SQLAlchemy 2.0 type-hint style
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str] = mapped_column(String(500), nullable=True)
    completed: Mapped[bool] = mapped_column(Boolean, default=False)

# Create all tables in the database (if they don't already exist)
Base.metadata.create_all(bind=engine)


# ==========================================================
# 3. PYDANTIC SCHEMAS (Data Validation)
# ==========================================================
# Schema for incoming request data (POST/Create)
class TodoCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=100, description="Title of the Todo item")
    description: Union[str, None] = Field(default=None, max_length=500)

# Schema for updating request data (PUT/Update)
class TodoUpdate(BaseModel):
    title: Union[str, None] = None
    description: Union[str, None] = None
    completed: Union[bool, None] = None

# Schema for outgoing response data (GET/Response)
class TodoResponse(BaseModel):
    id: int
    title: str
    description: Union[str, None]
    completed: bool
    
    # Config to tell Pydantic to read ORM objects (SQLAlchemy models)
    class Config:
        from_attributes = True


# ==========================================================
# 4. INITIALIZE FASTAPI & GET_DB DEPENDENCY
# ==========================================================
app = FastAPI(title="FastAPI: SQLite & SQLAlchemy CRUD")

# Dependency to get db session per request. Yields DB session, then closes it automatically.
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ==========================================================
# 5. CRUD ENDPOINTS (THE LOGIC)
# ==========================================================

# --- CREATE ---
@app.post("/todos", response_model=TodoResponse, status_code=status.HTTP_201_CREATED)
def create_todo(todo_in: TodoCreate, db: Session = Depends(get_db)):
    # Convert Pydantic model to SQLAlchemy Table instance
    new_todo = TodoTable(
        title=todo_in.title,
        description=todo_in.description
    )
    db.add(new_todo)  # Stage insertion
    db.commit()       # Commit transaction
    db.refresh(new_todo)  # Populate generated ID
    return new_todo

# --- READ ALL ---
@app.get("/todos", response_model=List[TodoResponse])
def get_all_todos(db: Session = Depends(get_db)):
    # Select * from todos
    todos = db.query(TodoTable).all()
    return todos

# --- READ ONE ---
@app.get("/todos/{todo_id}", response_model=TodoResponse)
def get_one_todo(todo_id: int, db: Session = Depends(get_db)):
    todo = db.query(TodoTable).filter(TodoTable.id == todo_id).first()
    if todo is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Todo with ID {todo_id} not found"
        )
    return todo

# --- UPDATE ---
@app.put("/todos/{todo_id}", response_model=TodoResponse)
def update_todo(todo_id: int, todo_in: TodoUpdate, db: Session = Depends(get_db)):
    db_todo = db.query(TodoTable).filter(TodoTable.id == todo_id).first()
    if db_todo is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Todo with ID {todo_id} not found"
        )
        
    # Update fields only if they were provided in the request body
    if todo_in.title is not None:
        db_todo.title = todo_in.title
    if todo_in.description is not None:
        db_todo.description = todo_in.description
    if todo_in.completed is not None:
        db_todo.completed = todo_in.completed
        
    db.commit()
    db.refresh(db_todo)
    return db_todo

# --- DELETE ---
@app.delete("/todos/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_todo(todo_id: int, db: Session = Depends(get_db)):
    db_todo = db.query(TodoTable).filter(TodoTable.id == todo_id).first()
    if db_todo is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Todo with ID {todo_id} not found"
        )
    db.delete(db_todo)
    db.commit()
    # 204 status code sends no body content back
    return None


# ----------------------------------------------------------
# HOW TO RUN THIS FILE
# ----------------------------------------------------------
if __name__ == "__main__":
    uvicorn.run("08_database_crud_sqlite:app", host="127.0.0.1", port=8000, reload=True)


# --- QUICK SUMMARY FOR RETESTING ---
# 1. Run this file: `python 08_database_crud_sqlite.py`
# 2. A file named `todos.db` will be created in this directory.
# 3. Go to: http://127.0.0.1:8000/docs
# 4. Try out POST `/todos` to add a task (e.g. title: "Learn FastAPI", description: "From scratch!").
# 5. Try GET `/todos` to see your saved tasks.
# 6. Try PUT `/todos/1` to toggle `"completed": true`.
# 7. Try DELETE `/todos/1` to delete the task.


# ==========================================================
# REAL-LIFE USE CASES
# ==========================================================

# 1. TODO / TASK MANAGER (like Jira / Trello / Notion)
#    - POST /tasks → create a new task (INSERT into DB)
#    - GET /tasks → fetch all tasks (SELECT * from DB)
#    - PUT /tasks/5 → mark task 5 as complete (UPDATE in DB)
#    - DELETE /tasks/5 → remove task (DELETE from DB)
#    - Every task management tool is built on top of CRUD operations.

# 2. USER MANAGEMENT (like any SaaS product)
#    - POST /users → register new user (INSERT)
#    - GET /users → admin lists all users (SELECT)
#    - PUT /users/10 → update profile (UPDATE)
#    - DELETE /users/10 → account deletion (DELETE)
#    - Companies like Freshworks, Zoho use this exact pattern.

# 3. BLOG / CMS PLATFORM (like Medium / WordPress API)
#    - POST /articles → author creates new post (INSERT)
#    - GET /articles → readers fetch all posts (SELECT)
#    - PUT /articles/3 → editor updates content (UPDATE)
#    - DELETE /articles/3 → author deletes post (DELETE)

# 4. INVENTORY MANAGEMENT (like Warehouse Management System)
#    - POST /products → add new product to inventory (INSERT)
#    - GET /products?category=electronics → filtered stock list (SELECT with filter)
#    - PUT /products/7 → update price or stock count (UPDATE)
#    - DELETE /products/7 → discontinue product (soft or hard DELETE)


# ==========================================================
# MNC INTERVIEW QUESTIONS & ANSWERS
# ==========================================================

# Q1. What is an ORM and why is SQLAlchemy used in FastAPI projects?
# A:  ORM (Object Relational Mapper) lets you interact with a database using Python objects
#     instead of writing raw SQL strings.
#     Without ORM:  db.execute("SELECT * FROM users WHERE id = 5")
#     With ORM:     db.query(User).filter(User.id == 5).first()
#     Why SQLAlchemy:
#       - Industry standard in Python. Used in Netflix, Reddit, Instagram, Dropbox.
#       - Prevents SQL injection attacks automatically.
#       - Works with any DB: SQLite, PostgreSQL, MySQL, Oracle.

# Q2. What is the difference between `db.add()`, `db.commit()`, and `db.refresh()`?
# A:  db.add(obj)     → Stages the object for insertion (like git add). NOT in DB yet.
#     db.commit()     → Writes the staged changes to the database permanently (like git commit).
#     db.refresh(obj) → Reloads the object from DB to get auto-generated values (like the new ID).
#     ALWAYS call refresh() after commit() when you need the generated primary key.

# Q3. What is the difference between SQLite and PostgreSQL? When do you use which?
# A:  SQLite:
#       - File-based database (no server needed). Perfect for development & learning.
#       - NOT for production (single writer, no concurrent connections).
#       - Created automatically: `sqlite:///./todos.db` creates a local file.
#     PostgreSQL:
#       - Full-featured database server. Used in ALL production systems.
#       - Handles thousands of concurrent connections.
#       - Used by: Instagram, Uber, Twitch, Shopify.
#     Rule: Use SQLite to learn/develop. Switch to PostgreSQL before going to production.

# Q4. What does `from_attributes = True` in Pydantic's Config class do?
# A:  By default, Pydantic models only accept dictionaries as input.
#     SQLAlchemy returns ORM objects (like `TodoTable` instances), not dicts.
#     `from_attributes = True` (was `orm_mode = True` in Pydantic v1) tells Pydantic:
#       "Hey, also accept ORM objects! Read attributes by name, not just dict keys."
#     Without it, `return todo_obj` in a route with `response_model=TodoResponse` would crash.

# Q5. What is the purpose of a `get_db` dependency with `yield` in FastAPI?
# A:  It follows the "open-use-close" pattern for database connections:
#       1. `db = SessionLocal()` → Opens a fresh DB connection/transaction.
#       2. `yield db` → Passes it to the route. The route does its DB work.
#       3. `finally: db.close()` → ALWAYS closes the connection, even if an error occurs.
#     Why this matters:
#       - DB connections are expensive resources. You must close them.
#       - Without `finally`, a crash in the route would leave the connection open forever,
#         eventually exhausting the connection pool. (Classic production bug!)
