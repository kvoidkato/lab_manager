# 🔬 Lab Setup Manager - UNIOSUN Software Engineering

## Overview

The **Lab Setup Manager** is a Python-based utility designed to streamline the setup and maintenance of development environments, particularly for students and staff in the UNIOSUN Software Engineering program. It automates common command-line tasks, making it easier to manage Git repositories, Python Virtual Environments (Venvs), package dependencies, and perform basic system health checks.

This script is primarily intended for **Windows environments** due to its reliance on `ctypes.windll.shell32` for administrative checks and Windows-specific commands like `cls`, `sfc`, and `DISM`.

### ✨ Key Features

* **Setup Automation:** Execute the main `setup.bat` file to perform initial PLEM (Python, Library, Environment, Manager) installation and configuration.
* **App Installation (New):** Install applications and tools easily using the **Chocolatey** package manager for Windows.
* **Git Management:** Clone single or multiple Git repositories into a dedicated `git_repos` directory.
* **Venv Management:**
    * **Creation:** Easily create new Python Virtual Environments.
    * **Dependency Update:** Upgrade PIP and all installed packages within a specified Venv, or all Venvs in the root directory.
    * **Package Installation:** Install new Python packages into a specified Venv.
* **System Health Checks:** Run Windows system scans (`sfc /scannow`, `DISM /CheckHealth`) and check installed versions of **Python** and **Git**. (Requires elevated/administrator privileges).
* **File Sorting:** Organize files in a specified directory into categorized folders (Documents, Images, Archives, Scripts, Videos, Applications).

## 🚀 Getting Started

### Prerequisites

1.  **Python:** Python must be installed and accessible via the system PATH.
2.  **Git:** Git must be installed and accessible via the system PATH for cloning operations.

### Usage

1.  **Download:** Place the `menu.py` (and any associated scripts like `setup.bat` or `el_scan.py` if they exist) into your desired project directory.
2.  **Run:** Execute the script from your command prompt:
    ```bash
    python menu.py
    ```
3.  **Navigate:** Use the numbered menu options to select the desired action.


### 📋 Menu Options

| Option | Description | Notes |
| :---: | :--- | :--- |
| **1** | **Run PLEM Setup** | Executes an external `setup.bat` script (assumed to handle core tool and app installation). |
| **2** | **Clone Git Repository** | Clones one or more repositories into a sub-folder named `git_repos`. |
| **3** | **Create Virtual Environment (Venv)** | Prompts for a Venv name and creates it using `python -m venv`. |
| **4** | **Sort Directories/Files** | Organizes files (e.g., `.pdf`, `.jpg`, `.zip`) in a specified path into dedicated folders. |
| **5** | **Update Venv Dependencies** | Upgrades PIP and all installed packages in a specified Venv or all Venvs. |
| **6** | **Show Environment Status** | Checks for elevated permissions and runs system health checks (`sfc`, `DISM`) and version checks for Python and Git. |
| **7** | **Install Packages** | Prompts for a Venv and package name(s) to install using `pip install`. |
| **8** | **Install Applications (via Choco)** | **NEW:** Installs one or more Windows applications using the Chocolatey package manager. |
| **H** | **Help** | Reads and displays the content of an external `readme.txt` file. |
| **0** | **Exit Manager** | Terminates the script. |

## ⚙️ Functions Explained

The core logic of the script is contained in several helper functions:

### `execute_command` & `execute_check_command`

These functions are wrappers around Python's `subprocess.run()`. They provide consistent logging for command execution, success, and detailed error handling, ensuring users know exactly what command failed and why. `execute_check_command` specifically captures and prints the command's standard output and error log.

### `is_admin`

A Windows-specific function using the `ctypes` library to check if the script is currently running with **administrator (elevated) privileges**. This is crucial for running system diagnostic commands like `sfc` and `DISM`.

### `update_venv_deps`

This function is robust. It can update **all** detected Venvs in the current directory or a single specified Venv. For each Venv, it performs these steps:
1. Upgrades **PIP** itself.
2. Uses `pip freeze` to list **all** installed packages.
3. Iterates through the list and runs `pip install -U <package_name>` to upgrade each one individually.

## ALL IN ALL, click the `lab.exe` file to start the application.

## 🤝 Contribution

This project is part of the UNIOSUN Software Engineering curriculum. Contributions or suggestions for improvement are welcome! Feel free to fork the repository and submit pull requests.

---

## 📜 License

This project is open-source and available under the MIT license.
