#combine dosages from input pops and combine all the SNPs that overlap to output combined dosages and combined sample files
#by Angela Andaleon (aandaleon@luc.edu)
from __future__ import division #using python 2 like a fool
import pandas as pd

pops = ["LWK", "MKK", "YRI"]
chrs = range(1, 23)
combined = "AFR"
#chrs = range(22, 23) #for testing
print("Combining dosages for: " + ", ".join(pops))

for chr in chrs:
    #load in first
    pop_1 = pd.read_csv("/home/jennifer/New_Dosages/" + pops[0] + "/" + pops[0] + "_" + str(chr) + ".dosage.txt", delim_whitespace = True, header = None)
    pop_1.columns = ["chr", "rsid", "pos", "A1", "A0", "AF"] + list(pd.read_csv("samples_" + pops[0] + ".txt", delim_whitespace = True, header = None).loc[:, 0]) #add column names of individuals to keep them straight
    pop_1 = pop_1.drop("AF", axis = 1) #drop allele frequency b/c dosage-file specific
    
    #then load in the rest of them
    for pop_num in range(1, len(pops)):
        pop_2 = pd.read_csv("/home/jennifer/New_Dosages/" + pops[pop_num] + "/" + pops[pop_num] + "_" + str(chr) + ".dosage.txt", delim_whitespace = True, header = None)
        pop_2.columns = ["chr", "rsid", "pos", "A1", "A0", "AF"] + list(pd.read_csv("samples_" + pops[pop_num] + ".txt", delim_whitespace = True, header = None).loc[:, 0])
        pop_2 = pop_2.drop("AF", axis = 1)
        pop_1 = pd.merge(pop_1, pop_2, on = ["chr", "rsid", "pos", "A1", "A0"], how = "inner") #inner join b/c predictdb does not play well with missing values, so only keep SNPs in common
        
    #re-add allele frequency column
    dosages_only = pop_1.iloc[:, 5:] #can't calculate w/ string columns
    AF = dosages_only.sum(axis = 1) / len(dosages_only.columns) #recalculate allele frequencies
    pop_1.insert(5, "AF", AF) #needs to be index 5
    pop_1.to_csv("chr" + str(chr) + "_" + combined + ".dosage.txt", sep = " ", columns = None, header = False, index = False)
    
    #write combined samples file
    samples = list(pop_1.columns[6:])
    samples = pd.DataFrame({0: samples, 1: samples}) #I'm going to assume FID and IID are the same
    samples.to_csv("samples_" + combined + ".txt", sep = " ", columns = None, header = False, index = False)
    print("Completed with chr. " + str(chr) + ".")    
print("Completed with combining dosages. Have a nice day :).")