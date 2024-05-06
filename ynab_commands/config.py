import logging
from pathlib import Path

from pydantic.env_settings import BaseSettings
from pydantic.types import SecretStr

log = logging.getLogger(__name__)


class Config(BaseSettings):
    # YNAB
    bearer_id: SecretStr = SecretStr("123")
    budget_id: str = "123"
    splitwise_id: str = "123"

    # Splitwise
    splitwise_consumer_key: SecretStr = SecretStr("123")
    splitwise_consumer_secret: SecretStr = SecretStr("123")
    splitwise_api_key: SecretStr = SecretStr("123")


CONFIG = Config(_env_file=Path(__file__).parents[1] / "prod.env")  # type: ignore[call-arg]
