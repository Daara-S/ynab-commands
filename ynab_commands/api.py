from typing import Any

import requests
import requests_cache

from ynab_commands.models import BudgetSummaryResponse, TransactionsResponse

BEARER = "h-imXmpN2xiBk92Eq9ASs2epACVhXm8UGAa-Wgsp7yY"
AUTH = ("Authorization", "Bearer %s")


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
    response = session.get(url=url, params=params, headers={"Authorization": f"Bearer {token}"})

    if response.status_code == 200:
        return response.json()

    response.raise_for_status()
    return response.ok


class BudgetApi:
    _base_url: str = "https://api.youneedabudget.com/v1/"

    def __init__(self, token: str, session: requests.Session | None = None):
        self._token = token
        self._session = session or requests_cache.CachedSession("ynab_cache")

    def get_budgets(self, **kwargs):
        url = f"{self._base_url}/budgets"
        payload = parse_payload(**kwargs)
        response_json = get(self._session, url, self._token, params=payload)

        return BudgetSummaryResponse(**response_json['data'])

    def get_transactions(self, budget_id: str, **kwargs):
        """ Returns budget transactions

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

        response_json = get(self._session, url, token=self._token,  params=payload)

        return TransactionsResponse(**response_json['data'])


# todo
# add tests similar to https://github.com/Doist/todoist-api-python/tree/39bd9975cb92184a984d22deb0328b9443b2d48c/tests
# test with converting a single transaction into a split transaction when filtering by flag_color

if __name__ == "__main__":
    api = BudgetApi(token=BEARER)
    x = api.get_budgets(include_accounts=False)
    # response = api.get_transactions(budget_id="92629b87-5720-4845-b802-867240d1f293", since_date="2022-11-15")
    # for tran in response.transactions:
    #     if tran.flag_color is not None:
    #         print('x')
    #     if tran.subtransactions != []:
    #         print('x')
    print('x')
