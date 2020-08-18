from . import app, models, repos
from flask import json, request
from flask_marshmallow import exceptions


@app.route('/')
def home():
    return 'here we go again!'


# curl -H 'Content-Type: application/json' http://127.0.0.1:5000/accounts
@app.route('/accounts')
def get_accounts():
    return models.accounts_schema.jsonify(repos.MemStorage.Accounts)


# curl -X POST -d '{"customer_id":2,"currency":"USD","balance":500}' -H 'Content-Type: application/json' http://127.0.0.1:5000/accounts
@app.route('/accounts', methods=['POST'])
def post_account():
    json_data = request.get_json()
    if not json_data:
        return {"message": "No input data provided"}, 400
    # validate and deserialize input
    try:
        account = models.account_schema.load(json_data)
    except exceptions.ValidationError as err:
        return err.messages, 422
    repos.MemStorage.insertAccount(account)
    # @TODO handle uncaught exceptions
    return json.jsonify(account), 201


# curl -X POST -d '{"sender_id":2,"receiver_id":2,"currency":"USD","amount":500}' -H 'Content-Type: application/json' http://127.0.0.1:5000/transfer
@app.route('/transfer', methods=['POST'])
def post_transfer():
    json_data = request.get_json()
    if not json_data:
        return {"message": "No input data provided"}, 400
    # validate and deserialize input
    try:
        transfer = models.transfer_schema.load(json_data)
    except exceptions.ValidationError as err:
        return err.messages, 422
    return json.jsonify("done")
