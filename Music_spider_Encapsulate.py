import time, os, datetime, re
from urllib.parse import quote
import json
import requests
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


'''
Downloader作为父类，Rank,Title,Artist 作为子类
在父类里定义的操作
    count
    next page
    

直接链接拼接比较好
歌曲下载计数

子类 输入参数  ：Artist Title Acount OutputDir SearchEngine 


Rank    直接解析QQ或者网易云的链接
Title   +数据库选择
Artist  +数据库选择








'''


class Downloader():

    def __init__(self):
        self.migu = 'http://tool.liumingye.cn/music/?page=audioPage&type=migu&name='
        self.yqd = 'http://tool.liumingye.cn/music/?page=audioPage&type=YQD&name='
        self.yqb = 'http://tool.liumingye.cn/music/?page=audioPage&type=YQB&name='

        # 设置option,不显示浏览器窗口,最大等待5秒
        option = webdriver.ChromeOptions()
        option.add_argument('headless')
        self.driver = webdriver.Chrome(r'D:\Code\Music_spider\driver\chromedriver.exe', options=option)
        self.driver.implicitly_wait(5)

    def _get_info(self, item):
        # Attention：class name 中包含空格时会出现BUG，用CSS选择器可以实现
        # Attention: 优化css选择器，减少误选
        artist = item.find_element_by_css_selector("[class='aplayer-list-author']").text
        title = item.find_element_by_css_selector("[class='aplayer-list-title']").text
        index = int(item.find_element_by_css_selector("[class='aplayer-list-index']").text)

        downloader_icon = item.find_element_by_css_selector(
            "[class='aplayer-list-download iconfont icon-xiazai']")

        self.driver.execute_script("arguments[0].click();", downloader_icon)

        # try:
        #     downloader_icon.click()
        # except:
        #     # 悬停显示的元素上面这个用法会报错
        #     self.driver.execute_script("arguments[0].click();", downloader_icon)

        links = self.driver.find_elements_by_css_selector(
            "[class='input-group-append']>[class='btn btn-outline-secondary download']")
        links = [link.get_attribute('href') for link in links]
        links = list(filter(None, links))

        cover = self.driver.find_element_by_css_selector(
            "[class='btn btn-outline-secondary pic_download']").get_attribute(
            'href')

        # 解析完成下载链接之后，要关闭dialog，返回上一级，从而实现遍历
        back = self.driver.find_element_by_css_selector("div>[class='btn btn-primary']")
        time.sleep(1)
        back.click()

        return index, artist, title, cover, links

    def _saver(self, message):
        # 下载log
        file_name = self.download_dir + '/' + self.now_time + '_download_log.txt'
        with open(file_name, 'a', encoding='utf-8') as f:
            f.write(json.dumps(message, ensure_ascii=False))
            f.write('\n')

    def _downloader(self, Artist, Music_name, Cover, Urls):
        lrc_name = self.download_dir + '/' + Artist + '_' + Music_name + '.lrc'
        file_name = self.download_dir + '/' + Artist + '_' + Music_name + '.mp3'
        cover_name = self.download_dir + '/' + Artist + '_' + Music_name + '.jpg'

        file = requests.get(Cover)
        with open(cover_name, 'wb') as f:
            f.write(file.content)

        lrc_url = Urls[-1]
        file = requests.get(lrc_url)
        with open(lrc_name, 'wb') as f:
            f.write(file.content)

        if len(Urls) == 5:
            file_url = Urls[-3]
        elif len(Urls) < 5:
            file_url = Urls[-2]

        file = requests.get(file_url)
        with open(file_name, 'wb') as f:
            f.write(file.content)

    def nextpage(self):
        pass






class Rank_spider(Downloader):
    '''
    如果不是网易云或者QQ的链接，尝试当作Mymp3的解析
    '''

    def __init__(self, engine='All', ifpop=True):
        pass

    def parse(self,Rank):
        pass



class Artist_spider(Downloader):

    def __init__(self, engine='All', ifpop=True):
        super(Artist_spider, self).__init__()
        pass

    def download(self,artist, count , download_dir):
        download_page = self.migu+artist

        self.driver.get(download_page)
        print(download_page)
        self.driver.quit()






class Title_spider(Downloader):
    def __init__(self, Title_spider, engine='All', ifpop=True):
        pass

    def download(self, Artist, download_path, ):
        pass


if __name__ == '__main__':
    os.chdir(r'D:\Code\Music_spider')
    count = 30
    download_dir = r'D:\temp'
    artist = '林肯公园'
    title_list = [
        'PLANET ラムジ',
        ' Butter-Fly 和田光司',
        ' 名探侦コナン メイン・テーマ(银翼ヴァージョン)	大野克夫'
    ]
    rank_list = [
        'https://y.music.163.com/m/playlist?id=752385924&creatorId=500939979&userid=500939979',
    ]

    music = Artist_spider()
    music.download(artist,50,download_dir)

