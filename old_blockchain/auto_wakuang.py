#
import schedule
import requests
import time
from functools import partial
from itertools import repeat
import time
from multiprocessing import Pool, freeze_support

headers = {

    'Accept': "application/json, text/plain, */*",

    'Content-Type': "application/json;charset=UTF-8"
}


def safeRequests(url, data, headers, cookies):
    result = ""

    try:
        if (cookies == ""):
            cookies = {}
            cookies['isvisit'] = '1'
        result = requests.post(url, data=data, headers=headers, cookies=cookies)
        jsonResult = result.json()

        if jsonResult['errcode'] == 701:
            raise Exception("该重试了")
    except Exception as e:

        raise e
    return result


def dig(account, password):
    cookies = login(account, password)

    for num in range(0, 61):
        idJson = "{\"id\":" + str(num) + "}"
        url = 'https://blockchain.sanyunlian.cn/wsy_blockchain/web/index.php?m=newDigMine&a=recMinerals'
        data = idJson

        cookies = cookies
        result = safeRequests(url, data, headers, cookies)

        if result.status_code == 200:
            jsonResult = result.json()
    loginOut(cookies)


def login(user, password):
    dataJson = "{\"account\":\"" + user + "\",\"password\":\"" + password + "\",\"type\":1,\"lang_id\":\"1\"}"

    url = 'https://blockchain.sanyunlian.cn/wsy_blockchain/web/index.php?m=user&a=login'
    data = dataJson

    cookies = ""
    result = safeRequests(url, data, headers, cookies)
    time.sleep(2)
    return result.cookies


def loginOut(cookies):
    url = 'https://blockchain.sanyunlian.cn//wsy_blockchain/web/index.php?m=user&a=logOut'
    data = ""
    cookies = cookies
    result = safeRequests(url, data, headers, cookies)
    return result


def useTool(account, password):
    cookies = login(account, password)

    url = 'https://blockchain.sanyunlian.cn//wsy_blockchain/web/index.php?m=newDigMine&a=propLuckDraw'
    data = ""

    cookies = cookies
    result = safeRequests(url, data, headers, cookies)
    loginOut(cookies)
    return result


def userQianDao(account, password):
    cookies = login(account, password)
    url = 'https://blockchain.sanyunlian.cn//wsy_blockchain/web/index.php?m=personal&a=userSign'
    data = ""
    cookies = cookies
    result = safeRequests(url, data, headers, cookies)
    loginOut(cookies)
    return result


def job(account, password):
    print(account, "运行开始脚")
    tryTimes = 0
    TIMES = 10
    while tryTimes <= TIMES:
        try:
            requests = dig(account, password)
            time.sleep(1)
            break;
        except Exception as e:
            if (tryTimes + 1 == TIMES):
                print(account, "运行异常，需重试", e)
            tryTimes = tryTimes + 1
    tryTimes = 0
    while tryTimes <= TIMES:
        try:
            requests = useTool(account, password)
            time.sleep(1)
            break;
        except Exception as e:
            if (tryTimes + 1 == TIMES):
                print(account, "运行异常，需重试", e)
            tryTimes = tryTimes + 1
    tryTimes = 0
    while tryTimes <= TIMES:
        try:
            requests = userQianDao(account, password)
            time.sleep(1)
            break;
        except Exception as e:
            if (tryTimes + 1 == TIMES):
                print(account, "运行异常，需重试", e)
            tryTimes = tryTimes + 1
    print(account, "完成")






def main():
    array = {'13790399274': "zzcbygd1", '18336026137': "a1701010130", "15913803153": "tai123456",
             "13676247140": "888888zjh", "15016885067": "ps9292ps", "13751386481": "qazwsx123456",
             "13929458901": "hefangju0901", "18319016923": "zhang169233", "13539739236": "love120834064",
             "13560848705": "WH900808"}
    print("hello world")
    for name, password in array.items():
        with Pool() as pool:
             pool.starmap(job, [(name,password)])


if __name__=="__main__":
    freeze_support()
    main()