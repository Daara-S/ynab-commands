import pytest
import responses
from requests import Session

from ynab_commands.config import TestConfig
from ynab_commands.ynab_api import YNABApi


@pytest.fixture()
def requests_mock():
    with responses.RequestsMock() as requestsMock:
        yield requestsMock


@pytest.fixture()
def ynab_api() -> YNABApi:
    return YNABApi(token=TestConfig.bearer_id, session=Session())
