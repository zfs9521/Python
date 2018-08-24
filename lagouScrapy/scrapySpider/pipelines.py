# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import MySQLdb
class InfoPipeline(object):
    def process_item(self,item,spider):
        if  'formatTime' in item.keys():
            print('------------------')
            conn=MySQLdb.connect(host="127.0.0.1",user="root",password="",db="jobInfo",charset='utf8',use_unicode=True)
            cur=conn.cursor()
            insertInto="""
                insert into jobInfos(jobInfo1,jobInfo2,jobInfo3,jobInfo4,jobInfo5,jobInfo6,job,jobLink,address,money,need1,need2,companyName,companyLink,industry1,industry2,industry3,treatment,formatTime,datetime) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
            """
            cur.execute(insertInto,(item['jobInfo1'],item['jobInfo2'],item['jobInfo3'],item['jobInfo4'],item['jobInfo5'],item['jobInfo6'],item['job'],item['jobLink'],item['address'],item['money'],item['need1'],item['need2'],item['companyName'],item['companyLink'],item['industry1'],item['industry2'],item['industry3'],item['treatment'],item['formatTime'],item['datetime']))
            conn.commit()
            print(item)
            print('------------------')
        elif 'jobRequest' in item.keys():
            print(item)
            print('xxxxxcxxxxxxxxx')
        elif 'companyManager' in item.keys():
            print('kkkkkkkkkkkkk')
        else:
            print('Error!!!!!!!')



