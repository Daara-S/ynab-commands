import logging

from pydantic import SecretStr
from splitwise import Splitwise, User
from splitwise.user import Friend

from ynab_commands.models import ExpenseData

log = logging.getLogger(__name__)


class SplitwiseAPI:
    _api: Splitwise
    _current_user: User

    def __init__(
        self, consumer_key: SecretStr, consumer_secret: SecretStr, api_key: SecretStr
    ):
        self._api = Splitwise(
            consumer_key=consumer_key.get_secret_value(),
            consumer_secret=consumer_secret.get_secret_value(),
            api_key=api_key.get_secret_value(),
        )
        self._current_user = self._api.getCurrentUser()

    def _get_wife(self, first_name: str) -> Friend:
        friends = self._api.getFriends()
        return next(friend for friend in friends if friend.first_name == first_name)

    def _create_expense(
        self, description: str, total: float, friend_id: int
    ) -> ExpenseData:
        owed_share = total / 2
        return ExpenseData(
            **{
                "description": description,
                "cost": total,
                "users": [
                    {
                        "id": self._current_user.id,
                        "paid_share": total,
                        "owed_share": owed_share,
                    },
                    {
                        "id": friend_id,
                        "paid_share": 0,
                        "owed_share": owed_share,
                    },
                ],
            }
        )

    def update_splitwise(self, total: float):
        friend = self._get_wife(first_name="Jasperi")
        log.debug(f"found wife: {friend.first_name}.")

        expense = self._create_expense(
            description="Groceries and takeout",
            total=total,
            friend_id=friend.id,
        )
        log.debug(f"created_expense: {expense.dict()}")

        expense, errors = self._api.createExpense(expense)

        if errors is not None:
            log.error("An error occurred in updating splitwise: %s", errors.getErrors())
        else:
            print(f"{total:.2f} added to splitwise")
