from __future__ import annotations

from collections import Counter
from enum import IntEnum
from typing import Any, Iterator, List, Literal

from pydantic import BaseModel
from splitwise import Expense, User

FLAG_COLOR = Literal["red", "orange", "yellow", "green", "blue", "purple"]


class MilliUnits(int):
    def __repr__(self):
        return f"£{abs(self / 1000)}"

    def to_float(self) -> float:
        return abs(self / 1000)

    def __add__(self, other) -> MilliUnits:
        return MilliUnits(super().__add__(other))

    def __radd__(self, other) -> MilliUnits:
        return self.__add__(other)


class ExpenseUser(BaseModel, User):
    id: int
    paid_share: float
    owed_share: float


class ExpenseData(BaseModel, Expense):
    description: str
    cost: float
    users: list[ExpenseUser]


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
    display_symbol: bool


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
    last_reconciled_at: str | None = None
    debt_original_balance: int | None = None
    debt_interest_rates: dict[str, Any] | None = None
    debt_minimum_payments: dict[str, Any] | None = None
    debt_escrow_amounts: dict[str, Any] | None = None
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
    amount: MilliUnits
    category_id: str | None
    payee_id: str | None
    payee_name: str | None
    memo: str | None


class SaveSubTransaction(BaseTransaction):
    amount: MilliUnits


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


class SaveTransactionWithIdOrImportId(BaseTransaction):
    id: str
    amount: MilliUnits | None
    account_id: str | None
    date: str | None
    approved: bool | None
    cleared: str | None
    flag_color: FLAG_COLOR | None
    subtransactions: list[SaveSubTransaction]


class PatchTransactionWrapper(BaseModel):
    transactions: List[SaveTransactionWithIdOrImportId]


class TransactionDetail(BaseTransaction):
    id: str
    date: str
    cleared: str  # todo make enum
    approved: bool
    flag_color: FLAG_COLOR | None
    flag_name: str | None
    account_id: str
    transfer_account_id: str | None
    transfer_transaction_id: str | None
    matched_transaction_id: str | None
    import_id: str | None
    import_payee_name: str | None
    import_payee_name_original: str | None
    debt_transaction_type: str | None
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

    def __iter__(self) -> Iterator[TransactionDetail]:  # type:ignore[override]
        return iter(self.transactions)

    def __len__(self) -> int:
        return len(self.transactions)

    @property
    def total_accounts(self) -> int:
        accounts = set([transaction.account_id for transaction in self.transactions])
        return len(accounts)

    @property
    def transaction_total(self) -> MilliUnits:
        return MilliUnits(sum(transaction.amount for transaction in self.transactions))

    def get_transactions_to_split(self) -> TransactionsResponse:
        return TransactionsResponse(
            transactions=[t for t in self.transactions if t.should_split],
            server_knowledge=self.server_knowledge,
        )

    def print_transaction_info(self) -> None:
        account_names = [transaction.account_name for transaction in self.transactions]
        account_counts = Counter(account_names)

        print(repr(self.transaction_total))
        for account, count in account_counts.items():
            print(f"{account}: {count} transactions")
