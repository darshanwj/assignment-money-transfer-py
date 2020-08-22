from .db import get_db


class Accounts():

    @classmethod
    def insert_account(cls, account):
        db = get_db()
        db.execute(
            'INSERT INTO account (customer_id, currency, balance) VALUES (?, ?, ?)',
            (account['customer_id'], account['currency'],
             str(account['balance']))
        )
        db.commit()
        cur = db.execute('SELECT last_insert_rowid()')
        return cur.fetchone()[0]

    @classmethod
    def find_account_by_id(cls, id):
        db = get_db()
        cur = db.execute('SELECT * FROM account WHERE id = ?', (id,))
        acc = cur.fetchone()
        return acc

    @classmethod
    def find_accounts(cls):
        db = get_db()
        cur = db.execute('SELECT * FROM account')
        accs = cur.fetchall()
        return accs

    @classmethod
    def update_balances(cls, sender_id, sender_bal, receiver_id, receiver_bal):
        db = get_db()
        db.execute('UPDATE account SET balance = ? WHERE id = ?',
                   (str(sender_bal), sender_id))
        db.execute('UPDATE account SET balance = ? WHERE id = ?',
                   (str(receiver_bal), receiver_id))
        db.commit()
