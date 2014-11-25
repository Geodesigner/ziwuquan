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


class CnblogSpider(RedisMixin, CrawlSpider):
    name = 'cnblog'
    redis_key = 'cnblog:start_urls'
    allowed_domains = ['zzk.cnblogs.com', 'www.cnblogs.com', 'kb.cnblogs.com', 'q.cnblogs.com']

    rules = (
        Rule(SgmlLinkExtractor(), callback='parse', follow=True),
    )

    def set_crawler(self, crawler):
        CrawlSpider.set_crawler(self, crawler)
        RedisMixin.setup_redis(self)

    def parse(self, response):
        sel = Selector(response)

        re_article_list = re.compile("zzk\.cnblogs\.com\/s\?w\=")

        if re_article_list.search(response.url):
            urlposts = sel.xpath('//div[@class="searchItem"]/h3[@class="searchItemTitle"]/a/@href').extract()
            urlpages = sel.xpath('//div[@id="paging_block"]/div[@class="pager"]/a/@href').extract()

            urls = urlposts + urlpages

            for url in urls:
                utf8_url = url.encode('utf-8')
                base_url = get_base_url(response)

                if not utf8_url.startswith('http://'):
                    url = urljoin_rfc(base_url, utf8_url)

                yield Request(url, callback=self.parse)
                # yield Request(url, meta={'renderjs': "true"}, callback=self.parse)

        else:
            title = sel.xpath('//*[@id="cb_post_title_url"]/text()').extract()
            content = sel.xpath('//*[@id="cnblogs_post_body"]/node()').extract()
            created = sel.xpath('//*[@id="post-date"]/text()').extract()

            if len(content) != 0:
                item = ZiwuItem()
                item['url'] = response.url

                if len(title) == 0:
                    title = sel.xpath('//title/text()').extract()

                item['title'] = ''.join(title).strip()

                item_content = ''.join(content).strip()

                cleaner = Cleaner(page_structure=False, links=False, safe_attrs_only=True, safe_attrs = frozenset([]))
                clean_content = cleaner.clean_html(item_content)
                item['content'] = clean_content
                item['description'] = filter_tags(clean_content)

                if len(created) == 0:
                    created = ['1900-1-1 00:00']

                item['created'] = datetime.datetime.strptime(''.join(created).strip(), "%Y-%m-%d %H:%M")
                item['type'] = 1
                item['pagerank'] = 1

                yield item

            else:
                pass
