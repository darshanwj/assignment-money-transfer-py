from . import app, models, repos
from flask import json, request
from flask_marshmallow import exceptions


@app.route('/')
def home():
    return 'here we go again!'


@app.route('/accounts')
def getAccounts():
    account = models.Account(2, "USD", 243.23)
    repos.MemStorage.insertAccount(account)
    return models.accounts_schema.jsonify(repos.MemStorage.Accounts)


# curl -X POST -d '{"customer_id":2,"currency":"USD","balance":500}' -H 'Content-Type: application/json' http://127.0.0.1:5000/accounts
@app.route('/accounts', methods=['POST'])
def postAccount():
    json_data = request.get_json()
    if not json_data:
        return {"message": "No input data provided"}, 400
    # Validate and deserialize input
    try:
        account = models.account_schema.load(json_data)
    except exceptions.ValidationError as err:
        return err.messages, 422
    repos.MemStorage.insertAccount(account)
    # @TODO handle uncaught exceptions
    return json.jsonify(account)
