from copy import copy, deepcopy

import pytest

from tests.data.examples import (
    EXAMPLE_ACCOUNT,
    EXAMPLE_BUDGET_LIST,
    EXAMPLE_TRANSACTION,
    EXAMPLE_TRANSACTION_LIST,
)
from ynab_commands.main import split_transaction
from ynab_commands.models import (
    Account,
    BudgetSummaryResponse,
    TransactionDetail,
    TransactionsResponse,
)


def test_budget_summary_response():
    sample_data = dict(EXAMPLE_BUDGET_LIST)
    budget_summary = BudgetSummaryResponse(**sample_data["data"])
    assert budget_summary.dict() == sample_data["data"]


def test_account():
    sample_data = dict(EXAMPLE_ACCOUNT)
    account = Account(**sample_data)
    assert account.dict() == sample_data


def test_split_into_subtransaction():
    sample_data = dict(EXAMPLE_TRANSACTION)
    transaction = TransactionDetail(**sample_data["data"]["transaction"])
    updated_transaction = split_transaction(transaction)
    assert updated_transaction.subtransactions[0].amount == pytest.approx(
        transaction.amount / 2
    )
    assert updated_transaction.subtransactions[0].category_id == transaction.category_id


@pytest.fixture
def unsplit_transaction():
    sample_data = deepcopy(EXAMPLE_TRANSACTION)
    sample_data["data"]["transaction"]["subtransactions"] = []
    sample_data["data"]["transaction"]["flag_color"] = "purple"
    return TransactionDetail(**sample_data["data"]["transaction"])


@pytest.fixture
def transaction_dict():
    return dict(EXAMPLE_TRANSACTION).copy()


def test_filter_transactions(unsplit_transaction, transaction_dict):
    transaction = TransactionDetail(**transaction_dict["data"]["transaction"])
    all_transactions = [transaction, unsplit_transaction]

    filtered_transactions = [t for t in all_transactions if t.should_split]
    assert len(filtered_transactions) == 1


@pytest.fixture
def transaction_list_dict():
    return dict(EXAMPLE_TRANSACTION_LIST).copy()


class TestTransactionsResponse:
    def test_transactions_response(self):
        sample_data = dict(EXAMPLE_TRANSACTION_LIST)
        transaction_response = TransactionsResponse(**sample_data["data"])
        assert transaction_response.dict() == sample_data["data"]

    def test_total_transactions(self):
        sample_data = dict(EXAMPLE_TRANSACTION_LIST)
        sample_data["data"]["transactions"].append(
            sample_data["data"]["transactions"][0]
        )
        transaction_response = TransactionsResponse(**sample_data["data"])
        assert len(transaction_response.transactions) == 2

    def test_total_accounts(self):
        sample_data = dict(EXAMPLE_TRANSACTION_LIST)
        sample_data["data"]["transactions"].append(
            EXAMPLE_TRANSACTION["data"]["transaction"]
        )
        sample_data["data"]["transactions"][0]["account_id"] = "account1"
        sample_data["data"]["transactions"][1]["account_id"] = "account2"
        transaction_response = TransactionsResponse(**sample_data["data"])
        assert transaction_response.total_accounts == 2

    def test_parsing_transctions_to_split(self, transaction_list_dict):
        sample_data = transaction_list_dict
        purple_transaction = copy(sample_data["data"]["transactions"][0])
        purple_transaction["flag_color"] = "purple"
        purple_transaction["subtransactions"] = []
        sample_data["data"]["transactions"].append(purple_transaction)
        transaction_response = TransactionsResponse(**sample_data["data"])
        filtered_response = transaction_response.get_transactions_to_split()
        assert len(filtered_response) == 1

    def test_iterating_over_transactions(self, transaction_list_dict):
        sample_data = transaction_list_dict
        purple_transaction = copy(sample_data["data"]["transactions"][0])
        sample_data["data"]["transactions"].append(purple_transaction)
        transaction_response = TransactionsResponse(**sample_data["data"])
        filter_a = [t for t in transaction_response.transactions]
        filter_b = [t for t in transaction_response]
        assert len(filter_a) == len(filter_b)
