import get_commit
import asyncio

async def main():
    commit_count = await get_commit.run('hwc9169')
    print(commit_count)

asyncio.run(main())