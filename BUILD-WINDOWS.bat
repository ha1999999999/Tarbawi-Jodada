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

set "PY_LAUNCHER=py -3"
%PY_LAUNCHER% -c "import sys; print(sys.version)" >nul 2>nul
if errorlevel 1 goto NO_PYTHON

if not exist ".build_env\Scripts\python.exe" (
  echo Creating an isolated build environment...
  %PY_LAUNCHER% -m venv ".build_env"
  if errorlevel 1 goto VENV_ERROR
)

set "PY=.build_env\Scripts\python.exe"
if not exist "%PY%" goto VENV_ERROR

echo Installing build dependencies...
"%PY%" -m pip install --upgrade pip
if errorlevel 1 goto DEP_ERROR
"%PY%" -m pip install -r requirements-build.txt
if errorlevel 1 goto DEP_ERROR

echo Running project tests...
set "PYTHONPATH=%CD%\app"
"%PY%" -m py_compile app\main.py app\web_app.py
if errorlevel 1 goto TEST_ERROR
"%PY%" test_core.py
if errorlevel 1 goto TEST_ERROR
"%PY%" test_exports.py
if errorlevel 1 goto TEST_ERROR
"%PY%" test_lifecycle.py
if errorlevel 1 goto TEST_ERROR

if exist dist rmdir /s /q dist
if exist build\Tarbawi-Jodada rmdir /s /q build\Tarbawi-Jodada
if exist release rmdir /s /q release
mkdir release

echo Building the portable application...
"%PY%" -m PyInstaller --clean "Tarbawi-Jodada.spec"
if errorlevel 1 goto BUILD_ERROR

if not exist "dist\Tarbawi-Jodada.exe" goto BUILD_ERROR
mkdir "release\Tarbawi-Jodada-Portable"
copy /y "dist\Tarbawi-Jodada.exe" "release\Tarbawi-Jodada-Portable\Tarbawi-Jodada.exe" >nul
if errorlevel 1 goto BUILD_ERROR

set "ISCC="
if exist "%ProgramFiles(x86)%\Inno Setup 6\ISCC.exe" set "ISCC=%ProgramFiles(x86)%\Inno Setup 6\ISCC.exe"
if exist "%ProgramFiles%\Inno Setup 6\ISCC.exe" set "ISCC=%ProgramFiles%\Inno Setup 6\ISCC.exe"

if defined ISCC (
  echo Building the installer...
  "%ISCC%" "build\Tarbawi-Jodada.iss"
  if errorlevel 1 goto INSTALLER_ERROR
  if not exist "release\Tarbawi-Jodada-Setup.exe" goto INSTALLER_ERROR
  echo.
  echo BUILD COMPLETE
  echo Portable: release\Tarbawi-Jodada-Portable\Tarbawi-Jodada.exe
  echo Installer: release\Tarbawi-Jodada-Setup.exe
  goto DONE
)

echo.
echo PORTABLE BUILD COMPLETE
echo File: release\Tarbawi-Jodada-Portable\Tarbawi-Jodada.exe
echo Inno Setup was not found. The portable build is still valid.
echo Install Inno Setup once if you also need Setup.exe, then run this file again.
goto DONE

:NO_PYTHON
echo Python 3.12 or a compatible Python 3 installation was not found.
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

:TEST_ERROR
echo Project tests failed. The executable was not built.
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
