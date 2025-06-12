# -*- coding: utf-8 -*-
"""
# @项目名称 :猿人学
# @文件名称 :main.py
# @作者名称 :sxzhang1
# @日期时间 : 2025/6/11 11:28
# @文件介绍 :
"""
import time
import execjs
from curl_cffi import requests


def main():
    # 编译并执行 JS
    ctx = execjs.compile(open('files/decode.js', 'r', encoding='utf-8').read())
    dt = int(time.time()) * 1000 + 100000000
    cookies = {}

    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36',
    }
    num_total = num = 0
    for i in range(1, 6):
        m = f'{ctx.call("oo0O0", dt)}丨{dt // 1000}'
        params = {'page': i, 'm': m, }
        print(f"正在请求第{i}页，m值为：{m}")
        url = 'https://match.yuanrenxue.cn/api/match/1'
        response = requests.get(url, params=params, cookies=cookies, headers=headers)
        data = response.json().get('data')
        for item in data:
            num_total += item.get('value')
            num += 1
        time.sleep(1)
    print(num_total // num)


if __name__ == '__main__':
    main()
