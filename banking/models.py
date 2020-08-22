from . import repos, ma, app
from flask_marshmallow import fields, exceptions
from marshmallow import validate, post_load
import decimal


class AccountSchema(ma.Schema):
    id = fields.fields.Int(dump_only=True)
    customer_id = fields.fields.Int(required=True)
    currency = fields.fields.Str(
        required=True, validate=validate.OneOf(app.config['_CURRENCIES']))
    balance = fields.fields.Decimal(
        required=True, places=2, as_string=True, rounding=decimal.ROUND_DOWN)


account_schema = AccountSchema()
accounts_schema = AccountSchema(many=True)


class TransferSchema(ma.Schema):
    sender_id = fields.fields.Int(required=True)
    receiver_id = fields.fields.Int(required=True)
    currency = fields.fields.Str(
        required=True, validate=validate.OneOf(app.config['_CURRENCIES']))
    amount = fields.fields.Decimal(
        required=True, places=2, as_string=True, rounding=decimal.ROUND_DOWN)

    @post_load(pass_many=True)
    def validate_transfer(self, data, **kwags):
        sender = repos.Accounts.find_account_by_id(data['sender_id'])
        if not sender:
            raise exceptions.ValidationError(
                'Sender account not found', 'sender_id')
        receiver = repos.Accounts.find_account_by_id(data['receiver_id'])
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
