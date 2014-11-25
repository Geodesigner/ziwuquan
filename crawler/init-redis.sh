#! /bin/bash
PATH=/bin:/sbin:/usr/bin:/usr/sbin:/usr/local/bin:/usr/local/sbin:~/bin
export PATH

echo "=========================="
echo "Ziwu Crawler"
echo "=========================="

cur_dir=$(pwd)

crawlname="esri"
echo "Please input the crawl name:"
read -p "(Default name: esri):" crawlname
if [ "$crawlname" = "" ]; then
		crawlname="esri"
fi
echo "==========================="
echo "crawlname=$crawlname"
echo "==========================="

python init-redis/$crawlname.py
