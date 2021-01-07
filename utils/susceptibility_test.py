# -*- coding: utf-8 -*-

"""

@ author: Taehyeong Kim, Minji Kang, Fusion Data Analytics and Artificial Intelligence Lab

"""

import pandas as pd
import re

class SusceptibilityTest:
    
    def __init__(self):
        print("--- susceptibility test ---")
        
        
    def susceptibility_test(self, df):
        
        # (Organism, Amount, Colony Count) extraction
        df=self.extractor(df, "organ", "organism")
        df=self.extractor(df, "amount", "amount")
        df=self.extractor(df, "colony count", "colony_count")
        
        # Organism Check
        
        # Delete organism == ""
        df = df.drop(df[df["organism"] == ""].index)
        
        organ_name = (i for i in df['organism'])
        
        for _ in range(len(df["organism"])):

            organ = next(organ_name)
            
            df["organism"].iat[_]=self.organ_check(organ).strip()
            
        # Organism List
        organ_list=pd.Series(sorted(list(set(df["organism"]))), name='Organ List')
        organ_list.to_csv("utils/validation/organ_list.csv", index = False, header=True, encoding = "CP949")
            
        # Anti Extraction & Susceptibility Test
        df=self.new_susceptibility_test(df)
            
        return df
        
        
    def extractor(self, df, extract_value, feature_name):
        
        temp_list = []
        
        organ_result = (i for i in df["organ_result"])
        
        for _ in range(len(df)):
            
            text = next(organ_result)
            
            sentence = (i for i in text)
            
            for num in range(len(text)):
                
                element = next(sentence)
                
                element = element.strip()
                
                if (extract_value in element) and (len(element.split(":")) >= 2):
                    temp_list.append(element.split(":")[1].strip())
                    break

                elif (extract_value in element) and (len(element.split(";")) >= 2):
                    temp_list.append(element.split(";")[1].strip())
                    break

                elif num==len(text)-1:
                    temp_list.append("None")
                    
        df_extract=pd.DataFrame(temp_list)
        df_extract.index = df.index
        df_extract.rename(columns={0:feature_name}, inplace=True)
        
        result_df=pd.concat([df, df_extract], axis=1)
        result_df=result_df[result_df["organism"]!="None"]
        
        return result_df
        
        
    def new_susceptibility_test(self, df):
        
    # Anti Extraction
        anti_re = re.compile("[\S\s]+(?=\s[ris+])")
        anti_list = []
        
        temp_result = (i for i in df["organ_result"])
        
        for _ in range(len(df)):
            
            temp_text = next(temp_result)
            
            for i in temp_text[1:]:
                
                i = i.strip('*')
                split_i = i.split()
                
                if 'esbl' in split_i:
                    
                    anti_name = 'esbl'
                    
                elif 'high' in split_i:
                    
                    anti_name = self.anti_check(i)
                    
                elif ("s" in split_i) or ("i" in split_i) or ("r" in split_i) :
                    
                    for split_i_index, split_i_element in enumerate(split_i):
                        
                        if ("s" == split_i_element) or ("i" == split_i_element) or ("r" == split_i_element) :
                            
                            sir_index = split_i_index
                            break
                            
                    anti_name = ' '.join(split_i[:sir_index])
                    anti_name = self.anti_check(anti_name).strip()
                    
                anti_list.append(anti_name)
                
        for anti_name in (list(set(anti_list))):
                df[anti_name] = None
                

    # Susceptibility Test
        
        temp_result = (i for i in df["organ_result"])
        
        for _ in range(len(df["organ_result"])):
            
            temp_text = next(temp_result)
            
            for i in temp_text[1:]:
                
                i = i.strip('*').strip()
                split_i = i.split()
                
                if 'esbl' in split_i:
                    
                    anti_name = 'esbl'
                    anti_value = split_i[1:]
                    anti_value = ' '.join(anti_value)
                    anti_value = re.sub(r'\([^)]*\)', '', anti_value)
                    df[anti_name].iat[_] = anti_value.split()
                    
                elif 'high' in split_i:
                    
                    anti_name = self.anti_check(i)
                    anti_value = i.replace(anti_name,'')
                    anti_value = re.sub(r'\([^)]*\)', '', anti_value) #?
                    df[anti_name].iat[_] = anti_value.split()
                    
                elif ("s" in split_i) or ("i" in split_i) or ("r" in split_i) :
                    
                    for split_i_index, split_i_element in enumerate(split_i):
                        
                        if ("s" == split_i_element) or ("i" == split_i_element) or ("r" == split_i_element) :
                            
                            sir_index = split_i_index
                            break
                            
                    anti_name = ' '.join(split_i[:sir_index])
                    anti_name = self.anti_check(anti_name).strip()
                    anti_value = ' '.join(split_i[sir_index:])
                    anti_value = anti_value.replace('. .',' 0.')
                    
                    if '* inh' in anti_value: # * inh 1.0 (mcg/ml)에서 감수성
                        inh_index = anti_value.find('* inh')
                        anti_value = anti_value[:inh_index]
                        
                    anti_value = re.sub(r'\([^)]*\)', '', anti_value).strip(')')
                    df[anti_name].iat[_] = anti_value.split()
        
        # Delete Antibiotic == ""
        if "" in list(df.columns):
            df = df.drop("",axis=1)
            
        # Antibiotic List
        anti_list=list(filter(lambda x : x != "",anti_list))
        anti_list=pd.Series(sorted(list(set(anti_list))), name='Anti List')
        anti_list.to_csv("utils/validation/anti_list.csv", index = False, header=True, encoding = "CP949")
        
        return df
        
        
    def organ_check(self, x):
        
        if "moraxella (b.) catarrhalis" in x:
            return x
            
        if "beta-haemolytic streptococcus" in x: # 2002
            return x
            
        if "α-hemolysis streptococci" in x:
            return x
            
        if "α-hemolysis streptococcus" in x: #1건존재
            return x
            
        if "alpha-hemolytic streptococcus" in x:
            return x
            
        if "non- typhi salmonella" in x:
            return x
            
        if "r -hemolysis streptococci" in x:
            return x
            
        if "alcaligenes species (faecalis)" in x:
            x = "alcaligenes faecalis"
            return x
            
        if "moraxella spp(osloensis)" in x:
            x = "moraxella osloensis"
            return x
            
        if "flavobacterium odoratum" in x:
            x = "myroides odoratus"
            return x
            
        if "flavbacterium odoratum" in x: #오타2건존재
            x = "myroides odoratus"
            return x
            
        if "cdc group ef-4" in x:
            x = "neisseria animaloris "
            return x


        else:
            
            for i in [" ss", " spp"]:
                ss_index = x.find(i)
                if ss_index != -1:
                    break
                    
            if ss_index != -1 and " " in x[:ss_index]:
                x = x[:ss_index]
                
            if "-" in x:
                slice_index = x.find("-")
                x = x[:slice_index]
                
            if "," in x:
                slice_index = x.find(",")
                x = x[:slice_index]
                
            if "(" in x:
                slice_index = x.find("(")
                x = x[:slice_index]
                
            if ")" in x:
                slice_index = x.find(")")
                x = x[:slice_index]
                
            if "." in x:
                slice_index = x.find(".")
                x = x[:slice_index]
                
            return x
            
            
    def anti_check(self, x):
        
        if "penicillin-g" in x:
            x = 'penicillin'
            return x
            
        if "oxacillin mic" in x:
            x = 'oxacillin'
            return x
            
        if "isoniazid" in x: #isoniazid 0.2mcg/ml     isoniazied 0.2    
            x = 'isoniazid'
            return x
            
        if "esbl" in x:
            x = 'esbl'
            return x
            
        if "beta  lactamase" in x:
            return x
            
        else:

            num = re.compile('[0-9]')
            num.findall(x)
            if len(num.findall(x)) > 0:
                slice_index = x.find(num.findall(x)[0])
                x = x[:slice_index].strip()

            if "syn" in x:
                slice_index = x.find("syn")
                x = x[:slice_index].strip()

            if "(" in x:
                slice_index = x.find("(")
                x = x[:slice_index]

            if "  " in x:
                slice_index = x.find("  ")
                x = x[:slice_index]

            if ":" in x:
                slice_index = x.find(":")
                x = x[:slice_index]

            if ";" in x:
                slice_index = x.find(";")
                x = x[:slice_index]

            if ">" in x:
                slice_index = x.find(">")
                x = x[:slice_index]

            if "<" in x:
                slice_index = x.find("<")
                x = x[:slice_index]        

            return x