#!/bin/bash

echo "🍎 Mac環境のセットアップを開始するよ！"

# Python3の存在チェック
if ! command -v python3 &> /dev/null
then
    echo "❌ Python3 が見つかりません。Homebrew経由でインストールします..."
    
    # Homebrewチェック
    if ! command -v brew &> /dev/null
    then
        echo "❌ Homebrew が見つかりません。今からインストールします..."
        /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
        
        echo ""
        echo "✅ Homebrewのインストールが完了しました！"
        echo "⚠️ ターミナルを一度閉じて、再起動してからもう一度このスクリプトを実行してください。"
        exit 0
    fi

    brew install python3
fi

# venvが無ければ作成
if [ ! -d "venv" ]; then
  echo "🔧 仮想環境を作成します..."
  python3 -m venv venv
fi

# venvをアクティベート
source venv/bin/activate

# ライブラリインストール
pip install --upgrade pip
pip install -r requirements.txt

# Playwrightセットアップ
python3 -m playwright install

echo "✅ セットアップ完了！次回からは python3 main.py で起動してください"
