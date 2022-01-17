import aiohttp
import logging
import json
import redis 

from main import logger
from lxml import html

logger = logging.getLogger()
logger.setLevel(logging.INFO)


async def run(redis: redis.Redis, user: str) -> int:
    async with aiohttp.ClientSession() as session:
        github_url = 'https://github.com/' + user
        async with session.get(github_url) as resp:
            resp = await resp.text()
            tree = html.fromstring(resp)
            try:
                week_commit = await get_week_commit_count(tree)
                logger.info('%s의 일주일 커밋수: %d', user, week_commit)
                total_commit = await get_total_commit_count(tree)
                logger.info('%s의 총 커밋수: %d', user, total_commit)
                commit_count = {'week_commit_count': week_commit, 'total_commit_count': total_commit}
                await redis.set(user, json.dumps(commit_count))
                return {user: json.dumps(commit_count)}
            except Exception as e:
                logger.fatal(e)


async def get_week_commit_count(tree):
    week_commit_count = 0
    week_commits = tree.cssselect('g[transform]')[-1]
    for week_commit in week_commits:
        week_commit_count += int(week_commit.attrib['data-count'])
    
    return week_commit_count


async def get_total_commit_count(tree):
    element = tree.cssselect('h2.f4.text-normal.mb-2')[-1]
    total_commit_count = int(element.text.split('\n')[1].strip().replace(',', ''))

    return total_commit_count