# -*- coding: utf-8 -*-
"""
# @项目名称 :yuanrenxue_roblem_solving
# @文件名称 :main.py
# @作者名称 :sxzhang1
# @日期时间 : 2025/6/23 16:06
# @文件介绍 :
"""
import base64
import re
import html
from io import BytesIO

import requests
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.ttLib import TTFont

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
    'referer': 'https://match.yuanrenxue.cn/match/7',
    'sec-ch-ua': '"Google Chrome";v="135", "Not-A.Brand";v="8", "Chromium";v="135"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36',
    'x-requested-with': 'XMLHttpRequest',
}
font_num = {
    623: '1', 11863711918420: '3', 1464767009960: '6', 1281870178852: '9', 648370088: '2', 125784729951: '5', 127: '7',
    32767: '4', 96168420882065986: '8', 43144338: '0',
}
num_list = []
for i in range(1, 6):
    params = {'page': i, }

    response = requests.get('https://match.yuanrenxue.cn/api/match/7', params=params, cookies=cookies, headers=headers)
    font = TTFont(BytesIO(base64.b64decode(response.json().get('woff'))))
    # 获取 cmap 表（字符映射表）
    cmap = font['cmap'].getBestCmap()
    font_dict = dict()

    for _, name in list(cmap.items())[:20]:
        # 获取字形对象
        font_dict[name] = font_num.get(
            int(''.join([str(int(bin(flag), 2)) for flag in list(font['glyf'][name].flags)]), 2))
    for item in response.json().get('data'):
        item_list = [cmap.get(ord(html.unescape(i))) for i in re.findall("&#x\\w\\d+", item.get('value'))]
        num_list.append( int(''.join([font_dict.get(i) for i in item_list])))
print(max(num_list))
