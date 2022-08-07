# -*- coding:utf-8 -*-
# 解析保存下载的page_{}.json文件，将里面所有交易的钱包地址保存下来

import os

page_folder = "./transactions/eth/pages"
hex_folder = "./transactions/eth/hexes"

pages = os.listdir(page_folder)

curr_cnt = len(pages)