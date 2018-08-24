# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapys.scrapySpider.scrapySpider.items import jobsInfoSpiderItem
from scrapys.scrapySpider.scrapySpider.items import jobsNeedsInfoSpiderItem
from scrapys.scrapySpider.scrapySpider.items import companyInfoSpiderItem
from datetime import  datetime
class LagouSpider(CrawlSpider):
    name = 'lagou'
    # allowed_domains = ['www.baidu.com']
    start_urls = ['https://www.lagou.com/']

    rules = (
        Rule(LinkExtractor(allow='zhaopin/.*'), callback='jobsInfo', follow=True),
        Rule(LinkExtractor(allow='jobs/\d+\.html'), callback='jobNeedsInfo', follow=True),
        # Rule(LinkExtractor(allow='gongsi/\d+\.html'), callback='companyInfo', follow=True),
    )


    def jobsInfo(self,response):
        jobInfo=response.css('#filterBrief a::text').extract()#职位要求
        jobInfo1=jobInfo[0]#工作地点
        jobInfo2 = jobInfo[1]#工作经验
        jobInfo3 = jobInfo[2]#学历要求
        jobInfo4 = jobInfo[3]#融资阶段
        jobInfo5 = jobInfo[4]#行业领域
        jobInfo6 = jobInfo[5]#公司规模
        job = response.css('.position_link h3::text').extract()  # 岗位具体
        jobLink=response.css('.position_link::attr(href)').extract()
        address = response.css('.position_link em::text').extract()  # 工作地点
        formatTime = response.css('.format-time::text').extract()  # 发布时间
        money = response.css('.money::text').extract()  # 薪资水平
        need = response.css('.p_bot div::text').extract()  # 需要条件
        companyName = response.css('.company_name a::text').extract()  # 公司名称
        companyLink=response.css('.company_name a::attr(href)').extract()
        industry = response.css('.company .industry::text').extract()#公司简介

        treatment = response.css('.li_b_r::text').extract()  # 公司待遇
        items=jobsInfoSpiderItem()
        for index in range(len(job)):
            items['jobInfo1']=jobInfo1.strip()
            items['jobInfo2'] = jobInfo2.strip()
            items['jobInfo3'] = jobInfo3.strip()
            items['jobInfo4'] = jobInfo4.strip()
            items['jobInfo5'] = jobInfo5.strip()
            items['jobInfo6'] = jobInfo6.strip()
            items['job']=job[index].strip()
            items['jobLink']=jobLink[index]
            items['address']=address[index].strip()
            items['formatTime']=formatTime[index].strip()
            items['money']=money[index].strip()
            if need[index].strip()=='':
                items['need1']='无'
                items['need2']='无'
            else:
                needs=need[index].split('/')
                items['need1']=needs[0].strip()
                items['need2']=needs[1].strip()
            items['companyName']=companyName[index].strip()
            splits = industry[index].split('/') # 公司简介
            industry1 = splits[0]
            industry2 = splits[1]
            industry3 = splits[2]
            items['industry1']=industry1.strip()
            items['industry2'] = industry2.strip()
            items['industry3'] = industry3.strip()
            items['companyLink']=companyLink[index].strip()
            items['treatment']=treatment[index].strip()
            items['datetime']=datetime.now()#获取时间
            yield items



    def jobNeedsInfo(self,response):
        company = response.css('.company::text').extract_first('')  # 公司
        job=response.css('.job-name span::text').extract_first('')#职位
        jobRequestList = response.css('.job_request span::text').extract()
        jobRequest=''
        for o in jobRequestList:
            jobRequest+=o# 工作条件
        positionLabelList = response.css('.labels::text').extract()
        positionLabel=''
        for o in positionLabelList:
            positionLabel+=o+'/'# 职位标签
        jobAdvantage = response.css('.job-advantage p::text').extract_first('') # 职位诱惑
        jbDescriptionList = response.css('.job_bt p::text').extract()
        jbDescription=''
        for o in jbDescriptionList:
            jbDescription+=o# 工作描述
        jbAddressList = response.css('.work_addr a::text').extract()
        jbAddress=''
        for o in jbAddressList:
            jbAddress+=o# 工作地址
        item=jobsNeedsInfoSpiderItem()
        item['company'] = company.strip()  # 公司
        item['job']=job.strip()
        item['jobRequest'] = jobRequest.strip() # 工作条件
        item['positionLabel'] = positionLabel.strip()  # 职位标签
        item['jobAdvantage'] = jobAdvantage.strip()  # 职位诱惑
        item['jbDescription'] = jbDescription.strip()  # 工作描述
        item['jbAddress'] = jbAddress.strip()  # 工作地址
        yield item


    def companyInfo(self,response):
        company = scrapy.Field()  # 公司
        companyWord = scrapy.Field()  # 公司语
        companyInfo = scrapy.Field()  # 公司基本信息
        companyManager = scrapy.Field()  # 公司管理者
        companyManagerInfo = scrapy.Field()  # 公司管理者信息
        companyLabel = scrapy.Field()  # 公司标签

        company = scrapy.Field()  # 公司
        companyWord = scrapy.Field()  # 公司语
        companyInfo = scrapy.Field()  # 公司基本信息
        companyManager = scrapy.Field()  # 公司管理者
        companyManagerInfo = scrapy.Field()  # 公司管理者信息
        companyLabel = scrapy.Field()  # 公司标签
