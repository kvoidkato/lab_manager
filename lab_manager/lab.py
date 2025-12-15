import subprocess
import sys
import time
import os
import shutil
import ctypes

os.system("title Lab Setup Manager - UNIOSUN Software Engineering")
folder_path = os.path.dirname(os.path.abspath(sys.argv[0]))

def is_choco_package_installed(package_name):
    print(f"Checking Chocolatey for package: {package_name}...")
    try:
        result = subprocess.run(
            ['choco', 'list', package_name],
            capture_output=True,
            text=True,
            check=False 
        )
        if result.returncode != 0:
            print(f"Error running 'choco list': {result.stderr.strip()}")
            return False
        target_entry = f"{package_name}"
        for line in result.stdout.splitlines():
            if line.strip().lower().startswith(target_entry.lower()):
                print(f"Package '{package_name}' found in Chocolatey local list.")
                return True
        print(f"Package '{package_name}' not found in Chocolatey local list.")
        return False
    except FileNotFoundError:
        print("Error: 'choco' command not found. Cannot check package status.")
        return False
    except Exception as e:
        print(f"An unexpected error occurred while checking Chocolatey: {e}")
        return False

def find_system_python():
    system_python_path = shutil.which("python")
    if system_python_path:
        if sys.executable.lower() not in system_python_path.lower():
            return system_python_path
    system_python_path = shutil.which("python3")
    if system_python_path:
        return system_python_path
    return None

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
        print(f"[ERROR]: {e.stderr.strip()}")
        print(f"Return Code: {e.returncode}")
        return
    except FileNotFoundError:
        print(f"!!! Error: Command/Tool not found. Make sure system tools are installed.")
        return

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def run_script(script):
    print(f"\n--- Running {script} ---\n")
    try:
        if script.endswith(".py"):
            cmd = [sys.executable, script]
            shell = True
        else: 
            cmd = script
            shell = False
        subprocess.run(cmd, shell=shell, check=True, text=True, capture_output=False)
    except subprocess.CalledProcessError as e:
        print(f"\n!!! Error: {script} failed with exit code {e.returncode}.\n", file=sys.stderr)
    except FileNotFoundError:
        print(f"!!! Error: Script or file not found: {script}", file=sys.stderr)
    input("\nPress ENTER key to continue...")

