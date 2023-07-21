import asyncio
import os
from playwright.async_api import async_playwright
import aiohttp
import ssl
import random
from fake_useragent import UserAgent
import time
from datetime import datetime

auth = "brd-customer-hl_1a46ebb2-zone-scraping_browser1:c3kth4rs56ej"
browser_url = f'https://{auth}@brd.superproxy.io:9222'

ua = UserAgent()

async def download_image(url, filepath):
    if os.path.exists(filepath):
        print(f'Skipping {url} - already downloaded')
        return
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url, ssl=ssl.SSLContext()) as resp:  # SSL verification disabled
                if resp.status == 200:
                    with open(filepath, 'wb') as f:
                        f.write(await resp.read())
                    await asyncio.sleep(random.uniform(1, 9)) #MAYBE CHANGE THIS
                    print(f'Downloaded {url}')
                else:
                    print(f'Failed to download {url}')
        except Exception as e:
            print(f'Error downloading {url}: {e}')

async def asyncdefmain():
    start_time = time.time()

    async with async_playwright() as pw:
        print('Connecting to browser...')
        browser = await pw.chromium.launch(headless=False)
        print('Connected to browser.')
        page = await browser.new_page()
        await page.set_extra_http_headers({'User-Agent': ua.random})
        print('Navigating to page...')
        await page.goto('https://www.goat.com/search', timeout=160000)
        await asyncio.sleep(4)
        print('Page loaded.')
        await page.wait_for_selector('.jugzgk, .kjpMyF')
        await asyncio.sleep(2)
        print('Evaluating page...')

        downloaded_count = 0
        for _ in range(3):  # Scroll 3 times
            image_elements = await page.query_selector_all('.jugzgk, .kjpMyF')
            for image in image_elements:
                url = await image.get_attribute('srcset')
                url = await image.get_attribute('srcset')
                if url is not None:
                    url = url.split(", ")[4].split(" ")[0]  # Get the 200w image URL
                alt_text = await image.get_attribute('alt')
                class_name = 'shoes' if 'kjpMyF' in (await image.get_attribute('class') or '') else 'clothes'
                if not os.path.exists(class_name):
                    os.makedirs(class_name)
                filename = f"{alt_text}.png"
                filepath = os.path.join(class_name, filename)
                print(f'Downloading {url} to {filepath}...')
                await download_image(url, filepath)
                downloaded_count += 1
                if downloaded_count == 10:
                    break
            await page.evaluate(f"window.scrollBy(0, {random.uniform(500, 1000)});")  # Random scroll distance
            await asyncio.sleep(random.uniform(2, 5))  # Random delay between scrolls
            if downloaded_count == 10:
                break

        end_time = time.time()
        total_time = end_time - start_time
        print(f"Downloaded {downloaded_count} images in {total_time:.2f} seconds")

        timestamp = datetime.now().strftime('%-m/%-d/%y @ %-I:%M%p')
        with open('download_time.txt', 'a') as f:
            f.write(f"Downloaded {downloaded_count} images in {total_time:.2f} seconds at {timestamp}\n")

        print('Closing browser...')
        await browser.close()

def main():
    asyncio.run(asyncdefmain())

if __name__ == '__main__':
    main()