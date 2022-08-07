# -*- coding:utf-8 -*-
# 解析保存下载的page_{}.json文件，将里面所有交易的钱包地址保存下来

import os
import time
import json

page_folder = "./transactions/eth/pages"
hex_folder = "./transactions/eth/hexes"

pages = os.listdir(page_folder)
pages = [os.path.join(page_folder, page) for page in pages]
curr_cnt = len(pages)

address_list = set()


while True:
    for i, page_path in enumerate(pages):
        with open(page_path, 'r', encoding = 'utf-8', errors = 'ignore') as fin:
            j_dict = json.load(fin)
        tx_dict_list = j_dict["transactions"]
        for j, tx_dict in enumerate(tx_dict_list):
            from_addr = tx_dict["from"]
            to_addr = tx_dict["to"]
            address_list.add(from_addr)
            address_list.add(to_addr)
    print("sleep")
    time.sleep(10)
    new_pages = os.listdir(page_folder)
    new_cnt = len(new_pages)
    if new_cnt == curr_cnt:
        print("10 seconds no update")
        break
    pages = [os.path.join(page_folder, page) for page in pages[curr_cnt]]
