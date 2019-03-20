import csv
from requests import get
from pyquery import PyQuery as pq
from time import sleep

with open('/root/anquan/files_exploits.csv','r',encoding='utf-8') as csvfile:
    reader = csv.reader(csvfile)

    for row in reader:
        try:
            if 'id' in row:
                row.append('CVE')
                row.append('E-DB')
                with open('/root/anquan/files.csv','w') as w:
                    writer = csv.writer(w, delimiter=',')
                    writer.writerow(row)
                continue
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36'}
            url = 'https://www.exploit-db.com/exploits/' + row[0]
            response = get(url,headers=headers)
            doc = pq(response.text)
            CVE = doc('.exploit_list td:nth-child(1) .external').text()
            EDB = doc('td:nth-child(1) img').attr('alt')
            row += [CVE,EDB]
            print(row)
            with open('/root/anquan/files.csv', 'a',encoding='utf-8-sig') as f:
                writer = csv.writer(f, delimiter=',')
                writer.writerow(row)
        except:
            pass





