import json
import requests



file_path = './Response18.txt'


def downloader(url, file_name):
    file = requests.get(url)
    with open(file_name, 'wb') as f:
        f.write(file.content)


with open(file_path) as f:
    data = f.read()
    data = json.loads(data)['data']['list']

    for item in data:
        # print(item.keys())
        m_name = item['name']
        m_artist = item['artist']
        cover = item['cover']
        lyric = item['lrc']
        file_name = m_artist + '_' + m_name + '.mp3'
        try:
            mp3 = item['url_320']
            downloader(mp3, file_name)
            print(file_name, '下载完成')
        except:
            print(m_name + '没有高品质音乐')
