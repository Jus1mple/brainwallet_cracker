# -*- coding:utf-8 -*-
# 爬取所有的交易地址以及里面包含的钱包地址
# author: Matthew
# 

import time
import random
import multiprocessing
import asyncio
import requests

api_url = "https://api.blockchain.info/v2/eth/data/transactions/"
page = 0 # 页面编号，从0开始
page_size = 500 # 每页最大数据量，之前测试blocks的时候发现网页最大size只能到500

url = api_url + "?page={}&size=" + str(page_size)

save_path = "./transactions/eth"

headers = {
    "cf-cache-status" : "DYNAMIC",
    "control-type" : "application/json; charset=utf-8",
    "expect-ct": 'max-age=604800, report-uri="https: // report-uri.cloudflare.com/cdn-cgi/beacon/expect-ct"',
    "retry-after" : "48",
    "strict-transport-security" : "max-age=31536000; includeSubDomains; preload",
    "vary" : "Accept-Encoder",
    "x-original-host" : "api.blockchain.info"
    
}

def interval():
    """随机间隔1~3s，防止api接口访问过快把IP给封了"""
    time.sleep(random.randint(1,3))


def single_run(page = 0):
    response = requests.get(url.format(page))
    print(response)


def test():
    single_run(page = 0)


if __name__ == "__main__":
    """Entrance"""
    test()
