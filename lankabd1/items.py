# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class Lankabd1Item(scrapy.Item):
    # define the fields for your item here like:
    ticker = scrapy.Field()
    name = scrapy.Field()
    link = scrapy.Field()
    stockID = scrapy.Field()
    industry = scrapy.Field()

    # http://stackoverflow.com/a/20602179/2378780
    def keys(self):
        return ['industry', 'stockID', 'ticker', 'name'] # , 'link']
