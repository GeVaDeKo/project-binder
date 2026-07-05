@echo off
echo Updating Project-Binder...
set INSTALL_DIR=%USERPROFILE%\.project-binder

echo Updating Project-Binder...
if not exist "%INSTALL_DIR%" (
    echo Project-Binder is not installed yet.
    echo Run install.bat first.
    pause
    exit /b 1
)

rmdir /S /Q "%INSTALL_DIR%\binder"
mkdir "%INSTALL_DIR%\binder"

xcopy /E /I /Y binder "%INSTALL_DIR%\binder"
copy /Y project-binder.py "%INSTALL_DIR%\project-binder.py"
copy /Y binder.bat "%INSTALL_DIR%\binder.bat"

echo.
echo Update complete!
pause