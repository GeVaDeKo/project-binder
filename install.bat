@echo off
set INSTALL_DIR=%USERPROFILE%\.project-binder

echo Installing Project-Binder...
if exist "%INSTALL_DIR%" rmdir /S /Q "%INSTALL_DIR"
mkdir "%INSTALL_DIR%"

xcopy /E /I /Y binder "%INSTALL_DIR%\binder"
copy /Y project-binder.py "%INSTALL_DIR%\project-binder.py"
copy /Y binder.bat "%INSTALL_DIR%\binder.bat"

echo.
echo Installed Project-Binder to %INSTALL_DIR%
echo Add this to your PATH:
echo %INSTALL_DIR%
pause