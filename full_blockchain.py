#
import schedule
import requests
import time


def safeRequests(url,data,headers,cookies):
    result=""
    tryTimes=0
    while tryTimes<=3:
        try:
            result = requests.post(url,data=data,headers=headers,cookies=cookies)
            return result
        except Exception as e:
            print(e)
            time.sleep(2)
            tryTimes= tryTimes+1

def dig(cookies):
    headers = {
        'Accept': "application/json, text/plain, */*",
        'Content-Type': "application/json;charset=UTF-8"
    }

    for num in range(0, 61):
        idJson = "{\"id\":" + str(num) + "}"
        url = 'https://blockchain.07s04.cn/wsy_blockchain/web/index.php?m=newDigMine&a=recMinerals'
        data = idJson
        headers =headers
        cookies = cookies
        result = safeRequests(url,data,headers,cookies)
        time.sleep(1)

        if result.status_code == 200:
            jsonResult = result.json()



def login(user, password):
    dataJson = "{\"account\":\"" + user + "\",\"password\":\"" + password + "\",\"type\":1,\"lang_id\":\"1\"}"

    headers = {

        'Accept': "application/json, text/plain, */*",

        'Content-Type': "application/json;charset=UTF-8"
    }
    url = 'https://blockchain.07s04.cn/wsy_blockchain/web/index.php?m=user&a=login'
    data = dataJson
    headers = headers
    cookies = ""
    result = safeRequests(url, data, headers, cookies)

    return result.cookies


def qiandao():
    pass


def useTool(cookies):
    headers = {

        'Accept': "application/json, text/plain, */*",

        'Content-Type': "application/json;charset=UTF-8"
    }
    url = 'https://blockchain.07s04.cn/wsy_blockchain/web/index.php?m=newDigMine&a=propLuckDraw'
    data = ""
    headers = headers
    cookies = cookies
    result = safeRequests(url, data, headers, cookies)



def userQianDao(cookies):
    headers = {

        'Accept': "application/json, text/plain, */*",

        'Content-Type': "application/json;charset=UTF-8"
    }
    url = 'https://blockchain.07s04.cn/wsy_blockchain/web/index.php?m=personal&a=userSign'
    data = ""
    headers = headers
    cookies = cookies
    result = safeRequests(url, data, headers, cookies)




def job():
    cookies = login("13929458901", "hefangju0901")
    dig(cookies)
    useTool(cookies)
    userQianDao(cookies)
    print("第二个用户完成", time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), cookies)
    time.sleep(10)

    cookies = login("13790399274", "zzcbygd1")
    dig(cookies)
    useTool(cookies)
    userQianDao(cookies)
    print("第三个用户完成", time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), cookies)
    time.sleep(10)

    cookies = login("18336026137", "a1701010130")
    dig(cookies)
    useTool(cookies)
    userQianDao(cookies)
    print("第四个用户完成", time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), cookies)
    time.sleep(10)

    cookies = login("15913803153", "tai123456")
    dig(cookies)
    useTool(cookies)
    userQianDao(cookies)
    print("第五个用户完成", time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), cookies)
    time.sleep(10)


schedule.every(10).seconds.do(job)

while True:
    schedule.run_pending()
    time.sleep(1)






