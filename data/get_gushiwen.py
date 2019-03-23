#!/usr/bin/env python3
# -*- coding=utf-8 -*-

# description:
# author:jack
# create_time: 2017/12/30
"""
解析“古诗文”网站的爬虫结果
"""

import json
import re
import logging
import urllib3
import os
import sys
import time
import requests
import traceback
from bs4 import BeautifulSoup
import pymysql
logging.basicConfig(stream=sys.stdout, level=logging.INFO)


# def connect_db():
#     return pymysql.connect(host='10.194.62.48',
#                            port=3306,
#                            user='root',
#                            password='',
#                            database='saiya_test',
#                            charset='')


# def create_gushiwen_table():
#     sql_str = (
#         """
#         DROP TABLE IF EXISTS `bot_shici`;
#         CREATE TABLE `bot_shici` (
#               `id` int unsigned NOT NULL AUTO_INCREMENT PRIMARY KEY,
#               `mingju` varchar(256) NOT NULL,
#               `url` varchar(256) NOT NULL,
#               `chuzi` varchar(256) NOT NULL,
#               `text` text NOT NULL,
#               `yiwen` text NOT NULL,
#               `zhushi` text NOT NULL,
#               `shangxi` text NOT NULL,
#               `beijing` text NOT NULL
#         );
#         """)
#     logging.info(sql_str)
#     con = connect_db()
#     cur = con.cursor()
#     cur.execute(sql_str)
#     rows = cur.fetchall()
#     cur.close()
#     con.close()
#     assert len(rows) == 1, 'Fatal error: country_code does not exists!'
#     return rows[0][0]


# def insert_to_db(shici_item):
#     sql_str = (
#         """
#         INSERT INTO bot_shici(mingju, url, chuzi, text, yiwen, zhushi, shangxi, beijing) VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')
#         """ % (
#             shici_item["mingju"].replace("'", "").replace("\n", ""),
#             shici_item["url"].replace("'", "").replace("\n", ""),
#             shici_item["chuzi"].replace("'", "").replace("\n", ""),
#             shici_item["text"].replace("'", "").replace("\n", ""),
#             shici_item["yiwen"].replace("'", "").replace("\n", ""),
#             shici_item["zhushi"].replace("'", "").replace("\n", ""),
#             shici_item["shangxi"].replace("'", "").replace("\n", ""),
#             shici_item["beijing"].replace("'", "").replace("\n", ""))
#        )
#     logging.info(sql_str)
#     con = connect_db()
#     cur = con.cursor()
#     cur.execute(sql_str)
#     rows = cur.fetchall()
#     cur.close()
#     con.close()
#     assert len(rows) == 1, 'Fatal error: country_code does not exists!'
#     return rows[0][0]

def insert(result):
    #####   SET      ######
    dproxy_url = "http://nj03-wise-2www099.nj03.baidu.com:8123/DproxyServer/cmd"
    headers = {
        "Content-Type": "application/json;charset=UTF-8",
        "User-Agent": "not-python"
    }
    body = {
        "cmd": "SET",
        "args": [result['url'], json.dumps(result, ensure_ascii=False)]
    }
    set_response = requests.post(dproxy_url, headers=headers, data=json.dumps(body))
    print(set_response.text)
    #####    CHECK     ######
    # time.sleep(1)
    # body = {
    #     "cmd": "GET",
    #     "args": [result['url']]
    # }
    # get_response = requests.post(dproxy_url, headers=headers, data=json.dumps(body))
    # check_res = json.loads((get_response.text))['res']
    # check_res = json.loads(check_res)
    # print (json.dumps(check_res, ensure_ascii=False))


def handle_file(file_path_list=[]):
    all_urls = list(map(str.strip, open("all_gushiwen_urls", "r").readlines()))
    print (all_urls)
    all_gushiwen_urls_file = open("all_gushiwen_urls", "a+")
    for file_path in file_path_list:
        try:
            soup = BeautifulSoup(open(file_path), "lxml")
        except Exception:
            traceback.print_exc()
        # print (soup.prettify())
        try:
            mingjus = soup.find_all('a', attrs={"style": " float:left;"})
        except Exception:
            traceback.print_exc()
        for a_mingju in mingjus:
            result = {}
            try:
                # print (a_mingju.prettify())
                # print (a_mingju.text)
                result["mingju"] = a_mingju.text
                gushiwen_url = ('https://so.gushiwen.org' + a_mingju['href'])
                gushiwen_html = requests.get(gushiwen_url)
                if gushiwen_url in all_urls:
                    print ("exists url:" + gushiwen_url)
                    continue
                all_urls.append(gushiwen_url)
                all_gushiwen_urls_file.write(gushiwen_url + "\n")
                # print (gushiwen_html.url)
                result["url"] = gushiwen_html.url
                gushiwen_html.encoding = 'utf-8'
                soup = BeautifulSoup(gushiwen_html.text, "lxml")
                # print (soup.prettify())
                time.sleep(3)
                cont_div = soup.find_all('div', attrs={"class": "cont"})[1]
                # print (cont_div.prettify())
                #############################
                title = cont_div.find('h1').text
                # print (title)
                #############################
                chuzi = cont_div.find('p').text
                # print (chuzi)
                result["chuzi"] = chuzi
                #############################
                contson_div = cont_div.find('div', attrs={"class": "contson"})
                # print (contson_div.text)
                result["text"] = contson_div.text.strip()
                #############################
                contyishang_div = soup.find('div', attrs={"class": "contyishang"})
                # print (contyishang_div.find_all('p')[0].text)
                result["yiwen"] = contyishang_div.find_all('p')[0].text.strip()[2:]
                #############################
                # print (contyishang_div.find_all('p')[1].text)
                result["zhushi"] = contyishang_div.find_all('p')[1].text.strip()[2:]
                #############################
                shangxi_div = soup.find_all('div', attrs={"class": "contyishang"})[1]
                # print (shangxi_div.prettify())
                shangxi_text = ""
                for shangxi_p in shangxi_div.find_all('p'):
                    shangxi_text += shangxi_p.text
                # print (shangxi_text)
                shangxi_text = shangxi_text.strip()
                right_dot = (shangxi_text.rfind("。"))
                shangxi_text = shangxi_text[:right_dot + 1]
                result["shangxi"] = shangxi_text
                #############################
                result["beijing"] = ""
                if len(soup.find_all('div', attrs={"class": "contyishang"})) >= 3:
                    shangxi_div = soup.find_all('div', attrs={"class": "contyishang"})[2]
                    # print (shangxi_div.find('p').text)
                    result["beijing"] = shangxi_div.find('p').text.strip()
                #############################
            except AttributeError as e:
                logging.warning(traceback.print_exc())
            except IndexError as e:
                logging.warning(traceback.print_exc())
            except Exception as e:
                logging.warning(traceback.print_exc())
                raise e
            print (json.dumps(result, indent=4, ensure_ascii=False))
            insert(result)
    all_gushiwen_urls_file.close()
    return all_urls


if __name__ == '__main__':
    pwd = os.path.dirname(os.path.realpath(__file__))
    html_dir = os.path.join(pwd, "gushiwen")
    #### parse html ; write to json file #####
    result_json_file = open(os.path.join(pwd, "result.json"), "w+")
    file_path_list = []
    for root, dirs, files in os.walk(html_dir, topdown=False):
        for name in files:
            if not name.endswith("html"):
                continue
            file_path = os.path.join(root, name)
            print(file_path)
            file_path_list.append(file_path)
    handle_file(file_path_list=file_path_list)
