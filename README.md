# Todo
[] Add sync with splitwise
[] Change Put to Patch to make it faster
[] containerize and put online with a cron job to run it

### Spltwise sync
The sync will pull the latest transactions from splitwise based on the most recent transaction in the YNAB tracked account

Basic version will just pull total funds from "https://secure.splitwise.com/api/v3.0/get_groups"
and will grab the debts in `groups[0]["original_debts"]["amount"]`

It will then take the difference between the account balance and the debt and make a transaction on the account to get it in line with
splitwise value.
