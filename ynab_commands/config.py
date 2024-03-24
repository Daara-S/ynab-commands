from pydantic.env_settings import BaseSettings
from pydantic.types import SecretStr


class Config(BaseSettings):
    bearer_id: SecretStr = SecretStr("123")
    budget_id: str = "123"
    splitwise_id: str = "123"
