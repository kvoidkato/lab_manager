>>     ============================================================
>>     ---- LAB MANAGER V2.0: OFFICIAL USER MANUAL             ----
>>     ============================================================

    DEVELOPER: Bello Royyan A.
    COMPANY:   UNIOSUN
    DATE:      Monday, 22nd December, 2025
    VERSION:   v1.0.0 (Official Release)

    OVERVIEW:
    The Lab Setup Manager is a professional-grade utility designed to
    automate the configuration of Computing labs for FOCIT, UNIOSUN.
    It streamlines software deployment, environment isolation, 
    and portable project recovery.

>>     --- SYSTEM PREREQUISITES ---
    1. Internet Connection: Required for PLEM, Git, and Pip tasks.
    2. Admin Privileges: Required for System Scans and Smart Backups.
    3. Disk Space: Ensure sufficient space for backups and installs.

>>     --- KEY FUNCTIONALITIES ---

    [01] PLEM SETUP:
    The automated engine for lab deployment. Uses 'setup.bat' and 'plem.py'
    to install dependencies defined in your configuration files.

    [02] GIT INTEGRATION:
    Simplifies repository deployment. Clones repos into the 'git_repos' 
    directory using isolated subfolders.

    [03] ENVIRONMENT SETUP:
    Generates isolated virtual environments (venvs) to prevent global 
    package pollution and ensure project dependency isolation.

    [04] FILE SORTER:
    Automatically organizes cluttered directories. Files are categorized 
    by extension into Documents, Images, Archives, Scripts, and Apps.

    [05] VENV MANAGEMENT:
    Updates all installed packages within a specific venv or every venv 
    found in the root directory (type 'all').

    [06] SYSTEM HEALTH:
    Runs elevated system checks including Python/Git versioning, SFC 
    scans, and DISM health restoration to fix system images.

    [07] PACKAGE MANAGER:
    Allows for direct installation of specific Python packages into 
    selected virtual environments via Pip.

    [08] TOOL INSTALLER:
    Checks for Chocolatey and automates the installation or force-upgrade 
    of system applications and tools.

    [09] NETWORK STATUS:
    An internet address health checker that pings URLs to verify 
    connection speed, status codes, and service availability.

    [10] SAVE SNAPSHOT (New):
    Scans the local directory for Git repositories and extracts their 
    remote 'origin' URLs to 'projects.txt'.

    [11] SELECTIVE BACKUP (V2.0 Core):
    Performs a "Smart Backup." It compresses your project code but ignores 
    heavy, reproducible data like 'venv', '.git', and junk folders.

    [12] ENVIRONMENT REBUILD (New):
    Reads 'projects.txt' and 'info.json' to automatically clone 
    repositories and recreate venvs on a fresh system.

>>     --- DEBUGGING & LOGGING ---
    V2.0 maintains a persistent diary in 'lab_manager_logs.log'.
    - Type 'L' or 'log': View recent System Events or Errors.
    - Type 'C' or 'clr': Safely clears the log file history.
    - Type 'S': Activates direct Shell Access (CMD) within the manager.

>>     --- TROUBLESHOOTING ---
    - [WinError 5] Access Denied: Right-click lab.exe and 'Run as Administrator'.
    - Connection Error: Verify internet and repository URL spelling.
    - Tool Not Found: Verify Chocolatey or Git is installed in System PATH.

>>     ============================================================
>>     ------------ END OF UNIOSUN SOFTWARE ENGINEERING -----------
>>     ============================================================