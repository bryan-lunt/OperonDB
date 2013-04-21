import operondb
import schema


import sqlalchemy
import sqlalchemy.engine
import sqlalchemy.engine.url

from sqlalchemy.orm import sessionmaker

class LuntOperonDBConnection(operondb.OperonDBConnection):
	
	schema = schema
	
	def __init__(self,inengine,config):
		self.engine = inengine
		self.createTables(force=False)
		self.SessionClass = sessionmaker(bind=self.engine)
		super(LuntOperonDBConnection, self).__init__(config)
	
	def get_raw_session(self):
		"""
		Get a new session to the operon database.
		
		@rtype: sqlalchemy.orm.session.Session
		@return session: A new SQLAlchemy session connected to the database and ready to use operondb.schema objects.
		"""
		return self.SessionClass()
	
	def createTables(self,force=False):
		try:
			schema.create_tables(self.engine)
		except:
			if force:
				raise Exception("Could not create tables")
			else:
				pass

	def getChromosomeIDfromGene(self,geneid):
		tempSession = self.get_raw_session()
		
		ourGene = tempSession.query(schema.Gene).filter_by(PID=geneid).first()
		itsOperon = ourGene.operon
		
		return itsOperon.chromosomeGI

	def getOperonIDfromGene(self,geneid):
		tempSession = self.get_raw_session()
		ourGene = tempSession.query(schema.Gene).filter_by(PID=geneid).first()
		
		return ourGene.operonID

	def getTaxnameFromGene(self, geneid):
		tempSession = self.get_raw_session()
		ourGene = tempSession.query(schema.Gene).filter_by(PID=geneid).first()
		itsOperon = ourGene.operon
		itsChromosome = itsOperon.chromosome
		itsGenome = itsChromosome.genome
		
		return itsGenome.Taxname


def new_connection(config):
	
	#create an appropriate engine, and wrap it in an OperonDBConnection object.
	
	ConnectionURL = sqlalchemy.engine.url.URL(**config)
	
	theengine = sqlalchemy.create_engine(ConnectionURL)
	
	return LuntOperonDBConnection(theengine,config)