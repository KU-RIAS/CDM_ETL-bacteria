# -*- coding: utf-8 -*-

"""

@ author: Taehyeong Kim, Minji Kang, Fusion Data Analytics and Artificial Intelligence Lab

"""

import pandas as pd
from collections import Counter
from collections import OrderedDict
# import tqdm

class ResistanceLabel:
    
    def __init__(self):
        print("--- resistance label ---")
        
        
    def resistance_label(self, df):

        resistance_table = pd.read_csv("utils/resistance_table.csv")

        df["resistance_label"] = df["organism"]

        for i in range(len(resistance_table)):

            exist_list =[j for j in resistance_table['anti'][i].lower().split(',') if j in df.columns]

            if exist_list != []:

                sel_df = df[exist_list]

                for feature in exist_list:

                    sel_df[feature] = sel_df[feature].apply(lambda d: d if isinstance(d, list) else [])

                sel_df['check'] = sel_df.sum(axis = 1).apply(lambda x : 1 if "r" in x or "i" in x else 0)

                table_organ = resistance_table['organism'][i].strip().lower()


                for k in range(len(sel_df)):

                    if (sel_df["check"].iat[k]) == 1:

                        if table_organ in df["organism"].iat[k]:
                            df["resistance_label"].iat[k] +=  "\n" + resistance_table['resistant_bacteria'][i]

        df = self.exception_pan(df)
        df = self.exception_20(df)
        df = self.exception_28(df)

        # check_mdr

        for q in range(len(df["resistance_label"])):
            df["resistance_label"].iat[q]=df["resistance_label"].iat[q].split("\n")

        check_mdr=list(set(resistance_table[resistance_table["mdr"]!="none"]["resistant_bacteria"]))
        check_sdr=list(set(resistance_table[resistance_table["mdr"]=="none"]["resistant_bacteria"]))

        for b in range(len(df["resistance_label"])):

            label_list = df['resistance_label'].tolist()
            count_list=Counter(label_list[b])

            check_label=[]

            if len(df["resistance_label"].iat[b]) > 1:

                for m in check_mdr:

                    if count_list[m]>=3:

                        if "multidrug resistant methicillin resistant staphylococcus" in m:
                            m = m[:41]

                        else:
                            name_index = m.find("resistant") + 9
                            m = m[:name_index]

                        check_label.append(m + " " + df["organism"].iat[b])

                for s in check_sdr:

                    if count_list[s]>=1:

                        if s == "pan drug resistant bacteria":
                            s = "pan drug resistant"

                        name_index = s.find("resistant") + 9
                        s = s[:name_index]

                        check_label.append(s + " " + df["organism"].iat[b])

                if len(check_label)>=1:
                    check_label=self.exception_48_49(check_label)
                    df["resistance_label"].iat[b] = check_label

                else:
                    check_label = df["organism"].iat[b]
                    df["resistance_label"].iat[b] = [check_label]


        # exception_20,28 organism add
        for m in range(len(df["resistance_label"])):
            if "carbapenem resistant bacteria" in df["resistance_label"].iloc[m]:
                df["resistance_label"].iloc[m].append("carbapenem resistant " + df["organism"].iloc[m])
                df["resistance_label"].iloc[m].remove("carbapenem resistant bacteria")
                df["resistance_label"].iloc[m] = list(set(df["resistance_label"].iloc[m]))
            else:
                pass

        for m in range(len(df["resistance_label"])):
            if "fluoroquinolone resistant bacteria" in df["resistance_label"].iloc[m]:
                df["resistance_label"].iloc[m].append("fluoroquinolone resistant " + df["organism"].iloc[m])
                df["resistance_label"].iloc[m].remove("fluoroquinolone resistant bacteria")
                df["resistance_label"].iloc[m] = list(set(df["resistance_label"].iloc[m]))
            else:
                pass
            
        df=self.hierarchy_key(df)
            
        return df
        
        
    def exception_pan(self, df): # pan drug

        exist_list = pd.read_csv("utils/validation/anti_list.csv", encoding='CP949')
        exist_list = exist_list["Anti List"]

        sel_df = df[exist_list]

        for feature in exist_list:

            sel_df[feature] = sel_df[feature].apply(lambda d: d if isinstance(d, list) else [])

        set_list = list(sel_df.sum(axis = 1))

        for i in range(len(set_list)):
            if "s" not in set_list[i]:
                if (set_list[i].count('r') + set_list[i].count('i')) >=6:
                    df["resistance_label"].iat[i] +=  "\n" + "pan drug resistant bacteria"

        return df
        
        
    def exception_20(self, df):

        exist_list_set = ['ertapenem','imipenem','meropenem','doripenem']
        exist_list = []

        for i in range(len(exist_list_set)):
            if exist_list_set[i] in df.columns:
                exist_list.append(exist_list_set[i])

        if not exist_list:
            return df

        sel_df = df[exist_list]

        for feature in exist_list:

            sel_df[feature] = sel_df[feature].apply(lambda d: d if isinstance(d, list) else [])

        sel_df['check'] = sel_df.sum(axis = 1).apply(lambda x : 1 if "r" in x or "i" in x else 0)

        for k in range(len(sel_df)):

            if (sel_df["check"].iat[k]) == 1:
                df["resistance_label"].iat[k] +=  "\n" + "carbapenem resistant"
            else:
                pass

        return df
        
        
    def exception_28(self, df):

        exist_list_set = ['moxifloxacin','ciprofloxacin','levofloxacin']
        exist_list = []

        for i in range(len(exist_list_set)):
            if exist_list_set[i] in df.columns:
                exist_list.append(exist_list_set[i])

        if not exist_list:
            return df

        sel_df = df[exist_list]

        for feature in exist_list:

            sel_df[feature] = sel_df[feature].apply(lambda d: d if isinstance(d, list) else [])

        sel_df['check'] = sel_df.sum(axis = 1).apply(lambda x : 1 if "r" in x or "i" in x else 0)

        for k in range(len(sel_df)):

            if (sel_df["check"].iat[k]) == 1:
                df["resistance_label"].iat[k] +=  "\n" + "fluoroquinolone resistant"
            else:
                pass

        return df
        
        
    def exception_48_49(self, check_label):

        # 48 & 49
        if "methicillin resistant staphylococcus" not in check_label:

            if "multidrug resistant methicillin resistant staphylococcus" in check_label:
                check_label.remove("multidrug resistant methicillin resistant staphylococcus")
                check_label.append("staphylococcus aureus")

            else:
                return check_label

        elif "methicillin resistant staphylococcus aureus" in check_label:
            return check_label

        return check_label
    
    def hierarchy_key(self, df):
    
        key_list=['pan','vancomycin','glycopeptide','multidrug','carbapenem','fluoroquinolone','tetracycline','penicillin','methicillin']

        df["hierarchy_key"] = df["resistance_label"]

        hi_result = (i for i in df["hierarchy_key"])

        for n in range(len(df["hierarchy_key"])):

            save=[]

            label=next(hi_result)

            label_element = (i for i in label)

            for j in range(len(label)):

                element = next(label_element)

                key_element = (i for i in key_list)

                for i in range (len(key_list)):

                    key = next(key_element)

                    if key in element:

                        save.append(element)

                        hisave=list(OrderedDict.fromkeys(save))

                        df["hierarchy_key"].iat[n] = hisave

        for i in range(len (max (df['hierarchy_key'], key = len))):
            df["Key"+str(i+1)]=None

        for i in range(len(df['hierarchy_key'])):
            for j in range(len(df['hierarchy_key'].iat[i])):
                df["Key"+str(j+1)].iat[i]=df['hierarchy_key'].iat[i][j]

        return df