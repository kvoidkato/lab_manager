@echo off
echo Cleaning old builds...
rmdir /s /q build dist
del /f lab.spec
echo Starting PyInstaller Build...
C:\Users\Kato\AppData\Local\Programs\Python\Python312\scripts\pyinstaller --noconfirm --onefile --console --icon "lab_icon.ico" --version-file "version_info.txt" lab.py
echo Build Complete!.
pause