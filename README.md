# wallet
test task wallet system


docker-compose build

docker-compose run -p 127.0.0.1:5000:5000 web


forms:

/signup

/login

/logout

/

--------------------

api:

-----------------

POST /api/signup

    import requests
    import json
    s = requests.Session()
    URL = 'http://localhost:5000/api/signup'
    params = json.dumps({'name': 'test1', 'email': 'test1@localhost.ru', 'password': 'Pa$$w0rd'})
    headers = {'Content-Type': 'application/json'}
    r = s.post(url=URL, data=params, headers=headers)

----------------

POST /api/login

    URL = 'http://localhost:5000/api/login'
    params = json.dumps({'email': 'test1@localhost.ru', 'password': 'Pa$$w0rd'})
    #or for bank account
    #from config import Config
    #params = json.dumps({'email': Config.BANK_EMAIL, 'password': Config.BANK_PASS})
    headers = {'Content-Type': 'application/json'}

------------------

GET /api/wallet

return {'wallet_id': wallet.wallet_id, 'user_id': wallet.user_id, 'balance': wallet.balance, 'operations': operations_list}

--------------------

POST /api/external_to_wallet

    URL = 'http://localhost:5000/api/external_to_wallet'
    headers = {'Content-Type': 'application/json'}
    params = json.dumps({'wallet_id': 2, 'amount': 115.6, 'details': 'Перевод из Тинькофф'})
    r = s.post(url=URL, data=params, headers=headers)
    
return {'status': 'OK', 'operation_id': operation.operation_id, 'wallet_id': wallet.wallet_id, 'balance': wallet.balance}

---------------------

POST /api/wallet_to_wallet

    URL = 'http://localhost:5000/api/wallet_to_wallet'
    headers = {'Content-Type': 'application/json'}
    params = json.dumps({'wallet_id': 1, 'amount': 11.1})
    r = s.post(url=URL, data=params, headers=headers)

return {'status': 'OK', 'operation_id': sender_operation.operation_id, 'wallet_id': sender_wallet.wallet_id, 'balance': sender_wallet.balance}
