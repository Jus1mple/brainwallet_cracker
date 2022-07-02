# -*- coding:utf-8 -*-
# get addresses on the website
# author: Matthew
# date: 07/01/2022

import re
from unittest import result
import random
from numpy import single
import requests
import time
from bs4 import BeautifulSoup
from selenium import webdriver
import selenium.common.exceptions as Exceptions
import os
import re
import selenium.common.exceptions as sexception
from lxml import etree
import json
import multiprocessing

url = "https://privatekeyfinder.io/brainwallet" # root url1


def get_all_Coin_name_dict(url, xpath = ""):
    """根据指定的xpath爬取所有可能的虚拟货币名称以及对应的url。返回一个`dict`"""
    headers = {
        "Accept-Encoding" : "gzip, deflate, br",
        "User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36",
        "Connection" : "Upgrade",
        "Cache-Control" : "no-cache",
        "Host" : "gc.kis.v2.scr.kaspersky-labs.com",
    }
    response = requests.get(url, headers = headers)
    print(response.txt)



if __name__ == "__main__":
    """Program Entrance"""
    get_all_Coin_name_dict(url = url)