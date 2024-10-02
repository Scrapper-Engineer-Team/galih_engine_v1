import asyncio
import re
from playwright.async_api import Playwright, async_playwright, expect


async def run(playwright: Playwright) -> None:
    browser = await playwright.chromium.launch(headless=False)
    context = await browser.new_context()
    page = await context.new_page()
    await page.goto("https://sipukat.kemendesa.go.id/petaterpadu.php?v=2021")
    await asyncio.sleep(1)
    await page.hover('//*[@id="map"]/div[2]/div[2]/div')
    await asyncio.sleep(1)
    await page.get_by_label("Google Street").uncheck()
    await page.get_by_label("Provinsi").uncheck()
    await page.get_by_label("Zoom in").click()
    await asyncio.sleep(1)
    await page.hover('//*[@id="map"]/div[2]/div[2]/div')
    await page.get_by_label("Kawasan Trans.").uncheck()
    await page.get_by_label("RTSP").check()

    await asyncio.sleep(1)

    await page.evaluate("gotoxy(140.679220993,-7.396393214475)")
    await asyncio.sleep(1)
    
    mlt = (540,166)
    mlb = (540,747)
    mrt = (1409,166) 
    mrb = (1409,747)

    for x in range(540, 1410 + 4, 4):
        for y in range(170, 750 + 4, 4):
            await page.mouse.click(x, y)
            print('lagi ngeklik x:', x, 'y:', y)



    # ---------------------
    await context.close()
    await browser.close()


async def main() -> None:
    async with async_playwright() as playwright:
        await run(playwright)


asyncio.run(main())
