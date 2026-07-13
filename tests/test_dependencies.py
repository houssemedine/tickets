from unittest.mock import Mock, patch

import pytest

from app.dependencies import get_db


def test_get_db_closes_session():
    session = Mock()

    with patch("app.dependencies.SessionLocal", return_value=session):
        dependency = get_db()
        assert next(dependency) is session

        with pytest.raises(StopIteration):
            next(dependency)

    session.close.assert_called_once_with()
