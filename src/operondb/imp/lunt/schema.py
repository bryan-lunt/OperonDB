'''
Created on Apr 11, 2013

@author: lunt
'''

import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()

from sqlalchemy import Column, Integer, String, Boolean, Sequence, ForeignKey
from sqlalchemy.orm import relationship, backref

class Genome(Base):
	__tablename__ = 'genome'
	
	Taxid		= Column(Integer, primary_key=True, index=True)
	GenomeID	= Column(Integer)
	Taxname		= Column(String)
	
	def __init__(self,taxid,genomeid,taxname):
		self.Taxid = taxid
		self.GenomeID = genomeid
		self.Taxname = taxname
	
class Chromosome(Base):
	__tablename__ = 'chromosome'
	
	accession	= Column(String, unique=True, nullable=False)
	GI			= Column(Integer, primary_key = True)
	GenomeID	= Column(Integer)
	Taxid		= Column(Integer, ForeignKey('genome.Taxid'))
	
	genome		= relationship('Genome',backref=backref('chromosomes',order_by=GI))

	def __init__(self,accession,gi,genomeid,taxid):
		self.accession	= accession
		self.GI			= gi
		self.GenomeID	= genomeid
		self.Taxid		= taxid

class Operon(Base):
	__tablename__ = 'operon'
	
	id			= Column(Integer, Sequence('operon_id_seq'), primary_key=True)
	beginning	= Column(Integer)
	ending		= Column(Integer)
	sense		= Column(Boolean, nullable=False)
	chromosomeGI = Column(Integer, ForeignKey('chromosome.GI'))
	
	chromosome	= relationship('Chromosome',backref=backref('operons',order_by=beginning))
	
	def __init__(self,chromoGI,sense,begin=None,end=None):
		self.beginning	= begin
		self.ending		= end
		self.sense		= sense
		self.chromosomeGI	= chromoGI

class Gene(Base):
	__tablename__ = 'gene'
	
	
	PID			= Column(Integer, index=True,primary_key=True)
	sense		= Column(Boolean)
	beginning	= Column(Integer)
	ending		= Column(Integer)
	length		= Column(Integer)
	UniProtAC	= Column(String, index=True)
	UniProtID	= Column(String, index=True)
	operonID	= Column(Integer, ForeignKey('operon.id'), index=True)
	
	operon		= relationship('Operon',backref=backref('genes',order_by=beginning))
	
	def __init__(self,PID,operonID,sense,beginning=None,ending=None,length=None,UniProtAC=None,UniProtID=None):
		self.PID		= PID
		self.operonID	= operonID
		self.sense		= sense
		self.beginning	= beginning
		self.ending		= ending
		self.length		= length
		self.UniProtAC	= UniProtAC
		self.UniProtID	= UniProtID

def create_tables(anEngine):
	Base.metadata.create_all(anEngine)