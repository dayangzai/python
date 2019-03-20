import requests
import os
from hashlib import md5
from multiprocessing.pool import Pool

def get_page(offset):
    headers = {
        'x-requested-with':'XMLHttpRequest',
        'user-agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
        'referer':'https://www.toutiao.com/search/?keyword=%E8%A1%97%E6%8B%8D'
    }
    params = {
        'offset':offset,
        'format':'json',
        'keyword':'街拍',
        'autoload':'true',
        'count':20,
        'cur_tab':1,
        'from':'search_tab'
    }
    respons = requests.get('https://www.toutiao.com/search_content/',params=params,headers=headers)
    if respons.status_code == 200:
        return respons.json()

def get_images(json):
    if json.get('data'):
        for item in json.get('data'):
            if item.get('title'):
                title = item.get('title')
                images = item.get('image_list')
                yield {
                'title': title,
                'image': images
                }

def save(data):
    path = '/tmp/' + data.get('title') + '/'
    print(path)
    if not os.path.exists(path):
        os.mkdir(path)
    for i in data['image']:
        url = 'http:' + i.get('url')
        html = requests.get(url)
        MD5 = md5(html.content).hexdigest()
        with open('{}{}.{}'.format(path,MD5,'jpg'),'wb') as f:
            f.write(html.content)

def main(offset):
    res_json = get_page(offset)
    for i in get_images(res_json):
        save(i)
    

if __name__=='__main__':
    GROUP_START = 1
    GROUP_END = 7
    groups = ([x * 20 for x in range(GROUP_START, GROUP_END + 1)])
    pool = Pool(100)
    pool.map(main, groups)
    pool.close()
    pool.join()
