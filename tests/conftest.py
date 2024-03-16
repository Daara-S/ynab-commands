import pytest
import responses
from requests import Session

from ynab_commands.config import Config
from ynab_commands.ynab_api import YNABApi


@pytest.fixture()
def requests_mock():
    with responses.RequestsMock() as requestsMock:
        yield requestsMock


@pytest.fixture
def config():
    return Config()


@pytest.fixture()
def ynab_api(config) -> YNABApi:
    return YNABApi(token=config.bearer_id, session=Session())
