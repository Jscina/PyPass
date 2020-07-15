@echo off
cd %CD%\src
echo Installing necessary modules
pip -q install cryptography PyQt5 pyinstaller
echo Creating PyPass.exe
pyinstaller -w --onefile --icon=locked.ico PyPass.py
echo Removing unnecessary modules
pip -y -q uninstall cryptography PyQt5 pyinstaller
echo Sorting Files
move %CD%\locked.ico ..\locked.ico
move %CD%\dist\PyPass.exe ..\PyPass.exe
echo "" > ..\usernames.txt
echo "" > ..\passwords.txt
cd ..\
echo Deleting Unneeded Directory
rmdir /Q /S %CD%\src
echo Done