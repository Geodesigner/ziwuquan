#!/usr/bin/python

import redis

# r_server = redis.Redis("211.155.92.154")
r_server = redis.Redis("121.40.202.173")

r_server.delete("csdn:static")
with open("init-redis/data/csdn.txt") as sites:
    urls = sites.read().splitlines()
    for url in urls:
        r_server.sadd("csdn:static", url)

r_server.delete("csdn:start_urls")
urls = r_server.smembers("csdn:static")
for url in urls:
    r_server.lpush("csdn:start_urls", url)
