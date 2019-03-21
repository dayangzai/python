#!/usr/bin/Python
#-*- decoding: utf-8 -*-


import csv
import pymysql


db = pymysql.connect(host='localhost',user='root',password='shuaiqitaozigege',port=3306,db='mayun',charset='utf8')
cursor = db.cursor()
with open('mayun_weibo.csv','r') as f:
  reader = csv.DictReader(f)
  for data in reader:
#    print(data)
    table = 'mayun_weibo'
    keys = ', '.join(data.keys())
    values = ', '.join(['%s'] * len(data))
    sql = 'INSERT INTO {table}({keys}) VALUES ({values})'.format(table=table, keys=keys, values=values)
    try:
      if cursor.execute(sql, tuple(data.values())):
        print(data['index_id'],'Successful')
        db.commit()
    except:
      print(data['index_id'],'Failed')
      db.rollback()
db.close()
        
