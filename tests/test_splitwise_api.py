from unittest.mock import MagicMock, patch

import pytest
from splitwise.user import CurrentUser

from ynab_commands.models import ExpenseData
from ynab_commands.splitwise_api import SplitwiseAPI


def test_create_expense_returns_expense_data_obj(splitwise_api: SplitwiseAPI):
    mock_user = MagicMock(spec=CurrentUser)
    mock_user.id = 111
    total_cost = 12.23
    with patch.object(splitwise_api._api, "getCurrentUser", return_value=mock_user):
        expense = splitwise_api._create_expense(
            description="groceries", total=total_cost, friend_id=12
        )
        assert isinstance(expense, ExpenseData)
        assert expense.users[0].id == 111
        assert expense.users[1].id == 12
        assert sum(user.owed_share for user in expense.users) == pytest.approx(
            total_cost
        )
