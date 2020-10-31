# cbioportal script

## What is this script?
This is a Python script created for the lab of Dr. Jianhua Yang (PhD, Texas Children's Hospital) in order to automate the process of finding RNF (RING finger proteins) genes to investigated based on bioinformatics data in cbioportal. It searches for significantly amplified and mutated RNF genes in the MSK Impact 2017 Study using the open source Swagger API (based on REST) created by cbioportal. 

## Structure
There are only two files that are used in this script. getGeneIdList.py contains only one function which returns a list of Entrez Gene Id's (Numerical) from the name of the genes provided. The RNF proteins are the proteins from [RNF1,RNF225]; however, some of them have proper, unique names which break from this convention. The original list of genes was provided in the excel sheet "rnf_proteins.xlsx"; however, the actual input that getGeneIdList() takes is a txt file "unique_proteins.txt" which was created from copy and pasting the column of unique names, with spaces for the genes with the standard RNF_ name. 

The main file which executes the script is "main.py" which uses the list of Entrez Gene Id's and queries for instances of mutations and amplifications. Afterwards, it outputs the resulting counts of each gene's mutations or amplifications to two appropriately named sheets in rnf_output.xlsx.
