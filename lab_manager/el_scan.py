import subprocess
import os
import sys

folder_path = os.path.dirname(os.path.abspath(sys.argv[0]))
os.system("title System Scan Script: UNIOSUN Software Engineering")

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
        return
    except FileNotFoundError:
        print(f"!!! Error: Command/Tool not found. Make sure system tools are installed.")
        return
    
def execute_check_command(command, command_type="System"):
    print(f"\n--- Running {command_type} Command ---")
    
    is_list = isinstance(command, list)
    command_str = ' '.join(command) if is_list else command
    print(f"Executing: {command_str}")

    try:
        result = subprocess.run(command, shell=not is_list, check=True, text=True, capture_output=True)
        print("--- Scan Output ---")
        print(result.stdout)
        print(f"ErrorLog: {result.stderr}")
        print(f"--- {command_type} Command Successful ---")
    except subprocess.CalledProcessError as e:
        print(f"\n!!! {command_type} Execution Failed for command: '{e.cmd}'")
        print(e.stdout)
        print(f"[ERROR]: {e.stderr.strip()}")
        print(f"Return Code: {e.returncode}")
        return
    except FileNotFoundError:
        print(f"!!! Error: Command/Tool not found. Make sure system tools are installed.")
        return

def show_env_status():
    print("\n--- Running system checks ---\n")
    print("\n")
    print("This might take a while. You may run other tasks.\n\n")
    python_version_check_cmd = ["python", "--version"]
    execute_command(python_version_check_cmd, "Python Check")
    git_version_check_cmd = ["git", "--version"]
    execute_command(git_version_check_cmd)
    print("\n   Checking Virtual Environments...\n")
    venvs = []
    elements = [item for item in os.listdir(folder_path) if os.path.isdir(os.path.join(folder_path, item))]
    for folder in elements:
        if os.path.exists(f"{folder}/scripts/python.exe"):
            print(f"Folder {folder} is a venv. Appending to venv list...") 
            venvs.append(folder)
    if not venvs:
        print("No venv is present inside the root folder. Skipping...")
        input("\nPress ENTER key to continue...")
        return
    for venv in venvs:
        venv_path_s = os.path.join(venv, 'scripts', 'python.exe')
        freeze_command = [venv_path_s, '-m', 'pip', 'freeze']
        print(f"Listing installed packages for '{venv}'...\n")
        pip_result = subprocess.run([venv_path_s, '-m', 'pip', '--version'], capture_output=True,text=True,check=True)
        print(f"Pip version: {pip_result.stdout}")
        try:
            freeze_result = subprocess.run(freeze_command,capture_output=True,text=True,check=True)
            packages_to_upgrade = freeze_result.stdout.strip().splitlines()
            if not packages_to_upgrade:
                print("No packages found in the virtual environment to upgrade.")
                return
            print(f"Found {len(packages_to_upgrade)} packages in {venv}")
            for line in packages_to_upgrade:
                package_name = line.split('==')[0].strip()
                print("*"*15)
                print(f"-- Package Name: {package_name}")
                print(f"-- Package Version: {line.split('==')[1].strip()}")
                print("*"*15)
        except subprocess.CalledProcessError as e:
            print(f"\nFreeze command failed.")
            print(f"Error log: {e}")            
        except Exception as e:
            print(f"\nAn unexpected error occurred: {e}")
    sys_scan = input("\033[92mRun system scans (y/n): \033[0m")
    if sys_scan == "y":
        run_system_check_cmd = ["sfc", "/scannow"]
        execute_check_command(run_system_check_cmd, "System Scan")
        run_system_health_check_cmd = ["DISM", "/Online", "/Cleanup-Image", "/CheckHealth"]
        execute_check_command(run_system_health_check_cmd, "System Health Check")
        system_health_restore_health_cmd = ["DISM", "/Online", "/Cleanup-Image", "/RestoreHealth"]
        fix = input("\nRun '/RestoreHealth' to fix system image (y/n): ")
    else:
        input("\nPress ENTER key to continue...")
        return
    if fix == "y":
        execute_check_command(system_health_restore_health_cmd, "System Restore Health")
    else:
        pass
    input("\nPress ENTER key to continue...")

if __name__ == "__main__":
    show_env_status()