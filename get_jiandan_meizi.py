#!/use/bin/env Python
#-*- conding: utf-8 -*-

from selenium import webdriver
from pyquery import PyQuery as pq
import requests
from re import findall

driver = webdriver.Chrome()
driver.get('http://jandan.net/ooxx')
driver.find_element_by_link_text(u"妹子图").click()
html = driver.execute_script("return document.documentElement.outerHTML")
doc = pq(html)
for item in doc('#comments img').items():
    image_url = item.attr('src')
    html = requests.get(image_url)
    if html.status_code == 200:
        name = findall('.*/(.*)',image_url)[0]
        with open('C:\\Users\\dayan\\Desktop\\jiandan\\' + name,'wb') as f:
            f.write(html.content)
while len(doc('.previous-comment-page')) > 0:
    driver.find_element_by_link_text(u"下一页").click()
    html = driver.execute_script("return document.documentElement.outerHTML")
    doc = pq(html)
    for item in doc('#comments img').items():
        image_url = item.attr('src')
        html = requests.get(image_url)
        if html.status_code == 200:
            name = findall('.*/(.*)', image_url)[0]
            with open('C:\\Users\\dayan\\Desktop\\jiandan\\' + name, 'wb') as f:
                f.write(html.content)
driver.close()
