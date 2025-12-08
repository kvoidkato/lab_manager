import yaml
import platform
import subprocess
import sys
import time
import ctypes
import os

config_file = 'plem.yaml'

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def is_choco_available():
    print("\nChecking if Chocolatey was pre-installed...")
    time.sleep(1.5)
    try:
            result = subprocess.run(['choco', '-v'], capture_output=True,text=True,check=True)
            print('Chocolatey is Installed.')
    except FileNotFoundError:
        print("Chocolatey is not Installed.")
        install_choco = input('Proceed with Chocolatey installation? (y/n): ')
        powershell_command = (
            "Set-ExecutionPolicy Bypass -Scope Process -Force;"
            "iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))"
        )
        if install_choco == "y":
            try:
                command_to_run = ['powershell.exe', '-NoProfile', '-ExecutionPolicy', 'Bypass', '-Command', powershell_command]
                print("Executing Chocolatey installation command...")
                result = subprocess.run(command_to_run,capture_output=True,text=True,check=True)
                print("---Command Output---")
                print(result.stdout)
                print("\n  Re-run PLEM script as chocolatey was just installed.")
                print("---Execution Complete---")
                sys.exit(0)
            except subprocess.CalledProcessError as e:
                print(f"Error during command execution (Exit Code {e.returncode}):")
                print(f"STDOUT: {e.stdout}")
                print(f"STDERR: {e.stderr}")
            except FileNotFoundError:
                print("Error: powershell.exe not found.")
            except Exception as e:
                print(f"An unexpected error occurred: {e}")
        else: 
            print("Exiting PLEM script with exit code 2.")
            sys.exit(0)

def load_config(file_path):
    try:
        with open(file_path, 'r') as f:
            config = yaml.safe_load(f)
        return config
    except FileNotFoundError:
        print(f"Error: Configuration file '{file_path}' not found.")
        sys.exit(1)
    except yaml.YAMLError as e:
        print(f"Error parsing YAML file: {e}")
        sys.exit(1)

def execute_command(command, command_type="System"):
    print(f"\n--- Running {command_type} Command ---")
    
    is_list = isinstance(command, list)
    command_str = ' '.join(command) if is_list else command
    print(f"Executing: {command_str}")

    try:
        subprocess.run(command, shell=not is_list, check=True, text=True, capture_output=False)
        print(f"--- {command_type} Command Successful ---")
    except subprocess.CalledProcessError as e:
        print(f"\n!!! {command_type} Execution Failed for command: '{e.cmd}'")
        print(f"Return Code: {e.returncode}")
        sys.exit(e.returncode)
    except FileNotFoundError:
        print(f"!!! Error: Command/Tool not found. Make sure system tools are installed.")
        sys.exit(1)

def check_tool_availability(tool_name, command_to_check):
    print(f"\nChecking for required package manager: {tool_name}...")
    try:
        subprocess.run(command_to_check, shell=True, check=True, capture_output=True,text=True)
        print(f"Tool {tool_name} is installed and available.")
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        print(f"Tool {tool_name} is NOT found.")
        print(f"Please install {tool_name} or remove this dependency from the YAML file.")
        return False

def is_app_installed(app_name, check_command):
    print(f"Checking if {app_name} is already installed...")
    try:
        subprocess.run(check_command, shell=True, check=True,  capture_output=True,text=True)
        print(f"{app_name} is already installed. Skipping installation.")
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        print(f"{app_name} not found. Proceeding with installation.")
        return False

def is_module_installed(module_name):
    try:
        __import__(module_name)
        return True
    except ImportError:
        return False

def get_venv_python_path(venv_name):
    if platform.system() == "Windows":
        return os.path.join(venv_name, "scripts", "python.exe")
    else:
        print("Unsupported os.")
        return
    
def create_venv():
    if not os.path.exists(venv_dir_name):
        print("Creating virtual environment...")
        execute_command([sys.executable, "-m", "venv", venv_dir_name], "Virtual Environment Creation")
    else:
        print(f"Virtual environment {venv_dir_name} already exists.")
    return get_venv_python_path(venv_dir_name)

def setup_python_dependencies(config, venv_int):
    deps = config.get('python_dependencies', {})
    required_packages = deps.get('pip_install', [])
    if not required_packages:
        print("No Python packages found for 'pip_install'. Skipping.")
        return
    packages_to_install = []
    print(f"\n Checking Python Dependencies ")
    for package_spec in required_packages:
        package_name = package_spec.split('==')[0].split('>')[0].split('<')[0]
        if is_module_installed(package_name):
            print(f"Module {package_name} is already installed. Skipping.")
        else:
            packages_to_install.append(package_spec)
    if not packages_to_install:
        print("All required Python packages are already installed.")
        return
    print(f"\n  Installing {len(packages_to_install)} Python Dependencies via pip ")
    command = [venv_int, "-m", "pip", "install"] + packages_to_install
    execute_command(command, command_type="Pip Installation")


def setup_system_tools(config):
    tools = config.get('system_tools', {})
    current_os = platform.system().lower()
    system_commands = tools.get(current_os, [])
    if not system_commands:
        print(f"No system tools defined for OS: {current_os.capitalize()}. Skipping.")
        return
    manager_check = {
        'windows': ('choco', 'choco -v'),
        'darwin': ('brew', 'brew --version'),
        'linux': ('snap', 'snap version') 
    }
    if current_os in manager_check:
        tool_name, check_command = manager_check[current_os]
        if not check_tool_availability(tool_name, check_command):
            print("Skipping system tool setup due to missing package manager.")
            return
    print(f"\n Installing System Tools for {current_os.capitalize()} ")
    app_check_map = {
        'visualstudiocode': ('VS Code', 'code --version'),
        'node': ('Node.js', 'node -v'),
    }
    for command in system_commands:
        should_skip = False
        for keyword, (app_name, check_cmd) in app_check_map.items():
            if keyword in command.lower():
                if is_app_installed(app_name, check_cmd):
                    should_skip = True
                break
        if not should_skip:
            execute_command(command, command_type="System Tool Setup")



def main():
    print("="*40)
    print(f"    PLEM: Py-Lab Environment Manager    ")
    print("="*40)
    config = load_config(config_file)
    metadata = config["metadata"]
    print(f"\n- Lab Name: {metadata['lab_name']}")
    print(f"- Version: {metadata['version']}")
    print(f"- About: {metadata['description']}")
    print(f"\n {metadata['dev']}. All Rights Reserved.")
    time.sleep(2)
    print(" Checking for elevated permissions...")
    time.sleep(1)
    if is_admin():
        global venv_dir_name
        venv_dir_name = input("Enter virtual environment name: ")
        venv_python_interpreter = create_venv()
        setup_python_dependencies(config, venv_python_interpreter)
        is_choco_available()
        setup_system_tools(config)
        print("\n PLEM Setup Complete! ")
    else: 
        print("PLEM is not running as Administrator. Attempting to elevate permissions...")
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, __file__, None, 1)
        sys.exit(0)
if __name__ == "__main__":
    main()