import os, sys, re
import psycopg # Yes, we use psycopg...
base = ''
arquivo = ''
 
if not os.path.exists('/usr/bin/pv'):
	print("The pv package is not installed.\n Installing pv.")
	os.system('sudo apt-get install pv')
 
for arg in sys.argv:
	if arg.startswith('-b'):
		base = re.sub('-b', '', arg)
	elif arg.startswith('-a'): 
		arquivo = re.sub('-a', '', arg)
 
if not base or not arquivo:
	print("""
Specify the postgres's variables before use
python dump.py -b<basename> -a<filename>
""")
else:
	conn = psycopg.connect("dbname=%s user=%s "% (os.environ['PGDATABASE'], os.environ['PGUSER'])) 
	cur = conn.cursor()
	cur.execute("SELECT pg_database_size(pg_database.datname) "\
	            "FROM pg_database WHERE pg_database.datname = '%s'" % os.environ['PGDATABASE']) 
	base_size = int(cur.fetchone()[0] / 2)
 
	# Let's go to candy mountain Charlie...
	print('\nGenerating dump from  %s to %s' % (base, arquivo)) 
	os.system('pg_dump %s | pv -s %d > %s ' % (base, base_size, arquivo)) 
	print('Dump file generated!')
