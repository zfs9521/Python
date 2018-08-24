# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ScrapyspiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass
class jobsInfoSpiderItem(scrapy.Item):
    jobInfo1=scrapy.Field()#工作地点
    jobInfo2 = scrapy.Field()#工作经验
    jobInfo3 = scrapy.Field()#学历要求
    jobInfo4 = scrapy.Field()#融资阶段
    jobInfo5 = scrapy.Field()#行业领域
    jobInfo6 = scrapy.Field()#公司规模
    job=scrapy.Field()#岗位
    jobLink=scrapy.Field()#岗位链接
    companyLink=scrapy.Field()#公司链接
    address=scrapy.Field()#工作地点
    formatTime=scrapy.Field()#发布时间
    money=scrapy.Field()#薪资水平
    need1=scrapy.Field()#需要条件
    need2= scrapy.Field()
    companyName=scrapy.Field()#公司名称
    industry1 =scrapy.Field()#公司简介
    industry2 = scrapy.Field()
    industry3 = scrapy.Field()
    treatment=scrapy.Field()#公司待遇
    datetime=scrapy.Field()#获取信息时间

class jobsNeedsInfoSpiderItem(scrapy.Item):
    company=scrapy.Field()#公司
    job=scrapy.Field()
    jobRequest=scrapy.Field()#工作条件
    positionLabel=scrapy.Field()#职位标签
    jobAdvantage=scrapy.Field()#职位诱惑
    jbDescription=scrapy.Field()#工作描述
    jbAddress=scrapy.Field()#工作地址


class companyInfoSpiderItem(scrapy.Item):
    company=scrapy.Field()#公司
    companyWord=scrapy.Field()#公司语
    companyInfo=scrapy.Field()#公司基本信息
    companyManager=scrapy.Field()#公司管理者
    companyManagerInfo=scrapy.Field()#公司管理者信息
    companyLabel=scrapy.Field()#公司标签
