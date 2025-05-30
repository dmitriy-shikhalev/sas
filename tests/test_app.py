from unittest.mock import Mock, patch

import pytest

from sas import app


def test_init():
    """Test App.__init__."""
    settings = Mock()
    app_ = app.App(settings)
    assert app_.settings is settings


@pytest.mark.parametrize(
    "is_db_exists",
    [
        False,
        True,
    ],
)
@patch("sas.app.WordService")
@patch("sas.app.CsvSource")
@patch("sas.app.db.initialize")
def test_initialize(db_initialize_mock, csv_source_mock, word_service_mock, is_db_exists):
    """Test App.initialize."""
    db_initialize_mock.return_value = is_db_exists
    settings = Mock()
    app_ = app.App(settings)
    app_.initialize()

    db_initialize_mock.assert_called_once_with(settings)
    if is_db_exists:
        csv_source_mock.assert_not_called()
        word_service_mock.assert_not_called()
    else:
        csv_source_mock.assert_called_once_with(filename=settings.csv_words_filename)
        csv_source_mock.return_value.read_words.assert_called_once_with()
        word_service_mock.assert_called_once_with()
        word_service_mock.return_value.add_many.assert_called_once_with(
            csv_source_mock.return_value.read_words.return_value
        )
