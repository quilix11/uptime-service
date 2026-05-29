import json

import redis.asyncio as aioredis

from services.pinger import ping_website

rc = aioredis.from_url("redis://localhost:6379")


async def monitoring_and_save(url: str):
    result = await ping_website(url)

    data = json.dumps(result)

    await rc.set(url, data)
