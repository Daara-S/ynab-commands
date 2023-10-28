import argparse
from datetime import datetime, timedelta
from typing import Counter

from requests import Session

from scripts.splitwise_connection import Splitwise, configs, os
from ynab_commands.models import TransactionDetail
from ynab_commands.ynab_api import YNABApi

CONFIG = configs[os.getenv('ENV', 'Prod')]


def get_date(weeks: int) -> str:
    backdate = datetime.today() - timedelta(weeks=weeks)
    return str(backdate.date())

def currency(amount: int) -> float:
    return abs(amount / 1000.0)


class BudgetSync:
    def __init__(self) -> None:
        self.api = YNABApi(token=CONFIG.bearer_id, session=Session())
        self.splitwise_api = Splitwise(
            CONFIG.splitwise_consumer_key.get_secret_value(),
            CONFIG.splitwise_consumer_secret.get_secret_value(),
            api_key=CONFIG.splitwise_api_key.get_secret_value()
        )
        self.parser = argparse.ArgumentParser(prog="YNAB Commands", description="Split YNAB transactions")

    def run(self):
        self.parser.parse_args()

        response = self.api.get_transactions(
            budget_id=CONFIG.budget_id,
            since_date=get_date(weeks=4)
        )

        filtered_transactions = self.filter_transactions(response.transactions)
    
        if len(filtered_transactions) == 0:
            print("No transactions found to split. Exiting.")
            return
    
        self.print_transaction_info(filtered_transactions)
    
        continue_split: bool = input("Continue with transaction split? [y/N]: ").lower().strip() == 'y'
        if not continue_split:
            print("Exiting.")
            return
    
        self.split_transactions(filtered_transactions)
    
    def filter_transactions(self, transactions: list[TransactionDetail]) -> list[TransactionDetail]:
        return [
            transaction for transaction in transactions 
            if transaction.flag_color == "purple" and transaction.subtransactions == []
        ]
    
    def print_transaction_info(self, filtered_transactions: list[TransactionDetail]) -> None:
        account_counts = Counter(transaction.account_name for transaction in filtered_transactions)
        for account, count in account_counts.items():
            print(f"{account}: {count} transactions")

    def split_transactions(self, filtered_transactions: list[TransactionDetail]) -> None:
        transaction_total = sum(transaction.amount for transaction in filtered_transactions)

        for transaction in filtered_transactions:
            updated_transaction = transaction.split(
                splitwise_id=CONFIG.splitwise_id
            )
            self.api.update_transaction(
                budget_id=CONFIG.budget_id,
                transaction_id=transaction.id,
                updated_transaction=updated_transaction,
            )
            self.add_to_splitwise()

        print(f"Processed {len(filtered_transactions)} transactions")
        print(f"Add £{currency(transaction_total):.2f} to splitwise")

    def add_to_splitwise(self):
        # friend = [
        #     friend for friend in self.splitwise_api.getFriends() 
        #     if friend.first_name == "Jasperi"
        # ]
        pass
