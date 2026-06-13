# Environment Variables

```python
# ==========================================
# ENVIRONMENT VARIABLES (FOR BEGINNERS)
# ==========================================

# --- WHAT ARE ENVIRONMENT VARIABLES? ---
# Environment variables are SECRET pieces of information stored OUTSIDE your code.
# Things like API keys, database passwords, and secret tokens should NEVER
# be written directly in your code (someone could steal them from GitHub!).
# Instead, you store them in a special file called `.env` and read them in Python.

# --- SIMPLE ANALOGY ---
# Your code is like a public notice board — anyone can read it.
# Environment variables are like a locked safe — only your app can open it.

# --- REAL-WORLD USE CASES ---
# * FastAPI: Store database URL, JWT secret key, OpenAI API key in .env
# * LangGraph: Store your LLM provider API keys (OpenAI, Anthropic, Google)
# * All projects: NEVER hardcode secrets in your code!

import os  # Built-in module to access environment variables

print("==========================================")
print("1. SETTING AND READING ENV VARIABLES WITH os")
print("==========================================")

# Set environment variables (normally done in .env file, not in code):
os.environ["APP_NAME"] = "My FastAPI App"
os.environ["APP_VERSION"] = "1.0.0"
os.environ["DEBUG_MODE"] = "True"

# Read them:
app_name = os.environ.get("APP_NAME")
app_version = os.environ.get("APP_VERSION")

print("App Name:", app_name)
print("App Version:", app_version)

# If the variable doesn't exist, use a default value:
db_url = os.environ.get("DATABASE_URL", "sqlite:///./test.db")
print("Database URL:", db_url)

print()

# ==========================================
print("2. CREATING A .env FILE")
print("==========================================")

# A .env file looks like this (plain text, no quotes):
#
#   APP_NAME=My FastAPI App
#   DATABASE_URL=postgresql://user:password@localhost/mydb
#   OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxx
#   SECRET_KEY=mysupersecretkey123
#   DEBUG=True

# Let's create a sample .env file to demonstrate:
env_content = """APP_NAME=My FastAPI App
DATABASE_URL=sqlite:///./myapp.db
SECRET_KEY=mysecretkey_do_not_share
DEBUG=True
OPENAI_API_KEY=sk-fake-key-for-demo-only
"""

with open(".env.example", "w") as f:
    f.write(env_content)

print("Created .env.example file successfully!")
print("In a real project, rename this to .env and add to .gitignore")

print()

# ==========================================
print("3. READING .env FILE WITH python-dotenv")
print("==========================================")

# The `python-dotenv` package reads your .env file automatically.
# Install it with: pip install python-dotenv

# Real usage in FastAPI projects:
#
#   from dotenv import load_dotenv
#   import os
#
#   load_dotenv()  # Reads .env file and loads all variables
#
#   DATABASE_URL = os.environ.get("DATABASE_URL")
#   SECRET_KEY   = os.environ.get("SECRET_KEY")
#   OPENAI_KEY   = os.environ.get("OPENAI_API_KEY")

print("To use python-dotenv:")
print("  pip install python-dotenv")
print()
print("Then in your Python file:")
print("  from dotenv import load_dotenv")
print("  load_dotenv()                          # Reads .env file")
print("  key = os.environ.get('OPENAI_API_KEY') # Reads the value")

print()

# ==========================================
print("4. FASTAPI USE CASE — Settings class with env vars")
print("==========================================")

# In FastAPI, the best practice is to create a Settings class
# that reads all your configuration from environment variables.

# Real FastAPI pattern (with pydantic-settings):
#
#   from pydantic_settings import BaseSettings
#
#   class Settings(BaseSettings):
#       app_name: str = "My API"
#       database_url: str
#       secret_key: str
#       openai_api_key: str
#       debug: bool = False
#
#       class Config:
#           env_file = ".env"  # Automatically reads from .env file!
#
#   settings = Settings()
#   print(settings.app_name)
#   print(settings.database_url)

# Here we simulate it using os.environ:
class Settings:
    def __init__(self):
        self.app_name    = os.environ.get("APP_NAME", "Default App")
        self.secret_key  = os.environ.get("SECRET_KEY", "change_this_in_production")
        self.debug       = os.environ.get("DEBUG", "False") == "True"

settings = Settings()
print("App Name:", settings.app_name)
print("Debug Mode:", settings.debug)
print("Secret Key:", settings.secret_key[:10] + "***")  # Only show first 10 chars

print()

# ==========================================
print("5. IMPORTANT RULES for environment variables")
print("==========================================")
print("  1. NEVER hardcode secrets (API keys, passwords) in your .py files")
print("  2. ALWAYS add .env to your .gitignore file")
print("  3. Create a .env.example file (without real values) for teammates")
print("  4. Use os.environ.get('KEY', 'default') to avoid crashes if key is missing")
print("  5. For production, use your hosting platform's secret manager (e.g., Railway, Render)")
```
