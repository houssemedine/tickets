from sqlalchemy.orm import Session

from app.repositories.tickets import TicketRepository
from app.schemas.ticket import TicketCreate, TicketStatus, TicketUpdate


def create_ticket(repo: TicketRepository, title: str = "Premier ticket"):
    return repo.create(TicketCreate(title=title, description=f"Description de {title}"))


def test_create_and_get_ticket(db_session: Session):
    repo = TicketRepository(db_session)

    created = create_ticket(repo)

    assert created.id is not None
    assert created.status == TicketStatus.OPEN
    assert created.created_at is not None
    assert repo.get_by_id(created.id) is created
    assert repo.count_all() == 1


def test_list_all_and_paginate_tickets(db_session: Session):
    repo = TicketRepository(db_session)
    created = [create_ticket(repo, f"Ticket {index}") for index in range(3)]

    assert repo.list_all() == created
    assert repo.list_paginated(limit=1, offset=1) == [created[1]]


def test_update_existing_ticket(db_session: Session):
    repo = TicketRepository(db_session)
    created = create_ticket(repo)

    updated = repo.update_full(
        created.id,
        TicketUpdate(title="Titre modifié", description="Description modifiée"),
    )

    assert updated is created
    assert updated.title == "Titre modifié"
    assert updated.description == "Description modifiée"
    assert updated.status == TicketStatus.OPEN


def test_update_unknown_ticket_returns_none(db_session: Session):
    repo = TicketRepository(db_session)

    assert (
        repo.update_full(
            999,
            TicketUpdate(title="Titre", description="Description"),
        )
        is None
    )


def test_close_ticket(db_session: Session):
    repo = TicketRepository(db_session)
    created = create_ticket(repo)

    closed = repo.close(created.id)

    assert closed is created
    assert closed.status == TicketStatus.CLOSED
    assert repo.close(created.id) == "already_closed"


def test_close_unknown_ticket_returns_none(db_session: Session):
    repo = TicketRepository(db_session)

    assert repo.close(999) is None
