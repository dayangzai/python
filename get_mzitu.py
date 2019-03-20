#!/usr/bin/env Python
#-*- coding: utf-8 -*-

import requests
from pyquery import PyQuery as pq
from hashlib import md5

class download_img():
    def __init__(self,url):
        self.base_url = url
        self.s = requests.session()
        self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.79 Safari/537.36'}
        self.img_headers = {'Referer': 'http://www.mzitu.com/137840/6',
                            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.79 Safari/537.36'}
    #获取总的page数
    def get_page_sum(self):
        html = self.s.get(self.base_url,headers = self.headers)
        if html.status_code == 200:
            doc = pq(html.text)
            sum_page = doc('.dots+ .page-numbers').text()
            return sum_page
        return None
    #获取当前页面内的所有2级url
    def get_2j_url(self,url):
        html = self.s.get(url,headers = self.headers)
        if html.status_code == 200:
            doc = pq(html.text)
            url_list = []
            for item in doc('#pins a').items():
                if len(item.text()) > 0:
                    url_list.append([item.text(),item.attr('href')])
            return url_list
    #获取2级url内的每一张图片URL
    def get_img_url(self,url):
        html = self.s.get(url[1],headers = self.headers)
        if html.status_code == 200:
            doc = pq(html.text)
            page = int(doc('.dots+ a span').text())
            img_url = [doc('.main-image img').attr('src')]
            for item in range(1,page + 1):
                try:
                    page_url = '{}/{}'.format(url[1],str(item))
                    html = self.s.get(page_url,headers=self.headers)
                    if html.status_code == 200 :
                        doc = pq(html.text)
                        img_url.append(doc('.main-image img').attr('src'))
                except:
                    pass
            return {url[0]:img_url}
    #保存图片
    def save(self,url):
        for key,value in url.items():
            Sum = len(value)
            start = 0
            for item in value:
                try:
                    start += 1
                    html = self.s.get(item,headers=self.img_headers)
                    if html.status_code == 200:
                        MD5 = md5(html.content).hexdigest()
                        with open('C:\\Users\\dayan\\Desktop\\mzitu\\{}.jpg'.format(MD5),'wb') as f:
                            f.write(html.content)
                    print('{}：{} 总{}张图片，下载完成第{}张，剩余{}张未下载.'.format(key,item,Sum,start,Sum-start))
                except:
                    pass

def main():
    base_url = 'http://www.mzitu.com/'
    get = download_img(base_url)
    sum_page = int(get.get_page_sum())
    print(sum_page)
    url_2j = get.get_2j_url(base_url)
    for index in url_2j:
        img_url = get.get_img_url(index)
        get.save(img_url)
    for i in range(2,sum_page+1):
        try:
            url = 'http://www.mzitu.com/page/{}/'.format(str(i))
            url_2j = get.get_2j_url(url)
            for index in url_2j:
                img_url = get.get_img_url(index)
                get.save(img_url)
        except:
            pass

if __name__=='__main__':
    main()

