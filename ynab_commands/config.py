from pathlib import Path

from pydantic.env_settings import BaseSettings
from pydantic.types import SecretStr

ENV_DIR = Path(__file__).parents[1]


class Config(BaseSettings):
    bearer_id: SecretStr = SecretStr("123")
    budget_id: str = "123"
    splitwise_id: str = "123"
