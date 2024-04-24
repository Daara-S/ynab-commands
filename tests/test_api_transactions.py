import responses

from ynab_commands.models import BudgetSummaryResponse, TransactionsResponse

REST_API_BASE_URL = "https://api.youneedabudget.com/v1/"


def test_get_transactions(config, ynab_api, requests_mock, transaction_list_json):
    budget_id = "1234"
    requests_mock.add(
        responses.GET,
        f"{REST_API_BASE_URL}budgets/{budget_id}/transactions",
        json=transaction_list_json,
        status=200,
    )
    transactions = ynab_api.get_transactions(budget_id)

    assert len(requests_mock.calls) == 1
    assert (
        requests_mock.calls[0].request.headers["Authorization"]
        == f"Bearer {config.bearer_id.get_secret_value()}"
    )
    assert transactions == TransactionsResponse(**transaction_list_json["data"])


def test_get_budgets(config, ynab_api, requests_mock, budget_list_json):
    requests_mock.add(
        responses.GET,
        f"{REST_API_BASE_URL}budgets",
        json=budget_list_json,
        status=200,
    )
    budgets = ynab_api.get_budgets()
    assert len(requests_mock.calls) == 1
    assert (
        requests_mock.calls[0].request.headers["Authorization"]
        == f"Bearer {config.bearer_id.get_secret_value()}"
    )
    assert budgets == BudgetSummaryResponse(**budget_list_json["data"])
