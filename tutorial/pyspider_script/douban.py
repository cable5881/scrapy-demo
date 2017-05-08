#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2017-03-19 17:39:43
# Project: douban

from pyspider.libs.base_handler import *
from myProxy import *
from IOUtil import IOUtil
from db import mongoDb
import random
import spider_config

class Handler(BaseHandler):
    crawl_config = {
    }
    
    headers = spider_config.default_headers
    
    def __init__(self):
        self.base_url = 'https://movie.douban.com/j/search_subjects?type=tv&tag=%E7%BE%8E%E5%89%A7&sort=recommend&page_limit=20&page_start='
        self.io_util = IOUtil()
        self.proxyPool = proxypool(100)
        self.db = mongoDb
    
    # @every(minutes=24 * 60)
    def on_start(self):
        for p in range(0,50):
            self.headers['User-Agent'] = random.choice(spider_config.USER_AGENT_LIST)
            self.crawl(self.base_url + str((p * 20)), callback = self.index_page, headers = self.headers, validate_cert=False, proxy = random.choice(self.proxyPool))
            
    # 10 days
    @config(age=10 * 24 * 60 * 60)
    def index_page(self, response):
        for d in response.json['subjects']:
            self.headers['User-Agent'] = random.choice(spider_config.USER_AGENT_LIST)
            self.crawl(d["url"], callback = self.detail_page, fetch_type = 'js', headers = self.headers, proxy = random.choice(self.proxyPool))
        
    @config(priority=2)
    def detail_page(self, response):
        cn = response.doc('#info > span:nth-child(18) > span.pl').text()

        # return self.property_dict[cn]
        # profile = response.doc('div.o_r_contact ul')
        # profile.remove('em')
        
        # img_src = response.doc('div.o_big_img_bg_b img').attr.src
        # file_src_parts = img_src.split('/')
        # file_parent_root = file_src_parts[-2]
        # file_name = file_src_parts[-1]
		
        # self.headers['User-Agent'] = random.choice(USER_AGENT_LIST)
        # self.crawl(img_src, callback = self.save_img, save={'file_parent_root': file_parent_root, 'file_name': file_name}, proxy = random.choice(self.proxyPool), headers = {
            # 'Accept':"image/webp,image/*,*/*;q=0.8",
            # "Accept-Encoding":"gzip, deflate, sdch",
            # "Cache-Control":"no-cache",
            # "Host":"img.kukan5.com:808",
            # "Pragma":"no-cache",
            # "Proxy-Connection":"keep-alive",
            # "Referer":response.url
        # })
        
        # drama = {
            # "img_src" : file_parent_root + '/' + file_name,
            # "title_en" : profile.find('li:nth-child(2)').text(),
            # "title_cn" : profile.find('li:nth-child(3)').text(),
            # "debut_date" : profile.find('li:nth-child(7)').text(),
            # "plot" : profile.find('li:nth-child(9)').text(),
            # "nation" : profile.find('li:nth-child(10) label:nth-child(1)').text(),
            # "tv" : profile.find('li:nth-child(10) label:nth-child(2)').text(),
            # "hot" : profile.find('li:nth-child(11) label:nth-child(1)').text(),
            # "length" : profile.find('li:nth-child(11) label:nth-child(2)').text(),
            # "category" : profile.find('li:nth-child(12) label:nth-child(2)').text(),

            # "script_writers" : [x.text() for x in profile.find('li:nth-child(4) a').items()],
            # "directors" : [x.text() for x in profile.find('li:nth-child(5) a').items()],
            # "actors" : [x.text() for x in profile.find('li:nth-child(6) a').items()],

            # "average_score" : response.doc('div#average-score').text(),
            # "star5_num" : response.doc('span#small-total-star5').text(),
            # "star4_num" : response.doc('span#small-total-star4').text(),
            # "star3_num" : response.doc('span#small-total-star3').text(),
            # "star2_num" : response.doc('span#small-total-star2').text(),
            # "star1_num" : response.doc('span#small-total-star1').text()
           
        # }
        
        # self.store(drama)

    
    def store(self, drama):
        self.db.insert_one(drama)
    
    def save_img(self, response):
        file_parent_root = response.save['file_parent_root']
        self.io_util.mkDir(file_parent_root)
        file_path = file_parent_root + '/' + response.save['file_name']
        # print(file_path)
        self.io_util.save(response.content, file_path)
		
    
    


