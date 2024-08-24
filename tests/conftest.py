import json
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest
import responses
from requests import Session

from ynab_commands.config import Config
from ynab_commands.splitwise_api import SplitwiseAPI
from ynab_commands.ynab_api import YNABApi

DATA_PATH = Path(__file__).parent / "data"


@pytest.fixture()
def requests_mock():
    with responses.RequestsMock() as requestsMock:
        yield requestsMock


@pytest.fixture
def config():
    return Config()


@pytest.fixture
def splitwise_api(config: Config):
    mock_api = MagicMock()

    with patch("splitwise.Splitwise", return_value=mock_api):
        splitwise_api_instance = SplitwiseAPI(
            consumer_secret=config.splitwise_consumer_key,
            consumer_key=config.splitwise_consumer_key,
            api_key=config.splitwise_api_key,
        )
        yield splitwise_api_instance


@pytest.fixture()
def ynab_api(config) -> YNABApi:
    return YNABApi(token=config.bearer_id, session=Session())


@pytest.fixture
def transaction_list_json():
    with open(Path(DATA_PATH / "transaction_list.json"), "r") as file:
        return json.load(file)


@pytest.fixture
def budget_list_json():
    with open(Path(DATA_PATH / "budget_list.json"), "r") as file:
        return json.load(file)


@pytest.fixture
def account_json():
    with open(Path(DATA_PATH / "account.json"), "r") as file:
        return json.load(file)


@pytest.fixture
def transaction_json():
    with open(Path(DATA_PATH / "transaction.json"), "r") as file:
        return json.load(file)


@pytest.fixture
def unsplit_transaction_json():
    with open(Path(DATA_PATH / "transaction.json"), "r") as file:
        transaction_json = json.load(file)

    transaction_json["data"]["transaction"]["subtransactions"] = []
    transaction_json["data"]["transaction"]["flag_color"] = "purple"
    return transaction_json
