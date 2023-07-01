from enum import IntEnum
from typing import Literal

from pydantic import BaseModel

FLAG_COLOR = Literal["red", "orange", "yellow", "green", "blue", "purple"]


class DateFormat(BaseModel):
    format: str


class CurrencyFormat(BaseModel):
    iso_code: str
    example_format: str
    decimal_digits: int
    decimal_separator: str
    symbol_first: bool
    group_separator: str
    currency_symbol: str
    display_symbol: str


class AccountType(IntEnum):
    pass


class Account(BaseModel):
    id: str
    name: str
    type: str  # todo convert to enum
    on_budget: bool
    closed: bool
    note: str | None
    balance: int
    uncleared_balance: int
    cleared_balance: int
    transfer_payee_id: str
    direct_import_linked: bool
    direct_import_in_error: bool
    deleted: bool


class BudgetSummary(BaseModel):
    id: str
    name: str
    last_modified_on: str
    first_month: str
    last_month: str
    date_format: DateFormat
    currency_format: CurrencyFormat
    accounts: list[Account] | None


class BudgetSummaryResponse(BaseModel):
    budgets: list[BudgetSummary]
    default_budget: BudgetSummary | None


class BaseTransaction(BaseModel):
    amount: int
    category_id: str | None
    payee_id: str | None
    payee_name: str | None
    memo: str | None


class SaveSubTransaction(BaseTransaction):
    amount: int


class SubTransaction(BaseTransaction):
    id: str
    transaction_id: str
    category_name: str | None
    transfer_account_id: str | None
    transfer_transaction_id: str | None
    deleted: bool


class SaveTransactionWrapper(BaseTransaction):
    account_id: str
    date: str
    cleared: str | None
    approved: bool
    flag_color: FLAG_COLOR | None
    import_id: str | None
    subtransactions: list[SaveSubTransaction] | None


class TransactionDetail(BaseTransaction):
    id: str
    date: str
    cleared: str  # todo make enum
    approved: bool
    flag_color: FLAG_COLOR | None
    account_id: str
    transfer_account_id: str | None
    transfer_transaction_id: str | None
    matched_transaction_id: str | None
    import_id: str | None
    deleted: bool
    account_name: str
    category_name: str | None
    subtransactions: list[SubTransaction]

    def split(self, splitwise_id: str) -> SaveTransactionWrapper:
        split_amount = self.amount / 2
        personal_subtransaction = SaveSubTransaction(
            amount=split_amount,
            category_id=self.category_id,
            payee_id=self.payee_id,
            payee_name=self.payee_name,
            memo=self.memo,
        )
        splitwise_subtransaction = SaveSubTransaction(
            amount=split_amount,
            category_id=splitwise_id,
            payee_id=self.payee_id,
            payee_name=self.payee_name,
            memo="Auto-split",
        )
        return SaveTransactionWrapper(
            amount=self.amount,
            account_id=self.account_id,
            date=self.date,
            approved=True,
            flag_color=None,
            category_id=None,
            cleared="cleared",
            subtransactions=[personal_subtransaction, splitwise_subtransaction]
        )


class TransactionsResponse(BaseModel):
    transactions: list[TransactionDetail]
    server_knowledge: int

    @property
    def total_transactions(self) -> int:
        return len(self.transactions)

    @property
    def total_accounts(self) -> int:
        accounts = set([transaction.account_id for transaction in self.transactions])
        return len(accounts)