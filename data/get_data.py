#!/usr/bin/env python3
# -*- coding=utf-8 -*-

# description:
# author:jack
# create_time: 2017/12/30
"""
解析“西窗烛”网站的爬虫结果
"""

import json
import re
import logging
import urllib3
import os
import requests
from bs4 import BeautifulSoup


def handle_file(file_path=""):
    results = []
    try:
        soup = BeautifulSoup(open(file_path), "lxml")
        for work_item_div in soup.find_all('div', attrs={"class": "work-item"}):
            result = {}
            for work_header_div in work_item_div.find_all('div', attrs={"class": "work-header"}):
                for work_type_a in work_header_div.find_all('a', attrs={"class": "work-type"}):
                    result["work_type"] = work_type_a.text.strip()
                for work_title_a in work_header_div.find_all('a', attrs={"class": "work-title"}):
                    result["work_title"] = work_title_a.text.strip()
                for work_author_sup in work_header_div.find_all('sup', attrs={"class": "work-author"}):
                    result["work_author"] = work_author_sup.text.strip()

            for work_content_div in work_item_div.find_all('div', attrs={"class": "work-content"}):
                result["work_content"] = work_content_div.text.strip()
            print (json.dumps(result, indent=4, ensure_ascii=False))
            hanyu_url = "https://hanyu.baidu.com/s?"
            payload = {
                'wd': result["work_title"].replace(" · ", " "),
                'from': 'poem'
            }
            hanyu_html = requests.get(hanyu_url, params=payload)
            print (hanyu_html.url)
            hanyu_html.encoding = 'utf-8'
            soup = BeautifulSoup(hanyu_html.text, "lxml")
            # print (soup.prettify())
            try:
                poem_detail_body_div = soup.find('div', attrs={"class": "poem-detail-body"})
                print (poem_detail_body_div.prettify())
                poem_gray = poem_detail_body_div.find('span', attrs={"class": "poem-detail-header-author"})
                result["poem_gray"] = poem_gray.text.strip()
                poem_main_text = ""
                for temp in poem_detail_body_div.find_all('p', attrs={"class": "poem-detail-main-text", "id": "body_p"}):
                    poem_main_text += temp.text.strip()
                result["poem_main_text"] = poem_main_text
                poem_main_text_means = ""
                for temp in poem_detail_body_div.find_all('p', attrs={"class": "poem-detail-main-text", "id": "means_p"}):
                    poem_main_text_means += temp.text.strip()
                result["poem_main_text_means"] = poem_main_text_means
            except Exception as e:
                logging.warning(hanyu_html.url)
                logging.warning(str(e))
            print (json.dumps(result, indent=4, ensure_ascii=False))
            results.append(result)
            # result_json_file.write(json.dumps(result, ensure_ascii=False) + "\n")
    except Exception as e:
        print (e)
    return results


if __name__ == '__main__':
    pwd = os.path.dirname(os.path.realpath(__file__))
    html_dir = os.path.join(pwd, "html")
    #### parse html ; write to json file #####
    result_json_file = open(os.path.join(pwd, "result.json"), "w+")
    results = []
    for root, dirs, files in os.walk(html_dir, topdown=False):
        for name in files[:1]:
            if not name.endswith("result"):
                continue
            file_path = os.path.join(root, name)
            # print(file_path)
            temp_results = handle_file(file_path=file_path)
            results.extend(temp_results)
    # print (json.dumps(results, indent=4, ensure_ascii=False))
    result_json_file.write(json.dumps(results, indent=4, ensure_ascii=False))
    result_json_file.close()
    ##### get result from json file #####
    # result_json_file = open(os.path.join(pwd, "result.json"), "r")
    # results = json.load(result_json_file)
    # print (results)
