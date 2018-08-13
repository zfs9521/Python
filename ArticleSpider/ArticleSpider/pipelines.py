# -*- coding: utf-8 -*-
from scrapy.pipelines.images import ImagesPipeline
from scrapy.exporters import JsonItemExporter
import codecs
import json
import MySQLdb
import MySQLdb.cursors
from twisted.enterprise import adbapi
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


# class ArticlespiderPipeline(object):
#     def process_item(self, item, spider):
#         lines = json.dumps(dict(item),ensure_ascii=False) + "\n"
#         self.file.write(lines)
#         return item

class JsonWithEncodingPipeline(object):
    def __init__(self):
        self.file = codecs.open('article.json','w',encoding='utf-8')
    def process_item(self, item, spider):
        lines = json.dumps(dict(item),ensure_ascii=False) + "\n"
        self.file.write(lines)
        return item
    def spider_closed(self,spider):
        self.file.close()

#Scrapy自带的
# class JsonExporterPipeline(object):
#     def __init__(self):
#         self.file = open('articleexport.json','wb')
#         self.exporter = JsonItemExporter(self.file,encoding='utf-8',ensure_ascii= False)
#         self.exporter.start_exporting()
#
#     def close_spider(self,spider):
#         self.exporter.finish_exporting()
#         self.file.close()
#     def process_item(self,item,spider):
#         self.exporter.export_item(item)
#         return item

class MysqlPipeline(object):
    def __init__(self):
        self.conn = MySQLdb.connect('127.0.0.1','root','password','article_spider',charset='utf8',use_unicode=True)
        self.cursor = self.conn.cursor()
    def process_item(self,item,spider):
        insert_sql = """
            insert into jobbole_article(url_object_id,title,url,fav_nums)
            VALUES (%s, %s, %s, %s)
            """
        self.cursor.execute(insert_sql,(item['url_object_id'],item['title'],item['url'],item['fav_nums']))
        self.conn.commit()

#连接池ConnectionPool
#    def __init__(self, dbapiName, *connargs, **connkw):
class MysqlTwistedPipeline(object):
    def __init__(self, dbpool):
        self.dbpool = dbpool

    @classmethod
    def from_settings(cls, settings):
        dbparms = dict(
            host = settings["MYSQL_HOST"],
            db = settings["MYSQL_DBNAME"],
            user = settings["MYSQL_USER"],
            passwd = settings["MYSQL_PASSWORD"],
            charset='utf8',
            cursorclass=MySQLdb.cursors.DictCursor,
            use_unicode=True,
        )
        #**dbparms-->("MySQLdb",host=settings['MYSQL_HOST']
        dbpool = adbapi.ConnectionPool("MySQLdb", **dbparms)

        return cls(dbpool)

    def process_item(self, item, spider):
        #使用twisted将mysql插入变成异步执行
        query = self.dbpool.runInteraction(self.do_insert, item)
        query.addErrback(self.handle_error, item, spider) #处理异常

    def handle_error(self, failure, item, spider):
        #处理异步插入的异常
        print (failure)

    def do_insert(self, cursor, item):
        #执行具体的插入
        #根据不同的item 构建不同的sql语句并插入到mysql中
        insert_sql, params = item.get_insert_sql()
        cursor.execute(insert_sql, params)

# class ArticleImagePipeline(ImagesPipeline):
#     def item_completed(self, results, item, info):
#         for ok,value in results:
#             image_file_path = value['path']
#         item['front_image_path'] = image_file_path
#         return item