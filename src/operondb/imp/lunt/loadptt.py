#!/usr/bin/env python

import re
import csv
import os
import sys

from operondb import *
from operondb.imp.lunt.schema import Genome, Chromosome, Operon, Gene

#gene generator, reads gene PTT files
def readptt_yield_genes(myfile):
	reader = csv.reader(myfile,delimiter='\t')
	reader.next()
	reader.next()
	reader.next()
	for line in reader:
		retval = {}
		beginend = re.split("\\.\\.",line[0])
		retval["start"] = beginend[0]
		retval["ending"] = beginend[1]
		retval["sense"] = line[1] is "+"
		retval["length"] = line[2]
		retval["PID"] = line[3]
		if( line[4] is "-"):
			retval["gene"] = None
		else:
			retval["gene"] = line[4]
		retval["synonym"] = line[5]
		if( line[6] is "-"):
			retval["code"] = None
		else:
			retval["code"] = line[6]
		if( line[7] is "-"):
			retval["COG"] = []
		else:
			retval["COG"] = line[7].split(',')
		if( line[8] is "-"):
			retval["product"] = None
		else:
			retval["product"] = line[8]

		OneGene = Gene(retval['PID'],None,retval['sense'],retval['start'],retval['ending'],retval['length'])

		yield OneGene


#a generator over operons
#call it with an iterator gotten from the readptt(filename) function
#Operon Prediction in our program is exactly an FSA
def operons(geneitr,operonGap=200):	
	alist = list()
	#do unambiguous internal operons
	for gene in geneitr:
		if len(alist) == 0 or (gene.sense is alist[-1].sense and int(gene.beginning) - int(alist[-1].ending) < operonGap):
			#continuing a started operon
			alist.append(gene)
		else:
			#return an operon
			#retval = {"start":alist[0]["start"],"ending":alist[-1]["ending"],"sense":alist[-1]["sense"],"genes":alist}
			retval = Operon(None,alist[0].sense,alist[0].beginning,alist[0].ending)
			retval.genes = alist
			yield retval
			alist = [gene]
			
	#cleanup the last operon.
	#retval = {"start":alist[0]["start"],"ending":alist[-1]["ending"],"sense":alist[-1]["sense"],"genes":alist}
	retval = Operon(None,alist[0].sense,alist[0].beginning,alist[0].ending)
	retval.genes = alist
	yield retval

def	load_operons_from_ptt(asession,fileobject,theChromosome=None):
	"""
	"""

	myoperons = operons(readptt_yield_genes(fileobject))

	for oneOp in myoperons:
		oneOp.chromosome = theChromosome
		asession.add(oneOp)


#main
def main():
	from optparse import OptionParser
	
	parser = OptionParser("%prog [options] <.ptt file>")
	parser.add_option('-c',dest='configfile',default=None)
	options, args = parser.parse_args()
	
	INFILE = args[0]

	accession = os.path.basename(INFILE).replace(".ptt","")
	print accession
	
	
	#connect
	DBCon = get_connection(read_config([options.configfile]) if options.configfile is not None else None)
	asess = DBCon.get_raw_session()

	try:
		mainChromo = asess.query(Chromosome).filter_by(accession=accession)[0]
	except:
		print "Chromosome not yet created."

	
	#read operons
	load_operons_from_ptt(asess,open(INFILE),mainChromo)
	
	asess.commit()
	asess.close()


if __name__ == "__main__":
	main()
