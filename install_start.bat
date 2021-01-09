@echo off
%CD%\python_env\Scripts\activate.bat pip install cryptography PyQt5 && pyinstaller -F -w -i=locked.ico %CD%\src\PyPass.py && %CD%\python_env\Scripts\deactivate.bat
:: First half of the installation