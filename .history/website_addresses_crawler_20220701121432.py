# -*- coding:utf-8 -*-
# get addresses on the website
# author: Matthew
# date: 07/01/2022

import re
import random

from click import option
from numpy import single
from py import process
import requests
import time
from bs4 import BeautifulSoup
from selenium import webdriver
import selenium.common.exceptions as Exceptions
import os
import re
import selenium.common.exceptions as sexception
from selenium.webdriver.common.by import By
from lxml import etree
import json
import multiprocessing

url = "https://privatekeyfinder.io/brainwallet" # root url1


def get_all_Coin_name_dict(url, xpath):
    """根据指定的xpath爬取所有可能的虚拟货币名称以及对应的url。返回一个`dict`"""
    driver = webdriver.Chrome()
    driver.get(url)
    name_list = driver.find_elements(by = By.XPATH, value = xpath)
    name_list = [name.get_attribute("href") for name in name_list]
    print(name_list)
    print(name_list[0].split('/')[-2])
    name_dict = {name.split('/')[-2] : name for name in name_list}
    driver.close()
    with open("./results/coin_dict.json", 'w', encoding = 'utf-8', errors = 'ignore') as fout:
        dict_json = json.dumps(name_dict, sort_keys = False, indent = 4, separators = (",", ": "))
        fout.write(dict_json)
    
def multi_crawl():
    """多线程爬取网页"""
    with open("./results/coin_dict.json", 'r', encoding = "utf-8", errors = 'ignore') as fin:
        url_dict = json.load(fin)
    print(url_dict)
    url_name_list = list(url_dict.keys())
    for url_name in url_name_list:
        if not os.path.exists("./results/" + url_name):
            os.mkdir("./results/" + url_name)

    process_cnt = 3
    num_batches = len(url_name_list) // process_cnt
    if num_batches * process_cnt < len(url_name_list):
        num_batches += 1
    for i in range(num_batches):
        process_list = []
        tmp_list = url_name_list[i * process_cnt : (i + 1) * process_cnt]
        for url_name in tmp_list:
            process_list.append(multiprocessing.Process(
                target = single_crawl, args = (url_name, url_dict[url_name])))

        for _, p_i in enumerate(process_list):
            p_i.start()
        for _, p_i in enumerate(process_list):
            p_i.join()


def single_crawl(name, url):
    max_page_xpath = "/html/body/div[1]/div/div[3]/div/div/div[2]/div/div/div[3]/ul/li[5]/a"
    driver = webdriver.Chrome()
    driver.get(url)
    max_page_tag = driver.find_element(by = By.XPATH, value = max_page_xpath)
    max_page = int(max_page_tag.get_attribute("data-ci-pagination-page"))
    driver.close()
    # print(max_page)
    for page in range(1, max_page + 1):
        time.sleep(3)
        crawl_page(coin_name=name, page_url = url + f"?page={page}", page=page)
        time.sleep(1)


