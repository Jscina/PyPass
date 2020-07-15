#!/bin/bash
cd src
echo Installing necessary modules
pip -q install cryptography PyQt5 pyinstaller
echo Creating PyPass.exe
pyinstaller -w --onefile --icon=locked.ico PyPass.py
echo Removing unnecessary modules
pip -y -q uninstall cryptography PyQt5 pyinstaller
echo Sorting Files
mv locked.ico ../locked.ico
mv/dist/PyPass.exe ../PyPass.exe
echo "" > ../usernames.txt
echo "" > ../passwords.txt
cd ../
echo Deleting Unnecessary Directory
rm -rf src
rm -rf install.bat
echo You may delete this installation file now