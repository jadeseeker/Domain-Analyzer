import sqlite3
import dns.resolver
import time
import re
import codecs
import thread
import sys

#extract public dns nameservers' IP from public-dns.txt
#filepath: a file that contains public dns nameserver info to extract from
#return a dictionary where key is country-id and value is a list containing all the dns nameservers in this country
def extract_public_dns_info(filepath):
    '''extract dns infomation from the file inputed.
        return a dictionary where key is country-id and value is a list containing all the dns nameservers in this country'''
    fin = codecs.open(filepath, "r", "utf-8")
    text = fin.read()
    fin.close()

    pattern = re.compile(r"<country-id>(.*?)</country-id>.*?<ip>(.*?)</ip>", re.S)
    data = pattern.findall(text)

    dic = {}
    for entry in data:
        if entry[0] not in dic:
            dic[entry[0]] = []
        #delete nameserver using ipv6
        if re.match(r'\d+\.\d+\.\d+\.\d+$', entry[1]):
            dic[entry[0]].append(entry[1].encode('ascii'))
    return dic

#get dns resolution from dns server
#domain: domain name to be queried
#nameserver: domain sent to this DNS nameserver to be queried
#return dns :: resolver :: Answer :: Class Answer in dnspython lib
def dns_resolution(domain, nameserver):
    '''resolve the domain by a nameserver.
        return dns :: resolver :: Answer :: Class Answer in dnspython lib'''
    my_resolver = dns.resolver.Resolver(configure=False)
    #lifetime is 4s
    my_resolver.lifetime = 4
    a = []
    a.append(nameserver)
    my_resolver.nameservers = a
    answer = my_resolver.query(domain)
    return answer

#create tables
def create_tables():
    conn = sqlite3.connect('dns_resolution_info.db');
    print "Database connected successfully";

    conn.execute('''PRAGMA foreign_keys = ON;''')

#DNS_IP: Public DNS nameserver IP addr
#COUNTRY_ID: unique ID of the country where the associated Public DNS nameserver in
    conn.execute('''CREATE TABLE NAMESERVERS
           (DNS_IP      CHAR(50) PRIMARY KEY,
            COUNTRY_ID  CHAR(10) NOT NULL);''')
    print "Table:nameservers created successfully";

#DOMAIN: domain names to be queried
#ACTIVE: a flag set to 0 when not want to query it again
    conn.execute('''CREATE TABLE DOMAINS
           (DOMAIN CHAR(50) PRIMARY KEY,
            ACTIVE int NOT NULL);''')
    print "Table:domains created successfully";

#RESULTS_ID: a distinct ID for every DNS look up
#SEQ: the sequence of IPs returned by one DNS look up
#RESOLVED_IP: resolved IP for a certain domain
#TTL: time to live for a domain in a certain DNS server cache
    conn.execute('''CREATE TABLE RESULTS
           (RESULTS_ID INT,
            SEQ       INT,
            RESOLVED_IP CHAR(50) NOT NULL,
            TTL         INT NOT NULL,
            PRIMARY KEY(RESULTS_ID,SEQ));''')
    print "Table:results created successfully";

#QUERY_CNT: a counter for how many times a dommain has been queried
#TIMESTAMP: the current time when a domain is queried
    conn.execute('''CREATE TABLE QUERYS
           (DOMAIN CHAR(50),
            DNS_IP  CHAR(50),
            QUERY_CNT INT NOT NULL,
            TIMESTAMP CHAR(50),
            RESULTS_ID INT,
            FOREIGN KEY(RESULTS_ID) REFERENCES RESULTS(RESULTS_ID)
            PRIMARY KEY(DOMAIN,DNS_IP,QUERY_CNT));''')
    print "Table:querys created successfully";

    conn.close()

#import public dns nameservers and domains to be queried
#both public dns nameservers and domains are contained in the text files in the directory
#public dns nameservers info in public-dns.txt
#domains info in domains.txt
def import_init_data():
    dic = extract_public_dns_info('public-dns.txt')

    conn = sqlite3.connect('dns_resolution_info.db')

