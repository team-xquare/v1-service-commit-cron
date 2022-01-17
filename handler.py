import json
import logging
import time
import asyncio
import get_commit
import aioredis

logger = logging.getLogger()
logger.setLevel(logging.INFO)

async def main():
    redis = aioredis.from_url('redis://127.0.0.1')
    github_ids = ["Sonchaegeon", "hwc9169", "jeongjiwoo0522", "kimxwan0319", "leeseojune53", "JaewonKim04", "silverbeen", "JaewonKim04"]
    fts = [asyncio.ensure_future(get_commit.run(redis, github_id)) for github_id in github_ids]
    return await asyncio.gather(*fts)

def lambda_handler(event, context):
    logging.info('깃허브 커밋 수 크롤러 동작.....')
    start = time.time()
    body = asyncio.run(main())
    end = time.time()
    logging.info('총 소요 시간: %s', end - start)


    response = {
        "statusCode": 200,
        "body": json.dumps(body)
    }

    return response

    # Use this code if you don't use the http event with the LAMBDA-PROXY
    # integration
    """
    return {
        "message": "Go Serverless v1.0! Your function executed successfully!",
        "event": event
    }
    """
