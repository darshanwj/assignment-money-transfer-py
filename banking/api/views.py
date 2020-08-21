from . import bp
from .. import models, repos
from flask import json, request
from flask_marshmallow import exceptions


# curl -H 'Content-Type: application/json' http://127.0.0.1:5000/accounts
@bp.route('/accounts')
def get_accounts():
    return models.accounts_schema.jsonify(repos.MemStorage.Accounts)


# curl -X POST -d '{"customer_id":2,"currency":"USD","balance":500}' -H 'Content-Type: application/json' http://127.0.0.1:5000/accounts
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
    repos.MemStorage.insert_account(account)
    # @TODO handle uncaught exceptions
    return json.jsonify(account), 201


# curl -X POST -d '{"sender_id":2,"receiver_id":2,"currency":"USD","amount":500}' -H 'Content-Type: application/json' http://127.0.0.1:5000/transfer
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
    transfer['sender']['balance'] -= transfer['amount']
    transfer['receiver']['balance'] += transfer['amount']
    return json.jsonify(transfer['sender']), 201
