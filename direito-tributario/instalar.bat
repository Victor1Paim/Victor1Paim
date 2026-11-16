@echo off
REM Instalação do kit (Windows). Antes: instale Node.js LTS, Python 3.11+ e FFmpeg (veja LEIA-ME.md).
cd /d "%~dp0"
where node >nul 2>nul || (echo FALTA o Node.js: winget install OpenJS.NodeJS.LTS & pause & exit /b 1)
where python >nul 2>nul || (echo FALTA o Python: winget install Python.Python.3.12 & pause & exit /b 1)
where ffmpeg >nul 2>nul || (echo FALTA o FFmpeg: winget install Gyan.FFmpeg & pause & exit /b 1)
python -m pip install -r requirements.txt || (pause & exit /b 1)
cd video
call npm install || (pause & exit /b 1)
cd ..
echo.
echo Tudo instalado. Teste com:  python scripts\kit.py tudo demo-cafezinho
pause
