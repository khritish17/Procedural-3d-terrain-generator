@echo off
REM This batch file finds the global Python executable path on Windows.
REM It then writes the found path to a text file named 'python_path.txt'
REM in the same directory as this batch file.

set "PYTHON_EXE_PATH="
set "OUTPUT_FILE_NAME=global_python_path.txt"

REM Get the directory of the current batch file
set "SCRIPT_DIR=%~dp0"

REM Construct the full path for the output file
set "OUTPUT_FILE_FULL_PATH=%SCRIPT_DIR%%OUTPUT_FILE_NAME%"

REM --- Try to find 'python.exe' first ---
where /q python.exe 2>nul
if %errorlevel% equ 0 (
    for %%i in (python.exe) do (
        set "PYTHON_EXE_PATH=%%~$PATH:i"
        goto :found_python
    )
)

REM --- If 'python.exe' is not found, try 'python3.exe' ---
where /q python3.exe 2>nul
if %errorlevel% equ 0 (
    for %%i in (python3.exe) do (
        set "PYTHON_EXE_PATH=%%~$PATH:i"
        goto :found_python
    )
)

:found_python
if defined PYTHON_EXE_PATH (
    REM Write the path to the file
    echo %PYTHON_EXE_PATH%> "%OUTPUT_FILE_FULL_PATH%"
    
    exit /b 0
) else (
    echo Error: Global Python executable not found in your system's PATH.
    echo Please ensure Python is installed and its directory is added to your PATH.
    echo.
    echo No output file was created.
    echo.
    exit /b 1
)