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
from ziwu.misc.util import filter_tags

from ziwu.items import ZiwuItem

import re
import datetime


class EsribbsSpider(RedisMixin, CrawlSpider):
    name = 'esribbs'
    redis_key = 'esribbs:start_urls'
    allowed_domains = ['bbs.esrichina-bj.cn', 'www.gisall.com']

    rules = (
        Rule(SgmlLinkExtractor(), callback='parse', follow=True),
    )

    def set_crawler(self, crawler):
        CrawlSpider.set_crawler(self, crawler)
        RedisMixin.setup_redis(self)

    def parse(self, response):
        sel = Selector(response)

        re_fid_bj = re.compile("bbs\.esrichina\-bj\.cn\/ESRI\/archiver\/\?fid\-")
        re_tid_bj = re.compile("bbs\.esrichina\-bj\.cn\/ESRI\/archiver\/\?tid\-")
        re_item_bj = re.compile("bbs\.esrichina\-bj\.cn\/ESRI\/viewthread\.php\?tid")

        re_fid_gisall = re.compile("www\.gisall\.com\/archiver\/\?fid\-")
        re_tid_gisall = re.compile("www\.gisall\.com\/archiver\/\?tid\-")
        re_item_gisall = re.compile("www\.gisall\.com\/forum\.php\?mod\=viewthread\&tid\=")

        if re_fid_bj.search(response.url) or re_fid_gisall.search(response.url):
            urlposts = sel.xpath('//div[@id="content"]/ul/li/a/@href').extract()

            for url in urlposts:
                utf8_url = url.encode('utf-8')
                base_url = get_base_url(response)

                if not utf8_url.startswith('http://'):
                    url = urljoin_rfc(base_url, utf8_url)

                yield Request(url, callback=self.parse)

            urlpages = sel.xpath('//div[@id="content"]/div[@class="page"]/a/@href').extract()

            for url in urlpages:
                utf8_url = url.encode('utf-8')
                base_url = get_base_url(response)

                if not utf8_url.startswith('http://'):
                    url = urljoin_rfc(base_url, utf8_url)

                yield Request(url, callback=self.parse)

        elif re_tid_bj.search(response.url):
            title = sel.xpath('//title/text()').extract()
            content = sel.xpath('//div[@id="content"]/node()').extract()
            urls = sel.xpath('//div[@id="footer"]/strong/a/@href').extract()

            if len(content) != 0:
                item = ZiwuItem()
                item['title'] = ''.join(title).strip()

                item_content = ''.join(content).strip()

                cleaner = Cleaner(page_structure=False, links=False, safe_attrs_only=True, safe_attrs = frozenset([]))
                clean_content = cleaner.clean_html(item_content)
                item['content'] = clean_content
                item['description'] = filter_tags(clean_content)

                for url in urls:
                    utf8_url = url.encode('utf-8')
                    base_url = get_base_url(response)

                    if not utf8_url.startswith('http://'):
                        url = urljoin_rfc(base_url, utf8_url)
                        item['url'] = url

                item['created'] = datetime.datetime.strptime('1900-1-1 00:00', "%Y-%m-%d %H:%M")
                item['type'] = 1
                item['pagerank'] = 1

                yield item

        elif re_tid_gisall.search(response.url):
            title = sel.xpath('//title/text()').extract()
            content = sel.xpath('//div[@id="content"]/node()').extract()
            urls = sel.xpath('//div[@id="end"]/a/@href').extract()

            if len(content) != 0:
                item = ZiwuItem()
                item['title'] = ''.join(title).strip()

                item_content = ''.join(content).strip()

                cleaner = Cleaner(page_structure=False, links=False, safe_attrs_only=True, safe_attrs = frozenset([]))
                clean_content = cleaner.clean_html(item_content)

                item['content'] = clean_content
                item['description'] = filter_tags(clean_content)

                for url in urls:
                    utf8_url = url.encode('utf-8')
                    base_url = get_base_url(response)

                    if not utf8_url.startswith('http://'):
                        url = urljoin_rfc(base_url, utf8_url)
                        item['url'] = url

                        # yield Request(url, callback=self.parse)

                item['created'] = datetime.datetime.strptime('1900-1-1 00:00', "%Y-%m-%d %H:%M")
                item['type'] = 1
                item['pagerank'] = 1

                yield item

        # elif re_item.search(response.url):
        #     title = sel.xpath('//title/text()').extract()
        #     content = sel.xpath('//div[@class="postmessage firstpost"]/div[@class="t_msgfontfix"]/table/tr/td[@class="t_msgfont"]/text()').extract()

        #     if len(content) != 0:
        #         item = ZiwuItem()
        #         item['url'] = response.url
        #         item['title'] = ''.join(title).strip()

        #         item_content = ''.join(content).strip()

        #         cleaner = Cleaner(page_structure=False, links=False, safe_attrs_only=True, safe_attrs = frozenset([]))
        #         clean_content = cleaner.clean_html(item_content)

        #         item['content'] = clean_content

        #         item['type'] = 1

        #         yield item
