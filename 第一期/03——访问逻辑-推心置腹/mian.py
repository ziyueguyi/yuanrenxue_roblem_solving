# -*- coding: utf-8 -*-
"""
# @项目名称 :yuanrenxue_roblem_solving
# @文件名称 :mian.py
# @作者名称 :sxzhang1
# @日期时间 : 2025/6/12 15:27
# @文件介绍 :
"""
import statistics

from curl_cffi import requests

session = requests.Session()
session.headers.update({  # 设置第一个请求的headers
    'Content-Length': '0',
    'Accept': '*/*',
    'Referer': 'https://match.yuanrenxue.cn/match/3',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Cookie': '',
})
num_list = []
for i in range(1, 6):
    session.post("https://match.yuanrenxue.cn/jssm")
    print(f"正在请求第{i}页，sessionid值为：{session.cookies.get("sessionid")}")
    params = {'page': i}
    response = session.get('https://match.yuanrenxue.cn/api/match/3', params=params)
    data = response.json()
    num_list.extend([item['value'] for item in data['data']])
print(statistics.mode(num_list))

