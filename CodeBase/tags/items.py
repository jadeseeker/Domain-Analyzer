# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class TagsItem(scrapy.Item):
    tag = scrapy.Field()
    position = scrapy.Field()
    url = scrapy.Field()

class FrameTags(scrapy.Item):
    url  = scrapy.Field()
    frameRatio = scrapy.Field()
    frame = scrapy.Field()
    jsRatio = scrapy.Field()
    linkRatio = scrapy.Field()
    script = scrapy.Field()


class ScriptTags(scrapy.Item):
    url = scrapy.Field()
    script = scrapy.Field()    
