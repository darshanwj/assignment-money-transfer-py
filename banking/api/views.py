from . import bp
from .. import models, repos
from flask import json, request
from flask_marshmallow import exceptions


# curl -H 'Content-Type: application/json' http://127.0.0.1:5000/api/accounts
@bp.route('/accounts')
def get_accounts():
    return models.accounts_schema.jsonify(repos.Accounts.find_accounts())


# curl -X POST -d '{"customer_id":2,"currency":"USD","balance":500}' -H 'Content-Type: application/json' http://127.0.0.1:5000/api/accounts
@bp.route('/accounts', methods=['POST'])
def post_account():
    json_data = request.get_json()
    if not json_data:
        return {'message': 'No input data provided'}, 400
    # validate and deserialize input
    try:
        account = models.account_schema.load(json_data)
    except exceptions.ValidationError as err:
        return err.messages, 422
    id = repos.Accounts.insert_account(account)
    # @TODO handle uncaught exceptions
    return models.account_schema.jsonify(repos.Accounts.find_account_by_id(id)), 201


# curl -X POST -d '{"sender_id":2,"receiver_id":2,"currency":"USD","amount":500}' -H 'Content-Type: application/json' http://127.0.0.1:5000/api/api/transfer
@bp.route('/transfer', methods=['POST'])
def post_transfer():
    json_data = request.get_json()
    if not json_data:
        return {'message': 'No input data provided'}, 400
    # validate and deserialize input
    try:
        transfer = models.transfer_schema.load(json_data)
    except exceptions.ValidationError as err:
        return err.messages, 422
    # just do it!
    sender_bal = transfer['sender']['balance']
    sender_bal -= transfer['amount']
    receiver_bal = transfer['receiver']['balance']
    receiver_bal += transfer['amount']
    repos.Accounts.update_balances(
        transfer['sender_id'], sender_bal, transfer['receiver_id'], receiver_bal)
    return models.account_schema.jsonify(transfer['sender']), 201
