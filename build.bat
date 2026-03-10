@echo off
chcp 65001 > nul
echo ===================================================
echo   captureSolvedAC - .exe 빌드 스크립트
echo ===================================================
echo.

echo [1/3] 패키지 설치 중...
pip install -r requirements.txt
if %errorlevel% neq 0 ( echo 오류: pip install 실패 & pause & exit /b 1 )

echo.
echo [2/3] Playwright Chromium 설치 중...
playwright install chromium
if %errorlevel% neq 0 ( echo 오류: playwright install 실패 & pause & exit /b 1 )

echo.
echo [3/3] PyInstaller 빌드 중...
pyinstaller captureSolvedAC.spec --clean --noconfirm
if %errorlevel% neq 0 ( echo 오류: PyInstaller 빌드 실패 & pause & exit /b 1 )

echo.
echo ===================================================
echo   빌드 완료!
echo   dist\captureSolvedAC.exe 파일을 확인하세요.
echo   처음 실행 시 Chromium 브라우저가 자동 설치됩니다.
echo ===================================================
pause
