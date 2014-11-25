#!/usr/bin/python

import redis

# r_server = redis.Redis("211.155.92.154")
r_server = redis.Redis("121.40.202.173")

r_server.delete("cnblog:static")
with open("init-redis/data/cnblog.txt") as sites:
    urls = sites.read().splitlines()
    for url in urls:
        r_server.sadd("cnblog:static", url)

r_server.delete("cnblog:start_urls")
urls = r_server.smembers("cnblog:static")
for url in urls:
    r_server.lpush("cnblog:start_urls", url)
