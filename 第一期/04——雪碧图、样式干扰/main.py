# -*- coding: utf-8 -*-
"""
# @项目名称 :yuanrenxue_roblem_solving
# @文件名称 :main.py
# @作者名称 :sxzhang1
# @日期时间 : 2025/6/13 09:33
# @文件介绍 :
"""
import re

import execjs
import requests
from lxml import html

number_dict = {1214: '0', 490: '1', 1022: '2', 1138: '3', 774: '4', 914: '5', 1290: '6', 806: '7', 1334: '8', 1258: '9'}
cookies = {
    'Hm_lvt_434c501fe98c1a8ec74b813751d4e3e3': '1749526096,1749538037,1749540164,1749609599',
    'no-alert3': 'true',
    'm': 'ae82075ee0147956ca3cce82a5ac5940|1749708765000',
    'sessionid': 'jwxet0idmq3dlrncz0qaep5g15hupbvw',
    'tk': '-9006859064502646364',
}

headers = {
    'accept': 'application/json, text/javascript, */*; q=0.01',
    'accept-language': 'zh,zh-CN;q=0.9',
    'cache-control': 'no-cache',
    'pragma': 'no-cache',
    'priority': 'u=0, i',
    'referer': 'https://match.yuanrenxue.cn/match/4',
    'sec-ch-ua': '"Google Chrome";v="135", "Not-A.Brand";v="8", "Chromium";v="135"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36',
    'x-requested-with': 'XMLHttpRequest',
    # 'cookie': 'Hm_lvt_434c501fe98c1a8ec74b813751d4e3e3=1749526096,1749538037,1749540164,1749609599; no-alert3=true; m=ae82075ee0147956ca3cce82a5ac5940|1749708765000; sessionid=jwxet0idmq3dlrncz0qaep5g15hupbvw; tk=-9006859064502646364',
}
with open('files/decode.js', 'r', encoding='utf-8') as f:
    encrypt = f.read()
    cookie_m = execjs.compile(encrypt)
num_total = 0
for i in range(1, 6):
    params = {'page': i}
    response = requests.get('https://match.yuanrenxue.cn/api/match/4', params=params, cookies=cookies, headers=headers)
    data = response.json()
    md5 = cookie_m.call('hex_md5', f"{data.get('key')}{data.get('value')}")
    print(f"正在请求第{i}页，m值为：{md5}")
    tb_list = html.fromstring(data.get("info")).xpath('td')
    for tl in tb_list:
        num_list = []
        img_src_list = tl.xpath(f'img[not(contains(@class, "{md5}"))]')
        for isl in img_src_list:
            num_list.append({
                "style": float(re.findall("-?\\d+\\.\\d+|-?\\d+", isl.xpath('@style')[0])[0]),
                "num": number_dict.get(len(isl.xpath('@src')[0]))
            })
        [d.update({'style': 11 * i + d.get('style', 0)}) for i, d in enumerate(num_list)]
        num_list = list(sorted(num_list, key=lambda x: x['style']))
        num_total +=int(''.join([i['num'] for i in num_list]))
print(num_total)
