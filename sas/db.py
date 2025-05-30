import logging
import os.path

from peewee import SqliteDatabase

from sas.models import Attempt, Pool, PoolWord, User, UserWord, Word, db
from sas.settings import Settings

logger = logging.getLogger(__name__)


def _create_tables(database: SqliteDatabase):
    """Create all tables."""
    database.create_tables(
        [
            User,
            Word,
            Pool,
            UserWord,
            PoolWord,
            Attempt,
        ]
    )


def _is_db_exist(settings: Settings):
    """Check if db exists."""
    if os.path.exists(settings.db_filename):
        return True
    return False


def _db_initialization(settings: Settings, db: SqliteDatabase):
    """Init db, bind models, create connection."""
    db.init(settings.db_filename, pragmas={"journal_mode": "wal"})  # todo: remove pragmas argument?
    db.bind([User, Word, PoolWord, UserWord, Pool, Attempt])
    db.connect()


def initialize(settings: Settings) -> bool:
    """Initialize with start of program."""
    is_db_exists = _is_db_exist(settings)
    _db_initialization(settings, db)
    if not is_db_exists:
        _create_tables(db)
    return is_db_exists