def git_clone():
    repo_url = input("\033[92mInput repository URL (separate with | for multiple): \033[0m").strip()
    if not repo_url:
        print("\nError: Repository URL is required. Exiting...")
        return
    repo_urls = repo_url.split("|")
    repo_urls = [url.strip() for url in repo_urls if url.strip()]
    base_dir = "git_repos"
    
    try:
        if not os.path.exists(base_dir):
            os.mkdir(base_dir)
            print(f"'{base_dir}' folder created.")
        else:
            print(f"'{base_dir}' folder already exists.")
        print(f'\n   Cloning into "{base_dir}" subdirectories...')
        
        for each_repo_url in repo_urls:
            repo_name = each_repo_url.rstrip('/').split('/')[-1].replace('.git', '')
            destination_path = os.path.join(base_dir, repo_name)
            print(f"--- Cloning {each_repo_url} into {destination_path} ---")
            subprocess.run(["git", "clone", each_repo_url, destination_path],check=True,capture_output=True,text=True)
            print(f"--- Cloned successfully ---")
        print("\n   Git Cloning Complete.\n")
        
    except FileNotFoundError:
        print("Error: Git command not found. Make sure Git is installed and in your PATH.\n")
    except subprocess.CalledProcessError as e:
        print("Error cloning git repository. Check URL or path permissions. \n")
        print(f"Command: {e.cmd}")
        print(f"Return Code: {e.returncode}")
        print(f"Stderr (Git output): {e.stderr.strip()}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        
    input("\nPress ENTER key to continue...")
    subprocess.run(["cls"], shell=True)

def create_venv ():
    venv_name = input("\033[92mInput virtual environment name: \033[0m")
    venv_path = os.path.join(os.getcwd(), venv_name)
    global_py = find_system_python()

    if os.path.exists(venv_path):
        print(f"\nVirtual environment '{venv_name}' already exists.\n")
        return
    print(f"\nCreating virtual environment '{venv_name}' via {global_py}...\n")
    try:
        cmd_string = f'"{global_py}" -m venv "{venv_name}"'
        subprocess.run(cmd_string, check=True, shell=True, capture_output=False)
        print("  Venv created successfully!\n")
    except subprocess.CalledProcessError as e:
        print("Error: Failed to create Venv.\n")
        print(f"Command executed: {e.cmd}")
        print(f"Stdout: {e.stdout.strip()}")
        print(f"Stderr: {e.stderr.strip()}")
    input("\nPress ENTER key to continue...")
    
def sort():
    target_dir = input("\033[92mEnter the directory path to sort (e.g., ./downloads): \033[0m").strip()

    if not os.path.isdir(target_dir):
        print(f"\nError: Directory '{target_dir}' not found.\n")
        return
    print(f"\nSorting files in: {target_dir}\n")
    extensions = {
        '.txt': 'Documents', '.pdf': 'Documents', '.doc': 'Documents',
        '.docx': 'Documents', '.pptx': "Documents",
        '.jpg': 'Images', '.png': 'Images', '.gif': 'Images',
        '.zip': 'Archives', '.rar': 'Archives',
        '.py': 'Scripts', '.sh': 'Scripts',
        '.mkv': 'Videos', '.mp4': "Videos",
        '.exe': 'Applications', '.msi': 'Applications', '.apk': 'Applications'
    }
    for filename in os.listdir(target_dir):
        source_path = os.path.join(target_dir, filename)
        if os.path.isdir(source_path) or filename == 'sort.py':
            continue
        _, file_extension = os.path.splitext(filename)
        file_extension = file_extension.lower()
        if file_extension in extensions:
            dest_folder = os.path.join(target_dir, extensions[file_extension])
            os.makedirs(dest_folder, exist_ok=True)
            shutil.move(source_path, os.path.join(dest_folder, filename))
            print(f"Moved {filename} to {extensions[file_extension]}\n")
    print("   Directory sorting complete.")
    input("\nPress ENTER key to continue...")

def update_venv_deps():
    venv_to_update = input("\033[92mEnter venv name ('all' to update all venvs): \033[0m")
    venvs = []
    if venv_to_update == "all":
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
            pip_cmd = [venv_path_s, '-m', 'pip', 'install', '--upgrade', 'pip']
            execute_command(pip_cmd, "Upgrading PIP")
            freeze_command = [venv_path_s, '-m', 'pip', 'freeze']
            print("Listing installed packages for upgrade...")
            try:
                freeze_result = subprocess.run(freeze_command,capture_output=True,text=True,check=True)
                packages_to_upgrade = freeze_result.stdout.strip().splitlines()
                if not packages_to_upgrade:
                    print("No packages found in the virtual environment to upgrade.")
                    return
                print(f"Found {len(packages_to_upgrade)} packages. Starting individual upgrades...")
                for line in packages_to_upgrade:
                    package_name = line.split('==')[0].strip()
                    upgrade_command = [venv_path_s, '-m', 'pip', 'install', '-U', package_name]
                    print(f"-> Upgrading {package_name}...")
                    subprocess.run(upgrade_command,capture_output=False,check=True)
                print("\n--- All packages in the virtual environment have been upgraded. ---")
            except subprocess.CalledProcessError as e:
                print(f"\nUpgrade failed for a package. Check the logs.")
                print(f"Error log: {e}")            
            except Exception as e:
                print(f"\nAn unexpected error occurred: {e}")
            print("All PIP packages updated.")
            print(f"Finished updating packages for {venv}")
        input("\nPress ENTER key to continue...")
    elif venv_to_update in os.listdir(os.path.dirname(__file__)):
        print("\nUpdating pip...")
        venv_path = os.path.join(venv_to_update, 'scripts', 'python.exe')
        pip_cmd = [venv_path, '-m', 'pip', 'install', '--upgrade', 'pip']
        execute_command(pip_cmd, "Upgrading PIP")
        freeze_command = [venv_path, '-m', 'pip', 'freeze']
        print("Listing installed packages for upgrade...")
        try:
            freeze_result = subprocess.run(freeze_command,capture_output=True,text=True,check=True)
            packages_to_upgrade = freeze_result.stdout.strip().splitlines()
            if not packages_to_upgrade:
                print("No packages found in the virtual environment to upgrade.")
                input("\nPress ENTER key to continue...")
                return
            print(f"Found {len(packages_to_upgrade)} packages. Starting individual upgrades...")
            for line in packages_to_upgrade:
                package_name = line.split('==')[0].strip()
                upgrade_command = [venv_path, '-m', 'pip', 'install', '-U', package_name]
                print(f"-> Upgrading {package_name}...")
                subprocess.run(upgrade_command,capture_output=False,check=True)
            print("\n--- All packages in the virtual environment have been upgraded. ---")
        except subprocess.CalledProcessError as e:
            print(f"\nUpgrade failed for a package. Check the logs.")
            print(f"Error log: {e}")            
        except Exception as e:
            print(f"\nAn unexpected error occurred: {e}")
    else:
        print("ERROR: Venv not found.")
    input("\nPress ENTER key to continue...")

def show_env_status():
    print("\033[92m>>>   Checking for elevated permissions...\033[0m")
    time.sleep(2)
    if is_admin():
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
        for venv in venvs:
            venv_path_s = os.path.join(venv, 'scripts', 'python.exe')
            freeze_command = [venv_path_s, '-m', 'pip', 'freeze']
            print(f"Listing installed packages for '{venv}'...\n")
            pip_result = subprocess.run([venv_path_s, '-m', 'pip', '--version'], capture_output=True,text=True,check=True)
            print(f"Pip version for {venv}: {pip_result.stdout}")
            try:
                freeze_result = subprocess.run(freeze_command,capture_output=True,text=True,check=True)
                packages_to_upgrade = freeze_result.stdout.strip().splitlines()
                if not packages_to_upgrade:
                    print("No packages found in the virtual environment.")
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
    else:
        print("Relaunching as administrator to perform system scan...")
        script_path = os.path.abspath(sys.argv[0])
        admin_args = "--scan"
        ctypes.windll.shell32.ShellExecuteW(None, "runas", script_path, admin_args, None, 1)
        input("\nPress ENTER key to continue...")

def install_packages():
    venv_to_install_to = input("\033[92mEnter venv name: \033[0m")
    package_to_install = input("\n\033[92mEnter package name: \033[0m")
    packages_to_install = package_to_install.split(" ")
    if venv_to_install_to in os.listdir(folder_path):
        venv_to_install_to_py_path = os.path.join(venv_to_install_to, 'scripts', 'python.exe')
        install_cmd = [venv_to_install_to_py_path, "-m", "pip", "install"] + packages_to_install
        print(f"Installing {len(packages_to_install)} packages via pip...")
        execute_command(install_cmd, "Package Installation")
    else:
        print("ERROR: Venv not found")
        print(f"{venv_to_install_to} not found in {os.path.dirname(__file__)}")
    input("\nPress ENTER key to continue...")

def install_apps():
    app_to_install = input("\033[92mEnter app name: \033[0m")
    apps_to_install = app_to_install.split(" ")
    print(f"Installing {len(apps_to_install)} apps via choco...")
    for app in apps_to_install:
        if is_choco_package_installed(app):
            print(f'Package {app} is installed. Skipping...')
            continue
        install_cmd = ['choco', 'install', app]
        execute_command(install_cmd, 'App/Tool Installation')
        print("\n")

def help():
    green = '\033[92m'  
    reset = '\033[0m'
    readme_path = os.path.join(folder_path, 'readme.txt')
    try:
        with open(readme_path, 'r', encoding='utf-8') as readme:
            readme_content = readme.read()
    except FileNotFoundError:
        print(f"Error: readme.txt not found in the script directory {readme_path}.")
        return
    for line in readme_content.splitlines():
        is_green = line.strip().startswith('>>')
        output_line = green + line + reset if is_green else line
        for char in output_line:
            sys.stdout.write(char)
            sys.stdout.flush()
            time.sleep(0.001)
        sys.stdout.write('\n')
    input("\nPress ENTER key to continue...")

def menu():
    while True:
        time.sleep(1)
        subprocess.run(["cls"], shell=True)
        print("\n")
        print("                  _______________________________________________________________________")
        print("                 |                                                                       |")
        print("                 |    ===============================================================    |")
        print("                 |                      Lab Manager - Main Menu                          |")
        print("                 |    ===============================================================    |")
        print("                 |                                                                       |")
        print("                 |   [1] Run PLEM Setup (Installs Python/Apps/Packages)                  |")
        print("                 |                                                                       |")
        print("                 |   [2] Clone Git Repository                                            |")
        print("                 |                                                                       |")
        print("                 |   [3] Create Virtual Environment (Venv)                               |")
        print("                 |                                                                       |")
        print("                 |   [4] Sort Directories/Files                                          |")
        print("                 |                                                                       |")
        print("                 |   [5] Update Venv Dependencies                                        |")
        print("                 |                                                                       |")
        print("                 |   [6] Show Environment Status / System Scans                          |")
        print("                 |                                                                       |")
        print("                 |   [7] Install Packages                                                |")
        print("                 |                                                                       |")
        print("                 |   [8] Install Applications/Tools                                      |")
        print("                 |                                                                       |")
        print("                 |   [H] Help                                                            |")
        print("                 |                                                                       |")
        print("                 |   [0] Exit Manager                                                    |")
        print("                 |                                                                       |")
        print("                 |_______________________________________________________________________|")

        choice = input("\033[92m\n\n                 Enter task number (0, 1, 2, 3, 4, 5, 6, 7, 8, H): \033[0m").lower().strip()

        if choice == "1":
            subprocess.run(["cls"], shell=True)
            time.sleep(1)
            setup_path = os.path.join(folder_path, "setup.bat")
            execute_command(setup_path, "PLEM Setup (setup.bat)")
            if not os.path.exists(setup_path):
                print("\nERROR: 'setup.bat' not found in expected location.")
                print(f"Expected path: {setup_path}")
                print("Make sure menu.exe and setup.bat are both in the same directory.")
        elif choice == "2":
            subprocess.run(["cls"], shell=True)
            time.sleep(1)
            git_clone()
        elif choice == "3":
            subprocess.run(["cls"], shell=True)
            time.sleep(1)
            create_venv()
        elif choice == "4":
            subprocess.run(["cls"], shell=True)
            time.sleep(1)
            sort()
        elif choice == "5":
            subprocess.run(["cls"], shell=True)
            time.sleep(1)
            update_venv_deps()
            input("\nPress ENTER key to continue...")
        elif choice == "6":
            subprocess.run(["cls"], shell=True)
            time.sleep(1)
            show_env_status()
        elif choice == "7":
            subprocess.run(["cls"], shell=True)
            time.sleep(1)
            install_packages()
        elif choice == "8":
            subprocess.run(["cls"], shell=True)
            time.sleep(1)
            install_apps()
            input("\nPress ENTER to continue...")
        elif choice == "h":
            subprocess.run(["cls"], shell=True)
            time.sleep(1)
            help()
        elif choice == "0":
            print("\n    Exiting Lab Manager...")
            time.sleep(1)
            exit(0)
        else:
            print("Invalid choice! Try again.")
            time.sleep(1)
            subprocess.run(["cls"], shell=True)

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1].lower() == '--scan':
        show_env_status()
        sys.exit(0)
    menu()