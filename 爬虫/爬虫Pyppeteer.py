import requests
from pyquery import PyQuery as pq

# 普通方式
url = 'http://quotes.toscrape.com/js/'
response = requests.get(url)
doc = pq(response.text)
print('Quotes: ', doc('.quote').length)

# pyppeteer方式
import asyncio
from pyppeteer import launch
from pyquery import PyQuery as pq

async def main():
    browser = await launch()
    page = await browser.newPage()
    await page.goto('http://quotes.toscrape.com/js/')
    doc = pq(await page.content())
    print('Quotes: ', doc('.quote').length)
    await browser.close()

asyncio.get_event_loop().run_until_complete(main())


# 模拟网页截图，保存pdf
async def main():
    browser = await launch()
    page = await browser.newPage()
    await page.goto('http://quotes.toscrape.com/js/')
    await page.screenshot(page='example.png')
    await page.pdf(path='example.pdf')
    dimensions = await page.evaluate('''() => {
        return {
            width: document.documentElement.clientWidth,
            height: document.documentElement.clientHeight,
            deviceScaleFactor: window.devicePixelRatio,
        }
    }''')

    print(dimensions)

    await browser.close()

asyncio.get_event_loop().run_until_complete(main())

