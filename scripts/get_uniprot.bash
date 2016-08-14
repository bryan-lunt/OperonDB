#!/bin/bash

basedir=$1
mkdir -p ${basedir}

pushd ${basedir}

curl ftp://ftp.uniprot.org/pub/databases/uniprot/current_release/knowledgebase/reference_proteomes/README > README.uniprot
curl ftp://ftp.ncbi.nlm.nih.gov/genomes/genbank/bacteria/assembly_summary.txt > assembly_summary_bacteria.txt
curl ftp://ftp.ncbi.nlm.nih.gov/genomes/genbank/archaea/assembly_summary.txt > assembly_summary_archaea.txt


#get the IDs of all the proteomes so we can look up which genome assemblies they come from.
awk '/Proteome_ID/,/^$/ {print $0;}' README.uniprot | head -n-1 | tail -n+2 > uniprot_proteome_list.txt

mkdir -p refproteome_id_mappings
#(cd refproteome_id_mappings; wget ftp://ftp.uniprot.org/pub/databases/uniprot/current_release/knowledgebase/reference_proteomes/Bacteria/*idmapping.gz)
#(cd refproteome_id_mappings; wget ftp://ftp.uniprot.org/pub/databases/uniprot/current_release/knowledgebase/reference_proteomes/Archaea/*idmapping.gz)

popd
