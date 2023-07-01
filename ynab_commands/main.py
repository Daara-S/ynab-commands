import os
from datetime import datetime, timedelta

import typer
from requests import Session

from config import configs
from ynab_commands.budget_api import BudgetApi

config = configs[os.getenv('ENV', 'Test')]


def get_date(weeks: int = 4) -> str:
    backdate = datetime.today() - timedelta(weeks=weeks)
    return str(backdate.date())


def main():
    api = BudgetApi(token=config.bearer_id, session=Session())

    completed_transactions = 0
    response = api.get_transactions(
        budget_id=config.budget_id, since_date=get_date(weeks=4)
    )

    for transaction in response.transactions:
        if transaction.flag_color == "purple" and transaction.subtransactions == []:
            updated_transaction = transaction.split(
                splitwise_id=config.splitwise_id
            )
            api.update_transaction(
                budget_id=config.budget_id,
                transaction_id=transaction.id,
                updated_transaction=updated_transaction,
            )
            completed_transactions += 1
    print(f"Processed {completed_transactions} transactions")


if __name__ == "__main__":
    typer.run(main)
