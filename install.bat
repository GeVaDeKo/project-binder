@echo off
set INSTALL_DIR=%USERPROFILE%\.project-binder
mkdir "%INSTALL_DIR%" 2>nul

xcopy /E /Y "%~dp0binder" "%INSTALL_DIR%\binder\"
copy /Y "%~dp0project-binder.py" "%INSTALL_DIR%\project-binder.py"
copy /Y "%~dp0binder.bat" "%INSTALL_DIR%\binder.bat"

echo.
echo Installed Project-Binder to %INSTALL_DIR%
echo Add this to your PATH:
echo %INSTALL_DIR%