import pytest

from sas.main import function


def test_blank_function():
    """Test blank function."""
    with pytest.raises(ZeroDivisionError):
        function()
