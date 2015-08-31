


import difflib
import getopt
import sqlite3
import sys
import hashlib
from bs4 import BeautifulSoup


def usage():
    print "--database1=<databasename>: Give the database file"
    print "--database2=<databasename>:  Give the database file"
    print "--help:  To see the help"


# Calculates differences in databases using html output
def change(html):

    added = "diff_add"
    changed = "diff_chg"
    deleted = "diff_sub"

    count = 0

    #Feed html into beautifulsoup for parsing
    soup = BeautifulSoup(html)

    #Count the number of "difference" tags seen in html file
    count += len(soup.find_all("span", "diff_add"))
    count += len(soup.find_all("span", "diff_chg"))
    count += len(soup.find_all("span", "diff_sub"))

    #Normalize count by length of HTML file
    #length = len(soup.get_text())

    #print count
    #print length

    return count

def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "ho:v", ["help", "database1=", "database2="])
    except getopt.GetoptError as err:
        # print help information and exit:
        print str(err) # will print something like "option -a not recognized"
        usage()
        sys.exit(2)
    database1 = ""
    database2 = ""
    for o, a in opts:
        if o in ("-h", "--help"):
            usage()
            sys.exit()
        elif o in "--database1":
            database1 = a
        elif o in "--database2":
            database2 = a
        else:
            assert False, "unhandled option"
            sys.exit()

    #If no arguments given
    if (not database1) or (not database2):
        usage()
        sys.exit(2)

    #Collect content from databases
    htmlDiff = difflib.HtmlDiff()

    # Generating the database handler
    cur1 = load_database(database1)
    cur2 = load_database(database2)

    # Generating unique urls in the database
    url1 = get_urls(cur1)
    url2 = get_urls(cur2)

    # Getting the common urls and unique urls

    common_urls = set(url1).intersection(set(url2))
    unique1 = set(url1).difference(common_urls)
    unique2 = set(url2).difference(common_urls)

    distance = 0

    # Calculating distance in the common urls
    for url in common_urls:
        url = "\""+ str(url[0]) + "\""
        string1 = ""
        string2 = ""

        # Selecting the tags of the given url
        page_cur1 = select_page(cur1, url)
        page_cur2 = select_page(cur2, url)

        for w in page_cur1:
            string1 += str(w)+"\n"

        for w in page_cur2:
            string2 += str(w)+"\n"

        # Checking hash of the two web pages
        if hashlib.sha256(string1).hexdigest() != hashlib.sha256(string2).hexdigest():
            # If hash unequal then calculating the edit distance
            htmlOut = htmlDiff.make_file(string1, string2)
            distance += change(htmlOut)

    # Calculating distance in the unique urls
    if unique1 is not None:
        string = ""
        for url in unique1:
            string = ""
            cursor = select_page(cur1, url)
            for tag in cursor:
                string += str(tag)
        distance += len(string)

    if unique2 is not None:
        string = ""
        for url in unique2:
            string = ""
            cursor = select_page(cur2, url)
            for tag in cursor:
                string += str(tag)
        distance += len(string)

    print distance


def load_database(database_name):
    conn = sqlite3.connect(database_name)
    cur = conn.cursor()
    return cur


def get_urls(cur):
    try:
        cursor = cur.execute('select DISTINCT url from Tag')
        return cursor
    except sqlite3.Error as e:
        print "An error occurred: ", e.args[0]


def select_page(cur, page):
    try:
        cursor = cur.execute('select tag from Tag where url=%s order by position ASC ' % page)
        return cursor
    except sqlite3.Error as e:
        print "An error occurred: ", e.args[0]


if __name__ == "__main__": main()
