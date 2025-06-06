import subprocess
import os 
import sys

def setup_virtual_env(env_name = ".venv", requirements_file = "requirements.txt"):
    """
    Creates our virtual environment and installs libraries into it.
    """
    # absolute path for current directory
    curr_dir = os.path.dirname(os.path.abspath(__file__))

    # full path for virtual environment directory
    full_env_path = os.path.join(curr_dir, env_name)

    # full path of the requirements file
    full_requirements_path = os.path.join(curr_dir, requirements_file)

    # requirements file path valididty check
    if not os.path.exists(full_requirements_path):
        print(f"Error: '{requirements_file}' file not found at '{full_requirements_path}'")
        sys.exit(1)
    
    # checking whether the given env_name is new or already exists
    if not os.path.exists(full_env_path):
        print(f"Creating virtual environment:'{env_name}'")
        # 
        try:
            subprocess.run([sys.executable, "-m", "venv", full_env_path], check=True)
            env_list = open("env_list.txt", "a")
            env_list.write(f"{env_name}\n")
            env_list.close()
            print(f"Virtual environment '{env_name}' created successfully")
        except subprocess.CalledProcessError as e:
            print(f"Error creating virtual environment '{env_name}'")
            sys.exit(1)
    else:
        print(f"Virtual environment '{env_name}' already exist")
    install_requirements(env_name=env_name, requirements_file="requirements.txt")

def install_requirements(env_name = ".venv", requirements_file = "requirements.txt"):
    # once the environment is created, install the requirements
    # absolute path for current directory
    curr_dir = os.path.dirname(os.path.abspath(__file__))

    # full path of the requirements file
    full_requirements_path = os.path.join(curr_dir, requirements_file)

    # full path for virtual environment directory
    full_env_path = os.path.join(curr_dir, env_name)
    print("Installing the required dependencies")
    try:
        # determine the pip executable
        # pip_executable = None
        if sys.platform == "win32":
            pip_executable = os.path.join(full_env_path, "Scripts", "pip.exe")
        else:
            pip_executable = os.path.join(full_env_path, "bin", "pip")
        if not os.path.exists(pip_executable):
            print(f"Error: pip executable not found in virtual environment at '{pip_executable}'")
            sys.exit(1)
        
        # install the requirements using the virtual environment's pip
        commands = [pip_executable, 
                    "install", 
                    "-r", full_requirements_path, 
                    "--upgrade",
                    "--disable-pip-version-check"]
        result = subprocess.run(commands, capture_output=True, text=True, check=True)
        if result.stdout:
            print("STDOUT during installation:")
            print(result.stdout)
        if result.stderr:
            print("Warning/Errors during installation:")
            print(result.stderr)
    except subprocess.CalledProcessError as e:
        print(f"Error during library installation:")
        print(f"Command: {' '.join(e.cmd)}")
        print(f"Return Code: {e.returncode}")
        print(f"STDOUT:\n{e.stdout}")
        print(f"STDERR:\n{e.stderr}")
        sys.exit(1)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        sys.exit(1)

def activate_helper(env_name):
    if sys.platform == "win32":
        print(f".\\{env_name}\\Scripts\\activate")
    else:
        print(f"source ./{env_name}/bin/activate")

def menu():
    print(f"MENU")
    print(f"1. SETUP NEW VIRTUAL ENVIRONMENT")
    print(f"2. ACTIVATE HELPER CODE")
    opt = input()
    try:
        env_list = open("env_list.txt", "r") 
        all_env = env_list.readlines()
        all_env = [ele.strip("\n") for ele in all_env]
        env_list.close()
    except:
        all_env = []
    if opt == "1":
        print(f"Choose a virtual environment name other than the following:")
        print(f"{all_env}")
        env_name = input()
        if env_name not in all_env:
            setup_virtual_env(env_name=env_name)
        else:
            print(f"Try some name other than this {all_env}")
    elif opt == "2":
        print(f"Choose the virtual environment name")
        print(f"{all_env}")
        env_name = input()
        if env_name in all_env:
            activate_helper(env_name=env_name)
        else:
            print("Choose a the required environment name from this:")
            print(f"{all_env}")
    else:
        print("Error: No such options!!")

if __name__ == "__main__":
    menu()
