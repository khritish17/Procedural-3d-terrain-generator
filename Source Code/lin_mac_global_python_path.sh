#!/bin/bash

# This script finds the global Python executable path on Linux/macOS.
# It then writes the found path to a text file named 'global_python_path.txt'
# in the same directory as this script.

PYTHON_EXE_PATH=""
OUTPUT_FILE_NAME="global_python_path.txt"

# Get the directory of the current script
# $0 is the path to the script itself
# dirname "$0" extracts the directory part
SCRIPT_DIR="$(dirname "$0")"

# Construct the full path for the output file
OUTPUT_FILE_FULL_PATH="${SCRIPT_DIR}/${OUTPUT_FILE_NAME}"

# --- Try to find 'python' first ---
# 'command -v' is preferred over 'which' as it's a shell built-in
# and generally more reliable across different shells.
# It prints the path if found and sets exit status to 0.
if command -v python &> /dev/null; then
    PYTHON_EXE_PATH="$(command -v python)"
elif command -v python3 &> /dev/null; then # --- If 'python' not found, try 'python3' ---
    PYTHON_EXE_PATH="$(command -v python3)"
fi

# Check if a Python executable was found
if [ -n "$PYTHON_EXE_PATH" ]; then
    # Write the path to the file
    echo "$PYTHON_EXE_PATH" > "${OUTPUT_FILE_FULL_PATH}"
    echo "Global Python executable path found and written to: ${OUTPUT_FILE_FULL_PATH}"
    echo "Path: ${PYTHON_EXE_PATH}"
    exit 0 # Success
else
    # Output error message to standard error (>&2)
    echo "Error: Global Python executable (python or python3) not found in your system's PATH." >&2
    echo "Please ensure Python is installed and its directory is added to your PATH." >&2
    echo "No output file was created." >&2
    exit 1 # Failure
fi