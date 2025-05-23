import asyncio
from playwright.async_api import async_playwright
import requests
from datetime import datetime

WEBHOOK_URL = 'https://script.google.com/macros/s/AKfycbxrdqHR3F8B-YeLIRktM01a8nVGblw2Zi7hBCO5pO4IRksowYZMWtj_UkTQin5M7RPa/exec'  # ←あなたのGAS Webhook URLに置き換えてね
NUM_BROWSERS = 8

async def scrape_instance(instance_id):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context(viewport={'width': 400, 'height': 600})
        page = await context.new_page()

        # TikTok Live一覧ページへアクセス
        await page.goto('https://www.tiktok.com/@fukurai.mikoto/live')
        await asyncio.sleep(5)  # 読み込み待ち（時間長めに）

        seen_ids = set()
        last_url = ""

        print(f"[{instance_id}] ✅ 開始完了！配信者のIDを収集中...")

        while True:
            try:
                # ↓キー送信して次のライブに切り替える
                await page.keyboard.press("ArrowDown")
                await asyncio.sleep(2)

                current_url = page.url
                if current_url != last_url and '@' in current_url:
                    last_url = current_url
                    user_id = current_url.split('@')[1].split('/')[0]
                    if user_id not in seen_ids:
                        seen_ids.add(user_id)
                        print(f"[{instance_id}] 💡 ID検出: {user_id}")
                        payload = {
                            'userId': user_id,
                            'source': f'instance-{instance_id}',
                            'timestamp': datetime.now().isoformat()
                        }
                        try:
                            requests.post(WEBHOOK_URL, json=payload)
                        except Exception as e:
                            print(f"[{instance_id}] ❌ GAS送信失敗:", e)

            except Exception as e:
                print(f"[{instance_id}] ❌ エラー発生:", e)
                await asyncio.sleep(5)

        await browser.close()

async def main():
    tasks = []
    for i in range(NUM_BROWSERS):
        tasks.append(scrape_instance(i + 1))
    await asyncio.gather(*tasks)

if __name__ == "__main__":
    asyncio.run(main())
