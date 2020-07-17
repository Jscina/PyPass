#!/bin/bash
cd src
echo Installing necessary modules
pip -q install cryptography PyQt5 pyinstaller
echo Creating PyPass.exe
pyinstaller -w --onefile --icon=locked.ico PyPass.py
echo Removing unnecessary modules
pip -y -q uninstall cryptography PyQt5 pyinstaller
cd ../
echo Deleting Unnecessary Directory
rm -rf src/build && rm -rf src/__pycache__
rm -rf src/*.spec
rm -rf install.bat
mv src/dist/* ../PyPass
rm -rf src
echo You may delete this installation file now
