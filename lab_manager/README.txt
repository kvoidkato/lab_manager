>>	==========================
>>	----LAB MANAGER MANUAL----
>>	==========================

	DEVELOPER: Bello Royyan A.
	
	DATE CREATED: Tuesday, 2nd December, 2025

	VERSION: v1.0.3

	LAST UPDATE: 05-12-2025: 10:24

	VERSION HISTORY: v1.0.0 [02-12-2025: 15:49]
			 v1.0.1 [03-12-2025: 23:02]
			 v1.0.2 [04-12-2025: 21:34]

	USAGE:
		PLEM SETUP: 
			>> Requires internet connection!
			Setting up computer labs and systems software for Computing students in the
			Faculty Of Computing and Information Technology, FOCIT, UNIOSUN. Runs automatically
			with little supervision.

			Type choice [1] to run the 'setup.bat' file and 'plem.py' script and enter the required
 			inputs.

			Make sure to right-click the script and run as administrator, if not enabled, the
			PLEM Setup will automatically request admin privileges. Press 'Yes' to continue setup.

			To add new tools and apps for installation, navigate to the root directory of the exe file
			and click the 'plem.yaml' file to view, add the packages you want to install via 'pip'
			under the section 'python_dependencies', add the tools/apps to be installed via 'choco'
			under the section 'system_tools'.
			Be sure of the tool name before inputting it there, make sure you input the app name from
			choco not just any name e.g to install vscode editor:

				    >> choco install -y visualstudiocode
				NOT
				    >> choco install -y VS Code
			
			Errors can popup anytime due to several factors, ensure you have a strong internet connection
			and enough disk space for installations, allow 'admin' privileges to run without interference.

			PLEM Setup is designed to install python dependencies/packages first and then install tools/apps,
			the process is run via the 'setup.bat' and 'plem.py', so do not alter any of the files.

		GIT CLONING:
			>> Requires internet connection!
			To make it easier to clone repos from Github and other version control systems, the git cloning
			feature was integrated to aid students to have little or no understanding of the git command line.

		VENV CREATION:
			The venv feature is to make project isolation easier, by creating venvs for each project, python
			dependency isolation is made possible and projects are a lot more accessible.

			NOTE: The PLEM Setup creates a venv in the process, so all python dependencies installed aren't
			      globally installed.

		FILE SORTING:
			An helper script to help organize messy folders, the easy trick to navigate to the target folder
			and copy the path from the top input field e.g if the target folder were the downloads folder:

				  >>  C:\Users\FOCIT\Downloads

			The path should look like this, take note that the 'FOCIT' may be different depending on the current
			user's name. The destination folders are already pre-programmed as:

				  >> '.txt': 'Documents', '.pdf': 'Documents', '.doc': 'Documents',
        			  >> '.docx': 'Documents', '.pptx': "Documents",'.gif': 'Images',
        			  >> '.jpg': 'Images', '.png': 'Images', 'Archives', '.rar': 'Archives',
        			  >> '.zip': '.exe': 'Applications', '.msi': 'Applications', '.apk': 'Applications',
        			  >> '.py': 'Scripts', '.sh': 'Scripts', '.mkv': 'Videos', '.mp4': "Videos",
		
		UPDATING VENV DEPENDENCIES:
			>> Requires internet connection!
			Update all dependencies of a specific venv, to do this, input the name of the venv (ensure it is typed
			correctly to prevent FileNotFoundError) or type in "all", this will automatically search the directory
			where the menu.exe is placed for all venvs, then update all python dependencies present (perfect for 
			up-to-date management of venvs for students).

		INSTALLING PACKAGES:
			>> Requires internet connection!
			This option is to install packages to the specified venv, you can install multiple packages by separating
			with a whitespace like this
				>> Enter package name: django pandas numpy requests
				>> Installing 4 packages via pip...

		HELP MENU:
			A manual of the lab manager executable.

		EXIT:
			Option [0] exits the lab manager.


>>		=======================================
>>			     END OF MANUAL
>>		=======================================

