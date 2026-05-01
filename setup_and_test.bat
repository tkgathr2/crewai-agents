@echo off
chcp 65001 >nul
echo ============================================================
echo   CrewAI セットアップ＆テスト
echo ============================================================
echo.

echo [1/3] Python バージョン確認...
python --version
if %ERRORLEVEL% neq 0 (
    echo ERROR: Python がインストールされていません
    pause
    exit /b 1
)

echo.
echo [2/3] CrewAI インストール...
pip install "crewai[anthropic]" crewai-tools "httpx[socks]"
if %ERRORLEVEL% neq 0 (
    echo ERROR: インストールに失敗しました
    pause
    exit /b 1
)

echo.
echo [3/3] テスト実行...
python test_quick.py

echo.
echo ============================================================
echo   セットアップ完了
echo ============================================================
pause
