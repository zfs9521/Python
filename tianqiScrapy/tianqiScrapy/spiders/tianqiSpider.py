# -*- coding: utf-8 -*-
import scrapy
from scrapyPro.tianqiScrapy.tianqiScrapy.items import TianqiscrapyItem

class TianqiSpider(scrapy.Spider):
    name = 'tianqiSpider'
    start_urls = ['https://tianqi.moji.com/weather/china']

    def parse(self, response):
        hrefList=response.css('.city_list.clearfix a::attr(href)').extract()
        for href in hrefList:
            url='https://tianqi.moji.com/'+href
            yield scrapy.http.Request(url,callback=self.parse_city)
    def parse_city(self,response):
        hrefList=response.css('.city_hot a::attr(href)').extract()
        for href in hrefList:
            yield scrapy.http.Request(href,callback=self.city_tianqi)
    def city_tianqi(self,response):
        cityName=response.css('.search_default em::text').extract_first('')
        cityAir=response.css('.wea_alert.clearfix em::text').extract_first('')
        cityTemperature=response.css('.wea_weather.clearfix em::text').extract_first('')
        cityStatus=response.css('.wea_weather.clearfix b::text').extract_first('')
        cityHumidity=response.css('.wea_about.clearfix span::text').extract_first('')
        cityWind=response.css('.wea_about.clearfix em::text').extract_first('')
        cityPrompt=response.css('.wea_tips.clearfix em::text').extract_first('')
        tianqiSpider=TianqiscrapyItem()
        tianqiSpider['cityName']=cityName
        tianqiSpider['cityAir'] = cityAir
        tianqiSpider['cityTemperature'] = cityTemperature
        tianqiSpider['cityStatus'] = cityStatus
        tianqiSpider['cityHumidity'] = cityHumidity
        tianqiSpider['cityWind'] = cityWind
        tianqiSpider['cityPrompt'] = cityPrompt
        yield tianqiSpider

