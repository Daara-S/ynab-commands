import pytest
import responses
from requests import Session

from tests.data.defaults import DEFAULT_TOKEN
from ynab_commands.budget_api import BudgetApi


@pytest.fixture()
def requests_mock():
    with responses.RequestsMock() as requestsMock:
        yield requestsMock


@pytest.fixture()
def budget_api() -> BudgetApi:
    return BudgetApi(DEFAULT_TOKEN, session=Session())
