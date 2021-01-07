# -*- coding: utf-8 -*-

"""

@ author: Taehyeong Kim, Minji Kang, Fusion Data Analytics and Artificial Intelligence Lab

"""

import pandas as pd
import re
import tqdm

class ConceptIdMapping:
    
    def __init__(self):
        print("--- concept_id mapping ---")
        
        
    def concept_id_mapping(self, df):
        
        # concept_id, no_label 파일 불러오기
        concept = pd.read_csv("utils/concept_id_table.csv", encoding = "CP949", index_col = 'concept_id')
        concept["concept_name"] = concept.concept_name.apply(lambda x : x.lower())
        no_label_table = pd.read_csv("utils/no_label_mapping.csv", encoding = "CP949", index_col = 'origin_concept_name')
        no_label_table["concept_name"] = no_label_table.concept_name.apply(lambda x : x.lower())

        # concept_id dict형태로 만들기
        concept_dic = concept['concept_name'].to_dict()
        id_dic = {v: k for k, v in concept_dic.items()}
        label_list = df['resistance_label'].values.tolist()

        # no_label dict형태 만들기 (origin : 대체)
        no_label_dict = no_label_table["concept_name"].to_dict()

        # 바꾼 concept_id list
        concept_label = []
        concept_label_final = []
        # concept_id가 없는 라벨 list
        no_label = []

        # 라벨을 concept_id로 바꾸기
        for label in label_list:
            one_concept_label =[]
            for one_label in label:
                if one_label in id_dic:
                    one_concept_label.append(id_dic[one_label])
                else:
                    # 대체 이름으로 바꾸고 concept_id 맵핑
                    if one_label in no_label_dict:
                        one_label = no_label_dict[one_label]
                        one_concept_label.append(id_dic[one_label])
                    else:
                        one_concept_label.append('no label')
                        no_label.append(one_label)
            concept_label.append(one_concept_label)
            concept_label_final.append(one_concept_label[0])

        # 데이터 프레임에 열 추가
        df['concept_id'] = concept_label
        df['concept_id_final'] = concept_label_final

        # No Label List
        if len(no_label)!=0:
            no_label_list=pd.Series(sorted(list(set(no_label))), name='No Label List')
            no_label_list.to_csv("utils/validation/no_label_list.csv", index = False, header=True, encoding = "CP949")
            
        return df