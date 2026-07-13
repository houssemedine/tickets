import pytest
from pydantic import ValidationError

from app.schemas.ticket import TicketCreate


def test_ticket_create_accepts_valid_payload():
    ticket = TicketCreate(title="API en erreur", description="Erreur HTTP 500")

    assert ticket.title == "API en erreur"
    assert ticket.description == "Erreur HTTP 500"


@pytest.mark.parametrize(
    "payload",
    [
        {"title": "", "description": "Description valide"},
        {"title": "Titre valide", "description": ""},
        {"title": "x" * 201, "description": "Description valide"},
    ],
)
def test_ticket_create_rejects_invalid_payload(payload):
    with pytest.raises(ValidationError):
        TicketCreate(**payload)