def crawl_page(coin_name, page_url, page):
    options = webdriver.ChromeOptions()
    options.add_argument('-ignore-certificate-errors')
    options.add_argument('-ignore -ssl-errors')
    driver = webdriver.Chrome(options = options)
    driver.get(page_url)
    # time.sleep(15)
    # failure = 0
    # while True:
    #     try:
    #         total_balance = driver.find_element(
    #             by=By.XPATH, value = "/html/body/div[1]/div/div[3]/div/div/div[2]/div/div/div[2]/div[2]/span/span[1]")
    #         # print(total_balance.text)
    #         total_balance = float(total_balance.text.strip('\r').strip('\n').strip(' ').split(' ')[-1]) # get value only 
    #         # print(total_balance)
    #         total_received = driver.find_element(by = By.XPATH, value = "/html/body/div[1]/div/div[3]/div/div/div[2]/div/div/div[2]/div[2]/span/span[2]")
    #         total_received = float(total_received.text.strip('\r').strip('\n').strip(' ').split(' ')[-1]) # get value only
    #         total_tx = driver.find_element(by = By.XPATH, value = "/html/body/div[1]/div/div[3]/div/div/div[2]/div/div/div[2]/div[2]/span/span[3]")
    #         total_tx = float(total_tx.text.strip('\r').strip('\n').strip(' ').split(' ')[-1]) # get value only
    #         break
    #     except:
    #         failure += 1
    #         print("loop 1 failed: ", failure)
    #         continue
    # print(total_balance)
    # print(total_received)
    # print(total_tx)
    
    address_types = ["P2PKH(c)", "P2SH(c)", "BECH32(c)", "P2PKH(u)"]
    col3_type = ["balance", "tx", "recv"]
    page_dict = {}
    # page_dict["total balance"] = total_balance
    # page_dict["total received"] = total_received
    # page_dict["total_tx"] = total_tx
    page_dict["tables"] = {}

    tr_list = driver.find_elements(by = By.XPATH, value = "/html/body/div[1]/div/div[3]/div/div/div[2]/div/div/div[4]/table/tbody/tr")
    tr_cnt = len(tr_list)
    PK_span_tags_xpath = "/html/body/div[1]/div/div[3]/div/div/div[2]/div/div/div[4]/table/tbody/tr[{}]/td[1]/div/span[1]"
    PK_xpath = "/html/body/div[1]/div/div[3]/div/div/div[2]/div/div/div[4]/table/tbody/tr[{}]/td[1]/div[{}]/span[2]"
    Passphrase_xpath = "/html/body/div[1]/div/div[3]/div/div/div[2]/div/div/div[4]/table/tbody/tr[{}]/td[1]/div[{}]/strong"
    addr_div_xpath = "/html/body/div[1]/div/div[3]/div/div/div[2]/div/div/div[4]/table/tbody/tr[{}]/td[2]/div" # 这是用来检验是否由div标签，如果有的话那说明存在地址名称，否则就是直接读
    addr_span_names_xpath = "/html/body/div[1]/div/div[3]/div/div/div[2]/div/div/div[4]/table/tbody/tr[{}]/td[2]/div[{}]/span[1]" # 如果上面的xpath没有报异常就运行这个
    addr_span_xpath = "/html/body/div[1]/div/div[3]/div/div/div[2]/div/div/div[4]/table/tbody/tr[{}]/td[2]/div[{}]/span[2]"
    except_addr_span_xpath = "/html/body/div[1]/div/div[3]/div/div/div[2]/div/div/div[4]/table/tbody/tr[{}]/td[2]/span" # 这个是报异常之后调用的
    
    address_xpath = "/html/body/div[1]/div/div[3]/div/div/div[2]/div/div/div[4]/table/tbody/tr[{}]/td[2]/div[{}]/span[2]" # format(tr_i, addr_j)
    address_value_xpath = "/html/body/div[1]/div/div[3]/div/div/div[2]/div/div/div[4]/table/tbody/tr[{}]/td[3]/div[{}]/span[{}]/span" # format(tri, addr_j, col3_k)
    except_address_value_xpath = "/html/body/div[1]/div/div[3]/div/div/div[2]/div/div/div[4]/table/tbody/tr[{}]/td[3]/span[1]/span"
    for i in range(1, tr_cnt + 1):
        row_dict = {} # 每一行构成一个字典
        failure = 0
        # while True:
        #     try:
        span_tags = driver.find_elements(by = By.XPATH, value = PK_span_tags_xpath)
        span_tags = [tag.text for tag in span_tags] # 获得第一列上面所有的PK和passphrase名称
        
        # 优先处理最后一个，因为最后一个一定是passphrase
        passphrase = driver.find_element(by = By.XPATH, value = Passphrase_xpath.format(i, len(span_tags)))
        passphrase = passphrase.text
        row_dict["passphrase"] = passphrase
        # 处理前面的 len(span_tags) - 1个
        for j, pk_name in enumerate(span_tags[:-1]):
            pk = driver.find_element(by = By.XPATH, value = PK_xpath.format(i, j + 1))
            pk = pk.text
            row_dict[pk_name] = pk
        
        row_dict["Addresses"] = {}
        address_dict = {} # 地址构成字典

        try:
            # 表明正常运行
            addr_divs = driver.find_elements(by = By.XPATH, value = addr_div_xpath.format(i))
            addr_types = driver.find_elements(by = By.XPATH, value = addr_span_names_xpath)
            addr_types = [addrtype.text for addrtype in addr_types]
            
        except:
            pass
        
        
        for j, address_type in enumerate(address_types):
            address = driver.find_element(by = By.XPATH, value = address_xpath.format(i, j + 1))
            address = address.text
            address_dict[address_type] = {}
            address_dict[address_type]["address"] = address
            for k, col_type in enumerate(col3_type):
                type_val = driver.find_element(by = By.XPATH, value = address_value_xpath.format(i, j + 1, k + 1))
                type_val = type_val.text
                address_dict[address_type][col_type] = type_val

        row_dict["Addresses"] = address_dict
        page_dict["tables"][str(i)] = row_dict
    
    with open("./results/{}/page_{}.json".format(coin_name, page), 'w', encoding = 'utf-8', errors = 'ignore') as fout:
        dict_json = json.dumps(page_dict, sort_keys = False, indent = 4, separators = (",", ": "))
        fout.write(dict_json)
        
    

if __name__ == "__main__":
    """Program Entrance"""
    # coinname_xpath = "/html/body/div[1]/div/div[3]/div[3]/div/a"
    # get_all_Coin_name_dict(url = url, xpath = coinname_xpath)
    # single_crawl(name = "bitcoin", url = "https://privatekeyfinder.io/brainwallet/bitcoin/") 
    # crawl_page(coin_name = "bitcoin", page_url = "https://privatekeyfinder.io/brainwallet/bitcoin/?page=1", page = 1)
    multi_crawl()
