#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ziwu.components.redis.spiders import RedisMixin

from scrapy.selector import Selector
from scrapy.http import Request

from scrapy.utils.response import get_base_url
from scrapy.utils.url import urljoin_rfc

from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor

from lxml.html.clean import Cleaner

from ziwu.items import ZiwuItem

import re

class S3newsSpider(RedisMixin, CrawlSpider):
    name = 's3news'
    redis_key = 'ziwu:start_urls'
    allowed_domains = ["blog.csdn.net"]

    rules = (
        # follow all links
        Rule(SgmlLinkExtractor(), callback='parse', follow=True),
    )

    def set_crawler(self, crawler):
        CrawlSpider.set_crawler(self, crawler)
        RedisMixin.setup_redis(self)

    def parse(self, response):
        sel = Selector(response)

        # urls = sel.xpath('//@href').extract()
        urls = sel.xpath('//li[@class="next_article"]/a/@href').extract()

        item = ZiwuItem()
        item['url'] = response.url
        item['title'] = ''.join(sel.xpath('//div[@id="article_details"]/div[@class="article_title"]/h1/span/a/text()').extract())

        itemcontent = ''.join(sel.xpath('//div[@id="article_details"]/div[@id="article_content"]/node()').extract())

        cleaner = Cleaner(page_structure=False, links=False, safe_attrs_only=True, safe_attrs = frozenset([]))
        cleansed = cleaner.clean_html(itemcontent)

        item['content'] = cleansed

        yield item

        for url in urls:
            utf8_url = url.encode('utf-8')
            base_url = get_base_url(response)

            """The following regex to match the prefix and postfix of urls"""
            postfix = re.compile(r'.+\.((jpg)|(ico)|(rar)|(zip)|(doc)|(ppt)|(xls)|(css)|(exe)|(pdf))x?$')
            prefix = re.compile(r'^((javascript:)|(openapi)).+')

            if postfix.match(utf8_url):
                continue
            if prefix.match(utf8_url):
                continue
            if not utf8_url.startswith('http://'):
                weburl = urljoin_rfc(base_url, utf8_url)

            yield Request(weburl, callback=self.parse)
