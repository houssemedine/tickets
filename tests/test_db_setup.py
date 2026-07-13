from sqlalchemy import inspect
from app.core.db import engine
from app.models.ticket import Base

def test_tables_are_created() -> None:
    Base.metadata.create_all(bind=engine)

    insp = inspect(engine)
    assert "tickets" in insp.get_table_names()
