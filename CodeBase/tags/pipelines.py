# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from database import scrapyDatabase

class TagsPipeline(object):

    def open_spider(self, spider):
        if spider.name == "getTags":
            #Database object
            self.database = scrapyDatabase(spider.db_name)

            #Create Tag,Domain tables if they don't exist
            self.database.createTagTable('Tag')

            #Initialize counter
            self.count = 0

        if spider.name == "getFrames":
            #Database object
            self.database = scrapyDatabase(spider.db_name)

            #Create Tag,Domain tables if they don't exist
            self.database.createFrameTable('Frame')
        
        if spider.name == "getScript":
            #Database object
            self.database = scrapyDatabase(spider.db_name)

            #Create Tag,Domain tables if they don't exist
            self.database.createScriptTable('Scripts')

    def process_item(self, item, spider):
        
        if spider.name == "getTags":
            #Extract items
            tag = item['tag']
            position = item['position']
            url = item['url']

            #Insert the tag into the database
            self.database.insertTag('Tag', dict(tag=tag, position=position, url=url))

            #Increment count
            self.count += 1

            #If enough inserts have been called, commit (actually execute to database)
            if self.count%100 == 0:
                self.database.conn.commit()

            return item
            
        if spider.name == "getFrames":
            #Extract items
            url = str(item['url'])
            frameRatio = float(item['frameRatio'])
            frame = str(item['frame'])
            jsRatio = float(item['jsRatio'])
            linkRatio = float(item['linkRatio'])
            script  = str(item['script'])
            #Insert the tag into the database
            self.database.insertFrame('Frame', dict(url=url, frameRatio=frameRatio, frame=frame, jsRatio=jsRatio, linkRatio=linkRatio, script=script))

            #If enough inserts have been called, commit (actually execute to database)
            if self.count % 100 == 0:
                self.database.conn.commit()

        if spider.name == "getScript":
            #Extract items
            url = item['url']
            script = item['script']
            #Insert the tag into the database
            self.database.insertScript('Scripts', dict(url=url, script=script))

            #Increment count
            self.count += 1

            #If enough inserts have been called, commit (actually execute to database)
            if self.count%100 == 0:
                self.database.conn.commit()

    def close_spider(self, spider):
        if spider.name == "getTags" or spider.name == "getFrames" or spider.name == "getScript":
            #Commit queries to database
            self.database.conn.commit()

