from fastapi import APIRouter
from pydantic import BaseModel

from services.monitoring import monitoring_and_save

app = APIRouter()


class TargetURL(BaseModel):
    url: str


@app.post("/monitor/add")
async def add_url_for_monitoring(data: TargetURL):
    url = data.url

    await monitoring_and_save(url)

    return {"message": f"{url} successfully added"}
