# -*- coding: utf-8 -*-

import scrapy
import json
import os
from price.items import PriceItem
from urllib import quote
from price.spiders.utils import isnumber, replace_keyword

class ZolSpider(scrapy.spiders.Spider):
	name = "zol"
	allowed_domains = ["zol.com.cn"]
	start_urls = []
	cookie = {
		'ip_ck':'5cWC5Pz3j7QuMjIzMzYwLjE0NzE4Mjg2OTg=',
		'__gads':'ID=39bc8b32c4293282:T=1471828698:S=ALNI_Ma6sEAy58b-vSLZiMWARy2TS1BXZg',
		'listSubcateId':'57',
		'Hm_lvt_ae5edc2bc4fc71370807f6187f0a2dd0':'509437064,1509526961',
		'Hm_lpvt_ae5edc2bc4fc71370807f6187f0a2dd0':'1509530224'
	}

	def __init__(self):
		self.models = self.load_model_csv('/Users/kiri/test/output/anjindai/models.csv')
		self.start_urls = self.models.keys()
		self.results = {}

	def start_requests(self):
		for url in self.start_urls:
			yield scrapy.Request(url,cookies=self.cookie)

	def parse(self, response):
		if not response.url in self.models:
			return
			
		#response.body.decode(response.encoding)
		model = self.models[response.url]
		count = 0
		for sel in response.css('.list-item'):
			name = sel.css('.pro-intro').xpath('./h3/a')[0]
			url = u'http://detail.zol.com.cn' + name.xpath('./@href')[0].extract()
			web_id = name.xpath('./@id')[0].extract()[8:]
			name = u''.join(name.xpath('.//text()').extract())
			price = sel.css('.price-type').xpath("./text()")[0].extract()
			if isnumber(price):
				item = PriceItem()
				item['webId'] = web_id
				item['name'] = name
				item['brand'] = model['brand']
				item['model'] = model['model']
				item['price'] = int(float(price))
				item['url'] = url
				item['source'] = 'zol'
				count += 1
				yield item
		if count > 0:
			self.results[model['line']] = count

	def closed(self, reason):
		print 'zol closed, reason:'
		print reason
		print self.results
		with open(os.getcwd() + '/zol_stats.json', 'w') as f:
			json.dump(self.results, f)

	def load_model_csv(self, path):
		csv = open(path, 'r')
		lines = csv.readlines()
		csv.close()
		urls = {}
		for s in lines:
			comps = s.strip().split(',')
			if len(comps) == 2:
				device = {'line': s.strip(), 'brand': comps[0], 'model': comps[1]}
				keyword = ''
				if comps[0].lower() in comps[1].lower():
					keyword = comps[1]
				else:
					keyword = comps[0] + '+' + comps[1]
				keyword = keyword.replace(' ', '+')
				keyword = replace_keyword(keyword)
				keyword = quote(keyword)
				url = 'http://detail.zol.com.cn/index.php?c=SearchList&subcateId=57&keyword=' + keyword
				urls[url] = device
		return urls

