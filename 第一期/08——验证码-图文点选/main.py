# -*- coding: utf-8 -*-
"""
# @项目名称 :yuanrenxue_roblem_solving
# @文件名称 :main.py
# @作者名称 :sxzhang1
# @日期时间 : 2025/6/24 13:49
# @文件介绍 :
"""
import base64
from collections import Counter

import cv2
import numpy as np
from PIL import Image, ImageFont, ImageDraw
import imagehash
from curl_cffi import requests
from lxml import html


class ClickSelect:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'accept': 'application/json, text/javascript, */*; q=0.01',
            'accept-language': 'zh,zh-CN;q=0.9',
            'cache-control': 'no-cache',
            'pragma': 'no-cache',
            'priority': 'u=0, i',
            'referer': 'https://match.yuanrenxue.cn/match/8',
            'sec-ch-ua': '"Google Chrome";v="135", "Not-A.Brand";v="8", "Chromium";v="135"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36',
            'x-requested-with': 'XMLHttpRequest',
        })
        self.session.cookies.update({
            'sessionid': 'jwxet0idmq3dlrncz0qaep5g15hupbvw',
            'qpfccr': 'true',
            'no-alert3': 'true',
        }

        )
        # 九宫典型位置
        self.block_list = [159, 169, 179, 459, 469, 479, 759, 769, 779]

    def get_verify(self):
        """
        获取提示词和点选图片
        :return:
        """
        response = self.session.get('https://match.yuanrenxue.cn/api/match/8_verify')
        if response.status_code == 200:
            h = html.fromstring(response.json().get("html"))
            tip = h.xpath('//div/p/text()')
            img = h.xpath('//div/img/@src')[0].replace('data:image/jpeg;base64,', '')
            # with open("files/img/original_image.jpg", "wb") as f:
            #     f.write(base64.b64decode(img))
            print("提示词为：", tip)
            return tip, base64.b64decode(img)

    @staticmethod
    def write_img(img):
        """
        保存cv2结构图片
        :param img:
        :return:
        """

        # # 保存为图片文件
        cv2.imwrite("files/img/deal_image2.jpg", img)

    # 超过10 个点跨域才算干扰处理，避免字体相同颜色噪点导致文字消失
    @staticmethod
    def noise_line(imgarray, color):
        """
        干扰线判断
        :param imgarray:
        :param color:
        :return:
        """
        c = 0
        row, col = imgarray.shape[:2]
        for u in range(row):
            for v in range(col):
                if (imgarray[u, v] == color).all():
                    c += 1
        return c > 10

    def deal_img(self, img):
        """

        :param img:
        :return:
        """
        img_cv = cv2.imdecode(np.frombuffer(img, np.uint8), cv2.IMREAD_COLOR)
        img_counter = Counter([tuple(i) for i in img_cv.reshape(-1, 3)]).most_common()
        for j in img_counter:
            if j[1] > 3000 or j[1] < 100:
                img_cv[np.all(img_cv == j[0], axis=-1)] = (0, 0, 0)
            elif (self.noise_line(img_cv[:, :15, :], j[0]) or
                  self.noise_line(img_cv[:, 105:120, :], j[0]) or
                  self.noise_line(img_cv[:, 205:220, :], j[0]) or
                  self.noise_line(img_cv[:9, :, :], j[0]) or
                  self.noise_line(img_cv[95:105, :, :], j[0]) or
                  self.noise_line(img_cv[195:205, :, :], j[0])):
                # img_cv[np.all(img_cv == j[0], axis=-1)] = (120, 120, 120)
                img_cv[np.all(img_cv == j[0], axis=-1)] = (0, 255, 0)
            else:
                img_cv[np.all(img_cv == j[0], axis=-1)] = (255, 255, 255)
        return img_cv

    @staticmethod
    def extract_white_text(img):
        # 转为灰度图
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # 提取白色文字（设定阈值）
        _, binary = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY)

        # 形态学操作增强文字结构
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 2))
        cleaned = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, kernel)

        return cleaned

    # Step 2: 提取绿色干扰线掩膜（HSV颜色空间）
    @staticmethod
    def extract_green_mask(img):
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

        # 绿色 HSV 范围
        lower_green = np.array([40, 40, 40])
        upper_green = np.array([80, 255, 255])

        mask = cv2.inRange(hsv, lower_green, upper_green)
        return mask

    # Step 3: 分析干扰线周围像素，决定用黑色还是白色填充
    @staticmethod
    def repair_interference_lines(img, green_mask):
        repaired = img.copy()
        h, w = img.shape[:2]

        for y in range(h):
            for x in range(w):
                if green_mask[y, x] == 255:
                    roi = img[max(0, y - 2):y + 3, max(0, x - 2):x + 3]
                    gray_roi = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)

                    # 统计周围像素中白色和黑色的比例
                    white_pixels = np.sum(gray_roi > 200)
                    black_pixels = np.sum(gray_roi < 50)

                    total_pixels = roi.size // 3

                    white_ratio = white_pixels / total_pixels
                    black_ratio = black_pixels / total_pixels

                    # 如果周围是白色为主，则填充白色；否则填充黑色
                    if white_ratio > black_ratio:
                        repaired[y, x] = [255, 255, 255]  # 白色
                    else:
                        repaired[y, x] = [0, 0, 0]  # 黑色
        return repaired

    # Step 3: 增强白色文字结构（闭运算连接断开的笔画）
    @staticmethod
    def enhance_white_text(repaired_img):
        """
        修复字体
        :param repaired_img:
        :return:
        """
        gray = cv2.cvtColor(repaired_img, cv2.COLOR_BGR2GRAY)

        # 二值化处理
        _, binary = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY)

        # 形态学闭运算增强连通性
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 2))
        cleaned = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, kernel)

        return cleaned

    @staticmethod
    def structuring_element(img):
        """
        字体字形修复
        :param img:
        :return:
        """
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
        # 闭运算：先膨胀后腐蚀 → 填补文字内部空洞
        img_cv = cv2.morphologyEx(img, cv2.MORPH_CLOSE, kernel)
        img_cv = cv2.medianBlur(img_cv, 1)  # 中值滤波去噪
        img_cv = cv2.dilate(img_cv, kernel, iterations=1)
        return img_cv

    def split_image_into_3x3(self, img):
        """
        将图像切割为 3x3 网格
        :return:
        """
        # Step 2: 确保图像可被均分
        tile_h = img.shape[:2][0] // 3
        tile_w = img.shape[:2][1] // 3
        img_list = []
        # Step 3: 切割图像并保存
        for i in range(3):
            for j in range(3):
                x_start = j * tile_w
                y_start = i * tile_h
                tile = img[y_start:y_start + tile_h, x_start:x_start + tile_w]
                self.set_left_right_black(tile)
                img_list.append(tile)
                # cv2.imwrite(f"files/img/{i * 3 + j + 1}.png", tile)
        return img_list

    # Step 4: 去除左侧白边
    @staticmethod
    def set_left_right_black(img):
        """
        将图像左侧 20 像素设置为黑色
        :param img:
        :return:
        """
        # 确保图像宽度大于 0
        _, w = img.shape[:2]
        img[:, :20] = 0
        img[:, w - 3:] = 0

        return img

    # 创建空白图像（RGB）
    @staticmethod
    def create_text_image(text="汉"):
        """
        字体转图片
        :param text:
        :return:
        """
        # 创建黑色背景图像
        img = Image.new('RGB', (100, 100), color=(0, 0, 0))

        # 加载字体文件（支持中文）
        font = ImageFont.truetype("msyhbd.ttc", 80)

        # 获取绘制对象
        draw = ImageDraw.Draw(img)

        # 获取文字包围框
        text_bbox = font.getbbox(text)

        # 靠右对齐 + 垂直居中
        x = 100 - text_bbox[2] - text_bbox[0] + 5
        y = (100 - text_bbox[3] - text_bbox[1]) // 2

        # 绘制文字
        draw.text((x, y), text, fill=(255, 255, 255), font=font)
        return img

    @staticmethod
    def phash_similarity(img1, img2):
        hash1 = imagehash.phash(img1)
        hash2 = imagehash.phash(Image.fromarray(img2))
        return abs(hash1 - hash2)  # 差值越小越相似

    def get_verify_site(self):
        tip, img = self.get_verify()
        # Step 1: 预处理图片，处理字体、背景、干扰线颜色
        img = self.deal_img(img)
        # Step 2: 提取绿色干扰线掩膜
        green_mask = self.extract_green_mask(img)
        # Step 3: 修复干扰线（替换为黑色/白色）
        img = self.repair_interference_lines(img, green_mask)
        img = self.enhance_white_text(img)
        img = self.structuring_element(img)
        img = self.structuring_element(img)
        img_list = self.split_image_into_3x3(img)
        answer = ""
        for i in tip:
            hash_list = []
            font_img = self.create_text_image(i)
            for im in img_list:
                hash_list.append(self.phash_similarity(font_img, im))
            answer += f"{self.block_list[hash_list.index(min(hash_list))]}|"
        # self.write_img(img)
        return answer

    def run(self):
        digit_counter = Counter()
        for i in range(1, 6):
            print(f"正在取{i}页数据")
            num = 1
            while num <= 10:
                try:
                    answer = self.get_verify_site()
                    print(f"位置数据：{answer}", end=" ")
                    params = {'page': i, 'answer': answer}
                    response = self.session.get('https://match.yuanrenxue.cn/api/match/8', params=params)
                    if response.json().get('status') == '1':
                        print(f"请求成功")
                        data = response.json().get('data')
                        digit_counter.update([d.get('value') for d in data])
                        break
                    else:
                        print(f"请求失败")
                        num += 1
                        continue
                except Exception as e:
                    print(f"位置数据：请求异常，{e.__str__()}")
        print(digit_counter.most_common(1)[0])


if __name__ == '__main__':
    cs = ClickSelect()
    cs.run()
