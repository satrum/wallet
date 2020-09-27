test task: simple wallet system

    1. нужна консистентность данных
    2. нужно обрабатывать быстро много транзакций
    3. транзакции 2 типов - внесение средств на кошелек, перевод с кошелька на кошелек

1 Приближение:

- База данных пока sqlite, в продуктивной же среде, потребуется отдельный сервер postgresql, располагающийся на постоянном хранилище данных
- Внесение средств извне должна осуществлять сама платежная система, поэтому /api/external_to_wallet авторизуется специальной учеткой, создаваемой при старте приложения
- Перевод с кошелька на кошелек возможен любым пользователем, у которого есть кошелек. Пользователь авторизуется, указывает сумму и кошелек на который хочет отправить средства со своего
- Добавил метод получения баланса и операций по кошельку, того пользователя который авторизовался
- Авторизация Basic с сохранением сессии

- Возможна ситуация когда с одним кошельком происходит множество одновременных внесений и переводов. В таком случае есть 2 варианта (реализован 2 вариант):
 
     - api методы создают асинхронную задачу, она попадает в очередь и выполняется по очереди. (проблема: не более 1 воркера, последовательное выполнение, база данных будет простаивать, а очередь накапливаться)
     - api методы проверяют блокировку на кошельках (отправителя и получателя). Если ее нет - блокируют, создают операции, изменяют баланс кошельков, разблокируют. Тогда возможно параллельная обработка операций с не связанными кошельками. (проблема: дополнительная операция записи в кошелек(блок, разблок), нужен таймаут для запроса, возможно операция не всегда будет проходить, не укладываясь в таймаут)


2 Развитие:
    
- Авторизацию можно изменить - oauth 2.0, с периодическим обновлением JWS токена
- отправление уведомлений (асинхронная задача)
- холды
- двухшагового перевода с созданием требования со стороны получателя
- вывода денег
- ввода денег с транзакцией банковского кошелька (для каждого банка отправителя создать учетку)
- БД postgres
- асинхронный фреймворк (https://pgjones.gitlab.io/quart/ - based on asyncio, flask API support)
   


Запуск:

    docker-compose build
    docker-compose run -p 127.0.0.1:5000:5000 web



Формы для http://127.0.0.1:5000/ :
    
    /signup - регистрация name, email, password
    /login - вход email, password
    /logout - выход
    / - страница после входа

--------------------

API:

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
