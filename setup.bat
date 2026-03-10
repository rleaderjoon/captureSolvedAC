@echo off
chcp 65001 > nul
echo ===================================================
echo   captureSolvedAC - 설치 스크립트
echo ===================================================
echo.

:: Python 탐색
set PYTHON=
where python >nul 2>&1 && set PYTHON=python
if "%PYTHON%"=="" (
    if exist "%LOCALAPPDATA%\Programs\Python\Python312\python.exe" (
        set PYTHON=%LOCALAPPDATA%\Programs\Python\Python312\python.exe
    )
)
if "%PYTHON%"=="" (
    echo Python을 찾을 수 없습니다.
    echo https://www.python.org/downloads/ 에서 Python을 설치하세요.
    echo 설치 시 "Add Python to PATH" 체크박스를 반드시 선택하세요.
    pause
    exit /b 1
)

echo 사용할 Python: %PYTHON%
echo.

echo [1/2] Python 패키지 설치 중...
"%PYTHON%" -m pip install -r requirements.txt
if %errorlevel% neq 0 ( echo 오류: pip install 실패 & pause & exit /b 1 )

echo.
echo [2/2] Playwright Chromium 브라우저 설치 중 (약 150MB)...
"%PYTHON%" -m playwright install chromium
if %errorlevel% neq 0 ( echo 오류: playwright install 실패 & pause & exit /b 1 )

echo.
echo ===================================================
echo   설치 완료!
echo   start.bat 를 더블클릭하면 앱이 시작됩니다.
echo ===================================================
pause
