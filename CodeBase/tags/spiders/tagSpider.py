from tags.items import TagsItem
from tags.items import FrameTags
from tags.items import ScriptTags
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.lxmlhtml import LxmlLinkExtractor
from tags.database import scrapyDatabase
import time
from bs4 import BeautifulSoup
import scrapy
from tld import get_tld


# Tag spider to parse the tags for a given url, database = tags.db
class TagSpider(CrawlSpider):
    name = 'getTags'
    allowed_domains = []
    start_urls = []
    database = ""
    rules = (
        Rule(LxmlLinkExtractor(), callback='parse_tags'),
    )

    def __init__(self, url=None, db_name='tags.db', *args, **kwargs):
        CrawlSpider.__init__(self)

        #If name was not provided, default to a name
        self.db_name = db_name

        #Define space in which spider can crawl
        #Also define space in which spider begins to crawl
        self.add_url(url)
 
   # Sanitising the url and adding to the list
    def add_url(self, url):
        url = url.rstrip("\n")
        if "http" not in url:
            url = "http://" + url
        try:        
            domain = get_tld(url)
            self.allowed_domains.append(domain)
            self.start_urls.append(url)
        except:
            print  "Url cannot be parsed: "+url


    def parse_tags(self, response):
        #Get URL of web page
        url = response.url
    
        #Print helpful output
        print "Crawling: ", url

        #Give text of webpage to beautifulsoup to be parsed
        bs = BeautifulSoup(response.body)

        #Parse the tags of the web page
        for info in enumerate(bs.findAll()):

            pos, t = info
            final = ""
            tag_attrs = list()
            
            #Gather attributes of tag (if there are any)
            for attr, val in t.attrs.iteritems():
                tag_attrs.append("{0}=\"{1}\"".format(attr, val))

            #Insert tag name into final string
            final += "<{0}".format(t.name)

            #Insert attributes and values into final string
            for attr in tag_attrs:
                final += " {0}".format(attr)
            final += ">"

            #Define item
            item = TagsItem()

            #Insert data into item
            item['tag'] = final
            item['position'] = pos
            item['url'] = url

            yield item


# Content spider to parse the contents for a given url, database = contents.db
class ContentSpider(CrawlSpider):
    name = "getContent"
    allowed_domains = []
    start_urls = []
    database = ""
    rules = (
        Rule(LxmlLinkExtractor(), callback='parse_contents'),
    )


    def __init__(self, url=None, db_name=None, *args, **kwargs):
        CrawlSpider.__init__(self)

        #If name was not provided, default to a name
        if db_name is None:
            db_name = "contents.db"

        #Database object
        self.database = scrapyDatabase(db_name)

        #Create Content table if it doesn't exist
        self.database.createContentTable('Content')

        #Define space in which spider can crawl
        #Also define space in which spider begins to crawl
        self.add_url(url)


    # Sanitising the url and adding to the list
    def add_url(self, url):
        url = url.rstrip("\n")

        if "https" in url:
            temp = url.strip("https://")
            self.allowed_domains.append(temp)
            self.start_urls.append(url)
        
        elif "http" in url and "https" not in url:
            temp = url.rstrip("http://")
            self.allowed_domains.append(temp)
            self.start_urls.append(url)
        
        else:
            self.allowed_domains.append(url)
            self.start_urls.append("http://%s" % url)

    def parse_contents(self, response):

        #Get URL of web page
        url = response.url

        #Print helpful output
        print "Crawling: ", url

        #Parse the content of the web page
        for sel in response.xpath('//*').extract():
            # Beautiful Soup Method to get all the text on the crawled page
            soup = BeautifulSoup(sel)

            #Insert the content line into the database
            self.database.insertContent('Content', dict(start_url=self.start_urls[0], content=soup.get_text()))


