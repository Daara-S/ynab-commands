import responses

from tests.data.defaults import REST_API_BASE_URL, DEFAULT_TOKEN


def test_get_transactions(budget_api, requests_mock, transactions_response_json, transactions_response):
    budget_id = "1234"
    expected_endpoint = f"{REST_API_BASE_URL}/budgets/{budget_id}/transactions"

    requests_mock.add(
        responses.GET,
        expected_endpoint,
        json=transactions_response_json,
        status=200
    )

    transactions = budget_api.get_transactions(budget_id)

    assert len(requests_mock.calls) == 1
    assert requests_mock.calls[0].request.headers["Authorization"] == f"Bearer {DEFAULT_TOKEN}"
    assert transactions == transactions_response
