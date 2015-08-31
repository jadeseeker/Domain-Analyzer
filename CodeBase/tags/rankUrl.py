

import sqlite3
import re


class Rank():

    db_name = ""
    category = ""
    upper_threshold = 400000000
    lower_threshold = 1000
    conn = ""
    cur = ""
    out = ""

    def __init__(self, db_name="", category=""):
        self.db_name = db_name
        self.category = category
        self.out = self.category+"_keywords.txt"

    def get_rank(self):
        self.conn = sqlite3.connect(self.db_name)
        self.cur = self.conn.cursor()
        cursor = self.select_content('Content')

        keywords = {}
        with open(self.out, 'r') as file_name:
            for line in file_name:
                line = line.split("\t")
                keywords.update({line[0]: int(line[1])})

        rank = 0
        old_url = "temp"
        new_url = "temp"
        flag = 0
        for row in cursor:
            new_url = row[0]
            if (old_url != new_url) and (flag == 1):
                print "The rank of "+old_url+" in "+self.category+" is:"+str(rank)
                rank = 0
            flag = 1
            old_url = row[0]
            words = []
            words += re.compile('\w+').findall(row[1])

            for w in words:
                if w in keywords:
                    rank += keywords[w]
        print "The rank of "+old_url+" in "+self.category+" is: "+str(self.normalise_rank(rank))

    def normalise_rank(self, rank):
        if rank >= self.upper_threshold:
            return 100
        elif rank <= self.lower_threshold:
            return 0
        else:
            num = 100*(rank - self.lower_threshold)
            den = (self.upper_threshold - self.lower_threshold)
            return int(num/den)

    def select_content(self, table_name):

        # Returning the contents of the selected table in the database
        try:
            cursor = self.cur.execute('select * from ' + table_name)
            return cursor
        except sqlite3.Error as e:
            print "An error occurred: ", e.args[0]
