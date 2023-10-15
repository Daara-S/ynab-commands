import os

from splitwise import Expense, Splitwise
from splitwise.user import ExpenseUser

from ynab_commands.config import configs

CONFIG = configs[os.getenv('ENV', 'Prod')]

def main():
    sObj = Splitwise(
        CONFIG.splitwise_consumer_key.get_secret_value(),
        CONFIG.splitwise_consumer_secret.get_secret_value(),
        api_key=CONFIG.splitwise_api_key.get_secret_value()
    )
    friends = sObj.getFriends()
    friend = [friend for friend in friends if friend.first_name == "Jasperi"][0]
    print(friend.id)

    myself = sObj.getCurrentUser()
    print(myself.id)

    expense = Expense()
    expense.setCost("10.0")
    expense.setDescription("test expense")
    user1 = ExpenseUser()
    user1.setId(myself.id)
    user1.setPaidShare("10.0")
    user1.setOwedShare("5.0")
    user2 = ExpenseUser()
    user2.setId(friend.id)
    user2.setPaidShare("0.00")
    user2.setOwedShare("5.0")
    expense.addUser(user1)
    expense.addUser(user2)
    nExpense, errors = sObj.createExpense(expense)
    print(nExpense.getId())

if __name__ == "__main__":
    main()
