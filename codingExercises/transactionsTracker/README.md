# Transaction Tracker — Coding Interview Practice

## Overview

Build and extend a simple in-memory transaction tracking service in Python.

This exercise simulates a progressive coding interview: you start with an existing implementation, fix bugs, implement new functionality, handle edge cases, and improve performance by introducing an additional data structure.

**Goal:** Practice reading unfamiliar code, making targeted changes, testing behavior, and explaining engineering tradeoffs.

## Setup

Requirements:

* Python 3.9+
* No external dependencies

Create a file named `transactions_tracker.py` and begin with the following code:

```python
class TransactionStore:
    def __init__(self):
        self.transactions = {}

    def add(self, transaction):
        self.transactions[transaction["id"]] = transaction

    def get(self, transaction_id):
        return self.transactions.get(transaction_id)

    def total_for_user(self, user_id):
        total = 0
        for transaction in self.transactions.values():
            if transaction["user_id"] == user_id:
                total = transaction["amount"]
        return total


if __name__ == "__main__":
    store = TransactionStore()

    store.add({"id": "t1", "user_id": "u1", "amount": 20})
    store.add({"id": "t2", "user_id": "u1", "amount": 30})
    store.add({"id": "t3", "user_id": "u2", "amount": 10})

    print("User u1 total:", store.total_for_user("u1"))
    print("User u2 total:", store.total_for_user("u2"))
    print("Transaction t1:", store.get("t1"))
```

Run the program:

```bash
python transactions_tracker.py
```

Observe the output before making changes. Use the test harness to verify each change as you progress.

## Stage 1 — Debug Existing Code

The `total_for_user(user_id)` method returns an incorrect total when a user has multiple transactions.

Tasks:

* Identify the bug.
* Explain why it occurs.
* Make the smallest possible fix.
* Verify the result for users with one transaction and multiple transactions.

Constraint: Do not rewrite the method or change the data structure.

## Stage 2 — Implement User Lookup

Add the following method:

```python
def get_by_user(self, user_id):
    ...
```

Requirements:

* Return a list of all transactions belonging to the specified user.
* Return an empty list if the user has no transactions.
* Preserve the order in which transactions were added.
* Do not modify the stored transactions.

Test users with multiple transactions, one transaction, and no transactions.

## Stage 3 — Reject Duplicate Transaction IDs

Currently, adding a transaction with an existing ID silently overwrites the original transaction.

Update `add(transaction)` to meet these requirements:

* Store new transactions normally.
* Raise `ValueError` when a transaction ID already exists.
* Preserve the original transaction if a duplicate is rejected.

Test both normal additions and duplicate additions.

## Stage 4 — Improve Lookup Performance

The current implementation of `get_by_user()` scans every transaction.

Introduce an additional data structure that supports efficient lookup by user ID.

Requirements:

* `add()` updates the main store and the additional index.
* `get_by_user()` uses the additional index rather than scanning every transaction.
* Duplicate IDs remain rejected.
* Results remain in insertion order.
* Both data structures remain consistent.

Consider the tradeoffs of maintaining redundant data and the potential for inconsistencies.

## Stage 5 — Implement Removal

Add the following method:

```python
def remove(self, transaction_id):
    ...
```

Requirements:

* Remove the transaction from the store.
* Update all relevant data structures.
* Return the removed transaction on success.
* Return `None` if the transaction ID does not exist.
* Ensure totals and user-specific lookups remain correct after removal.

Test removing an existing transaction, removing a nonexistent transaction, and removing a user's last transaction.

## Testing Checklist

Use this checklist as you work:

* [ ] A user with multiple transactions gets the correct total.
* [ ] A user with one transaction gets the correct total.
* [ ] An unknown user gets an empty list from `get_by_user()`.
* [ ] User-specific lookup returns all the correct transactions in insertion order.
* [ ] Adding a duplicate ID raises `ValueError`.
* [ ] A rejected duplicate does not overwrite the original transaction.
* [ ] Adding a transaction updates all data structures.
* [ ] Removing a transaction updates all data structures.
* [ ] Removing a nonexistent ID returns `None`.
* [ ] Removing the last transaction for a user leaves lookup behavior correct.
* [ ] Totals remain correct after additions and removals.

## Interview Practice Guidelines

For each stage:

1. Read the existing implementation before editing.
2. Explain the problem and your intended approach out loud.
3. Make one change at a time.
4. Run the program and test relevant edge cases.
5. Review whether the change affects other methods or data structures.
6. Explain the time complexity and any relevant tradeoffs.

Try to solve each task independently before looking for help. If stuck, ask for a hint rather than a complete solution.

## Stretch Goals

After completing the required stages, consider:

* What happens if a transaction is missing a required field?
* Should negative amounts be allowed?
* How would you validate transaction data?
* What are the time complexities of `add()`, `get()`, `get_by_user()`, `total_for_user()`, and `remove()`?
* How would the design change if transactions were stored in a database?
* How would you test the class automatically with Python's built-in `unittest` module?

## Completion Criteria

The exercise is complete when all required behaviors work, all relevant tests pass, and the implementation maintains consistent state across its data structures.

Prioritize correctness and clarity over cleverness or premature optimization.
