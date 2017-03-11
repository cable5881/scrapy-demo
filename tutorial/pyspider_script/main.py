#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2017-03-07 19:05:22
# Project: meiju

from pyspider.libs.base_handler import *
from pymongo import MongoClient

import random

USER_AGENT_LIST = [
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
    "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5",
    "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SE 2.X MetaSr 1.0; SE 2.X MetaSr 1.0; .NET CLR 2.0.50727; SE 2.X MetaSr 1.0)",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; 360SE)",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24"
]

client = MongoClient("mongodb://112.74.44.140:27017")
db = client['drama']

class Handler(BaseHandler):
    crawl_config = {
    }

    # @every(minutes=24 * 60)
    def on_start(self):
        self.crawl('http://www.meijutt.com/file/list1.html', callback = self.index_page)

    # 10 days
    @config(age=10 * 24 * 60 * 60)
    def index_page(self, response):
        for each in response.doc('.cn_box2 .bor_img3_right a[href^="http"]').items():
            self.crawl(each.attr.href, callback = self.detail_page, fetch_type = 'js', headers = {"User-Agent" : random.choice(USER_AGENT_LIST)})
            
        self.crawl(response.doc('div.page a:nth-last-child(2)').attr.href, callback = self.index_page)
        
    @config(priority=2)
    def detail_page(self, response):
        profile = response.doc('div.o_r_contact ul')
        profile.remove('em')
        
        drama = {
            "img_src" : response.doc('div.o_big_img_bg_b img').attr.src,
            "title_en" : profile.find('li:nth-child(2)').text(),
            "title_cn" : profile.find('li:nth-child(3)').text(),
            "debut_date" : profile.find('li:nth-child(7)').text(),
            "plot" : profile.find('li:nth-child(9)').text(),
            "nation" : profile.find('li:nth-child(10) label:nth-child(1)').text(),
            "tv" : profile.find('li:nth-child(10) label:nth-child(2)').text(),
            "hot" : profile.find('li:nth-child(11) label:nth-child(1)').text(),
            "length" : profile.find('li:nth-child(11) label:nth-child(2)').text(),
            "category" : profile.find('li:nth-child(12) label:nth-child(2)').text(),

            "script_writers" : [x.text() for x in profile.find('li:nth-child(4) a').items()],
            "directors" : [x.text() for x in profile.find('li:nth-child(5) a').items()],
            "actors" : [x.text() for x in profile.find('li:nth-child(6) a').items()],

            "average_score" : response.doc('div#average-score').text(),
            "star5_num" : response.doc('span#small-total-star5').text(),
            "star4_num" : response.doc('span#small-total-star4').text(),
            "star3_num" : response.doc('span#small-total-star3').text(),
            "star2_num" : response.doc('span#small-total-star2').text(),
            "star1_num" : response.doc('span#small-total-star1').text()
           
        }
        
        self.store(drama)
        return drama
    
    def store(self, drama):
        db.dramas.insert_one(drama)
    
    
    
    
    
    
    
    
