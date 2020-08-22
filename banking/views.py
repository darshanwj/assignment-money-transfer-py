from . import models, repos, app
from flask import json, request
from flask_marshmallow import exceptions, fields


# curl -H 'Content-Type: application/json' http://127.0.0.1:5000/api/accounts
@app.route('/api/accounts')
def get_accounts():
    return models.accounts_schema.jsonify(repos.Accounts.find_accounts())


# curl -X POST -d '{"customer_id":2,"currency":"USD","balance":500}' -H 'Content-Type: application/json' http://127.0.0.1:5000/api/accounts
@app.route('/api/accounts', methods=['POST'])
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
@app.route('/api/transfer', methods=['POST'])
def post_transfer():
    json_data = request.get_json()
    if not json_data:
        return {'message': 'No input data provided'}, 400
    # validate and deserialize input
    try:
        transfer = models.transfer_schema.load(json_data)
    except exceptions.ValidationError as err:
        return err.messages, 422
    # try to use Decimal type directly
    f = fields.fields.Decimal(places=2)
    # just do it!
    sender_bal = f.deserialize(
        transfer['sender']['balance']) - transfer['amount']
    receiver_bal = f.deserialize(
        transfer['receiver']['balance']) + transfer['amount']
    repos.Accounts.update_balances(
        transfer['sender_id'], sender_bal, transfer['receiver_id'], receiver_bal)
    return models.account_schema.jsonify(repos.Accounts.find_account_by_id(transfer['sender_id'])), 201
