import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.core.logging import setup_logging
from app.core.db import engine
from app.models.ticket import Base
from app.routers.tickets import router as tickets_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    setup_logging()
    logging.getLogger("tickets").info("Starting up...")
    logging.getLogger("tickets").info("App startup: creating tables")
    Base.metadata.create_all(bind=engine)
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


app.include_router(tickets_router, prefix="/v1/tickets", tags=["tickets"])
