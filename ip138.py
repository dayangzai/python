#!/usr/bin/env Python
#-*- coding: utf-8 -*-
#outhor：dayangzai

import sys
import os
import requests
from bs4 import BeautifulSoup
from pyquery import PyQuery as pq
import re

'''
This script functions to query the IP address attribution !
'''

def usage():
    print('Usage: %s ip/iplistfile' %(sys.argv[0]))
    print('')
    print('Ex: %s 127.0.0.1' %(sys.argv[0]))

if len(sys.argv) < 2:
        usage()
        sys.exit()

def main():
 iplist = sys.argv[1]
 ip_list = []

 if os.path.isfile(iplist):
   for line in open(iplist,'r'):
     line = line.split()
     line = line[0].strip()
     ip_list.append(line)
 else:
   ip_list.append(iplist)

 #ip = input('请输入您要查询得IP：')
 for ip in ip_list:
  url = 'http://ip138.com/ips138.asp?ip={}&action=2'.format(ip)
  html = requests.get(url).content
  doc = pq(html.decode('gb2312'))
  IP = doc('h1').text()
  ascription  = re.sub('本站数据','IP地址归属',doc('li').html())
  print('{: <50s}{}'.format(IP,ascription))

if __name__ == '__main__':
 main()
