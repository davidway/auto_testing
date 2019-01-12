# -*- coding: utf-8 -*-

from appium import webself.driver

desired_caps = {
        'platformName': 'Android',
        'deviceName': 'emulator-5554',
        'platformVersion': '4.2',
        'appPackage': 'com.android.calculator2',
        'appActivity': 'com.android.calculator2.Calculator'
    }
self.driver = webself.driver.Remote('http://127.0.0.1:4723/wd/hub', desired_caps)
self.driver.find_element_by_name('7').click()
self.driver.find_element_by_name('+').click()
self.driver.find_element_by_name('8').click()
self.driver.find_element_by_name('=').click()
