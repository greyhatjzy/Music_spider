import os, re
import requests as req
from bs4 import BeautifulSoup
import pandas as pd

pd.set_option('display.max_columns', 10)
# 原始网站 https://pubs.acs.org/loi/ancham


journals_url = r'https://pubs.acs.org/toc/ancham/90/'

for issue_id in range(1, 0, -1):
    print('当前期刊号%d' % issue_id)
    journal_url = journals_url + str(issue_id)
    resp = req.get(journal_url)
    resp.encoding = 'utf-8'
    print(resp.status_code)

    soup = BeautifulSoup(resp.text, 'html.parser')

    articles = soup.select("[class='issue-item clearfix'] .issue-item_title a")
    abstracts_flag = soup.select("[class='issue-item_buttons-list'] li:nth-child(1)")
    abstracts = soup.select("[class='hlFld-Abstract'] p")

    results_tabel = pd.DataFrame(columns=['Index', 'Title', 'Journal', 'Doi', 'Flag', 'Key_words'])
    temp = pd.DataFrame(columns=['Flag', 'Abstract'])

    titles = [art.text for art in articles]
    dois = [art['href'] for art in articles]
    abstracts_flag = [flag.text for flag in abstracts_flag]
    abstracts = [abst.text for abst in abstracts]

    results_tabel['Index'] = '92_' + str(issue_id)
    results_tabel['Title'] = titles
    results_tabel['Journal'] = 'Analytical chemistry'
    results_tabel['Doi'] = dois
    results_tabel['Flag'] = abstracts_flag

    temp['Abstract'] = pd.Series(abstracts)
    temp['Flag'] = 'Abstract'

    results_tabel = pd.merge(results_tabel[results_tabel['Flag'] == 'Abstract'], temp, on='Flag', how='left')

    file_name = 'Result_90_' + str(issue_id) + '.csv'
    results_tabel.to_csv(file_name, index=None, encoding='gb18030')
