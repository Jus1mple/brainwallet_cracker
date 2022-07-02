# -*- coding:utf-8 -*-
# get addresses on the website
# author: Matthew
# date: 07/01/2022

import re
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
    
def crawl():
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36'}
    max_page=350
    url_terp = 'http://privatekeys.pw/bitcoin/brainwallet/{}'
    if not os.path.exists("./results/bicoin"):
        os.mkdir("./results/bitcoin")
    rows = list()
    for index in range(1,max_page):
        url = url_terp.format(index)
        print(url)
        r = requests.get(url, headers=headers).text
        soup = BeautifulSoup(r,'lxml')
        table = soup.find('table', {'class': 'table table-striped table-hover'})
        trs = table.find_all('tr')[1:]
        for tr in trs:
            row=[td.text.replace('\n', '').replace('\xa0', '').strip() for td in tr.find_all('td')]
            print(row)
            with open("bictoin/private_passphrase.txt", "a") as output:
                output.write("\t".join(row)+"\n")
        time.sleep(5)


if __name__ == "__main__":
    """Program Entrance"""
    # coinname_xpath = "/html/body/div[1]/div/div[3]/div[3]/div/a"
    # get_all_Coin_name_dict(url = url, xpath = coinname_xpath)
    crawl