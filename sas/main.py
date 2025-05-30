import logging

from sas.app import App
from sas.settings import Settings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def main():
    """Start the program."""
    settings = Settings()
    app = App(settings)
    app.initialize()
    app.serve()
