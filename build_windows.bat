@echo off
chcp 65001 >nul
setlocal
cd /d "%~dp0.."
where py >nul 2>nul
if errorlevel 1 (
  echo Python غير مثبت. هذا الملف مخصص لمرحلة البناء فقط.
  exit /b 1
)
py -m pip install --upgrade pyinstaller reportlab
if errorlevel 1 exit /b 1
pyinstaller --noconsole --onefile --name "Tarbawi-Jodada" app\main.py
if errorlevel 1 exit /b 1
echo تم إنشاء الملف التنفيذي داخل مجلد dist.
endlocal
pause
