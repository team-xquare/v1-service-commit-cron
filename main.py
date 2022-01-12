import get_commit
import asyncio
import time
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

async def main():
    github_ids = ["Sonchaegeon", "hwc9169", "jeongjiwoo0522", "kimxwan0319", "leeseojune53", "hwc9169", "silverbeen", "JaewonKim04"] * 10
    fts = [asyncio.ensure_future(get_commit.run(github_id)) for github_id in github_ids]
    r = await asyncio.gather(*fts)
    return r

def lambda_handler(event, context):
    logging.info('깃허브 커밋 수 크롤러 동작.....')
    start = time.time()
    a = asyncio.run(main())
    end = time.time()
    logging.info('총 소요 시간: %v', end - start)

    return a

