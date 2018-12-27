#
import schedule
import requests
import time

host = "https://blockchain.07s04.cn"
headers = {
    'Accept': "application/json, text/plain, */*",
    'Content-Type': "application/json;charset=UTF-8",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36 OPR/56.0.3051.52"
}
def safeRequests(url, data, headers, cookies):
    result = ""
    tryTimes = 0
    while tryTimes <= 5:
        try:
            result = requests.post(url, data=data, headers=headers, cookies=cookies)
            print(result.json())

            return result
        except Exception as e:
            print(e)
            tryTimes = tryTimes + 1


def dig(account,password):
    cookies = login(account, password)


    for num in range(0, 61):
        idJson = "{\"id\":" + str(num) + "}"
        url = host+"/wsy_blockchain/web/index.php?m=newDigMine&a=recMinerals'"
        data = idJson

        cookies = cookies
        result = safeRequests(url, data, headers, cookies)

        if result.status_code == 200:
            jsonResult = result.json()


def login(user, password):
    dataJson = "{\"account\":\"" + user + "\",\"password\":\"" + password + "\",\"type\":1,\"lang_id\":\"1\"}"

    headers = {

        'Accept': "application/json, text/plain, */*",

        'Content-Type': "application/json;charset=UTF-8"
    }
    url = host+'/wsy_blockchain/web/index.php?m=user&a=login'
    data = dataJson

    cookies = ""
    result = safeRequests(url, data, headers, cookies)

    return result.cookies


def qiandao():
    pass


def useTool(account,password):
    cookies = login(account, password)

    url = host+'/wsy_blockchain/web/index.php?m=newDigMine&a=propLuckDraw'
    data = ""

    cookies = cookies
    result = safeRequests(url, data, headers, cookies)


def userQianDao(account,password):
    cookies = login(account, password)

    url = host+'/wsy_blockchain/web/index.php?m=personal&a=userSign'
    data = ""

    cookies = cookies
    result = safeRequests(url, data, headers, cookies)


def job(account,password):

    dig(account,password)
    useTool(account,password)
    userQianDao(account,password)

    time.sleep(5)

array = {'13790399274': "zzcbygd1","13751386481":"qazwsx123456",'18336026137': "a1701010130","15913803153":"tai123456","13676247140":"888888zjh","15016885067":"ps9292ps"}


for name,password in array.items():
    job(name,password)
    time.sleep(6)