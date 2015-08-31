DNS Analysis Part
============================================================
Overview
============================================================
This DNS analysis part contains 2 modules. The first module is used to crawl DNS data and store the data in the database. The other part is used to perform analysis based on the DNS data retrieved from the database.

Enviroment requirements
============================================================
We use dnspython lib to resolve domains and TTL data.
Package for the lib is in the folder named ’tools' in the directory.
installation:
1.unpack the zip package to a directory.
2.cd to the directory
3.type 'python setup.py install'
note: install under root
reference:
http://www.dnspython.org/

Usage
============================================================
1. For the first time, run database_dns.py, create tables, import initial data and query all domains. 
1) The initial data contains public DNS nameservers and domains to be queried. 
2) Public DNS nameservers info is in the public-dns.txt.
3) Domains to be queried is in the domains.txt. When initializing, the path for domains.txt is needed. 
4) Query all the domains several times in several days. Every time the DNS data will be stored in the database.

2. For the analysis, run analysis_dns.py to perform analysis based on the DNS data retrieved from the database. The analysis results will be stored back in the database.
