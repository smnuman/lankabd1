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
    start_urls        = [
        'http://lankabd.com/analysis-tools/companies-statistics?siteLanguage=en&d-3724563-p=%s' % page for page in range(1,20,1)
    ]

    # Make it 'True' for error output from inside the module
    # else keep it 'False'
    BOT_DEBUG = False

    def parse(self, response):
        if response:
            if self.BOT_DEBUG:
                print "\tBOT[parse()]:(",response.status,"): ", response.url
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
                    fs_link             = '%25-'.join(fs_link.split('%-'))          # SPECIAL_CASE: removing faulty href in scraped data
                    if self.BOT_DEBUG and (ticker == "BRACSCBOND"):
                        print "\n\n\t......FINANCIAL LINK :[ ", fs_link," ]\n"
                    item['stockID']     = theLink.extract_first().split('=')[-1]
                    # save the extracted items
                    items.append(scrapy.Request(fs_link, callback=self.parse_further, meta={'item': item}))
            return items
        else:
            if self.BOT_DEBUG:
                print "\nparse(): BOT response failed ... \n\t[ status(",response.status,"): ", response.url, " ]\n"
            return

    def parse_further(self, response):
        if response:
            if self.BOT_DEBUG:
                print "\t\tparse_further() [TICKER]:(", response.status,"): ", response.url
            item = response.meta['item']
            HREF = response.css('#menu>li>a::attr(href)')[2].extract()
            item['link']     = response.urljoin(HREF)
            item['name']     = response.xpath('.//*[@id=\'pageTitle\']/h1[1]/text()').extract_first().split(' (')[-2].strip() #
            item['industry'] = response.css('.portalTitleL2 ::text').extract_first().split(' - ')[-2]
            yield item
        else:
            if self.BOT_DEBUG:
                print "\nBOT_ERR[parse_further()]: TICKER response failed ... \n\t[ status(", response.status,"): ", response.url," ]\n"
            return
