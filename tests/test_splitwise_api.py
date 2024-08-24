from unittest.mock import MagicMock, patch

import pytest
from splitwise.user import CurrentUser

from ynab_commands.splitwise_api import SplitwiseAPI


@pytest.mark.parametrize(
    "total, owed_share, adjusted_owed_share",
    [
        (10.01, 5.0, 5.01),
        (25.0, 12.5, 12.5),
        (13.99, 7, 6.99),
        (357.33, 178.66, 178.67),
    ],
)
def test_create_expense_sets_adjusted_owed_share_correctly(
    splitwise_api: SplitwiseAPI,
    total: float,
    owed_share: float,
    adjusted_owed_share: float,
):
    mock_user = MagicMock(spec=CurrentUser)
    mock_user.id = 111
    with patch.object(splitwise_api._api, "getCurrentUser", return_value=mock_user):
        expense = splitwise_api._create_expense(
            description="groceries", total=total, friend_id=12
        )
        assert expense.cost == total
        assert expense.users[0].owed_share == adjusted_owed_share
        assert expense.users[1].owed_share == owed_share
        assert sum(user.owed_share for user in expense.users) == pytest.approx(total)
