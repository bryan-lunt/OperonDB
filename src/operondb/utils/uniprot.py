
UNIPROT_PROTEOME_REQUEST_TEMPLATE="http://www.uniprot.org/proteomes/{proteome}"

import urllib2
import BeautifulSoup as BS

def get_assembly_ID_for_ref_proteome(proteome_id):
    s = BS.BeautifulSoup(urllib2.urlopen(UNIPROT_PROTEOME_REQUEST_TEMPLATE.format(proteome=proteome_id)))
    dbt = s.find("table",attrs={"class":"databaseTable"})
    aspan = dbt.find("span",text="Genome assembly")
    assembly_ID = aspan.parent.parent.nextSibling.find("a").getText().strip()
    return assembly_ID

