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


class CsdnSpider(RedisMixin, CrawlSpider):
    name = 'csdn'
    redis_key = 'csdn:start_urls'
    allowed_domains = ['blog.csdn.net']

    rules = (
        Rule(SgmlLinkExtractor(), callback='parse', follow=True),
    )

    def set_crawler(self, crawler):
        CrawlSpider.set_crawler(self, crawler)
        RedisMixin.setup_redis(self)

    def parse(self, response):
        sel = Selector(response)

        re_article_detail = re.compile("\/article\/details\/")

        if re_article_detail.search(response.url):
            title = sel.xpath('//div[@id="article_details"]/div[@class="article_title"]/h1/span/a/text()').extract()
            content = sel.xpath('//div[@id="article_details"]/div[@id="article_content"]/node()').extract()
            created = sel.xpath('//span[@class="link_postdate"]/text()').extract()

            item = ZiwuItem()
            item['url'] = response.url
            item['title'] = ''.join(title).strip()

            item_content = ''.join(content).strip()

            cleaner = Cleaner(page_structure=False, links=False, safe_attrs_only=True, safe_attrs = frozenset([]))
            clean_content = cleaner.clean_html(item_content)
            item['content'] = clean_content
            item['description'] = filter_tags(clean_content)

            item['created'] = datetime.datetime.strptime(''.join(created).strip(), "%Y-%m-%d %H:%M")
            item['type'] = 1
            item['pagerank'] = 1

            yield item

        else:
            urlposts = sel.xpath('//div[@class="article_title"]/h1/span/a/@href').extract()
            urlpages = sel.xpath('//div[@id="papelist"]/a/@href').extract()

            urls = urlposts + urlpages

            for url in urls:
                utf8_url = url.encode('utf-8')
                base_url = get_base_url(response)

                if not utf8_url.startswith('http://'):
                    url = urljoin_rfc(base_url, utf8_url)

                yield Request(url, callback=self.parse)
