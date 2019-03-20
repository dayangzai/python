#!/usr/bin/env Python
#-*- decoding: utf-8 -*-

import requests
from urllib import parse

def translation(test):
    Request_url = 'http://fanyi.youdao.com/translate?smartresult=dict&smartresult=rule'
    Form_Data={}
    Form_Data['i']=test
    Form_Data['from']='AUTO'
    Form_Data['to']='AUTO'
    Form_Data['smartresult']='dict'
    Form_Data['client']='fanyideskweb'
    Form_Data['salt']='1528177509799'
    Form_Data['sign']='bc7e8b6ddb0a0abad13647487daace1c'
    Form_Data['doctype']='json'
    Form_Data['version']='2.1'
    Form_Data['keyfrom']='fanyi.web'
    Form_Data['action']='FY_BY_REALTIME'
    Form_Data['typoResult']='false'
#    data = parse.urlencode(Form_Data)
#    Request_url += data
    s = requests.session()
    try:
        translate_results=s.get(Request_url,params=Form_Data).json()
        src=translate_results['translateResult'][0][0]['src']
        res=translate_results['translateResult'][0][0]['tgt']
        #print(translate_results)
        print('src:',src)
        print('result:',res)
    except:
        print('请输入正确的翻译内容！')

if __name__=='__main__':
    test = input('请输入要翻译的内容：')
    translation(test)
