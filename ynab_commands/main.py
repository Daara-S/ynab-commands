from ynab_commands.budget_sync import BudgetSync


def run():
    app = BudgetSync()
    app.run()


if __name__ == "__main__":
    run()
