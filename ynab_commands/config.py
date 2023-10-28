from pathlib import Path

from pydantic.env_settings import BaseSettings
from pydantic.types import SecretStr

ENV_DIR = Path(__file__).parents[1]


class Config(BaseSettings):
    bearer_id: SecretStr
    budget_id: str
    ynab_sw_account_id: str
    splitwise_id: str
    splitwise_consumer_key: SecretStr
    splitwise_consumer_secret: SecretStr
    splitwise_api_key: SecretStr



TestConfig = Config(_env_file=ENV_DIR / 'test.env')
ProdConfig = Config(_env_file=ENV_DIR / 'prod.env')

configs = {
    "Test": TestConfig,
    "Prod": ProdConfig
}
