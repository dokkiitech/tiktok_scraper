import asyncio
from playwright.async_api import async_playwright
import requests
import re
from datetime import datetime

WEBHOOK_URL = 'https://script.google.com/macros/s/AKfycbwabuV54SvTndvIyumukcMDYLWTpefxo4FAzZ8CHPq-B6QBERiVCVLBD8zQKLk5We2a/exec'  # ← GASの動画用URLに差し替えて！

async def scrape_recommended_videos():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context(viewport={"width": 500, "height": 800})
        page = await context.new_page()

        await page.goto("https://www.tiktok.com/ja-JP/")
        await asyncio.sleep(5)

        seen_ids = set()

        while True:
            html = await page.content()
            matches = re.findall(r'href="/@([a-zA-Z0-9_.]+)"', html)
            for user_id in matches:
                if user_id not in seen_ids:
                    seen_ids.add(user_id)
                    print(f"🎬 ID検出: {user_id}")
                    payload = {
                        'userId': user_id,
                        'source': 'recommend-instance',
                        'timestamp': datetime.now().isoformat()
                    }
                    try:
                        res = requests.post(WEBHOOK_URL, json=payload)
                        if res.text.strip() == 'duplicate':
                            print(f"⚠️ 重複: {user_id}")
                        else:
                            print(f"✅ 送信成功: {user_id}")
                    except Exception as e:
                        print("❌ エラー:", e)

            await page.keyboard.press("ArrowDown")
            await asyncio.sleep(2)

        await browser.close()

asyncio.run(scrape_recommended_videos())
