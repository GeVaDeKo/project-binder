@echo off
set INSTALL_DIR=%USERPROFILE%\.project-binder

echo Uninstalling Project-Binder...

if exist "%INSTALL_DIR%" (
    rmdir /S /Q "%INSTALL_DIR%"
    echo Project-Binder removed.
) else (
    echo Project-Binder was not installed.
)

echo.
echo Remove this from your PATH if you added it:
echo %INSTALL_DIR%
pause