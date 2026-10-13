class TransactionStore:
    def __init__(self):
        self.transactions = {}
        self.transactions_by_user = {}

    def add(self, transaction):
        if transaction["id"] in self.transactions:
            raise ValueError("Transaction id already exists")
        self.transactions[transaction["id"]] = transaction
        if transaction["user_id"] not in self.transactions_by_user:
            self.transactions_by_user[transaction["user_id"]] = {transaction["id"]: transaction}
        else:
            self.transactions_by_user[transaction["user_id"]][transaction["id"]] = transaction

    def get(self, transaction_id):
        return self.transactions.get(transaction_id)

    def total_for_user(self, user_id):
        total = 0
        for transaction in self.transactions.values():
            if transaction["user_id"] == user_id:
                total += transaction["amount"]
        return total

    # initial slow version
    # def get_by_user(self, user_id):
    #     transactions = []
    #     for transaction in self.transactions.values():
    #         if transaction["user_id"] == user_id:
    #             transactions.append(transaction)
    #     return transactions

    # new version with updated data structure
    def get_by_user(self, user_id):
        if user_id not in self.transactions_by_user:
            return []
        transactions = []
        for transaction in self.transactions_by_user[user_id].values():
            transactions.append(transaction)
        return transactions

    def remove(self, transaction_id):
        if transaction_id not in self.transactions:
            return None
        transaction = self.transactions.pop(transaction_id)
        user_id = transaction["user_id"]
        self.transactions_by_user[user_id].pop(transaction_id)



if __name__ == "__main__":
    store = TransactionStore()

    store.add({"id": "t1", "user_id": "u1", "amount": 20})
    store.add({"id": "t2", "user_id": "u1", "amount": 30})
    store.add({"id": "t3", "user_id": "u2", "amount": 10})
    # print(store.transactions)
    # print(store.transactions_by_user)

    print("User u1 total:", store.total_for_user("u1"))
    print("User u2 total:", store.total_for_user("u2"))
    print("Transaction t1:", store.get("t1"))
    print("User u1 transactions:", store.get_by_user("u1")) # Expect t1 and t2

    # store.add({"id": "t3", "user_id": "u2", "amount": 50}) # Expect to raise error
    print("User u2 transactions:", store.get_by_user("u2")) # Expect amount to be 10

    store.remove("t2")
    print(store.transactions)
    print(store.transactions_by_user)
    print("Transaction t2:", store.get("t2")) # Expect empty
    print("User u1 total:", store.total_for_user("u1")) # Expect to be 20
    print("User u1 transactions:", store.get_by_user("u1")) # Expect to be just t1

    print(store.get_by_user("u999"))
    print(store.remove("t999"))