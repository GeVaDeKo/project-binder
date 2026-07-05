@echo off
set "INSTALL_DIR=%USERPROFILE%\.project-binder"

echo Installing Project-Binder...
if exist "%INSTALL_DIR%" rmdir /S /Q "%INSTALL_DIR%"
mkdir "%INSTALL_DIR%"

xcopy /E /I /Y binder "%INSTALL_DIR%\binder"
copy /Y project-binder.py "%INSTALL_DIR%\project-binder.py"
copy /Y binder.bat "%INSTALL_DIR%\binder.bat"
powershell -NoProfile -ExecutionPolicy Bypass -Command "$dir='%INSTALL_DIR%'; $path=[Environment]::GetEnvironmentVariable('Path','User'); if (-not $path) { $path='' }; $items=$path -split ';' | Where-Object { $_ -ne '' }; if ($items -notcontains $dir) { $new=($items + $dir) -join ';'; [Environment]::SetEnvironmentVariable('Path',$new,'User') }"
echo.
echo Installed Project-Binder to %INSTALL_DIR%
echo.
echo Restart your terminal and run:
echo binder C:\path\to\project
pause