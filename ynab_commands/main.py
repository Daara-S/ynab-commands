import argparse
import sys
from collections import Counter
from datetime import datetime, timedelta

from requests import Session

from ynab_commands.config import Config
from ynab_commands.models import TransactionDetail
from ynab_commands.ynab_api import YNABApi

CONFIG = Config(_env_file=ENV_DIR / "prod.env")  # type: ignore[call-arg]  # noqa:F821


def get_date(weeks: int) -> str:
    backdate = datetime.today() - timedelta(weeks=weeks)
    return str(backdate.date())


def to_gbp(amount: int) -> float:
    return abs(amount / 1000.0)


def milliunits(amount: float | str) -> int:
    value = float(amount) * 1000
    return int(value)


def filter_transactions(
    transactions: list[TransactionDetail],
) -> list[TransactionDetail]:
    """todo move this to a property of TransactionDetail."""
    return [
        transaction
        for transaction in transactions
        if transaction.flag_color == "purple" and transaction.subtransactions == []
    ]


def print_transaction_info(filtered_transactions: list[TransactionDetail]) -> None:
    account_names = [transaction.account_name for transaction in filtered_transactions]
    account_counts = Counter(account_names)

    for account, count in account_counts.items():
        print(f"{account}: {count} transactions")


def split_transactions(filtered_transactions: list[TransactionDetail]) -> None:
    transaction_total = sum(transaction.amount for transaction in filtered_transactions)

    for transaction in filtered_transactions:
        updated_transaction = transaction.split(splitwise_id=CONFIG.splitwise_id)
        api.update_transaction(
            budget_id=CONFIG.budget_id,
            transaction_id=transaction.id,
            updated_transaction=updated_transaction,
        )

    print(f"Processed {len(filtered_transactions)} transactions")
    print(f"Add £{to_gbp(transaction_total):.2f} to splitwise")


if __name__ == "__main__":
    api = YNABApi(token=CONFIG.bearer_id, session=Session())
    parser = argparse.ArgumentParser(
        prog="YNAB Commands", description="Split YNAB transactions"
    )

    parser.parse_args()

    response = api.get_transactions(
        budget_id=CONFIG.budget_id, since_date=get_date(weeks=4)
    )

    filtered_transactions = filter_transactions(response.transactions)

    if len(filtered_transactions) == 0:
        print("No transactions found to split. Exiting.")
        sys.exit()

    print_transaction_info(filtered_transactions)

    continue_split: bool = (
        input("Continue with transaction split? [y/N]: ").lower().strip() == "y"
    )
    if not continue_split:
        print("Exiting.")
        sys.exit()

    split_transactions(filtered_transactions)
