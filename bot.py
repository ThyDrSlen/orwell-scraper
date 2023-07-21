import asyncio
import os
from playwright.async_api import async_playwright
import aiohttp
import ssl
import random
from fake_useragent import UserAgent


auth = os.environ.get('AUTH')
browser_url = f'https://{auth}@brd.superproxy.io:9222'

#TODO 
# setup array so that multiple auths can be used 
# keep track of time or how far scrolled down 
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
                    # await asyncio.sleep(random.uniform(1, 3)) #MAYBE CHANGE THIS
                    print(f'Downloaded {url}')
                else:
                    print(f'Failed to download {url}')
        except Exception as e:
            print(f'Error downloading {url}: {e}')

async def asyncdefmain():
    async with async_playwright() as pw:
        print('Connecting to browser...')
        browser = await pw.chromium.launch(headless=False)
        print('Connected to browser.')
        page = await browser.new_page()
        await page.set_extra_http_headers({'User-Agent': ua.random})
        print('Navigating to page...')
        await page.goto('https://www.goat.com/search', timeout=160000)
        print('Page loaded.')
        await page.wait_for_selector('.jugzgk, .kjpMyF')
        print('Evaluating page...')

        for _ in range(25):  # Scroll 25 times
            image_elements = await page.query_selector_all('.jugzgk, .kjpMyF')
            for image in image_elements:
                url = await image.get_attribute('srcset')
                url = await image.get_attribute('srcset')
                if url is not None:
                    url = url.split(", ")[7].split(" ")[0]   
                alt_text = await image.get_attribute('alt')
                class_name = 'shoes' if 'kjpMyF' in (await image.get_attribute('class') or '') else 'clothes'
                if not os.path.exists(class_name):
                    os.makedirs(class_name)
                filename = f"{alt_text}.png"
                filepath = os.path.join(class_name, filename)
                print(f'Downloading {url} to {filepath}...')
                await download_image(url, filepath)
            await page.evaluate(f"window.scrollBy(0, {random.uniform(300, 7000)});")  # Random scroll distance
            await asyncio.sleep(random.uniform(1, 3.5))  # Random delay between scrolls
        print('Closing browser...')
        await browser.close()

def main():
    asyncio.run(asyncdefmain())

if __name__ == '__main__':
    main()