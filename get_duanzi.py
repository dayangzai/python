#!/usr/bin/env Python
# -*- coding: utf-8 -*-


from selenium import webdriver
from pyquery import PyQuery as PQ
from bs4 import BeautifulSoup
from time import sleep


driver = webdriver.Chrome()
driver.implicitly_wait(30)
driver.get("http://jandan.net/duan")
html = driver.page_source
soup = BeautifulSoup(html,'html.parser')
for i in soup.select('.text p'):
    print(i.text, '\n' + '#' * 50)
    with open('/tmp/xiaoshuo.txt', 'a') as f:
        f.write(i.text + '\n' + '#'*50 + '\n')
while len(soup.select('.previous-comment-page')) > 0:
    driver.find_element_by_xpath(u"(//a[contains(text(),'下一页')])[2]").click()
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    for i in soup.select('.text p'):
        print(i.text, '\n' + '#' * 50)
        with open('/tmp/xiaoshuo.txt', 'a') as f:
            f.write(i.text + '\n' + '#' * 50 + '\n')
    sleep(3)
driver.close()
