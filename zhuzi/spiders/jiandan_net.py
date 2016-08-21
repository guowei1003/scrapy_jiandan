#!/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = '曹国伟'
#####################################
#煎蛋网是一个综合性网站，各种资源都存在，获取的比较麻烦，所以要定义一些规则才能更好的抓取。
#由于更新时间不同，每个栏目的抓取规则也不同。由于抓取是循环的，所以要定义下去重规则才行。我想应该根据时间来判断
#每个页面都只抓取第一页，其他的时间太久了，没有时效性
#抓取策略：
#   1、抓取煎蛋网站各个栏目中最新发布的信息（当日信息）
#   2、过期即失去时效性的页面要从数据库中剔除（一周前的信息），首先要保证数据库中存在100条数据
#   3、重首页获取每个小标题的页面（tag/XXX），跟进之后获取每个小标题下的具体信息页面，
#   4、每隔一小时抓取一遍
#####################################
import re,time,json,urllib

from scrapy.selector import Selector
try:
    from scrapy.spider import Spider
except:
    from scrapy.spider import BaseSpider as Spider


from scrapy.selector import Selector
from scrapy.contrib.spiders import CrawlSpider,Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor as sle
from scrapy.utils.response import get_base_url
from scrapy.utils.url import urljoin_rfc
from scrapy.http import Request

from ..items import Jiandan

# import uuid
#
# def getid():
#     return uuid.uuid1( ).hex
#定义去重函数######
# def norepeat_url(url):
#     """URL去重，定义一个文件在当前目录下，用来存放一爬取的URL,备用处理"""
#     if not url:
#         return 0
#     mark = 1
#     url = urllib.unquote(url)
#     file_d = open("./jiandan.txt",'a+')
#     # for line in file_d:
#     #     if line[:-1] == url:
#     #         mark = 0
#     #         break
#     # if mark == 0:
#     #     return 2
#     # else:
#     mark = len(file_d.readlines())+1
#     file_d.write(str(mark)+"    "+str(url)+"\n")
#     file_d.close()
#     return 1
# ##################
class Jiandan_net(CrawlSpider):
    """定义蜘蛛功能"""
    name = "jiandan"
    allowed_domains = ['jandan.net']
    start_urls = [#起始抓取URL
        "http://jandan.net/new"
    ]

    rules = (
        Rule(sle(allow=(r"/[\d]{4}/[\d]{2}/[\d]{2}/[\d\w-]{0,50}\.html$")),callback="prase_detail"),
        # Rule(sle(allow=(r"/page/[23]"))),
        Rule(sle(deny=(r"/tag/.*")),follow=False),
        # Rule(sle(deny=(r"/author/.*"))),
        Rule(sle(deny=(r"/page/.*")),follow=False),
        Rule(sle(deny=(r"(/v|/duan|/pic|/guanyu|/feed|/app|/|/author/.*)$")),follow=False),
    )


    def prase_detail(self,response):

        Items=[]
        resBody = Selector(text=response.body)
        base_url = get_base_url(response)#获取源网址成功
        print '***********************************',base_url
        title = resBody.xpath('//title/text()').extract()[0]#获取标题成功
        publishtime =resBody.xpath('//div[@class="time_s"]/text()').re("\s@\s(.*)\s,\s(.*)")#获取发布时间（需处理）
        author = resBody.xpath('//div[@class="time_s"]/a/text()').extract()[0]#获取作者成功
        content = resBody.xpath('//div[@class="post f"]//p').extract()#获取网页主内容成功

        item = Jiandan()
        item['title'] =title
        item['source_url'] =base_url
        item['publish_time'] =publishtime
        item['source_author'] =author
        item['content'] =content

        # file_d = open("./jiandan.txt",'a+')
        # mark = len(file_d.readlines())+1
        # file_d.write(str(mark)+"    "+str(get_base_url(response))+title.encode('utf-8')+str(content)+"\n")
        # file_d.close()
        return item
