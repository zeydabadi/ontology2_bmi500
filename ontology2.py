#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov 10 16:31:04 2018

@author: Mahmoud Zeydabadinezhad
"""
# convert as many ICD10-to-ICD9 1:many mappings as possible into 1:1 mappings
import pandas as pd
import sys
def ontology1(File1, File2):
    """
    Inputs: 
        - File1: Path to the 2018_I10gem.txt
        - File2 Path to the 2018_I9em.txt
    
    Outputs: 
        - Prints out the number of one-to-one, one-to-many, and terms with no mapping.
    """

    # Read the contents of 2018_I10gem.txt
    columns  = ['Code10','Code9','Flags'] 
    ICD10To9 = pd.read_fwf(File1, names=columns, converters={0:str, 1:str, 2:str})
    ICD10To9.drop('Flags', axis=1, inplace=True) # Remove the Flags column
    print("Total row# in 2018_I10gem.txt is: ", ICD10To9.shape[0])

    # Read the contents of ICD9.csv and ICD10.csv
    # The reason that I read TotalDiag as string is that the last row contains a big number so I cannot read it as int.
    # After reading it as string I need to delete that row and convert it back to int.
    ICD9  = pd.read_csv(File2,converters={0:str, 0:str})
    ICD9.drop(ICD9.columns[2:], axis=1,inplace=True) # Just leave the first two columns. I don't need the rest.
    ICD9.drop(ICD9.tail(1).index,inplace=True) #remove the last row
    ICD9["TotalDiag"] = pd.to_numeric(ICD9["TotalDiag"]) #Convert the second column to numeric

    GroupedCode = ICD10To9.sort_index().groupby('Code10').filter(lambda group: len(group) != 1) #Find Code10s that are repeated.
    print("Number of repeated ICD10 codes is: ", GroupedCode.shape[0])
    # Add a '.' to the Code9 after the third element to match the data in ICD9
    def addpoint(code):
        return code[0:3]+'.'+code[3:]

    GroupedCode['Code9'] = GroupedCode.Code9.apply(addpoint)

    # Merging GroupedCode and ICD9 and then sorting based on TotalDiag and then removing the repeated Code10s
    merged_df = pd.merge(GroupedCode, ICD9, right_on='ICD9CMCode', left_on='Code9')
    OneToOneCodes = merged_df.sort_values('TotalDiag', ascending=False).drop_duplicates(['Code10'])
    OneToOneCodes.drop(OneToOneCodes.columns[2:], axis=1,inplace=True) # Only keep the first two columns
    print("Number of ICD10 codes after mapping to most frequent ICD9 code is: ", OneToOneCodes.shape[0])
    print("\nThe first 10 rows of the one to one mapping codes:\n",OneToOneCodes.head(10))
    

if __name__== "__main__":
    if len(sys.argv) == 3:
        ontology1(sys.argv[1],sys.argv[2])
    else:
        sys.exit("\nUsage: ontology2 path_to_2018_I10gem.txt path_to_ICD9.csv\n\n\n\n")