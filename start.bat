@echo off
chcp 65001 > nul

:: Python 실행 경로 탐색
set PYTHON=
where python >nul 2>&1 && set PYTHON=python
if "%PYTHON%"=="" (
    if exist "%LOCALAPPDATA%\Programs\Python\Python312\python.exe" (
        set PYTHON=%LOCALAPPDATA%\Programs\Python\Python312\python.exe
    )
)
if "%PYTHON%"=="" (
    if exist "%LOCALAPPDATA%\Programs\Python\Python311\python.exe" (
        set PYTHON=%LOCALAPPDATA%\Programs\Python\Python311\python.exe
    )
)
if "%PYTHON%"=="" (
    echo Python을 찾을 수 없습니다. setup.bat 를 먼저 실행하세요.
    pause
    exit /b 1
)

"%PYTHON%" main.py
