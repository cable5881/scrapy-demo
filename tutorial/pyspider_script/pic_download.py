#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2017-03-07 19:05:22
# Project: pic_download

from pyspider.libs.base_handler import *
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

class Handler(BaseHandler):
    crawl_config = {
    }

    def __init__(self):
        self.base_url = 'http://www.meijutt.com/file/list1.html'
        self.io_util = IOUtil()
	
    # @every(minutes=24 * 60)
    def on_start(self):
        self.crawl(self.base_url, callback = self.index_page)

    # 10 days
    @config(age=10 * 24 * 60 * 60)
    def index_page(self, response):
        for each in response.doc('.cn_box2 .bor_img3_right a[href^="http"]').items():
            self.crawl(each.attr.href, callback = self.detail_page, fetch_type = 'js', headers = {
                "User-Agent" : random.choice(USER_AGENT_LIST),
                "Accept-Encoding":"gzip, deflate, sdch",
                "Accept-Language":"zh-CN,zh;q=0.8",
                "Cache-Control":"no-cache",
                "Host":"www.meijutt.com",
                "Pragma":"no-cache",
                "Referer":"http://www.meijutt.com",
                "Upgrade-Insecure-Requests":1
            })
            
        self.crawl(response.doc('div.page a:nth-last-child(2)').attr.href, callback = self.index_page)
        
    @config(priority=2)
    def detail_page(self, response):
        img_src = response.doc('div.o_big_img_bg_b img').attr.src
        file_src_parts = img_src.split('/')
        file_parent_root = file_src_parts[-2]
        file_name = file_src_parts[-1]
		
        self.crawl(img_src, callback = self.save_img, save={'file_parent_root': file_parent_root, 'file_name': file_name}, headers = {
            "User-Agent" : random.choice(USER_AGENT_LIST),
            "Accept":"image/webp,image/*,*/*;q=0.8",
            "Accept-Encoding":"gzip, deflate, sdch",
            "Cache-Control":"no-cache",
            "Host":"img.kukan5.com:808",
            "Pragma":"no-cache",
            "Proxy-Connection":"keep-alive",
            "Referer":response.url
        })
    
    # def store(self, drama):
    #    db.dramas.insert_one(drama)
    
    
    def save_img(self, response):
        file_parent_root = self.io_util.mkDir(response.save['file_parent_root'])
        file_path = file_parent_root + '/' + response.save['file_name']
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
            return dir_path
        else:
            return dir_path

    def save(self, content, path):
        f = open(path, 'wb')
        f.write(content)
        f.close()

	# 获得链接的后缀名，通过图片 URL 获得
    def getExtension(self, url):
        extension = url.split('.')[-1]
        return extension  
