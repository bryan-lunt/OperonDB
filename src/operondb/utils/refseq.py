
ASSEMBLY_TABLE_SQL="""CREATE TABLE if not exists assem_sum (assembly_accession, bioproject, biosample, wgs_master, refseq_category, taxid, species_taxid, organism_name, infraspecific_name, isolate, version_status, assembly_level, release_type, genome_rep, seq_rel_date, asm_name, submitter, gbrs_paired_asm, paired_asm_comp, ftp_path, excluded_from_refseq);"""

import sqlite3
import csv

class assm_table(object):
    """
A database table (backed with sqlite3) for storing information about assemblies.

This can be used to figure out where the cannonical assembly for a particular species is. (maybe?)

    """
    def __init__(self):
        self.conn = sqlite3.connect(":memory:")
        self.conn.execute(ASSEMBLY_TABLE_SQL)
    
    def populate_from(self,file_like):
        """
        Populate the assembly table from a uniprot assembly_summary.txt file.

An example file is available at "ftp://ftp.ncbi.nlm.nih.gov/genomes/genbank/bacteria/assembly_summary.txt"


        """
        tsv_reader = csv.reader(file_like,delimiter="\t")
        for i in tsv_reader:
            if i[0].startswith("#"):
                continue
            try:
                self.conn.execute("insert into assem_sum values (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)", map(lambda x:x.decode("utf8"),i))
            except:
                print i
    
    def get_by_assembly_accession(self,assm_accession):
        cursor = self.conn.execute("select assembly_accession, taxid, species_taxid, ftp_path from assem_sum where assembly_accession = (?)", [assm_accession])
        return cursor

