# -*- coding: utf-8 -*-
"""
# @项目名称 :yuanrenxue_roblem_solving
# @文件名称 :main.py
# @作者名称 :sxzhang1
# @日期时间 : 2025/6/11 14:04
# @文件介绍 :
"""
import random
import time
from functools import reduce

import execjs
import requests


def main():
    num_total = 0
    for i in range(1, 6):

        with open('files/decode.js', 'r', encoding='utf-8') as f:
            encrypt = f.read()
            cookie_m = execjs.compile(encrypt).call('get_m')
        print(f"正在请求第{i}页，m值为：{cookie_m}")
        headers = {"user-agent": "yuanrenxue,project", }
        cookies = {
            'm': cookie_m,
        }
        url = f"https://match.yuanrenxue.com/api/match/2?page={i}"
        response = requests.get(url, headers=headers, cookies=cookies)
        time.sleep(random.randint(3, 5))
        num_total += sum(item.get('value') for item in response.json()['data'])
    print(num_total)


if __name__ == '__main__':
    main()
