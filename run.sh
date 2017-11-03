#!/bin/bash

rm -fr *.json
# rm -fr *.log
scrapy crawl zol -o zol_items.json #--logfile=zol.log
scrapy crawl jd -o jd_items.json #--logfile=jd.log
scrapy crawl jd_detail -o jd_detail_items.json

cp *.json ~/test/output/