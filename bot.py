import asyncio
import os
from playwright.async_api import async_playwright
import aiohttp
import ssl
import random
from fake_useragent import UserAgent
from rich.console import Console
from tqdm.asyncio import tqdm as async_tqdm

console = Console()

ua = UserAgent()

async def download_image(url, filepath):
    if os.path.exists(filepath):
        console.print(f'📁 Skipping {url} - already downloaded\n', style="bold red")
        console.print('-' * 50)
        return
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url, ssl=ssl.SSLContext()) as resp:  # SSL verification disabled
                if resp.status >= 200 and resp.status < 300:  # Success
                    with open(filepath, 'wb') as f:
                        f.write(await resp.read())
                    console.print(f'✅ Downloaded {url}\n', style="bold green")
                else:
                    console.print(f'⚠️ Failed to download {url}, status code {resp.status}\n', style="bold red")
                console.print('-' * 50)
        except Exception as e:
            console.print(f'🚫 Error downloading {url}: {e}\n', style="bold red")
            console.print('-' * 50)

async def asyncdefmain():
    async with async_playwright() as pw:
        console.print('Connecting to browser...\n', style="bold blue")
        browser = await pw.chromium.launch(headless=False)
        console.print('Connected to browser.\n', style="bold green")
        console.print('-' * 50)
        page = await browser.new_page()
        await page.set_extra_http_headers({'User-Agent': ua.random})
        console.print('Navigating to page...\n', style="bold blue")
        await page.goto('https://www.goat.com/search', timeout=160000)
        console.print('Page loaded.\n', style="bold green")
        console.print('-' * 50)
        await page.wait_for_selector('.jugzgk, .kjpMyF')
        console.print('Evaluating page...\n', style="bold blue")
        console.print('-' * 50)

        progress_bar = async_tqdm(total=25, ncols=100, desc="Scrolling and Downloading Images")  # tqdm progress bar
        for _ in range(25):  # Scroll 25 times
            image_elements = await page.query_selector_all('.jugzgk, .kjpMyF')
            for image in image_elements:
                url = await image.get_attribute('srcset')
                if url is not None:
                    url = url.split(", ")[-1].split(" ")[0]   
                alt_text = await image.get_attribute('alt')
                class_name = 'shoes' if 'kjpMyF' in (await image.get_attribute('class') or '') else 'clothes'
                if not os.path.exists(class_name):
                    os.makedirs(class_name)
                filename = f"{alt_text}.png"
                filepath = os.path.join(class_name, filename)
                console.print(f'⌛ Downloading {url} to {filepath}...\n', style="bold blue")
                await download_image(url, filepath)
            await page.evaluate(f"window.scrollBy(0, {random.uniform(300, 7000)});")  # Random scroll distance
            await asyncio.sleep(random.uniform(1, 3.5))  # Random delay between scrolls
            progress_bar.update(1)  # update progress after each scroll
            progress_bar.refresh()  # manually refresh the progress bar
        progress_bar.close()

        console.print('Closing browser...\n', style="bold blue")
        console.print('-' * 50)
        await browser.close()

def main():
    asyncio.run(asyncdefmain())

if __name__ == '__main__':
    main()
