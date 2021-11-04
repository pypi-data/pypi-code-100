import pandas as pd
import numpy as np
import os
import datetime
import time
import jaconv
import re
import dask
import dask.dataframe as dd
from dask import delayed
from dsdtools import build_hiveserver2_session

#lst_dir = os.listdir('/home/emeric.szaboky/workspace_shared/logistics_data/Building Type Data/')

### just some common function
class Utility():
    
    def normalize_jp_address(self, str_addr, flag=0):
        """
        normalize japanese address for building type detection and address match 
        @flag==1 is to normalize address for address match else just for building type
        """
        
        str_addr = jaconv.normalize(str_addr)
#         str_addr = str_addr.replace("(?<=[0-9])[－|ー](?=[0-9])","-") ##Harmonising the dashes that occur between two numbers
#         str_addr = str_addr.replace("(?<=[ァ-ヴ])-","ー") ##Harmonising the dashes that occur between two numbers
        str_addr = re.sub(r"(?<=[0-9])[－|ー](?=[0-9])", "-", str_addr)
        str_addr = re.sub(r"(?<=[ァ-ヴ])-", "ー", str_addr)
        str_addr = re.sub(r"\\.", "", str_addr)
#         str_addr = str_addr.replace("\\.","") ##Removing periods
        str_addr = str_addr.replace("?", "-") #?
#        str_addr = str_addr.replace("*", "-") 
        str_addr = str_addr.replace(",", "")
        str_addr = str_addr.replace(", ", "")
        if flag == 0:
            pattern0 = re.compile(r'(?<=[0-9])番地(?=[0-9])|(?<=[0-9])番地-(?=[0-9])|(?<=[0-9])番地の(?=[0-9])|(?<=[0-9])番(?=[0-9])|(?<=[0-9])番-(?=[0-9])')
            pattern1 = re.compile(r'(?<=[0-9])の(?=[0-9])')
            pattern2 = re.compile(r' -(?=[0-9])|(?<=[0-9])- ')
            pattern3 = re.compile(r'丁目 (?=[0-9])')
#            pattern4 = re.compile(r'(?<=[0-9])*(?=[0-9])')
            str_addr = re.sub(pattern1, r'-', str_addr)
            str_addr = re.sub(pattern0, r'-', str_addr)
            str_addr = re.sub(pattern2, r'-', str_addr)
            str_addr = re.sub(pattern3, r'丁目', str_addr)
#            str_addr = re.sub(pattern4, r'-', str_addr)

#         if flag == 0:
#             if re.search('[0-9]の[0-9]', str_addr): str_addr = str_addr.replace('の', '-')
#             elif re.search('[0-9]番地[0-9]', str_addr): str_addr = str_addr.replace('番地', '-')
#             elif re.search('[0-9]番地-[0-9]', str_addr): str_addr = str_addr.replace('番地-', '-')
#             elif re.search('[0-9]番地の[0-9]', str_addr): str_addr = str_addr.replace('番地の', '-')
#             elif re.search('[0-9]番[0-9]', str_addr): str_addr = str_addr.replace('番', '-')
#             elif re.search('[0-9]番-[0-9]', str_addr): str_addr = str_addr.replace('番-', '-')
#             elif re.search(' -[0-9] |', str_addr): 
#                 pattern = re.compile(r' -(?=[0-9])|(?<=[0-9])- ')
              
#                 str_addr = re.sub(pattern, r'-', str_addr)
        
