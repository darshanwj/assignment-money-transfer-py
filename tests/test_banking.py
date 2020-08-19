from banking import app
import pytest


# This client fixture will be called by each individual test.
# It gives us a simple interface to the application, where we can trigger test requests to the application
@pytest.fixture
def client():
    # disable error catching during request handling, so that you get better error reports when performing test requests
    app.config['TESTING'] = True
    return app.test_client()


def test_home(client):
    rv = client.get('/')
    assert b'{"message":"here we are!"}\n' in rv.data


def test_end_to_end(client):
    # create sender account
    rv = client.post('/accounts', json={
        'customer_id': '1',
        'currency': 'USD',
        'balance': 260
    })
    json_data = rv.get_json()
    print(json_data)
    assert not json_data.get('id') is None
    sender_id = json_data.get('id')

    # create receiver account
    rv = client.post('/accounts', json={
        'customer_id': '1',
        'currency': 'USD',
        'balance': 840
    })
    json_data = rv.get_json()
    print(json_data)
    assert not json_data.get('id') is None
    receiver_id = json_data.get('id')

    # find both in list of accounts
    rv = client.get('/accounts')
    json_data = rv.get_json()
    print(json_data)
    assert len(json_data) == 2
    for account in json_data:
        assert account.get('customer_id') == 1
        assert account.get('currency') == 'USD'
    assert json_data[0].get('id') == sender_id
    assert json_data[1].get('id') == receiver_id

    # test invalid transfers
    cases = [
        (1212, receiver_id, 'USD', 100),
        (sender_id, 2323, 'USD', 100),
        (sender_id, receiver_id, 'AED', 100),
        (sender_id, receiver_id, 'USD', 300)
    ]
    for case in cases:
        rv = client.post('/transfer', json={
            'sender_id': case[0],
            'receiver_id': case[1],
            'currency': case[2],
            'amount': case[3]
        })
        print(rv.get_json())
        assert rv.status_code == 422

    # test valid transfer
    rv = client.post('/transfer', json={
        'sender_id': sender_id,
        'receiver_id': receiver_id,
        'currency': 'USD',
        'amount': 100
    })
    print(rv.get_json())
    assert rv.status_code == 201
