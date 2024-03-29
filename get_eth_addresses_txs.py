# -*- coding:utf-8 -*-
# author: Matthew
# date: 07/10/2022
# description: 获得以太坊钱包地址的交易信息
import time
import json
import requests
import urllib
import os

url = "http://api.etherscan.io/api?module=account&action=txlist&address={}&startblock=0&endblock=99999999999999&sort=asc&apikey={}"
api_key_token = "8U69T2ZH46C994T7G1YTDE6SH51BAG3447"

page_start = 130
page_end = 130

max_call = 100000


def load_addresses(page_start, page_end, max_count):
    cnt = 0
    address_dict = {}
    for pi in range(page_start, page_end + 1):
        with open("./results/ethereum/page_{}.json".format(pi), 'r', encoding = 'utf-8', errors = 'ignore') as fin:
            json_dict = json.load(fin)
        table_dict = json_dict["tables"]
        for key in table_dict:
            address_dict[table_dict[key]["Addresses"]["Addresses"]["address"]] = table_dict[key]["passphrase"]
            cnt += 1
            if cnt == max_count:
                return address_dict
    return address_dict


def sleep():
    """API每秒最多请求5次，因此请求5次之后sleep 1.1s作为间隔"""
    time.sleep(1.1)


address_dict = load_addresses(page_start = page_start, page_end = page_end, max_count = max_call)

for i, key in enumerate(list(address_dict.keys())):
    print(key)
    if os.path.exists("./json/ethereum/{}.json".format(key)):
        continue
    response = requests.get(url = url.format(key, api_key_token))
    # print(response.text.strip())
    with open("./json/ethereum/{}.json".format(key), 'w', encoding = 'utf-8', errors = 'ignore') as fout:
        fout.write(response.text.strip())
    if (i + 1) % 5 == 0:
        sleep()
    if (i + 1) % 100 == 0:
        print("Processing: ", i + 1)

