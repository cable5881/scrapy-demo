#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2017-05-09 21:27:48
# Project: douban_api

from pyspider.libs.base_handler import *
from myProxy import *
import random
import spider_config

from models import Drama
from mysql_db import MysqlDb


class Handler(BaseHandler):
    crawl_config = {
    }

    headers = spider_config.default_headers

    def __init__(self):
        self.base_url = 'https://movie.douban.com/j/search_subjects?type=tv&tag=%E7%BE%8E%E5%89%A7&sort=recommend&page_limit=20&page_start='
        self.proxyPool = proxypool(100)
        self.db = MysqlDb()

    @every(minutes=24 * 60)
    def on_start(self):
        for p in range(0, 20):
            self.headers['User-Agent'] = random.choice(spider_config.USER_AGENT_LIST)
            self.crawl(self.base_url + str((p * 20)), callback=self.index_page, headers=self.headers,
                       validate_cert=False, proxy=random.choice(self.proxyPool))

    @config(age=10 * 24 * 60 * 60)
    def index_page(self, response):
        for d in response.json['subjects']:
            url = 'https://api.douban.com/v2/movie/subject/' + d['id']
            self.crawl(url, callback=self.detail_page, validate_cert=False)

    # self, _id, image, title_en, duration, year, episodes,
    # avg_rating, seasons_count, current_season, title_cn = None,
    # website = None， summary = None, douban_url = None, aka = None):
    @config(priority=2)
    def detail_page(self, response):
        drama = self.handle_drama(response)
        director_list = self.handle_director(response)
        cast_list = self.handle_cast(response)
        drama_type_list = self.handle_drama_type(response)
        self.db.insert_drama_all(drama, director_list, cast_list, drama_type_list)

    def handle_director(self, response):
        drama_json = response.json
        return drama_json['directors']

    def handle_cast(self, response):
        drama_json = response.json
        return drama_json['casts']

    def handle_drama_type(self, response):
        drama_json = response.json
        return drama_json['genres']

    def handle_drama(self, response):
        drama_json = response.json
        _id = drama_json['id']
        image = drama_json['images']['large']
        title_en = drama_json['original_title']
        title_cn = drama_json['title']
        # duration = drama_json['duration']
        year = drama_json['year']
        episodes = drama_json['episodes_count']
        current_season = drama_json['current_season']
        seasons_count = drama_json['seasons_count']
        avg_rating = drama_json['rating']['average']
        summary = drama_json['summary']
        douban_url = drama_json['alt']
        aka = None
        if len(drama_json['aka']) > 0:
            aka = drama_json['aka'][0]

        return Drama(_id=_id, image=image, title_cn=title_cn, title_en=title_en,
                     year=year, episodes=episodes, current_season=current_season,
                     seasons_count=seasons_count, douban_url=douban_url, avg_rating=avg_rating,
                     summary=summary, aka=aka)
