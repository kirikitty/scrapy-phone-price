# -*- coding: utf-8 -*-

import scrapy
import json
import os
import urllib2
from price.spiders.utils import isnumber, replace_keyword
from urllib import quote
from price.items import DetailItem

# https://c0.3.cn/stock?skuId=12693782459&area=1_72_2799_0&venderId=174907&cat=9987,653,655&extraParam={%22originid%22:%221%22}
# https://p.3.cn/prices/mgets?skuIds=J_12693782459
# https://club.jd.com/comment/productCommentSummaries.action?referenceIds=12693782459
#

class JdDetailSpider(scrapy.spiders.Spider):
	name = "jd_detail"
	allowed_domains = ["jd.com"]
	start_urls = []
	count = 0

	def __init__(self):
		self.models = self.load_model_json(os.getcwd() + '/jd_items.json')
		self.start_urls = self.models.keys()

	def parse(self, response):
		if not response.url in self.models:
			return

		model = self.models[response.url]

		next_is_brand = False
		next_is_model = False
		item = {'webId': model['webId'], 'brand': model['brand'], 'model': model['model']}
		for sel in response.css('.Ptable-item').xpath('.//dt | .//dd'):
			if sel.xpath('./@class'):
				continue
			text = sel.xpath('./text()')[0].extract()
			if sel.extract().startswith('<dt>'):
				if text == u'品牌':
					next_is_brand = True
				elif text == u'型号':
					next_is_model = True
			if sel.extract().startswith('<dd>'):
				if next_is_brand:
					item['webBrand'] = text
					next_is_brand = False
				elif next_is_model:
					if not text == u'以官网信息为准':
						item['webModel'] = text
					next_is_model = False
			if len(item) == 5:
				break
		if len(item) > 3:
			self.count += 1
			yield DetailItem(item)

	def closed(self, reason):
		print 'jd closed, reason:'
		print reason
		print 'get item details: ' + str(self.count)

	def load_model_json(self, path):
		with open(path, 'r') as f:
			obj = json.load(f)
			models = {}
			for m in obj:
				key = m[u'url']
				models[key] = m
			return models