#add DNS nameserver and the corresponding country id to the table nameservers
    for countryid,ips in dic.items():
        cnt = 0
        for ip in ips:
            conn.execute("INSERT INTO NAMESERVERS (DNS_IP,COUNTRY_ID) \
                          VALUES ('%s','%s')"%(ip, countryid))
            cnt += 1
            if cnt == 2:
                break

#load text file containing the domains to a list 
    print 'input domains file path:'
    domains = []
    path = raw_input()
    filep = open(path)
    while 1:
        line = filep.readline()
        if not line:
            break
        line = line.strip('\n')
        line = line.strip('\r')
        domains.append(line)
    filep.close()

#add  domains and the corresponding ACTIVE flag to the table nameservers
#ACTIVE flag is all set to 1 when initialization
    for domain in domains:
        try:
            conn.execute("INSERT INTO DOMAINS (DOMAIN, ACTIVE) \
                          VALUES ('%s', 1)"%domain);
        except BaseException,para:
            pass
    conn.commit()
    print "Initial Records created successfully";
    conn.close()


################################multi thread######################################
import threading
import Queue

exit_flag = 0
database_lock = threading.Lock()
queue_lock = threading.Lock()

class Task:
    def __init__(self, domain, query_cnt, results_id, server, alternate_server = None):
        self.server = server
        self.domain = domain
        self.alternate_server = alternate_server
        self.results_id = results_id
        self.query_cnt = query_cnt
        
class QueryThread(threading.Thread):
    def __init__(self, q):
        threading.Thread.__init__(self)
        self.q = q
    def deal_failure(self, conn, domain, query_cnt, server, results_id):
        timestr = time.strftime('%Y%m%d %H%M%S',time.localtime(time.time()))
        database_lock.acquire()
        conn.execute("INSERT INTO RESULTS \
                     (RESULTS_ID,SEQ,RESOLVED_IP,TTL) \
                      VALUES (%d,%d,'%s',%d)"%
                     (results_id,1,"0.0.0.0",0));
        conn.execute("INSERT INTO QUERYS \
                     (DOMAIN,DNS_IP,QUERY_CNT,TIMESTAMP,RESULTS_ID) \
                      VALUES ('%s','%s',%d,'%s',%d)"%
                     (domain,server,query_cnt,timestr,results_id));
        conn.commit()
        database_lock.release()
    def save_result(self, conn, results, domain, query_cnt, server, results_id):
        timestr = time.strftime('%Y%m%d %H%M%S',time.localtime(time.time()))
        seq = 1
        database_lock.acquire()
        for result in results[:]:
            sys.stdout.write("domain:%s,nameserver:%s\nresolved ip %d is %s\n"%(domain, server, seq, result))
            result = re.sub(r'\d+$', '0', str(result))
            
            conn.execute("INSERT INTO RESULTS \
                         (RESULTS_ID,SEQ,RESOLVED_IP,TTL) \
                          VALUES (%d,%d,'%s',%d)"%
                         (results_id,seq,result,results.rrset.ttl));
            seq += 1
            
        conn.execute("INSERT INTO QUERYS \
                     (DOMAIN,DNS_IP,QUERY_CNT,TIMESTAMP,RESULTS_ID) \
                      VALUES ('%s','%s',%d,'%s',%d)"%
                     (domain,server,query_cnt,timestr,results_id));
        conn.commit()
        database_lock.release()
    def run(self):
        conn = sqlite3.connect('dns_resolution_info.db', check_same_thread=False)
        while not exit_flag:
            this_task = None
            queue_lock.acquire()
            if not self.q.empty():
                this_task = self.q.get()
            queue_lock.release()
            if not this_task:
                continue
            try:
                results = dns_resolution(this_task.domain,this_task.server)
            except:
                sys.stdout.write('''domain:%s,nameserver:%s\nresolution exception happend in first try\n'''%
                                 (this_task.domain, this_task.server))
                if this_task.alternate_server:
                    sys.stdout.write("domain:%s,alternate nameserver:%s\ntry again...\n"%
                                     (this_task.domain, this_task.alternate_server))
                    try:
                        results = dns_resolution(this_task.domain,this_task.alternate_server)
                    except:
                        sys.stdout.write("domain:%s,alternate nameserver:%s\nsecond try fail\n"%
                                         (this_task.domain, this_task.alternate_server))
                        self.deal_failure(conn, 
                                         this_task.domain,
                                         this_task.query_cnt,
                                         this_task.alternate_server,
                                         this_task.results_id)
                    else:
                        self.save_result(conn, results,
                                         this_task.domain,
                                         this_task.query_cnt,
                                         this_task.alternate_server,
                                         this_task.results_id)
            else:
                self.save_result(conn, results,
                                 this_task.domain,
                                 this_task.query_cnt,
                                 this_task.server,
                                 this_task.results_id)
        conn.close()

