# -*- coding:utf-8 -*-
# author: Matthew
# date: 07/10/2022
# description: 获得以太坊钱包地址的交易信息
import time
import json
url = "http://api.etherscan.io/api?module=account&action=txlist&address={}&startblock=0&endblock=99999999&sort=asc&apikey={}"


page_start = 1
page_end = 130

max_call = 100000


def load_addresses(page_start, page_end, max_count):
    cnt = 0
    for pi in range(page_start, page_end + 1):
        with open("./results/ethereum/page_{}.json".format(pi), 'r', encoding = 'utf-8', errors = 'ignore') as fin:
            


def sleep():
    """API每秒最多请求5次，因此请求5次之后sleep 1.1s作为间隔"""
    time.sleep(1.1)



for i in range(1, max_call + 1):
    
    if i % 5 == 0:
        sleep()
    