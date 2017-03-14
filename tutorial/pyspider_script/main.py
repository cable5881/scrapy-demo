#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2017-03-07 19:05:22
# Project: meiju

from pyspider.libs.base_handler import *
from pymongo import MongoClient
import random
import os

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

DIR_PATH = 'g:/img'

client = MongoClient("mongodb://112.74.44.140:27017")
db = client['drama']

class Handler(BaseHandler):
    crawl_config = {
    }
    
    headers = {
        "Accept-Encoding":"gzip, deflate, sdch",
        "Accept-Language":"zh-CN,zh;q=0.8",
        "Cache-Control":"no-cache",
        "Host":"www.meijutt.com",
        "Pragma":"no-cache",
        "Referer":"http://www.meijutt.com",
        "Upgrade-Insecure-Requests":1
    }

    def __init__(self):
        self.base_url = 'http://www.meijutt.com/file/list1.html'
        self.io_util = IOUtil()
    
    # @every(minutes=24 * 60)
    def on_start(self):
        self.crawl('http://www.meijutt.com/file/list1.html', callback = self.index_page, headers = self.headers)

    # 10 days
    @config(age=10 * 24 * 60 * 60)
    def index_page(self, response):
        for each in response.doc('.cn_box2 .bor_img3_right a[href^="http"]').items():
            self.headers['User-Agent'] = random.choice(USER_AGENT_LIST)
            self.crawl(each.attr.href, callback = self.detail_page, fetch_type = 'js', headers = self.headers)
            
        self.crawl(response.doc('div.page a:nth-last-child(2)').attr.href, callback = self.index_page, headers = self.headers)
        
    @config(priority=2)
    def detail_page(self, response):
        profile = response.doc('div.o_r_contact ul')
        profile.remove('em')
        
        img_src = response.doc('div.o_big_img_bg_b img').attr.src
        file_src_parts = img_src.split('/')
        file_parent_root = file_src_parts[-2]
        file_name = file_src_parts[-1]
		
        self.headers['User-Agent'] = random.choice(USER_AGENT_LIST)
        self.crawl(img_src, callback = self.save_img, save={'file_parent_root': file_parent_root, 'file_name': file_name}, headers = {
            'Accept':"image/webp,image/*,*/*;q=0.8",
            "Accept-Encoding":"gzip, deflate, sdch",
            "Cache-Control":"no-cache",
            "Host":"img.kukan5.com:808",
            "Pragma":"no-cache",
            "Proxy-Connection":"keep-alive",
            "Referer":response.url
        })
        
        drama = {
            "img_src" : file_parent_root + '/' + file_name,
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
    
    def save_img(self, response):
        file_parent_root = response.save['file_parent_root']
        self.io_util.mkDir(file_parent_root)
        file_path = file_parent_root + '/' + response.save['file_name']
        # print(file_path)
        self.io_util.save(response.content, file_path)
		
    
    
class IOUtil(object):
    def __init__(self):
        self.path = DIR_PATH
        if not self.path.endswith('/'):
            self.path = self.path + '/'
        if not os.path.exists(self.path):
            os.makedirs(self.path)

    def mkDir(self, path):
        path = path.strip()
        dir_path = self.path + path

        if not os.path.exists(dir_path):
            os.makedirs(dir_path)

    def save(self, content, path):
        absolute_path = self.path + path
        f = open(absolute_path, 'wb')
        f.write(content)
        f.close()

	# 获得链接的后缀名，通过图片 URL 获得
    def getExtension(self, url):
        extension = url.split('.')[-1]
        return extension  
