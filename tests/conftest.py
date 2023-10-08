import pytest
import responses
from requests import Session

from ynab_commands.config import TestConfig
from ynab_commands.budget_api import BudgetApi


@pytest.fixture()
def requests_mock():
    with responses.RequestsMock() as requestsMock:
        yield requestsMock


@pytest.fixture()
def budget_api() -> BudgetApi:
    return BudgetApi(token=TestConfig.bearer_id, session=Session())
