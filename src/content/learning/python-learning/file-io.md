# File Io

## PYTHON FILE INPUT / OUTPUT (FILE I/O) (FOR BEGINNERS)

## WHY IS FILE I/O IMPORTANT?

File I/O (Input/Output) allows your program to read data from files on your disk 
and write data back to files.

Examples of why we need this:
  * Log Files: Recording when errors occur in your app.
  * Config Files: Reading settings for your FastAPI application.
  * Data Persistence: Saving user inputs or results so they aren't lost when the program closes.

```python
import os
```

## 1. WRITING TO A FILE ('w' mode)

To write to a file, use the `open()` function with mode `'w'` (write).
WARNING: `'w'` mode will OVERWRITE the file if it already exists!
The `with` statement is a context manager that automatically closes the file for you.

```python
print("--- 1. WRITING TO A FILE ---")
with open("example.txt", "w") as file:  #YOU CAN WRITE ANYTHING I NSTEAD OF FILE
    file.write("Hello, Ritesh!\n")
    file.write("Welcome to Python File I/O.\n")
    file.write("Line 3: Writing data is easy.")

print("example.txt created and written successfully.")
print()
```

## 2. READING FROM A FILE ('r' mode)

To read, use mode `'r'`.

```python
print("--- 2. READING FROM A FILE ---")
```

Method A: Reading the entire file content at once

```python
print(">> Method A: Read entire file")
with open("example.txt", "r") as file:
    content = file.read()
    print(content)

print()
```

Method B: Reading line-by-line (highly memory efficient for large files)

```python
print(">> Method B: Loop through lines")
with open("example.txt", "r") as file:
    for line in file:
        # We use strip() because each line already has a '\n' (newline) character
        print("Line:", line.strip())

print()
```

## 3. APPENDING TO A FILE ('a' mode)

If you don't want to delete existing content, use mode `'a'` (append).
This adds new text to the end of the file.

```python
print("--- 3. APPENDING TO A FILE ---")
with open("example.txt", "a") as file:
    file.write("\nLine 4: This line was appended later!")
```

Read the file again to show the change

```python
with open("example.txt", "r") as file:
    print(file.read())
print()
```

## 4. SAFE FILE I/O WITH TRY/EXCEPT

If you try to read a file that doesn't exist, Python will crash with `FileNotFoundError`.
Always use `try/except` to make file reading safe!

```python
print("--- 4. SAFE FILE I/O ---")
non_existent_file = "missing_file.txt"

try:
    with open(non_existent_file, "r") as file:
        data = file.read()
except FileNotFoundError:
    print(f"Error: The file '{non_existent_file}' does not exist! Program continues safely.")

print()
```

## 5. FASTAPI USE CASE — Logging Server Requests

In FastAPI, we often log requests or errors to a file so we can view them later.

```python
print("--- 5. FASTAPI LOGGING USE CASE ---")

def log_api_request(endpoint: str, status_code: int):
    # Appends request information to a log file
    log_message = f"[LOG] Request to '{endpoint}' returned status {status_code}\n"
    with open("server.log", "a") as log_file:
        log_file.write(log_message)
```

Simulating two user hits

```python
log_api_request("/users/me", 200)
log_api_request("/admin/settings", 403)
```

Print log file content

```python
print("Current Server Logs:")
with open("server.log", "r") as log_file:
    print(log_file.read())
```

CLEANUP: Let's remove the files we created so we don't clutter your workspace

```python
if os.path.exists("example.txt"):
    os.remove("example.txt")
if os.path.exists("server.log"):
    os.remove("server.log")
```

