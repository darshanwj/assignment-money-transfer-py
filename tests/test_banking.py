from banking import app, db
import pytest
import os


@pytest.fixture
def client():
    """This client fixture will be called by each individual test. 
    It gives us a simple interface to the application, where we can trigger test requests to the application 
    """
    app.config.update(
        # disable error catching during request handling, so that you get better error reports when performing test requests
        TESTING=True,
        _DATABASE=os.path.join(app.instance_path, 'banking-tests.sqlite3')
    )
    # Empty db before each test
    with app.app_context():
        db.init_db()

    return app.test_client()


def test_create_account(client):
    for tc in [
        ('260.532', '260.53'),
        (425.2, '425.20'),
        ('73.4962', '73.49'),
        ('167.2999', '167.29'),
        ('872.001', '872.00'),
        ('872.009', '872.00'),
        (35.895, '35.89'),
        ('24', '24.00'),
        (62, '62.00'),
    ]:
        rv = client.post('/api/accounts', json={
            'customer_id': '1',
            'currency': 'USD',
            'balance': tc[0]
        })
        json_data = rv.get_json()
        print(json_data)
        assert rv.status_code == 201
        assert not json_data.get('id') is None
        assert json_data['customer_id'] == 1
        assert json_data['currency'] == 'USD'
        assert json_data['balance'] == tc[1]

    # unsupported currency
    rv = client.post('/api/accounts', json={
        'customer_id': '1',
        'currency': 23,
        'balance': 'LKR'
    })
    json_data = rv.get_json()
    print(json_data)
    assert rv.status_code == 422

    assert client.post('/api/accounts').status_code == 400


def test_end_to_end(client):
    # create sender account
    sender_bal = '260.53'
    rv = client.post('/api/accounts', json={
        'customer_id': '1',
        'currency': 'USD',
        'balance': sender_bal
    })
    json_data = rv.get_json()
    print(json_data)
    assert rv.status_code == 201
    sender_id = json_data.get('id')
    assert not sender_id is None

    # create receiver account
    receiver_bal = '840'
    rv = client.post('/api/accounts', json={
        'customer_id': '1',
        'currency': 'USD',
        'balance': receiver_bal
    })
    json_data = rv.get_json()
    print(json_data)
    assert rv.status_code == 201
    receiver_id = json_data.get('id')
    assert not receiver_id is None

    # find both in list of accounts
    rv = client.get('/api/accounts')
    json_data = rv.get_json()
    print(json_data)
    assert rv.status_code == 200
    assert len(json_data) == 2
    for account in json_data:
        assert account.get('customer_id') == 1
        assert account.get('currency') == 'USD'
    assert json_data[0].get('id') == sender_id
    assert json_data[1].get('id') == receiver_id

    # another one diff currency
    rv = client.post('/api/accounts', json={
        'customer_id': '1',
        'currency': 'GBP',
        'balance': 39400
    })
    json_data = rv.get_json()
    print(json_data)
    assert rv.status_code == 201
    lkr_acc = json_data.get('id')
    assert not lkr_acc is None

    # test invalid transfers
    rv = client.post('/api/transfer')
    for tc in [
        (1212, receiver_id, 'USD', 100),
        (sender_id, 2323, 'USD', 100),
        (sender_id, receiver_id, 'AED', 100),
        (sender_id, receiver_id, 'USD', 300),
        (sender_id, lkr_acc, 'USD', 35)
    ]:
        rv = client.post('/api/transfer', json={
            'sender_id': tc[0],
            'receiver_id': tc[1],
            'currency': tc[2],
            'amount': tc[3]
        })
        print(rv.get_json())
        assert rv.status_code == 422

    # test valid transfer
    rv = client.post('/api/transfer', json={
        'sender_id': sender_id,
        'receiver_id': receiver_id,
        'currency': 'USD',
        'amount': '100.00'
    })
    json_data = rv.get_json()
    print(json_data)
    assert rv.status_code == 201
    assert json_data.get('id') == sender_id

    # confirm account balances
    rv = client.get('/api/accounts')
    json_data = rv.get_json()
    print(json_data)
    assert rv.status_code == 200
    assert json_data[0].get('balance') == '160.53'
    assert json_data[1].get('balance') == '940.00'
