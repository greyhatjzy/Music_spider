import requests
from urllib.request import urlopen, Request
from bs4 import BeautifulSoup
import re
import os
import gzip
import json

'''
测试网页httpbin.org

Attention:
    1.网址中的参数有中文报错，要变成编码形式。e.g. name=周杰伦 --->name=%E5%91%A8%E6%9D%B0%E4%BC%A6
    


'''
url = 'http://tool.liumingye.cn/music/?page=audioPage&type=migu&name=%E5%91%A8%E6%9D%B0%E4%BC%A6'
#url = 'https://www.douban.com/'
# # 获取一个get请求
# response = urlopen(url, timeout=10)
# # (response.read().decode('utf-8'))
# print(response.status)

# 获取一个post请求
# import urllib.parse
#
# data = bytes(urllib.parse.urlencode({'hello': 'world'}), encoding='utf-8')
# response = urlopen(url, data=data)
# print(response.read().decode('utf-8'))

# 增加信息，模拟浏览器
headers = {"Accept": "text/html,application/xhtml+xml,"
                     "application/xml;q=0.9,image/webp,image/apng,"
                     "*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            "Accept-Encoding":" gzip, deflate",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
            "Cache-Control": "max-age=0",
            "Cookie": "UM_distinctid=173b301acfc308-04faef6924753b-3972095d-1fa400-173b301ad004d3; "
                    "myfreemp3_lang=zh-cn; CNZZDATA1277593802=1255473617-1596435498-%7C1596605456",

            "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) "
                                 "Chrome/84.0.4147.105 Safari/537.36"}


req = Request(url=url, headers=headers)
response = urlopen(req)
response_decode=gzip.decompress(response.read()).decode('utf-8')
print(response_decode)

if __name__ == '__main__':
    os.chdir('/home/jzy/Desktop/Scrapy_project')
