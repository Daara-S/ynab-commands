from tests.data.examples import EXAMPLE_BUDGET_LIST, EXAMPLE_ACCOUNT, EXAMPLE_TRANSACTION_LIST
from ynab_commands.models import (BudgetSummaryResponse, DateFormat, CurrencyFormat, Account, BudgetSummary,
                                  TransactionsResponse, SubTransaction)


def test_budget_summary_response():
    sample_data = dict(EXAMPLE_BUDGET_LIST)
    budget_summary = BudgetSummaryResponse(**sample_data["data"])

    assert budget_summary.budgets[0].id == sample_data["data"]["budgets"][0]["id"]
    assert budget_summary.budgets[0].name == sample_data["data"]["budgets"][0]["name"]
    assert budget_summary.budgets[0].last_modified_on == sample_data["data"]["budgets"][0]["last_modified_on"]
    assert budget_summary.budgets[0].first_month == sample_data["data"]["budgets"][0]["first_month"]
    assert budget_summary.budgets[0].last_month == sample_data["data"]["budgets"][0]["last_month"]
    assert budget_summary.budgets[0].date_format == DateFormat(**sample_data["data"]["budgets"][0]["date_format"])
    assert budget_summary.budgets[0].currency_format == CurrencyFormat(
        **sample_data["data"]["budgets"][0]["currency_format"])
    assert budget_summary.budgets[0].accounts[0] == Account(**sample_data["data"]["budgets"][0]["accounts"][0])
    assert budget_summary.default_budget == BudgetSummary(**sample_data["data"]["default_budget"])


def test_account():
    sample_data = dict(EXAMPLE_ACCOUNT)
    account = Account(**sample_data)

    assert account.id == sample_data["id"]
    assert account.name == sample_data["name"]
    assert account.type == sample_data["type"]
    assert account.on_budget == sample_data["on_budget"]
    assert account.closed == sample_data["closed"]
    assert account.note == sample_data["note"]
    assert account.balance == sample_data["balance"]
    assert account.cleared_balance == sample_data["cleared_balance"]
    assert account.uncleared_balance == sample_data["uncleared_balance"]
    assert account.transfer_payee_id == sample_data["transfer_payee_id"]
    assert account.direct_import_linked == sample_data["direct_import_linked"]
    assert account.direct_import_in_error == sample_data["direct_import_in_error"]
    assert account.deleted == sample_data["deleted"]


def test_transactions_response():
    sample_data = dict(EXAMPLE_TRANSACTION_LIST)
    transaction_response = TransactionsResponse(**sample_data["data"])

    assert transaction_response.transactions[0].id == sample_data["data"]["transactions"][0]["id"]
    assert transaction_response.transactions[0].date == sample_data["data"]["transactions"][0]["date"]
    assert transaction_response.transactions[0].amount == sample_data["data"]["transactions"][0]["amount"]
    assert transaction_response.transactions[0].memo == sample_data["data"]["transactions"][0]["memo"]
    assert transaction_response.transactions[0].cleared == sample_data["data"]["transactions"][0]["cleared"]
    assert transaction_response.transactions[0].approved == sample_data["data"]["transactions"][0]["approved"]
    assert transaction_response.transactions[0].flag_color == sample_data["data"]["transactions"][0]["flag_color"]
    assert transaction_response.transactions[0].account_id == sample_data["data"]["transactions"][0]["account_id"]
    assert transaction_response.transactions[0].payee_id == sample_data["data"]["transactions"][0]["payee_id"]
    assert transaction_response.transactions[0].category_id == sample_data["data"]["transactions"][0]["category_id"]
    assert transaction_response.transactions[0].transfer_account_id == sample_data["data"]["transactions"][0][
        "transfer_account_id"]
    assert transaction_response.transactions[0].transfer_transaction_id == sample_data["data"]["transactions"][0][
        "transfer_transaction_id"]
    assert transaction_response.transactions[0].matched_transaction_id == sample_data["data"]["transactions"][0][
        "matched_transaction_id"]
    assert transaction_response.transactions[0].import_id == sample_data["data"]["transactions"][0]["import_id"]
    assert transaction_response.transactions[0].deleted == sample_data["data"]["transactions"][0]["deleted"]
    assert transaction_response.transactions[0].account_name == sample_data["data"]["transactions"][0]["account_name"]
    assert transaction_response.transactions[0].payee_name == sample_data["data"]["transactions"][0]["payee_name"]
    assert transaction_response.transactions[0].category_name == sample_data["data"]["transactions"][0]["category_name"]
    assert transaction_response.transactions[0].subtransactions[0] == SubTransaction(
        **sample_data["data"]["transactions"][0]["subtransactions"][0])
    assert transaction_response.server_knowledge == sample_data["data"]["server_knowledge"]
