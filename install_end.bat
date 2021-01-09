rd /s /q %CD%\python_env
mkdir %CD%\PyPass
copy %CD%\locked.ico %CD%\PyPass\locked.ico
copy %CD%\LICENSE %CD%\PyPass\LICENSE
rd /s /q %CD%\build
move /y %CD%\dist\PyPass.exe %CD%\PyPass\PyPass.exe
rd /s /q %CD%\dist
del %CD%\PyPass.spec
rd /s /q %CD%\src
move %CD%\PyPass C:\PyPass
:: Second half of the installation