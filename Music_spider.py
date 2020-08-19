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
        self.driver = webdriver.Chrome('E:\Music_spider\driver\chromedriver.exe')
        self.driver.implicitly_wait(5)
        self.download_dir = download_dir
        self.count = count

    def download_artist(self, artist):
        # 下载统计表格
        self.download_df = pd.DataFrame(columns=['Artist', 'Music_name', 'Type', 'Quality', 'Url'])

        # 从原始页面搜索
        self.driver.get(self.orig_website)
        input_tag = self.driver.find_element_by_id('input')
        input_tag.send_keys(artist)
        input_tag.send_keys(Keys.ENTER)
        time.sleep(2)


        # href是JS生成的，如果直接寻找下载节点，没有href信息
        # download_links =self.driver.find_elements_by_css_selector("[class='btn btn-outline-secondary download']")

        current_page = self.driver.find_element_by_class_name('aplayer-list')
        #next_page = self.driver.find_element_by_class_name('aplayer-more')

        downloader_icon = current_page.find_elements_by_css_selector("[class='aplayer-list-download iconfont icon-xiazai']")
        repr()

        # for item in download_links:
        #     # Attention：class name 中包含空格时会出现BUG，用CSS选择器可以实现
        #     artist = item.find_element_by_css_selector("[class='aplayer-list-author']").text
        #     title = item.find_element_by_css_selector("[class='aplayer-list-title']").text
        #     print('正在解析：', artist, title)
        #
        #     downloader_icon = item.find_element_by_css_selector("[class='aplayer-list-download iconfont icon-xiazai']")
        #     downloader_icon.click()
        #     # Attention: 优化css选择器，减少误选
        #     links = self.driver.find_elements_by_css_selector(
        #         "[class='input-group-append']>[class='btn btn-outline-secondary download']")
        #     back = self.driver.find_element_by_css_selector("[class='btn btn-primary']")
        #     next_page = self.driver.find_element_by_css_selector("[class='aplayer-more']")
        #     # 解析完成下载链接之后，要关闭dialog，返回上一级，从而实现遍历
        #     links = [link.get_attribute('outerHTML') for link in links]
        #     musical_urls, quality, type = self.data_clean(links)
        #     #
        #     download_df_temp = pd.DataFrame(columns=['Artist', 'Music_name', 'Type', 'Quality', 'Url'])
        #     download_df_temp['Artist'] = [artist] * len(musical_urls)
        #     download_df_temp['Music_name'] = [title] * len(musical_urls)
        #     download_df_temp['Type'] = type
        #     download_df_temp['Quality'] = quality
        #     download_df_temp['Url'] = musical_urls
        #     self.download_df = self.download_df.append(download_df_temp, ignore_index=True)
        #     download_df_temp.drop(download_df_temp.index, inplace=True)
        #
        #     time.sleep(2)
        #     back.click()
        #
        #     # 滚轮会影响按钮的点击
        #     try:
        #         self.driver.execute_script('window.scrollBy(0,50);')
        #         time.sleep(1)
        #     except:
        #         next_page.click()
        #         pass
        #
        # self.download_df.to_csv('./Download_info.csv', index=None, encoding='gb18030')
        # print(self.download_df)
        self.driver.quit()

    def download_rank(self, rank_name):
        pass




    def data_clean(self, links):
        # 对爬取的数据进行清洗
        # resourceType = 2    MP3格式    resourceType=E      FLAC格式
        # toneFlag=LQ，PQ，HQ，SQ 品质递增
        # 1.map出下载链接
        # 2.选择MP3格式，按照品质权重递增

        musical_urls = []
        for link in links:
            pattern = re.compile('http://..*channel=0')
            musical_urls.append(pattern.findall(link))
        # 清除空值,去除list套壳，倒序
        musical_urls = list(filter(None, musical_urls))
        musical_urls = [musical_url[0] for musical_url in musical_urls]
        musical_urls.reverse()

        # # URL筛选
        token_m = re.compile('resourceType=')
        token_q = re.compile('toneFlag=')

        type_list = []
        quality_list = []
        for url in musical_urls:
            type_pos = token_m.search(url).span()[1]
            type = url[type_pos:type_pos + 1]
            type_list.append(type)

            quality_pos = token_q.search(url).span()[1]
            quality = url[quality_pos:quality_pos + 2]
            quality_list.append(quality)
        return musical_urls, quality_list, type_list

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
    os.chdir('E:\Music_spider')
    count = 50
    download_dir = '/media/jzy/Data/Music'
    downloader = Music_Download(download_dir, count)
    downloader.download_artist('周杰伦')
    # downloader.download_rank()
