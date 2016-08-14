#!/bin/bash

basedir=$1
mkdir -p ${basedir}

pushd ${basedir}

curl ftp://ftp.uniprot.org/pub/databases/uniprot/current_release/knowledgebase/reference_proteomes/README > README.uniprot
curl ftp://ftp.ncbi.nlm.nih.gov/genomes/genbank/bacteria/assembly_summary.txt > assembly_summary_bacteria.txt
curl ftp://ftp.ncbi.nlm.nih.gov/genomes/genbank/archaea/assembly_summary.txt > assembly_summary_archaea.txt


#get the IDs of all the proteomes so we can look up which genome assemblies they come from.
#unfortunately, this doed not limit itself to bacteria and archaea....
awk '/Proteome_ID/,/^$/ {print $0;}' README.uniprot | head -n-1 | tail -n+2 > uniprot_proteome_list.txt

#get the lists of available Bacteria and Archae proteomes.
curl ftp://ftp.uniprot.org/pub/databases/uniprot/current_release/knowledgebase/reference_proteomes/Bacteria/ > uniprot_Bacteria_filelist.txt
curl ftp://ftp.uniprot.org/pub/databases/uniprot/current_release/knowledgebase/reference_proteomes/Archaea/ > uniprot_Archaea_filelist.txt

#get just a list of uniprot ids and (taxids?)
awk '/ UP/' uniprot_Archaea_filelist.txt | sed 's/^.*UP\([[:digit:]]\+\)_\([[:digit:]]\+\).*/UP\1	\2/;' | uniq > uniprot_Archaea_ids.txt
awk '/ UP/' uniprot_Bacteria_filelist.txt | sed 's/^.*UP\([[:digit:]]\+\)_\([[:digit:]]\+\).*/UP\1 \2/;' | uniq > uniprot_Bacteria_ids.txt

mkdir -p refproteome_id_mappings
#(cd refproteome_id_mappings; wget ftp://ftp.uniprot.org/pub/databases/uniprot/current_release/knowledgebase/reference_proteomes/Bacteria/*idmapping.gz)
#(cd refproteome_id_mappings; wget ftp://ftp.uniprot.org/pub/databases/uniprot/current_release/knowledgebase/reference_proteomes/Archaea/*idmapping.gz)

popd
