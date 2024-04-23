import argparse
import sys
from collections import Counter
from datetime import datetime, timedelta
from pathlib import Path

from requests import Session

from ynab_commands.config import Config
from ynab_commands.models import (
    SaveSubTransaction,
    SaveTransactionWrapper,
    TransactionDetail,
    TransactionsResponse,
)
from ynab_commands.ynab_api import YNABApi

CONFIG = Config(_env_file=Path(__file__).parents[1] / "prod.env")  # type: ignore[call-arg]


def get_date(weeks: int) -> str:
    backdate = datetime.today() - timedelta(weeks=weeks)
    return str(backdate.date())


def milliunits_to_gbp(amount: int) -> float:
    """Convert milliunits to pounds."""
    return abs(amount / 1000.0)


def gbp_to_milliunits(amount: float | str) -> int:
    """Convert pounds to milliunits."""
    value = float(amount) * 1000
    return int(value)


def print_transaction_info(filtered_response: TransactionsResponse) -> None:
    account_names = [transaction.account_name for transaction in filtered_response]
    account_counts = Counter(account_names)

    for account, count in account_counts.items():
        print(f"{account}: {count} transactions")


def split_transaction(transaction: TransactionDetail) -> SaveTransactionWrapper:
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
    return SaveTransactionWrapper(
        payee_id=None,
        payee_name=None,
        memo=None,
        import_id=None,
        amount=transaction.amount,
        account_id=transaction.account_id,
        date=transaction.date,
        approved=True,
        flag_color=None,
        category_id=None,
        cleared="cleared",
        subtransactions=[personal_subtransaction, splitwise_subtransaction],
    )


def split_and_update_transaction(
    filtered_response: TransactionsResponse,
) -> None:
    for transaction in filtered_response:
        updated_transaction = split_transaction(transaction)
        api.update_transaction(
            budget_id=CONFIG.budget_id,
            transaction_id=transaction.id,
            updated_transaction=updated_transaction,
        )

    print(f"Processed {len(filtered_response)} transactions")
    print(
        f"Add £{milliunits_to_gbp(filtered_response.transaction_total):.2f} to splitwise"  # noqa: E501
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="YNAB Commands", description="Split YNAB transactions"
    )
    parser.parse_args()

    api = YNABApi(token=CONFIG.bearer_id, session=Session())
    response = api.get_transactions(
        budget_id=CONFIG.budget_id, since_date=get_date(weeks=4)
    )

    filtered_response = response.get_transactions_to_split()

    if len(filtered_response.transactions) == 0:
        print("No transactions found to split. Exiting.")
        sys.exit()

    print_transaction_info(filtered_response)

    continue_split: bool = (
        input("Continue with transaction split? [y/N]: ").lower().strip() == "y"
    )
    if not continue_split:
        print("Exiting.")
        sys.exit()

    split_and_update_transaction(filtered_response)
