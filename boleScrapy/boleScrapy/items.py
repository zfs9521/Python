# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class FirstscrapyItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title=scrapy.Field()
    tag=scrapy.Field()
    goodNum= scrapy.Field()
    saveNum= scrapy.Field()
    sayNum= scrapy.Field()
    article=scrapy.Field()
    img=scrapy.Field()

