# 🔬 Lab Setup Manager - UNIOSUN Software Engineering

## Overview

The **Lab Setup Manager** is a portable, executable utility (packaged as `lab.exe` or `menu.exe`) designed to streamline the setup and maintenance of development environments for UNIOSUN Software Engineering students and staff.

By consolidating common command-line tasks (Git, Venv, Pip, Chocolatey, and Windows diagnostics), this tool significantly reduces manual setup time and ensures environment consistency.

⚠️ **Compatibility Note:** This manager is specifically designed for **Windows environments**. Administrative privileges are required for running system scans (Option 6) and installing applications (Option 8).

## ✨ Key Features

* **Portability:** Distributed as a single executable file (e.g., `lab.exe`).
* **Setup Automation:** Executes a linked `setup.bat` script for initial PLEM (Python, Library, Environment, Manager) installation and core tool setup.
* **App Installation (via Chocolatey):** Easily install multiple Windows applications and tools using the Chocolatey package manager.
* **Venv Management:**
    * **Creation:** Automatically detects and uses the system Python executable to create new Virtual Environments.
    * **Dependency Update:** Upgrade PIP and all installed packages within a specified Venv, or all Venvs in the root directory.
    * **Package Installation:** Install new Python packages into a specified Venv.
* **Git Management:** Clone single or multiple Git repositories into a dedicated `git_repos` directory.
* **System Health Checks:** Check installed versions of **Python** and **Git**, list details of all local Venvs, and run powerful Windows system integrity scans (`sfc`, `DISM`).

## 🚀 Getting Started

### Prerequisites

1.  **Windows OS:** This tool is Windows-specific.
2.  **Git:** Git must be installed and in your system's PATH for cloning operations.
3.  **Chocolatey (Optional):** Chocolatey must be installed and in your system's PATH to use the Application Installation feature (Option 8).

### Usage

1.  **Download:** Place the compiled executable (e.g., `lab.exe`) and the supporting files (`setup.bat`, `readme.txt`, etc.) into your desired root directory.
2.  **Run:** Double-click the executable or run it from the command prompt:
    ```bash
    .\lab.exe
    ```
3.  **Navigate:** Use the numbered menu options to select the desired task.



## 📋 Menu Options

| Option | Description | Requirements |
| :---: | :--- | :--- |
| **1** | **Run PLEM Setup** | Requires `setup.bat` in the same directory. |
| **2** | **Clone Git Repository** | Requires Git to be installed and in PATH. |
| **3** | **Create Virtual Environment (Venv)** | Requires System Python in PATH. |
| **4** | **Sort Directories/Files** | None (File management tool). |
| **5** | **Update Venv Dependencies** | Requires a valid Venv. |
| **6** | **Show Environment Status / System Scans** | Elevated (Admin) rights recommended for full scans (`sfc`, `DISM`). |
| **7** | **Install Packages** | Requires a valid Venv and internet access. |
| **8** | **Install Applications/Tools** | **NEW:** Requires Chocolatey (choco) installed and Elevated (Admin) rights. |
| **H** | **Help** | Reads and displays content from `readme.txt`. |
| **0** | **Exit Manager** | None. |

## ⚙️ Core Logic and Functions

### Installation & Checking

* **`install_apps()`:** Prompts the user for one or more application names. It uses the new `is_choco_package_installed()` helper to check if an app is already present via Chocolatey before attempting the install, preventing redundant installations.
* **`is_choco_package_installed(package_name)`:** Executes `choco list [package_name]` and parses the output to verify if the package is installed locally.
* **`find_system_python()`:** Intelligently locates the global Python executable (`python` or `python3`) on the system, even if the current execution environment is the compiled executable, to ensure Venvs are created correctly.

### System Diagnostics

* **`show_env_status()`:** This powerful function bundles all environmental checks:
    1.  Checks Python and Git versions.
    2.  Scans the current directory for Venvs and lists packages installed in each.
    3.  If running as Administrator, prompts the user to run deep system integrity checks (`sfc /scannow` and `DISM /CheckHealth`).
    4.  Handles the relaunch of the program with elevated privileges if needed to run the system scans.

## ALL IN ALL, click the `lab.exe` file to start the application.

## 🤝 Contribution

This tool is a valuable asset to the UNIOSUN Software Engineering community. If you have suggestions for new features, bug fixes, or improvements, please submit an issue or open a pull request.

---

## 📜 License

This project is open-source and available under the MIT License.
