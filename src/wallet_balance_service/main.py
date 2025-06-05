import asyncio
from fastapi import FastAPI
from .routes import router
from .db.db import Base, engine
from .consumer import consume

Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(router)

@app.on_event("startup")
async def startup_event():
    asyncio.create_task(consume())