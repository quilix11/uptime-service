import time

import httpx


async def ping_website(url: str):
    async with httpx.AsyncClient(timeout=10) as cl:
        start = time.perf_counter()
        try:
            response = await cl.get(url)
            end = time.perf_counter()
            total_time = end - start

            return {
                "status_code": response.status_code,
                "response_time": int(total_time * 1000),
                "is_online": response.status_code < 400,
            }

        except httpx.TimeoutException:
            total_time = time.perf_counter() - start
            return {
                "status_code": None,
                "response_time": int(total_time * 1000),
                "is_online": False,
            }

        except httpx.RequestError:
            total_time = time.perf_counter() - start
            return {
                "status_code": None,
                "response_time": int(total_time * 1000),
                "is_online": False,
            }
