#!/bin/bash

SRC="E:/Python-Learning"
DST="src/content/learning/python-learning"

mkdir -p "$DST"

# Day 1 - First Program
cat > "$DST/day-1-first-program.md" << 'EOF'
# Day 1 - First Program

## Hello World

Python's simplest program:

```python
print("Hello World")
```

This is the starting point for any Python journey. The `print()` function outputs text to the console.
EOF
echo "Created day-1-first-program.md"

# Function to convert a Python file to markdown
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

# Python Fundamentals
generate_md "$SRC/01-python-fundamentals/01_strings_and_methods.py" "strings-and-methods" "Strings & Methods"
generate_md "$SRC/01-python-fundamentals/02_multiline_strings.py" "multiline-strings" "Multiline Strings"
generate_md "$SRC/01-python-fundamentals/03_lists_and_methods.py" "lists-and-list-methods" "Lists & List Methods"
generate_md "$SRC/01-python-fundamentals/04_tuples_and_methods.py" "tuples" "Tuples"
generate_md "$SRC/01-python-fundamentals/05_sets_and_methods.py" "sets" "Sets"
generate_md "$SRC/01-python-fundamentals/06_dictionaries_and_methods.py" "dictionaries" "Dictionaries"
generate_md "$SRC/01-python-fundamentals/07_user_input.py" "user-input" "User Input"
generate_md "$SRC/01-python-fundamentals/08_if_else.py" "if-else-conditions" "If-Else Conditions"
generate_md "$SRC/01-python-fundamentals/08b_match_case.py" "match-case" "Match Case"
generate_md "$SRC/01-python-fundamentals/09_loops.py" "loops" "Loops"
generate_md "$SRC/01-python-fundamentals/10_functions.py" "functions-and-arguments" "Functions & Arguments"
generate_md "$SRC/01-python-fundamentals/11_type_hints.py" "type-hints" "Type Hints & Type Checking"
generate_md "$SRC/01-python-fundamentals/12_classes_and_oop.py" "oop-classes-and-objects" "OOP - Classes & Objects"
generate_md "$SRC/01-python-fundamentals/13_decorators.py" "decorators" "Decorators"
generate_md "$SRC/01-python-fundamentals/14_async_await.py" "async-await" "Async/Await"
generate_md "$SRC/01-python-fundamentals/15_exception_handling.py" "exception-handling" "Exception Handling"
generate_md "$SRC/01-python-fundamentals/16_modules_and_imports.py" "modules-and-imports" "Modules & Imports"
generate_md "$SRC/01-python-fundamentals/17_json_handling.py" "json-handling" "JSON Handling"
generate_md "$SRC/01-python-fundamentals/18_list_comprehensions.py" "list-comprehensions" "List Comprehensions"
generate_md "$SRC/01-python-fundamentals/19_lambda_map_filter.py" "lambda-map-filter" "Lambda, Map & Filter"
generate_md "$SRC/01-python-fundamentals/20_generators_and_iterators.py" "generators-and-iterators" "Generators & Iterators"
generate_md "$SRC/01-python-fundamentals/21_typeddict_and_dataclasses.py" "typeddict-and-dataclasses" "TypedDict & Dataclasses"
generate_md "$SRC/01-python-fundamentals/22_environment_variables.py" "environment-variables" "Environment Variables"
generate_md "$SRC/01-python-fundamentals/23_file_io.py" "file-io" "File I/O"

# Deep Python
generate_md "$SRC/02-deep-python/01_dunder_methods.py" "dunder-methods" "Dunder Methods"
generate_md "$SRC/02-deep-python/02_context_managers.py" "context-managers" "Context Managers"
generate_md "$SRC/02-deep-python/03_decorators_deep_dive.py" "decorators-deep-dive" "Decorators Deep Dive"

echo ""
echo "All files created successfully!"
