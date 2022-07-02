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

def get_all_Coin_name_dict(xpath):
    """根据指定的xpath爬取所有可能的虚拟货币名称以及对应的url。返回一个`dict`"""
    