# -*- coding: utf-8 -*-

import scrapy

from lankabd1.items import Lankabd1Item

class LankaSpider(scrapy.Spider):
    name              = "lanka"
    allowed_domains   = ["lankabd.com"]
    start_urls        = [
        'http://lankabd.com/analysis-tools/companies-statistics?siteLanguage=en&d-3724563-p=%s' % page for page in range(1,20,1)
    ]


    def parse(self, response):
        if response:
            items = []
            # selectors
            COMPANY_TICKER_SELECTOR = 'td[1]/a/text()'
            COMPANY_LINK_SELECTOR   = 'td[1]/a/@href'
            # take all the rows containing company informations
            COMPANY_SELECTOR        = '//*[@id=\'oneStatistics\']//tbody/tr'
            companies               = response.xpath(COMPANY_SELECTOR)
            for company in companies:
                item    = Lankabd1Item()
                theLink = company.xpath(COMPANY_LINK_SELECTOR)
                ticker  = company.xpath(COMPANY_TICKER_SELECTOR).extract_first()
                if ticker is not None:
                    item['ticker']  = ticker
                    fs_link         = response.urljoin(theLink.extract_first()) # http://stackoverflow.com/a/39024960/2378780
                    fs_link         = '%25-'.join(fs_link.split('%-'))          # SPECIAL_CASE: removing faulty href in scraped data
                    item['stockID'] = theLink.extract_first().split('=')[-1]
                    # fetch & save some more extracted items
                    response_parse_further = scrapy.Request(fs_link, callback=self.parse_further, meta={'item': item})
                    items.append(response_parse_further)
            return items

    def parse_further(self, response):
        # pf_items = []
        item = response.meta['item']

        if response:
            HREF_CSS_SELECTOR     = '#menu>li>a::attr(href)'
            NAME_XPATH_SELECTOR   = './/*[@id=\'pageTitle\']/h1[1]/text()'
            INDUSTRY_CSS_SELECTOR = '.portalTitleL2 ::text'

            HREF             = response.css(HREF_CSS_SELECTOR)[2].extract()
            HREF             = '%25-'.join(HREF.split('%-'))          # SPECIAL_CASE: removing faulty href in scraped data

            item['url']      = response.urljoin(HREF)
            item['name']     = response.xpath(NAME_XPATH_SELECTOR).extract_first().split(' (')[-2].strip() #
            item['industry'] = response.css(INDUSTRY_CSS_SELECTOR).extract_first().split(' - ')[-2]
            return [scrapy.Request(response.urljoin(HREF), callback=self.parse_table, meta={'item': item})]

            # print "\n\t\t[PF]:Fetching table for ",item['ticker'], " from ", HREF
            # response_parse_table = scrapy.Request(item['url'], callback=self.parse_table, meta={'item2': item})
            # print "\t\t\t", type(response_parse_table), " & pf_items - ", type(pf_items)
            # pf_items.append(response_parse_table)
            # print "\t\t... table fetched!\n"
        # else:
        #     yield item
        # yield pf_items

    def parse_table(self, response):
        item = response.meta['item']
        if response:
            # YEAREND_XPATH = "//*[@id='sampleForm']/h1/span[3]/font/text()"
            # item['yearEnd'] = response.xpath(YEAREND_XPATH).extract_first()
            YEAREND_CSS = '.note>font ::text'
            item['yearEnd'] = response.css(YEAREND_CSS).extract_first()
        return [item]
