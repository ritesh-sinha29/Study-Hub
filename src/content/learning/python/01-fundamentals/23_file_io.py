# ==========================================================
# PYTHON FILE INPUT / OUTPUT (FILE I/O) (FOR BEGINNERS)
# ==========================================================

# --- WHY IS FILE I/O IMPORTANT? ---
# File I/O (Input/Output) allows your program to read data from files on your disk
# and write data back to files.
#
# Examples of why we need this:
#   * Log Files: Recording when errors occur in your app.
#   * Config Files: Reading settings for your FastAPI application.
#   * Data Persistence: Saving user inputs or results so they aren't lost when the program closes.
#
# **HOW IT WORKS INTERNALLY:** When you open a file, the OS allocates a FILE
# DESCRIPTOR — an integer handle that represents the open connection to
# the file. All read/write calls go through this descriptor. Forgetting to
# close it leaks the descriptor (OS has a limit). The `with` statement
# guarantees `file.close()` is called even if an exception occurs.
#
# **BUFFERING:** Python writes to an in-memory buffer first, then flushes to
# disk. Call `file.flush()` or use `buffering=0` for unbuffered writes when
# you need data on disk immediately (e.g., real-time logging).
#
# **KEY INSIGHT:** Always specify `encoding='utf-8'` when opening text files:
#   `open("file.txt", "r", encoding="utf-8")`
# The default encoding is platform-dependent (UTF-8 on Linux/Mac, cp1252
# on Windows), which causes silent data corruption when sharing files.

import os

# ==========================================================
# 1. WRITING TO A FILE ('w' mode)
# ==========================================================
# To write to a file, use the `open()` function with mode `'w'` (write).
# WARNING: `'w'` mode will OVERWRITE the file if it already exists!
# The `with` statement is a context manager that automatically closes the file for you.

print("--- 1. WRITING TO A FILE ---")
with open("example.txt", "w") as file:  #YOU CAN WRITE ANYTHING I NSTEAD OF FILE
    file.write("Hello, Ritesh!\n")
    file.write("Welcome to Python File I/O.\n")
    file.write("Line 3: Writing data is easy.")

print("example.txt created and written successfully.")
print()


# ==========================================================
# 2. READING FROM A FILE ('r' mode)
# ==========================================================
# To read, use mode `'r'`. 

print("--- 2. READING FROM A FILE ---")

# Method A: Reading the entire file content at once
print(">> Method A: Read entire file")
with open("example.txt", "r") as file:
    content = file.read()
    print(content)

print()

# Method B: Reading line-by-line (highly memory efficient for large files)
print(">> Method B: Loop through lines")
with open("example.txt", "r") as file:
    for line in file:
        # We use strip() because each line already has a '\n' (newline) character
        print("Line:", line.strip())

print()


# ==========================================================
# 3. APPENDING TO A FILE ('a' mode)
# ==========================================================
# If you don't want to delete existing content, use mode `'a'` (append).
# This adds new text to the end of the file.

print("--- 3. APPENDING TO A FILE ---")
with open("example.txt", "a") as file:
    file.write("\nLine 4: This line was appended later!")

# Read the file again to show the change
with open("example.txt", "r") as file:
    print(file.read())
print()


# ==========================================================
# 4. SAFE FILE I/O WITH TRY/EXCEPT
# ==========================================================
# If you try to read a file that doesn't exist, Python will crash with `FileNotFoundError`.
# Always use `try/except` to make file reading safe!

print("--- 4. SAFE FILE I/O ---")
non_existent_file = "missing_file.txt"

try:
    with open(non_existent_file, "r") as file:
        data = file.read()
except FileNotFoundError:
    print(f"Error: The file '{non_existent_file}' does not exist! Program continues safely.")

print()


# ==========================================================
# 5. FASTAPI USE CASE — Logging Server Requests
# ==========================================================
# In FastAPI, we often log requests or errors to a file so we can view them later.

print("--- 5. FASTAPI LOGGING USE CASE ---")

def log_api_request(endpoint: str, status_code: int):
    # Appends request information to a log file
    log_message = f"[LOG] Request to '{endpoint}' returned status {status_code}\n"
    with open("server.log", "a") as log_file:
        log_file.write(log_message)

# Simulating two user hits
log_api_request("/users/me", 200)
log_api_request("/admin/settings", 403)

# Print log file content
print("Current Server Logs:")
with open("server.log", "r") as log_file:
    print(log_file.read())


# CLEANUP: Let's remove the files we created so we don't clutter your workspace
if os.path.exists("example.txt"):
    os.remove("example.txt")
if os.path.exists("server.log"):
    os.remove("server.log")

# ==========================================
# REAL-LIFE USE CASES
# ==========================================
#
# 1. Log Exporter Service: Appending trace warnings and error logs to a local
#    file using append mode.
#
# 2. Local Storage Database: Saving application JSON settings files locally.
#
# 3. Bulk Report Generation: Creating CSV file reports on disk from lists of
#    databases.

# ==========================================
# MNC INTERVIEW QUESTIONS & ANSWERS
# ==========================================
#
# Q1. Why should you always use the 'with' statement when opening files in
#     Python?
# A:  The 'with' statement implements the context manager protocol. It
#     guarantees that the file is closed automatically once the code block
#     exits, even if an exception is raised inside the block. This prevents
#     file descriptors/resource leaks.
#
# Q2. What are the differences between 'w', 'a', and 'x' file opening modes?
# A:  `'w'` mode opens a file for writing, completely overwriting the existing
#     content or creating the file if it does not exist. `'a'` mode opens a
#     file for writing, but appends all new text to the end of the file
#     without deleting existing data. `'x'` mode (exclusive creation) opens a
#     file for writing, but throws a `FileExistsError` if the file already
#     exists, ensuring you never accidentally overwrite existing data. See the
#     comparison table below:
#     
#     | Mode | Action | If File Exists | If File Doesn't Exist |
#     | :--- | :--- | :--- | :--- |
#     | `'w'` | Write | Overwrites contents | Creates new file |
#     | `'a'` | Append | Appends to the end | Creates new file |
#     | `'x'` | Exclusive Write| Raises `FileExistsError` | Creates new file |
#
# Q3. What is the difference between read(), readline(), and readlines()?
# A:  `read()` reads the entire file into a single string, which is simple but
#     can consume massive memory for large files. `readline()` reads a single
#     line from the file at a time, making it highly memory-efficient.
#     `readlines()` reads all lines from the file and returns them as a list
#     of strings. For large files, it is best to iterate directly over the
#     file object (`for line in file:`), which uses `readline()` internally to
#     keep memory usage extremely low. See the comparison table below:
#     
#     | Method | Returns | Reads | Memory Usage |
#     | :--- | :--- | :--- | :--- |
#     | `read()` | String | Entire file content | High (loads whole file) |
#     | `readline()` | String | One line at a time | Low (one line in memory) |
#     | `readlines()` | List of strings | All lines as a list | High (loads whole list) |