from . import db


class MemStorage:
    Accounts = []

    @classmethod
    def insert_account(cls, account):
        cls.Accounts.append(account)
        pass

    @classmethod
    def find_account_by_id(cls, id):
        for account in cls.Accounts:
            if account['id'] == id:
                return account
