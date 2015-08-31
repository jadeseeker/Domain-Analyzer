

# -*- coding: utf-8 -*-

# Scrapy settings for tags project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'tags'

SPIDER_MODULES = ['tags.spiders']
NEWSPIDER_MODULE = 'tags.spiders'

# Log file
LOG_FILE = "log.txt"

# Add item pipeline
ITEM_PIPELINES = {
    'tags.pipelines.TagsPipeline': 1
}

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'tags (+http://www.yourdomain.com)'

# Rotate user agents
# NOTE: code grabbed from "http://tangww.com/2013/06/UsingRandomAgent/"
DOWNLOADER_MIDDLEWARES = {
    'scrapy.contrib.downloadermiddleware.useragent.UserAgentMiddleware' : None,
    'tags.comm.rotate_useragent.RotateUserAgentMiddleware' :400
}

# Delay downloads
DOWLOAD_DELAY = 2

# Disable cookies
COOKIES_ENABLED = False

# Disable retries (can slow down crawl)
RETRY_ENABLED = False
