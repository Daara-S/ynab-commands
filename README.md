# Todo
- add splitwise API to automatically send that total to be split equally
- add sync option to sync splitwise balance with Splitwise tracked account
  - my split transactions will send money to the splitwise tracked account instead of to the budget category
  

### Spltwise sync
The sync will pull the latest transactions from splitwise based on the most recent transaction in the YNAB tracked account

Basic version will just pull total funds from "https://secure.splitwise.com/api/v3.0/get_groups"
and will grab the debts in `groups[0]["original_debts"]["amount"]`

It will then take the difference between the account balance and the debt and make a transaction on the account to get it in line with 
splitwise value.
