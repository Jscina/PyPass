@echo off
pyinstaller -F -w -i=locked.ico PyPass.py
mkdir %CD%\PyPass
copy %CD%\locked.ico %CD%\PyPass\locked.ico
copy %CD%\LICENSE %CD%\PyPass\LICENSE
rd /s /q %CD%\build
move /y %CD%\dist\PyPass.exe %CD%\PyPass\PyPass.exe
rd /s /q %CD%\dist
del %CD%\PyPass.spec
7z a -SFX PyPass_SFX.exe PyPass
rd /s /q %CD%\PyPass