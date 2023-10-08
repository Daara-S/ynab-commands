import os
from datetime import datetime, timedelta

import typer
from requests import Session

from config import configs
from models import TransactionDetail
from ynab_commands.budget_api import BudgetApi

config = configs[os.getenv('ENV', 'Prod')]


def get_date(weeks: int = 4) -> str:
    backdate = datetime.today() - timedelta(weeks=weeks)
    return str(backdate.date())


def filter_transactions(transactions: list[TransactionDetail]) -> list[TransactionDetail]:
    filtered_list = []
    for transaction in transactions:
        if transaction.flag_color == "purple" and transaction.subtransactions == []:
            filtered_list.append(transaction)
    return filtered_list


def print_transaction_info(filtered_transactions: list[TransactionDetail]) -> None:
    account_dict = {}
    for transaction in filtered_transactions:
        if transaction.account_name not in account_dict:
            account_dict[transaction.account_name] = 1
        else:
            account_dict[transaction.account_name] += 1
    for account, total in account_dict.items():
        print(f"{account}: {total}")


def main():
    api = BudgetApi(token=config.bearer_id, session=Session())

    response = api.get_transactions(
        budget_id=config.budget_id, since_date=get_date(weeks=4)
    )
    filtered_transactions = filter_transactions(response.transactions)
    total_transactions = len(filtered_transactions)

    if total_transactions == 0:
        print("No transactions found to split. Exiting.")
        raise typer.Exit()

    print_transaction_info(filtered_transactions)

    should_split: bool = typer.confirm("Continue with transaction split?")
    if not should_split:
        raise typer.Abort()

    for transaction in filtered_transactions:
        updated_transaction = transaction.split(
            splitwise_id=config.splitwise_id
        )
        api.update_transaction(
            budget_id=config.budget_id,
            transaction_id=transaction.id,
            updated_transaction=updated_transaction,
        )
    print(f"Processed {total_transactions} transactions")


if __name__ == "__main__":
    typer.run(main)
