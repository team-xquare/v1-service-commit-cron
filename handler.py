import json
import logging
import time
import asyncio
import get_commit
import redis

logger = logging.getLogger()
logger.setLevel(logging.INFO)

rd = redis.StrictRedis(host='redis', port=6379, db=0)

async def main():
    github_ids = ["Sonchaegeon", "hwc9169", "jeongjiwoo0522", "kimxwan0319", "leeseojune53", "hwc9169", "silverbeen", "JaewonKim04"]
    fts = [asyncio.ensure_future(get_commit.run(github_id)) for github_id in github_ids]
    r = await asyncio.gather(*fts)
    return r

def lambda_handler(event, context):
    logging.info('깃허브 커밋 수 크롤러 동작.....')
    start = time.time()
    loop = asyncio.get_event_loop()
    body = loop.run_until_complete(main())
    loop.close()
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
