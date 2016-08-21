# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy import log
import scrapy
from twisted.enterprise import adbapi
from scrapy.http import Request
from scrapy.exceptions import DropItem
from scrapy.contrib.pipeline.images import ImagesPipeline
import time
import MySQLdb
import MySQLdb.cursors as cursors
import sys,os,re
import errno
import uuid
import codecs
import json
import urllib2
from PIL import Image

class ZhuziPipeline(object):

    def __init__(self):
        # self.file = codecs.open('./tencent.txt', 'a',encoding="utf-8")
        self.dbpool = adbapi.ConnectionPool(
            'MySQLdb',
            db = "zhuzi",
            user = 'root',
            passwd = '111111',
            cursorclass = cursors.DictCursor,
            charset = 'utf8',
            use_unicode = True
        )
        self.path = "D:/Fastpan/workspace/Django/IceFire/static/media_pic/"
        # self.path = os.path.join(os.getcwd(),'../../../../../workspace/Django/IceFire/static/media_pic/')
        # self.uuid_sign = None
        # self.title =None
        # self.publish_time = None
        # self.create_time = None
        # self.source_author = None
        self.source_site = u"煎蛋网"
        # self.source_url = None
        self.cornterite =""
        self.data_class = "W"
        self.beyond_class = 'jiandan'
        # self.content = None
        self.support_count=0
        self.oppose_count = 0
        self.read_count =0
        self.comment_count =0
        self.tags = ''
        self.remarks = ''

    def process_item(self, item, spider):#处理必须调用函数，用于主控处理

        query = self.dbpool.runInteraction(self._conditional_insert, item)
        query.addErrback(self.handle_error)

        return item

    def _conditional_insert(self,tx,item):
        #逻辑实现
        #定性：最新的一个内容标记推荐，100篇内容中只有最新的为推荐内容

        title =item.get("title").encode("utf-8")

        #首先根据标题来判断数据库中是否重复
        allcount = tx.execute('select title from icecream_data')

        # if allcount:
        art_list = [x["title"] for x in tx.fetchall()]
        if title.decode('utf-8') not in art_list:
            # self.file.write(json.dumps(dict({'title':title.decode('utf-8'),'list':art_list}),ensure_ascii=False)+'\n')
            if allcount >= 1000:
                tx.execute('select id from icecream_data order by publish_time limit 1')
                del_id = tx.fetchone()
                tx.execute('select uuid_sign from icecream_data where id like "%s"' %del_id['id'])
                del_uuid = tx.fetchone()[0]
                tx.execute('delete from icecream_data where id like "%s"' %del_id['id'])
                for i in os.listdir(self.path):
                    if i.split('_')[0] == del_uuid:
                        try:
                            os.remove(self.path+i)
                        except  WindowsError:
                            pass

            uuid_sign = self.process_getuuid()

            publish_time = self.process_time(item.get("publish_time"))
            create_time = time.time()
            source_author = item.get("source_author").encode("utf-8")
            source_url = item.get("source_url")
            content = self.process_content(item.get("content"),uuid_sign)
            insert_sql = 'insert into icecream_data (uuid_sign,title,data_class,beyond_class,cornerite,source_site,source_url,source_author,content,create_time,publish_time,support_count,oppose_count,read_count,comment_count,tags,remarks) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
            tx.execute(insert_sql, (uuid_sign,title,self.data_class,self.beyond_class,self.cornterite,self.source_site,source_url,source_author,content,create_time,publish_time,self.support_count,self.oppose_count,self.read_count,self.comment_count,self.tags,self.remarks))

            # (self.uuid_sign,self.title,self.data_class,self.beyond_class,self.cornterite,self.source_site,self.source_url,self.source_author,self.content,self.create_time,self.publish_time,self.support_count,self.oppose_count,self.read_count,self.remarks)
            # x=tx.execute('select * from icecream_data')
            # res = tx.fetchmany(100)
            # for i in res:
            #     self.file.write(json.dumps(i,ensure_ascii=False)+'\n')
            # self.file.write(str(type(self.publish_time))+'\n')

    def handle_error(self, e):
        log.err(e)

    def process_time(self,ptime):
        #将创建时间处理成标准时间戳
        if not ptime:
            return u'时间未知'
        year,month,day,hour,minute,second,ap = ptime[0][0:4],ptime[0][5:7],ptime[0][8:10],ptime[1][0:2],ptime[1][3:5],'00',ptime[1][-2:]
        if ap == "am" and hour == '12':
            hour ='00'
        elif ap == "am" and hour != "12":
            hour = hour
        elif ap == "pm" and hour == '12':
            hour = hour
        elif ap == 'pm' and hour != "12":
            hour = str(int(hour)+12)
        putime = time.mktime(time.strptime('%s-%s-%s %s:%s:%s' %(year,month,day,hour,minute,second),'%Y-%m-%d %H:%M:%S') )
        return putime
    def process_content(self,content,uuid):

        #数据处理网页详细内容
        #处理成标准格式
        # {"Data_image":[],"Data_alt":[],"Data_art":""}
        #
        if not content:
            return u'数据错误'
        newcontent={"Data_image":[],"Data_alt":[],"Data_art":""}
        # image_sign = re.compile(r"img")
        for i in content:
            img = re.findall(r'<img src="(.*)" alt="(.*)">',i)
            newi = "_p_start_"+i[3:-4]+"_p_end_"
            if img:
                for j in img:

                    newcontent["Data_alt"].append(j[1])
                    picname = uuid+"_"+j[0].split('/').pop()

                    try:
                        pic = urllib2.urlopen(j[0], timeout=30).read()
                        f = open(self.path+picname,'wb')
                        f.write(pic)
                        f.close()
                        newcontent["Data_image"].append('/static/media_pic/'+picname)
                    except:
                        newcontent["Data_image"].append('/static/media_pic/error.jpg')

                newi = re.sub(r'<img .*>','_here_image_',newi)
            newcontent["Data_art"] +=newi

        if newcontent["Data_image"] and newcontent["Data_image"][0][-3:] == 'jpg' :
            newimgname = newcontent["Data_image"][0].split('/').pop()
            try:
                im = Image.open(self.path+newimgname)
                im = im.resize((230, 150))
                im.save(self.path+newimgname.split('_')[0]+'_thumbnails_'+newimgname.split('_')[-1])
            except:
                pass
        return json.dumps(newcontent,ensure_ascii=False)


    def process_getuuid(self):
        return str(uuid.uuid1().hex)

    # def spider_closed(self, spider):
    #     self.file.close()
