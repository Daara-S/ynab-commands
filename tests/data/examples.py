EXAMPLE_BUDGET_LIST = {
    "data": {
        "budgets": [
            {
                "id": "string",
                "name": "string",
                "last_modified_on": "2022-12-03T18:23:02.916Z",
                "first_month": "string",
                "last_month": "string",
                "date_format": {
                    "format": "string"
                },
                "currency_format": {
                    "iso_code": "string",
                    "example_format": "string",
                    "decimal_digits": 0,
                    "decimal_separator": "string",
                    "symbol_first": True,
                    "group_separator": "string",
                    "currency_symbol": "string",
                    "display_symbol": True
                },
                "accounts": [
                    {
                        "id": "string",
                        "name": "string",
                        "type": "checking",
                        "on_budget": True,
                        "closed": True,
                        "note": "string",
                        "balance": 0,
                        "cleared_balance": 0,
                        "uncleared_balance": 0,
                        "transfer_payee_id": "string",
                        "direct_import_linked": True,
                        "direct_import_in_error": True,
                        "deleted": True
                    }
                ]
            }
        ],
        "default_budget": {
            "id": "string",
            "name": "string",
            "last_modified_on": "2022-12-03T18:23:02.916Z",
            "first_month": "string",
            "last_month": "string",
            "date_format": {
                "format": "string"
            },
            "currency_format": {
                "iso_code": "string",
                "example_format": "string",
                "decimal_digits": 0,
                "decimal_separator": "string",
                "symbol_first": True,
                "group_separator": "string",
                "currency_symbol": "string",
                "display_symbol": True
            },
            "accounts": [
                {
                    "id": "string",
                    "name": "string",
                    "type": "checking",
                    "on_budget": True,
                    "closed": True,
                    "note": "string",
                    "balance": 0,
                    "cleared_balance": 0,
                    "uncleared_balance": 0,
                    "transfer_payee_id": "string",
                    "direct_import_linked": True,
                    "direct_import_in_error": True,
                    "deleted": True
                }
            ]
        }
    }
}

EXAMPLE_ACCOUNT = {
    "id": "string",
    "name": "string",
    "type": "checking",
    "on_budget": True,
    "closed": True,
    "note": "string",
    "balance": 0,
    "cleared_balance": 0,
    "uncleared_balance": 0,
    "transfer_payee_id": "string",
    "direct_import_linked": True,
    "direct_import_in_error": True,
    "deleted": True
}

EXAMPLE_TRANSACTION_LIST = {
    "data": {
        "transactions": [
            {
                "id": "string",
                "date": "string",
                "amount": 0,
                "memo": "string",
                "cleared": "cleared",
                "approved": True,
                "flag_color": "red",
                "account_id": "string",
                "payee_id": "string",
                "category_id": "string",
                "transfer_account_id": "string",
                "transfer_transaction_id": "string",
                "matched_transaction_id": "string",
                "import_id": "string",
                "deleted": True,
                "account_name": "string",
                "payee_name": "string",
                "category_name": "string",
                "subtransactions": [
                    {
                        "id": "string",
                        "transaction_id": "string",
                        "amount": 0,
                        "memo": "string",
                        "payee_id": "string",
                        "payee_name": "string",
                        "category_id": "string",
                        "category_name": "string",
                        "transfer_account_id": "string",
                        "transfer_transaction_id": "string",
                        "deleted": True
                    }
                ]
            }
        ],
        "server_knowledge": 0
    }
}