class FrameSpider(CrawlSpider):
    name = 'getFrames'
    allowed_domains = []
    start_urls = []
    database = ""
    rules = (
        Rule(LxmlLinkExtractor(), callback='parse_frames'),
    )

    def __init__(self, url = None, db_name = None, filename= None):
        # Initialising the inherited crawler
        CrawlSpider.__init__(self)
        
        self.db_name = db_name
        # Initialising the variable

        if url is not None:
            self.add_url(url)

        # Reading input from a file
        if filename is not None:
            with open(filename) as f:
                lines = f.readlines()
                for line in lines:          
                    self.add_url(line)

    # Sanitising the url and adding to the list
    def add_url(self, url):
        url = url.rstrip("\n")
        if "http" not in url:
            url = "http://" + url
        try:
            domain = get_tld(url)
            self.allowed_domains.append(domain)
            self.start_urls.append(url)
        except:
            print "Url not parsaed: "+url

    def parse_frames(self, response):
        
        # Get URL of the web page
        url = response.url

        # Log Message for crawling a url 
        print "Crawling: ",url
        
        # Total number of tags
        totalFrames  = len(response.xpath("//iframe"))

        #Beautiful soup handler
        soup = BeautifulSoup(response.body)

        # Gives the total length of all tags
        len_num_tags = 0
        #Parse the tags of the web page
        for info in enumerate(soup.findAll()):
            
            pos, t = info
            final = ""
            tag_attrs = list()

            #Gather attributes of tag (if there are any)
            for attr, val in t.attrs.iteritems():
                tag_attrs.append("{0}=\"{1}\"".format(attr, val))

            #Insert tag name into final string
            final += "<{0}".format(t.name)

            #Insert attributes and values into final string
            for attr in tag_attrs:
                final += " {0}".format(attr)
            final += ">"
            len_num_tags += len(str(final))

        # Ratio of total length of all iframe to total length of all tags
        frameRatio = float(totalFrames)/float(len_num_tags)

        # Iterating over each frame
        for frame in response.xpath("//iframe").extract():
            # Beautiful Soup object to store a frame
            soup = BeautifulSoup(frame)
            no_frame = BeautifulSoup(frame) 
            
            # Removing html and body tags
            soup.html.unwrap()
            soup.body.unwrap()
            no_frame.html.unwrap()
            no_frame.body.unwrap()

            # Removing iframe from the string
            no_frame.iframe.unwrap()

            # Items to send to the database:
            # url, frameRatio, frame, jsRatio, linkRatio, script

            # Scrapy item to store crawled data
            item = FrameTags()
            item['url'] = url
            item['frameRatio'] = frameRatio
            item['frame'] = soup
           
            # Getting the length of the frame contents
            frameLen = len(str(no_frame))

            # Getting the total number of tags in iframe
            tagsFrame = len(soup.findAll())

            # Getting the JS Ratio of the iframe
            scriptLen = 0            
            for script in soup.findAll('script'):
                scriptLen += len(str(script))

            # Ratio of length of all javascript to length of iframe
            item['jsRatio'] = 0
            if frameLen is not 0:
                item['jsRatio'] = scriptLen/frameLen
            
            # Getting the link ratio
            linkLen = 0
            item['linkRatio'] = 0

            # Getting the total numeber of link tags
            for link in soup.findAll('a'):
                linkLen += 1

            if tagsFrame is not 0:
                item['linkRatio'] = linkLen/tagsFrame

            # Getting all the javascript in the frame
            if soup.findAll('script'):
                for script in soup.findAll('script'):
                    item['script'] = script
                    yield item
            else:
                item['script'] = "No Script"
                yield item


class urlSpider(scrapy.Spider):
    name = "urlSpider"
    allowed_domains = [] 
    start_urls = []


    def __init__(self, filename=None):
        scrapy.Spider.__init__(self)
        with open(filename) as f:
            lines = f.readlines()
            for line in lines:
                self.add_url(line)


    # Sanitising the url and adding to the list
    def add_url(self, url):
        url = url.rstrip("\n")

        if "https" in url:
            temp = url.strip("https://")
            self.allowed_domains.append(temp)
            self.start_urls.append(url)
        
        elif "http" in url and "https" not in url:
            temp = url.rstrip("http://")
            self.allowed_domains.append(temp)
            self.start_urls.append(url)
        
        else:
            self.allowed_domains.append(url)
            self.start_urls.append("http://%s" % url)


    def parse(self, response):
        for link in response.xpath("//a/@href").extract():
            print link


class ScriptSpider(CrawlSpider):
    name = 'getScript'
    allowed_domains = []
    start_urls = []
    database = ""
    rules = (
        Rule(LxmlLinkExtractor(), callback='parse_script'),
    )

    def __init__(self, url = None, db_name = None, filename= None):
        # Initialising the inherited crawler
        CrawlSpider.__init__(self)
        
        self.db_name = db_name
        # Initialising the variable

        if url is not None:
            self.add_url(url)

        # Reading input from a file
        if filename is not None:
            with open(filename) as f:
                lines = f.readlines()
                for line in lines:          
                    self.add_url(line)

    # Sanitising the url and adding to the list
    def add_url(self, url):
        url = url.rstrip("\n")
        if "http" not in url:
            url = "http://" + url
        try:
            domain = get_tld(url)
            self.allowed_domains.append(domain)
            self.start_urls.append(url)
        except:
            print "Url not parsaed: "+url

    def parse_script(self, response):
        url = response.url
        
        # Log Message for crawling a url 
        print "Crawling: ",url
        
        bs = BeautifulSoup(response.body)

        for tag in bs.findAll():
            if tag.name == 'script':
                item = ScriptTags()

                item['url'] = url
                item['script'] = str(tag)
                yield item
