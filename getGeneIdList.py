from bravado.client import SwaggerClient

# getGeneIdList() returns a list of entrez gene id's based on 
# the unique gene names of RNF proteins given in the textfile.
def getGeneIdList():

    # Connect to cbioportal api
    cbioportal = SwaggerClient.from_url('https://www.cbioportal.org/api/api-docs',
                                        config={"validate_requests":False,"validate_responses":False})

    for a in dir(cbioportal):
        cbioportal.__setattr__(a.replace(' ', '_').lower(), cbioportal.__getattr__(a))

    # Read information from txt file with gene names
    rnfFile = open("unique_proteins.txt", "r")

    # Read file of with unique gene names where empty lines signify RNF[Line #]
    # exceptions represents cases where there is no RNF gene
    # Create geneList to store all gene names
    geneList = []
    exceptions = [42, 117, 118, 120, 132, 136, 140, 143, 162]
    for i in range(1,226):
        currentGene = rnfFile.readline().rstrip('\n')
        if i in exceptions:
            continue
        if len(currentGene) == 0: # if gene is empty, the name is normal rnf[#]
            geneList.append("RNF" + str(i))
        else:
            geneList.append(currentGene)

    # Create a txt file with all gene Names filled in for future reference
    outFile = open("full_gene_list.txt", "w+")
    for gene in geneList:
        outFile.write(gene)
        outFile.write("\n")

    

    # Use database to get entrez gene id corresponding to gene names
    entrezGeneIdList = []
    for geneName in geneList:
        #print(geneName)
        entrezGeneIdList.append(cbioportal.genes.getGeneUsingGET(
            geneId = geneName
        ).result().entrezGeneId)

    outFile2 = open("gene_ids.txt", "w+")
    for geneId in entrezGeneIdList:
        outFile2.write(str(geneId))
        outFile2.write("\n")
    
    return entrezGeneIdList


l1 = getGeneIdList()