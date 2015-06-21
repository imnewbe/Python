#! /usr/bin/env python
import scrapy
from twisted.internet import reactor
from scrapy.contrib.spiders import CrawlSpider,Rule
from scrapy.contrib.linkextractors import LinkExtractor
class MySpider(CrawlSpider):
	name = '2'
	allow = ['bbs.tianyan.cn']
	star = ['http://bbs.tianya.cn/post-16-1023511-1.shtml']
	rules = (Rule(LinkExtractor(allow=('bbs.tianya.cn/post-16-1023511-\d+')),'parse_item',follow=True))
	def parse_item(self, response):
		item=downItem()
		item['text']=response.xpath('//div[@class="bbs-content"]')
		return item
class downItem(scrapy.Item):
	text= scrapy.Field()



