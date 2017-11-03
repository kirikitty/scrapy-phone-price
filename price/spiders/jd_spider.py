# -*- coding: utf-8 -*-

import scrapy
import json
import os
from price.spiders.utils import isnumber, replace_keyword
from urllib import quote
from price.items import PriceItem

class JdSpider(scrapy.spiders.Spider):
	name = "jd"
	allowed_domains = ["jd.com"]
	start_urls = []

	def __init__(self):
		self.models = self.load_model_csv('/Users/kiri/test/output/anjindai/models.csv')
		self.start_urls = self.models.keys()
		self.results = {}

	def parse(self, response):
		if not response.url in self.models:
			return

		model = self.models[response.url]
		count = 0
		for sel in response.xpath('//div[@id="J_goodsList"]/ul/li'):
			price = sel.css('.p-price').xpath('./strong/i/text()')[0].extract()
			name = u''.join(sel.css('.p-name').xpath('./a/em//text()').extract())
			web_id = sel.xpath('./@data-sku')[0].extract()
			url = sel.css('.p-name').xpath('./a/@href')[0].extract()
			if url.startswith('//'):
				url = u'https:' + url
			if isnumber(price):
				item = PriceItem()
				item['webId'] = web_id
				item['name'] = name
				item['brand'] = model['brand']
				item['model'] = model['model']
				item['price'] = int(float(price))
				item['url'] = url
				item['source'] = 'jd'
				count += 1
				yield item
		if count > 0:
			self.results[model['line']] = count

	def closed(self, reason):
		print 'jd closed, reason:'
		print reason
		print self.results
		with open(os.getcwd() + '/jd_stats.json', 'w') as f:
			json.dump(self.results, f)

	def load_model_csv(self, path):
		with open(path, 'r') as csv:
			lines = csv.readlines()
			models = {}
			for s in lines:
				comps = s.strip().split(',')
				if len(comps) == 2:
					device = {'line': s.strip(), 'brand': comps[0], 'model': comps[1]}
					keyword = ''
					if comps[0].lower() in comps[1].lower():
						keyword = comps[1]
					else:
						keyword = comps[0] + ' ' + comps[1]
					keyword = replace_keyword(keyword)
					keyword = quote(keyword)
					url = 'https://search.jd.com/Search?enc=utf-8&cid3=655&keyword=' + keyword
					models[url] = device
			return models
