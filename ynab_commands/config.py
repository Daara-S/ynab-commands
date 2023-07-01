from pathlib import Path

from pydantic.env_settings import BaseSettings
from pydantic.types import SecretStr

ENV_DIR = Path(__file__).parents[1]


class Config(BaseSettings):
    bearer_id: SecretStr
    budget_id: str
    splitwise_id: str


TestConfig = Config(_env_file=ENV_DIR / 'test.env')
ProdConfig = Config(_env_file=ENV_DIR / 'prod.env')

configs = {
    "Test": TestConfig,
    "Prod": ProdConfig
}
