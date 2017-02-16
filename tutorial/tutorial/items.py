# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class TutorialItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    author = scrapy.Field()
    text = scrapy.Field()
    tags = scrapy.Field()

class DramaItem(scrapy.Item):
	href = scrapy.Field()
	img_src = scrapy.Field()
	title_cn = scrapy.Field()
	title_en = scrapy.Field()
	tv = scrapy.Field()
	year = scrapy.Field()
	plot = scrapy.Field()
