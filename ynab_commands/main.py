import argparse
import logging
import sys

from requests import Session

from ynab_commands.config import CONFIG
from ynab_commands.splitwise_api import SplitwiseAPI
from ynab_commands.utilities import get_date
from ynab_commands.ynab_api import YNABApi

log = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.DEBUG, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)


def run():
    parser = argparse.ArgumentParser(
        prog="YNAB Commands", description="Split YNAB transactions"
    )
    parser.parse_args()

    ynab_api = YNABApi(token=CONFIG.bearer_id, session=Session())
    splitwise_api = SplitwiseAPI(  # noqa: F841
        consumer_key=CONFIG.splitwise_consumer_key,
        consumer_secret=CONFIG.splitwise_consumer_secret,
        api_key=CONFIG.splitwise_api_key,
    )
    response = ynab_api.get_transactions(
        budget_id=CONFIG.budget_id, since_date=get_date(weeks=4)
    )

    filtered_response = response.get_transactions_to_split()
    log.debug(f"Found {len(filtered_response.transactions)} transaction to split.")

    if len(filtered_response.transactions) == 0:
        print("No transactions found to split. Exiting.")
        sys.exit()

    filtered_response.print_transaction_info()

    continue_split: bool = (
        input("Continue with transaction split? [y/N]: ").lower().strip() == "y"
    )
    if not continue_split:
        print("Exiting.")
        sys.exit()

    ynab_api.split_and_update_transaction(
        filtered_response=filtered_response,
    )
    # splitwise_api.update_splitwise(total=filtered_response.transaction_total)


if __name__ == "__main__":
    run()
