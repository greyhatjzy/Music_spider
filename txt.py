import os
import requests as req
from bs4 import BeautifulSoup

os.chdir(r'D:\temp\新建文件夹')
resp = req.get("http://www.ting89.com/books/1433.html")
resp.encoding = 'gb18030'

print(resp.status_code)
# print(resp.text)
soup = BeautifulSoup(resp.text, 'html.parser')
items = soup.select('.compress li a')
# print(items)
titles = []
download_url = 'http://mp3-f.ting89.com:9090/斗破苍穹/'

def saver(file_name, url):
    file = req.get(url)
    with open(file_name, 'wb') as f:
        f.write(file.content)


for item in items[584:]:
    file_name = item.attrs['title'] + '.mp3'

    url = download_url + file_name
    print(url)

    try:
        saver(file_name, url)
        print('文件保存完成')
    except:
        print('下载失败')

    #break[