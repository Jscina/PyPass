@echo off
pyinstaller -D -w -i=locked.ico PyPass.py
copy %CD%\locked.ico %CD%\dist\PyPass\locked.ico
rd /s /q %CD%\build
move /y %CD%\dist\PyPass %CD%\PyPass
rd /s /q %CD%\dist
del %CD%\PyPass.spec