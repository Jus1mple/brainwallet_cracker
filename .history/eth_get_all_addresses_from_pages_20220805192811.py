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

while True:
    for i, page_path in enumerate(pages):
        with open(page_path, 'r', encoding = 'utf-8', errors = 'ignore') as fin:
            j_dict = json.load(fin)
        trans_dict_list = j_dict["transactions"]
        