import aiohttp
import logging
import json

from main import logger
from lxml import html
from handler import rd 

logger = logging.getLogger()
logger.setLevel(logging.INFO)

commit = {
    "user_id": {"week_commit": 123, "total_commit": 1234}
}

async def run(user: str) -> int:
    async with aiohttp.ClientSession() as session:
        github_url = 'https://github.com/' + user
        async with session.get(github_url) as resp:
            resp = await resp.content()
            tree = html.fromstring(resp)
            try:
                week_commit = await get_week_commit_count(tree)
                logger.info('%s의 일주일 커밋수: %d', user, week_commit)
                total_commit = await get_total_commit_count(tree)
                logger.info('%s의 총 커밋수: %d', user, total_commit)
                data_commit = {'week_commit_count': week_commit, 'total_commit_count': total_commit}
            except Exception as e:
                logger.fatal(e)

            rd.set(user, json.dumps(data_commit))

async def get_week_commit_count(tree):
    week_commit_count = 0
    week_commits = tree.xpath('//*[@id="js-pjax-container"]/div[2]/div/div[2]/div[2]/div/div[2]/div[1]/div/div/div/svg/g/g[53]')[0]
    for week_commit in week_commits:
        week_commit_count += int(week_commit['data-count'])
    
    return week_commit_count

async def get_total_commit_count(tree):
    e = tree.xpath('//*[@id="js-pjax-container"]/div[2]/div/div[2]/div[2]/div/div[2]/div[1]/div/h2')
    total_commit_count = int(e[0].text.split('\n')[1].strip().replace(',', ''))
    
    return total_commit_count