@echo off

ECHO 🪟 Windows環境のセットアップを開始します...

REM Pythonチェック（whereコマンド）
where python >nul 2>nul
IF ERRORLEVEL 1 (
    ECHO ❌ Pythonが見つかりません。インストールしてください。
    START https://www.python.org/downloads/
    EXIT /B
)

REM 仮想環境作成
IF NOT EXIST venv (
    ECHO 🔧 仮想環境を作成中...
    python -m venv venv
)

REM 仮想環境アクティベート
CALL venv\Scripts\activate.bat

REM ライブラリインストール
pip install --upgrade pip
pip install -r requirements.txt

REM Playwrightセットアップ
python -m playwright install

ECHO ✅ セットアップ完了！次回からは python main.py を実行してください
PAUSE
