from . import ma, repos
from flask_marshmallow import fields, exceptions
from marshmallow import validates
import uuid


class AccountSchema(ma.Schema):
    id = fields.fields.UUID(load_only=True, missing=uuid.uuid1)
    customer_id = fields.fields.Int(required=True)
    currency = fields.fields.Str(required=True)
    balance = fields.fields.Float(required=True)


account_schema = AccountSchema()
accounts_schema = AccountSchema(many=True)


class TransferSchema(ma.Schema):
    sender_id = fields.fields.UUID(required=True)
    receiver_id = fields.fields.UUID(required=True)
    currency = fields.fields.Str(required=True)
    amount = fields.fields.Float(required=True)

    @validates('sender_id')
    def validate_sender(self, sender_id):
        if not repos.MemStorage.findAccountById(sender_id):
            raise exceptions.ValidationError('Sender account not found')

    @validates('receiver_id')
    def validate_receiver(self, receiver_id):
        if not repos.MemStorage.findAccountById(receiver_id):
            raise exceptions.ValidationError('Receiver account not found')


transfer_schema = TransferSchema()
