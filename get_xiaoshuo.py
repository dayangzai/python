#!/usr/bin/env Python
#-*- coding: utf-8 -*-

from bs4 import BeautifulSoup
from multiprocessing import Pool
import requests
import re


def xiaoshuo_url(url):
    s = requests.session()
    content = s.get(url).text
    soup = BeautifulSoup(content,'html.parser')
    global txt_url_list
    for i in soup.find_all(class_='two'):
        if i.a:
            txt_url_list.append([i.a.get('href'),re.sub('全文阅读','',i.a.getText())])
    return txt_url_list

def download_page_list(url):
    s = requests.session()
    content = s.get(url[0]).text
    soup = BeautifulSoup(content, 'html.parser')
    page_list = []
    for i in soup.find_all(class_='mulu_list')[0].find_all('a'): page_list.append([url[0] + i.get('href'),i.getText()])
    page_list.insert(0,url[1])
    return page_list

def requests_page(url_list):
    s = requests.session()
    for num in range(1,len(url_list) + 1):
        respons = s.get(url_list[num][0])
        if respons.status_code != 200:
            print(url_list[num][0],url_list[num][1] + '   下载失败')
            continue
        content = respons.text
        soup = BeautifulSoup(content,'html.parser')
        txt = soup.find_all(class_="contentbox")
        p = re.compile('(.*)show_style\(\)',re.S)
        txt_content = re.sub('[\xa0\n\r�3�/>br]','',re.findall(p,txt[0].getText())[0]).strip()
        with open('C:\\Users\\dayan\\Documents\\temp\\' + url_list[0],'a+') as f:
            f.write(url_list[num][1] + '\n\n' + txt_content + '\n\n')
        print('{}  下载完成。'.format(url_list[num][1]))
    print(url_list[0] + '小说下载完成。')

if __name__=='__main__':
    txt_url_list = []
    result = xiaoshuo_url('https://www.ybdu.com/book1/0/1/')
    pool = Pool(processes=30)
    for url in result:
        print(url)

        xiaoshuo = requests_page(download_page_list(url))
        requests_page(xiaoshuo)
    for i in range(2,186):
        xiaoshuo_url('https://www.ybdu.com/book1/0/{}/'.format(i))

