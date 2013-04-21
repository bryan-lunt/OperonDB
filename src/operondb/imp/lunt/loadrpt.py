#!/usr/bin/env python

import re
import csv
import os


from operondb import *
from operondb.imp.lunt.schema import Genome, Chromosome, Operon, Gene

neededrptfields = ['Accession','GI']
nullablefields = ['Taxid','Taxname','Genome_ID']
def readrpt(myfile):
	tmpdict = {}
	#retval = dict([tuple(re.split(' *:|= *',line.strip())[:2]) for line in myfile])
	#if any([not retval.has_key(field) for field in neederptfields]):
	#	return None
	for line in myfile:
		footmp = re.split(' *:|= *',line)
		tmpdict[footmp[0].strip()] = footmp[1].strip()
	
	retval = Chromosome(tmpdict['Accession'].split('.')[0],tmpdict['GI'],tmpdict.get('Genome_ID'),tmpdict.get('Taxid'))
	return retval

#main
def main():
	from optparse import OptionParser
	
	parser = OptionParser("%prog [options] <.ptt file>")
	parser.add_option('-c',dest='configfile',default=None)
	options, args = parser.parse_args()
	
	INFILE = args[0]
	
	oneChromo = readrpt(open(INFILE))
	
	#connect
	DBCon = get_connection(read_config([options.configfile]) if options.configfile is not None else None)
	asess = DBCon.get_raw_session()
	
	asess.add(oneChromo)
	
	asess.commit()
	asess.close()
	

if __name__ == "__main__":
	main()
