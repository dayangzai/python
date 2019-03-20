import requests
from pyquery import PyQuery as pq
import csv

url = 'https://m.weibo.cn/api/container/getIndex'
headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
           'Referer':'https://m.weibo.cn/u/2145291155',
           'Host':'m.weibo.cn',
           'X-Requested-With':'XMLHttpRequest'}

def get_content(page):
    params = {
        'type':'uid',
        'value':'2145291155',
        'containerid':'1076032145291155',
        'page': page
    }
    try:
        respons = requests.get(url,headers=headers,params=params)
        if respons.status_code == 200:
            return respons.json()
    except requests.ConnectionError as e:
        print('Error',e.args)

def get_page(content):
    page_result = get_content(1)['data']['cardlistInfo']['total']
    page_one = page_result/10
    page_two = page_result//10
    if page_one > page_two:
        page = page_two + 1
        return page
    else:
        page = page_two
        return page

def Params(params_content):
    items = params_content['data']['cards']
    for item in items:
        perse = item.get('mblog')
        global index_id
        index_id+=1
        yield {
            'index_id': index_id,
            'id': perse.get('id'),
            'text': pq(perse.get('text')).text(),
            'attitudes': perse.get('attitudes_count'),
            'comments': perse.get('comments_count'),
            'reposts': perse.get('reposts_count')
        }

def save_csv(file):
    with open('mayun_weibo.csv','a',encoding='utf-8') as f:
        names = ['index_id','id','text','attitudes','comments','reposts']
        writer = csv.DictWriter(f,fieldnames=names)
        writer.writerow(file)

def main():
    #获取微博内的所有page
    page_result = get_content(1)
    pages = get_page(page_result)
    global index_id
    index_id=0
    with open('mayun_weibo.csv','w',encoding='utf-8') as f:
        fieldnames = ['index_id','id','text','attitudes','comments','reposts']
        writer = csv.DictWriter(f,fieldnames=fieldnames)
        writer.writeheader()
    for page in range(1,pages+1):
        #请求对应page内容
        content = get_content(page)
        result = Params(content)
        for i in result:
            print(i)
            save_csv(i)

if __name__=='__main__':
    main()


