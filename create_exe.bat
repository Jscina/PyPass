@echo off
pyinstaller -D -w -i=locked.ico PyPass.py
copy %CD%\locked.ico %CD%\dist\PyPass\locked.ico