#             elif re.search('丁目 [0-9]', str_addr): str_addr = str_addr.replace('丁目 ', '丁目')
#             else: pass
        else:
            str_addr = str_addr.replace("ー", "-")
            str_addr = str_addr.replace(" ", "")
            str_addr = str_addr.replace("ケ", "ヶ")
            str_addr = str_addr.replace("~", "-")
            str_addr = str_addr.replace("|", "-")
            str_addr = str_addr.replace("′", "")
            str_addr = str_addr.replace("'", "")
            str_addr = str_addr.replace("ッ", "ツ")
            str_addr = str_addr.replace("号室", "")
            str_addr = str_addr.replace("号", "")

        return str_addr
    
    
    
    def detect_building_type(self, address_norm):
        """
        normalize japanese address for building type detection and address match 
        @flag==1 is to normalize address for address match else just for building type
        """
        #print("read the business code")
        #colnames=['JIS_code', 'business_kana', 'business_kanji', 'prefecture', 'city', 'town_area_name', 'address', 'postal_code', 'old_postal_code', 'handling_bureau', 'receiver_type', 'multiple_numbers', 'correction_code']
        #business_zip = dd.read_csv('/home/emeric.szaboky/workspace_shared/logistics_data/Building Type Data/BUSINESS_ZIP.CSV', names=colnames, encoding='shift_jis_2004')
        #business_zip['postal_code'] = business_zip['postal_code'].apply(lambda x: '{0:0>7}'.format(x))
        #zip_code = business_zip["postal_code"].tolist()
        #print("begin to detect the building type:")
        #             if df_building["receiver_postal_code"] in zip_code:
        #                 df_building.at[i,'building_type_pred'] = 'Business'    
        if 'ミュージックハイツ1F' in address_norm:
            return 'Business'
        elif '(株)' in address_norm:
            return 'Business'
        elif '青果' in address_norm:
            return 'Business'
        elif '青果' in address_norm:
            return 'Business'
        elif 'エージェンシー' in address_norm:
            return'Business'
        elif '株式会社' in address_norm:
            return 'Business'
        elif '救急車隊' in address_norm:
            return 'Business'
        elif '衛生隊' in address_norm:
            return 'Business'
        elif "ヌーベルバーグ" in address_norm: 
            return 'Business'
        elif "BSLLSHZW" in address_norm:     
            return 'Business'
        elif "TWMNSSWM" in address_norm:     
            return 'Business'
        elif address_norm.endswith('内'):
            return 'Business'
        elif address_norm.endswith('隊'):
            return 'Business'
        elif address_norm.endswith('大学'):
            return 'Business'
        elif (re.search('ビル[1-9][0-9]{2,2}', address_norm)):
            return 'Unit'
        elif 'マルニヤビルディング' in address_norm:
            return 'Unit'
        elif 'ビル' in address_norm: 
            return 'Business'
        elif 'FLAT' in address_norm:
            return 'Unit'
        elif '号室' in address_norm:
            return 'Unit'

        # 2 misclassifications 
        elif '号' in address_norm:
            return 'Unit'

        # Unusual House Classifications based on standalone　1-4 digit number search - no other numbers
        # 丁 form added
        elif len(re.findall("[0-9]{1,4}", address_norm)) == 1 and not re.search('-[0-9]{1,4}', address_norm) and not re.search('[0-9]{1,4}-', address_norm) and not re.search('-[0-9]{1,4}-', address_norm) and not re.search('[0-9]{1,5}の', address_norm) and not re.search('の[0-9]{1,4}', address_norm) and not re.search('の[0-9]{1,4}の', address_norm) and not re.search('丁目[0-9]{1,4}', address_norm) and not re.search('丁[0-9]{1,4}', address_norm):        
            return 'House'

        # 3 misclassifications 
        # find addresses with what seems to be a "building name" (characters after main address portion x-x-x) 
        #elif re.search('([一-龠ぁ-ゔァ-ヴ ]{1,}[0-9]{1,4}-[0-9]{1,3}-[0-9]{1,3}[一-龠ぁ-ゔァ-ヴA-Za-z ]{1,})', address_norm):
        #    test_building_label.at[i,'BUILDING_LAB_PRED'] = 'Unit'

        # 2 misclassifications 
        # find trailing numbers after main address portion and building name 
        elif re.search('([一-龠ぁ-ゔァ-ヴ ]{1,}[0-9]{1,4}-[0-9]{1,3}-[0-9]{1,3}[一-龠ぁ-ゔァ-ヴA-Za-z ]{1,}.*[0-9]{1,4})', address_norm):
            return 'Unit'

        # 2 misclassifications 
        # find trailing numbers after main address portion and building name 
        # TRAILING UNIT SIMPLE FORM 
        # x-x form 
        elif re.search('([一-龠ぁ-ゔァ-ヴ ]{1,}[0-9]{1,4}-[0-9]{1,4}[一-龠ぁ-ゔァ-ヴA-Za-z ]{1,}.*[0-9]{1,4})', address_norm):
            return 'Unit'
        # x-x-x form 
        elif re.search('([一-龠ぁ-ゔァ-ヴ ]{1,}[0-9]{1,4}-[0-9]{1,4}-[0-9]{1,3}[一-龠ぁ-ゔァ-ヴA-Za-z ]{1,}.*[0-9]{1,4})', address_norm):
            return 'Unit'

        # 2 misclassifications 
        # find trailing numbers after main address portion and building name
        # TRAILING UNIT x-x form 
        # x-x form 
        elif re.search('([一-龠ぁ-ゔァ-ヴ ]{1,}[0-9]{1,4}-[0-9]{1,4}[一-龠ぁ-ゔァ-ヴA-Za-z ]{1,}.*[0-9]-[0-9]{1,4})', address_norm):
            return 'Unit'
        # x-x-x form 
        elif re.search('([一-龠ぁ-ゔァ-ヴ ]{1,}[0-9]{1,4}-[0-9]{1,4}-[0-9]{1,3}[一-龠ぁ-ゔァ-ヴA-Za-z ]{1,}.*[0-9]-[0-9]{1,4})', address_norm):
            return 'Unit'


        # Unit Classifications based on standalone 3 digit number search - is this line necessary? 
        # 丁 form added
        elif re.search('[1-9][0-9][0-9]{1,1}', address_norm) and not re.search('-[1-9][0-9][0-9]{1,1}', address_norm) and not re.search('[1-9][0-9][0-9]{1,1}-', address_norm) and not re.search('-[1-9][0-9][0-9]{1,1}-', address_norm) and not re.search('[1-9][0-9][0-9]{1,1}の', address_norm) and not re.search('の[1-9][0-9][0-9]{1,1}', address_norm) and not re.search('の[1-9][0-9][0-9]{1,1}の', address_norm) and not re.search('[1-9][0-9][0-9][0-9]-', address_norm) and not re.search('-[1-9][0-9][0-9][0-9]', address_norm) and not re.search('-[1-9][0-9][0-9][0-9]-', address_norm) and not re.search('[1-9][0-9][0-9][0-9]の', address_norm) and not re.search('の[1-9][0-9][0-9][0-9]', address_norm) and not re.search('の[1-9][0-9][0-9][0-9]の', address_norm) and not re.search('丁目[1-9][0-9][0-9]{1,1}', address_norm) and not re.search('丁目[1-9][0-9][0-9][0-9]', address_norm) and not re.search('丁[1-9][0-9][0-9]{1,1}', address_norm) and not re.search('丁[1-9][0-9][0-9][0-9]', address_norm): 
            return 'Unit'

        # Unit Classifications based on standalone 4 digit number search - necessary? 
        # 丁 form added
        elif re.search('[1-9][0-9]{3,3}', address_norm) and not re.search('-[1-9][0-9]{3,3}', address_norm) and not re.search('[1-9][0-9]{3,3}-', address_norm) and not re.search('-[1-9][0-9]{3,3}-', address_norm) and not re.search('[1-9][0-9]{3,3}の', address_norm) and not re.search('の[1-9][0-9]{3,3}', address_norm) and not re.search('の[1-9][0-9]{3,3}の', address_norm) and not re.search('丁目[1-9][0-9]{3,3}', address_norm) and not re.search('丁[1-9][0-9]{3,3}', address_norm): 
            return 'Unit'


        # Unit x{1,4}-x{1,4}-x{3,3} shape - must come before below "Regular House" logic because if not, it will be mislassified as house 
        # version with 丁目 AND NUMBER kanji     
        elif (re.search('一丁目[0-9]{1,4}-[0-9]{3,3}', address_norm) or re.search('二丁目[0-9]{1,4}-[0-9]{3,3}', address_norm) or re.search('三丁目[0-9]{1,4}-[0-9]{3,3}', address_norm) or re.search('四丁目[0-9]{1,4}-[0-9]{3,3}', address_norm) or re.search('五丁目[0-9]{1,4}-[0-9]{3,3}', address_norm) or re.search('六丁目[0-9]{0,4}-[0-9]{3,3}', address_norm) or re.search('七丁目[0-9]{1,4}-[0-9]{3,3}', address_norm) or re.search('八丁目[0-9]{1,4}-[0-9]{3,3}', address_norm) or re.search('九丁目[0-9]{1,4}-[0-9]{3,3}', address_norm) or re.search('十丁目[0-9]{1,4}-[0-9]{3,3}', address_norm)) and not re.search("丁目[0-9]{1,4}-[0-9]{3,3}-[0-9]{1,4}", address_norm):
            return 'Unit'
        # version with 丁 AND NUMBER kanji     
        elif (re.search('一丁[0-9]{1,4}-[0-9]{3,3}', address_norm) or re.search('二丁[0-9]{1,4}-[0-9]{3,3}', address_norm) or re.search('三丁[0-9]{1,4}-[0-9]{3,3}', address_norm) or re.search('四丁[0-9]{1,4}-[0-9]{3,3}', address_norm) or re.search('五丁[0-9]{1,4}-[0-9]{3,3}', address_norm) or re.search('六丁[0-9]{0,4}-[0-9]{3,3}', address_norm) or re.search('七丁[0-9]{1,4}-[0-9]{3,3}', address_norm) or re.search('八丁[0-9]{1,4}-[0-9]{3,3}', address_norm) or re.search('九丁[0-9]{1,4}-[0-9]{3,3}', address_norm) or re.search('十丁[0-9]{1,4}-[0-9]{3,3}', address_norm)) and not re.search("丁[0-9]{1,4}-[0-9]{3,3}-[0-9]{1,4}", address_norm):
            return 'Unit'
        ## version with 丁目 kanji
        elif re.search("[0-9]{1,4}丁目[0-9]{1,4}-[0-9]{3,3}", address_norm) and not re.search("[0-9]{1,4}丁目[0-9]{1,4}-[0-9]{3,3}-[0-9]{1,4}", address_norm):
            return 'Unit'
        ## version with 丁 kanji
        elif re.search("[0-9]{1,4}丁[0-9]{1,4}-[0-9]{3,3}", address_norm) and not re.search("[0-9]{1,4}丁[0-9]{1,4}-[0-9]{3,3}-[0-9]{1,4}", address_norm):
            return 'Unit'
        ## main - check if i should include xxxx unit 
        elif re.search("[0-9]{1,4}-[0-9]{1,4}-[0-9]{3,4}", address_norm) and not re.search("[0-9]{1,4}-[0-9]{1,4}-[0-9]{3,4}-[0-9]{1,4}", address_norm) and not re.search("[0-9]{1,4}-[0-9]{1,4}-[0-9]{1,4}-[0-9]{3,4}", address_norm) and not re.search("[0-9]{1,4}-[0-9]{1,4}-[0-9]{1,4}-[0-9]{3,4}-[0-9]{1,4}", address_norm):
            return 'Unit'


        # x-x form unit number -> unit
        #elif re.search('[0-9]{1,4}-[0-9]{1,4}', df_building['receiver_address_n']) and not re.search('-[0-9]{1,4}-[0-9]{1,4}-', df_building['receiver_address_n']) and re.search('[一-龠ぁ-ゔァ-ヴA-Za-z ][0-9]{1,4}[一-龠ぁ-ゔァ-ヴA-Za-z ]', df_building['receiver_address_n']):
         #   test_building_label.at[i,'BUILDING_LAB_PRED'] = 'Unit'
        #elif re.search('[0-9]{1,4}丁目[0-9]{1,4}', df_building['receiver_address_n']) and not re.search('-[0-9]{1,4}丁目[0-9]{1,4}-', df_building['receiver_address_n']) and re.search('[一-龠ぁ-ゔァ-ヴA-Za-z ][0-9]{1,4}[一-龠ぁ-ゔァ-ヴA-Za-z ]', df_building['receiver_address_n']):
         #   test_building_label.at[i,'BUILDING_LAB_PRED'] = 'Unit'

          #  and not re.search('[一-龠ぁ-ゔァ-ヴA-Za-z ][0-9]{1,4}(?![丁目])[一-龠ぁ-ゔァ-ヴA-Za-z ]', df_building['receiver_address_n'])


        # "Regular House"
        # label x-x, x-x-x, x-x-x-x addresses with no unit number as houses 
        # version with 丁目 AND NUMBER kanji 
        elif (re.search('一丁目[0-9]{1,4}', address_norm) or re.search('二丁目[0-9]{1,4}', address_norm) or re.search('三丁目[0-9]{1,4}', address_norm) or re.search('四丁目[0-9]{1,4}', address_norm) or re.search('五丁目[0-9]{1,4}', address_norm) or re.search('六丁目[0-9]{1,4}', address_norm) or re.search('七丁目[0-9]{1,4}', address_norm) or re.search('八丁目[0-9]{1,4}', address_norm) or re.search('九丁目[0-9]{1,4}', address_norm) or re.search('十丁目[0-9]{1,4}', address_norm)) and not re.search('丁目[0-9]{1,4}-[0-9]{1,4}-[0-9]{3,4}', address_norm) and not re.search('丁目[0-9]{1,4}-[0-9]{1,4}-[0-9]{1,4}-[0-9]{3,4}', address_norm) and not re.search('[一-龠ぁ-ゔァ-ヴA-Za-z ][0-9]{1,4}[一-龠ぁ-ゔァ-ヴA-Za-z ]', address_norm):
            return 'House'
        # version with 丁 AND NUMBER kanji 
        elif (re.search('一丁[0-9]{1,4}', address_norm) or re.search('二丁[0-9]{1,4}', address_norm) or re.search('三丁[0-9]{1,4}', address_norm) or re.search('四丁[0-9]{1,4}', address_norm) or re.search('五丁[0-9]{1,4}', address_norm) or re.search('六丁[0-9]{1,4}', address_norm) or re.search('七丁[0-9]{1,4}', address_norm) or re.search('八丁[0-9]{1,4}', address_norm) or re.search('九丁[0-9]{1,4}', address_norm) or re.search('十丁[0-9]{1,4}', address_norm)) and not re.search('丁[0-9]{1,4}-[0-9]{1,4}-[0-9]{3,4}', address_norm) and not re.search('丁[0-9]{1,4}-[0-9]{1,4}-[0-9]{1,4}-[0-9]{3,4}', address_norm) and not re.search('[一-龠ぁ-ゔァ-ヴA-Za-z ][0-9]{1,4}[一-龠ぁ-ゔァ-ヴA-Za-z ]', address_norm):
            return 'House'
        # version with 丁目 kanji 
        elif re.search('[0-9]{1,4}丁目[0-9]{1,4}', address_norm) and not re.search('[0-9]{1,4}丁目[0-9]{1,4}-[0-9]{1,4}-[0-9]{3,4}', address_norm) and not re.search('[0-9]{1,4}丁目[0-9]{1,4}-[0-9]{1,4}-[0-9]{1,4}-[0-9]{3,4}', address_norm) and not re.search('[一-龠ぁ-ゔァ-ヴA-Za-z ][0-9]{1,4}(?![丁目])[一-龠ぁ-ゔァ-ヴA-Za-z ]', address_norm):
            return 'House'
        # version with 丁 kanji 
        elif re.search('[0-9]{1,4}丁[0-9]{1,4}', address_norm) and not re.search('[0-9]{1,4}丁[0-9]{1,4}-[0-9]{1,4}-[0-9]{3,4}', address_norm) and not re.search('[0-9]{1,4}丁[0-9]{1,4}-[0-9]{1,4}-[0-9]{1,4}-[0-9]{3,4}', address_norm) and not re.search('[一-龠ぁ-ゔァ-ヴA-Za-z ][0-9]{1,4}(?![丁目])[一-龠ぁ-ゔァ-ヴA-Za-z ]', address_norm):
            return 'House'
        # fix for x-x case 
        elif re.search('[0-9]{1,4}-[0-9]{1,4}', address_norm) and not re.search('[0-9]{1,4}-[0-9]{1,4}-[0-9]{1,4}-[0-9]{3,4}', address_norm) and not re.search('[0-9]{1,4}-[0-9]{1,4}-[0-9]{1,4}-[0-9]{1,4}-[0-9]{3,4}', address_norm) and not re.search('[一-龠ぁ-ゔァ-ヴA-Za-z ][0-9]{1,4}[一-龠ぁ-ゔァ-ヴA-Za-z ]', address_norm):
            return 'House'


        # address format logic 
    #review

        # 4 parts 
        # clean 
        elif re.search('[1-9]-[1-9]-[1-9]-[1-9][0-9]{2,3}', address_norm):
            return 'Unit'
        # add logic for not 2
        elif re.search('[1-9]-[1-9]-[1-9]-[1-9]{1,2}', address_norm):
            return 'House'
        elif re.search('[1-9]丁目[1-9]-[1-9]-[1-9][0-9]{2,3}', address_norm):
            return 'Unit'
        elif re.search('[1-9]丁[1-9]-[1-9]-[1-9][0-9]{2,3}', address_norm):
            return 'Unit'
        elif re.search('[1-9]丁目[1-9]-[1-9]-[1-9]{1,2}', address_norm):
            return 'House'
        elif re.search('[1-9]丁[1-9]-[1-9]-[1-9]{1,2}', address_norm):
            return 'House'


        # clean 
        elif re.search('[1-9]-[1-9]-[1-9][0-9]-[1-9][0-9]{2,3}', address_norm):
            return 'Unit'
        elif re.search('[1-9]-[1-9]-[1-9][0-9]-[1-9]{1,2}', address_norm):
            return 'House'
        elif re.search('[1-9]丁目[1-9]-[1-9][0-9]-[1-9][0-9]{2,3}', address_norm):
            return 'Unit'
        elif re.search('[1-9]丁[1-9]-[1-9][0-9]-[1-9][0-9]{2,3}', address_norm):
            return 'Unit'
        elif re.search('[1-9]丁目[1-9]-[1-9][0-9]-[1-9]{1,2}', address_norm):
            return 'House'
        elif re.search('[1-9]丁[1-9]-[1-9][0-9]-[1-9]{1,2}', address_norm):
            return 'House'


        # clean 
        elif re.search('[1-9]-[1-9][0-9]-[1-9]-[1-9][0-9]{2,3}', address_norm):
            return 'Unit'
        elif re.search('[1-9]-[1-9][0-9]-[1-9]-[1-9]{1,2}', address_norm):
            return 'House'
        elif re.search('[1-9]丁目[1-9][0-9]-[1-9]-[1-9][0-9]{2,3}', address_norm):
            return 'Unit'
        elif re.search('[1-9]丁[1-9][0-9]-[1-9]-[1-9][0-9]{2,3}', address_norm):
            return'Unit'
        elif re.search('[1-9]丁目[1-9][0-9]-[1-9]-[1-9]{1,2}', address_norm):
            return 'House'
        elif re.search('[1-9]丁[1-9][0-9]-[1-9]-[1-9]{1,2}', address_norm):
            return 'House'


        # clean   
        elif re.search('[1-9]-[1-9][0-9]-[1-9][0-9]-[1-9][0-9]{2,3}', address_norm):
            return 'Unit'
        elif re.search('[1-9]-[1-9][0-9]-[1-9][0-9]-[1-9]{1,2}', address_norm):
            return'House'
        elif re.search('[1-9]丁目[1-9][0-9]-[1-9][0-9]-[1-9][0-9]{2,3}', address_norm):
            return 'Unit'
        elif re.search('[1-9]丁[1-9][0-9]-[1-9][0-9]-[1-9][0-9]{2,3}', address_norm):
            return 'Unit'
        elif re.search('[1-9]丁目[1-9][0-9]-[1-9][0-9]-[1-9]{1,2}', address_norm):
            return 'House'
        elif re.search('[1-9]丁[1-9][0-9]-[1-9][0-9]-[1-9]{1,2}', address_norm):
            return 'House'
                       

        # clear
        elif re.search('[1-9]-[0-9]{3,3}-[1-9]-[0-9]{3,3}', address_norm): 
            return 'Unit'
        elif re.search('[1-9]丁目[0-9]{3,3}-[1-9]-[0-9]{3,3}', address_norm): 
            return 'Unit'
        elif re.search('[1-9]丁[0-9]{3,3}-[1-9]-[0-9]{3,3}', address_norm): 
            return 'Unit'

        # 3 parts 
        elif re.search('[1-9]-[1-9]-[1-9]', address_norm) and not re.search('-[1-9]-[1-9]-[1-9]', address_norm) and not re.search('[1-9]-[1-9]-[1-9]-', address_norm) and not re.search('-[1-9]-[1-9]-[1-9]-', address_norm):
            return 'House'

        elif re.search('([一-龠ぁ-ゔァ-ヴ ]{1,}[0-9]{1,4}-[0-9]{1,3}-[0-9]{1,3}[一-龠ぁ-ゔァ-ヴA-Za-z ]{1,})', address_norm):
            return 'Business'

        else:
            return 'None'

        #return df_building
        
    def detect_building_type_revised(self, address_norm):
        """
        normalize japanese address for building type detection and address match 
        @flag==1 is to normalize address for address match else just for building type
        """
        #print("read the business code")
        #colnames=['JIS_code', 'business_kana', 'business_kanji', 'prefecture', 'city', 'town_area_name', 'address', 'postal_code', 'old_postal_code', 'handling_bureau', 'receiver_type', 'multiple_numbers', 'correction_code']
        #business_zip = dd.read_csv('/home/emeric.szaboky/workspace_shared/logistics_data/Building Type Data/BUSINESS_ZIP.CSV', names=colnames, encoding='shift_jis_2004')
        #business_zip['postal_code'] = business_zip['postal_code'].apply(lambda x: '{0:0>7}'.format(x))
        #zip_code = business_zip["postal_code"].tolist()
        #print("begin to detect the building type:")
        #             if df_building["receiver_postal_code"] in zip_code:
        #                 df_building.at[i,'building_type_pred'] = 'Business'    
        if 'ミュージックハイツ1F' in address_norm:
            return 'Business'
        elif '(株)' in address_norm:
            return 'Business'
        elif '青果' in address_norm:
            return 'Business'
        elif '青果' in address_norm:
            return 'Business'
        elif 'コーポレーション' in address_norm:
            return 'Business'
        elif 'エージェンシー' in address_norm:
            return'Business'
        elif '株式会社' in address_norm:
            return 'Business'
        elif '救急車隊' in address_norm:
            return 'Business'
        elif '衛生隊' in address_norm:
            return 'Business'
        elif '町店' in address_norm:
            return 'Business' 
        elif '店' in address_norm:
            return 'Business' 
        elif "ヌーベルバーグ" in address_norm: 
            return 'Business'
        elif "BSLLSHZW" in address_norm:     
            return 'Business'
        elif "TWMNSSWM" in address_norm:     
            return 'Business'
        elif address_norm.endswith('内'):
            return 'Business'
        elif address_norm.endswith('隊'):
            return 'Business'
        elif address_norm.endswith('大学'):
            return 'Business'
        elif (re.search('ビル[1-9][0-9]{2,2}', address_norm)):
            return 'Unit'
        elif 'マルニヤビルディング' in address_norm:
            return 'Unit'
        elif 'ビル' in address_norm: 
            return 'Business'
        elif 'FLAT' in address_norm:
            return 'Unit'
        elif '号室' in address_norm:
            return 'Unit'

        # 2 misclassifications 
        #elif '号' in address_norm:
         #   return 'Unit'

        # Unusual House Classifications based on standalone　1-4 digit number search - no other numbers
        # 丁 form added
        elif len(re.findall("[0-9]{1,4}", address_norm)) == 1 and not re.search('-[0-9]{1,4}', address_norm) and not re.search('[0-9]{1,4}-', address_norm) and not re.search('-[0-9]{1,4}-', address_norm) and not re.search('[0-9]{1,5}の', address_norm) and not re.search('の[0-9]{1,4}', address_norm) and not re.search('の[0-9]{1,4}の', address_norm) and not re.search('丁目[0-9]{1,4}', address_norm) and not re.search('丁[0-9]{1,4}', address_norm):        
            return 'House'

        # 3 misclassifications 
        # TESTING 
        # find addresses with what seems to be a "building name" (characters after main address portion x-x-x) 
        #elif re.search('([一-龠ぁ-ゔァ-ヴ ]{1,}[0-9]{1,4}-[0-9]{1,3}-[0-9]{1,3}[一-龠ぁ-ゔァ-ヴA-Za-z ]{1,})', address_norm) and not re.search('([一-龠ぁ-ゔァ-ヴ ]{1,}[0-9]{1,4}-[0-9]{1,3}-[0-9]{1,3}[一-龠ぁ-ゔァ-ヴA-Za-z ]{1,}.*[0-9]{1,4})', address_norm):
         #   return 'Business'

        # 2 misclassifications 
        # find trailing numbers after main address portion and building name 
        elif re.search('([一-龠ぁ-ゔァ-ヴ ]{1,}[0-9]{1,4}-[0-9]{1,3}-[0-9]{1,3}[一-龠ぁ-ゔァ-ヴA-Za-z ]{1,}.*[0-9]{1,4})', address_norm):
            return 'Unit'

        # 2 misclassifications 
        # find trailing numbers after main address portion and building name 
        # TRAILING UNIT SIMPLE FORM 
        # x-x form 
        elif re.search('([一-龠ぁ-ゔァ-ヴ ]{1,}[0-9]{1,4}-[0-9]{1,4}[一-龠ぁ-ゔァ-ヴA-Za-z ]{1,}.*[0-9]{1,4})', address_norm):
            return 'Unit'
        # x-x-x form 
        elif re.search('([一-龠ぁ-ゔァ-ヴ ]{1,}[0-9]{1,4}-[0-9]{1,4}-[0-9]{1,3}[一-龠ぁ-ゔァ-ヴA-Za-z ]{1,}.*[0-9]{1,4})', address_norm):
            return 'Unit'

        # 2 misclassifications 
        # find trailing numbers after main address portion and building name
        # TRAILING UNIT x-x form 
        # x-x form 
        elif re.search('([一-龠ぁ-ゔァ-ヴ ]{1,}[0-9]{1,4}-[0-9]{1,4}[一-龠ぁ-ゔァ-ヴA-Za-z ]{1,}.*[0-9]-[0-9]{1,4})', address_norm):
            return 'Unit'
        # x-x-x form 
        elif re.search('([一-龠ぁ-ゔァ-ヴ ]{1,}[0-9]{1,4}-[0-9]{1,4}-[0-9]{1,3}[一-龠ぁ-ゔァ-ヴA-Za-z ]{1,}.*[0-9]-[0-9]{1,4})', address_norm):
            return 'Unit'


        # Unit Classifications based on standalone 3 digit number search - is this line necessary? 
        # 丁 form added
        elif re.search('[1-9][0-9][0-9]{1,1}', address_norm) and not re.search('-[1-9][0-9][0-9]{1,1}', address_norm) and not re.search('[1-9][0-9][0-9]{1,1}-', address_norm) and not re.search('-[1-9][0-9][0-9]{1,1}-', address_norm) and not re.search('[1-9][0-9][0-9]{1,1}の', address_norm) and not re.search('の[1-9][0-9][0-9]{1,1}', address_norm) and not re.search('の[1-9][0-9][0-9]{1,1}の', address_norm) and not re.search('[1-9][0-9][0-9][0-9]-', address_norm) and not re.search('-[1-9][0-9][0-9][0-9]', address_norm) and not re.search('-[1-9][0-9][0-9][0-9]-', address_norm) and not re.search('[1-9][0-9][0-9][0-9]の', address_norm) and not re.search('の[1-9][0-9][0-9][0-9]', address_norm) and not re.search('の[1-9][0-9][0-9][0-9]の', address_norm) and not re.search('丁目[1-9][0-9][0-9]{1,1}', address_norm) and not re.search('丁目[1-9][0-9][0-9][0-9]', address_norm) and not re.search('丁[1-9][0-9][0-9]{1,1}', address_norm) and not re.search('丁[1-9][0-9][0-9][0-9]', address_norm): 
            return 'Unit'

        # Unit Classifications based on standalone 4 digit number search - necessary? 
        # 丁 form added
        elif re.search('[1-9][0-9]{3,3}', address_norm) and not re.search('-[1-9][0-9]{3,3}', address_norm) and not re.search('[1-9][0-9]{3,3}-', address_norm) and not re.search('-[1-9][0-9]{3,3}-', address_norm) and not re.search('[1-9][0-9]{3,3}の', address_norm) and not re.search('の[1-9][0-9]{3,3}', address_norm) and not re.search('の[1-9][0-9]{3,3}の', address_norm) and not re.search('丁目[1-9][0-9]{3,3}', address_norm) and not re.search('丁[1-9][0-9]{3,3}', address_norm): 
            return 'Unit'


        # Unit x{1,4}-x{1,4}-x{3,3} shape - must come before below "Regular House" logic because if not, it will be mislassified as house 
        # version with 丁目 AND NUMBER kanji     
        elif (re.search('一丁目[0-9]{1,4}-[0-9]{3,3}', address_norm) or re.search('二丁目[0-9]{1,4}-[0-9]{3,3}', address_norm) or re.search('三丁目[0-9]{1,4}-[0-9]{3,3}', address_norm) or re.search('四丁目[0-9]{1,4}-[0-9]{3,3}', address_norm) or re.search('五丁目[0-9]{1,4}-[0-9]{3,3}', address_norm) or re.search('六丁目[0-9]{0,4}-[0-9]{3,3}', address_norm) or re.search('七丁目[0-9]{1,4}-[0-9]{3,3}', address_norm) or re.search('八丁目[0-9]{1,4}-[0-9]{3,3}', address_norm) or re.search('九丁目[0-9]{1,4}-[0-9]{3,3}', address_norm) or re.search('十丁目[0-9]{1,4}-[0-9]{3,3}', address_norm)) and not re.search("丁目[0-9]{1,4}-[0-9]{3,3}-[0-9]{1,4}", address_norm):
            return 'Unit'
        # version with 丁 AND NUMBER kanji     
        elif (re.search('一丁[0-9]{1,4}-[0-9]{3,3}', address_norm) or re.search('二丁[0-9]{1,4}-[0-9]{3,3}', address_norm) or re.search('三丁[0-9]{1,4}-[0-9]{3,3}', address_norm) or re.search('四丁[0-9]{1,4}-[0-9]{3,3}', address_norm) or re.search('五丁[0-9]{1,4}-[0-9]{3,3}', address_norm) or re.search('六丁[0-9]{0,4}-[0-9]{3,3}', address_norm) or re.search('七丁[0-9]{1,4}-[0-9]{3,3}', address_norm) or re.search('八丁[0-9]{1,4}-[0-9]{3,3}', address_norm) or re.search('九丁[0-9]{1,4}-[0-9]{3,3}', address_norm) or re.search('十丁[0-9]{1,4}-[0-9]{3,3}', address_norm)) and not re.search("丁[0-9]{1,4}-[0-9]{3,3}-[0-9]{1,4}", address_norm):
            return 'Unit'
        ## version with 丁目 kanji
        elif re.search("[0-9]{1,4}丁目[0-9]{1,4}-[0-9]{3,3}", address_norm) and not re.search("[0-9]{1,4}丁目[0-9]{1,4}-[0-9]{3,3}-[0-9]{1,4}", address_norm):
            return 'Unit'
        ## version with 丁 kanji
        elif re.search("[0-9]{1,4}丁[0-9]{1,4}-[0-9]{3,3}", address_norm) and not re.search("[0-9]{1,4}丁[0-9]{1,4}-[0-9]{3,3}-[0-9]{1,4}", address_norm):
            return 'Unit'
        ## main - check if i should include xxxx unit 
        elif re.search("[0-9]{1,4}-[0-9]{1,4}-[0-9]{3,4}", address_norm) and not re.search("[0-9]{1,4}-[0-9]{1,4}-[0-9]{3,4}-[0-9]{1,4}", address_norm) and not re.search("[0-9]{1,4}-[0-9]{1,4}-[0-9]{1,4}-[0-9]{3,4}", address_norm) and not re.search("[0-9]{1,4}-[0-9]{1,4}-[0-9]{1,4}-[0-9]{3,4}-[0-9]{1,4}", address_norm):
            return 'Unit'


        # x-x form unit number -> unit
        #elif re.search('[0-9]{1,4}-[0-9]{1,4}', df_building['receiver_address_n']) and not re.search('-[0-9]{1,4}-[0-9]{1,4}-', df_building['receiver_address_n']) and re.search('[一-龠ぁ-ゔァ-ヴA-Za-z ][0-9]{1,4}[一-龠ぁ-ゔァ-ヴA-Za-z ]', df_building['receiver_address_n']):
         #   test_building_label.at[i,'BUILDING_LAB_PRED'] = 'Unit'
        #elif re.search('[0-9]{1,4}丁目[0-9]{1,4}', df_building['receiver_address_n']) and not re.search('-[0-9]{1,4}丁目[0-9]{1,4}-', df_building['receiver_address_n']) and re.search('[一-龠ぁ-ゔァ-ヴA-Za-z ][0-9]{1,4}[一-龠ぁ-ゔァ-ヴA-Za-z ]', df_building['receiver_address_n']):
         #   test_building_label.at[i,'BUILDING_LAB_PRED'] = 'Unit'

          #  and not re.search('[一-龠ぁ-ゔァ-ヴA-Za-z ][0-9]{1,4}(?![丁目])[一-龠ぁ-ゔァ-ヴA-Za-z ]', df_building['receiver_address_n'])


        # "Regular House"
        # label x-x, x-x-x, x-x-x-x addresses with no unit number as houses 
        # version with 丁目 AND NUMBER kanji 
        elif (re.search('一丁目[0-9]{1,4}', address_norm) or re.search('二丁目[0-9]{1,4}', address_norm) or re.search('三丁目[0-9]{1,4}', address_norm) or re.search('四丁目[0-9]{1,4}', address_norm) or re.search('五丁目[0-9]{1,4}', address_norm) or re.search('六丁目[0-9]{1,4}', address_norm) or re.search('七丁目[0-9]{1,4}', address_norm) or re.search('八丁目[0-9]{1,4}', address_norm) or re.search('九丁目[0-9]{1,4}', address_norm) or re.search('十丁目[0-9]{1,4}', address_norm)) and not re.search('丁目[0-9]{1,4}-[0-9]{1,4}-[0-9]{3,4}', address_norm) and not re.search('丁目[0-9]{1,4}-[0-9]{1,4}-[0-9]{1,4}-[0-9]{3,4}', address_norm) and not re.search('[一-龠ぁ-ゔァ-ヴA-Za-z ][0-9]{1,4}[一-龠ぁ-ゔァ-ヴA-Za-z ]', address_norm):
            return 'House'
        # version with 丁 AND NUMBER kanji 
        elif (re.search('一丁[0-9]{1,4}', address_norm) or re.search('二丁[0-9]{1,4}', address_norm) or re.search('三丁[0-9]{1,4}', address_norm) or re.search('四丁[0-9]{1,4}', address_norm) or re.search('五丁[0-9]{1,4}', address_norm) or re.search('六丁[0-9]{1,4}', address_norm) or re.search('七丁[0-9]{1,4}', address_norm) or re.search('八丁[0-9]{1,4}', address_norm) or re.search('九丁[0-9]{1,4}', address_norm) or re.search('十丁[0-9]{1,4}', address_norm)) and not re.search('丁[0-9]{1,4}-[0-9]{1,4}-[0-9]{3,4}', address_norm) and not re.search('丁[0-9]{1,4}-[0-9]{1,4}-[0-9]{1,4}-[0-9]{3,4}', address_norm) and not re.search('[一-龠ぁ-ゔァ-ヴA-Za-z ][0-9]{1,4}[一-龠ぁ-ゔァ-ヴA-Za-z ]', address_norm):
            return 'House'
        # version with 丁目 kanji 
        elif re.search('[0-9]{1,4}丁目[0-9]{1,4}', address_norm) and not re.search('[0-9]{1,4}丁目[0-9]{1,4}-[0-9]{1,4}-[0-9]{3,4}', address_norm) and not re.search('[0-9]{1,4}丁目[0-9]{1,4}-[0-9]{1,4}-[0-9]{1,4}-[0-9]{3,4}', address_norm) and not re.search('[一-龠ぁ-ゔァ-ヴA-Za-z ][0-9]{1,4}(?![丁目])[一-龠ぁ-ゔァ-ヴA-Za-z ]', address_norm):
            return 'House'
        # version with 丁 kanji 
        elif re.search('[0-9]{1,4}丁[0-9]{1,4}', address_norm) and not re.search('[0-9]{1,4}丁[0-9]{1,4}-[0-9]{1,4}-[0-9]{3,4}', address_norm) and not re.search('[0-9]{1,4}丁[0-9]{1,4}-[0-9]{1,4}-[0-9]{1,4}-[0-9]{3,4}', address_norm) and not re.search('[一-龠ぁ-ゔァ-ヴA-Za-z ][0-9]{1,4}(?![丁目])[一-龠ぁ-ゔァ-ヴA-Za-z ]', address_norm):
            return 'House'
        # fix for x-x case 
        elif re.search('[0-9]{1,4}-[0-9]{1,4}', address_norm) and not re.search('[0-9]{1,4}-[0-9]{1,4}-[0-9]{1,4}-[0-9]{3,4}', address_norm) and not re.search('[0-9]{1,4}-[0-9]{1,4}-[0-9]{1,4}-[0-9]{1,4}-[0-9]{3,4}', address_norm) and not re.search('[一-龠ぁ-ゔァ-ヴA-Za-z ][0-9]{1,4}[一-龠ぁ-ゔァ-ヴA-Za-z ]', address_norm):
            return 'House'


        # address format logic 
    #review

        # 4 parts 
        # clean 
        elif re.search('[1-9]-[1-9]-[1-9]-[1-9][0-9]{2,3}', address_norm):
            return 'Unit'
        # add logic for not 2
        elif re.search('[1-9]-[1-9]-[1-9]-[1-9]{1,2}', address_norm):
            return 'House'
        elif re.search('[1-9]丁目[1-9]-[1-9]-[1-9][0-9]{2,3}', address_norm):
            return 'Unit'
        elif re.search('[1-9]丁[1-9]-[1-9]-[1-9][0-9]{2,3}', address_norm):
            return 'Unit'
        elif re.search('[1-9]丁目[1-9]-[1-9]-[1-9]{1,2}', address_norm):
            return 'House'
        elif re.search('[1-9]丁[1-9]-[1-9]-[1-9]{1,2}', address_norm):
            return 'House'


        # clean 
        elif re.search('[1-9]-[1-9]-[1-9][0-9]-[1-9][0-9]{2,3}', address_norm):
            return 'Unit'
        elif re.search('[1-9]-[1-9]-[1-9][0-9]-[1-9]{1,2}', address_norm):
            return 'House'
        elif re.search('[1-9]丁目[1-9]-[1-9][0-9]-[1-9][0-9]{2,3}', address_norm):
            return 'Unit'
        elif re.search('[1-9]丁[1-9]-[1-9][0-9]-[1-9][0-9]{2,3}', address_norm):
            return 'Unit'
        elif re.search('[1-9]丁目[1-9]-[1-9][0-9]-[1-9]{1,2}', address_norm):
            return 'House'
        elif re.search('[1-9]丁[1-9]-[1-9][0-9]-[1-9]{1,2}', address_norm):
            return 'House'


        # clean 
        elif re.search('[1-9]-[1-9][0-9]-[1-9]-[1-9][0-9]{2,3}', address_norm):
            return 'Unit'
        elif re.search('[1-9]-[1-9][0-9]-[1-9]-[1-9]{1,2}', address_norm):
            return 'House'
        elif re.search('[1-9]丁目[1-9][0-9]-[1-9]-[1-9][0-9]{2,3}', address_norm):
            return 'Unit'
        elif re.search('[1-9]丁[1-9][0-9]-[1-9]-[1-9][0-9]{2,3}', address_norm):
            return'Unit'
        elif re.search('[1-9]丁目[1-9][0-9]-[1-9]-[1-9]{1,2}', address_norm):
            return 'House'
        elif re.search('[1-9]丁[1-9][0-9]-[1-9]-[1-9]{1,2}', address_norm):
            return 'House'


        # clean   
        elif re.search('[1-9]-[1-9][0-9]-[1-9][0-9]-[1-9][0-9]{2,3}', address_norm):
            return 'Unit'
        elif re.search('[1-9]-[1-9][0-9]-[1-9][0-9]-[1-9]{1,2}', address_norm):
            return'House'
        elif re.search('[1-9]丁目[1-9][0-9]-[1-9][0-9]-[1-9][0-9]{2,3}', address_norm):
            return 'Unit'
        elif re.search('[1-9]丁[1-9][0-9]-[1-9][0-9]-[1-9][0-9]{2,3}', address_norm):
            return 'Unit'
        elif re.search('[1-9]丁目[1-9][0-9]-[1-9][0-9]-[1-9]{1,2}', address_norm):
            return 'House'
        elif re.search('[1-9]丁[1-9][0-9]-[1-9][0-9]-[1-9]{1,2}', address_norm):
            return 'House'
                       

        # clear
        elif re.search('[1-9]-[0-9]{3,3}-[1-9]-[0-9]{3,3}', address_norm): 
            return 'Unit'
        elif re.search('[1-9]丁目[0-9]{3,3}-[1-9]-[0-9]{3,3}', address_norm): 
            return 'Unit'
        elif re.search('[1-9]丁[0-9]{3,3}-[1-9]-[0-9]{3,3}', address_norm): 
            return 'Unit'

        # 3 parts 
        elif re.search('[1-9]-[1-9]-[1-9]', address_norm) and not re.search('-[1-9]-[1-9]-[1-9]', address_norm) and not re.search('[1-9]-[1-9]-[1-9]-', address_norm) and not re.search('-[1-9]-[1-9]-[1-9]-', address_norm):
            return 'House'

        elif re.search('([一-龠ぁ-ゔァ-ヴ ]{1,}[0-9]{1,4}-[0-9]{1,3}-[0-9]{1,3}[一-龠ぁ-ゔァ-ヴA-Za-z ]{1,})', address_norm):
            return 'Business'

        else:
            return 'None'        

            
    def dask_to_pandas(self, table):
        n = table.npartitions
        lst_all = []
        s = 0
        for i in range(n):
            #print(i)
            df = table.get_partition(i)
            df_p = df.compute()
        
            #s = s+len(df_p)
            #print(len(df_p), s)
            lst_all.append(df_p)
        
        df_final = pd.concat(lst_all).reset_index(drop=True)
    
        return df_final
            
            
    def preprocess_order_no(self, lst_o):
    # preprocessing order no of logistics data
        lst_order_n = []
        for d in lst_o:
            if type(d) is not str:
                lst_order_n.append(d)
            elif d.endswith("-bk-1"):
                lst_order_n.append(d[:-5])
            elif d.endswith("-fk-1"):
                lst_order_n.append(d[:-5])
            elif d.endswith("-001"):
                lst_order_n.append(d[:-4])
            elif d.endswith("-1"):
                lst_order_n.append(d[:-2])
            else:
                lst_order_n.append(d)
                
        return lst_order_n
    
    def get_order_no(self, date_str):
    # get rakuten order no
        data_str = "../../logistics_data/data/"
        lst_dir = os.listdir(data_str)
        lst_dir_s = [s for s in lst_dir if s.startswith(date_str)]
        lst_dir_s.sort()
        lst_df = []
        for d_s in lst_dir_s:
            df = pd.read_csv("{d_r}/{d}/TMS.ALLOCATION_REQUEST_DETAILS_VW_out.csv".format(d_r=data_str,d=d_s))
            lst_df.append(df)
        df_all = pd.concat(lst_df).reset_index(drop=True)
        lst_order = list((df_all.RAKUTEN_ORDER_NO.unique()))
        lst_order_rakuten = self.preprocess_order_no(lst_order)

        return lst_order_rakuten
    
