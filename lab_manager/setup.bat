@echo off
SETLOCAL ENABLEDELAYEDEXPANSION

SET PYTHON_VERSION=3
SET PLEM_SCRIPT=plem.py 

SET CHOC_INSTALL_CMD=powershell -NoProfile -ExecutionPolicy Bypass -Command "iex ((New-Object System.Net.WebClient).DownloadString('https://chocolatey.org/install.ps1'))"

echo.
echo ===========================================
echo === PLEM Bootstrap: Starting Setup ===
echo ===========================================
echo.

:: --- 1. Check/Install Chocolatey ---
echo [INFO] Checking for Chocolatey...

where choco >nul 2>nul
if %errorlevel% neq 0 (
    echo [INFO] Chocolatey not found. Installing now...
    
    CALL :install_choco
    
    if %errorlevel% neq 0 (
        echo [ERROR] Failed to install Chocolatey. Run this script as Administrator.
        goto :exit_fail
    ) else (
        echo [SUCCESS] Chocolatey installed.
        echo [INFO] Restarting Command Prompt to load Chocolatey environment variables...
        
        start "PLEM Restart" cmd /k "%~dpn0.bat" %*
        goto :eof 
    )
) else (
    echo [INFO] Chocolatey found. Proceeding.
)

:: --- 2. Check/Install Python ---
echo.
echo --- Checking Python ---
where python.exe >nul 2>nul
if %errorlevel% equ 0 (
    echo [INFO] Python is already installed and in PATH. Skipping system install.
) else (
    echo [INFO] Python not found. Installing via Chocolatey...
    
    :: Install Python silently and confirm
    choco install python!PYTHON_VERSION! -y --confirm
    
    if !errorlevel! neq 0 (
        echo [ERROR] Failed to install Python using Chocolatey. Check logs above.
        goto :exit_fail
    ) else (
        echo [SUCCESS] Python installed.
    )
)

:: --- 3. Execute PLEM ---
echo.
echo ===========================================
echo === Python is ready. Executing PLEM... ===
echo ===========================================

python %PLEM_SCRIPT% %*

if %errorlevel% neq 0 (
    echo [ERROR] PLEM script exited with errors.
    goto :exit_fail
)

goto :exit_success

:install_choco
    %CHOC_INSTALL_CMD%
    goto :eof

:exit_success
echo.
echo ===========================================
echo === PLEM Bootstrap Finished Successfully ===
echo ===========================================
goto :exit_debug

:exit_fail
echo.
echo ===========================================
echo === PLEM Bootstrap FAILED ===
echo ===========================================
goto :exit_debug

:exit_debug
echo.
echo Press any key to close the window...
PAUSE >nul
ENDLOCAL
exit /b %errorlevel%