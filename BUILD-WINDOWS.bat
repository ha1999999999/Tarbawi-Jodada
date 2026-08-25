@echo off
setlocal EnableExtensions
cd /d "%~dp0"

echo.
echo ==================================================
echo   Tarbawi-Jodada Windows Build
echo ==================================================
echo.

where py >nul 2>nul
if errorlevel 1 goto NO_PYTHON

if not exist ".build_env\Scripts\python.exe" (
  echo Creating an isolated build environment...
  py -3 -m venv ".build_env"
  if errorlevel 1 goto VENV_ERROR
)

set "PY=.build_env\Scripts\python.exe"
echo Installing build dependencies...
"%PY%" -m pip install --upgrade pip pyinstaller reportlab weasyprint
if errorlevel 1 goto DEP_ERROR

if exist dist rmdir /s /q dist
if exist release rmdir /s /q release
mkdir release

echo Building the portable application...
"%PY%" -m PyInstaller --clean "Tarbawi-Jodada.spec"
if errorlevel 1 goto BUILD_ERROR

mkdir "release\Tarbawi-Jodada-Portable"
copy /y "dist\Tarbawi-Jodada.exe" "release\Tarbawi-Jodada-Portable\Tarbawi-Jodada.exe" >nul

set "ISCC="
if exist "%ProgramFiles(x86)%\Inno Setup 6\ISCC.exe" set "ISCC=%ProgramFiles(x86)%\Inno Setup 6\ISCC.exe"
if exist "%ProgramFiles%\Inno Setup 6\ISCC.exe" set "ISCC=%ProgramFiles%\Inno Setup 6\ISCC.exe"

if defined ISCC (
  echo Building the installer...
  "%ISCC%" "build\Tarbawi-Jodada.iss"
  if errorlevel 1 goto INSTALLER_ERROR
  echo.
  echo BUILD COMPLETE
  echo Portable: release\Tarbawi-Jodada-Portable\Tarbawi-Jodada.exe
  echo Installer: release\Tarbawi-Jodada-Setup.exe
  goto DONE
)

echo.
echo PORTABLE BUILD COMPLETE
 echo File: release\Tarbawi-Jodada-Portable\Tarbawi-Jodada.exe
 echo Inno Setup was not found. Install it once, then run this file again.
start "" "https://jrsoftware.org/isdl.php"
goto DONE

:NO_PYTHON
echo Python 3.11, 3.12, or 3.13 was not found.
echo Install Python from the page that will open, then run this file again.
echo During setup, enable: Add Python to PATH
start "" "https://www.python.org/downloads/windows/"
goto FAIL

:VENV_ERROR
echo Could not create the isolated build environment.
goto FAIL

:DEP_ERROR
echo Could not install build dependencies. Internet is needed only during the build.
goto FAIL

:BUILD_ERROR
echo PyInstaller could not create the Windows executable.
goto FAIL

:INSTALLER_ERROR
echo The portable executable was created, but the installer build failed.
goto FAIL

:FAIL
pause
exit /b 1

:DONE
pause
exit /b 0
