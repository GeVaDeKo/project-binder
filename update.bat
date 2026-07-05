@echo off
echo Updating Project-Binder...
set INSTALL_DIR=%USERPROFILE%\.project-binder

powershell -ExecutionPolicy Bypass -Command ^
 "Invoke-WebRequest https://raw.githubusercontent.com/GeVaDeKo/project-binder/main/project-binder.py -OutFile '%INSTALL_DIR%\binder\project-binder.py'"

echo.
echo Update complete!