
# Steps to perform various functions in BlackThread

# Crawling:
# There are two spiders in BlackThread, one is called getTags spider and is used to extract all the tags on a given domain.
# The other is called getContent and is used to extract all the text on a given page. These spiders are defined in the
# tagSpider.py file under the spider's directory.
# To crawl using any of these two spiders use the command: BlackThread crawl <spider_name> arguments
# The arguments in BlackThread are passed as key-value pairs, except the help argument.
# The arguments given in BlackThread augment the utility of the functions and provide greater control to the user.
# While some arguments are optional, some are necessary to execute the function involved.
# The list of arguments for the crawl function are given below:

# --spider = <spider name> [Required]:    Give the name of spider to use for crawling, possible values= getTags or getContent
# --input=<filename>:                     To give batch URL's for crawling in a file, either this or the URL argument are required.
# -url=<URL>:                             To crawl a particular URL, either this or the input argument is required
# --depth=<Depth_Limit>:                  Set the depth level for crawling, no limit by default, optional argument
# --help:                                 To see the help for crawling


# Generating Keywords:
# The keywords utility is used to return a file containing high frequency words and their frequency on a given URL.

import getopt
import sys
import subprocess
from getKeywords import Keywords
from rankUrl import Rank
from tags.lexical import lexical_analysis
from tags.model_selection import model

def usage(base):
    # Basic help manual
    if base == "main":
        print "\nBlackThread is web agility analysis and ranking system that crawls various websites to determine " + \
              "malicious and benign behaviour and also rank and categorise websites into different industries" + \
              "based on keywords extracted." + \
              "Functions available in BlackThread environment are listed below, " + \
              "you can see the specification of each function by using --help after each function\n\n" + \
              "crawl\n" + "keywords\n" + "rank\n" + "classifier\n" + "classify\n"

    # Help Manual for using the crawling utility
    if base == "crawl":
        print "\nThe crawl utility is used to crawl and parse tags and content on web pages.\n" + \
              "The utility takes in key, value pairs as arguments. All the possible arguments" + \
              "for the crawl utility are described below\n\n"

        print "--spider=<spider name> [Required]:\t\tGive the name of spider to use for crawling" + \
              ", possible values= getTags or getContent\n"
        print "--input=<filename>:\t\tTo give batch URL's for crawling in a file\n"
        print "--url=<URL>:\t\t\tTo crawl a particular URL\n"
        print "--depth=<Depth_Limit>:\t\tSet the depth level for crawling, no limit by default\n"
        print "--database=<database name>:\t\t Name of the database where you want to store result"
        print "--help:\t\t\t\tTo see the help for crawling\n"

    # Help Manual for using the keywords utility
    if base == "keywords":
        print "\nThe keywords utility is used to extract all the keywords from a parsed HTML page" + \
              "based on a certain window defined by the user.\n" + \
              "If no window is given then all words that occur more than a default limit" + \
              "will be returned. The utility takes in key, value pairs as arguments. All the possible arguments" + \
              " for the keywords utility are described below\n\n"
        print "--database=<database name>:\t\tGive the address of the database containing results from crawled spider\n"
        print "--limit=<value>:\t\t\tDefines the number of top keywords to be returned\n"
        print "--category=<name>:\t\t\tGive the category of the keywords extracted, eg: Defense, Finance etc\n"
        print "--help:\t\t\t\t\tTo see the help for keywords utility\n"

    # Help Manual for using the rank utility
    if base == "rank":
        print "\nThe rank utility is used to rank domain based on the category given by the user." + \
              "Users can give batch domains in a file or give individual domain.\n" + \
              "The utility takes in key, value pairs as arguments. All the possible arguments" + \
              "for the keywords utility are described below\n\n"
        print "--database=<database name>:\t\t Name of the database containing crawled URL content"
        print "--category=<category name>:\t\tGive the category of the keywords extracted, eg: Defense, Finance etc\n"
        print "--help:\t\t\t\t\tTo see the help for rank utility\n"

    # Help Manual for using the classifier generation utility
    if base == "classifier":
        print "\nThe classifier utility is used to perform cross validation and generate evaluation statistics and plot the " \
              "ROC curve for different models. Users need to select between structural agility and lexical analysis in the category." + "\n\n"
        print "--category=<category name>:\t\t Name of the category"
        print "--list:\t\tList all the classifiers in the utility\n"
        print "--help:\t\t\t\t\tTo see the help for classifier utility\n"

     # Help Manual for using the lexical classification
    if base == "classify":
        print "\nThe classify utility takes in a url and does lexical analysis and returns ." + "\n\n"
        print "--url=<url>:\t\t URL to classify"
        print "--help:\t\t\t\t\tTo see the help for classify utility\n"


