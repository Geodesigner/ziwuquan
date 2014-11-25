#!/usr/bin/env python
# -*- coding: utf-8 -*-

BOT_NAME = 'ziwu'

SPIDER_MODULES = ['ziwu.spiders']
NEWSPIDER_MODULE = 'ziwu.spiders'

COOKIES_ENABLED = False
DOWNLOAD_DELAY = 6

# redis
SCHEDULER = "ziwu.components.redis.scheduler.Scheduler"
SCHEDULER_PERSIST = True
# SCHEDULER_QUEUE_CLASS = 'ziwu.components.redis.queue.SpiderPriorityQueue'
# SCHEDULER_QUEUE_CLASS = 'ziwu.components.redis.queue.SpiderQueue'
# SCHEDULER_QUEUE_CLASS = 'ziwu.components.redis.queue.SpiderStack'

SCHEDULER_IDLE_BEFORE_CLOSE = 10

# Specify the host and port to use when connecting to Redis (optional).
REDIS_HOST = '121.40.202.173' #aliyun
REDIS_PORT = 6379

# MONGODB_URI = 'mongodb://localhost:27017'
# MONGODB_DATABASE = 'ziwu'
# MONGODB_COLLECTION = 'article'
# MONGODB_UNIQUE_KEY = 'url'
# MONGODB_ADD_TIMESTAMP = True

POSTGRESQL_HOST = '211.155.92.154' #Mos
POSTGRESQL_PORT = '5432'
POSTGRESQL_DATABASE = 'ziwu'
POSTGRESQL_USER = 'ziwu'
POSTGRESQL_PASSWORD = 'mosZiwuPasswd'

ITEM_PIPELINES = {
    'ziwu.pipelines.DuplicatesPipeline': 200,
    # 'ziwu.components.redis.pipelines.RedisPipeline': 300,
    # 'ziwu.components.mongodb.pipelines.MongoDBPipeline': 301,
    'ziwu.components.postgresql.pipelines.PostgreSQLPipeline': 302,
}

# DOWNLOAD_HANDLERS = {
#     'http': 'ziwu.components.scrapyjs.dhandler.WebkitDownloadHandler',
#     'https': 'ziwu.components.scrapyjs.dhandler.WebkitDownloadHandler',
# }

DOWNLOADER_MIDDLEWARES = {
    # 'ziwu.components.scrapyjs.middleware.WebkitDownloader': 100,
    'ziwu.misc.middleware.CustomUserAgentMiddleware': 400,
    # 'ziwu.misc.middleware.CustomHttpProxyMiddleware': 410,
    'scrapy.contrib.downloadermiddleware.useragent.UserAgentMiddleware': None,
}
