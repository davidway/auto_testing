# -*- coding: UTF-8 -*-


import json

from model import User
from dao import UserDao

import requests
import time


class UserService:

    def bassCreateUser(self,username,userId):

        user = User.User()

        user.name = username
        user.id = userId

        user = user.__dict__
        # 打印字典
        print(user)
        # 字典转化为json
        userJson = json.dumps(user)

        userDao = UserDao.UserDao
        userDao.baasCreateUser(userJson)

    def findUserInfo(self):
        userDao = UserDao.UserDao
        array =[]
        array = userDao.findUserInfo()
        return array
    def updateUserInfo(userInfo):
        userDao = UserDao.UserDao
        userDao.update(userInfo)
