from unittest.mock import Mock, patch

import pytest

from sas import db
from sas.models import Attempt, Pool, PoolWord, User, UserWord, Word


@patch("sas.db.Word")
@patch("sas.db.UserWord")
@patch("sas.db.User")
@patch("sas.db.PoolWord")
@patch("sas.db.Pool")
@patch("sas.db.Attempt")
def test_create_tables(attempt_mock, pool_mock, pool_word_mock, user_mock, user_word_mock, word_mock):
    """Test function create_tables."""
    database = Mock()

    db._create_tables(database)

    database.create_tables.assert_called_once_with(
        [
            user_mock,
            word_mock,
            pool_mock,
            user_word_mock,
            pool_word_mock,
            attempt_mock,
        ]
    )


@patch("sas.db.os.path.exists", return_value=False)
def test_is_db_exists_false(exists_mock):
    """Test _is_db_exists with False result."""
    settings = Mock()
    result = db._is_db_exist(settings)
    assert result is False
    exists_mock.assert_called_once_with(settings.db_filename)


@patch("sas.db.os.path.exists", return_value=True)
def test_is_db_exists_true(exists_mock):
    """Test _is_db_exists with True result."""
    settings = Mock()
    result = db._is_db_exist(settings)
    assert result is True
    exists_mock.assert_called_once_with(settings.db_filename)


def test_db_initialization():
    """Trest _db_initialization."""
    settings = Mock()
    db_mock = Mock()
    db._db_initialization(settings, db_mock)

    db_mock.init.assert_called_once_with(settings.db_filename, pragmas={"journal_mode": "wal"})
    db_mock.bind.assert_called_once_with([User, Word, PoolWord, UserWord, Pool, Attempt])
    db_mock.connect.assert_called_once_with()


@pytest.mark.parametrize(
    "is_db_exist",
    [
        False,
        True,
    ],
)
@patch("sas.db.db")
@patch("sas.db._is_db_exist")
@patch("sas.db._db_initialization")
@patch("sas.db._create_tables")
def test_initialize(_create_tables_mock, _db_initialization_mock, _is_db_exist_mock, db_mock, is_db_exist):
    """Test initialize."""
    _is_db_exist_mock.return_value = is_db_exist
    settings = Mock()

    db.initialize(settings)

    _is_db_exist_mock.assert_called_once_with(settings)
    _db_initialization_mock.assert_called_once_with(settings, db_mock)

    if is_db_exist:
        _create_tables_mock.assert_not_called()
    else:
        _create_tables_mock.assert_called_once_with(db_mock)
