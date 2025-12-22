import subprocess
import sys
import time
import os
import shutil
import ctypes
from pathlib import Path
import logging
import stat
import zipfile
import json

os.system("title Lab Setup Manager - UNIOSUN Software Engineering")
CYAN = "\033[96m"    # Headers
GREEN = "\033[92m"   # Numbers
YELLOW = "\033[93m"  # Highlights
GRAY = "\033[90m"    # Dividers/Metadata
BOLD = "\033[1m"     # Emphasis
RED = "\033[91m"     # Exit/Warnings
RESET = "\033[0m"
if getattr(sys, 'frozen', False):
    base_dir = Path(sys.executable).resolve().parent
else:
    base_dir = Path(__file__).resolve().parent
log_file = base_dir / "lab_manager_logs.log"
backup_dir = base_dir / "lab_manager_backups"
projects_dir = base_dir / "projects.txt"

logging.basicConfig(filename=log_file, filemode="a", format="%(asctime)s - %(levelname)s - [%(funcName)s] - %(message)s", level=logging.INFO)
logging.info("--- Lab Manager V2.0 Session Started ---")

def is_choco_available():
    try:
        subprocess.run(['choco', '-v'], check=True, text=True, capture_output=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False

def is_choco_package_installed(package_name):
    print(f"Checking Chocolatey for package: {package_name}...")
    try:
        result = subprocess.run(['choco', 'list', package_name],capture_output=True,text=True,check=False )
        if result.returncode != 0:
            print(f"Error running 'choco list'")
            logging.error(f"Error running 'choco list': {result.stderr.strip()}")
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
        print(f"\033[91mAn unexpected error occurred while checking Chocolatey. Check log for details.\033[0m")
        logging.error(f"An unexpected error occurred while checking Chocolatey: {e}")
        logging.exception("Traceback, is_choco_package_installed: ")
        return False

def remove_readonly(func, path, excinfo):
    os.chmod(path, stat.S_IWRITE)
    func(path)

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
        logging.error(f"System Check command failed. Error details: {e}")
        return
    except FileNotFoundError as e:
        print(f"!!! Error: Command/Tool not found. Make sure system tools are installed.")
        logging.exception(f"System Tool not available. Error details: {e}")
        return

def execute_task(command, task_name):
    print(f"\n>>> Starting Task: {task_name}")
    logging.info(f"Executing: {' '.join(command)}")
    try:
        process = subprocess.Popen( command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, shell=True )
        for line in process.stdout:
            print(f"  [STDOUT]: {line.strip()}")
        process.wait()
        if process.returncode == 0:
            logging.info(f"Task '{task_name}' completed successfully.")
            return True
        else:
            error_output = process.stderr.read()
            logging.error(f"Task '{task_name}' failed with code {process.returncode}")
            logging.error(f"Error Message: {error_output}")
            print(f"\033[91mError in {task_name}! Check the log for details.\033[0m")
            return False
    except Exception as e:
        logging.exception(f"Unexpected crash during task: {task_name}. Error details: {e}")
        return False
    
"""def execute_check_command(command, command_type="System"):
    print(f"\n--- Running {command_type} Command ---")
    
    is_list = isinstance(command, list)
    command_str = ' '.join(command) if is_list else command
    print(f"Executing: {command_str}")

    try:
        result = subprocess.run(command, shell=not is_list, check=True, text=True, capture_output=True)
        print("--- Scan Output ---")
        print(result.stdout)
        print(f"--- {command_type} Command Successful ---")
        logging.info("System Scan COMPLETE.")
    except subprocess.CalledProcessError as e:
        print(f"\n!!! {command_type} Execution Failed for command: '{e.cmd}'")
        print(f"[ERROR]: {e.stderr.strip()}")
        print(f"Return Code: {e.returncode}")
        logging.error(f"Failed to run system check command. {e}")
        logging.exception(f"System Check Failure. Error Details: ")
        return
    except FileNotFoundError:
        print(f"!!! Error: Command/Tool not found. Make sure system tools are installed.")
        return """

def is_admin():
    try:
        logging.info("User is ADMIN")
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        logging.info("User is NOT ADMIN.")
        return False

""" def run_script(script):
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
    input("\nPress ENTER key to continue...") """

def check_address_health(url, max_timeout):
    print(f"{GREEN}Installing requests module...{RESET}")
    request_cmd = ["pip", "install", "requests"]
    runresult = subprocess.run(request_cmd, shell=True, text=True)
    if runresult.returncode == 1:
        print("Install failed..")
        logging.error(runresult.stdout)
        logging.error(runresult.stderr)
        return
    try:
        import requests
    except ImportError as e:
        print("Could not import module.")
        logging.exception("Requests module not accessed. {e}")
    start_time = time.time()
    logging.info(f"Starting ping requests. [{start_time}]")
    result = {
        'url':url,
        'success':False,
        'status_code': None,
        'message': 'An unknown error has occurred',
        'time_ms': None
    }
    try:
        response = requests.get(url, timeout=max_timeout)
        response.raise_for_status()
        result['status_code'] = response.status_code
        result['success'] = True
        result['message'] = f'OK. Address is up and running, responded with status code {response.status_code}'
    except requests.exceptions.RequestException as e:
        logging.error(f"CONNECTION ERROR while trying to connect to {url}")
        result['status_code'] = "CONN_ERROR"
        result['message'] = f"Connection error: {type(e).__name__} - Details: {str(e)}"
    except requests.exceptions.HTTPError as e:
        logging.error(f"{e.response.status_code} returned by {url}")
        result["status_code"] = e.response.status_code
        result["message"] = f"HTTP Failure: Address returned {e.response.status_code}"
    except requests.exceptions.Timeout:
        logging.error(f"Max timeout exceeded.")
        result["status_code"] = "TIMEOUT"
        result["message"] = f"Request timed out after {max_timeout}"
    finally:
        end_time = time.time()
        result["time_ms"] = round((end_time - start_time) * 1000, 2)
        logging.info(f"Ending ping requests. [{end_time}]")
    return result

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
            logging.info(f"'{base_dir}' folder created.")
        else:
            print(f"'{base_dir}' folder already exists.")
        print(f'\n   Cloning into "{base_dir}" subdirectories...')
        
        for repo_url in repo_urls:
            repo_name = repo_url.rstrip('/').split('/')[-1].replace('.git', '')
            destination_path = os.path.join(base_dir, repo_name)
            print(f"--- Cloning {repo_url} into {destination_path} ---")
            subprocess.run(["git", "clone", repo_url, destination_path],check=True,capture_output=True,text=True)
            logging.info(f"{repo_url} cloned into git_repos successfully.")
            print(f"--- Cloned successfully ---")
        print("\n   Git Cloning Complete.\n")
        
    except FileNotFoundError:
        print("Error: Git command not found. Make sure Git is installed and in your PATH.\n")
        logging.error("Error: Git command not found. Make sure Git is installed and in your PATH.\n")
    except subprocess.CalledProcessError as e:
        print("Error cloning git repository. Check URL or path permissions. \n")
        print(f"Command: {e.cmd}")
        print(f"Return Code: {e.returncode}")
        print(f"Stderr (Git output): {e.stderr.strip()}")
        logging.error(f"Error cloning git repository. Check URL or path permissions.{e}")
    except Exception as e:
        print(f"\033[91mAn unexpected error occurred. Check log for details\033[0m]")
        logging.exception("Traceback, git_clone: ")
        
    input("\nPress ENTER key to continue...")
    subprocess.run(["cls"], shell=True)

def hide_system_files():
    files_to_hide = ["setup.bat", "plem.py", "build.bat", "lab.py", "version_info.txt", "lab_manager_logs.log", "lab_icon.ico", "README.txt"]
    # FILE_ATTRIBUTE_HIDDEN = 2
    # FILE_ATTRIBUTE_SYSTEM = 4
    # Combined = 6
    for file_name in files_to_hide:
        file_path = base_dir / file_name
        if file_path.exists():
            try:
                # Use ctypes to set Windows file attributes to Hidden + System
                ctypes.windll.kernel32.SetFileAttributesW(str(file_path), 6)
            except Exception as e:
                logging.error(f"Failed to hide {file_name}: {e}")
hide_system_files()

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
        logging.info(f"Created {venv_name} successfully in {base_dir}")
        print("  Venv created successfully!\n")
    except subprocess.CalledProcessError as e:
        logging.error(f"Error creating virtual environment: {e}")
        logging.exception("Unexpected crash encountered. Traceback: ")
        print("Error: Failed to create Venv.\n")
        print(f"Command executed: {e.cmd}")
        print(f"Stdout: {e.stdout.strip()}")
        print(f"Stderr: {e.stderr.strip()}")
    input("\nPress ENTER key to continue...")
    
def sort():
    target_dir = input("\033[92mEnter the directory path to sort (e.g., ./downloads): \033[0m").strip()

    if not os.path.isdir(target_dir):
        print(f"\nError: Directory '{target_dir}' not found.\n")
        logging.warning(f"Target sort directory not found: {target_dir}")
        return
    print(f"\nSorting files in: {target_dir}\n")
    logging.info("Sorting process initiated.")
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
            logging.info(f"Created new destination folder at {dest_folder}")
            logging.info(f"Destination folder at {dest_folder} created.")
            shutil.move(source_path, os.path.join(dest_folder, filename))
            print(f"Moved {filename} to {extensions[file_extension]}\n")
            logging.info(f"Moved {filename} to {extensions[file_extension]}\n")
    print("   Directory sorting complete.")
    logging.info("Sorting process COMPLETE")
    input("\nPress ENTER key to continue...")

def update_venv_deps():
    venv_to_update = input("\033[92mEnter venv name ('all' to update all venvs): \033[0m")
    venvs = []
    if venv_to_update == "all":
        elements = [item for item in os.listdir(base_dir) if os.path.isdir(os.path.join(base_dir, item))]
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
            execute_task(pip_cmd, "Upgrading PIP")
            freeze_command = [venv_path_s, '-m', 'pip', 'freeze']
            print("Listing installed packages for upgrade...")
            try:
                freeze_result = subprocess.run(freeze_command,capture_output=True,text=True,check=True)
                packages_to_upgrade = freeze_result.stdout.strip().splitlines()
                if not packages_to_upgrade:
                    print("No packages found in the virtual environment to upgrade.")
                    time.sleep(2)
                    return
                print(f"Found {len(packages_to_upgrade)} packages. Starting individual upgrades...")
                for line in packages_to_upgrade:
                    package_name = line.split('==')[0].strip()
                    upgrade_command = [venv_path_s, '-m', 'pip', 'install', '-U', package_name]
                    print(f"-> Upgrading {package_name}...")
                    subprocess.run(upgrade_command,capture_output=False,check=True)
                    logging.info(f"Upgrading {line} started.")
                print("\n--- All packages in the virtual environment have been upgraded. ---")
            except subprocess.CalledProcessError as e:
                print(f"\nUpgrade failed for a package. Check the logs.")
                logging.error("Error encountered while upgrading package.")
                logging.error(f"Error log: {e}")            
            except Exception as e:
                print(f"\nAn unexpected error occurred: {e}")
                logging.exception("Traceback for failed upgrade, update_venv_deps: ")
            print("All PIP packages updated.")
            print(f"Finished updating packages for {venv}")
    elif venv_to_update in os.listdir(os.path.dirname(__file__)):
        print("\nUpdating pip...")
        venv_path = os.path.join(venv_to_update, 'scripts', 'python.exe')
        pip_cmd = [venv_path, '-m', 'pip', 'install', '--upgrade', 'pip']
        execute_task(pip_cmd, "Upgrading PIP")
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
                logging.info(f"Upgrading {line} started.")
            print("\n--- All packages in the virtual environment have been upgraded. ---")
        except subprocess.CalledProcessError as e:
            print(f"\033[91m\nUpgrade failed for a package. Check the logs.\033[0m")
            logging.error("Error encountered while upgrading package.")
            logging.error(f"Error log: {e}")       
        except Exception as e:
            print(f"\033[91m\nAn unexpected error occurred. Check the logs for details.\033[0m")
            logging.exception("Traceback for failed upgrade, update_venv_deps: ")
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
        execute_task(python_version_check_cmd, "Python Check")
        git_version_check_cmd = ["git", "--version"]
        execute_task(git_version_check_cmd, "Git Check")
        print("\n   Checking Virtual Environments...\n")
        venvs = []
        elements = [item for item in os.listdir(base_dir) if os.path.isdir(os.path.join(base_dir, item))]
        for folder in elements:
            if os.path.exists(f"{folder}/scripts/python.exe"):
                print(f"Folder {folder} is a venv. Appending to venv list...") 
                logging.info(f"{folder} is a virtual environment")
                venvs.append(folder)
        logging.info(f"{len(venvs)} virtual environments are present in the base directory.")
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
                logging.error(f"Freeze command failed. Error log: {e}")            
            except Exception as e:
                print(f"\033[91m\nAn unexpected error occurred. Check logs for details.\033[0m")
                logging.exception(f"Unexpected crash occured, show_env_status: ")
        sys_scan = input("\033[92mRun system scans (y/n): \033[0m")
        if sys_scan == "y":
            run_system_check_cmd = ["sfc", "/scannow"]
            execute_task(run_system_check_cmd, "System Scan")
            run_system_health_check_cmd = ["DISM", "/Online", "/Cleanup-Image", "/CheckHealth"]
            execute_task(run_system_health_check_cmd, "System Health Check")
            system_health_restore_health_cmd = ["DISM", "/Online", "/Cleanup-Image", "/RestoreHealth"]
            fix = input("\nRun '/RestoreHealth' to fix system image (y/n): ")
        else:
            input("\nPress ENTER key to continue...")
            return
        if fix == "y":
            execute_task(system_health_restore_health_cmd, "System Restore Health")
        else:
            pass
        logging.info("sfc and DISM commands successfully run.")
        input("\nPress ENTER key to continue...")
    else:
        print("Relaunching as administrator to perform system scan...")
        script_path = os.path.abspath(sys.argv[0])
        admin_args = "--scan"
        logging.info(f"Relaunched application to elevate rights and run system scans.")
        logging.info("ADMIN Terminal Start.")
        ctypes.windll.shell32.ShellExecuteW(None, "runas", script_path, admin_args, None, 1)
        input("\nPress ENTER key to continue...")

def install_packages():
    venv_to_install_to = input("\033[92mEnter venv name: \033[0m")
    package_to_install = input("\n\033[92mEnter package name: \033[0m")
    packages_to_install = package_to_install.split(" ")
    if venv_to_install_to in os.listdir(base_dir):
        venv_to_install_to_py_path = os.path.join(venv_to_install_to, 'scripts', 'python.exe')
        install_cmd = [venv_to_install_to_py_path, "-m", "pip", "install"] + packages_to_install
        print(f"Installing {len(packages_to_install)} packages via pip...")
        logging.info(f"Installing {len(packages_to_install)} packages via pip...")
        execute_task(install_cmd, "Package Installation")
    else:
        print("ERROR: Venv not found")
        print(f"{venv_to_install_to} not found in {os.path.dirname(__file__)}")
    input("\nPress ENTER key to continue...")

def install_apps():
    print("Checking if Chocolatey is installed...")
    time.sleep(1)
    if not is_choco_available():
        print("\n!!! ERROR: Chocolatey ('choco' command) not found.")
        print("Please ensure Chocolatey is installed and added to your system PATH.")
        return
    app_to_install = input("\033[92mEnter app name(s): \033[0m").strip()
    if not app_to_install:
        print("No app name provided. Exiting.")
        return
    apps_to_install = app_to_install.split(" ")
    force_upgrade = False
    pre_installed_apps = [app for app in apps_to_install if is_choco_package_installed(app)]
    if pre_installed_apps:
        print(f"\nPackages already installed: {', '.join(pre_installed_apps)}")
        choice = input("\033[92mDo you want to FORCE an upgrade/reinstall for these? (y/n): \033[0m").lower().strip()
        if choice == 'y':
            force_upgrade = True
    print(f"\nStarting installation/upgrade of {len(apps_to_install)} app(s) via choco...")
    for app in apps_to_install:
        install_cmd = ['choco', 'install', app, '-y']
        if is_choco_package_installed(app):
            if force_upgrade:
                install_cmd = ['choco', 'upgrade', app, '-y', '--allow-empty-checksums']
                execute_task(install_cmd, f'Force Upgrade for {app}')
                logging.info(f"Installing/Upgrading {app} via choco...")
            else:
                print(f'\nPackage {app} is already installed. Skipping (run with "y" for force upgrade).')
            continue
        execute_task(install_cmd, f'App/Tool Installation for {app}')
        print("\n")

def check_network_status():
    print("\n--- Internet Address Health Checker ---\n")
    address_input = input("\033[92mInput URL to check (e.g., https://google.com): \033[0m").strip()
    address_inputs = address_input.split(" ")
    if not address_input:
        print("\nError: URL is required.")
        input("\nPress ENTER key to continue...")
        return
    for address in address_inputs:
        if not address.startswith(('http://', 'https://')):
            address = "https://" + f"{address}"
        try:
            print("\nChecking service health... (Max timeout: 5 seconds)")
            result = check_address_health(address, max_timeout=5)
            print("\n--- Health Check Report ---")
            if result['success']:
                print(f"\033[92m[STATUS: SUCCESS]\033[0m")
            else:
                print(f"\033[91m[STATUS: FAILURE]\033[0m")  
            print(f"URL: {result['url']}")
            print(f"Code: {str(result['status_code'])}")
            print(f"Time: {str(result['time_ms'])} ms")
            print(f"Message: {result['message']}") 
        except Exception as e:
            print(f"\033[91m\n!!! An unexpected error occurred. Check log for details.\033[0m")
            logging.exception(f"Unexpected error, 'check_network_status': ")
    input("\nPress ENTER key to continue...")

def save_project_state():
    logging.info("--- Starting Lab Capture ---")
    print("--- Project State Save Initiation ---")
    found_gits = []
    for git_dir in base_dir.rglob(".git"):
        project_path = git_dir.parent
        try:
            git_cmd = ["git", "-C", str(project_path), "remote", "get-url", "origin"]
            git_url = subprocess.run(git_cmd, text=True, capture_output=True, check=True)
            author = git_url.stdout.strip().split("/")[-2]
            found_gits.append(f"{project_path.name} by {author} | {git_url.stdout.strip()}")
        except subprocess.CalledProcessError as e:
            print("Error getting repository info. Check log for details. Skipping..")
            logging.error(f"Error details, save_project_state: {e}")
            continue
    if found_gits:
        logging.info(f"Found {len(found_gits)}.")
        logging.info(f"Writing 'found_gits' to 'projects.txt'")
        projects_dir.write_text("\n".join(found_gits))
        logging.info(f"Successfully saved projects' state of {str(base_dir)}")
        print("Successfully saved git projects' state.")
    else:
        print("No git repos found in base directory.")
        logging.info(f"No git repos found in {base_dir}")
    input("\nPress ENTER key to continue...")

def create_lab_backup():
    script_path = os.path.abspath(sys.argv[0])
    admin_args = ""
    print("--- Lab Backup Process Initiated ---\n")    
    if not is_admin():
        print("Relaunching as administrator...")
        logging.info("ADMIN Terminal Start.")
        ctypes.windll.shell32.ShellExecuteW(None, "runas", script_path, admin_args, None, 1)
        return
    temp_backup = base_dir / "temp"
    if temp_backup.exists(): 
        try:
            shutil.rmtree(temp_backup, onexc=remove_readonly)
            logging.info("Deleted old temporary backup folder.")
        except Exception as e:
            print(f"!!! Error: Could not clear temp folder. Is a file open? {e}")
            return
    try:
        temp_backup.mkdir()
    except Exception as e:
        print(f"Error: {e}")
        return
    ignored = ["venv", ".git", "__pycache__", "lab_manager_backups", "temp", "Scripts", "Lib", ".gitignore", "Include", "pyvenv.cfg"]
    app_files = ["plem.py", "lab.py", "plem.yaml", "setup.bat", "README.txt", "lab_manager_logs.log", "Z_RED.txt", "lab.exe", "build.bat", "version_info.txt"]
    files_copied = 0
    folders_processed = 0
    if projects_dir.exists():
        shutil.copy2(projects_dir, temp_backup)
        print("Found a 'projects.txt' file, appended it to temp.")
    filein = temp_backup / 'info.json'
    logging.info(f"Defined info file path for temporary storage.")
    backup_stats = {}
    for item in base_dir.iterdir():
        if item.name == "git_repos":
            print("[-] Skipping 'git_repos' folder.")
            continue
        if item.name in ignored or (item.is_file() and item.name in app_files):
            if item.is_file():
                print(f"[-] Skipping app file: {item.name}.")
            continue
        if item.is_file() and not item.name in ignored and not item.name in app_files:
            print(f"Found a {item.suffix} file, appending to temp.")
            shutil.copy2(item, temp_backup)
            files_copied += 1
        if item.is_dir():
            folders_processed += 1
            is_venv = (item / "pyvenv.cfg").exists()
            status_type = "[VENV]" if is_venv else "[PROJ]"
            backup_stats[item.name] = status_type
            print(f"\n{status_type} Processing: {item.name}")
            dest_folder = temp_backup / item.name
            for file in item.rglob("*"):
                if file.is_file() and not any(part in ignored for part in file.parts):
                    rel_path = file.relative_to(item)
                    target_path = dest_folder / rel_path
                    try:
                        target_path.parent.mkdir(parents=True, exist_ok=True)
                        shutil.copy2(file, target_path)
                        files_copied += 1
                        print(f"    -> Progress: {files_copied} files backed up...", end="\r")
                    except Exception as e:
                        logging.error(f"Failed to copy {file.name}: {e}")
        with open(filein, "w") as fileinfo:
            json.dump(backup_stats, fileinfo, indent=4)
        logging.info(f"Created info file for {item}.")
        logging.info("Wrote status type to info.json.")
    logging.info("\n" + "="*40)
    logging.info("        BACKUP SUMMARY")
    logging.info("="*40)
    logging.info(f" Folders Scanned:  {folders_processed}")
    logging.info(f" Files Copied:     {files_copied}")
    logging.info(f" Backup Location:  {temp_backup}")
    logging.info("="*40)
    print(f"Processed {folders_processed} folders and backed up {files_copied} files.")

    print("\n--- Compressing files ---")
    if not backup_dir.exists():
        print("'lab_manager_backups' folder not found.")
        logging.info("Creating 'lab_manager_backups' folder to store zip.")
        try:
            backup_dir.mkdir()
            logging.info("Successfully created backups folder.")
        except Exception as e:
            logging.exception(f"Failed to create backups folder: {e}")
    archive_name = backup_dir / f'lab_manager_backup_{int(time.time())}'
    try:
        shutil.make_archive(archive_name, "zip", temp_backup)
        shutil.rmtree(temp_backup)
        print(f"Compressed backup folder created in 'lab_manager_backups' folder.")
        logging.info("Deleted 'temp_backup' folder.")
        logging.info(f"Appended {archive_name} to {backup_dir}")
    except:
        print("Failed to create zip file for backup.")
        logging.error(f"Failed to create zip file {archive_name} or remove temporary storage.")
    input("\nPress ENTER key to continue...")

def rebuild_lab_from_backup():
    temp_backup = base_dir / 'r_temp'
    if temp_backup.exists():
        try:
            shutil.rmtree(temp_backup)
            logging.info("Deleted existing temporary storage.")
        except Exception as e:
            logging.error("Failed to delete existing temporary storage.")
            logging.exception(f"Error: {e}")
            return
    temp_backup.mkdir()
    logging.info("Temporary storage folder created.")
    if not backup_dir.exists():
        print("Backups folder not found")
        logging.warning("'lab_manager_backup' folder not found.")
        return
    backup = input(f"{CYAN}Backup folder name: {RESET}")
    backup_path = backup_dir / f"{backup}.zip"
    if not backup_path.exists():
        print("\nSpecified backup timestamp doesn't exist.")
        logging.warning(f"{backup_path} not found in {backup_dir}")
        return
    print("\nZip file found.")
    logging.info(f"Found {backup} in {backup_dir}")
    with zipfile.ZipFile(backup_path, 'r') as backup_zip:
        backup_zip.extractall(temp_backup)
        logging.info("Extraction into temporary storage complete.")
    backup_info = temp_backup / 'info.json'
    if not backup_info.exists():
        logging.warning("No 'info.json' file found.")
        logging.warning("Virtual environment/Project rebuild cancelled.")
        print("Missing .txt file.")
        return
    print("Found 'info.json' file. Rebuilding venvs/projects...")
    logging.info("info.json file found.")
    with open(backup_info, "r") as infofile:
        info = json.load(infofile)
    if not info:
        print("Nothing found in 'info.json'. Rebuild cancelled.")
        logging.warning(".txt file empty. Can not continue virtual environment/project rebuild.")
    for item in temp_backup.glob("*"):
        if item.is_dir():
            for key in info.keys():
                if item.name == key:
                    logging.info(f"Found {item.name} in 'info.json' file.")
                    if info[item.name] == "[VENV]":
                        logging.info(f"{item.name} is virtual environment.")
                        print(f"-> {item.name} is a virtual environment. Rebuilding...")
                        items_moved = 0
                        venv_name = item.name
                        venv_path = base_dir / venv_name
                        global_py = find_system_python()
                        if os.path.exists(venv_path):
                            print(f"\nVirtual environment '{venv_name}' already exists. Skipping.\n")
                            continue
                        print(f"\nCreating virtual environment '{venv_name}' via {global_py}...\n")
                        try:
                            cmd_string = f'python -m venv "{venv_name}"'
                            subprocess.run(cmd_string, check=True, shell=True, capture_output=False)
                            logging.info(f"Created {venv_name} successfully in {base_dir}")
                            print("  Venv created successfully!\n")
                            for file in item.iterdir():
                                try:
                                    shutil.move(file, venv_path)
                                    print(f"Moved files from backup to virtual environment {venv_name}.")
                                    items_moved += 1
                                except Exception as e:
                                    logging.error("Error moving file from temporary storage.")
                                    logging.exception(f"Details: {e}")
                                    print("Could not move a file.")
                            print(f"Backup complete for {item}")
                            logging.info(f"Successfully moved {items_moved} items from temporary storage to new venv.")
                        except subprocess.CalledProcessError as e:
                            logging.error(f"Error creating virtual environment: {e}")
                            logging.exception(f"Unexpected crash encountered. Traceback: {e}")
                            print("Error: Failed to create Venv.\n")
                            print(f"Command executed: {e.cmd}")
                            print(f"Stdout: {e.stdout.strip()}")
                            print(f"Stderr: {e.stderr.strip()}")
                    else:
                        logging.info(f"{item.name} is a project folder.")
                        print(f"-> {item.name} is a project folder. Rebuilding...")
                        try:
                            shutil.move(item, base_dir)
                            logging.info("Successfully rebuilt project folder into base directory.")
                        except Exception as e:
                                logging.error("Error moving folder from temporary storage.")
                                logging.exception(f"Details: {e}")
                                print("Could not move project folder.")
                        print(f"Backup complete for {item}")
        else:
            if not (base_dir / item.name).exists():
                if not item.name == "info.json" or not item.name == "projects.txt":
                    print(f"{item.name} is a file. Moving to base directory...")
                    shutil.move(item, base_dir)
                    logging.info(f"Moved {item} to base directory")
    print(f"\n{GREEN}Venv / Project Rebuild COMPLETE{RESET}")
    print(f"\n{GREEN}Starting GIT REPO Rebuild...{RESET}\n")
    b_project_dir = temp_backup / "projects.txt"
    if not b_project_dir.exists():
        print("No 'projects.txt' file found.")
        logging.warning("projects.txt file not found.")
        logging.warning("Repository cloning cancelled.")
        time.sleep(2)
        shutil.rmtree(temp_backup)
        return
    raw_gits = b_project_dir.read_text().strip()
    gits = raw_gits.splitlines()
    g_base_dir = "git_repos"
    if not os.path.exists(g_base_dir):
        os.mkdir(g_base_dir)
        print(f"'{g_base_dir}' folder created.")
        logging.info(f"'{g_base_dir}' folder created.")
    else:
        print(f"'{g_base_dir}' folder already exists.")
    for git in gits:
        git_url = git.split("|")[-1].strip()
        repo_url = git_url
        if not repo_url:
            print("\nError: Repository URL is required. Exiting...")
            time.sleep(2)
            shutil.rmtree(temp_backup)
            return
        try:
            print(f'\n   Cloning into "{g_base_dir}" subdirectories...')
            repo_name = repo_url.rstrip('/').split('/')[-1].replace('.git', '')
            destination_path = os.path.join(g_base_dir, repo_name)
            print(f"--- Cloning {repo_url} into {destination_path} ---")
            subprocess.run(["git", "clone", repo_url, destination_path],check=True,capture_output=True,text=True)
            logging.info(f"{repo_url} cloned into git_repos successfully.")
            print(f"--- Cloned successfully ---")
            print("\n   Git Cloning Complete.\n")
            
        except FileNotFoundError:
            print("Error: Git command not found. Make sure Git is installed and in your PATH.\n")
            logging.error("Error: Git command not found. Make sure Git is installed and in your PATH.\n")
        except subprocess.CalledProcessError as e:
            print(f"{RED}Error cloning git repository. Check URL or path permissions. \n{RESET}")
            logging.error(f"Command: {e.cmd}")
            logging.error(f"Return Code: {e.returncode}")
            logging.error(f"Stderr (Git output): {e.stderr.strip()}")
            logging.exception(f"Error cloning git repository. Check URL or path permissions.{e}")
        except Exception as e:
            print(f"\033[91mAn unexpected error occurred. Check log for details\033[0m]")
            logging.exception(f"Traceback, git_clone: {e}")
    shutil.rmtree(temp_backup)
    input("\nPress ENTER key to continue...")

def help():
    green = '\033[92m'  
    reset = '\033[0m'
    readme_path = base_dir / "README.txt"
    try:
        with readme_path.open('r', encoding='utf-8') as readme:
            for line in readme:
                is_header = line.strip().startswith('>>')
                output_line = green + line + reset if is_header else line
                for char in output_line:
                    sys.stdout.write(char)
                    sys.stdout.flush()
                    time.sleep(0.0001)
                sys.stdout.write('\n')
    except FileNotFoundError:
        logging.error(f"Manual missing at {readme_path}")
        print(f"Error: README.txt not found.")
    input("\nPress ENTER key to continue...")

def clear_system_logs():
    print(f"\n{YELLOW}{BOLD} WARNING: This will permanently delete all activity history.{RESET}")
    confirm = input(f"    Are you sure? (y/n): ").lower().strip()
    if confirm == 'y':
        try:
            with log_file.open('w') as f:
                f.write(f"--- Log Cleared by User at {time.ctime()} ---\n")
            logging.info("Log file was reset.")
            print(f"\n{GREEN}Logs cleared successfully.{RESET}")
        except Exception as e:
            logging.exception("Failed to clear logs:")
            print(f"{RED}Error: Access denied to log file.{RESET}")
    else:
        print(f"\n{GRAY}Operation cancelled.{RESET}")
    time.sleep(1.5)
def analyze_logs(limit=5):
    if not log_file.exists():
        print(f"{RED}No log file found.{RESET}")
        return
    print(f"\n{CYAN}{BOLD}RECENT ACTIVITY LOGS (Last {limit}){RESET}")
    print(f"{GRAY}------------------------------------------------------------{RESET}")
    try:
        lines = log_file.read_text().splitlines()
        recent_lines = lines[-limit:]
        for line in recent_lines:
            if "ERROR" in line or "CRITICAL" in line:
                print(f"{RED}{line}{RESET}")
            elif "WARNING" in line:
                print(f"{YELLOW}{line}{RESET}")
            elif "SUCCESS" in line or "Task Started" in line:
                print(f"{GREEN}{line}{RESET}")
            else:
                print(f"{GRAY}{line}{RESET}")
    except Exception as e:
        print(f"{RED}Error reading log file: {e}{RESET}")
    print(f"{GRAY}------------------------------------------------------------{RESET}")
    input("\nPress ENTER key to continue...")
def open_shell_access():
    logging.info("User requested Shell Access.")
    print(f"\n{CYAN}{BOLD}>>> SHELL ACCESS ACTIVATED{RESET}")
    print(f"{GRAY}Type 'exit' to return to Lab Manager Menu.{RESET}\n")
    try:
        subprocess.run("cmd.exe /K prompt LAB-SHELL: $P$G", shell=True)
        logging.info("User exited Shell Access.")
        print(f"\n{GREEN}<<< Returned to Lab Manager.{RESET}")
        time.sleep(1)
    except Exception as e:
        logging.exception("Failed to launch shell access:")
        print(f"{RED}Error: Could not launch shell.{RESET}")
def typewriter_print(text, speed=0.0001, color=""):
    reset = '\033[0m'
    full_text = f"{color}{text}{reset}" if color else text
    
    for char in full_text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(speed)
    sys.stdout.write('\n')

page_limit = 1
def menu():
    page = 0
    while True:
        subprocess.run(["cls"], shell=True)
        header = f"""
    {CYAN}{BOLD}LAB MANAGER v2.0.25{RESET} {GRAY} | UNIOSUN Software Engineering{RESET}
    {GRAY}------------------------------------------------------------{RESET}
    {GRAY}LOGS:{RESET} Active  {GRAY}| DIR:{RESET} {base_dir.name}  {GRAY}| STATUS:{RESET} {GREEN}Ready{RESET}
    {GRAY}------------------------------------------------------------{RESET}
        """
        
        if page == 0:
            content = f"""
    {CYAN}{BOLD}  PRIMARY OPERATIONS             SYSTEM UTILITIES{RESET}
    {GRAY}  ------------------             ----------------{RESET}
      {GREEN}[01]{RESET} PLEM Deployment       {GREEN}[06]{RESET} System Health
      {GREEN}[02]{RESET} Git Integration       {GREEN}[07]{RESET} Package Manager
      {GREEN}[03]{RESET} Environment Setup     {GREEN}[08]{RESET} Tool Installer
      {GREEN}[04]{RESET} File Sorter           {GREEN}[09]{RESET} Network Status
      {GREEN}[05]{RESET} Venv Management       {GREEN}[H]{RESET}  Help Manual

    {GRAY}  [nt] Next Page  >>{RESET}
            """
        else:
            content = f"""
    {CYAN}{BOLD}  V2.0 PORTABILITY               DEVELOPER TOOLS{RESET}
    {GRAY}  ----------------               ---------------{RESET}
      {GREEN}[10]{RESET} Save Snapshot         {GREEN}[L]{RESET} View Recent Logs
      {GREEN}[11]{RESET} Selective Backup      {GREEN}[C]{RESET} Clear System Logs
      {GREEN}[12]{RESET} Environment Rebuild   {GREEN}[S]{RESET} Shell Access

    {GRAY}  << [bk] Back Page{RESET}
            """

        footer = f"""
    {GRAY}------------------------------------------------------------{RESET}
      {YELLOW}[H]{RESET} Help    {YELLOW}[L]{RESET} Logs    {RED}[0]{RESET} Exit Manager
    """
        full_menu = header + content + footer
        typewriter_print(full_menu, speed=0.0001)
        choice = input(f"\n    {CYAN}Selection »{RESET} ").lower().strip()
        if choice == "1":
            subprocess.run(["cls"], shell=True)
            time.sleep(1)
            setup_path = os.path.join(base_dir, "setup.bat")
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
        elif choice == "9":
            subprocess.run(["cls"], shell=True)
            time.sleep(1)
            check_network_status()
        elif choice == "10":
            subprocess.run(["cls"], shell=True)
            time.sleep(1)
            save_project_state()
        elif choice == "11":
            subprocess.run(["cls"], shell=True)
            time.sleep(1)
            create_lab_backup()
        elif choice == "12":
            subprocess.run(["cls"], shell=True)
            time.sleep(1)
            rebuild_lab_from_backup()
        elif choice == "log" or choice == "l":
            subprocess.run(["cls"], shell=True)
            time.sleep(1)
            limit = int(input("\n\033[92mLast log count limit: \033[0m"))
            analyze_logs(limit=limit)
        elif choice == "clr" or choice == "c":
            subprocess.run(["cls"], shell=True)
            time.sleep(1)
            clear_system_logs()
        elif choice == "next" or choice == "nt":
            if page >= page_limit:
                print("\033[92mThis is as far as you can go!\033[0m")
            else:
                subprocess.run(["cls"], shell=True)
                page += 1
            time.sleep(1)
        elif choice == "back" or choice == "bk":
            if page < 1:
                print("\033[92mYou are currently in the homepage, you can't go any further!\033[0m")
            else: 
                subprocess.run(["cls"], shell=True)
                page -= 1
            time.sleep(1)
        elif choice == 's':
            subprocess.run(["cls"], shell=True)
            time.sleep(1)
            open_shell_access()
        elif choice == "h":
            subprocess.run(["cls"], shell=True)
            time.sleep(1)
            help()
        elif choice == "0" or choice == "exit":
            print("\n    Exiting Lab Manager...")
            logging.info("Application exited by user.")
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