def query_multi_thread(n, domains = None):
    threads = []

    #infinite length queue
    queue = Queue.Queue(0)
    
    conn = sqlite3.connect('dns_resolution_info.db', check_same_thread=False)

    cursor = conn.execute("SELECT * from NAMESERVERS order by country_id")
    servers = cursor.fetchall()
    if not domains:
        cursor = conn.execute("SELECT * from DOMAINS")
        domains = cursor.fetchall()
        domains = [domain[0] for domain in domains if domain[1] == 1] 
    cursor = conn.execute("SELECT max(results_id) from QUERYS")
    id_cnt = cursor.fetchall()
    if id_cnt[0][0]:
        id_cnt = int(id_cnt[0][0]) + 1
        print id_cnt
    else:
        id_cnt = 1
    cursor = conn.execute("SELECT max(query_cnt) from QUERYS")
    query_cnt = cursor.fetchall()
    if query_cnt[0][0]:
        query_cnt = int(query_cnt[0][0]) + 1
    else:
        query_cnt = 1
    conn.close()

    global exit_flag
    exit_flag = 0
    for i in range(n):
        thrd = QueryThread(queue)
        threads.append(thrd)
        thrd.start()
    
    queue_lock.acquire()
    for domain in domains:
        i = 0
        while i < len(servers):
            if i + 1 < len(servers) and servers[i][1] == servers[i + 1][1]:
                queue.put(Task(domain,query_cnt,id_cnt,servers[i][0],servers[i + 1][0]))
                i = i + 2
            else:
                queue.put(Task(domain,query_cnt,id_cnt,servers[i][0]))
                i = i + 1
            id_cnt += 1
    queue_lock.release()

    while not queue.empty():
        pass

    exit_flag = 1
    for t in threads:
        t.join()
    print "Query results updated successfully"
################################multi thread###################################

#a function that can be used to send sql statement to query data in database
#sql: a sql statement to retrieve data needed from database
#return the result for the sql statement
def easy_sql(sql):
    conn = sqlite3.connect('dns_resolution_info.db')
    cursor = conn.execute(sql)
    for row in cursor.fetchall():
        print row
    print
    print "Operation done successfully";
    conn.close()

if __name__ == '__main__':
    while(True):
        print "1.create database tables"
        print "2.import initial data(DNS nameservers and domains)"
        print "3.DNS look up for all domains and store results"
        print "4.sql statement to retrieve data in database(type sql statement)"
        print "5.exit"
        print "input choice:"
        choice = raw_input()
        try:
            if '1' == choice:
                create_tables()
            elif '2' == choice:
                import_init_data()
            elif '3' == choice:
                query_multi_thread(75)
            elif '4' == choice:
                sql = raw_input()
                easy_sql(sql)
            else:
                break
        except BaseException, para:
            print para
        finally:
            print



