# -*- coding:utf-8 -*-
# 爬取所有的交易地址以及里面包含的钱包地址
# author: Matthew
# 

import time

api_url = "https://api.blockchain.info/v2/eth/data/transactions/"
page = 0 # 页面编号，从0开始
page_size = 500 # 每页最大数据量，之前测试blocks的时候发现网页最大size只能到500

def interval():
    
