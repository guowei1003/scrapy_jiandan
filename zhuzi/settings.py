# -*- coding: utf-8 -*-

# Scrapy settings for zhuzi project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'zhuzi'
DOWNLOAD_TIMEOUT = 1200
DOWNLOAD_DELAY = 3
SPIDER_MODULES = ['zhuzi.spiders']
NEWSPIDER_MODULE = 'zhuzi.spiders'
ITEM_PIPELINES = {
    'zhuzi.pipelines.ZhuziPipeline': 800,
}
# ITEM_PIPELINES = ['second.pipelines.MySQLStorePipeline']
# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'zhuzi (+http://www.yourdomain.com)'
