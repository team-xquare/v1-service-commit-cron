import get_commit
import asyncio
import time

s = time.time()

async def main():
    github_ids = ["Sonchaegeon", "hwc9169", "jeongjiwoo0522", "kimxwan0319", "leeseojune53", "hwc9169", "silverbeen", "JaewonKim04"] * 10
    fts = [asyncio.ensure_future(get_commit.run(github_id)) for github_id in github_ids]
    r = await asyncio.gather(*fts)
    return r

a = asyncio.run(main())
e = time.time()
print(len(a), a)
print(e -s )