import csv

import asyncio
import aiohttp
import async_timeout


from scrapy.http import HtmlResponse

results = []

async def fetch(session, url):
    with async_timeout.timeout(10):
        async with session.get(url) as response:
            return await response.text()

def parse(url, body):
    response = HtmlResponse(url=url, body=body)
    for repository in response.css('li.public'):
        name = repository.xpath('.//a[@itemprop="name codeRepository"]/text()').re_first(r"\n\s*(.*)")
        update_time = repository.xpath('.//relative-time/@datetime').extract_first()
        results.append((name, update_time))

async def task(url):
    async with aiohttp.ClientSession() as session:
        html = await fetch(session, url)
        parse(url, html.encode('utf-8'))

def main():
    loop = asyncio.get_event_loop()
    urls = ('https://github.com/shiyanlou?tab=repositories',
            'https://github.com/shiyanlou?after=Y3Vyc29yOnYyOpK0MjAxNy0wNi0wNlQyMjoyMToxMFrOBZKVZw%3D%3D&tab=repositories',
            'https://github.com/shiyanlou?after=Y3Vyc29yOnYyOpK0MjAxNS0wMS0yNlQwMzozMDoyNVrOAcdiUA%3D%3D&tab=repositories',
            'https://github.com/shiyanlou?after=Y3Vyc29yOnYyOpK0MjAxNC0xMS0yMVQxMDowOTowMlrOAZ0AWQ%3D%3D&tab=repositories')
    tasks = [task(url) for url in urls]
    loop.run_until_complete(asyncio.gather(*tasks))
    with open('/home/shiyanlou/shiyanlou-repos.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(results)

if __name__ == '__main__':
    main()
