#!/usr/bin/env python
# -*- coding: utf-8 -*-

from twisted.internet import reactor
from twisted.enterprise import adbapi
import psycopg2

from hashlib import md5
from scrapy import log

import datetime

class PostgreSQLPipeline(object):
    """ PostgreSQL pipeline class """
    def __init__(self, dbpool):
        self.dbpool = dbpool

    @classmethod
    def from_settings(cls, settings):
        dbargs = dict(
            host=settings['POSTGRESQL_HOST'],
            port=settings['POSTGRESQL_PORT'],
            database=settings['POSTGRESQL_DATABASE'],
            user=settings['POSTGRESQL_USER'],
            password=settings['POSTGRESQL_PASSWORD'],
        )
        dbpool = adbapi.ConnectionPool('psycopg2', **dbargs)
        return cls(dbpool)

    def process_item(self, item, spider):
        self.dbpool.runInteraction(self._insert_item, item, spider)

        return item

    def _insert_item(self, txn, item, spider):
        """Perform an insert or update."""
        guid = self._get_guid(item)
        now = datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M')

        txn.execute("""SELECT EXISTS(
            SELECT 1 FROM article WHERE guid = %s
        )""", (guid, ))
        ret = txn.fetchone()[0]

        if ret:
            txn.execute("""
                UPDATE article
                SET url=%s, title=%s, description=%s, content=%s, created=%s, type=%s, pagerank=%s, updated=%s
                WHERE guid=%s
            """, (item['url'], item['title'], item['description'], item['content'], item['created'], item['type'], item['pagerank'], now, guid))
            spider.log("Item updated in db: %s %r" % (guid, item))
        else:
            txn.execute("""
                INSERT INTO article (guid, url, title, description, content, created, type, pagerank, updated)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (guid, item['url'], item['title'], item['description'], item['content'], item['created'], item['type'], item['pagerank'], now))
            spider.log("Item stored in db: %s %r" % (guid, item))

    def _handle_error(self, failure, item, spider):
        """Handle occurred on db interaction."""
        # do nothing, just log
        log.err(failure)

    def _get_guid(self, item):
        """Generates an unique identifier for a given item."""
        # hash based solely in the url field
        return md5(item['url']).hexdigest()
