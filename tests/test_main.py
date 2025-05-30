from unittest.mock import patch

from sas.main import main


@patch("sas.main.App")
@patch("sas.main.Settings")
def test_main(settings_mock, app_mock):
    """Test blank function."""
    main()

    settings_mock.assert_called_once_with()
    app_mock.assert_called_once_with(settings_mock.return_value)
    app_mock.return_value.serve.assert_called_once_with()
