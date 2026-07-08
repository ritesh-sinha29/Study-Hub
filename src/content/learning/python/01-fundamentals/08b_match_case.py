# ==========================================================
# PYTHON MATCH-CASE / SWITCH-CASE (FOR BEGINNERS)
# ==========================================================

# --- WHAT IS MATCH-CASE? ---
# Match-case (introduced in Python 3.10) is Python's version of a "switch-case" statement.
# It is a modern, clean, and powerful alternative to writing long chains of `if-elif-else` statements.
#
# Instead of checking conditions manually:
#   if command == "start": ..
#   elif command == "stop": ..
#
# You match a value against patterns:
#   match command:
#       case "start": ..
#       case "stop": ..

# --- WHY USE IT? ---
# 1. Cleaner readability when checking a single variable against many values.
# 2. Pattern Matching: It can match complex structures (like lists and dictionaries) and extract values from them.
#
# **HOW IT WORKS INTERNALLY:** match-case is NOT just if-elif sugar. Python's
# structural pattern matching actually deconstructs the matched value against
# each case pattern. This means cases can bind sub-parts of the value to
# local names automatically (e.g., `case {"role": role}` extracts the role).
#
# GUARD CLAUSES: You can add an `if` condition inside a case:
#   case x if x > 100:   <- only matches numbers greater than 100
#
# **KEY INSIGHT:** The `_` wildcard case matches **EVERYTHING** and doesn't bind a
# name. Always put it last — it acts as the default/else branch.


# ==========================================================
# 1. BASIC MATCH-CASE
# ==========================================================
# The `_` case acts as the wildcard/default (equivalent to `else`).

def get_role_permission(role: str) -> str:
    match role:
        case "admin":
            return "Full access to everything."
        case "editor":
            return "Can edit and publish articles."
        case "viewer":
            return "Can only read content."
        case _:
            # Default case (runs if no other cases match)
            return "Unknown role. Access denied."


print("--- 1. BASIC MATCH-CASE ---")
print("Admin access:", get_role_permission("admin"))
print("Guest access:", get_role_permission("guest"))
print()


# ==========================================================
# 2. MATCHING MULTIPLE VALUES (OR)
# ==========================================================
# You can use the pipe `|` symbol to match multiple values in a single case block.

def get_http_status_message(status_code: int) -> str:
    match status_code:
        case 200 | 201:
            return "Success!"
        case 400 | 401 | 403 | 404:
            return "Client-side Error."
        case 500 | 502 | 503:
            return "Server-side Error."
        case _:
            return "Unknown status code."


print("--- 2. MATCHING MULTIPLE VALUES ---")
print("Status 200:", get_http_status_message(200))
print("Status 404:", get_http_status_message(404))
print()


# ==========================================================
# 3. MATCHING WITH CONDITIONS (IF GUARDS)
# ==========================================================
# You can add an `if` condition directly inside a `case` to refine when it matches.

def process_number(num: int):
    match num:
        case 0:
            print("Number is exactly zero.")
        case n if n > 0:
            # Matches any number > 0, and assigns it to the variable 'n'
            print(f"{n} is a positive number.")
        case n if n < 0:
            print(f"{n} is a negative number.")


print("--- 3. MATCHING WITH IF GUARDS ---")
process_number(0)
process_number(42)
process_number(-10)
print()


# ==========================================================
# 4. STRUCTURAL PATTERN MATCHING (ADVANCED)
# ==========================================================
# Match-case can inspect lists/tuples and extract variables from them.

def parse_command(command_parts: list[str]):
    match command_parts:
        case ["quit"] | ["exit"]:
            print("Shutting down..")
        case ["load", filename]:
            # Matches if the list has exactly two elements, and the first is "load".
            # The second element is stored in the variable 'filename'.
            print(f"Loading data from file: {filename}")
        case ["save", filename, "--force"]:
            print(f"Force saving data to: {filename}")
        case ["save", filename]:
            print(f"Saving data to: {filename}")
        case _:
            print("Unknown command format!")


print("--- 4. STRUCTURAL PATTERN MATCHING ---")
parse_command(["quit"])
parse_command(["load", "users.json"])
parse_command(["save", "backup.zip", "--force"])
parse_command(["delete", "everything"])  # Matches default case
print()

# ==========================================
# REAL-LIFE USE CASES
# ==========================================
# 1. API Response Router: Handling different JSON shapes and status codes
#    - **Step 1**: Cleanly in a single controller.
#
# 2. CLI Command Parser: Mapping user commands (e.g., 'git checkout <branch>',
#    - **Step 1**: 'git commit -m <msg>') to logical handlers.
#
# 3. State Machine Reducers: Updating application states based on action types
#    - **Step 1**: And payloads.

# ==========================================
# MNC INTERVIEW QUESTIONS & ANSWERS
# ==========================================
#
# Q1. What is the difference between match-case and if-elif-else in Python?
# A:  `if-elif-else` checks boolean expressions sequentially, which is simple
#     and fast for basic conditions. `match-case` (introduced in Python 3.10)
#     provides structural pattern matching. It does not just check values, but
#     also parses the shape, type, and structure of data, and binds matched
#     sub-components to local variables automatically. Use `if-elif-else` for
#     simple range/logical checks, and `match-case` for complex data shapes
#     (like JSON API routing, state machines, or parsing ASTs). See the
#     comparison table below:
#     
#     | Feature | match-case | if-elif-else |
#     | :--- | :--- | :--- |
#     | **Match Type** | Structure, shape, attributes | Boolean conditions only |
#     | **Variable Binding** | Automatically binds variables | Manually extract variables |
#     | **Readability** | High for complex nested structures | Can become complex and nested |
#
# Q2. What does the wildcard case _ represent in a match block?
# A:  The underscore `_` acts as a wildcard pattern. It matches absolutely
#     anything and acts as the 'default' fallback case (like 'else' in an
#     if-statement or 'default' in a C-style switch statement). It must always
#     be placed at the very end of the match block.
#
# Q3. How can you add conditions (guards) to a case pattern?
# A:  You can add an 'if' condition directly to a case pattern (e.g. `case [x,
#     y] if x == y:`). The pattern matches only if the shape is correct AND
#     the guard condition evaluates to True. This keeps routing logic clean
#     and cohesive.