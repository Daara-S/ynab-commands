from datetime import datetime, timedelta
from pathlib import Path

import typer
from dotenv import dotenv_values
from requests import Session

from ynab_commands.budget_api import BudgetApi

ENV_FILE = "test.env"


def get_date(weeks: int = 4) -> str:
    backdate = datetime.today() - timedelta(weeks=weeks)
    return str(backdate.date())


def main():
    config = dotenv_values(Path(__file__).parent.parent / ENV_FILE)
    api = BudgetApi(token=config["BEARER_ID"], session=Session())

    completed_transactions = 0
    response = api.get_transactions(
        budget_id=config["BUDGET_ID"], since_date=get_date(weeks=4)
    )
    for transaction in response.transactions:
        if transaction.flag_color == "purple" and transaction.subtransactions == []:
            updated_transaction = transaction.split(
                splitwise_id=config["SPLITWISE_ID"]
            )
            api.update_transaction(
                budget_id=config["BUDGET_ID"],
                transaction_id=transaction.id,
                updated_transaction=updated_transaction,
            )
            completed_transactions += 1
    print(f"Processed {completed_transactions} transactions")


if __name__ == "__main__":
    typer.run(main)