#     def read_logistics_data():
        
    def execute_sql(self, sql_str, flag):
    # excute sql 1 is return query result, other is just e
        h = build_hiveserver2_session()
        h.execute(sql_str)
        if flag ==1:
            df_h = h.as_pandas()
            print("get a query result and returen dataframe")
            return df_h 
        else:
            print("complete sql executing")
    
    def create_order_no_table(self, table_str):
        sql_drop = "DROP TABLE {}".format(table_str)
        self.execute_sql(sql_drop, 0)
        sql="""
    CREATE TABLE IF NOT EXISTS {ts}
    (
    order_no STRING
    )
    ROW FORMAT DELIMITED
    FIELDS TERMINATED BY ','
    LINES TERMINATED BY '\n'
    STORED AS TEXTFILE
    LOCATION '/tmp/{ts}'
    """.format(ts=table_str)    
        self.execute_sql(sql, 0)
        
        print("complete table creating")
    
    def upload_file_hive(self, table_str, file_str):
        # Upload file
        from dsdtools import build_hdfs_session
        hdfs = build_hdfs_session()
        hdfs.makedirs("/tmp/{}".format(table_str))
        #hdfs.delete("/tmp/{}/{}.csv".format(table_str,file_str), recursive=True)
        hdfs.upload("/tmp/{}".format(table_str), "{}.csv".format(file_str))
        
        print("complete data uploading to hive table")
        
    def create_easy_order(self, table_str, file_str):
        ### create easy_id and rakuten_order_no table
        self.upload_file_hive(table_str, file_str)
        self.create_order_no_table(table_str)
