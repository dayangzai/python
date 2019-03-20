import requests
import re
import json

def get_one_page(url):
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:60.0) Gecko/20100101 Firefox/60.0'}
    response = requests.get(url,headers=headers)
    if response.status_code == 200:
        return response.text
    return None

def get_content(html):
    pattern = re.compile('<dd>.*?board-index.*?>(.*?)</i>.*?data-src="(.*?)"\salt="(.*?)".*?"star">\s*(.*?)\s*?</p>.*?"releasetime">(.*?)</p>.*?integer">(.*?)</i>.*?fraction">(.*?)</i>',re.S)
    items = re.findall(pattern,html)
    for item in items:
        yield{
            'index':item[0],
            'image':item[1],
            'title':item[2],
            'actor':item[3],
            'time':item[4],
            'score':str(item[5]) + str(item[6])
        }

def write_to_json(content):
    print(content)
    with open('result.txt','a',encoding='utf-8') as f:
        f.write(json.dumps(content,ensure_ascii=False) + '\n')

def main():
    for i in range(0,1):
        index = i*10
        url = 'http://maoyan.com/board/4?offset={}'.format(index)
        html = get_one_page(url)
        for content in get_content(html):
            write_to_json(content)

if __name__=='__main__':
    main()
