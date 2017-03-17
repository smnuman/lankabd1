# -*- coding: utf-8 -*-
# from scrapy.contrib.spiders import CrawlSpider, Rule
# from scrapy.linkextractors import LinkExtractor as LE
#
# from lankabd1.items import Lankabd1Item
#
# class LankaSpider(CrawlSpider):
#     name              = "lanka"
#     allowed_domains   = ["lankabd.com"]
#     start_urls        = ['http://lankabd.com/analysis-tools/companies-statistics']
#
#     rules             = (
#         # http://disq.us/p/to4tg5
#         Rule(LE(allow = (), restrict_xpaths=('//a[@id="HistoricalMostActiveStocks"]',)), callback="parse_items"),
#         Rule(LE(allow = (), restrict_xpaths=('//a[@class="nextPage"]',)), callback="parse_items", follow=True),
#     )
#
#     def parse_items(self, response):
#         items = []
#         # take all the rows containing company informations
#         COMPANY_SELECTOR = '//*[@id=\'oneStatistics\']//tbody/tr'
#
#         for company in response.xpath(COMPANY_SELECTOR):
#             item = Lankabd1Item()
#             # selectors
#             COMPANY_NAME_SELECTOR = 'td[1]/a/text()'
#             # COMPANY_LINK_SELECTOR = 'td[1]/a/@href'
#             COMPANY_LINK_SELECTOR = 'td[1]/a/@href'
#             # scrape rows for intended info
#             theLink         = company.xpath(COMPANY_LINK_SELECTOR)
#             item['name']    = company.xpath(COMPANY_NAME_SELECTOR).extract_first()
#             # http://stackoverflow.com/a/39024960/2378780
#             item['link']    = response.urljoin(theLink.extract_first())
#             item['stockID'] = theLink.extract_first().split('=')[-1]
#             # save the extracted items
#             items.append(item)
#
#         return items
#
#
#
# http://lankabd.com/analysis-tools/companies-statistics?d-3724563-p=2&siteLanguage=en>

import scrapy

from lankabd1.items import Lankabd1Item

class LankaSpider(scrapy.Spider):
    name              = "lanka"
    allowed_domains   = ["lankabd.com"]
    start_urls        = ['http://lankabd.com/analysis-tools/companies-statistics?siteLanguage=en&d-3724563-p=%s' % page for page in range(1,25,1)]


    def parse(self, response):
        items            = []
        # take all the rows containing company informations
        COMPANY_SELECTOR = '//*[@id=\'oneStatistics\']//tbody/tr'
        companies        = response.xpath(COMPANY_SELECTOR)
        for company in companies:
            item         = Lankabd1Item()
            # selectors
            COMPANY_TICKER_SELECTOR = 'td[1]/a/text()'
            COMPANY_LINK_SELECTOR   = 'td[1]/a/@href'
            # scrape rows for intended info
            theLink                 = company.xpath(COMPANY_LINK_SELECTOR)
            ticker                  = company.xpath(COMPANY_TICKER_SELECTOR).extract_first()
            if ticker is not None:
                item['ticker']      = ticker
                # http://stackoverflow.com/a/39024960/2378780
                fs_link             = response.urljoin(theLink.extract_first())
                item['stockID']     = theLink.extract_first().split('=')[-1]
                # save the extracted items
                items.append(scrapy.Request(fs_link, callback=self.parse_further, meta={'item': item}))
        return items

    def parse_further(self, response):
        item = response.meta['item']
        HREF = response.css('#menu>li>a::attr(href)')[2].extract()
        item['link']     = response.urljoin(HREF)
        item['name']     = response.xpath('.//*[@id=\'pageTitle\']/h1[1]/text()').extract_first().split(' (')[-2].strip() #
        item['industry'] = response.css('.portalTitleL2 ::text').extract_first().split(' - ')[-2]
        yield item
