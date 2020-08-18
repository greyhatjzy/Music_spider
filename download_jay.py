# coding:utf-8
import requests
from urllib.request import urlopen, Request
import json
headers = {"user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) "
                                 "Chrome/84.0.4147.105 Safari/537.36"}


url = 'https://app.onenine.cc/m/api/search'

response = requests.get(url,headers=headers)

print(response.text)

