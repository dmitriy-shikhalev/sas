from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Settings for SAS app."""

    default_username: str = "default"
    db_filename: str = "sas_test.sqlite"
    csv_words_filename: str = "words.csv"
