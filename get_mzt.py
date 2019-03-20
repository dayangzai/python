#!/usr/bin/env Python
#-*- coding: utf-8 -*-


import requests
from pyquery import PyQuery as pq
from hashlib import md5




def get_mzt(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:60.0) Gecko/20100101 Firefox/60.0'}
    s = requests.session()
    respons = s.get(url,headers=headers)
    if respons.status_code == 200:
        return respons.text
    return None


def get_page(html):
    doc = pq(html)
    page = doc('.dots+ .page-numbers').text()
    return page


def get_image_url(html):
    doc = pq(html)
    img_list = doc('#comments img').items()
    for item in img_list:
        yield item.attr('src')


def save_image(img_url):
    global num
    num+=1
    html = requests.get(img_url)
    if html.status_code == 200:
        MD5 = md5(html.content).hexdigest()
        with open('/tmp/images/' + MD5 + '.jpg','wb') as f:
            f.write(html.content)


if __name__=='__main__':
    num = 0
    url = 'http://www.mzitu.com/zipai/comment-page-1/#comments'
    content = get_mzt(url)
    page_end = int(get_page(content))
    for index in range(1,page_end+1):
        url = 'http://www.mzitu.com/zipai/comment-page-{}/#comments'.format(index)
        content = get_mzt(url)
        start = num
        for item in get_image_url(content):
            save_image(item)
        print('共{}页内容，当前下载第{}页内容，本页下载完{}张图片,总下载完成{}张图片,剩余{}页未下载。'.format(page_end,index,num-start,num,page_end-index))