def crawl(opts):
    filename = ""
    url = ""
    depth = str(0)
    spider = "getTags"
    db_name=""
    for o, a in opts:
        if o in ("-h", "--help"):
            usage("crawl")
            sys.exit()
        elif o in "--input":
            filename = a
        elif o in "--url":
            url = a
        elif o in "--depth":
            depth = a
        elif o in "--spider":
            spider = a
        elif o in "--database":
            db_name = a

        else:
            usage("crawl")
            assert False, "unhandled option"

    if filename != "":
        with open(filename, 'r') as fr:
            count = 0
            for line in fr:
                line = line[:-1]
                param1 = "url=" + line
                depth_limit = "DEPTH_LIMIT=" + depth
                param2 = "db_name="+db_name+str(count)+".db"
                subprocess.call(["scrapy", "crawl", spider, "-s", depth_limit, "-a", param1, "-a", param2])
                count += 1

    elif url != "":
        param1 = "url=" + url
        depth_limit = "DEPTH_LIMIT=" + depth
        param2 = "db_name="+db_name
        subprocess.call(["scrapy", "crawl", spider, "-s", depth_limit, "-a", param1,"-a", param2])
    else:
        print "Please provide an input to read"
        sys.exit()


def keywords(opts):
    database = ""
    limit = 10
    category = ""
    for o, a in opts:
        if o in ("-h", "--help"):
            usage("keywords")
            sys.exit()
        elif o in "--database":
            database = a
        elif o in "--limit":
            limit = a
        elif o in ("--category"):
            category = a
        else:
            usage("keywords")
            assert False, "unhandled option"

    if database != "" and category != "":
        handle = Keywords(database, limit, category)
        handle.get_frequency()

    else:
        print "Please provide a database obtained from using getContent Spider and the category for the keywords"
        sys.exit()


def rank(opts):
    db_name = ""
    category = ""
    for o, a in opts:
        if o in ("-h", "--help"):
            usage("rank")
            sys.exit()
        elif o in "--database":
            db_name = a
        elif o in "--category":
            category = a
        else:
            usage("rank")
            assert False, "unhandled option"

    if db_name != "":
        handle = Rank(db_name, category)
        handle.get_rank()
        print "\nLegend:\n"
        print "If Rank =0:\t\t The URL is not associated with "+category+"\n"
        print "if Rank =100:\t\t The URL associates to "+category+" industry\n"
        print "If 0 < Rank <100:\t\t The URL is may or may not be associated with "+category + \
              " the degree of which depends on the rank"


def classifier(opts):
    category = ""
    for o, a in opts:
        if o in ("-h", "--help"):
            usage("classifier")
            sys.exit()
        elif o in "--category":
            category = a
        elif o in "--list":
            print "Models Present in the Utility"
            print "Support Vector Machine"
            print "Decision Tree"
            print "Gradient Descent"
            print "Random Forest"
            print "Gradient Boosting"
            print "Logistic Regression"
        else:
            usage("classifier")
            assert False, "unhandled option"

    #if category == "":
    subprocess.call(["python", "tags/model_selection.py"])


def classify(opts):
    url = ""
    for o, a in opts:
        if o in ("-h", "--help"):
            usage("classify")
            sys.exit()
        elif o in "--url":
            url = a
        else:
            usage("classify")
            assert False, "unhandled option"

    values  = lexical_analysis(url)
    model(values = values)




def main():
    try:
        opts, args = getopt.getopt(sys.argv[2:], "ho:v",
                                   ["help", "output=", "input=", "url=", "depth=", "spider=", "category=", "limit=",
                                    "database="])
    except getopt.GetoptError as err:
        # print help information and exit:
        print str(err)  # will print something like "option -a not recognized"
        usage("main")
        sys.exit(2)

    try:
        if sys.argv[1] == "crawl":
            crawl(opts)
        elif sys.argv[1] == "keywords":
            keywords(opts)
        elif sys.argv[1] == "rank":
            rank(opts)
        elif sys.argv[1] == "classifier":
            classifier(opts)
        elif sys.argv[1] == "classify":
            classify(opts)
        else:
            usage("main")
    except IndexError:
        usage("main")


if __name__ == "__main__":
    main()

