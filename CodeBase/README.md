##Web & Search Engine Crawling for Data Discovery

**Description:** You need to implement an efficient web crawler that is able to collect various data points from the site that it's crawling. For example, it needs to be able to keep state on all html, redirections, PEs, images, screen-shots etc. that can be found on a given site on a given day. Then, as you reiterate on all these sites, you will have to be able to create a report on the network "agility" of the site. That is, what was change and why it changed. for example, was it due to advertisement, or the type of the site (i.e., news site). You will a also have to implement a search engine crawler. Using existing APIs, and without getting blacklisted, and the most important keywords from the sites you have already crawled per industry (i.e., energy or defense industry), you need to create an ranking system on the most typical sites that co exists in web search per industry but are not listed in Alexa Ranking System.

--Dr. Manos Antonakakis

##BlackThread
This is our solution to the project described above.

##HOWTO:
####Install:
* TERMINAL > python setup.py install

####Learn about the different functionalities:
* TERMINAL > blackthread --help

####Perform structural analysis on webpages:

1. Gather/Crawling structure data on URLs:
    * Create a file, e.g. "input.txt", containing the list of URL's you wish to crawl to analyze a website's **structure**, each URL being separated by a newline.

    * **NOTE**: This will add tags to a database named "tags.db".
    * TERMINAL > blackthread crawl --help
    * TERMINAL > blackthread crawl --input=input.txt --depth=2 --spider=getTags
    * TERMINAL > blackthread crawl --url=www.guimp.com

2: Classifying a URL for malicious and benign behavior:

	* blackthread classify —url=<give url here>

####Construct a ranking system for webpages:
1. Gather content data on URLs:
    * Create a file, e.g. "input.txt", containing the list of URL's you wish to crawl to analyze a website's **content** (e.g. You wish to create extract keywords from industry specific websites in order to create a ranking system of webpage's based on their content), each URL being separated by a newline.
    * **NOTE**: This will add tags to a database named "contents.db".
    * TERMINAL > blackthread crawl --help
    * TERMINAL > blackthread crawl --input=input.txt --spider=getContent

2. Gather keywords on URLs:
    * **NOTE**: This will create a new file named "\_keywords.txt" (unless provided a category in which case the file will be named "category\_keywords.txt") and will **replace** any file named as such.
    * TERMINAL > blackthread keywords --help
    * TERMINAL > blackthread keywords --database=defense\_contents.db --category=defense

3. Create ranking system for URLs based on keywords found in industry specific areas:
    * TERMINAL > blackthread rank --help
    * TERMINAL > blackthread rank --database=defense\_contents.db --category=defense

##Input files
* benign.txt
    * List of benign websites
    * Top 426 - 500 websites on Alexa
    * Crawled with max depth of 3
* malicious.txt
    * List of 100 malicious websites from http://www.malwaredomainlist.com/hostslist/hosts.txt
* business-energy.txt
    * Websites specific to energy businesses.
    * http://www.alexa.com/topsites/category/Top/Business/Energy

##Tag Database Organization
*   Database Name: "tags.db"

*   Design for each table:
    *   Tag (tag, position, url, date)
        * tag = the tag
        * position = what position the tag was found on the webpage
        * url = url of the webpage

##Content Database Organization
*   Database Name: "contents.db"

*   Design for each table:
    *   Content (start\_url, content)
        * start_url = base url that crawl was started on
        * content = words seen in website 

*   Primary key: (URL)

##Software Organization:
####./README.md:
* This file.

####./scrapy.cfg:
* Configuration for crawler.

####./setup.py:
* Script to install software.

####./Keywords/:
* Folder that holds our lists of keywords for industry specific websites.

####./Lists/:
* Folder that holds our lists of URLs we crawl.

####./tags/crawl.py:
* Contains main function of software.
* Performs command-line parsing and running the crawler.

####./tags/getKeywords.py:
* Script to find top keywords in content database.

####./tags/items.py:
* Items to be used by web crawler for storing data about websites.

####./tags/pipelines.py:
* Pipeline used by webcrawler for storing data to output file.

####./tags/settings.py:
* Settings for web crawler.

####./tags/comm/rotate\_useragent.py:
* Rotates user agents in order to evade websites blocking the crawler.

####./tags/spiders/tagSpider.py:
* Web crawler that scrapes webpage tags and contents.

####./tags/spiders/database.py:
* Database implementations to store data from crawls.

##Requirements:
####Python >= 2.7.3

####Scrapy >= 0.24.4

####Twisted >= 14.0.2

####pyasn1 >= 0.1.7

####Service-identity >= 14.0.0

####BeautifulSoup4 >= 4.3.2

####Stop-Words >= 2014.5.26

####tld >= 0.7.2

####apt-get install python-scipy

####apt-get install python-sklearn

####pip install scipy >= 0.10.1

####pip install scikit-learn >= 0.15.2

####pip install argparse >= 1.2.1

####pip install numpy >= 1.9.1

####pip install matplotlib >- 1.1.1rc2

