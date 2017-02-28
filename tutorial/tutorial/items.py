# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class DramaItem(scrapy.Item):
    img_src = scrapy.Field()
    title_cn = scrapy.Field()
    title_en = scrapy.Field()
    tv = scrapy.Field()
    year = scrapy.Field()
    plot = scrapy.Field()
    debut_date = scrapy.Field()
    nation = scrapy.Field()
    hot = scrapy.Field()
    length = scrapy.Field()
    category = scrapy.Field()
    script_writers = scrapy.Field()
    directors = scrapy.Field()
    actors = scrapy.Field()
    average_score = scrapy.Field()
    star5_num = scrapy.Field()
    star4_num = scrapy.Field()
    star3_num = scrapy.Field()
    star2_num = scrapy.Field()
    star1_num = scrapy.Field()


