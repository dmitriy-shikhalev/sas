from unittest.mock import Mock, patch

import pytest

from sas.models import Pool, User, Word
from sas.services import PoolService, UserService, WordService


class TestUserService:
    """Tests for class UserService."""

    @patch("sas.services.UserWord")
    @patch("sas.services.Word.select", return_value=[Mock(), Mock()])
    def test_add(self, select_mock, user_word_mock):
        """Test .add."""
        user = Mock()

        user_service = UserService()
        user_service.add(user)

        user.save.assert_called_once_with()
        select_mock.assert_called_once_with()
        assert user_word_mock.call_count == 2
        user_word_mock.assert_any_call(user=user, word=select_mock.return_value[0], score=0)
        user_word_mock.assert_any_call(user=user, word=select_mock.return_value[1], score=0)
        user_word_mock.bulk_create.assert_called_once_with([user_word_mock.return_value, user_word_mock.return_value])

    @pytest.mark.parametrize(
        "user",
        [
            None,
            User(username="test user", score=13),
        ],
    )
    @patch("sas.services.User.get_or_none")
    def test_get(self, get_or_none_mock, user):
        """Test .get."""
        get_or_none_mock.return_value = user
        username = Mock()

        user_service = UserService()
        result = user_service.get(username)

        assert result is user
        get_or_none_mock.assert_called_once_with(username=username)


class TestPoolService:
    """Tests for class PoolService."""

    @patch("sas.services.Pool.select")
    def test_get(self, select_mock):
        """Test .get."""
        user = Mock()
        pool_service = PoolService()
        pool = pool_service.get(user)
        assert pool is select_mock.return_value.where.return_value.get_or_none.return_value

        select_mock.assert_called_once_with()
        select_mock.return_value.where.assert_called_once_with(Pool.finished == False)  # noqa: E712
        select_mock.return_value.where.return_value.get_or_none.assert_called_once_with()

    @pytest.mark.parametrize(
        "get_result",
        [
            None,
            Mock(),
        ],
    )
    def test_get_or_create(self, get_result):
        """Test .get_or_create."""
        user = Mock()
        pool_service = PoolService()

        with (
            patch.object(pool_service, "get", Mock(return_value=get_result)) as get_mock,
            patch.object(pool_service, "create") as create_mock,
        ):
            pool = pool_service.get_or_create(user)

            if get_result is None:
                assert pool is create_mock.return_value

                get_mock.assert_called_once_with(user)
                create_mock.assert_called_once_with(user)
            else:
                assert pool is get_mock.return_value

                get_mock.assert_called_once_with(user)
                create_mock.assert_not_called()

    @patch("sas.services.PoolWord.create")
    @patch(
        "sas.services.WordService",
        return_value=Mock(
            get_next_word_list=Mock(
                return_value=[
                    Word(english="test1", russian="тест1"),
                    Word(english="test2", russian="тест2"),
                ]
            )
        ),
    )
    @patch("sas.services.Pool.create")
    def test_create(self, pool_create_mock, word_service_mock, pool_word_create_mock):
        """Test .create."""
        user = Mock()
        pool_service = PoolService()

        pool_service.create(user)

        pool_create_mock.assert_called_once_with(user=user)

        word_service_mock.assert_called_once_with()
        word_service_mock.return_value.get_next_word_list.assert_called_once_with(user, count=user.pool_size)

        assert pool_word_create_mock.call_count == 2
        pool_word_create_mock.assert_any_call(
            pool=pool_create_mock.return_value,
            word=word_service_mock.return_value.get_next_word_list.return_value[0],
            score=0,
        )
        pool_word_create_mock.assert_any_call(
            pool=pool_create_mock.return_value,
            word=word_service_mock.return_value.get_next_word_list.return_value[1],
            score=0,
        )


class TestWordService:
    """Tests for class WordService."""

    @patch("sas.services.UserWord")
    @patch("sas.services.User.select", return_value=[Mock(), Mock()])
    def test_add(self, select_mock, user_word_mock):
        """Test .add."""
        word = Mock()

        word_service = WordService()
        word_service.add(word)

        word.save.assert_called_once_with()
        select_mock.assert_called_once_with()
        assert user_word_mock.call_count == 2
        user_word_mock.assert_any_call(user=select_mock.return_value[0], word=word, score=0)
        user_word_mock.assert_any_call(user=select_mock.return_value[1], word=word, score=0)
        user_word_mock.bulk_create.assert_called_once_with([user_word_mock.return_value, user_word_mock.return_value])

    @patch(
        "sas.services.db.atomic",
        return_value=Mock(
            __enter__=Mock(),
            __exit__=Mock(),
        ),
    )
    def test_add_many(self, atomic_mock):
        """Test .add_many."""
        words = [Mock(), Mock()]
        word_service = WordService()

        with patch.object(word_service, "add") as add_mock:
            word_service.add_many(words)

            atomic_mock.assert_called_once_with()
            atomic_mock.return_value.__enter__.assert_called_once_with()

            assert add_mock.call_count == 2
            add_mock.assert_any_call(words[0])
            add_mock.assert_any_call(words[1])

    @patch("sas.services.fn.MIN")
    @patch("sas.services.Word")
    @patch("sas.services.UserWord")
    def test_get_next_word_list(self, user_word_mock, word_mock, min_mock):
        """Test .get_next_word_list."""
        user = Mock()
        count = Mock()
        word_service = WordService()
        result = word_service.get_next_word_list(user, count=count)

        assert result == word_mock.select.return_value.join.return_value.where.return_value.limit.return_value

        min_mock.assert_called_once_with(user_word_mock.score)
        user_word_mock.select.assert_called_once_with(min_mock.return_value)
        user_word_mock.select.return_value.where.assert_called_once_with(user_word_mock.user == user)
        user_word_mock.select.return_value.where.return_value.scalar.assert_called_once_with()

        word_mock.select.assert_called_once_with()
        word_mock.select.return_value.join.assert_called_once_with(user_word_mock)
        word_mock.select.return_value.join.return_value.where.assert_called_once_with(
            user_word_mock.word == word_mock.english,
            user_word_mock.score == user_word_mock.select.return_value.where.return_value.scalar.return_value,
        )
        word_mock.select.return_value.join.return_value.where.return_value.limit.assert_called_once_with(count)
