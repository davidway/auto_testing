#
import schedule
import requests
import time
from requests_toolbelt.utils import dump
from functools import partial
from itertools import repeat
import time
from multiprocessing import Pool, freeze_support


headers = {

    'Accept': "application/json, text/plain, */*",

    'Content-Type': "application/json;charset=UTF-8"
}
login_cookies={}

#
import schedule
import requests
import time
from requests_toolbelt.utils import dump

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
        else:
            cookies['isvisit'] = '1'
        result = requests.post(url, data=data, headers=headers, cookies=cookies)
        jsonResult = result.json()
        print(jsonResult)
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




def getCardNumber(cookies,card_list_url):

    url = 'https://blockchain.sanyunlian.cn/wsy_blockchain/web/index.php?m=rights&a=getUserCardList'

    data=""
    cookies = cookies
    result = safeRequests(url, data, headers, cookies)
    jsonResult = result.json()
    dataJson = jsonResult['data']
    print(dataJson)
    dataArray=[]
    for each in dataJson:
        dataArray.append(each['card_num'])
    return dataArray

def userQuanyiCard(account, password):
    cookies = login(account, password)
    card_list_url = 'https://blockchain.sanyunlian.cn/wsy_blockchain/web/index.php?m=rights&a=getUserCardList'
    cardNumberArray = getCardNumber(cookies,card_list_url)
    for each in cardNumberArray:

        url = 'https://blockchain.sanyunlian.cn/wsy_blockchain/web/index.php?m=rights&a=receiveIntegral'

        data = {"card_num":""+each+""}
        print(data)

        result = safeRequests(url, data, headers, cookies)

    return result



def job(account, password):
    print(account, "运行开始脚")
    TIMES=10


    tryTimes = 0
    while tryTimes <= TIMES:
        try:
            requests = userQuanyiCard(account, password)
            time.sleep(1)
            break;
        except Exception as e:
            if (tryTimes + 1 == TIMES):
                print(account, "运行异常，需重试", e)
            tryTimes = tryTimes + 1
    print(account, "完成")




def main():
    array = { "15913803153": "tai123456",
             }
    for name, password in array.items():
        with Pool() as pool:
             pool.starmap(job, [(name,password)])


if __name__=="__main__":
    freeze_support()
    main()