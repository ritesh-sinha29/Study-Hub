# Background Tasks & File Uploads

```python
# ==========================================================
# FASTAPI STUDY GUIDE: 11. FILE UPLOADS & BACKGROUND TASKS
# ==========================================================

# --- WHAT IS UPLOADFILE? ---
# FastAPI lets you receive uploaded files using:
# 1. `bytes`: Reads the entire file into RAM. Good for small files only.
# 2. `UploadFile`: Recommended. It uses a temporary file on disk if the file exceeds a size limit.
#    This saves RAM. It also provides metadata like filename, content-type, and headers.
# Note: To use files, you must install the python-multipart package:
#   pip install python-multipart

# --- WHAT ARE BACKGROUND TASKS? ---
# Sometimes you need to perform a slow operation (like sending an email, writing logs,
# or processing an image) as a result of a request.
# You shouldn't make the user wait for this to finish before getting their response!
# FastAPI's `BackgroundTasks` lets you define a function to run *after* returning the response.

import time
import uvicorn
from fastapi import FastAPI, File, UploadFile, BackgroundTasks
from typing import List

app = FastAPI(title="FastAPI: File Uploads & Background Tasks")

# ==========================================================
# 1. FILE UPLOADS (SINGLE & MULTIPLE)
# ==========================================================

@app.post("/upload-single")
async def upload_single_file(file: UploadFile = File(...)):
    # You can read metadata:
    # - file.filename: Name of the file (e.g., "photo.jpg")
    # - file.content_type: MIME type (e.g., "image/jpeg")
    
    # To read file contents:
    contents = await file.read()  # Reads the file as bytes
    
    # Close the file to free up system resources
    await file.close()
    
    return {
        "filename": file.filename,
        "content_type": file.content_type,
        "size_bytes": len(contents),
        "message": "File received successfully!"
    }


@app.post("/upload-multiple")
async def upload_multiple_files(files: List[UploadFile] = File(...)):
    uploaded_files_info = []
    
    for file in files:
        # Just record the metadata (without reading all bytes to keep it fast)
        uploaded_files_info.append({
            "filename": file.filename,
            "content_type": file.content_type
        })
        await file.close()
        
    return {
        "files_count": len(files),
        "uploaded_files": uploaded_files_info
    }


# ==========================================================
# 2. BACKGROUND TASKS
# ==========================================================

# A standard Python function representing our slow background task
def write_log_report(email: str, message: str):
    # Simulate a slow email dispatch or PDF write (5 seconds)
    print(f"[Background Task] Start: Generating report for {email}...")
    time.sleep(5)
    print(f"[Background Task] Success: Report email sent to {email}! Message: '{message}'")


# Endpoint that schedules the background task
@app.post("/request-report")
async def request_report(email: str, background_tasks: BackgroundTasks):
    # Schedule the task: (task_function, arg1, arg2...)
    # The client will receive the return response IMMEDIATELY.
    # The function `write_log_report` will run in the background after the response is sent.
    background_tasks.add_task(write_log_report, email, "Your report is attached below.")
    
    return {
        "status": "Request received",
        "message": f"Your report request has been scheduled. An email will be sent to {email} shortly."
    }


# ----------------------------------------------------------
# HOW TO RUN THIS FILE
# ----------------------------------------------------------
if __name__ == "__main__":
    uvicorn.run("11_background_tasks_and_files:app", host="127.0.0.1", port=8000, reload=True)


# --- QUICK SUMMARY FOR RETESTING ---
# 1. Run this file: `python 11_background_tasks_and_files.py`
# 2. Go to: http://127.0.0.1:8000/docs
# 3. Try `/upload-single` by uploading any small text file or image.
# 4. Try `/request-report` with your email.
#    * Watch Swagger return the success response immediately (0 seconds delay).
#    * Check your Python terminal! After 5 seconds, you will see the prints:
#      `[Background Task] Success: Report email sent to ...` showing it executed in the background.


# ==========================================================
# REAL-LIFE USE CASES
# ==========================================================

# 1. EMAIL NOTIFICATION ON SIGNUP (like any app)
#    - User hits POST /register → account is created.
#    - A background task sends the welcome email AFTER the response is returned.
#    - User gets instant response ("Account created!") + email arrives in a few seconds.
#    - Without BackgroundTasks: User waits 3-5 seconds for email server before response!

# 2. ORDER CONFIRMATION (like Swiggy / Amazon)
#    - POST /orders → order saved to DB → response sent immediately.
#    - Background task: Send SMS + email + push notification to user.
#    - Background task: Notify restaurant/warehouse about the new order.
#    - All of this happens AFTER user sees "Order Placed Successfully!" — no waiting.

# 3. FILE PROCESSING (like resume parsing on Naukri.com)
#    - POST /upload-resume → file saved → user gets "Upload successful" response immediately.
#    - Background task: Parse the resume, extract skills, index them for search.
#    - This processing takes 10-30 seconds. User should NOT wait for this!

# 4. REPORT GENERATION (like any analytics dashboard)
#    - POST /reports/generate → user gets "Report is being generated" response.
#    - Background task: Run heavy DB queries, generate PDF, send download link via email.
#    - Report arrives in email in 2-3 minutes. User can use the app normally meanwhile.


# ==========================================================
# MNC INTERVIEW QUESTIONS & ANSWERS
# ==========================================================

# Q1. What are BackgroundTasks in FastAPI? When should you use them?
# A:  BackgroundTasks let you run a function AFTER the HTTP response is sent to the client.
#     Use them for tasks that:
#       - Are slow (email, SMS, PDF generation, image processing)
#       - The user doesn't need to wait for
#       - Must happen as a side effect of the request
#     DON'T use for: tasks that need to run in parallel on different servers.
#     For those, use a proper task queue: Celery + Redis or AWS SQS.

# Q2. What is the difference between BackgroundTasks and asyncio tasks in FastAPI?
# A:  BackgroundTasks → Runs AFTER the response is sent. Single server. Simple to use.
#                        Best for: quick side effects (sending 1 email, writing 1 log).
#     asyncio tasks (asyncio.create_task) → Runs concurrently WITH request handling.
#                        Best for: parallel async operations within a single request.
#     Celery (external) → Runs on SEPARATE worker machines. Survives server restarts.
#                        Best for: heavy jobs (video encoding, ML inference, bulk emails).
#     MNC tip: For anything that takes > 10 seconds, use Celery. For quick side effects, BackgroundTasks.

# Q3. What is UploadFile in FastAPI and why is it better than `bytes`?
# A:  `file: bytes` → Reads the ENTIRE file into RAM at once.
#                     Problem: A 1GB video file would crash your server!
#     `file: UploadFile` → Uses a spooled temp file on disk if file is large.
#                           RAM is NOT exhausted. File metadata is available.
#                           Can be read in chunks: await file.read(1024)
#     Always use UploadFile for production file upload endpoints.

# Q4. What library must be installed to handle file uploads in FastAPI?
# A:  `python-multipart` must be installed:
#       pip install python-multipart
#     Without it, FastAPI will raise a RuntimeError when you try to handle
#     form data or file uploads. This is a very common "it worked yesterday" bug!

# Q5. How does FastAPI's BackgroundTasks differ from Celery? When would you use Celery at an MNC?
# A:  BackgroundTasks:
#       - Built into FastAPI. No extra setup.
#       - Runs in the SAME process as the web server.
#       - If server restarts mid-task → task is LOST.
#       - Good for: sending 1 email, logging, minor cleanup.
#     Celery:
#       - Separate worker processes. Often on separate servers.
#       - Tasks are stored in a broker (Redis/RabbitMQ). Survives restarts.
#       - Supports retries, scheduling, task chaining, rate limiting.
#       - Good for: bulk email campaigns, video processing, nightly reports.
#     Rule at MNCs: Any task taking > 5-10 seconds or needs retry logic → use Celery.
```
