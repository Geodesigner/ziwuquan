#!/usr/bin/python

import redis

# r_server = redis.Redis("211.155.92.154")
r_server = redis.Redis("121.40.202.173")

r_server.delete("esribbs:static")
with open("init-redis/data/esribbs.txt") as sites:
    urls = sites.read().splitlines()
    for url in urls:
        r_server.sadd("esribbs:static", url)

r_server.delete("esribbs:start_urls")
urls = r_server.smembers("esribbs:static")
for url in urls:
    r_server.lpush("esribbs:start_urls", url)
