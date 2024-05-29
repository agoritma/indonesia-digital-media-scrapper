import asyncio
import aiohttp
from bs4 import BeautifulSoup

class SimpleWebScrap():
    async def requestContent(self, url:str) -> str:
        async with aiohttp.ClientSession(headers={'user-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36"}) as session:
            async with session.get(url) as response:
                return await response.text()
    
    async def scrapeContent(self, url:str):
        htmlParser = BeautifulSoup(await asyncio.create_task(self.requestContent(url)), "html.parser")
        try:
            tags:list = htmlParser.find("article").find_all(['p', 'td', 'h1'])
            if not tags: raise AttributeError
            contentList:list = [tag.get_text() for tag in tags if tag.get_text().encode('unicode-escape').decode('utf-8', 'strict').startswith('\\u') == False]
        except AttributeError as e:
            tags:list = htmlParser.find("body").find_all(['h1', 'p', 'td'])
            contentList:list = [tag.get_text() for tag in tags if tag.get_text().encode('unicode-escape').decode('utf-8', 'strict').startswith('\\u') == False]
        # return "".join(map(str,contentList))
        return contentList
    
if __name__ == "__main__":
    ws = SimpleWebScrap()
    print(asyncio.run(ws.scrapeContent("https://www.liputan6.com/news/read/5606770/jokowi-takziah-ke-rumah-duka-syarifah-salma-istri-habib-luthfi-di-pekalongan"+"?page=all")))