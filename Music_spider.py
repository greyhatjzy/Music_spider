# 下载歌曲的爬虫
import time, os, re
import requests
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

pd.set_option('display.max_columns', 10)


# TODO:
# 1.下载数量
# 2.滚轮的协调


class Music_Download():
    '''
    流程：


    '''

    def __init__(self, download_dir, count=20):
        self.orig_website = 'http://tool.liumingye.cn/music/?page=searchPage'
        self.driver = webdriver.Chrome('D:\Code\Music_spider\driver\chromedriver.exe')
        self.driver.implicitly_wait(5)
        self.download_dir = download_dir
        self.count = int(count)

    def download_artist(self, artist):

        # 从原始页面搜索
        self.driver.get(self.orig_website)
        input_tag = self.driver.find_element_by_id('input')
        input_tag.send_keys(artist)
        input_tag.send_keys(Keys.ENTER)
        time.sleep(2)

        # href是JS生成的，如果直接寻找下载节点，没有href信息
        # download_links =self.driver.find_elements_by_css_selector("[class='btn btn-outline-secondary download']")
        current_page = self.driver.find_elements_by_tag_name("[class='aplayer-list'] li")

        # if self.count >21:
        #     next_page = self.driver.find_element_by_class_name('aplayer-more')
        #     next_page.click()
        for ind in range(1,self.count):
            if self.count >21:
                if ind%13==0:
                    next_page = self.driver.find_element_by_class_name('aplayer-more')
                    next_page.click()
                for item in current_page:
                    Index, Artist, Music_name, Urls = self.get_url(item)
                    # print(Index, Artist, Music_name, Type,Quality,Url)
                    # break
                    lrc_url = Urls[-1]
                    hq_url = Urls[-1]

        self.driver.quit()

    def download_rank(self, rank_name):
        pass

    def get_url(self, item):

        # Attention：class name 中包含空格时会出现BUG，用CSS选择器可以实现
        artist = item.find_element_by_css_selector("[class='aplayer-list-author']").text
        title = item.find_element_by_css_selector("[class='aplayer-list-title']").text
        index = item.find_element_by_css_selector("[class='aplayer-list-index']").text
        print('正在解析第%s首歌：' % int(index), artist, title)

        downloader_icon = self.driver.find_element_by_css_selector("[class='aplayer-list-download iconfont icon-xiazai']")
        downloader_icon.click()
        # Attention: 优化css选择器，减少误选
        back = self.driver.find_element_by_css_selector("[class='btn btn-primary']")

        # 解析完成下载链接之后，要关闭dialog，返回上一级，从而实现遍历
        # link = []

        token_m = re.compile('resourceType=')
        token_q = re.compile('toneFlag=')
        links = self.driver.find_elements_by_css_selector(
            "[class='input-group-append']>[class='btn btn-outline-secondary download']")

        links = [link.get_attribute('href') for link in links]
        links = list(filter(None, links))
        back.click()
        return index, artist, title, links

    def data_clean(self, links):
        # 对爬取的数据进行清洗
        # resourceType = 2    MP3格式    resourceType=E      FLAC格式
        # toneFlag=LQ，PQ，HQ，SQ 品质递增
        # 1.map出下载链接
        # 2.选择MP3格式，按照品质权重递增

        # musical_urls = []
        # for link in links:
        #     pattern = re.compile('http://..*channel=0')
        #     musical_urls.append(pattern.findall(link))
        # # 清除空值,去除list套壳，倒序
        # musical_urls = list(filter(None, musical_urls))
        # musical_urls = [musical_url[0] for musical_url in musical_urls]
        # musical_urls.reverse()

        # # URL筛选
        token_m = re.compile('resourceType=')
        token_q = re.compile('toneFlag=')

        type_list = []
        quality_list = []

        links = list(filter(None, links))
        for link in links:
            print(link)
            type_pos = token_m.search(link).span()[1]
            type = link[type_pos:type_pos + 1]
            type_list.append(type)

            quality_pos = token_q.search(link).span()[1]
            quality = link[quality_pos:quality_pos + 2]
            quality_list.append(quality)

    def saver(self, message):

        # 下载log
        file_name = self.download_dir + 'download_log.txt'
        time_now = time.localtime()
        with open(file_name, 'a') as f:
            f.write(message)

    def downloader(url, file_name):
        file = requests.get(url)
        with open(file_name, 'wb') as f:
            f.write(file.content)


if __name__ == '__main__':
    # os.chdir('/home/jzy/Desktop/Scrapy_project')
    os.chdir('D:\Code\Music_spider')
    count = 50
    download_dir = '/media/jzy/Data/Music'
    downloader = Music_Download(download_dir, count)
    downloader.download_artist('周杰伦')
    # downloader.download_rank()
