from datetime import datetime, timedelta
from pathlib import Path

from dotenv import dotenv_values
from requests import Session

from ynab_commands.budget_api import BudgetApi

ENV_FILE = "test.env"

if __name__ == "__main__":
    config = dotenv_values(Path(__file__).parent.parent / ENV_FILE)
    two_week_backdate = datetime.today() - timedelta(weeks=4)
    # make sure to settle up budgets before running this
    api = BudgetApi(token=config["BEARER_ID"], session=Session())
    completed_transactions = 0
    response = api.get_transactions(
        budget_id=config["BUDGET_ID"], since_date=str(two_week_backdate.date())
    )
    for tran in response.transactions:
        if tran.flag_color == "purple" and tran.subtransactions == []:
            updated_transaction = tran.split_into_subtransaction(
                splitwise_id=config["SPLITWISE_ID"]
            )
            api.update_transaction(
                budget_id=config["BUDGET_ID"],
                transaction_id=tran.id,
                updated_transaction=updated_transaction,
            )
            completed_transactions += 1
    print(f"Processed {completed_transactions} transactions")
