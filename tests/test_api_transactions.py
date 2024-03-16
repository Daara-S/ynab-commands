import responses

from tests.data.defaults import REST_API_BASE_URL
from tests.data.examples import EXAMPLE_BUDGET_LIST, EXAMPLE_TRANSACTION_LIST
from ynab_commands.models import BudgetSummaryResponse, TransactionsResponse

budget_id = "1234"


def test_get_transactions(config, ynab_api, requests_mock):
    requests_mock.add(
        responses.GET,
        f"{REST_API_BASE_URL}budgets/{budget_id}/transactions",
        json=EXAMPLE_TRANSACTION_LIST,
        status=200,
    )
    transactions = ynab_api.get_transactions(budget_id)

    assert len(requests_mock.calls) == 1
    assert (
        requests_mock.calls[0].request.headers["Authorization"]
        == f"Bearer {config.bearer_id.get_secret_value()}"
    )
    assert transactions == TransactionsResponse(**EXAMPLE_TRANSACTION_LIST["data"])


def test_get_budgets(config, ynab_api, requests_mock):
    requests_mock.add(
        responses.GET,
        f"{REST_API_BASE_URL}budgets",
        json=EXAMPLE_BUDGET_LIST,
        status=200,
    )
    budgets = ynab_api.get_budgets()
    assert len(requests_mock.calls) == 1
    assert (
        requests_mock.calls[0].request.headers["Authorization"]
        == f"Bearer {config.bearer_id.get_secret_value()}"
    )
    assert budgets == BudgetSummaryResponse(**EXAMPLE_BUDGET_LIST["data"])
