import responses

from tests.data.defaults import REST_API_BASE_URL, DEFAULT_TOKEN

budget_id = "1234"


def test_get_transactions(budget_api, requests_mock, transactions_response_json, transactions_response):
    requests_mock.add(
        responses.GET,
        f"{REST_API_BASE_URL}budgets/{budget_id}/transactions",
        json=transactions_response_json,
        status=200
    )
    transactions = budget_api.get_transactions(budget_id)

    assert len(requests_mock.calls) == 1
    assert requests_mock.calls[0].request.headers["Authorization"] == f"Bearer {DEFAULT_TOKEN}"
    assert transactions == transactions_response


def test_get_budgets(budget_api, requests_mock, budget_summary_json, budget_summary):
    requests_mock.add(
        responses.GET,
        f"{REST_API_BASE_URL}budgets",
        json=budget_summary_json,
        status=200
    )
    budgets = budget_api.get_budgets()
    assert len(requests_mock.calls) == 1
    assert requests_mock.calls[0].request.headers["Authorization"] == f"Bearer {DEFAULT_TOKEN}"
    assert budgets == budget_summary
