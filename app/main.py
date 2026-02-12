from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.database.pool import db_pool
from app.routers import router as main_router
from fastapi.middleware.cors import CORSMiddleware
import logging

logger = logging.getLogger("uvicorn")

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting application")
    await db_pool.connect()
    yield
    await db_pool.disconnect()
    logger.info("Stopping application")

app = FastAPI(
    title="OYAPI",
    description="API для Telegram Mini App недвижимости",
    version="0.1.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health", tags=["System"])
async def healthcheck():
    return {"status": "ok"}

app.include_router(main_router)
