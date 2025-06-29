import bpy
import os
import sys
import subprocess

# Name of the file where the global Python executable path will be stored
GLOBAL_PYTHON_PATH_FILENAME = "global_python_path.txt"

def find_global_python_executable():
    """
    Attempts to find the global Python executable (python or python3)
    using platform-specific commands and returns its absolute path.
    Returns None if not found.
    """
    python_exe_path = None
    cmd = []
    
    # Determine the command based on the operating system
    if sys.platform.startswith('win'):
        cmd_candidates = ["where", "python", "where", "python3"] # 'where' is Windows equivalent of 'which'
    elif sys.platform == 'darwin' or sys.platform.startswith('linux'):
        cmd_candidates = ["which", "python", "which", "python3"] # 'which' for Unix-like systems
    else:
        print(f"WARNING: Unsupported platform: {sys.platform}. Cannot reliably find Python executable.")
        return None

    # Iterate through command candidates (python then python3)
    for i in range(0, len(cmd_candidates), 2):
        tool = cmd_candidates[i]
        exe_name = cmd_candidates[i+1]
        try:
            # Use env=os.environ.copy() to ensure subprocess inherits current PATH
            # shell=False is safer as the command is controlled.
            result = subprocess.run([tool, exe_name], check=True, text=True, capture_output=True, env=os.environ.copy())
            python_exe_path = result.stdout.strip()
            print(f"DEBUG: Found '{exe_name}' at: {python_exe_path}")
            return python_exe_path # Return the first one found
        except (subprocess.CalledProcessError, FileNotFoundError):
            print(f"DEBUG: '{exe_name}' not found or command failed with '{tool}'.")
            continue # Try the next candidate

    return None # Neither python nor python3 found

def find_and_write_global_python_path(addon_dir):
    """
    Finds the global Python executable and writes its path to a file
    within the addon's directory.
    This also handles running the external .bat or .sh scripts for initial setup
    if the path file doesn't exist.
    """
    output_file_full_path = os.path.join(addon_dir, GLOBAL_PYTHON_PATH_FILENAME)

    if not os.path.exists(output_file_full_path):
        print(f"INFO: {GLOBAL_PYTHON_PATH_FILENAME} not found. Attempting to create it...")

        python_exe = find_global_python_executable()

        if python_exe:
            try:
                with open(output_file_full_path, "w") as f:
                    f.write(python_exe)
                print(f"INFO: Global Python executable path written to: {output_file_full_path}")
            except IOError as e:
                print(f"ERROR: Could not write to {output_file_full_path}: {e}")
        else:
            print("ERROR: Global Python executable could not be found. Automatic setup failed.")
            print("Please ensure Python is installed and accessible via your system's PATH.")
            print("You may need to manually create 'global_python_path.txt' with the full path to your python.exe/python3 executable.")
            # Fallback to run external scripts if python wasn't found by internal logic
            # This is less ideal but matches original logic; prefer internal Python finding.
            try:
                if sys.platform.startswith("win"):
                    script_path = os.path.join(addon_dir, "win_global_python_path.bat")
                    if os.path.exists(script_path):
                        subprocess.run([script_path], check=True, cwd=addon_dir)
                        print(f"INFO: Executed '{os.path.basename(script_path)}' to attempt path finding.")
                elif sys.platform == "darwin" or sys.platform.startswith("linux"):
                    script_path = os.path.join(addon_dir, "lin_mac_global_python_path.sh")
                    if os.path.exists(script_path):
                        # Ensure the script is executable
                        if not os.access(script_path, os.X_OK):
                            os.chmod(script_path, 0o755)
                        subprocess.run([script_path], check=True, cwd=addon_dir)
                        print(f"INFO: Executed '{os.path.basename(script_path)}' to attempt path finding.")
                else:
                    print("WARNING: No external script to run for this platform.")
            except subprocess.CalledProcessError as e:
                print(f"ERROR: External path finding script failed: {e}")
                print(f"STDOUT: {e.stdout}")
                print(f"STDERR: {e.stderr}")
            except FileNotFoundError:
                print("ERROR: External path finding script not found.")
    else:
        print(f"INFO: {GLOBAL_PYTHON_PATH_FILENAME} already exists. Skipping path finding.")
