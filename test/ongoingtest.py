'''
Created on Apr 11, 2013

@author: lunt
'''

import operondb

DBCon = operondb.get_connection(operondb.read_config(['./operondb.cfg']))
asess = DBCon.get_raw_session()

schema = DBCon.schema

#myGenome = schema.Genome(1,2,'foobar baz')


#myChromo = schema.Chromosome('NC_1111',12345,2,1)

#myGenome.chromosomes = [myChromo]

#asess.add(myGenome)
#asess.commit()

DBCon.getOperonIDfromGene(110622980)