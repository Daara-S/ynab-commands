from __future__ import annotations

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

    @property
    def should_split(self) -> bool:
        return self.flag_color == "purple" and len(self.subtransactions) == 0


class TransactionsResponse(BaseModel):
    transactions: list[TransactionDetail]
    server_knowledge: int

    def __iter__(self):
        return iter(self.transactions)

    def __len__(self):
        return len(self.transactions)

    @property
    def total_accounts(self) -> int:
        accounts = set([transaction.account_id for transaction in self.transactions])
        return len(accounts)

    @property
    def transaction_total(self) -> int:
        return sum(transaction.amount for transaction in self.transactions)

    def get_transactions_to_split(self) -> TransactionsResponse:
        return TransactionsResponse(
            transactions=[t for t in self.transactions if t.should_split],
            server_knowledge=self.server_knowledge,
        )
