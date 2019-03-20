#!/usr/bin/env Python
# -*- coding: utf-8 -*-

import requests
from random import choice
import re
import os
import threading
'''

auther: dayangzai

'''
requests.packages.urllib3.disable_warnings()

class Download_img():
    def __init__(self,url,path):
        self.s = requests.session()
        self.url = url
        self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.79'}
        self.proxies = ['118.114.77.47:8080', '122.114.31.177:808','163.177.151.23:80','61.135.217.7:80']
        self.path = path
        self.Headers = {'Host': 'img1.mm131.me',
                       'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:57.0) Gecko/20100101 Firefox/57.0',
                       'Accept': '*/*',
                       'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
                       'Accept-Encoding': 'gzip, deflate',
                       'Referer': 'http://www.mm131.com/xinggan/2697.html',
                       'Connection': 'keep-alive',
                       'Cache-Control': 'max-age=0'}

    def request(self):
        respons = self.s.get(self.url, headers=self.headers, proxies={'http': choice(self.proxies)},verify=False).text
        pattern = re.compile('<dd>.*?href="(.*?\.html)">.*</dd>')
        url_list = re.findall(pattern, respons)
        global_url = [self.url]
        respons = self.s.get(global_url[0], headers=self.headers, proxies={'http': choice(self.proxies)}, verify=False).content.decode('gbk')
        url_text = re.findall('(list.*?\.html)', respons)[0]
        url_num = re.findall('list.*_(.*?)\.html', respons)[0]
        for NUM in range(2, int(url_num) + 1):
            url_args = re.sub('_[0-9]+\.', '_' + str(NUM) + '.', url_text)
            global_url.append(global_url[0] + url_args)
        for i in global_url:
            respons = self.s.get(i, headers=self.headers, proxies={'http': choice(self.proxies)}, verify=False).text
            pattern = re.compile('<dd>.*?href="(.*?\.html)"><img')
            url_list = url_list + re.findall(pattern, respons)
            url_list = url_list + re.findall(pattern, respons)
        print(url_list)
        return url_list

    def download_url(self,url):
        url_list = []
        url_list.append(url)
        img_lists = []
        new_list = []
        for i in url_list:
            new_list.append(i)
            for urls in new_list:
                try:
                    respons = self.s.get(urls, headers=self.headers, proxies={'http': choice(self.proxies)}, verify=False).text
                    pattern_img = re.compile('<div class="content-pic.*src="(http.*?\.jpg)"')
                    pattern_page = re.compile('<a href=\'(.{1,20}\.html)')
                    img_url = re.findall(pattern_img, respons)
                    global img_page
                    img_page = re.findall(pattern_page, respons)
                    img_page = list(set(img_page))
                    img_lists.append(img_url[0])
                    Url = re.findall('(http.*/)', urls)[0]
                except:
                    pass
                for index in img_page:
                    try:
                        respons = self.s.get(Url + index, headers=self.headers, proxies={'http': choice(self.proxies)}, verify=False).text
                        pattern_img = re.compile('<div class="content-pic.*src="(http.*?\.jpg)"')
                        pattern_page = re.compile('<a href=\'(.{120}\.html)')
                        img_url = re.findall(pattern_img, respons)
                        img_lists.append(img_url[0])
                        print(img_lists,'\n',len(img_lists))
                    except:
                        pass
        new_list = []
        return img_lists

    def download_img(self,url):
        if os.path.exists(self.path):
            pass
        else:
            os.mkdir(self.path)
        img_lists = url
        num = 0
        for URL in img_lists:
            try:
                num += 1
                rps = self.s.get(URL, headers=self.Headers, proxies={'http': choice(self.proxies)}, verify=False).content
                with open(self.path + str(num) + '.jpg', 'wb') as f:
                    f.write(rps)
            except:
                pass
if __name__=='__main__':
    f = Download_img('http://www.mm131.com/xinggan/','C:\\Users\\think\\Desktop\\jpg\\')
    url = f.request()
    thread = []
    for i in url:
        thread.append(threading.Thread(target=f.download_url,args=(i,)))
    for i in thread:
        i.start()
        while True:
            if len(threading.enumerate()) < 20:
                break
    for i in thread:
        i.join()
#    f.download_img(img_url)
