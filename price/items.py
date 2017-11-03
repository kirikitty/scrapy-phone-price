# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class PriceItem(scrapy.Item):
    # define the fields for your item here like:
    webId = scrapy.Field()
    name = scrapy.Field()
    brand = scrapy.Field()
    model = scrapy.Field()
    price = scrapy.Field()
    url = scrapy.Field()
    source = scrapy.Field()
    pass

class DetailItem(scrapy.Item):
    webId = scrapy.Field()
    webBrand = scrapy.Field()
    webModel = scrapy.Field()
    brand = scrapy.Field()
    model = scrapy.Field()
    commentCount = scrapy.Field()
