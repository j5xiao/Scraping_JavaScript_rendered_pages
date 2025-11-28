import asyncio
from pyppeteer import launch
from pyquery import PyQuery as pq

url = 'https://spa2.scrape.center/'

async def main():
    browser = await launch()
    page = await browser.newPage()
    await page.goto(url)

    await page.waitForSelector('.item .name')
    doc = pq(await page.content())
    names = [item.text() for item in doc('.item .name').items()]
    print("Name: {}".format(names))

    await browser.close()

asyncio.get_event_loop().run_until_complete(main())
