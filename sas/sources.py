import csv
import logging
from abc import ABC, abstractmethod
from typing import Iterable

from sas.models import Word

logger = logging.getLogger(__name__)


class AbstractSource(ABC):
    """Abstract class for any source."""

    @abstractmethod
    def read_words(self) -> Iterable[Word]:
        """Read words."""
        raise NotImplementedError  # pragma: no cover


class CsvSource(AbstractSource):
    """Realization of CSV source."""

    def __init__(self, filename: str):
        """Init method."""
        self.filename = filename

    def read_words(self) -> Iterable[Word]:
        """Read words."""
        with open(self.filename, "r") as fd:
            reader = csv.DictReader(fd, dialect=csv.unix_dialect)
            for row in reader:
                logger.info("row = %s", row)
                if row:
                    yield Word(**row)
