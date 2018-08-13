# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class TianqiscrapyItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    cityName = scrapy.Field()#城市名
    cityAir =scrapy.Field()#城市空气状况
    cityTemperature = scrapy.Field()#城市温度
    cityStatus = scrapy.Field()#城市天气状况
    cityHumidity =scrapy.Field()#城市湿度
    cityWind = scrapy.Field()#城市风力
    cityPrompt = scrapy.Field()#提示
