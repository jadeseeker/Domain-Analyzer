
import sqlite3
import re
from collections import Counter
import stop_words

class Keywords():

    def __init__(self,database,limit,category):
        self.conn = sqlite3.connect(database)
        self.cur = self.conn.cursor()

        self.limit = int(limit)
        self.out = category+"_keywords.txt"

    def select_content(self, table_name):

        # Returning the contents of the selected table in the database
        try:
            cursor = self.cur.execute('select * from ' + table_name)
            return cursor
        except sqlite3.Error as e:
            print "An error occurred: ", e.args[0]

    def get_frequency(self):

        # Selecting all the text in the database
        cursor = self.select_content('Content')

        # Initialising variables
        words = []
        count_handle = Counter()

        # Generating common word list to be removed from the keyword list to be generated
        sw = stop_words.get_stop_words("english")

        # Extracting all words from the given database
        for row in cursor:
            words += re.compile('\w+').findall(row[1])

        #Remove stop words from 'words' list
        words = [w.lower() for w in words if w.lower() not in sw]

        # Calculating the frequency of all words in the given database
        for w in words:
            count_handle[w] += 1

        # Writing the keywords returned into the file = category+ "_keyword.txt"
        with open(self.out, 'w') as file_name:
            for word in count_handle.most_common(self.limit):
                file_name.write(word[0]+"\t"+str(word[1])+"\n")


