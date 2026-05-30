import uvicorn
from fastapi import FastAPI

from api.url_add import app as url_router

app = FastAPI(title="Uptime Service")

app.include_router(url_router)

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
