from datetime import datetime
from enum import Enum
from pydantic import BaseModel, Field, ConfigDict


class TicketStatus(str, Enum):
    OPEN = "open"
    STALLED = "stalled"
    CLOSED = "closed"

class TicketBase(BaseModel):
    title : str = Field(..., min_length=1, max_length=200)
    description : str = Field(..., min_length=1)

class TicketRead(TicketBase):
    """Schema pour exposer un ticker
    """
    id: int
    status: TicketStatus
    created_at: datetime


    model_config = ConfigDict(from_attributes=True)

class TicketCreate(TicketBase):
    """Schéma d'entrée pour créer un ticket."""
    pass

class TicketUpdate(TicketBase):
    """Schéma d'entrée pour editer un ticket."""
    pass
