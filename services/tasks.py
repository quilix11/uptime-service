import taskiq
import taskiq_redis
from taskiq.schedule_sources import LabelScheduleSource

from services.monitoring import monitoring_and_save

broker = taskiq_redis.ListQueueBroker("redis://localhost:6379")

scheduler = taskiq.TaskiqScheduler(broker, sources=[LabelScheduleSource(broker)])


async def get_all_urls():
    return ["https://google.com", "https://github.com"]


@broker.task(schedule=[{"cron": "* * * * *"}])
async def periodic_ping_launcher():
    urls_to_check = await get_all_urls()
    for url in urls_to_check:
        await monitoring_and_save(url)
