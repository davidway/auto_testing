import json


from typing import Any


from typing import Any


class User:
    id=-1
    publicKey=""
    privateKey=""
    configId=""
    bassUserId=""
    bassUserName=""
    address=""

    def __init__(self) -> None:
        super().__init__()

    def __setattr__(self, name: str, value: Any) -> None:
        super().__setattr__(name, value)
    def setAddress(self,address):
        self.address = address
    def getAddress(self):
        return self.address

    def setPrivateKey(self, privateKey):
        self.privateKey = privateKey

    def getPrivateKey(self):
        return self.privateKey

    def setPublicKey(self, publicKey):
        self.publicKey = publicKey

    def getPublicKey(self):
        return self.publicKey

    def setBassUserName(self, bassUserName):
        self.bassUserName = bassUserName

    def getBassUserName(self):
        return self.bassUserName
    def setBassUserId(self, bassUserId):
        self.bassUserId = bassUserId

    def getBassUserId(self):
        return self.getBassUserId

##########################
# 创建MyClass对象
user = User()
# 添加数据c
user.setBassUserName("test")
print(user.getBassUserName())
# 对象转化为字典
user = user.__dict__
# 打印字典
print(user)
# 字典转化为json
userJson = json.dumps(user)
# 打印json数据
print(userJson)

##########################
# json转化为字典
myClassReBuild = json.loads(userJson)
# 打印重建的字典
print(myClassReBuild)
# 新建一个新的MyClass对象
user = User()
# 将字典转化为对象
user.__dict__ = myClassReBuild;
# 打印重建的对象
print(user.getBassUserName())