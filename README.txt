This directory contains stored SQL statements to create the amaranth operon database and scripts to populate it from files available at NCBI. The sql script can be executed from the postgresql terminal.

These scripts must be run in the following order:
operondb.imp.lunt.loadrpt.py
operondb.imp.lunt.loadptt.py


loadrpt.py
	Basically this script gets pointed at a directory whos subdirectories contain NCBI .rpt files whos metadata you'd like to load into the database.
	This script needs to have the first line after #main be edited for the settings in your database, obviously if you are not using postgresql, any other python database module will work, make sure that you have the proper schema in place.

loadptt.py
	Point this script at a directory whos sub directories contain .ptt files, and the appropriate gene and operon metadata will be loaded/created into the database.
	This script needs to have the first line after #main be edited for the settings in your database, obviously if you are not using postgresql, any other python database module will work, make sure that you have the proper schema in place.

CONFIGURATION
operondb searches the following configuration files:
"./operondb.cfg"
"~/.operondb.cfg"
"/etc/operondb.cfg"

and expects a section titled "operondb" to have (some of) the following parameters:

'imp' Tells which implementation to use, if omitted, defaults to 'operondb.imp.lunt'

'drivername' Tells SQLAlchemy what driver to use.
'username'	 etc
'password'	etc
'host'	etc
'port'	etc
'database'	etc
'query' Another SQLAlchemy specific option



CREATING THE DATABASE
once you have downloaded the .rpt and .ptt files from RefSeq, for each genome/chromosome, you should run

python -m operondb.imp.lunt.loadrpt ONEFILE.rpt
python -m operondb.imp.lunt.loadptt ONEFILE.ptt