#         easy_order_match = """
#             create table if not exists tianke01.logistics_users as 
#             select distinct rbd.easy_id, o_nos.order_no, rbd.reg_datetime 
#             from {} o_nos
#             left outer join 
#             rdsp_production_production_ex_odin_mart_v2.vw_red_basket_detail_tbl_current rbd 
#             on o_nos.order_no = rbd.order_no where reg_datetime >= '2020-08-15 00:00:00' 
#             and reg_datetime <= '2020-10-15 00:00:00' and cancel_datetime is null and easy_id is not null and easy_id > 0 """.format(table_str)
#         sql_drop = "DROP TABLE logistics_users2".format(table_str)
        sql_drop = "DROP TABLE tianke01.logistics_users"
        self.execute_sql(sql_drop, 0)
        print("begin to match easy_id and order_no in ichiba data")
        easy_order_match2 = """
            create table if not exists tianke01.logistics_users as 
            select distinct rbd.easy_id, rbd.order_no, rbd.reg_datetime 
            from rdsp_production_production_ex_odin_mart_v2.vw_red_basket_detail_tbl_current rbd 
            where rbd.reg_datetime >= '2020-05-01 00:00:00' and rbd.reg_datetime <= '2020-06-02 00:00:00' and rbd.cancel_datetime is null and rbd.easy_id is not null and easy_id > 0 and rbd.order_no in (select order_no from {})""".format(table_str) 
        self.execute_sql(easy_order_match2, 0)
        

    





