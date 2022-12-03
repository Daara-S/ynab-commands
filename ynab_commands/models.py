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


class SubTransaction(BaseModel):
    id: str
    transaction_id: str
    amount: int
    memo: str | None
    payee_id: str | None
    payee_name: str | None
    category_id: str | None
    category_name: str | None
    transfer_account_id: str | None
    transfer_transaction_id: str | None
    deleted: bool



class TransactionDetail(BaseModel):
    id: str
    date: str
    amount: int
    memo: str | None
    cleared: str # todo make enum
    approved: bool
    flag_color: FLAG_COLOR
    account_id: str
    payee_id: str | None
    category_id: str | None
    transfer_account_id: str | None
    transfer_transaction_id: str | None
    matched_transaction_id: str | None
    import_id: str | None
    deleted: bool
    account_name: str
    payee_name: str | None
    category_name: str | None
    subtransactions: list[SubTransaction]


class TransactionsResponse(BaseModel):
    transactions: list[TransactionDetail]
    server_knowledge: int