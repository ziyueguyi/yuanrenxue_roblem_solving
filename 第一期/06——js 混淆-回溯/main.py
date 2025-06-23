# -*- coding: utf-8 -*-
"""
# @项目名称 :yuanrenxue_roblem_solving
# @文件名称 :main.py
# @作者名称 :sxzhang1
# @日期时间 : 2025/6/20 10:07
# @文件介绍 :
"""
import time

import execjs
import requests

cookies = {
    'sessionid': 'jwxet0idmq3dlrncz0qaep5g15hupbvw',
    'RM4hZBv0dDon443M': 'ZkzA9aeAqAp6iu75xpavuYta0JQnLdaO6lnlB3E9GQP81lxqLHBHl3LuBoEcTfFc2chYum2AHCrRdi2L8ILTSI6mSYxImW2yCPESRcHZzCGPH4Qv40s5N5SEH8E0Ufu3IZCk5AEgCEeAfbPzgrvAky9FJ66fvQi6UA+R1jBZxpkRiooAZ1MpaoJkGOyGKnjwRjtvTOCgwCWKBO3+1HnirUcLb3Hi1Z98mDN1SnC5X9U=',
    'no-alert3': 'true',
    'm': '155',
}

headers = {
    'accept': 'application/json, text/javascript, */*; q=0.01',
    'accept-language': 'zh,zh-CN;q=0.9',
    'cache-control': 'no-cache',
    'pragma': 'no-cache',
    'priority': 'u=0, i',
    'referer': 'https://match.yuanrenxue.cn/match/6',
    'sec-ch-ua': '"Google Chrome";v="135", "Not-A.Brand";v="8", "Chromium";v="135"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36',
    'x-requested-with': 'XMLHttpRequest',
}
with open('files/decode.js', 'r', encoding='utf-8') as f:
    encrypt = f.read()
    ras_fun = execjs.compile(encrypt)
total_num = 0
for i in range(1, 6):
    t = int(time.time()) * 1000
    result = ras_fun.call('r', t)
    print(result)
    params = {
        'page': i,
        'm': result,
        'q': f'1-{t}|',
    }
    time.sleep(0.1)
    response = requests.get('https://match.yuanrenxue.cn/api/match/6', params=params, headers=headers)
    print(response.json())
    total_num += sum(item["value"] for item in response.json().get("data"))
print(total_num*24)

