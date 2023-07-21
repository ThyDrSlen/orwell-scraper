# Project Image Scraper: Vision Transformer Training

_"In a time of deceit, telling the truth is a revolutionary act."_ - George Orwell

In the spirit of Orwell's pursuit of truth, I present you with a tool that is as straightforward as it is powerful. This is a project that aims to scrape images from the web to train a Vision Transformer model for image classification. The code, written in Python, uses the asyncio, aiohttp, and playwright libraries to asynchronously download images from a website. It is designed to mimic human behavior by scrolling down the page and downloading images as it goes.

**Disclaimer:** This project is for educational purposes only. I do not condone the use of this web scraper for use on goat.com or any other website without explicit permission from the website owners. Always respect the terms of service of any website you scrape.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [How it Works](#how-it-works)
- [Contributing](#contributing)
- [License](#license)

## Installation

To use this script, you need to have Python installed along with the following libraries:

- asyncio
- aiohttp
- playwright
- os
- fake_useragent

You can install these libraries using pip:

```bash
pip install -r requirements.txt
```

Additionally, you will need an account with [BrightData](https://help.brightdata.com/hc/en-us/articles/13362921219729-Getting-started-with-Scraping-Browser) to set up a proxy system. This is necessary to avoid getting blocked when accessing websites.


## Usage

To run the script, simply navigate to the directory where the script is located and run:

```bash
python3 bot.py
```



## How it Works

The script works by launching a headless Chromium browser and navigating to a specific webpage. It then scrolls down the page, mimicking human behavior, and downloads images as it goes. The images are saved in separate directories based on their class (shoes or clothes).

The script uses the `fake_useragent` library to generate a random user agent for each request, making the script harder to detect and block. It also uses a random delay between each scroll and download operation to further mimic human behavior.

The script uses the `aiohttp` library to download the images asynchronously, which makes the script faster and more efficient. It also checks if an image has already been downloaded before attempting to download it, to avoid unnecessary downloads.

## Contributing

I welcome contributions to this project. If you have a feature you'd like to add, or a bug you'd like to fix, please fork the repository, make your changes, and submit a pull request.

## License

This project is licensed under the MIT License. 

_"The further a society drifts from truth, the more it will hate those who speak it."_ - George Orwell

In the spirit of Orwell's pursuit of truth, I present this tool to you. Use it wisely, and may it serve you well in your pursuit of knowledge and truth.
