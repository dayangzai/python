from requests import get
from pyquery import PyQuery as pq
import os

def get_zhihu(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'}
    respons = get(url,headers=headers)
    if respons.status_code == 200:
        return respons.text
    return None

def filter(html):
    doc = pq(html)
    list_item = doc('#js-explore-tab .explore-feed').items()
    for index in list_item:
        yield [
            index.find('.author-link-line').text(),
            index.find('h2').text(),
            pq(index.find('.content').html()).text()]

def save(path,text):
    for cnt in text:
        with open(path,'a') as f:
            f.write('\n'.join(cnt))
            f.write('\n' + '#' * 50 + '\n')

def main():
    url = 'https://www.zhihu.com/explore'
    path = '/tmp/result.txt'
    result = get_zhihu(url)
    content = filter(result)
    save(path,content)
    if os.path.isfile(path):
        print("爬取完成！")

    
if __name__=="__main__":
   main()

