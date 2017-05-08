#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2017-04-04 21:27:48
# Project: douban_api

from pyspider.libs.base_handler import *
from myProxy import *
from db import mongoDb
import random
import spider_config

class Handler(BaseHandler):
    crawl_config = {
    }

    headers = spider_config.default_headers

    def __init__(self):
        self.base_url = 'https://movie.douban.com/j/search_subjects?type=tv&tag=%E7%BE%8E%E5%89%A7&sort=recommend&page_limit=20&page_start='
        self.proxyPool = proxypool(100)
        self.db = mongoDb()

    @every(minutes=24 * 60)
    def on_start(self):
        for p in range(0, 20):
            self.headers['User-Agent'] = random.choice(spider_config.USER_AGENT_LIST)
            self.crawl(self.base_url + str((p * 20)), callback=self.index_page, headers=self.headers, validate_cert=False, proxy=random.choice(self.proxyPool))

    @config(age=10 * 24 * 60 * 60)
    def index_page(self, response):
        for d in response.json['subjects']:
            url = 'https://api.douban.com/v2/movie/' + d['id']
            self.crawl(url, callback=self.detail_page, validate_cert=False, save={'id': d['id'],'image': d['cover']})

    @config(priority=2)
    def detail_page(self, response):
        drama = response.json
        drama['_id'] = response.save['id']
        drama['image'] = response.save['image']
        drama.pop('mobile_link')
        drama.pop('id')
        drama.pop('alt')
        drama.pop('title')
        self.db.insert_one(response.json)
