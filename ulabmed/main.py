import os
import requests as req
from bs4 import BeautifulSoup
from lxml import etree

'''
beautiful soup 和 lxml 

'''


os.chdir(r'D:\Code\Music_spider\ulabmed')

resp = req.get("https://www.ulabmed.com/list-26-1.html#catStart").content
#resp.encoding = 'utf-8'
#soup = BeautifulSoup(resp.text, 'html.parser')

selector = etree.HTML(resp)
items = selector.xpath("/html/body/section/aside/div[3]/ul/li/ul/li")

for x in items:
    print(x[0].attrib)
    print(x[0].text)
    # print(dir(x))

    # break


