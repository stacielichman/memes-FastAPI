from fastapi import FastAPI

from app.api.v1.endpoints import meme
from app.db.base import engine, Base

app = FastAPI()


@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


app.include_router(meme.router, tags=["memes"])
