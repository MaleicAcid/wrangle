#!/bin/bash

curl -O http://hgdownload.cse.ucsc.edu/goldenPath/hg18/database/refGene.txt.gz
gunzip -c refGene.txt.gz > refGene_hg18
echo '{ "cgdata" : {"name" : "refGene_hg18", "type" : "genePred", "assembly" : "hg18"} }' > refGene_hg18.json
