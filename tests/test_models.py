from copy import deepcopy

from ynab_commands.models import (
    Account,
    BudgetSummaryResponse,
    ExpenseData,
    MilliUnits,
    TransactionDetail,
    TransactionsResponse,
)


def test_converting_milliunits_to_gbp():
    amount = MilliUnits(20_500)
    assert isinstance(amount, int)
    assert repr(amount) == "£20.5"


def test_adding_milliunits_returns_milliunits():
    total_as_addition = MilliUnits(200) + MilliUnits(300)
    assert isinstance(total_as_addition, MilliUnits)
    total_as_sum = sum([MilliUnits(200), MilliUnits(300)])
    assert isinstance(total_as_sum, MilliUnits)


def test_create_expense():
    expense = ExpenseData(
        **{
            "description": "test",
            "cost": 10,
            "users": [
                {
                    "id": 1234,
                    "paid_share": 10,
                    "owed_share": 5,
                },
                {
                    "id": 5678,
                    "paid_share": 0,
                    "owed_share": 5,
                },
            ],
        }
    )
    assert expense.cost == 10
    assert expense.users[0].id == 1234


def test_budget_summary_response(budget_list_json):
    budget_summary = BudgetSummaryResponse(**budget_list_json["data"])
    assert budget_summary.dict() == budget_list_json["data"]


def test_account(account_json):
    account = Account(**account_json)
    assert account.dict() == account_json


def test_filter_transactions(unsplit_transaction_json, transaction_json):
    unsplit_transaction = TransactionDetail(
        **unsplit_transaction_json["data"]["transaction"]
    )
    transaction = TransactionDetail(**transaction_json["data"]["transaction"])
    all_transactions = [transaction, unsplit_transaction]

    filtered_transactions = [t for t in all_transactions if t.should_split]
    assert len(filtered_transactions) == 1


class TestTransactionsResponse:
    def test_transactions_response(self, transaction_list_json):
        transaction_response = TransactionsResponse(**transaction_list_json["data"])
        assert transaction_response.dict() == transaction_list_json["data"]

    def test_total_transactions(self, transaction_list_json):
        second_transaction = deepcopy(transaction_list_json["data"]["transactions"][0])
        transaction_list_json["data"]["transactions"].append(second_transaction)
        transaction_response = TransactionsResponse(**transaction_list_json["data"])
        assert len(transaction_response.transactions) == 2

    def test_total_accounts(self, transaction_list_json):
        second_transaction = deepcopy(transaction_list_json["data"]["transactions"][0])
        transaction_list_json["data"]["transactions"].append(second_transaction)

        transaction_list_json["data"]["transactions"][0]["account_id"] = "account1"
        transaction_list_json["data"]["transactions"][1]["account_id"] = "account2"
        transaction_response = TransactionsResponse(**transaction_list_json["data"])
        assert transaction_response.total_accounts == 2

    def test_parsing_transctions_to_split(
        self, transaction_list_json, unsplit_transaction_json
    ):
        transaction_list_json["data"]["transactions"].append(
            unsplit_transaction_json["data"]["transaction"]
        )
        transaction_response = TransactionsResponse(**transaction_list_json["data"])
        filtered_response = transaction_response.get_transactions_to_split()
        assert len(filtered_response) == 1

    def test_iterating_over_transactions(
        self, transaction_list_json, unsplit_transaction_json
    ):
        transaction_list_json["data"]["transactions"].append(
            unsplit_transaction_json["data"]["transaction"]
        )
        transaction_response = TransactionsResponse(**transaction_list_json["data"])
        filter_a = [t for t in transaction_response.transactions]
        filter_b = [t for t in transaction_response]
        assert len(filter_a) == len(filter_b)
