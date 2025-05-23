
### ✅ `README.md`

````markdown
# TikTokユーザーID スクレイピングツール

おすすめ動画またはLive配信者のページから、TikTokユーザーIDを自動で取得し、Googleスプレッドシートに記録するツールです。

---

## 🖥 対応環境

- macOS（Intel/M1/M2）
- Windows 10/11
- Python 3.x

---

## 🔧 初回セットアップ手順

初回だけ、以下の手順で環境構築を行ってください。

### ◆ Mac の場合

```bash
chmod +x setup_mac.sh
./setup_mac.sh
````

> ⚠️ Homebrewがインストールされていない場合、自動インストールされます。その後、**ターミナルを再起動して再度 `./setup_mac.sh` を実行**してください。

---

### ◆ Windows の場合

1. `setup_win.bat` を**ダブルクリック**
2. 必要な環境構築がすべて自動で行われます
3. 実行後、`python main.py` でツールが起動します

---

## 🚀 2回目以降の起動

環境構築が完了したら、次回以降は以下のコマンドだけで実行できます。

```bash
# Mac
source venv/bin/activate
python3 main.py
```

```bat
:: Windows
venv\Scripts\activate
python main.py
```

---

## 📦 ファイル構成

```
├── main.py               # 実行ファイル（ユーザーIDスクレイピング）
├── setup_mac.sh          # Mac用セットアップスクリプト
├── setup_win.bat         # Windows用セットアップスクリプト
├── requirements.txt      # 使用ライブラリ一覧
├── README.md             # この説明ファイル
```

---

## 💬 補足

* `main.py` の中で指定された Google Apps Script（GAS）URLに対して、POST通信でIDを送信します
* GAS側ではスプレッドシートに自動で追記され、**重複は自動でスキップ**されます

---

## 🧠 注意事項

* TikTokの仕様変更により、HTML構造が変化すると動作しない場合があります
* Googleスプレッドシートの「API公開設定」「シート名」などは事前に正しく設定してください

---

## 😎 開発者向け

このツールは Playwright を使っています。ブラウザ操作の自動化が可能です。

* `requirements.txt` の中身：

  ```text
  playwright
  requests
  ```

* 初回実行時に `python3 -m playwright install` も自動で行われます

---

Enjoy 🎉

```

---

必要なら英語版にもできるし、QRコード付きマニュアルとかもいけるよ📄💕  
他にも加えたい内容あれば言って〜！
```
