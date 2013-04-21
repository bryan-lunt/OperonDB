'''
Created on Apr 11, 2013

@author: lunt
'''
import os, ConfigParser

import importlib

DEFAULT_IMPLEMENTATION = "operondb.imp.lunt"

class OperonDBConnection(object):
	"""
	Objects of this class represent open connections to an operon database, and have methods for some simple queries.
	
	
	"""

	def __init__(self,config):
		self.config = config
	
	def get_raw_session(self):
		"""
		Return a raw session from the underlying implementation.
		
		In general, you should not use this.
		
		@return: A raw session object, sqlalchemy, psychodb, etc
		"""
		raise NotImplementedError("Abstract Base Class")
		
	def close(self):
		"""Close the connection to the database, and invalidate this object.
		"""
		pass

	def createTables(self,force=False):
		raise NotImplementedError("Abstract Base Class")

	def getChromosomeIDfromGene(self, geneobject):
		"""Simple helper function, give it a gene object, or an int or string representation of the GI of a gene, and it finds the chromosome it belongs to.
		
		@param geneobject: Some representation of the gene.
		@type geneobject: Gene, str, or int
		
		@return:	An appropriate representation of the chromosome
		@rtype:		Based on input type, if input was a Gene, Chromosome; if str, str; if int, int
		"""
		raise NotImplementedError("Abstract Base Class")

	def getOperonIDfromGene(self, geneobject):
		"""Finds the operonID for the provided gene.
		
		@param geneobject: Some representation of the gene.
		@type geneobject: Gene, str, or int
		
		@return:	An appropriate representation of the operon
		@rtype:		Based on input type, if input was a Gene, Operon; if str, str; if int, int
		"""
		raise NotImplementedError("Abstract Base Class")

	def getTaxnameFromGene(self, geneobject):
		"""Gets the NCBI Taxname for the species that contains a particular gene.
		
		@param geneobject: Some representation of the gene.
		@type geneobject: Gene, str, or int
		
		@return:	An appropriate representation of the Taxname
		@rtype:		str
		"""
		raise NotImplementedError("Abstract Base Class")

def read_config(filelist=["./operondb.cfg",os.path.expanduser("~/.operondb.cfg"),"/etc/operondb.cfg"]):
	"""
	Helper method to read a configuration, mostly, it knows about default paths.
	
	@rtype: dict
	@return: A dictionary of connection information.
	
	"""
	configp = ConfigParser.ConfigParser()
	configp.read(filelist)
	optDictTmp = dict(configp.items("operondb"))
	
	#sanitize that for SQLAlchemy
	valid_keys = ['drivername','username','password','host','port','database','query']
	optDict = dict([(key,optDictTmp[key]) for key in valid_keys if optDictTmp.has_key(key)])
	
	return optDict

def get_connection(config=None):
	"""
	Factory function that creates a connection to an operon database.
	
	
	@param config: A dictionary of connection parameters, if not provided, they will be read from system default config files.
	@type config: dict
	
	@return: A new connection to the Operon Database described in config (or the default if None)
	@rtype: OperonDBConnection
	
	"""
	
	if config is None:
		config = read_config()#Reads the system default config.
	
	#magic
	moduleName = config.get("imp",DEFAULT_IMPLEMENTATION)
	mod = importlib.import_module(moduleName)
	
	retval = mod.new_connection(config)
	return retval