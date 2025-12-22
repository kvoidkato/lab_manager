# Lab Manager v1.0.0 🧪

![Version](https://img.shields.io/badge/version-1.0.0-blue)
![Python](https://img.shields.io/badge/python-3.12-green)
![Platform](https://img.shields.io/badge/platform-Windows-lightgrey)

**Lab Manager** is a professional-grade utility designed to automate the configuration, management, and recovery of Computing Lab environments at **FOCIT, UNIOSUN**. It streamlines software deployment, isolates development environments, and provides a "Smart Backup" system for portable project recovery.

---

## ✨ Key Features

* **🚀 Automated PLEM Setup:** One-click deployment of lab dependencies via `setup.bat` and `plem.yaml`.
* **📦 Smart Backups:** Compresses project source code while automatically excluding heavy, reproducible directories (like `venv`, `.git`, and `__pycache__`).
* **🔄 Environment Rebuild:** Uses snapshots (`projects.txt` and `info.json`) to automatically re-clone repositories and recreate virtual environments on fresh systems.
* **🛠️ System Health Suite:** Integrated SFC/DISM scans and network diagnostic tools to ensure lab PCs are running optimally.
* **🧹 File Sorter:** Automatically organizes cluttered directories into categorized folders (Documents, Scripts, Apps, etc.).

---

## 🚀 Getting Started

### Prerequisites
- **Windows 10/11**
- **Python 3.12** (Recommended)
- **Git** & **Chocolatey** (Will be auto-installed if listed in `plem.yaml`)

### Installation & Usage
1. Download the latest release from the `dist` folder.
2. Ensure `plem.yaml`, `setup.bat`, and `plem.py` are in the same directory as `lab.exe`.
3. **Run as Administrator** to allow the tool to perform system repairs and install software.

```bash
# To run from source:
python lab.py

├── lab.exe              # Main compiled executable
├── lab.py (Hidden)      # Source code
├── version_info.txt     # Metadata for Windows properties
├── plem.yaml            # Tool configuration file
├── setup.bat (Hidden)   # Logic for PLEM setup
├── plem.py   (Hidden)   # Core deployment engine
└── README.txt           # User manual

🛠️ Built With
Python 3.12 - Core logic.

PyInstaller - Executable bundling.

Windows API - Administrative and file attribute management.

👤 Developer
Bello Royyan A. UNIOSUN Software Engineering Supporting FOCIT lab infrastructure since 2025.

📄 License
This project is proprietary and developed for use at Osun State University (UNIOSUN). © 2025 Bello Royyan A. All rights reserved.
