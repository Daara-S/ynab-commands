from pydantic import SecretStr
from splitwise import Expense, Splitwise, User
from splitwise.user import ExpenseUser


class SplitwiseAPI:
    _api: Splitwise
    _user: User

    def __init__(
        self, consumer_key: SecretStr, consumer_secret: SecretStr, api_key: SecretStr
    ):
        self._api = Splitwise(
            consumer_key=consumer_key.get_secret_value(),
            consumer_secret=consumer_secret.get_secret_value(),
            api_key=api_key.get_secret_value(),
        )
        self._user = self._api.getCurrentUser()

    def update_splitwise(self, total: int):
        friend: User = next(
            friend
            for friend in self._api.getFriends()
            if friend.first_name == "Jasperi"
        )
        expense = Expense(
            {
                "description": "groceries and takeout",
                "cost": total,
            }
        )
        self_expense_user = ExpenseUser(
            {"id": self._user.id, "paid_share": total, "owed_share": total // 2}
        )
        friend_expense_user = ExpenseUser(
            {"id": friend.id, "paid_share": 0, "owed_share": total // 2}
        )

        expense.addUser(self_expense_user)
        expense.addUser(friend_expense_user)
        expense, errors = self._api.createExpense(expense)
        if errors is not None:
            raise errors
        print("{total:.2f} added to splitwise")
