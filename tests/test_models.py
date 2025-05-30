from sas import models


def test_pool_size_low():
    """Test User.pool_size with score lower than 10."""
    user = models.User(username="test", score=9)
    assert user.pool_size == 10


def test_pool_size_high():
    """Test User.pool_size with score more than 10."""
    user = models.User(username="test", score=157)
    assert user.pool_size == 150
