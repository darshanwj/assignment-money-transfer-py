from . import repos, ma
from flask_marshmallow import fields, exceptions
from marshmallow import validates, post_load
import uuid


class AccountSchema(ma.Schema):
    id = fields.fields.UUID(missing=uuid.uuid1)
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

    @post_load(pass_many=True)
    def validate_transfer(self, data, **kwags):
        sender = repos.MemStorage.find_account_by_id(data['sender_id'])
        if not sender:
            raise exceptions.ValidationError(
                'Sender account not found', 'sender_id')
        receiver = repos.MemStorage.find_account_by_id(data['receiver_id'])
        if not receiver:
            raise exceptions.ValidationError(
                'Receiver account not found', 'receiver_id')
        if sender['currency'] != data['currency']:
            raise exceptions.ValidationError(
                'Currency conversion not supported', 'currency')
        if sender['currency'] != receiver['currency']:
            raise exceptions.ValidationError(
                'Receiver should have the same currency as sender', 'currency')
        if sender['balance'] < data['amount']:
            raise exceptions.ValidationError(
                'Insufficient balance to perform transfer', 'balance')
        data['sender'] = sender
        data['receiver'] = receiver
        return data


transfer_schema = TransferSchema()
