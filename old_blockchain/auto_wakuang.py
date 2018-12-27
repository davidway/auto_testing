#
import schedule
import requests
import time
from requests_toolbelt.utils import dump

def safeRequests(url, data, headers, cookies):
    result = ""
    tryTimes = 0
    while tryTimes <= 5:
        try:
            result = requests.post(url, data=data, headers=headers,cookies=cookies)


            data = dump.dump_all(result)
            print(data.decode('utf-8'))
            return result
        except Exception as e:
            print(e)
            tryTimes = tryTimes + 1



def dig(account, password):
    cookies = login(account, password)
    headers = {
        'Accept': "application/json, text/plain, */*",
        'Content-Type': "application/json;charset=UTF-8"
    }

    for num in range(0, 61):
        idJson = "{\"id\":" + str(num) + "}"
        url = 'https://blockchain.sanyunlian.cn/wsy_blockchain/web/index.php?m=newDigMine&a=recMinerals'
        data = idJson
        headers = headers
        cookies = cookies
        result = safeRequests(url, data, headers, cookies)

        if result.status_code == 200:
            jsonResult = result.json()
    return result

def login(user, password):
    dataJson = "{\"account\":\"" + user + "\",\"password\":\"" + password + "\",\"type\":1,\"lang_id\":\"1\"}"

    headers = {

        'Accept': "application/json, text/plain, */*",

        'Content-Type': "application/json;charset=UTF-8"
    }
    url = 'https://blockchain.sanyunlian.cn/wsy_blockchain/web/index.php?m=user&a=login'
    data = dataJson
    headers = headers
    cookies = ""
    result = safeRequests(url, data, headers, cookies)

    return result.cookies


def qiandao():
    pass


def useTool(account, password):
    cookies = login(account, password)
    headers = {

        'Accept': "application/json, text/plain, */*",

        'Content-Type': "application/json;charset=UTF-8"
    }
    url = 'https://blockchain.sanyunlian.cn//wsy_blockchain/web/index.php?m=newDigMine&a=propLuckDraw'
    data = ""
    headers = headers
    cookies = cookies
    result = safeRequests(url, data, headers, cookies)


def userQianDao(account, password):
    cookies = login(account, password)
    headers = {

        'Accept': "application/json, text/plain, */*",

        'Content-Type': "application/json;charset=UTF-8"
    }
    url = 'https://blockchain.sanyunlian.cn//wsy_blockchain/web/index.php?m=personal&a=userSign'
    data = ""
    headers = headers
    cookies = cookies
    result = safeRequests(url, data, headers, cookies)
def clearCookies(requests):
    requests.cookies.clear()

def job(account, password):
    requests = dig(account, password)
    clearCookies(requests)
    useTool(account, password)
    userQianDao(account, password)

    time.sleep(5)


array = {'13790399274': "zzcbygd1", '18336026137': "a1701010130", "15913803153": "tai123456",
         "13676247140": "888888zjh", "15016885067": "ps9292ps"}

for name, password in array.items():
    job(name, password)
