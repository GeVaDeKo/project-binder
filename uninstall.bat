@echo off
set INSTALL_DIR=%USERPROFILE%\.project-binder

echo Uninstalling Project-Binder...

rmdir /S /Q "%INSTALL_DIR%"

echo.
echo Project-Binder removed.
pause