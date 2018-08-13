# -*- coding: utf-8 -*-
import scrapy
from scrapyPro.boleScrapy.boleScrapy.items import FirstscrapyItem
class BoleSpider(scrapy.Spider):
    name = 'bole'
    start_urls = ['http://blog.jobbole.com/all-posts/']

    def parse(self, response):

        divList=response.css('.post.floated-thumb')
        for div in divList:
            href=div.css('.archive-title::attr(href)').extract_first('')
            print(href)
            img=div.css('img::attr(src)').extract_first('')
            yield scrapy.http.Request(href,meta={'post-img':img},callback=self.parse_dea)
        next_url=response.css('.next.page-numbers::attr(href)').extract_first('')
        if next_url:
            yield scrapy.http.Request(next_url,callback=self.parse)

    def parse_dea(self,response):
        dicts=FirstscrapyItem()
        title=response.css('title::text').extract_first('')
        # print(title)
        tag=response.css('.entry-meta-hide-on-mobile a::text').extract()
        # print(tag)
        goodNum=response.css('h10::text').extract_first('')
        # print(goodNum)
        saveNum=response.css('span[data-book-type="1"]::text').extract_first('')
        # print(saveNum)
        sayNum=response.css('.btn-bluet-bigger.href-style.hide-on-480::text').extract_first('')
        # print(sayNum)
        articles=response.css('.entry p::text,li::text,h2::text').extract()
        article=''
        for string in articles:
            article+=string
        article.strip()
        # print(article)
        img=response.meta.get('post-img')
        dicts['title']=title
        dicts['tag']=tag
        dicts['goodNum']=goodNum
        dicts['saveNum']=saveNum
        dicts['sayNum']=sayNum
        dicts['article']=article
        dicts['img']=[img]
        yield dicts

