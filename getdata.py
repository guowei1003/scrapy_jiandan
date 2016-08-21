#-*- coding:utf-8 -*-
import os
import time

input = raw_input("按回车键开始")

a =1
if input == "":
    while 1:
        time.sleep(3600)#每小时获取一次
        print "正在进行第 "+str(a)+" 次获取..."
        os.system("scrapy crawl jiandan")
        print "已完成第 "+str(a)+" 次"
        a+=1