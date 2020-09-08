# 下载歌曲的爬虫
import time, os, datetime
import json
import requests
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


class Music_Download():

    def __init__(self, download_dir, count=20):
        self.orig_website = 'http://tool.liumingye.cn/music/?page=searchPage'
        option = webdriver.ChromeOptions()

        # 设置option,不显示浏览器窗口
        option.add_argument('headless')
        # self.driver = webdriver.Chrome()
        # self.driver = webdriver.Chrome(chrome_options=option)
        self.driver = webdriver.Chrome('D:\Code\Music_spider\driver\chromedriver.exe', options=option)
        # self.driver = webdriver.Chrome('D:\Code\Music_spider\driver\chromedriver.exe')

        self.driver.implicitly_wait(5)
        self.download_dir = download_dir
        self.count = int(count)+1
        self.now_time = datetime.datetime.now().strftime('%Y-%m-%d')

    def download_artist(self, artist, ifcontinue=False):
        '''
        默认下载20首歌曲，超过20首时，点击 next page

        '''

        self.search(artist, ifcontinue)

        # href是JS生成的，如果直接寻找下载节点，没有href信息
        # 当超过20首歌时，递归调用自己，节点选择最后20个即可。
        # download_links =self.driver.find_elements_by_css_selector("[class='btn btn-outline-secondary download']")

        current_page = self.driver.find_elements_by_tag_name("[class='aplayer-list'] li")[-20:]
        for item in current_page:
            index, Artist, Music_name, Cover, Urls = self.get_url(item)
            if index < self.count:
                print('正在解析第%s首歌：' % index, artist, '-', Music_name)
                info_json = {'Index': index, 'Artist': Artist, 'Music_name': Music_name, 'Urls': Urls}
                self.saver(info_json)

                try:
                    self.downloader(Artist, Music_name, Cover, Urls)
                except:
                    print('下载失败')

                if index % 5 == 0:
                    self.driver.execute_script('window.scrollBy(0,180);')

                if index % 20 == 0:
                    next_page = self.driver.find_element_by_class_name('aplayer-more')
                    next_page.click()
                    time.sleep(1)
                    self.driver.execute_script('window.scrollBy(0,280);')
                    self.download_artist(artist, ifcontinue=True)
            else:
                break
        self.driver.quit()

    def search(self, artist, ifcontinue):
        # TODO: 默认了搜索引擎

        # 从原始页面搜索
        if ifcontinue:
            pass
        else:
            self.driver.get(self.orig_website)
            input_tag = self.driver.find_element_by_id('input')
            input_tag.send_keys(artist)
            input_tag.send_keys(Keys.ENTER)
            time.sleep(2)

    def download_rank(self, rank_name):
        self.driver.get(rank_name)

        current_page = self.driver.find_elements_by_tag_name("[class='aplayer-list'] li")
        count = 0

        for item in current_page:
            Index, Artist, Music_name, Cover, Urls = self.get_url(item)

            info_json = {'Index': Index, 'Artist': Artist, 'Music_name': Music_name, 'Urls': Urls}

            self.saver(info_json)
            try:
                self.downloader(Artist, Music_name, Cover, Urls)
            except:
                print('下载失败')

            count += 1
            time.sleep(1)

            if count % 5 == 0:
                self.driver.execute_script('window.scrollBy(0,180);')

            if count % 20 == 0:
                next_page = self.driver.find_element_by_class_name('aplayer-more')
                next_page.click()
        self.driver.quit()

    def download_title(self, title):
        '''
        从3个主流媒体中搜索下载top N 的歌曲作为备选
        '''

        migu = 'http://tool.liumingye.cn/music/?page=audioPage&type=migu&name='
        yqd = 'http://tool.liumingye.cn/music/?page=audioPage&type=YQD&name='
        yqb = 'http://tool.liumingye.cn/music/?page=audioPage&type=YQB&name='
        search_engin = {'migu': migu, 'yqd': yqd, 'yqb': yqb}
        for engin in search_engin:
            website = search_engin[engin] + title
            self.driver.get(website)
            current_page = self.driver.find_element_by_tag_name("[class='aplayer-list'] li")
            Index, Artist, Music_name, Cover, Urls = self.get_url(current_page)
            Artist = engin + '_' + Index + '_' + Artist
            info_json = {'Index': Index, 'Artist': Artist, 'Music_name': Music_name, 'Urls': Urls}

            self.saver(info_json)
            try:
                self.downloader(Artist, Music_name, Cover, Urls)
            except:
                print('下载失败')
            time.sleep(1)
        self.driver.quit()

    def get_url(self, item):
        # Attention：class name 中包含空格时会出现BUG，用CSS选择器可以实现
        # Attention: 优化css选择器，减少误选
        artist = item.find_element_by_css_selector("[class='aplayer-list-author']").text
        title = item.find_element_by_css_selector("[class='aplayer-list-title']").text
        index = int(item.find_element_by_css_selector("[class='aplayer-list-index']").text)

        downloader_icon = item.find_element_by_css_selector(
            "[class='aplayer-list-download iconfont icon-xiazai']")

        try:
            downloader_icon.click()
        except:
            # 悬停显示的元素上面这个用法会报错
            self.driver.execute_script("arguments[0].click();", downloader_icon)

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

    def saver(self, message):
        # 下载log
        file_name = self.download_dir + '/' + self.now_time + '_download_log.txt'
        with open(file_name, 'a', encoding='utf-8') as f:
            f.write(json.dumps(message, ensure_ascii=False))
            f.write('\n')

    def downloader(self, Artist, Music_name, Cover, Urls):
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


if __name__ == '__main__':
    os.chdir(r'D:\Code\Music_spider')
    count = 30
    download_dir = r'D:\迅雷下载'
    artists_list = ['周杰伦', '薛之谦', '邓紫棋', '林俊杰', '陈奕迅', '许嵩', '毛不易', '王力宏', '林宥嘉', '五月天', '杨千嬅', '张信哲', ]
    title_list = [
        'PLANET ラムジ',
        ' Butter-Fly 和田光司',
        ' 名探侦コナン メイン・テーマ(银翼ヴァージョン)	大野克夫'
    ]
    rank_list = [
        r'http://tool.liumingye.cn/music/?page=audioPage&type=YQD&name=https%3A%2F%2Fmusic.163.com%2F%23%2Fplaylist%3Fid%3D2829883282']

    for artist in artists_list:
        downloader = Music_Download(download_dir, count)
        downloader.download_artist(artist)
        print('.................%s...................' % artist, '下载完成')

    # for title in title_list:
    #     downloader = Music_Download(download_dir, 1)
    #     downloader.download_title(title)
    #     break
    #
    # for rank in rank_list:
    #     downloader = Music_Download(download_dir, 100)
    #     downloader.download_rank(rank)
