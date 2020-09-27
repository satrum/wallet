import requests
import json

def test1():
    s = requests.Session()
    URL = 'http://localhost:5000/api/signup'
    params = json.dumps({'name': 'test1', 'email': 'test1@localhost.ru', 'password': 'Pa$$w0rd'})
    headers = {'Content-Type': 'application/json'}
    r = s.post(url=URL, data=params, headers=headers)

    print(r.status_code)
    print(r.headers)
    print(r.content)
    print(r.cookies.get_dict())
    return s

#4
cookie = {'session': '.eJwlzjsOwjAMANC7ZGbwL3Hcy1RxYgvWlk6Iu1OJ9U3vU_Y84nyW7X1c8Sj7a5Wt2FQIbW2B1oZkXkfM7otAIkGdQq2SkBgsI6xDughwRR1jsWUbc7C7pVE4tg5eW7irWGqOlUIQxD4zxAJ53YaYMxiUqTcud-Q64_hvuHx_njwvag.X20RuQ.Vsy1L-_1iJoXSlPqtCEP9sw-nUc'}
#6
#cookie = {'session': '.eJwlzjsOwjAMANC7ZGZw_InjXqaKE1uwtnRC3J1KrG96n7LnEeezbO_jikfZX6tsxaZCaGsLVFpFcxkxuy8EjgR1DDVBRjZYhlUGd2YgqTrGIss25iB3S8Pw2jq4tHBXttQcKxkhkHxmsEWldVutOYNACXujckeuM47_Rsr3B55CL2w.X20VnA.tn3J-Uez4g5x02VAdAyvqOSb6o4'}


def test2(s=None):
    URL = 'http://localhost:5000/api/login'
    params = json.dumps({'email': 'test1@localhost.ru', 'password': 'Pa$$w0rd'})
    from config import Config
    #params = json.dumps({'email': Config.BANK_EMAIL, 'password': Config.BANK_PASS})
    headers = {'Content-Type': 'application/json'}

    if s is None:
        s = requests.Session()
        r = s.post(url=URL, data=params, headers=headers)#, cookies=cookie)
    else:
        r = s.post(url=URL, data=params, headers=headers)

    print(r.status_code)
    print(r.headers)
    print(r.content)
    print(r.cookies.get_dict())
    return s

def test3(s=None):
    URL = 'http://localhost:5000/api/wallet'
    headers = {'Content-Type': 'application/json'}
    if s is None:
        s = requests.Session()
        r = s.get(url=URL, headers=headers, cookies=cookie)
    else:
        r = s.get(url=URL, headers=headers)
    print(r.status_code)
    print(r.headers)
    print(r.content)
    print(r.cookies.get_dict())
    return s

def test4(s):
    URL = 'http://localhost:5000/api/external_to_wallet'
    headers = {'Content-Type': 'application/json'}
    params = json.dumps({'wallet_id': 2, 'amount': 10.0, 'details': 'Перевод из Тинькофф'})
    r = s.post(url=URL, data=params, headers=headers)
    print(r.status_code)
    print(r.headers)
    print(r.content)
    print(r.cookies.get_dict())

def test5(s):
    URL = 'http://localhost:5000/api/wallet_to_wallet'
    headers = {'Content-Type': 'application/json'}
    params = json.dumps({'wallet_id': 2, 'amount': 1.0})
    r = s.post(url=URL, data=params, headers=headers)
    print(r.status_code)
    print(r.headers)
    print(r.content)
    print(r.cookies.get_dict())



#test1()

#s = test1()
#s = test2(s)

#s = test2()
#s = test3(s)

#test3()

#auth, ext2w
#s = test2()
#test4(s)

#auth, w2w
s = test2()
test5(s)