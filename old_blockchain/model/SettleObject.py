import json

class SettleObject:
    amount=""
    ownerAccount=""
    userPrivateKey=""
    srcAsset=""

settltObject = SettleObject()
settltObject.amount=1
#转换成json字符串

settltObject = settltObject.__dict__
# 打印字典
print(settltObject)
# 字典转化为json
userJson = json.dumps(settltObject)

print(userJson)