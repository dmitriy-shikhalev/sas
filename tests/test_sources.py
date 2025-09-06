import csv
from unittest.mock import Mock, patch

from sas.sources import CsvSource


def test_csv_source_init():
    """Test CsvSource.__init__."""
    filename = Mock()
    csv_source = CsvSource(filename)
    assert csv_source.filename is filename


@patch("sas.sources.Word")
@patch("sas.sources.csv.DictReader", return_value=[{"a": "b", "c": "d"}])
@patch("sas.sources.open")
def test_read_words(open_mock, dict_reader_mock, word_mock):
    """Test CsvSource.read_words."""
    filename = Mock()
    csv_source = CsvSource(filename)

    result = csv_source.read_words()

    assert list(result) == [word_mock.return_value]

    open_mock.assert_called_once_with(filename, "r")
    open_mock.return_value.__enter__.assert_called_once_with()
    dict_reader_mock.assert_called_once_with(open_mock.return_value.__enter__.return_value, dialect=csv.unix_dialect)
    word_mock.assert_called_once_with(a="b", c="d")
