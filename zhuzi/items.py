# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy.item as scrapy


class ZhuziItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class Jiandan(scrapy.Item):
    uuid_sign = scrapy.Field()          #UUID生成唯一标识(分析获取)
    title = scrapy.Field()              #title是网页标题（即时获取）
    data_class = scrapy.Field()         #数据分类(分析获取)
    source_site = scrapy.Field()        #源网站(分析获取)
    source_url = scrapy.Field()         #源网址（即时获取）
    source_author = scrapy.Field()      #作者（即时获取）
    cornterite = scrapy.Field()         #角标（后来获取）
    content = scrapy.Field()            #内容（即时获取）
    beyond_class = scrapy.Field()       #归类(分析获取)（煎蛋）
    create_time = scrapy.Field()        #获取网页的时间（分析获取）
    publish_time = scrapy.Field()       #数据发布时间（即时获取）
    tags = scrapy.Field()               #标签，关键字(分析获取)
    remarks = scrapy.Field()            #备注信息（后来获取）