#!/bin/bash

SRC="E:/Python-Learning/03-fastapi/01-fastapi-fundamentals"
DST="src/content/learning/fastapi"

mkdir -p "$DST"

generate_md() {
  local pyfile="$1"
  local mdname="$2"
  
  {
    echo "# $3"
    echo ""
    echo '```python'
    cat "$pyfile"
    echo '```'
  } > "$DST/$mdname.md"
  echo "Created $mdname.md"
}

generate_md "$SRC/01_introduction_and_setup.py" "introduction-and-setup" "Introduction & Setup"
generate_md "$SRC/02_path_parameters.py" "path-parameters" "Path Parameters"
generate_md "$SRC/03_query_parameters.py" "query-parameters" "Query Parameters"
generate_md "$SRC/04_request_body_pydantic.py" "request-body-pydantic" "Request Body & Pydantic"
generate_md "$SRC/05_response_models_and_status.py" "response-models-and-status" "Response Models & Status Codes"
generate_md "$SRC/06_error_handling.py" "error-handling" "Error Handling"
generate_md "$SRC/07_dependency_injection.py" "dependency-injection" "Dependency Injection"
generate_md "$SRC/08_database_crud_sqlite.py" "database-crud-sqlite" "Database CRUD with SQLite"
generate_md "$SRC/09_middleware_cors.py" "middleware-cors" "Middleware & CORS"
generate_md "$SRC/10_security_jwt.py" "security-jwt" "Security & JWT"
generate_md "$SRC/11_background_tasks_and_files.py" "background-tasks-and-files" "Background Tasks & File Uploads"

echo ""
echo "All FastAPI files created!"
