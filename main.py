import asyncio
from playwright.async_api import async_playwright
import requests
import re
from datetime import datetime
import os

WEBHOOK_URL = 'https://script.google.com/macros/s/AKfycbytrfkniHTWKsXkNOD7hQNyYEcmOBMD7p89OmgXOsLkVD-LelEkrIEyoJJKv34HQxTw/exec'
SHARD_FILE = 'shard.txt'
KEYWORD_FILE = 'keyword.txt'

def load_keywords():
    try:
        with open(KEYWORD_FILE, 'r', encoding='utf-8') as f:
            lines = [line.strip() for line in f if line.strip()]
            print(f"✅ 読み込んだキーワード数: {len(lines)}")
            return lines
    except Exception as e:
        print(f"❌ keyword.txt 読み込みエラー: {e}")
        return []

def load_sent_ids():
    if not os.path.exists(SHARD_FILE):
        print("🆕 shard.txt が見つからないので新規作成するよ")
        return set()
    with open(SHARD_FILE, 'r', encoding='utf-8') as f:
        sent = set(line.strip() for line in f if line.strip())
        print(f"📂 読み込み済みID数: {len(sent)}")
        return sent

def save_sent_id(user_url):
    with open(SHARD_FILE, 'a', encoding='utf-8') as f:
        f.write(user_url + '\n')
    print(f"📝 shard.txt に追記: {user_url}")

async def scrape_keyword(keyword, sent_ids):
    query = keyword.replace(' ', '%')
    search_url = f"https://www.tiktok.com/search/video?q={query}"
    print(f"\n🔍 キーワード検索: {keyword}")
    print(f"🌐 アクセスURL: {search_url}")

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context(viewport={"width": 600, "height": 800})
        page = await context.new_page()

        try:
            await page.goto(search_url)
            print("✅ 検索ページにアクセス成功")
            print("⏳ 10秒待機中（TikTokの初期ロード猶予）...")
            await asyncio.sleep(15)

            locator = page.locator("a[href*='/video/']")
            count = await locator.count()
            print(f"🎞️ 検出された動画数: {count}")
            if count == 0:
                print("⚠️ 動画が見つかりません。スキップ")
                await browser.close()
                return

            await locator.first.click()
            print("✅ 最初の動画をクリック")
            await asyncio.sleep(3)

        except Exception as e:
            print(f"❌ 動画クリック失敗: {e}")
            await browser.close()
            return

        last_url = ""
        while True:
            try:
                current_url = page.url
                print(f"➡️ 現在の動画URL: {current_url}")

                if current_url != last_url and '/video/' in current_url and '@' in current_url:
                    last_url = current_url
                    match = re.search(r'tiktok\.com/@([^/]+)', current_url)
                    if match:
                        user_id = match.group(1)
                        user_url = f"https://www.tiktok.com/@{user_id}"
                        if user_url in sent_ids:
                            print(f"⚠️ 重複スキップ: {user_url}")
                        else:
                            payload = {
                                'userId': user_id,
                                'source': f'keyword:{keyword}',
                                'timestamp': datetime.now().isoformat()
                            }
                            print(f"📡 GASへ送信: {payload}")
                            res = requests.post(WEBHOOK_URL, json=payload)
                            print(f"📬 GASステータス: {res.status_code} / レスポンス: {res.text.strip()}")

                            if res.status_code == 200 and res.text.strip() != 'duplicate':
                                save_sent_id(user_url)
                                sent_ids.add(user_url)
                            else:
                                print("⚠️ GAS側でスキップ or duplicate")

                await page.keyboard.press("ArrowDown")
                print("⬇️ ↓キー送信 → 次の動画へ")
                await asyncio.sleep(2)

            except Exception as e:
                print(f"❌ スクロール中断: {e}")
                break

        await browser.close()

async def main():
    keywords = load_keywords()
    if not keywords:
        print("🛑 キーワードが空です。終了します")
        return

    sent_ids = load_sent_ids()
    for keyword in keywords:
        await scrape_keyword(keyword, sent_ids)

asyncio.run(main())
