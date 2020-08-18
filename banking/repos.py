class MemStorage:
    Accounts = []

    @classmethod
    def insertAccount(cls, account):
        cls.Accounts.append(account)
        pass

    @classmethod
    def findAccountById(cls, id):
        for account in cls.Accounts:
            if account['id'] == id:
                return account
