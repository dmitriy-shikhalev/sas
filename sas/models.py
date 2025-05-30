import datetime

from peewee import (
    BooleanField,
    CharField,
    DateTimeField,
    ForeignKeyField,
    IntegerField,
    Model,
    SqliteDatabase,
)

db = SqliteDatabase(None)


class User(Model):
    """Model for user."""

    username = CharField(primary_key=True)
    score = IntegerField(null=False, default=0)

    @property
    def pool_size(self) -> int:
        """Calculate pool size for user."""
        size = self.score // 10  # type: ignore
        if size == 0:
            return 10
        return size * 10


class Word(Model):
    """Model for word."""

    english = CharField(primary_key=True)
    russian = CharField()


class Pool(Model):
    """Model for pool."""

    user = ForeignKeyField(User, backref="pool_set")
    start_dt = DateTimeField(default=datetime.datetime.now)
    end_dt = DateTimeField(null=True)
    finished = BooleanField(default=False)


class UserWord(Model):
    """Model for relation User-Model."""

    user = ForeignKeyField(User, backref="user_word_set")
    word = ForeignKeyField(Word, backref="user_word_set")
    score = IntegerField(null=False, default=0)


class PoolWord(Model):
    """Model for pool of words."""

    pool = ForeignKeyField(Pool, backref="pool_word_set")
    word = ForeignKeyField(Word, backref="pool_word_set")
    score = IntegerField(null=False, default=0)


class Attempt(Model):
    """Model for one attempt."""

    user = ForeignKeyField(User, backref="attempt_set")
    word = ForeignKeyField(Word, backref="attempt_set")
    dt = DateTimeField(default=datetime.datetime.now)
    success = BooleanField(null=False)
