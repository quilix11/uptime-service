import taskiq
import taskiq_redis
from sqlalchemy.future import select
from taskiq import TaskiqEvents
from taskiq.schedule_sources import LabelScheduleSource

from db.database import SessionLocal, engine
from db.models import Base, Website
from services.monitoring import monitoring_and_save

broker = taskiq_redis.ListQueueBroker("redis://localhost:6379")
scheduler = taskiq.TaskiqScheduler(broker, sources=[LabelScheduleSource(broker)])


@broker.on_event(TaskiqEvents.WORKER_STARTUP)
async def create_db_tables(state):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def get_all_urls():
    async with SessionLocal() as session:
        query = select(Website.url)
        result = await session.execute(query)
        urls = result.scalars().all()
        return urls


@broker.task(schedule=[{"cron": "* * * * *"}])
async def periodic_ping_launcher():
    urls_to_check = await get_all_urls()
    for url in urls_to_check:
        await monitoring_and_save(url)
