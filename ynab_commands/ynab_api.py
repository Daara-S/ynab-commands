import json
import logging
from typing import Any

import requests
import requests_cache
from pydantic.types import SecretStr

from ynab_commands.config import CONFIG
from ynab_commands.models import (
    Account,
    BudgetSummaryResponse,
    PatchTransactionWrapper,
    SaveSubTransaction,
    SaveTransactionWithIdOrImportId,
    SaveTransactionWrapper,
    TransactionDetail,
    TransactionsResponse,
)

log = logging.getLogger(__name__)


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
    log.debug(f"GET response: {response.status_code}.")
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
    log.debug(f"PUT response: {response.status_code}.")
    response.raise_for_status()
    if response.status_code != 200:
        raise requests.RequestException

    return response.json()


def patch(
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
    response = session.patch(url=url, headers=headers, data=data)
    log.debug(f"PATCH response: {response.status_code}.")
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
        log.debug("Grabbing budget transactions.")

        response_json = get(
            session=self._session, url=url, token=self._token, params=payload
        )

        return TransactionsResponse(**response_json["data"])

    def _update_transactions(
        self,
        budget_id: str,
        transactions: list[SaveTransactionWithIdOrImportId],
    ) -> Any:
        url = f"{self._base_url}/budgets/{budget_id}/transactions"
        transactions_obj = PatchTransactionWrapper(transactions=transactions).dict()
        log.debug("Patching transactions")
        response_json = patch(
            session=self._session,
            url=url,
            token=self._token,
            data=json.dumps(transactions_obj),
        )

        return response_json

    def split_and_update_transaction(
        self,
        filtered_response: TransactionsResponse,
    ) -> None:
        total_in_pounds = repr(filtered_response.transaction_total)
        updated_transactions = [self._split_transaction(t) for t in filtered_response]
        log.debug(
            "%s transactions worth %s about to be updated.",
            len(updated_transactions),
            total_in_pounds,
        )

        self._update_transactions(
            budget_id=CONFIG.budget_id,
            transactions=updated_transactions,
        )

        print(f"Processed {len(filtered_response)} transactions")
        print(f"Add {total_in_pounds} to splitwise")

    def _split_transaction(
        self, transaction: TransactionDetail
    ) -> SaveTransactionWithIdOrImportId:
        split_amount = transaction.amount // 2
        personal_subtransaction = SaveSubTransaction(
            amount=split_amount,
            category_id=transaction.category_id,
            payee_id=transaction.payee_id,
            payee_name=transaction.payee_name,
            memo=transaction.memo,
        )
        splitwise_subtransaction = SaveSubTransaction(
            amount=split_amount,
            category_id=CONFIG.splitwise_id,
            payee_id=transaction.payee_id,
            payee_name=transaction.payee_name,
            memo="Auto-split",
        )
        return SaveTransactionWithIdOrImportId(
            id=transaction.id,
            amount=transaction.amount,
            account_id=transaction.account_id,
            date=transaction.date,
            approved=True,
            cleared="cleared",
            subtransactions=[personal_subtransaction, splitwise_subtransaction],
        )
