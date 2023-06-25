import json
from typing import Any

import requests
import requests_cache

from ynab_commands.models import (
    BudgetSummaryResponse,
    TransactionsResponse,
    SaveTransactionWrapper,
    TransactionDetail,
)


def parse_payload(**kwargs):
    data = {}
    data.update(kwargs)
    return data


def get(
    session: requests.Session,
    url: str,
    token: str | None = None,
    params: dict[str, Any] | None = None,
):
    response = session.get(
        url=url, params=params, headers={"Authorization": f"Bearer {token}"}
    )

    if response.status_code == 200:
        return response.json()

    response.raise_for_status()
    return response.ok


def put(
    data: Any,
    session: requests.Session,
    url: str,
    token: str | None = None,
):
    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }
    response = session.put(url=url, headers=headers, data=data)
    if response.status_code == 200:
        return response.json()

    response.raise_for_status()
    return response.ok


def parse_transaction(updated_transaction):
    payload = {}
    payload["transaction"] = updated_transaction.dict()
    return json.dumps(payload)


class BudgetApi:
    _base_url: str = "https://api.youneedabudget.com/v1"

    def __init__(self, token: str, session: requests.Session | None = None):
        self._token = token
        self._session = session or requests_cache.CachedSession("ynab_cache")

    def get_budgets(self, **kwargs):
        url = f"{self._base_url}/budgets"
        payload = parse_payload(**kwargs)
        response_json = get(self._session, url, self._token, params=payload)

        return BudgetSummaryResponse(**response_json["data"])

    def get_transactions(self, budget_id: str, **kwargs):
        """Returns budget transactions

        param budget_id:
            The id of the budget.
            “last-used” can be used to specify the last used budget and
            “default” can be used if default budget selection is enabled
            (see: https://api.youneedabudget.com/#oauth-default-budget).
        param since_date:
            If specified, only transactions on or after this date will be included.
            The date should be ISO formatted (e.g. 2016-12-30).
        param type:
            If specified, only transactions of the specified type will be included.
            “uncategorized” and “unapproved” are currently supported.
        param last_knowledge_of_server:
            The starting server knowledge.
            If provided, only entities that have changed since last_knowledge_of_server will be included.
        return: TransactionsResponse
        """
        url = f"{self._base_url}/budgets/{budget_id}/transactions"
        payload = parse_payload(**kwargs)

        response_json = get(session=self._session, url=url, token=self._token, params=payload)

        return TransactionsResponse(**response_json["data"])

    def update_transaction(
        self,
        budget_id: str,
        transaction_id: str,
        updated_transaction: SaveTransactionWrapper,
    ):
        url = f"{self._base_url}/budgets/{budget_id}/transactions/{transaction_id}"
        data = parse_transaction(updated_transaction)
        response_json = put(
            session=self._session, url=url, token=self._token, data=data
        )

        return TransactionDetail(**response_json["data"]["transaction"])
