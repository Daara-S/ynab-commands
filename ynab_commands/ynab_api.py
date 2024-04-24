import json
from typing import Any

import requests
import requests_cache
from pydantic.types import SecretStr

from ynab_commands.models import (
    Account,
    BudgetSummaryResponse,
    SaveTransactionWrapper,
    TransactionDetail,
    TransactionsResponse,
)


def parse_payload(**kwargs: Any) -> dict[str, Any]:
    data = {}
    data.update(kwargs)
    return data


def get(
    session: requests.Session,
    url: str,
    token: SecretStr,
    params: dict[str, Any],
) -> Any:
    response = session.get(
        url=url,
        params=params,
        headers={"Authorization": f"Bearer {token.get_secret_value()}"},
    )
    response.raise_for_status()

    if response.status_code != 200:
        raise requests.RequestException

    return response.json()


def put(
    data: Any,
    session: requests.Session,
    url: str,
    token: SecretStr,
) -> Any:
    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {token.get_secret_value()}",
        "Content-Type": "application/json",
    }
    response = session.put(url=url, headers=headers, data=data)
    response.raise_for_status()
    if response.status_code != 200:
        raise requests.RequestException

    return response.json()


def parse_transaction(updated_transaction: SaveTransactionWrapper) -> str:
    payload = {"transaction": updated_transaction.dict()}
    return json.dumps(payload)


class YNABApi:
    _base_url: str = "https://api.youneedabudget.com/v1"
    _token: SecretStr
    _session: requests.Session

    def __init__(self, token: SecretStr, session: requests.Session | None = None):
        self._token = token
        self._session = session or requests_cache.CachedSession("ynab_cache")

    def get_budgets(self, **kwargs: Any) -> BudgetSummaryResponse:
        url = f"{self._base_url}/budgets"
        payload = parse_payload(**kwargs)
        response_json = get(self._session, url, self._token, params=payload)

        return BudgetSummaryResponse(**response_json["data"])

    def get_account(self, budget_id: str, account_id: str, **kwargs: Any) -> Account:
        url = f"{self._base_url}/budgets/{budget_id}/accounts/{account_id}"
        payload = parse_payload(**kwargs)
        response_json = get(self._session, url, self._token, params=payload)

        return Account(**response_json["data"]["account"])

    def get_transactions(self, budget_id: str, **kwargs: Any) -> TransactionsResponse:
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
            If provided, only entities that have changed since last_knowledge_of_server
            will be included.
        return: TransactionsResponse
        """
        url = f"{self._base_url}/budgets/{budget_id}/transactions"
        payload = parse_payload(**kwargs)

        response_json = get(
            session=self._session, url=url, token=self._token, params=payload
        )

        return TransactionsResponse(**response_json["data"])

    def update_transaction(
        self,
        budget_id: str,
        transaction_id: str,
        updated_transaction: SaveTransactionWrapper,
    ) -> TransactionDetail:
        url = f"{self._base_url}/budgets/{budget_id}/transactions/{transaction_id}"
        data = parse_transaction(updated_transaction)
        response_json = put(
            session=self._session, url=url, token=self._token, data=data
        )

        return TransactionDetail(**response_json["data"]["transaction"])
