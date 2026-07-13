"""Ticket model"""
from datetime import datetime, timezone
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import String, Enum as SAEnum, Integer
from app.schemas.ticket import TicketStatus

class Base(DeclarativeBase):
    """SQLAlchemy declarative base."""

class Ticket(Base):
    __tablename__ = "tickets"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    description: Mapped[str] = mapped_column(String, nullable=False)
    status: Mapped[TicketStatus] = mapped_column(
        SAEnum(TicketStatus), nullable=False, default=TicketStatus.OPEN
    )
    created_at: Mapped[datetime] = mapped_column(default=datetime.now(timezone.utc), nullable=False)
