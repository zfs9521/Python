# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import codecs
import json
class TianqiscrapyPipeline(object):
    def process_item(self, item, spider):
        return item
class TianqiPipeline(object):
    def __init__(self):
        self.file=codecs.open('tianqi.json','w','utf-8')
    def process_item(self,item,spider):
        file=json.dumps(dict(item),ensure_ascii=False)+'\n'
        self.file.write(file)
        return item
    def close_spider(self):
        self.file.close()
