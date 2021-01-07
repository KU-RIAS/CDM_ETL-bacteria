# -*- coding: utf-8 -*-

"""

@ author: Taehyeong Kim, Minji Kang, Fusion Data Analytics and Artificial Intelligence Lab

"""

import pandas as pd

import warnings
warnings.filterwarnings("ignore")

import utils.organ_result
import utils.susceptibility_test
import utils.resistance_label
import utils.concept_id_mapping

if __name__ == '__main__':
    
    print("csv read")
    df = pd.read_csv("data/sample data.csv", encoding = "CP949") # Data read
    print("data columns :", list(df.columns))
    
    # --- organ result ---
    df = utils.organ_result.OrganResult().organ_result(df)
    
    # --- susceptibility test ---
    df = utils.susceptibility_test.SusceptibilityTest().susceptibility_test(df)
    
    # --- resistance label ---
    df = utils.resistance_label.ResistanceLabel().resistance_label(df)
    
    # --- concept_id mapping ---
    df = utils.concept_id_mapping.ConceptIdMapping().concept_id_mapping(df)
    
    print("csv print")
    df.to_csv("result.csv", index = False, encoding = 'CP949')
    
    print("End!")