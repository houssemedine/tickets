"""Logging configuration."""
import logging
from logging import Logger

def setup_logging(level: int = logging.INFO) -> Logger:
    """Configure root logger + uvicorn loggers."""
    root = logging.getLogger()
    if root.handlers:
        for h in list(root.handlers):
            root.removeHandler(h)

    fmt = "%(asctime)s %(levelname)s %(name)s - %(message)s"
    datefmt = "%Y-%m-%dT%H:%M:%S"

    logging.basicConfig(level=level, format=fmt, datefmt=datefmt)

    for name in ("uvicorn", "uvicorn.error", "uvicorn.access", "fastapi"):
        logging.getLogger(name).setLevel(level)

    logger = logging.getLogger("tickets")
    logger.info("Logging configured")
    return logger
