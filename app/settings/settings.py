import typing
import urllib.parse
from functools import lru_cache

from dotenv import find_dotenv

from pydantic.types import PositiveInt, SecretStr


__all__ = ["Settings", "get_settings",]

from pydantic.v1 import BaseSettings


class _Settings(BaseSettings):
    """Base settings for all settings.

    Use double underscore for nested env variables loaded via python-decouple.

    Examples:
        `.env` file should look like::

            TELEGRAM__TOKEN=...
            TELEGRAM__WEBHOOK_DOMAIN_URL=...

            LOGGER__PATH_TO_LOG=./src/logs
            LOGGER__LEVEL=DEBUG

            API__HOST=127.0.0.1
            API__PORT=9191

    Warnings:
        Variables are loaded using python-decouple's `config` function from `.env` or `.env.dev`.
        Default values are provided in the class definitions if not specified in the environment.

    See Also:
        https://pypi.org/project/python-decouple/
        https://docs.pydantic.dev/latest/usage/pydantic_settings/
    """

    class Config:
        """Configuration of settings."""
        env_file_encoding = "utf-8"
        arbitrary_types_allowed = True
        case_sensitive = True
        env_nested_delimiter = "__"


class Postgresql(_Settings):
    """Postgresql settings."""

    #: str: Postgresql host.
    HOST: str = 'localhost'
    #: PositiveInt: positive int (x > 0) port of postgresql.
    PORT: PositiveInt = 5432
    #: str: Postgresql user.
    USER: str = "POSTGRES__USER"
    #: SecretStr: Postgresql password.
    PASSWORD: str = "POSTGRES__PASSWORD"
    #: str: Postgresql database name.
    DATABASE_NAME: str = "POSTGRES__DATABASE_NAME"
    DSN: typing.Optional[str] = None

    @property
    def db_url(self) -> str:
        """Build DSN for postgresql.

        Returns:
            str: PostgreSQL connection string (DSN).
        """
        return f"postgresql://{self.USER}:{urllib.parse.quote_plus(self.PASSWORD)}@{self.HOST}:{self.PORT}/{self.DATABASE_NAME}"

# class Logging(_Settings):
#     """Logging settings."""
#
#     #: LoggerLevel: Level of logging which outputs to stdout.
#     LEVEL: LoggerLevel = config("LOGGER__LEVEL", default=LoggerLevel.DEBUG, cast=LoggerLevel)
#     #: pathlib.Path: Path for saving logs on local storage.
#     FOLDER_PATH: pathlib.Path = config("LOGGER__FOLDER_PATH", default=pathlib.Path("./src/logs"), cast=pathlib.Path)
#
#     @validator("FOLDER_PATH")
#     def __create_dir_if_not_exist(cls, v: pathlib.Path):
#         """Create directory if it does not exist."""
#         if not v.exists():
#             v.mkdir(exist_ok=True, parents=True)
#         return v




class Settings(_Settings):
    """Server settings.

    Formed from `.env` or `.env.dev` if server running with parameter `dev`.
    """
    POSTGRES: Postgresql = Postgresql()


@lru_cache
def get_settings(env_file: str = ".env") -> Settings:
    """Create settings instance."""
    return Settings(_env_file=find_dotenv(env_file))
