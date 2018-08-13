# -*- coding: utf-8 -*-
import scrapy
import re
from scrapy.http import Request
from urllib import parse
from ArticleSpider.items import JobBoleArticleItem
from ArticleSpider.utils.common import get_md5
import datetime


class JobboleSpider(scrapy.Spider):
    name = 'jobbole'
    allowed_domains = ['blog.jobbole.com']
    start_urls = ['http://blog.jobbole.com/all-posts/']

    # def parse(self, response):
    # 	'''
    # 	1.获取文章列表页中的文章url并交给scrapy下载后并进行解析
    # 	2.获取下一页的url并交给scrapy进行下载,下载完成后交给parse
    # 	'''
    # 	post_urls = response.css('#archive .post.floated-thumb .post-thumb a::attr(href)').extract()
    # 	for post_url in post_urls:
    # 		#response.url即start_urls
    # 		# yield Request(url = post_url,callback = self.parse_detail)
    # 		#urljoin从相对路径获取绝对路径,第一个参数为绝对路径,第二个为相对路径
    # 		yield Request(url = parse.urljoin(response.url,post_url),callback = self.parse_detail)
    # 	next_urls = response.css('.next.page-numbers::attr(href)').extract()
    # 	if next_urls:
    # 		yield Request(url = parse.urljoin(response.url,post_url),callback= self.parse)
    # 		# yield Request(url = next_urls,callback= self.parse)
    # 	#提取下一页并交给scarpy进行下载





    def parse(self, response):
        """
                1. 获取文章列表页中的文章url并交给scrapy下载后并进行解析
                2. 获取下一页的url并交给scrapy进行下载， 下载完成后交给parse
                """
        # 解析列表页中的所有文章url并交给scrapy下载后并进行解析
        post_nodes = response.css("#archive .floated-thumb .post-thumb a")
        # post_urls = response.css("#archive .floated-thumb .post-thumb a::attr(href)").extract()
        for post_node in post_nodes:
            # request下载完成之后，回调parse_detail进行文章详情页的解析
            image_url = post_node.css("img::attr(src)").extract_first("")
            post_url = post_node.css("::attr(href)").extract_first("")
            yield Request(url=parse.urljoin(response.url, post_url), meta={"front_image_url": image_url},
                          callback=self.parse_detail)
            # 遇到href没有域名的解决方案
            # response.url + post_url
            print(post_url)
        # 提取下一页并交给scrapy进行下载
        next_url = response.css(".next.page-numbers::attr(href)").extract_first("")
        if next_url:
            yield Request(url=parse.urljoin(response.url, post_url), callback=self.parse)





    def parse_detail(self, response):
        article_item = JobBoleArticleItem()
        front_image_url = response.meta.get("front_image_url", "")  # 文章封面图
        title = response.css(".entry-header h1::text").extract_first()
        create_date = response.css(
            "p.entry-meta-hide-on-mobile::text").extract()[0].strip().replace("·", "").strip()
        praise_nums = response.css(".vote-post-up h10::text").extract()[0]
        fav_nums = response.css(".bookmark-btn::text").extract()[0]
        match_re = re.match(".*?(\d+).*", fav_nums)
        if match_re:
            fav_nums = int(match_re.group(1))
        else:
            fav_nums = 0
        comment_nums = response.css(
            "a[href='#article-comment'] span::text").extract()[0]
        match_re = re.match(".*?(\d+).*", comment_nums)
        if match_re:
            comment_nums = int(match_re.group(1))
        else:
            comment_nums = 0
        content = response.css("div.entry").extract()[0]

        tag_list = response.css(
            "p.entry-meta-hide-on-mobile a::text").extract()
        tag_list = [
            element for element in tag_list if not element.strip().endswith("评论")]
        tags = ",".join(tag_list)

		# 为实例化后的对象填充值
        article_item["url_object_id"] = get_md5(response.url)
        article_item["title"] = title
        article_item["url"] = response.url
        try:
            create_date = datetime.datetime.strptime(create_date, "%Y/%m/%d").date()
        except Exception as e:
            create_date = datetime.datetime.now().date()
        article_item["create_date"] = create_date
        article_item["front_image_url"] = [front_image_url]
        article_item["praise_nums"] = praise_nums
        article_item["comment_nums"] = comment_nums
        article_item["fav_nums"] = fav_nums
        article_item["tags"] = tags
        article_item["content"] = content
        yield article_item

        '''
		以下为用css选择器提取数据

		title = response.css(".entry-header h1::text").extract_first()
		#p可以不加
		create_date = response.css("p.entry-meta-hide-on-mobile::text").extract()[0].strip().replace('·','').strip()
		#获取点赞数
		praise_nums = response.css('#110287votetotal::text').extract()[0]
		#获取收藏数
		fav_nums = response.css('.btn-bluet-bigger.href-style.bookmark-btn .register-user-only::text ').extract()[0].strip()
		match_re = re.match('.*?(\d+).*',fav_nums)
		if match_re:
			#获取收藏数
			fav_nums = match_re.group(1)
		comment_nums = response.css('.btn-bluet-bigger.href-style.hide-on-480::text').extract()[0].strip()
		match_re = re.match('.*?(\d+).*',fav_nums)
		if match_re:
			comment_nums = match_re.group(1)
		tag_list = response.css('.entry-meta-hide-on-mobile a::text').extract()
		content = response.css('div.entry').extract()[0]
		tag_list = [element for element in tag_list if not element.strip().endswith('评论')]
		tag = ','.join(tag_list)
		'''


