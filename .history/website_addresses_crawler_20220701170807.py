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
    url_name_list = url_dict.keys()
    max_page = -1
    cpu_count = multiprocessing.cpu_count()
    if cpu_count >= len(url_dict):
        process_cnt = len(url_dict)
    else:
        process_cnt = cpu_count
    num_batches = len(url_name_list) // process_cnt
    for i in range(0, num_batches):
        tmp_name_list = url_name_list[i * process_cnt : (i + 1) * process_cnt]


def single_crawl(name, url):
    max_page_xpath = "/html/body/div[1]/div/div[3]/div/div/div[2]/div/div/div[3]/ul/li[5]/a"
    driver = webdriver.Chrome()
    driver.get(url)
    max_page_tag = driver.find_element(by = By.XPATH, value = max_page_xpath)
    max_page = int(max_page_tag.get_attribute("data-ci-pagination-page"))
    driver.close()
    # print(max_page)
    for page in range(1, max_page + 1):
        crawl_page(coin_name = name, url = url + f"?page={page}", page = page)
        


def crawl_page(coin_name, page_url, page):
    options = webdriver.ChromeOptions()
    options.add_argument('-ignore-certificate-errors')
    options.add_argument('-ignore -ssl-errors')
    driver = webdriver.Chrome(options = options)
    driver.get(page_url)
    # time.sleep(15)
    while True:
        try:
            total_balance = driver.find_element(
                by=By.XPATH, value = "/html/body/div[1]/div/div[3]/div/div/div[2]/div/div/div[2]/div[2]/span/span[1]")
            # print(total_balance.text)
            total_balance = float(total_balance.text.strip('\r').strip('\n').strip(' ').split(' ')[-1]) # get value only 
            # print(total_balance)
            total_received = driver.find_element(by = By.XPATH, value = "/html/body/div[1]/div/div[3]/div/div/div[2]/div/div/div[2]/div[2]/span/span[2]")
            total_received = float(total_received.text.strip('\r').strip('\n').strip(' ').split(' ')[-1]) # get value only
            total_tx = driver.find_element(by = By.XPATH, value = "/html/body/div[1]/div/div[3]/div/div/div[2]/div/div/div[2]/div[2]/span/span[3]")
            total_tx = float(total_tx.text.strip('\r').strip('\n').strip(' ').split(' ')[-1]) # get value only
            break
        except:
            continue
    print(total_balance)
    print(total_received)
    print(total_tx)
    address_types = ["P2PKH(c)", "P2SH(c)", "BECH32(c)", "P2PKH(u)"]
    col3_type = ["balance", "tx", "recv"]
    page_dict = {}
    page_dict["total balance"] = total_balance
    page_dict["total received"] = total_received
    page_dict["total_tx"] = total_tx
    page_dict["tables"] = {}
    brainwallet_dict = {}
    tr_list = driver.find_elements(by = By.XPATH, value = "/html/body/div[1]/div/div[3]/div/div/div[2]/div/div/div[4]/table/tbody/tr")
    tr_cnt = len(tr_list)
    HEX_xpath = "/html/body/div[1]/div/div[3]/div/div/div[2]/div/div/div[4]/table/tbody/tr{}/td[1]/div[1]/span[2]/a"
    WIFc_xpath = "/html/body/div[1]/div/div[3]/div/div/div[2]/div/div/div[4]/table/tbody/tr{}/td[1]/div[2]/span[2]"
    WIFu_xpath = "/html/body/div[1]/div/div[3]/div/div/div[2]/div/div/div[4]/table/tbody/tr{}/td[1]/div[3]/span[2]"
    Passphrase_xpath = "/html/body/div[1]/div/div[3]/div/div/div[2]/div/div/div[4]/table/tbody/tr{}/td[1]/div[4]/strong"
    address_xpath = "/html/body/div[1]/div/div[3]/div/div/div[2]/div/div/div[4]/table/tbody/tr{}/td[2]/div{}/span[2]" # format(tr_i, addr_j)
    address_value_xpath = "/html/body/div[1]/div/div[3]/div/div/div[2]/div/div/div[4]/table/tbody/tr{}/td[3]/div{}/span{}/span" # format(tri, addr_j, col3_k)

    for i in range(1, tr_cnt + 1):
        row_dict = {} # 每一行构成一个字典
        hex = driver.find_element(by = By.XPATH, value = HEX_xpath.format(i))
        hex = hex.text
        wifc = driver.find_element(by = By.XPATH, value = WIFc_xpath.format(i))
        wifc = wifc.text
        wifu = driver.find_element(by = By.XPATH, value = WIFu_xpath.format(i))
        wifu = wifu.text
        passphrase = driver.find_element(by = By.XPATH, value = Passphrase_xpath.format(i))
        passphrase = passphrase.text
        row_dict["HEX"] = hex
        row_dict["WIF(c)"] = wifc
        row_dict["WIF(u)"] = wifu
        row_dict["passphrase"] = passphrase
        row_dict["Addresses"] = {}
        address_dict = {} # 地址构成字典
        for j, address_type in enumerate(address_types):
            address = driver.find_element(by = By.XPATH, value = address_xpath.format(i, j))
            address = address.text
            address_dict[address_type] = {}
            address_dict[address_type]["address"] = address
            for k, col_type in enumerate(col3_type):
                type_val = driver.find_element(by = By.XPATH, value = address_value_xpath.format(i, j, k))
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
    # crawl_page(coin_name = "bitcoin", page_url = "https://privatekeyfinder.io/brainwallet/bitcoin/?page=1")
