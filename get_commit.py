import aiohttp
from main import logger
from bs4 import BeautifulSoup

async def run(user: str) -> int:
    async with aiohttp.ClientSession() as session:
        github_url = 'https://github.com/' + user
        async with session.get(github_url) as resp:
            resp = await resp.text()
            soup = BeautifulSoup(resp, features="html.parser")
            object = soup.find('h2', class_='f4 text-normal mb-2')
            try:
                resp = object.getText()
                commit_count = int(resp.split('\n')[1].strip().replace(',', ''))
                logger.info('%s 커밋수: %d', user, commit_count)
                return(commit_count)
            except Exception as e:
                logger.fatal(e)
            
