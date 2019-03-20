import json
import requests
from requests.exceptions import RequestException
import time
from lxml import etree

def get_one_page(url):
    try:
        headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:60.0) Gecko/20100101 Firefox/60.0'}
        response = requests.get(url,headers=headers)
        if response.status_code == 200:
            return response.text
        return None
    except RequestException:
        return None

def parse_one_page(html):
    html = etree.HTML(html)
    index_list = html.xpath('//dd/i[contains(@class,"board-index")]/text()')
    image_list = html.xpath('//dd/a/img[@class="board-img"]/@data-src')
    title_list = html.xpath('//dd/a[@class="image-link"]/@title')
    actor_list = html.xpath('//dd/div/div/div/p[@class="star"]/text()')
    time_list = html.xpath('//dd/div/div/div/p[@class="releasetime"]/text()')
    score_list = html.xpath('//dd/div/div/div[contains(@class,"movie-item-number")]/p/i/text()')
    score_list = [ ''.join(score_list[i:i+2]) for i in range(0,len(score_list),2)]
   
    for item in range(0,len(index_list)):
        yield {
            'index': index_list[item],
            'image': image_list[item],
            'title': title_list[item],
            'actor': actor_list[item].strip(),
            'time': time_list[item],
            'score': score_list[item]
        }

def write_to_file(content):
    print(content)
    with open('result.txt', 'a', encoding='utf-8') as f:
        f.write(json.dumps(content, ensure_ascii=False) + '\n')

def main(offset):
    url = 'http://maoyan.com/board/4?offset=' + str(offset)
    html = get_one_page(url)
    for item in parse_one_page(html):
        write_to_file(item)

if __name__ == '__main__':
    for i in range(10):
        main(offset=i * 10)
        time.sleep(1)
