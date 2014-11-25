#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json
import codecs

from scrapy.exceptions import DropItem

from pybloomfilter import BloomFilter

class DuplicatesPipeline(object):
    def __init__(self):
        self.bf = BloomFilter(10000000, 0.01, 'filter.bloom')
        self.f_write = open('visitedsites','w')
        # self.si = SearchIndex()
        # self.si.SearchInit()

    def process_item(self, item, spider):
        print '************%d pages visited!*****************' %len(self.bf)
        if self.bf.add(item['url']):#True if item in the BF
            raise DropItem("Duplicate item found: %s" % item)
        else:
            #print '%d pages visited!'% len(self.url_seen)
            self.save_to_file(item['url'], item['title'])
            # self.si.AddIndex(item)
            return item

    def save_to_file(self, url, title):
        self.f_write.write(url)
        self.f_write.write('\t')
        self.f_write.write(title.encode('utf-8'))
        self.f_write.write('\n')

    def __del__(self):
        """docstring for __del__"""
        self.f_write.close()
        # self.si.IndexDone()
