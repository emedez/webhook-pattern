from typing import Optional

from devtools import debug
from pydantic import BaseSettings


class Settings(BaseSettings):
    """
    Set environment variables to override the values here
    """

    API_ROOT_PATH: str = "/Prod"
    QUEUE_URL: Optional[str]
    DYNAMO_TABLE: Optional[str]

    class Config:
        case_sensitive = True
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
debug(settings)
