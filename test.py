#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@project: dazhongdianping
@file: test.py
@ide: PyCharm
@time: 2020-02-25 21:19:34
@author: Mr.Li
Copyright © 2020—2020 Mr.Li. All rights reserved.
"""
import re    #re库是对字符串进行解析，而lxml文件可以对xml文件进行解析
from lxml import etree
import requests

if __name__ == '__main__':
    with open('E:\桌面/123.html', 'r', encoding='UTF-8') as f:
        html = f.read()
    with open('E:\桌面\“儿童公园”的全部点评 - 广州亲子 - 大众点评网_files/be7628c9102b4236c9d9e1ba6c20645f.css') as f1:
        css_content = f1.read()
    with open('E:\桌面\“儿童公园”的全部点评 - 广州亲子 - 大众点评网_files/03ab6bd09c5ef0e1e1058e47993fb9c2.svg', encoding='UTF-8') as f2:
        svg_html = f2.read()
    '''svg_l = re.search(r'svgmtsi.*?(//s3plus.sankuai.com.*?svg)\);', css_content)
    svg_link = 'http:' + svg_l.group(1)
    svg_html = requests.get(svg_link).text'''
    y_list = re.findall('d="M0 (.*?) H600"', svg_html)    #y_list的元素为str
    font_dic = {}
    j = 0    #j为第j行
    font_size = int(re.findall(r'font-size:(.*?)px;fill:#333;}', svg_html)[0])
    for y in y_list:
        font_l = re.findall(r'<textPath xlink:href="#' + str(j+1) + '" textLength=".*?">(.*?)</textPath>', svg_html)
        font_list = re.findall(r'.{1}', font_l[0])
        for x in range(len(font_list)):    #x为每一行第x个字
            #print(str((x + 1) * font_size) + ',' + y)
            font_dic[str(x * font_size) + ',' + y] = font_list[x]
        j += 1
    '''------上面是获得字体字典的代码-------'''
    '''下面开始解析网页，将svg标签替换成字'''
    font_key_list = re.findall(r'<svgmtsi class="(.*?)"></svgmtsi>', html)
    #print(font_key_list)
    for font_key in font_key_list:
        pos_key = re.findall(r'.' + font_key + '{background:-(.*?).0px -(.*?).0px;}', css_content)
        #print(pos_key[0][1])
        pos_x = pos_key[0][0]
        pos_y_original = pos_key[0][1]
        for y in y_list:
            if int(pos_y_original) < int(y):
                pos_y = y
                break
        html = html.replace('<svgmtsi class="' + font_key + '"></svgmtsi>', font_dic[pos_x + ',' + pos_y])
        #print(pos_x)
        #print('<svgmtsi class="' + font_key + '"></svgmtsi>')
        #html_full_review = html.replace('<svgmtsi class="' + font_key + '"></svgmtsi>', font_dic[pos_x + ',' + pos_y])
        #html_full_review = html.replace('<svgmtsi class="' + font_key + '"></svgmtsi>', 'hhh')

    html_full_review = etree.HTML(html)
    reviews_items = html_full_review.xpath("//div[@class='reviews-items']/ul/li")
    for i in reviews_items:
        #r = i.xpath("./div/div[@class='review-words Hide']")[0].xpath('string(.)').strip()
        r = i.xpath("./div/div[@class='review-words Hide']/text()")
        print(r)
