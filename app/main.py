import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.core.logging import setup_logging


@asynccontextmanager
async def lifespan(app: FastAPI):
    setup_logging()
    logging.getLogger("tickets").info("Starting up...")
    yield


app = FastAPI(
    title="Tickets API",
    version="1.0.0",
    description="Mini projet d'entretien, Houssem Eddine Selmi",
    lifespan=lifespan,
)


@app.get("/health", tags=["health"])
def health_check():
    return {"status": "ok"}
