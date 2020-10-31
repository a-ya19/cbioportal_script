from bravado.client import SwaggerClient
from collections import Counter
from getGeneIdList import getGeneIdList
import xlsxwriter

# Connects to cbioportal database api
# Turned off validation requests because of discovered incorrect error throwing
cbioportal = SwaggerClient.from_url('https://www.cbioportal.org/api/api-docs',
                                    config={"validate_requests":False,"validate_responses":False})

# Make resources all lower-case and underlined for easy access
for a in dir(cbioportal):
    cbioportal.__setattr__(a.replace(' ', '_').lower(), cbioportal.__getattr__(a))

# Get list of studies: MSK is the largest query that contains correctly formatted categories
studyIds = ["msk_impact_2017"]

# Get list of gene Ids from function implemented in getGeneIdList.pycfor api to work correctly
geneList = getGeneIdList()

# Find number of amplifications
amplificationsInStudies = []
mutationsInStudies = []

for studyId in studyIds:
    print(studyId + "_all")
    print(studyId + "_cna")
    amplificationsInStudies.append(cbioportal.discrete_copy_number_alterations.fetchDiscreteCopyNumbersInMolecularProfileUsingPOST(
        discreteCopyNumberEventType = "AMP", # specifies amplification
        discreteCopyNumberFilter = {"entrezGeneIds":geneList, "sampleListId": studyId + "_all"}, # specifies genes to return
        molecularProfileId = studyId + "_cna", # specifies gistic for amplification events
        projection = "DETAILED" # returns detailed gene name for later use
    ).result())

    mutationsInStudies.append(cbioportal.mutations.fetchMutationsInMolecularProfileUsingPOST(
        mutationFilter = {"entrezGeneIds":geneList, "sampleListId": studyId + "_all"}, # specifies genes to return
        molecularProfileId = studyId + "_mutations", # specifies gistic for amplification events
        projection = "DETAILED"
    ).result())

mutation_counts = Counter()
for mutations in mutationsInStudies:
    mutation_counts += Counter([m.gene.hugoGeneSymbol for m in mutations])
    print(mutation_counts.most_common(6))

amplification_counts = Counter()
for amplifications in amplificationsInStudies:
    amplification_counts = Counter([a.gene.hugoGeneSymbol for a in amplifications])
    print(amplification_counts.most_common(5))

outWorkBook = xlsxwriter.Workbook("rnf_output.xlsx")
mutSheet = outWorkBook.add_worksheet("Mutations")
ampSheet = outWorkBook.add_worksheet("Amplifications")

mutSheet.write("A1", "Gene")
mutSheet.write("B1","Mutation")
ampSheet.write("A1", "Gene")
ampSheet.write("B1","Amplification")

# Print summary to terminal
geneCount = 0
print("\nGenes with Substantial Mutations:\n")
for gene, tally in mutation_counts.most_common():
    if tally < 10:
        break
    print(gene, tally)
    mutSheet.write(geneCount+1,0,gene)
    mutSheet.write(geneCount+1,1,tally)
    geneCount += 1

geneCount = 0
print("\nGenes with Substantial Amplification:\n")
for gene, tally in amplification_counts.most_common():
    if tally < 10:
        break
    print(gene, tally)
    ampSheet.write(geneCount+1,0,gene)
    ampSheet.write(geneCount+1,1,tally)
    geneCount += 1

outWorkBook.close()