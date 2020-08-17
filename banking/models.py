from . import ma
from flask_marshmallow import fields
import uuid


class Account:
    def __init__(self, customer_id, currency, balance):
        self.id = uuid.uuid1()
        self.customer_id = customer_id
        self.currency = currency
        self.balance = balance


class AccountSchema(ma.Schema):
    id = fields.fields.UUID(dump_only=True, default=uuid.uuid1())
    customer_id = fields.fields.Int(required=True)
    currency = fields.fields.Str(required=True)
    balance = fields.fields.Float(required=True)


account_schema = AccountSchema()
accounts_schema = AccountSchema(many=True)
