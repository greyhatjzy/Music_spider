import time,re
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import pandas  as pd

def spider(artist):
    driver = webdriver.Chrome()
    driver.implicitly_wait(5)
    driver.get("http://tool.liumingye.cn/music/?page=searchPage")

    input_tag = driver.find_element_by_id('input')
    input_tag.send_keys('周杰伦')
    input_tag.send_keys(Keys.ENTER)

    download_icons = driver.find_elements_by_class_name('init')
    for item in download_icons:
        # Attention：class name 中包含空格时会出现BUG，用CSS选择器可以实现
        downloader_icon = item.find_element_by_css_selector("[class='aplayer-list-download iconfont icon-xiazai']")
        downloader_icon.click()
        links = driver.find_elements_by_css_selector("[class='btn btn-outline-secondary download']")

        # 解析完成下载链接之后，要关闭dialog，返回上一级，从而实现遍历
        for link in links:

            print(link.get_attribute('outerHTML'))


    time.sleep(2)
    driver.quit()


#spider(' ')



# token_m=re.compile('resourceType=')
# musical_urls=[['http://218.205.239.34/MIGUM2.0/v1.0/content/sub/listenSong.do?toneFlag=LQ&amp;netType=00&amp;copyrightId=0&amp;contentId=600907000009041441&amp;resourceType=2&amp;channel=0'], ['http://218.205.239.34/MIGUM2.0/v1.0/content/sub/listenSong.do?toneFlag=PQ&amp;netType=00&amp;copyrightId=0&amp;contentId=600907000009041441&amp;resourceType=2&amp;channel=0'], ['http://218.205.239.34/MIGUM2.0/v1.0/content/sub/listenSong.do?toneFlag=HQ&amp;netType=00&amp;copyrightId=0&amp;contentId=600907000009041441&amp;resourceType=2&amp;channel=0'], ['http://218.205.239.34/MIGUM2.0/v1.0/content/sub/listenSong.do?toneFlag=SQ&amp;netType=00&amp;copyrightId=0&amp;contentId=600907000009041441&amp;resourceType=E&amp;channel=0'], [], [], []]
# musical_urls=list(filter(None,musical_urls))
# musical_urls=[musical_url[0] for musical_url in musical_urls]
#
# for url in musical_urls:
#     type_pos=token_m.search(url).span()[1]
#     type=url[type_pos:type_pos+1]
#
#
#
#     print(type)

download_df = pd.DataFrame(columns=['Artist', 'Music_name', 'Quality', 'Url'])
a=['a']*4
download_df['Artist']=a
print(download_df)