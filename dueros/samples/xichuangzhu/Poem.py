#!/usr/bin/env python3
# -*- encoding=utf-8 -*-

# description:
# author:jack
# create_time: 2018/1/3

"""
    desc:pass
"""
import os
import json
import random
import requests
import logging
from bs4 import BeautifulSoup


class Poem:
    @staticmethod
    def get_one_poem_item():
        pwd_dir = os.path.dirname(os.path.realpath(__file__))
        for i in range(3):
            pwd_dir = os.path.dirname(pwd_dir)
        all_gushiwen_urls_file = os.path.join(pwd_dir, "data", "all_gushiwen_urls")
        print (all_gushiwen_urls_file)
        all_gushiwen_urls = list(map(str.strip, open(all_gushiwen_urls_file, "r").readlines()))
        retry = 0
        while retry < 3:
            gushiwen_url = random.choice(all_gushiwen_urls)
            dproxy_url = "http://nj03-wise-2www099.nj03.baidu.com:8123/DproxyServer/cmd"
            headers = {
                "Content-Type": "application/json;charset=UTF-8",
                "User-Agent": "not-python"
            }
            body = {
                "cmd": "GET",
                "args": [gushiwen_url]
            }
            get_response = requests.post(dproxy_url, headers=headers, data=json.dumps(body))
            check_res = json.loads((get_response.text))['res']
            check_res = json.loads(check_res)
            # print (json.dumps(check_res, ensure_ascii=False))
            # print (random_index)
            if "《" not in check_res["mingju"]:
                break
        return check_res

    @staticmethod
    def get_one_random_image():
        image_list = [
            "https://timgsa.baidu.com/timg?image&quality=80&size=b9999_10000&sec=1552828152952&di=da0be8771e492d7dbc8459bcbd854ad5&imgtype=0&src=http%3A%2F%2Fimg.zcool.cn%2Fcommunity%2F016886595084f0a8012193a335336d.jpg%401280w_1l_2o_100sh.png",
            "http://img.zcool.cn/community/01cc795b5ac15ea801206a35b3515b.jpg@2o.jpg",
            "http://5b0988e595225.cdn.sohucs.com/images/20171122/6708befb1ac34736a53792d98774d785.jpeg",
            "http://img5.imgtn.bdimg.com/it/u=2720298202,992638099&fm=26&gp=0.jpg",
            "https://ss0.bdstatic.com/70cFvHSh_Q1YnxGkpoWK1HF6hhy/it/u=3483387577,3428143539&fm=26&gp=0.jpg",
            "https://ss1.bdstatic.com/70cFvXSh_Q1YnxGkpoWK1HF6hhy/it/u=3549226233,1582716986&fm=26&gp=0.jpg",
            "https://ss1.bdstatic.com/70cFvXSh_Q1YnxGkpoWK1HF6hhy/it/u=125803029,235641028&fm=26&gp=0.jpg",
            "https://ss3.bdstatic.com/70cFv8Sh_Q1YnxGkpoWK1HF6hhy/it/u=2588515873,1114542188&fm=26&gp=0.jpg",
            "https://ss2.bdstatic.com/70cFvnSh_Q1YnxGkpoWK1HF6hhy/it/u=3527936981,449062371&fm=27&gp=0.jpg",
            "https://ss3.bdstatic.com/70cFv8Sh_Q1YnxGkpoWK1HF6hhy/it/u=127436145,2696757588&fm=27&gp=0.jpg",
            "https://ss1.bdstatic.com/70cFuXSh_Q1YnxGkpoWK1HF6hhy/it/u=2691734441,2072301550&fm=27&gp=0.jpg",
            "https://ss3.bdstatic.com/70cFv8Sh_Q1YnxGkpoWK1HF6hhy/it/u=432880559,38644168&fm=27&gp=0.jpg",
            "https://ss0.bdstatic.com/70cFvHSh_Q1YnxGkpoWK1HF6hhy/it/u=2377221399,1044282759&fm=27&gp=0.jpg"
        ]
        return random.choice(image_list)

    @staticmethod
    def get_see_more(gushiwen_url=""):
        dproxy_url = "http://nj03-wise-2www099.nj03.baidu.com:8123/DproxyServer/cmd"
        headers = {
            "Content-Type": "application/json;charset=UTF-8",
            "User-Agent": "not-python"
        }
        body = {
            "cmd": "GET",
            "args": [gushiwen_url]
        }
        get_response = requests.post(dproxy_url, headers=headers, data=json.dumps(body))
        check_res = json.loads((get_response.text))['res']
        check_res = json.loads(check_res)
        return check_res



if __name__ == '__main__':
    Poem.get_see_more(title="静夜思", author="李白")
