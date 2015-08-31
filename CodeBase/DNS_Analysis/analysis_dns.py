import sqlite3
import dns.resolver
import time
import re
import codecs
import sys

def create_tables():
    conn = sqlite3.connect('dns_resolution_info.db')
    print "Database connected successfully"      
    conn.execute("""CREATE TABLE D_ANALYSIS (
			DOMAIN CHAR(50) NOT NULL,
			IP CHAR(50) NOT NULL , 
			TTL INT NOT NULL,
			CRAWL_ID INT,
			primary key (domain,ip))""")
   
    print "Table:D_ANALYSIS created successfully"

    conn.execute("""CREATE TABLE IP_ANALYSIS (
			CRAWL_ID INT NOT NULL,
			DOMAIN CHAR(50) NOT NULL,
			ip_count INT ,
			ttl_avg float ,
			PRIMARY KEY(DOMAIN,CRAWL_ID))""")
   
    print "Table:IP_ANALYSIS created successfully"

    conn.execute("""create table error (
			domain char(50) not null,
			err_rate int not null)""")

    conn.close()

def extract_data():
	conn = sqlite3.connect('dns_resolution_info.db')
	print "Database connected successfully"

	conn.execute("""drop table if exists d_analysis""")
	conn.execute("""drop table if exists ip_analysis""")
	conn.execute("""drop table if exists error""")


	create_tables()

	data= conn.execute("""select domain from domains""");
	domains=data.fetchall();


	data= conn.execute("""select max(query_cnt) from querys""")
	count=data.fetchone()

	for domain in domains:
		for i in xrange (1,count[0]+1):
			db = conn.execute("select q.domain, r.resolved_ip, r.ttl, q.query_cnt from results r, querys q where q.domain=('%s') and q.query_cnt=('%r') and q.results_id=r.results_id group by r.resolved_ip"%(domain[0],i));
			database= db.fetchall()
			for data in database:
				db=conn.cursor()
				db.execute("insert or ignore into d_analysis (domain, ip, ttl, crawl_id) values (?, ?, ?, ?)",(data[0],data[1],data[2],data[3]));
					
				conn.commit()

	conn.close
	ip_analysis();


def ip_analysis():
	
	conn=sqlite3.connect('dns_resolution_info.db');
	print 'database connected successfully'
	
	data= conn.execute("""select domain from domains""");
	domains=data.fetchall();


	data= conn.execute("""select max(query_cnt) from querys""")
	count=data.fetchone()

	for domain in domains:
		for i in xrange (1,count[0]+1):
			db=conn.execute("select count(*) from d_analysis where domain=('%s') and crawl_id=('%r') and ip!='0.0.0.0'"%(domain[0],i));
			ip=db.fetchall()
			db=conn.execute("select avg(ttl) from d_analysis where domain=('%s') and crawl_id=('%r') and ip!='0.0.0.0'"%(domain[0],i));
			ttl=db.fetchall()
			ip1=ip[0]
			cnt=ip1[0]
			ttl1=ttl[0]
			avg=ttl1[0]
			db=conn.cursor()
			db.execute("insert into ip_analysis (crawl_id,domain,ip_count,ttl_avg) values (?, ?, ?, ?)",(i, domain[0], cnt, avg));
			conn.commit();
			
	conn.close
	error()
		

def error():
	conn=sqlite3.connect('dns_resolution_info.db');
	print 'database connected successfully'
	
	data= conn.execute("""select domain from domains""");
	domains=data.fetchall();

	data= conn.execute("""select max(query_cnt) from querys""")
	count=data.fetchone()

	db=conn.execute("""select results_id from results where resolved_ip='0.0.0.0' """)
	database=db.fetchall()

	for domain in domains:
		country=['']
		for data in database:
			db=conn.execute("select n.country_id from nameservers n where n.dns_ip=(select dns_ip from querys where results_id='%r' and domain='%s') group by country_id"%(data[0],domain[0]));
			info=db.fetchall()
			country+=info
		err_rate=len(country)/count[0]
		db=conn.cursor()
		db.execute("insert into error (domain,err_rate) values (?, ?)",(domain[0],err_rate));
		conn.commit()
		

	conn.close	
	
if __name__ == '__main__':
	extract_data()
	print 'Analyzing...'
	print 'ip and TTL analysis data is in the Table: ip_analysis'
	print 'error analysis data is in the Table: error'
	     




	
	
	

