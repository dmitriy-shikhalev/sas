import logging
from typing import Iterable

from peewee import fn

from sas.db import db
from sas.models import Pool, PoolWord, User, UserWord, Word

logger = logging.getLogger(__name__)


class UserService:
    """Service for users."""

    @staticmethod
    def add(user: User):
        """Add new user."""
        user.save()

        words = Word.select()
        UserWord.bulk_create([UserWord(user=user, word=word, score=0) for word in words])

    @staticmethod
    def get(username: str) -> User | None:
        """Return user by username."""
        return User.get_or_none(username=username)


class PoolService:
    """Service for pools."""

    def get_or_create(self, user: User) -> Pool:
        """Get old or create new pool for user."""
        pool = self.get(user)
        if pool is None:
            pool = self.create(user)
        return pool

    @staticmethod
    def get(user: User) -> Pool:
        """Return new or current pool object."""
        pool = Pool.select().where(Pool.finished == False).get_or_none()  # noqa: E712
        return pool

    @staticmethod
    def create(user: User):
        """Create new pool."""
        pool = Pool.create(user=user)

        word_service = WordService()
        word_list = word_service.get_next_word_list(user, count=user.pool_size)
        for word in word_list:
            PoolWord.create(pool=pool, word=word, score=0)

        return pool


class WordService:
    """Service for words."""

    @staticmethod
    def add(word: Word):
        """Add new word to DB."""
        logger.info("Add word %s", word)
        word.save()

        users = User.select()
        UserWord.bulk_create([UserWord(user=user, word=word, score=0) for user in users])

    def add_many(self, words: Iterable[Word]):
        """Add many words."""
        logger.info("Add many")
        with db.atomic():
            for word in words:
                self.add(word)

    @staticmethod
    def get_next_word_list(user: User, count: int):
        """Get random count words with lowest score for this user."""
        min_score = UserWord.select(fn.MIN(UserWord.score)).where(UserWord.user == user).scalar()
        words = (
            Word.select()
            .join(UserWord)
            .where(
                UserWord.word == Word.english,
                UserWord.score == min_score,
            )
            .limit(count)
        )
        return words
