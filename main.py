import asyncio

from services.monitoring import monitoring_and_save


async def main():
    target_url = input("Write your link. Example: google.com")
    await monitoring_and_save(target_url)

if __name__ == "__main__":
    asyncio.run(main())
