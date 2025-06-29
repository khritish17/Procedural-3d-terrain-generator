import os 
import sys
import subprocess

def check_and_configure(addon_dir):
    # checks for the global python exe path file
    # if it does not exist: generates the file

    # the file name: 'python_exe_path.txt'
    python_exe_file = os.path.join(addon_dir, "python_exe_path.txt")
    print("-> PTG log: checking the existance of python_exe_path.txt")
    if not os.path.exists(python_exe_file):
        print("-> PTG log: global python executable path file not found !!!")
        # configure the python exe file
        print("-> PTG log: configuring the global python executable path file")
        python_paths = get_python_exe()
        if python_paths == None:
            print("-> PTG log: [Error] Python executable not found!!!")
        else:
            with open(python_exe_file, "w") as f:
                f.write(python_paths)
                print("-> PTG log: python_exe_path.txt configured")
    else:
        print("-> PTG log: python_exe_path.txt found !!!")



def get_python_exe():
    """
        rtype: returns the python exe path in string format
        if no executable found returns None
    """
    python_exe_paths = None
    cmd = []
    # commands based on system
    platform = sys.platform
    if platform.startswith('win'):
        cmd = ["where", "python", "where", "python3"]
    elif platform == 'darwin' or platform.startswith('linux'):
        cmd = ["which", "python", "which", "python3"]
    else:
        print(f"-> PTG log: [Warning] Unsupported platform: {platform}")
        return None
    
    for i in range(0, len(cmd), 2):
        tool = cmd[i]
        exe_name = cmd[i + 1]
        try:
            result = subprocess.run([tool, exe_name], check = True, text = True, capture_output=True, env = os.environ.copy())
            python_exe_paths = result.stdout.strip()
            print(f"-> PTG log: [Success] Python execuatable found successfully at: {python_exe_paths}")
            return python_exe_paths
        except Exception as e:
            print(f"-> PTG log:[Error] {e}")
            continue
    return None