# -*- coding: utf-8 -*-
"""
# @项目名称 :yuanrenxue_roblem_solving
# @文件名称 :1.py
# @作者名称 :sxzhang1
# @日期时间 : 2025/6/12 18:03
# @文件介绍 :
"""
import requests

cookies = {
    'Hm_lvt_434c501fe98c1a8ec74b813751d4e3e3': '1749526096,1749538037,1749540164,1749609599',
    'no-alert3': 'true',
    'm': 'ae82075ee0147956ca3cce82a5ac5940|1749708765000',
    'sessionid': 'jwxet0idmq3dlrncz0qaep5g15hupbvw',
    'tk': '-9006859064502646364',
}

headers = {
    'Accept':'*/*',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36',
    'Accept-Encoding': 'gzip, deflate, br, zstd',
    # 'content-length': '0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-ch-ua': '"Google Chrome";v="135", "Not-A.Brand";v="8", "Chromium";v="135"',
    'sec-ch-ua-mobile': '?0',
    'origin': 'https://match.yuanrenxue.cn',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-mode': 'cors',
    'sec-fetch-dest': 'empty',
    'referer': 'https://match.yuanrenxue.cn/match/3',
    'accept-language': 'zh,zh-CN;q=0.9',
    'priority': 'u=0, i',
    'Cookie': '',
}

response = requests.post('https://match.yuanrenxue.cn/jssm', headers=headers)
print(response.cookies)