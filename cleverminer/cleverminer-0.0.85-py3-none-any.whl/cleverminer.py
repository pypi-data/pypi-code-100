import time #line:1
import pandas as pd #line:3
class cleverminer :#line:5
    version_string ="0.0.85"#line:7
    def __init__ (O000OO0OOO000OO00 ,**OO0000000OOOO0OO0 ):#line:9
        O000OO0OOO000OO00 ._print_disclaimer ()#line:10
        O000OO0OOO000OO00 .stats ={'total_cnt':0 ,'total_valid':0 ,'control_number':0 ,'start_prep_time':time .time (),'end_prep_time':time .time (),'start_proc_time':time .time (),'end_proc_time':time .time ()}#line:18
        O000OO0OOO000OO00 ._init_data ()#line:19
        O000OO0OOO000OO00 ._init_task ()#line:20
        if len (OO0000000OOOO0OO0 )>0 :#line:21
            O000OO0OOO000OO00 .kwargs =OO0000000OOOO0OO0 #line:22
            O000OO0OOO000OO00 ._calc_all (**OO0000000OOOO0OO0 )#line:23
    def _init_data (OO0OO0000OO000O00 ):#line:25
        OO0OO0000OO000O00 .data ={}#line:27
        OO0OO0000OO000O00 .data ["varname"]=[]#line:28
        OO0OO0000OO000O00 .data ["catnames"]=[]#line:29
        OO0OO0000OO000O00 .data ["vtypes"]=[]#line:30
        OO0OO0000OO000O00 .data ["dm"]=[]#line:31
        OO0OO0000OO000O00 .data ["rows_count"]=int (0 )#line:32
        OO0OO0000OO000O00 .data ["data_prepared"]=0 #line:33
    def _init_task (OOO00OOO0O000OO0O ):#line:35
        OOO00OOO0O000OO0O .cedent ={'cedent_type':'none','defi':{},'num_cedent':0 ,'trace_cedent':[],'traces':[],'generated_string':'','filter_value':int (0 )}#line:44
        OOO00OOO0O000OO0O .task_actinfo ={'proc':'','cedents_to_do':[],'cedents':[]}#line:48
        OOO00OOO0O000OO0O .hypolist =[]#line:49
        OOO00OOO0O000OO0O .stats ['total_cnt']=0 #line:51
        OOO00OOO0O000OO0O .stats ['total_valid']=0 #line:52
        OOO00OOO0O000OO0O .stats ['control_number']=0 #line:53
        OOO00OOO0O000OO0O .result ={}#line:54
    def _get_ver (OOO0O0O000OO0000O ):#line:56
        return OOO0O0O000OO0000O .version_string #line:57
    def _print_disclaimer (O00O0000OOO0000O0 ):#line:59
        print ("***********************************************************************************************************************************************************************")#line:60
        print ("Cleverminer version ",O00O0000OOO0000O0 ._get_ver ())#line:61
        print ("IMPORTANT NOTE: this is preliminary development version of CleverMiner procedure. This procedure is under intensive development and early released for educational use,")#line:62
        print ("    so there is ABSOLUTELY no guarantee of results, possible gaps in functionality and no guarantee of keeping syntax and parameters as in current version.")#line:63
        print ("    (That means we need to tidy up and make proper design, input validation, documentation and instrumentation before launch)")#line:64
        print ("This version is for personal and educational use only.")#line:65
        print ("***********************************************************************************************************************************************************************")#line:66
    def _prep_data (O0OO0O0000000O000 ,O00O0OOOO0O000OO0 ):#line:68
        print ("Starting data preparation ...")#line:69
        O0OO0O0000000O000 ._init_data ()#line:70
        O0OO0O0000000O000 .stats ['start_prep_time']=time .time ()#line:71
        O0OO0O0000000O000 .data ["rows_count"]=O00O0OOOO0O000OO0 .shape [0 ]#line:72
        for O0OO0000O000O00OO in O00O0OOOO0O000OO0 .select_dtypes (exclude =['category']).columns :#line:73
            O00O0OOOO0O000OO0 [O0OO0000O000O00OO ]=O00O0OOOO0O000OO0 [O0OO0000O000O00OO ].apply (str )#line:74
        O000OO0O00OO0O0O0 =pd .DataFrame .from_records ([(O0OOOOOO0O0O0O0O0 ,O00O0OOOO0O000OO0 [O0OOOOOO0O0O0O0O0 ].nunique ())for O0OOOOOO0O0O0O0O0 in O00O0OOOO0O000OO0 .columns ],columns =['Column_Name','Num_Unique']).sort_values (by =['Num_Unique'])#line:76
        print ("Unique value counts are:")#line:77
        print (O000OO0O00OO0O0O0 )#line:78
        for O0OO0000O000O00OO in O00O0OOOO0O000OO0 .columns :#line:79
            if O00O0OOOO0O000OO0 [O0OO0000O000O00OO ].nunique ()<100 :#line:80
                O00O0OOOO0O000OO0 [O0OO0000O000O00OO ]=O00O0OOOO0O000OO0 [O0OO0000O000O00OO ].astype ('category')#line:81
            else :#line:82
                print (f"WARNING: attribute {O0OO0000O000O00OO} has more than 100 values, will be ignored.")#line:83
                del O00O0OOOO0O000OO0 [O0OO0000O000O00OO ]#line:84
        print ("Encoding columns into bit-form...")#line:85
        O000000OOO0OO0O0O =0 #line:86
        O0O0OOOOO000O000O =0 #line:87
        for OO0OO00OO0O0O0OO0 in O00O0OOOO0O000OO0 :#line:88
            print ('Column: '+OO0OO00OO0O0O0OO0 )#line:90
            O0OO0O0000000O000 .data ["varname"].append (OO0OO00OO0O0O0OO0 )#line:91
            OO0O0O0O00OO0OOOO =pd .get_dummies (O00O0OOOO0O000OO0 [OO0OO00OO0O0O0OO0 ])#line:92
            OOOOOO00OOOO0O0O0 =0 #line:93
            if (O00O0OOOO0O000OO0 .dtypes [OO0OO00OO0O0O0OO0 ].name =='category'):#line:94
                OOOOOO00OOOO0O0O0 =1 #line:95
            O0OO0O0000000O000 .data ["vtypes"].append (OOOOOO00OOOO0O0O0 )#line:96
            OO0O0O0OO0OOOOO0O =0 #line:99
            O0O0OOOO0O00O0000 =[]#line:100
            OOO0O0OO0OOO00O00 =[]#line:101
            for OOOOOOOO00O00OO0O in OO0O0O0O00OO0OOOO :#line:103
                print ('....category : '+str (OOOOOOOO00O00OO0O )+" @ "+str (time .time ()))#line:105
                O0O0OOOO0O00O0000 .append (OOOOOOOO00O00OO0O )#line:106
                O0OO00OO000OO0OOO =int (0 )#line:107
                OO0000000000OOOO0 =OO0O0O0O00OO0OOOO [OOOOOOOO00O00OO0O ].values #line:108
                for OOO000OOO000O0O00 in range (O0OO0O0000000O000 .data ["rows_count"]):#line:110
                    if OO0000000000OOOO0 [OOO000OOO000O0O00 ]>0 :#line:111
                        O0OO00OO000OO0OOO +=1 <<OOO000OOO000O0O00 #line:112
                OOO0O0OO0OOO00O00 .append (O0OO00OO000OO0OOO )#line:113
                OO0O0O0OO0OOOOO0O +=1 #line:123
                O0O0OOOOO000O000O +=1 #line:124
            O0OO0O0000000O000 .data ["catnames"].append (O0O0OOOO0O00O0000 )#line:126
            O0OO0O0000000O000 .data ["dm"].append (OOO0O0OO0OOO00O00 )#line:127
        print ("Encoding columns into bit-form...done")#line:129
        print ("Encoding columns into bit-form...done")#line:130
        print (f"List of attributes for analysis is: {O0OO0O0000000O000.data['varname']}")#line:131
        print (f"List of category names for individual attributes is : {O0OO0O0000000O000.data['catnames']}")#line:132
        print (f"List of vtypes is (all should be 1) : {O0OO0O0000000O000.data['vtypes']}")#line:133
        O0OO0O0000000O000 .data ["data_prepared"]=1 #line:135
        print ("Data preparation finished ...")#line:136
        print ('Number of variables : '+str (len (O0OO0O0000000O000 .data ["dm"])))#line:137
        print ('Total number of categories in all variables : '+str (O0O0OOOOO000O000O ))#line:138
        O0OO0O0000000O000 .stats ['end_prep_time']=time .time ()#line:139
        print ('Time needed for data preparation : ',str (O0OO0O0000000O000 .stats ['end_prep_time']-O0OO0O0000000O000 .stats ['start_prep_time']))#line:140
    def bitcount (OOOO0O0OO00O00OO0 ,OOOO00OOOO00O0OO0 ):#line:143
        O000OOOOOOO00O0OO =0 #line:144
        while OOOO00OOOO00O0OO0 >0 :#line:145
            if (OOOO00OOOO00O0OO0 &1 ==1 ):O000OOOOOOO00O0OO +=1 #line:146
            OOOO00OOOO00O0OO0 >>=1 #line:147
        return O000OOOOOOO00O0OO #line:148
    def _verifyCF (OO000OOOO00O0O0OO ,_OO0000OOO0O0O0OOO ):#line:151
        OOOO0OO0O0O000O0O =bin (_OO0000OOO0O0O0OOO ).count ("1")#line:152
        O00OOO0O00O00000O =[]#line:153
        O000O000O00OO000O =[]#line:154
        O0OO0OO0OO0O0O0OO =0 #line:155
        O0O000O0O0OO0OOOO =0 #line:156
        O0OO00O00OO0O0O0O =0 #line:157
        OOOO0O000O0OOO0OO =0 #line:158
        O0OOOO0O00O0OOO0O =0 #line:159
        OO0O0OOO00O0O0O0O =0 #line:160
        OOOO0O0OOO00O0O00 =0 #line:161
        OO0O00OOOOO0OO0OO =0 #line:162
        O0OO0000000OO0OOO =0 #line:163
        OO0O0OO00O00OO0O0 =OO000OOOO00O0O0OO .data ["dm"][OO000OOOO00O0O0OO .data ["varname"].index (OO000OOOO00O0O0OO .kwargs .get ('target'))]#line:164
        for OOO00O0OOOO00000O in range (len (OO0O0OO00O00OO0O0 )):#line:165
            O0O000O0O0OO0OOOO =O0OO0OO0OO0O0O0OO #line:166
            O0OO0OO0OO0O0O0OO =bin (_OO0000OOO0O0O0OOO &OO0O0OO00O00OO0O0 [OOO00O0OOOO00000O ]).count ("1")#line:167
            O00OOO0O00O00000O .append (O0OO0OO0OO0O0O0OO )#line:168
            if OOO00O0OOOO00000O >0 :#line:169
                if (O0OO0OO0OO0O0O0OO >O0O000O0O0OO0OOOO ):#line:170
                    if (O0OO00O00OO0O0O0O ==1 ):#line:171
                        OO0O00OOOOO0OO0OO +=1 #line:172
                    else :#line:173
                        OO0O00OOOOO0OO0OO =1 #line:174
                    if OO0O00OOOOO0OO0OO >OOOO0O000O0OOO0OO :#line:175
                        OOOO0O000O0OOO0OO =OO0O00OOOOO0OO0OO #line:176
                    O0OO00O00OO0O0O0O =1 #line:177
                    OO0O0OOO00O0O0O0O +=1 #line:178
                if (O0OO0OO0OO0O0O0OO <O0O000O0O0OO0OOOO ):#line:179
                    if (O0OO00O00OO0O0O0O ==-1 ):#line:180
                        O0OO0000000OO0OOO +=1 #line:181
                    else :#line:182
                        O0OO0000000OO0OOO =1 #line:183
                    if O0OO0000000OO0OOO >O0OOOO0O00O0OOO0O :#line:184
                        O0OOOO0O00O0OOO0O =O0OO0000000OO0OOO #line:185
                    O0OO00O00OO0O0O0O =-1 #line:186
                    OOOO0O0OOO00O0O00 +=1 #line:187
                if (O0OO0OO0OO0O0O0OO ==O0O000O0O0OO0OOOO ):#line:188
                    O0OO00O00OO0O0O0O =0 #line:189
                    O0OO0000000OO0OOO =0 #line:190
                    OO0O00OOOOO0OO0OO =0 #line:191
        OOOOOOOOO0OO00O00 =True #line:194
        for O0000OO0OOOOO0O0O in OO000OOOO00O0O0OO .quantifiers .keys ():#line:195
            if O0000OO0OOOOO0O0O =='Base':#line:196
                OOOOOOOOO0OO00O00 =OOOOOOOOO0OO00O00 and (OO000OOOO00O0O0OO .quantifiers .get (O0000OO0OOOOO0O0O )<=OOOO0OO0O0O000O0O )#line:197
            if O0000OO0OOOOO0O0O =='RelBase':#line:198
                OOOOOOOOO0OO00O00 =OOOOOOOOO0OO00O00 and (OO000OOOO00O0O0OO .quantifiers .get (O0000OO0OOOOO0O0O )<=OOOO0OO0O0O000O0O *1.0 /OO000OOOO00O0O0OO .data ["rows_count"])#line:199
            if O0000OO0OOOOO0O0O =='S_Up':#line:200
                OOOOOOOOO0OO00O00 =OOOOOOOOO0OO00O00 and (OO000OOOO00O0O0OO .quantifiers .get (O0000OO0OOOOO0O0O )<=OOOO0O000O0OOO0OO )#line:201
            if O0000OO0OOOOO0O0O =='S_Down':#line:202
                OOOOOOOOO0OO00O00 =OOOOOOOOO0OO00O00 and (OO000OOOO00O0O0OO .quantifiers .get (O0000OO0OOOOO0O0O )<=O0OOOO0O00O0OOO0O )#line:203
            if O0000OO0OOOOO0O0O =='S_Any_Up':#line:204
                OOOOOOOOO0OO00O00 =OOOOOOOOO0OO00O00 and (OO000OOOO00O0O0OO .quantifiers .get (O0000OO0OOOOO0O0O )<=OOOO0O000O0OOO0OO )#line:205
            if O0000OO0OOOOO0O0O =='S_Any_Down':#line:206
                OOOOOOOOO0OO00O00 =OOOOOOOOO0OO00O00 and (OO000OOOO00O0O0OO .quantifiers .get (O0000OO0OOOOO0O0O )<=O0OOOO0O00O0OOO0O )#line:207
            if O0000OO0OOOOO0O0O =='Max':#line:208
                OOOOOOOOO0OO00O00 =OOOOOOOOO0OO00O00 and (OO000OOOO00O0O0OO .quantifiers .get (O0000OO0OOOOO0O0O )<=max (O00OOO0O00O00000O ))#line:209
            if O0000OO0OOOOO0O0O =='Min':#line:210
                OOOOOOOOO0OO00O00 =OOOOOOOOO0OO00O00 and (OO000OOOO00O0O0OO .quantifiers .get (O0000OO0OOOOO0O0O )<=min (O00OOO0O00O00000O ))#line:211
            if O0000OO0OOOOO0O0O =='Relmax':#line:212
                if sum (O00OOO0O00O00000O )>0 :#line:213
                    OOOOOOOOO0OO00O00 =OOOOOOOOO0OO00O00 and (OO000OOOO00O0O0OO .quantifiers .get (O0000OO0OOOOO0O0O )<=max (O00OOO0O00O00000O )*1.0 /sum (O00OOO0O00O00000O ))#line:214
                else :#line:215
                    OOOOOOOOO0OO00O00 =False #line:216
            if O0000OO0OOOOO0O0O =='Relmin':#line:217
                if sum (O00OOO0O00O00000O )>0 :#line:218
                    OOOOOOOOO0OO00O00 =OOOOOOOOO0OO00O00 and (OO000OOOO00O0O0OO .quantifiers .get (O0000OO0OOOOO0O0O )<=min (O00OOO0O00O00000O )*1.0 /sum (O00OOO0O00O00000O ))#line:219
                else :#line:220
                    OOOOOOOOO0OO00O00 =False #line:221
        OO0O0OOO0000OOO00 ={}#line:222
        if OOOOOOOOO0OO00O00 ==True :#line:223
            OO000OOOO00O0O0OO .stats ['total_valid']+=1 #line:225
            OO0O0OOO0000OOO00 ["base"]=OOOO0OO0O0O000O0O #line:226
            OO0O0OOO0000OOO00 ["rel_base"]=OOOO0OO0O0O000O0O *1.0 /OO000OOOO00O0O0OO .data ["rows_count"]#line:227
            OO0O0OOO0000OOO00 ["s_up"]=OOOO0O000O0OOO0OO #line:228
            OO0O0OOO0000OOO00 ["s_down"]=O0OOOO0O00O0OOO0O #line:229
            OO0O0OOO0000OOO00 ["s_any_up"]=OO0O0OOO00O0O0O0O #line:230
            OO0O0OOO0000OOO00 ["s_any_down"]=OOOO0O0OOO00O0O00 #line:231
            OO0O0OOO0000OOO00 ["max"]=max (O00OOO0O00O00000O )#line:232
            OO0O0OOO0000OOO00 ["min"]=min (O00OOO0O00O00000O )#line:233
            OO0O0OOO0000OOO00 ["rel_max"]=max (O00OOO0O00O00000O )*1.0 /OO000OOOO00O0O0OO .data ["rows_count"]#line:234
            OO0O0OOO0000OOO00 ["rel_min"]=min (O00OOO0O00O00000O )*1.0 /OO000OOOO00O0O0OO .data ["rows_count"]#line:235
            OO0O0OOO0000OOO00 ["hist"]=O00OOO0O00O00000O #line:236
        return OOOOOOOOO0OO00O00 ,OO0O0OOO0000OOO00 #line:238
    def _verify4ft (OO000OOO0O0O000O0 ,_O000O0OO0OOOOO00O ):#line:240
        O000000OO0OOOO00O ={}#line:241
        OOOOO0OO0O0O0O00O =0 #line:242
        for O0O000O00OOO0O000 in OO000OOO0O0O000O0 .task_actinfo ['cedents']:#line:243
            O000000OO0OOOO00O [O0O000O00OOO0O000 ['cedent_type']]=O0O000O00OOO0O000 ['filter_value']#line:245
            OOOOO0OO0O0O0O00O =OOOOO0OO0O0O0O00O +1 #line:246
        OOO00O0OOOOOO00OO =bin (O000000OO0OOOO00O ['ante']&O000000OO0OOOO00O ['succ']&O000000OO0OOOO00O ['cond']).count ("1")#line:248
        OOOOOOO00OOOOOOOO =None #line:249
        OOOOOOO00OOOOOOOO =0 #line:250
        if OOO00O0OOOOOO00OO >0 :#line:259
            OOOOOOO00OOOOOOOO =bin (O000000OO0OOOO00O ['ante']&O000000OO0OOOO00O ['succ']&O000000OO0OOOO00O ['cond']).count ("1")*1.0 /bin (O000000OO0OOOO00O ['ante']&O000000OO0OOOO00O ['cond']).count ("1")#line:260
        OO0OOO00O0OO000O0 =1 <<OO000OOO0O0O000O0 .data ["rows_count"]#line:262
        OOOO00O000OO0OOO0 =bin (O000000OO0OOOO00O ['ante']&O000000OO0OOOO00O ['succ']&O000000OO0OOOO00O ['cond']).count ("1")#line:263
        O0O0OOOOOOOO0OO00 =bin (O000000OO0OOOO00O ['ante']&~(OO0OOO00O0OO000O0 |O000000OO0OOOO00O ['succ'])&O000000OO0OOOO00O ['cond']).count ("1")#line:264
        O0O000O00OOO0O000 =bin (~(OO0OOO00O0OO000O0 |O000000OO0OOOO00O ['ante'])&O000000OO0OOOO00O ['succ']&O000000OO0OOOO00O ['cond']).count ("1")#line:265
        O0O00O0OO0O0000O0 =bin (~(OO0OOO00O0OO000O0 |O000000OO0OOOO00O ['ante'])&~(OO0OOO00O0OO000O0 |O000000OO0OOOO00O ['succ'])&O000000OO0OOOO00O ['cond']).count ("1")#line:266
        O000O0000O000O000 =0 #line:267
        if (OOOO00O000OO0OOO0 +O0O0OOOOOOOO0OO00 )*(OOOO00O000OO0OOO0 +O0O000O00OOO0O000 )>0 :#line:268
            O000O0000O000O000 =OOOO00O000OO0OOO0 *(OOOO00O000OO0OOO0 +O0O0OOOOOOOO0OO00 +O0O000O00OOO0O000 +O0O00O0OO0O0000O0 )/(OOOO00O000OO0OOO0 +O0O0OOOOOOOO0OO00 )/(OOOO00O000OO0OOO0 +O0O000O00OOO0O000 )-1 #line:269
        else :#line:270
            O000O0000O000O000 =None #line:271
        OO0O0OO0O0O0OOOOO =0 #line:272
        if (OOOO00O000OO0OOO0 +O0O0OOOOOOOO0OO00 )*(OOOO00O000OO0OOO0 +O0O000O00OOO0O000 )>0 :#line:273
            OO0O0OO0O0O0OOOOO =1 -OOOO00O000OO0OOO0 *(OOOO00O000OO0OOO0 +O0O0OOOOOOOO0OO00 +O0O000O00OOO0O000 +O0O00O0OO0O0000O0 )/(OOOO00O000OO0OOO0 +O0O0OOOOOOOO0OO00 )/(OOOO00O000OO0OOO0 +O0O000O00OOO0O000 )#line:274
        else :#line:275
            OO0O0OO0O0O0OOOOO =None #line:276
        OO000OO00OOO00OO0 =True #line:277
        for OOOO0000OO0O00000 in OO000OOO0O0O000O0 .quantifiers .keys ():#line:278
            if OOOO0000OO0O00000 =='Base':#line:279
                OO000OO00OOO00OO0 =OO000OO00OOO00OO0 and (OO000OOO0O0O000O0 .quantifiers .get (OOOO0000OO0O00000 )<=OOO00O0OOOOOO00OO )#line:280
            if OOOO0000OO0O00000 =='RelBase':#line:281
                OO000OO00OOO00OO0 =OO000OO00OOO00OO0 and (OO000OOO0O0O000O0 .quantifiers .get (OOOO0000OO0O00000 )<=OOO00O0OOOOOO00OO *1.0 /OO000OOO0O0O000O0 .data ["rows_count"])#line:282
            if OOOO0000OO0O00000 =='pim':#line:283
                OO000OO00OOO00OO0 =OO000OO00OOO00OO0 and (OO000OOO0O0O000O0 .quantifiers .get (OOOO0000OO0O00000 )<=OOOOOOO00OOOOOOOO )#line:284
            if OOOO0000OO0O00000 =='aad':#line:285
                if O000O0000O000O000 !=None :#line:286
                    OO000OO00OOO00OO0 =OO000OO00OOO00OO0 and (OO000OOO0O0O000O0 .quantifiers .get (OOOO0000OO0O00000 )<=O000O0000O000O000 )#line:287
                else :#line:288
                    OO000OO00OOO00OO0 =False #line:289
            if OOOO0000OO0O00000 =='bad':#line:290
                if OO0O0OO0O0O0OOOOO !=None :#line:291
                    OO000OO00OOO00OO0 =OO000OO00OOO00OO0 and (OO000OOO0O0O000O0 .quantifiers .get (OOOO0000OO0O00000 )<=OO0O0OO0O0O0OOOOO )#line:292
                else :#line:293
                    OO000OO00OOO00OO0 =False #line:294
            O0OOO0O0OOO00O00O ={}#line:295
        if OO000OO00OOO00OO0 ==True :#line:296
            OO000OOO0O0O000O0 .stats ['total_valid']+=1 #line:298
            O0OOO0O0OOO00O00O ["base"]=OOO00O0OOOOOO00OO #line:299
            O0OOO0O0OOO00O00O ["rel_base"]=OOO00O0OOOOOO00OO *1.0 /OO000OOO0O0O000O0 .data ["rows_count"]#line:300
            O0OOO0O0OOO00O00O ["pim"]=OOOOOOO00OOOOOOOO #line:301
            O0OOO0O0OOO00O00O ["aad"]=O000O0000O000O000 #line:302
            O0OOO0O0OOO00O00O ["bad"]=OO0O0OO0O0O0OOOOO #line:303
            O0OOO0O0OOO00O00O ["fourfold"]=[OOOO00O000OO0OOO0 ,O0O0OOOOOOOO0OO00 ,O0O000O00OOO0O000 ,O0O00O0OO0O0000O0 ]#line:304
        return OO000OO00OOO00OO0 ,O0OOO0O0OOO00O00O #line:308
    def _verifysd4ft (O0OOOO00OO0O00000 ,_OO0000OOOOOO0O0O0 ):#line:310
        OO000O00OO0000O0O ={}#line:311
        OOOO0OOOO0OO00O0O =0 #line:312
        for O00OOOOO00O00O000 in O0OOOO00OO0O00000 .task_actinfo ['cedents']:#line:313
            OO000O00OO0000O0O [O00OOOOO00O00O000 ['cedent_type']]=O00OOOOO00O00O000 ['filter_value']#line:315
            OOOO0OOOO0OO00O0O =OOOO0OOOO0OO00O0O +1 #line:316
        O0O0O0O0OO0O0OOO0 =bin (OO000O00OO0000O0O ['ante']&OO000O00OO0000O0O ['succ']&OO000O00OO0000O0O ['cond']&OO000O00OO0000O0O ['frst']).count ("1")#line:318
        O00OOO00O0OO0O000 =bin (OO000O00OO0000O0O ['ante']&OO000O00OO0000O0O ['succ']&OO000O00OO0000O0O ['cond']&OO000O00OO0000O0O ['scnd']).count ("1")#line:319
        OOOOOOOO0O000000O =None #line:320
        O0OO0O000000OOOOO =0 #line:321
        O00OOOO0000000OO0 =0 #line:322
        if O0O0O0O0OO0O0OOO0 >0 :#line:331
            O0OO0O000000OOOOO =bin (OO000O00OO0000O0O ['ante']&OO000O00OO0000O0O ['succ']&OO000O00OO0000O0O ['cond']&OO000O00OO0000O0O ['frst']).count ("1")*1.0 /bin (OO000O00OO0000O0O ['ante']&OO000O00OO0000O0O ['cond']&OO000O00OO0000O0O ['frst']).count ("1")#line:332
        if O00OOO00O0OO0O000 >0 :#line:333
            O00OOOO0000000OO0 =bin (OO000O00OO0000O0O ['ante']&OO000O00OO0000O0O ['succ']&OO000O00OO0000O0O ['cond']&OO000O00OO0000O0O ['scnd']).count ("1")*1.0 /bin (OO000O00OO0000O0O ['ante']&OO000O00OO0000O0O ['cond']&OO000O00OO0000O0O ['scnd']).count ("1")#line:334
        O00OO0O00O0O00OO0 =1 <<O0OOOO00OO0O00000 .data ["rows_count"]#line:336
        O000OO00O0O00O0O0 =bin (OO000O00OO0000O0O ['ante']&OO000O00OO0000O0O ['succ']&OO000O00OO0000O0O ['cond']&OO000O00OO0000O0O ['frst']).count ("1")#line:337
        O00O0OOO0O000O0O0 =bin (OO000O00OO0000O0O ['ante']&~(O00OO0O00O0O00OO0 |OO000O00OO0000O0O ['succ'])&OO000O00OO0000O0O ['cond']&OO000O00OO0000O0O ['frst']).count ("1")#line:338
        O0O0OO000O0OO00OO =bin (~(O00OO0O00O0O00OO0 |OO000O00OO0000O0O ['ante'])&OO000O00OO0000O0O ['succ']&OO000O00OO0000O0O ['cond']&OO000O00OO0000O0O ['frst']).count ("1")#line:339
        OO0O00O00O00000OO =bin (~(O00OO0O00O0O00OO0 |OO000O00OO0000O0O ['ante'])&~(O00OO0O00O0O00OO0 |OO000O00OO0000O0O ['succ'])&OO000O00OO0000O0O ['cond']&OO000O00OO0000O0O ['frst']).count ("1")#line:340
        OOO0O00O00000O00O =bin (OO000O00OO0000O0O ['ante']&OO000O00OO0000O0O ['succ']&OO000O00OO0000O0O ['cond']&OO000O00OO0000O0O ['scnd']).count ("1")#line:341
        O0OOO000OOO000O00 =bin (OO000O00OO0000O0O ['ante']&~(O00OO0O00O0O00OO0 |OO000O00OO0000O0O ['succ'])&OO000O00OO0000O0O ['cond']&OO000O00OO0000O0O ['scnd']).count ("1")#line:342
        OOO0O0O00OO0O00O0 =bin (~(O00OO0O00O0O00OO0 |OO000O00OO0000O0O ['ante'])&OO000O00OO0000O0O ['succ']&OO000O00OO0000O0O ['cond']&OO000O00OO0000O0O ['scnd']).count ("1")#line:343
        O0OO000OO0OO000O0 =bin (~(O00OO0O00O0O00OO0 |OO000O00OO0000O0O ['ante'])&~(O00OO0O00O0O00OO0 |OO000O00OO0000O0O ['succ'])&OO000O00OO0000O0O ['cond']&OO000O00OO0000O0O ['scnd']).count ("1")#line:344
        O000000O0O0OO00OO =True #line:345
        for OO0OO00O00OOO000O in O0OOOO00OO0O00000 .quantifiers .keys ():#line:346
            if (OO0OO00O00OOO000O =='FrstBase')|(OO0OO00O00OOO000O =='Base1'):#line:347
                O000000O0O0OO00OO =O000000O0O0OO00OO and (O0OOOO00OO0O00000 .quantifiers .get (OO0OO00O00OOO000O )<=O0O0O0O0OO0O0OOO0 )#line:348
            if (OO0OO00O00OOO000O =='ScndBase')|(OO0OO00O00OOO000O =='Base2'):#line:349
                O000000O0O0OO00OO =O000000O0O0OO00OO and (O0OOOO00OO0O00000 .quantifiers .get (OO0OO00O00OOO000O )<=O00OOO00O0OO0O000 )#line:350
            if (OO0OO00O00OOO000O =='FrstRelBase')|(OO0OO00O00OOO000O =='RelBase1'):#line:351
                O000000O0O0OO00OO =O000000O0O0OO00OO and (O0OOOO00OO0O00000 .quantifiers .get (OO0OO00O00OOO000O )<=O0O0O0O0OO0O0OOO0 *1.0 /O0OOOO00OO0O00000 .data ["rows_count"])#line:352
            if (OO0OO00O00OOO000O =='ScndRelBase')|(OO0OO00O00OOO000O =='RelBase2'):#line:353
                O000000O0O0OO00OO =O000000O0O0OO00OO and (O0OOOO00OO0O00000 .quantifiers .get (OO0OO00O00OOO000O )<=O00OOO00O0OO0O000 *1.0 /O0OOOO00OO0O00000 .data ["rows_count"])#line:354
            if (OO0OO00O00OOO000O =='Frstpim')|(OO0OO00O00OOO000O =='pim1'):#line:355
                O000000O0O0OO00OO =O000000O0O0OO00OO and (O0OOOO00OO0O00000 .quantifiers .get (OO0OO00O00OOO000O )<=O0OO0O000000OOOOO )#line:356
            if (OO0OO00O00OOO000O =='Scndpim')|(OO0OO00O00OOO000O =='pim2'):#line:357
                O000000O0O0OO00OO =O000000O0O0OO00OO and (O0OOOO00OO0O00000 .quantifiers .get (OO0OO00O00OOO000O )<=O00OOOO0000000OO0 )#line:358
            if OO0OO00O00OOO000O =='Deltapim':#line:359
                O000000O0O0OO00OO =O000000O0O0OO00OO and (O0OOOO00OO0O00000 .quantifiers .get (OO0OO00O00OOO000O )<=O0OO0O000000OOOOO -O00OOOO0000000OO0 )#line:360
            if OO0OO00O00OOO000O =='Ratiopim':#line:363
                if (O00OOOO0000000OO0 >0 ):#line:364
                    O000000O0O0OO00OO =O000000O0O0OO00OO and (O0OOOO00OO0O00000 .quantifiers .get (OO0OO00O00OOO000O )<=O0OO0O000000OOOOO *1.0 /O00OOOO0000000OO0 )#line:365
                else :#line:366
                    O000000O0O0OO00OO =False #line:367
        OOOOO0O0OO00O0O0O ={}#line:368
        if O000000O0O0OO00OO ==True :#line:369
            O0OOOO00OO0O00000 .stats ['total_valid']+=1 #line:371
            OOOOO0O0OO00O0O0O ["base1"]=O0O0O0O0OO0O0OOO0 #line:372
            OOOOO0O0OO00O0O0O ["base2"]=O00OOO00O0OO0O000 #line:373
            OOOOO0O0OO00O0O0O ["rel_base1"]=O0O0O0O0OO0O0OOO0 *1.0 /O0OOOO00OO0O00000 .data ["rows_count"]#line:374
            OOOOO0O0OO00O0O0O ["rel_base2"]=O00OOO00O0OO0O000 *1.0 /O0OOOO00OO0O00000 .data ["rows_count"]#line:375
            OOOOO0O0OO00O0O0O ["pim1"]=O0OO0O000000OOOOO #line:376
            OOOOO0O0OO00O0O0O ["pim2"]=O00OOOO0000000OO0 #line:377
            OOOOO0O0OO00O0O0O ["deltapim"]=O0OO0O000000OOOOO -O00OOOO0000000OO0 #line:378
            if (O00OOOO0000000OO0 >0 ):#line:379
                OOOOO0O0OO00O0O0O ["ratiopim"]=O0OO0O000000OOOOO *1.0 /O00OOOO0000000OO0 #line:380
            else :#line:381
                OOOOO0O0OO00O0O0O ["ratiopim"]=None #line:382
            OOOOO0O0OO00O0O0O ["fourfold1"]=[O000OO00O0O00O0O0 ,O00O0OOO0O000O0O0 ,O0O0OO000O0OO00OO ,OO0O00O00O00000OO ]#line:383
            OOOOO0O0OO00O0O0O ["fourfold2"]=[OOO0O00O00000O00O ,O0OOO000OOO000O00 ,OOO0O0O00OO0O00O0 ,O0OO000OO0OO000O0 ]#line:384
        if O000000O0O0OO00OO :#line:386
            print (f"DEBUG : ii = {OOOO0OOOO0OO00O0O}")#line:387
        return O000000O0O0OO00OO ,OOOOO0O0OO00O0O0O #line:388
    def _verifynewact4ft (O000O00OOOO0OO000 ,_O0O000O00O00O0OOO ):#line:390
        OOO0O0000000000O0 ={}#line:391
        for O0O0OO0O00OOO00OO in O000O00OOOO0OO000 .task_actinfo ['cedents']:#line:392
            OOO0O0000000000O0 [O0O0OO0O00OOO00OO ['cedent_type']]=O0O0OO0O00OOO00OO ['filter_value']#line:394
        OO0OO0O0OO00O0OOO =bin (OOO0O0000000000O0 ['ante']&OOO0O0000000000O0 ['succ']&OOO0O0000000000O0 ['cond']).count ("1")#line:396
        OO0OO0OOO0OOOO0OO =bin (OOO0O0000000000O0 ['ante']&OOO0O0000000000O0 ['succ']&OOO0O0000000000O0 ['cond']&OOO0O0000000000O0 ['antv']&OOO0O0000000000O0 ['sucv']).count ("1")#line:397
        O0000OOOO00OOO000 =None #line:398
        O0OOO00O0OOOOOO0O =0 #line:399
        OO0OOO000OO0O0OO0 =0 #line:400
        if OO0OO0O0OO00O0OOO >0 :#line:409
            O0OOO00O0OOOOOO0O =bin (OOO0O0000000000O0 ['ante']&OOO0O0000000000O0 ['succ']&OOO0O0000000000O0 ['cond']).count ("1")*1.0 /bin (OOO0O0000000000O0 ['ante']&OOO0O0000000000O0 ['cond']).count ("1")#line:411
        if OO0OO0OOO0OOOO0OO >0 :#line:412
            OO0OOO000OO0O0OO0 =bin (OOO0O0000000000O0 ['ante']&OOO0O0000000000O0 ['succ']&OOO0O0000000000O0 ['cond']&OOO0O0000000000O0 ['antv']&OOO0O0000000000O0 ['sucv']).count ("1")*1.0 /bin (OOO0O0000000000O0 ['ante']&OOO0O0000000000O0 ['cond']&OOO0O0000000000O0 ['antv']).count ("1")#line:414
        O0000O00000000OOO =1 <<O000O00OOOO0OO000 .rows_count #line:416
        O0O000O0O0O000O00 =bin (OOO0O0000000000O0 ['ante']&OOO0O0000000000O0 ['succ']&OOO0O0000000000O0 ['cond']).count ("1")#line:417
        OO0O00O0OOOOOO00O =bin (OOO0O0000000000O0 ['ante']&~(O0000O00000000OOO |OOO0O0000000000O0 ['succ'])&OOO0O0000000000O0 ['cond']).count ("1")#line:418
        OO0OOO0OOO0000O00 =bin (~(O0000O00000000OOO |OOO0O0000000000O0 ['ante'])&OOO0O0000000000O0 ['succ']&OOO0O0000000000O0 ['cond']).count ("1")#line:419
        OO0O00O000O0OO0O0 =bin (~(O0000O00000000OOO |OOO0O0000000000O0 ['ante'])&~(O0000O00000000OOO |OOO0O0000000000O0 ['succ'])&OOO0O0000000000O0 ['cond']).count ("1")#line:420
        O00O00OO0OO000OO0 =bin (OOO0O0000000000O0 ['ante']&OOO0O0000000000O0 ['succ']&OOO0O0000000000O0 ['cond']&OOO0O0000000000O0 ['antv']&OOO0O0000000000O0 ['sucv']).count ("1")#line:421
        OO0O0O000OO00000O =bin (OOO0O0000000000O0 ['ante']&~(O0000O00000000OOO |(OOO0O0000000000O0 ['succ']&OOO0O0000000000O0 ['sucv']))&OOO0O0000000000O0 ['cond']).count ("1")#line:422
        O000OO00OO00000O0 =bin (~(O0000O00000000OOO |(OOO0O0000000000O0 ['ante']&OOO0O0000000000O0 ['antv']))&OOO0O0000000000O0 ['succ']&OOO0O0000000000O0 ['cond']&OOO0O0000000000O0 ['sucv']).count ("1")#line:423
        O00O00OO0O0OOOOO0 =bin (~(O0000O00000000OOO |(OOO0O0000000000O0 ['ante']&OOO0O0000000000O0 ['antv']))&~(O0000O00000000OOO |(OOO0O0000000000O0 ['succ']&OOO0O0000000000O0 ['sucv']))&OOO0O0000000000O0 ['cond']).count ("1")#line:424
        OOOOOOO0OOOO0OO00 =True #line:425
        for OOOO000000OOOOOO0 in O000O00OOOO0OO000 .quantifiers .keys ():#line:426
            if (OOOO000000OOOOOO0 =='PreBase')|(OOOO000000OOOOOO0 =='Base1'):#line:427
                OOOOOOO0OOOO0OO00 =OOOOOOO0OOOO0OO00 and (O000O00OOOO0OO000 .quantifiers .get (OOOO000000OOOOOO0 )<=OO0OO0O0OO00O0OOO )#line:428
            if (OOOO000000OOOOOO0 =='PostBase')|(OOOO000000OOOOOO0 =='Base2'):#line:429
                OOOOOOO0OOOO0OO00 =OOOOOOO0OOOO0OO00 and (O000O00OOOO0OO000 .quantifiers .get (OOOO000000OOOOOO0 )<=OO0OO0OOO0OOOO0OO )#line:430
            if (OOOO000000OOOOOO0 =='PreRelBase')|(OOOO000000OOOOOO0 =='RelBase1'):#line:431
                OOOOOOO0OOOO0OO00 =OOOOOOO0OOOO0OO00 and (O000O00OOOO0OO000 .quantifiers .get (OOOO000000OOOOOO0 )<=OO0OO0O0OO00O0OOO *1.0 /O000O00OOOO0OO000 .data ["rows_count"])#line:432
            if (OOOO000000OOOOOO0 =='PostRelBase')|(OOOO000000OOOOOO0 =='RelBase2'):#line:433
                OOOOOOO0OOOO0OO00 =OOOOOOO0OOOO0OO00 and (O000O00OOOO0OO000 .quantifiers .get (OOOO000000OOOOOO0 )<=OO0OO0OOO0OOOO0OO *1.0 /O000O00OOOO0OO000 .data ["rows_count"])#line:434
            if (OOOO000000OOOOOO0 =='Prepim')|(OOOO000000OOOOOO0 =='pim1'):#line:435
                OOOOOOO0OOOO0OO00 =OOOOOOO0OOOO0OO00 and (O000O00OOOO0OO000 .quantifiers .get (OOOO000000OOOOOO0 )<=O0OOO00O0OOOOOO0O )#line:436
            if (OOOO000000OOOOOO0 =='Postpim')|(OOOO000000OOOOOO0 =='pim2'):#line:437
                OOOOOOO0OOOO0OO00 =OOOOOOO0OOOO0OO00 and (O000O00OOOO0OO000 .quantifiers .get (OOOO000000OOOOOO0 )<=OO0OOO000OO0O0OO0 )#line:438
            if OOOO000000OOOOOO0 =='Deltapim':#line:439
                OOOOOOO0OOOO0OO00 =OOOOOOO0OOOO0OO00 and (O000O00OOOO0OO000 .quantifiers .get (OOOO000000OOOOOO0 )<=O0OOO00O0OOOOOO0O -OO0OOO000OO0O0OO0 )#line:440
            if OOOO000000OOOOOO0 =='Ratiopim':#line:443
                if (OO0OOO000OO0O0OO0 >0 ):#line:444
                    OOOOOOO0OOOO0OO00 =OOOOOOO0OOOO0OO00 and (O000O00OOOO0OO000 .quantifiers .get (OOOO000000OOOOOO0 )<=O0OOO00O0OOOOOO0O *1.0 /OO0OOO000OO0O0OO0 )#line:445
                else :#line:446
                    OOOOOOO0OOOO0OO00 =False #line:447
        O00OOO00O00OOO000 ={}#line:448
        if OOOOOOO0OOOO0OO00 ==True :#line:449
            O000O00OOOO0OO000 .stats ['total_valid']+=1 #line:451
            O00OOO00O00OOO000 ["base1"]=OO0OO0O0OO00O0OOO #line:452
            O00OOO00O00OOO000 ["base2"]=OO0OO0OOO0OOOO0OO #line:453
            O00OOO00O00OOO000 ["rel_base1"]=OO0OO0O0OO00O0OOO *1.0 /O000O00OOOO0OO000 .data ["rows_count"]#line:454
            O00OOO00O00OOO000 ["rel_base2"]=OO0OO0OOO0OOOO0OO *1.0 /O000O00OOOO0OO000 .data ["rows_count"]#line:455
            O00OOO00O00OOO000 ["pim1"]=O0OOO00O0OOOOOO0O #line:456
            O00OOO00O00OOO000 ["pim2"]=OO0OOO000OO0O0OO0 #line:457
            O00OOO00O00OOO000 ["deltapim"]=O0OOO00O0OOOOOO0O -OO0OOO000OO0O0OO0 #line:458
            if (OO0OOO000OO0O0OO0 >0 ):#line:459
                O00OOO00O00OOO000 ["ratiopim"]=O0OOO00O0OOOOOO0O *1.0 /OO0OOO000OO0O0OO0 #line:460
            else :#line:461
                O00OOO00O00OOO000 ["ratiopim"]=None #line:462
            O00OOO00O00OOO000 ["fourfoldpre"]=[O0O000O0O0O000O00 ,OO0O00O0OOOOOO00O ,OO0OOO0OOO0000O00 ,OO0O00O000O0OO0O0 ]#line:463
            O00OOO00O00OOO000 ["fourfoldpost"]=[O00O00OO0OO000OO0 ,OO0O0O000OO00000O ,O000OO00OO00000O0 ,O00O00OO0O0OOOOO0 ]#line:464
        return OOOOOOO0OOOO0OO00 ,O00OOO00O00OOO000 #line:466
    def _verifyact4ft (O0O000OO0O000000O ,_OO0O0OO0O00O00OO0 ):#line:468
        OOO0O00OO0O0O0O0O ={}#line:469
        for O00000OO0O0O0O00O in O0O000OO0O000000O .task_actinfo ['cedents']:#line:470
            OOO0O00OO0O0O0O0O [O00000OO0O0O0O00O ['cedent_type']]=O00000OO0O0O0O00O ['filter_value']#line:472
        OOO0O00O00OO0O000 =bin (OOO0O00OO0O0O0O0O ['ante']&OOO0O00OO0O0O0O0O ['succ']&OOO0O00OO0O0O0O0O ['cond']&OOO0O00OO0O0O0O0O ['antv-']&OOO0O00OO0O0O0O0O ['sucv-']).count ("1")#line:474
        O000O00000OO0OOO0 =bin (OOO0O00OO0O0O0O0O ['ante']&OOO0O00OO0O0O0O0O ['succ']&OOO0O00OO0O0O0O0O ['cond']&OOO0O00OO0O0O0O0O ['antv+']&OOO0O00OO0O0O0O0O ['sucv+']).count ("1")#line:475
        OOOO000OO00O00O0O =None #line:476
        OO00OOO0OO000OOO0 =0 #line:477
        OOOO00OOOO00OO0OO =0 #line:478
        if OOO0O00O00OO0O000 >0 :#line:487
            OO00OOO0OO000OOO0 =bin (OOO0O00OO0O0O0O0O ['ante']&OOO0O00OO0O0O0O0O ['succ']&OOO0O00OO0O0O0O0O ['cond']&OOO0O00OO0O0O0O0O ['antv-']&OOO0O00OO0O0O0O0O ['sucv-']).count ("1")*1.0 /bin (OOO0O00OO0O0O0O0O ['ante']&OOO0O00OO0O0O0O0O ['cond']&OOO0O00OO0O0O0O0O ['antv-']).count ("1")#line:489
        if O000O00000OO0OOO0 >0 :#line:490
            OOOO00OOOO00OO0OO =bin (OOO0O00OO0O0O0O0O ['ante']&OOO0O00OO0O0O0O0O ['succ']&OOO0O00OO0O0O0O0O ['cond']&OOO0O00OO0O0O0O0O ['antv+']&OOO0O00OO0O0O0O0O ['sucv+']).count ("1")*1.0 /bin (OOO0O00OO0O0O0O0O ['ante']&OOO0O00OO0O0O0O0O ['cond']&OOO0O00OO0O0O0O0O ['antv+']).count ("1")#line:492
        O0OOO00OO00O0O00O =1 <<O0O000OO0O000000O .data ["rows_count"]#line:494
        OOOO00OOO00000O00 =bin (OOO0O00OO0O0O0O0O ['ante']&OOO0O00OO0O0O0O0O ['succ']&OOO0O00OO0O0O0O0O ['cond']&OOO0O00OO0O0O0O0O ['antv-']&OOO0O00OO0O0O0O0O ['sucv-']).count ("1")#line:495
        O0OOOO0O0OO000OO0 =bin (OOO0O00OO0O0O0O0O ['ante']&OOO0O00OO0O0O0O0O ['antv-']&~(O0OOO00OO00O0O00O |(OOO0O00OO0O0O0O0O ['succ']&OOO0O00OO0O0O0O0O ['sucv-']))&OOO0O00OO0O0O0O0O ['cond']).count ("1")#line:496
        O0O00000O0OOO00OO =bin (~(O0OOO00OO00O0O00O |(OOO0O00OO0O0O0O0O ['ante']&OOO0O00OO0O0O0O0O ['antv-']))&OOO0O00OO0O0O0O0O ['succ']&OOO0O00OO0O0O0O0O ['cond']&OOO0O00OO0O0O0O0O ['sucv-']).count ("1")#line:497
        OO0O0O0OO0OOO00O0 =bin (~(O0OOO00OO00O0O00O |(OOO0O00OO0O0O0O0O ['ante']&OOO0O00OO0O0O0O0O ['antv-']))&~(O0OOO00OO00O0O00O |(OOO0O00OO0O0O0O0O ['succ']&OOO0O00OO0O0O0O0O ['sucv-']))&OOO0O00OO0O0O0O0O ['cond']).count ("1")#line:498
        OOO0O000000O00O0O =bin (OOO0O00OO0O0O0O0O ['ante']&OOO0O00OO0O0O0O0O ['succ']&OOO0O00OO0O0O0O0O ['cond']&OOO0O00OO0O0O0O0O ['antv+']&OOO0O00OO0O0O0O0O ['sucv+']).count ("1")#line:499
        O000O000OO00OO000 =bin (OOO0O00OO0O0O0O0O ['ante']&OOO0O00OO0O0O0O0O ['antv+']&~(O0OOO00OO00O0O00O |(OOO0O00OO0O0O0O0O ['succ']&OOO0O00OO0O0O0O0O ['sucv+']))&OOO0O00OO0O0O0O0O ['cond']).count ("1")#line:500
        OOOOO00O0OOOO0O00 =bin (~(O0OOO00OO00O0O00O |(OOO0O00OO0O0O0O0O ['ante']&OOO0O00OO0O0O0O0O ['antv+']))&OOO0O00OO0O0O0O0O ['succ']&OOO0O00OO0O0O0O0O ['cond']&OOO0O00OO0O0O0O0O ['sucv+']).count ("1")#line:501
        OO0OOOOO000000000 =bin (~(O0OOO00OO00O0O00O |(OOO0O00OO0O0O0O0O ['ante']&OOO0O00OO0O0O0O0O ['antv+']))&~(O0OOO00OO00O0O00O |(OOO0O00OO0O0O0O0O ['succ']&OOO0O00OO0O0O0O0O ['sucv+']))&OOO0O00OO0O0O0O0O ['cond']).count ("1")#line:502
        OO000OO0O0OOOO0OO =True #line:503
        for O0OO0O0O0O000OO0O in O0O000OO0O000000O .quantifiers .keys ():#line:504
            if (O0OO0O0O0O000OO0O =='PreBase')|(O0OO0O0O0O000OO0O =='Base1'):#line:505
                OO000OO0O0OOOO0OO =OO000OO0O0OOOO0OO and (O0O000OO0O000000O .quantifiers .get (O0OO0O0O0O000OO0O )<=OOO0O00O00OO0O000 )#line:506
            if (O0OO0O0O0O000OO0O =='PostBase')|(O0OO0O0O0O000OO0O =='Base2'):#line:507
                OO000OO0O0OOOO0OO =OO000OO0O0OOOO0OO and (O0O000OO0O000000O .quantifiers .get (O0OO0O0O0O000OO0O )<=O000O00000OO0OOO0 )#line:508
            if (O0OO0O0O0O000OO0O =='PreRelBase')|(O0OO0O0O0O000OO0O =='RelBase1'):#line:509
                OO000OO0O0OOOO0OO =OO000OO0O0OOOO0OO and (O0O000OO0O000000O .quantifiers .get (O0OO0O0O0O000OO0O )<=OOO0O00O00OO0O000 *1.0 /O0O000OO0O000000O .data ["rows_count"])#line:510
            if (O0OO0O0O0O000OO0O =='PostRelBase')|(O0OO0O0O0O000OO0O =='RelBase2'):#line:511
                OO000OO0O0OOOO0OO =OO000OO0O0OOOO0OO and (O0O000OO0O000000O .quantifiers .get (O0OO0O0O0O000OO0O )<=O000O00000OO0OOO0 *1.0 /O0O000OO0O000000O .data ["rows_count"])#line:512
            if (O0OO0O0O0O000OO0O =='Prepim')|(O0OO0O0O0O000OO0O =='pim1'):#line:513
                OO000OO0O0OOOO0OO =OO000OO0O0OOOO0OO and (O0O000OO0O000000O .quantifiers .get (O0OO0O0O0O000OO0O )<=OO00OOO0OO000OOO0 )#line:514
            if (O0OO0O0O0O000OO0O =='Postpim')|(O0OO0O0O0O000OO0O =='pim2'):#line:515
                OO000OO0O0OOOO0OO =OO000OO0O0OOOO0OO and (O0O000OO0O000000O .quantifiers .get (O0OO0O0O0O000OO0O )<=OOOO00OOOO00OO0OO )#line:516
            if O0OO0O0O0O000OO0O =='Deltapim':#line:517
                OO000OO0O0OOOO0OO =OO000OO0O0OOOO0OO and (O0O000OO0O000000O .quantifiers .get (O0OO0O0O0O000OO0O )<=OO00OOO0OO000OOO0 -OOOO00OOOO00OO0OO )#line:518
            if O0OO0O0O0O000OO0O =='Ratiopim':#line:521
                if (OO00OOO0OO000OOO0 >0 ):#line:522
                    OO000OO0O0OOOO0OO =OO000OO0O0OOOO0OO and (O0O000OO0O000000O .quantifiers .get (O0OO0O0O0O000OO0O )<=OOOO00OOOO00OO0OO *1.0 /OO00OOO0OO000OOO0 )#line:523
                else :#line:524
                    OO000OO0O0OOOO0OO =False #line:525
        O0OOOOOO0O0OO0OOO ={}#line:526
        if OO000OO0O0OOOO0OO ==True :#line:527
            O0O000OO0O000000O .stats ['total_valid']+=1 #line:529
            O0OOOOOO0O0OO0OOO ["base1"]=OOO0O00O00OO0O000 #line:530
            O0OOOOOO0O0OO0OOO ["base2"]=O000O00000OO0OOO0 #line:531
            O0OOOOOO0O0OO0OOO ["rel_base1"]=OOO0O00O00OO0O000 *1.0 /O0O000OO0O000000O .data ["rows_count"]#line:532
            O0OOOOOO0O0OO0OOO ["rel_base2"]=O000O00000OO0OOO0 *1.0 /O0O000OO0O000000O .data ["rows_count"]#line:533
            O0OOOOOO0O0OO0OOO ["pim1"]=OO00OOO0OO000OOO0 #line:534
            O0OOOOOO0O0OO0OOO ["pim2"]=OOOO00OOOO00OO0OO #line:535
            O0OOOOOO0O0OO0OOO ["deltapim"]=OO00OOO0OO000OOO0 -OOOO00OOOO00OO0OO #line:536
            if (OO00OOO0OO000OOO0 >0 ):#line:537
                O0OOOOOO0O0OO0OOO ["ratiopim"]=OOOO00OOOO00OO0OO *1.0 /OO00OOO0OO000OOO0 #line:538
            else :#line:539
                O0OOOOOO0O0OO0OOO ["ratiopim"]=None #line:540
            O0OOOOOO0O0OO0OOO ["fourfoldpre"]=[OOOO00OOO00000O00 ,O0OOOO0O0OO000OO0 ,O0O00000O0OOO00OO ,OO0O0O0OO0OOO00O0 ]#line:541
            O0OOOOOO0O0OO0OOO ["fourfoldpost"]=[OOO0O000000O00O0O ,O000O000OO00OO000 ,OOOOO00O0OOOO0O00 ,OO0OOOOO000000000 ]#line:542
        return OO000OO0O0OOOO0OO ,O0OOOOOO0O0OO0OOO #line:544
    def _verify_opt (OO00O0000000000OO ,OO0O0OOO00OOOOO0O ,OO00OO0O0000O0000 ):#line:546
        OOO0OOO0OO00OOO00 =False #line:547
        if not (OO0O0OOO00OOOOO0O ['optim'].get ('only_con')):#line:550
            return False #line:551
        OOO00000OOOO0O0O0 ={}#line:552
        for OOOO00O00OO0OO0OO in OO00O0000000000OO .task_actinfo ['cedents']:#line:553
            OOO00000OOOO0O0O0 [OOOO00O00OO0OO0OO ['cedent_type']]=OOOO00O00OO0OO0OO ['filter_value']#line:555
        O00O000OOOOOOOO00 =1 <<OO00O0000000000OO .data ["rows_count"]#line:557
        OOO0OO00OO00OOO0O =O00O000OOOOOOOO00 -1 #line:558
        O0OOOOO000000O00O =""#line:559
        O0OO00OOOOO00OOO0 =0 #line:560
        if (OOO00000OOOO0O0O0 .get ('ante')!=None ):#line:561
            OOO0OO00OO00OOO0O =OOO0OO00OO00OOO0O &OOO00000OOOO0O0O0 ['ante']#line:562
        if (OOO00000OOOO0O0O0 .get ('succ')!=None ):#line:563
            OOO0OO00OO00OOO0O =OOO0OO00OO00OOO0O &OOO00000OOOO0O0O0 ['succ']#line:564
        if (OOO00000OOOO0O0O0 .get ('cond')!=None ):#line:565
            OOO0OO00OO00OOO0O =OOO0OO00OO00OOO0O &OOO00000OOOO0O0O0 ['cond']#line:566
        OOOO0OO00OOO0O0O0 =None #line:569
        if (OO00O0000000000OO .proc =='CFMiner')|(OO00O0000000000OO .proc =='4ftMiner'):#line:594
            OO00O0OO00OO0OO00 =bin (OOO0OO00OO00OOO0O ).count ("1")#line:595
            for O00O0O0OO00O0OOO0 in OO00O0000000000OO .quantifiers .keys ():#line:596
                if O00O0O0OO00O0OOO0 =='Base':#line:597
                    if not (OO00O0000000000OO .quantifiers .get (O00O0O0OO00O0OOO0 )<=OO00O0OO00OO0OO00 ):#line:598
                        OOO0OOO0OO00OOO00 =True #line:599
                if O00O0O0OO00O0OOO0 =='RelBase':#line:601
                    if not (OO00O0000000000OO .quantifiers .get (O00O0O0OO00O0OOO0 )<=OO00O0OO00OO0OO00 *1.0 /OO00O0000000000OO .data ["rows_count"]):#line:602
                        OOO0OOO0OO00OOO00 =True #line:603
        return OOO0OOO0OO00OOO00 #line:606
        if OO00O0000000000OO .proc =='CFMiner':#line:609
            if (OO00OO0O0000O0000 ['cedent_type']=='cond')&(OO00OO0O0000O0000 ['defi'].get ('type')=='con'):#line:610
                OO00O0OO00OO0OO00 =bin (OOO00000OOOO0O0O0 ['cond']).count ("1")#line:611
                O0OOO0000O000OO0O =True #line:612
                for O00O0O0OO00O0OOO0 in OO00O0000000000OO .quantifiers .keys ():#line:613
                    if O00O0O0OO00O0OOO0 =='Base':#line:614
                        O0OOO0000O000OO0O =O0OOO0000O000OO0O and (OO00O0000000000OO .quantifiers .get (O00O0O0OO00O0OOO0 )<=OO00O0OO00OO0OO00 )#line:615
                        if not (O0OOO0000O000OO0O ):#line:616
                            print (f"...optimization : base is {OO00O0OO00OO0OO00} for {OO00OO0O0000O0000['generated_string']}")#line:617
                    if O00O0O0OO00O0OOO0 =='RelBase':#line:618
                        O0OOO0000O000OO0O =O0OOO0000O000OO0O and (OO00O0000000000OO .quantifiers .get (O00O0O0OO00O0OOO0 )<=OO00O0OO00OO0OO00 *1.0 /OO00O0000000000OO .data ["rows_count"])#line:619
                        if not (O0OOO0000O000OO0O ):#line:620
                            print (f"...optimization : base is {OO00O0OO00OO0OO00} for {OO00OO0O0000O0000['generated_string']}")#line:621
                OOO0OOO0OO00OOO00 =not (O0OOO0000O000OO0O )#line:622
        elif OO00O0000000000OO .proc =='4ftMiner':#line:623
            if (OO00OO0O0000O0000 ['cedent_type']=='cond')&(OO00OO0O0000O0000 ['defi'].get ('type')=='con'):#line:624
                OO00O0OO00OO0OO00 =bin (OOO00000OOOO0O0O0 ['cond']).count ("1")#line:625
                O0OOO0000O000OO0O =True #line:626
                for O00O0O0OO00O0OOO0 in OO00O0000000000OO .quantifiers .keys ():#line:627
                    if O00O0O0OO00O0OOO0 =='Base':#line:628
                        O0OOO0000O000OO0O =O0OOO0000O000OO0O and (OO00O0000000000OO .quantifiers .get (O00O0O0OO00O0OOO0 )<=OO00O0OO00OO0OO00 )#line:629
                        if not (O0OOO0000O000OO0O ):#line:630
                            print (f"...optimization : base is {OO00O0OO00OO0OO00} for {OO00OO0O0000O0000['generated_string']}")#line:631
                    if O00O0O0OO00O0OOO0 =='RelBase':#line:632
                        O0OOO0000O000OO0O =O0OOO0000O000OO0O and (OO00O0000000000OO .quantifiers .get (O00O0O0OO00O0OOO0 )<=OO00O0OO00OO0OO00 *1.0 /OO00O0000000000OO .data ["rows_count"])#line:633
                        if not (O0OOO0000O000OO0O ):#line:634
                            print (f"...optimization : base is {OO00O0OO00OO0OO00} for {OO00OO0O0000O0000['generated_string']}")#line:635
                OOO0OOO0OO00OOO00 =not (O0OOO0000O000OO0O )#line:636
            if (OO00OO0O0000O0000 ['cedent_type']=='ante')&(OO00OO0O0000O0000 ['defi'].get ('type')=='con'):#line:637
                OO00O0OO00OO0OO00 =bin (OOO00000OOOO0O0O0 ['ante']&OOO00000OOOO0O0O0 ['cond']).count ("1")#line:638
                O0OOO0000O000OO0O =True #line:639
                for O00O0O0OO00O0OOO0 in OO00O0000000000OO .quantifiers .keys ():#line:640
                    if O00O0O0OO00O0OOO0 =='Base':#line:641
                        O0OOO0000O000OO0O =O0OOO0000O000OO0O and (OO00O0000000000OO .quantifiers .get (O00O0O0OO00O0OOO0 )<=OO00O0OO00OO0OO00 )#line:642
                        if not (O0OOO0000O000OO0O ):#line:643
                            print (f"...optimization : ANTE: base is {OO00O0OO00OO0OO00} for {OO00OO0O0000O0000['generated_string']}")#line:644
                    if O00O0O0OO00O0OOO0 =='RelBase':#line:645
                        O0OOO0000O000OO0O =O0OOO0000O000OO0O and (OO00O0000000000OO .quantifiers .get (O00O0O0OO00O0OOO0 )<=OO00O0OO00OO0OO00 *1.0 /OO00O0000000000OO .data ["rows_count"])#line:646
                        if not (O0OOO0000O000OO0O ):#line:647
                            print (f"...optimization : ANTE:  base is {OO00O0OO00OO0OO00} for {OO00OO0O0000O0000['generated_string']}")#line:648
                OOO0OOO0OO00OOO00 =not (O0OOO0000O000OO0O )#line:649
            if (OO00OO0O0000O0000 ['cedent_type']=='succ')&(OO00OO0O0000O0000 ['defi'].get ('type')=='con'):#line:650
                OO00O0OO00OO0OO00 =bin (OOO00000OOOO0O0O0 ['ante']&OOO00000OOOO0O0O0 ['cond']&OOO00000OOOO0O0O0 ['succ']).count ("1")#line:651
                OOOO0OO00OOO0O0O0 =0 #line:652
                if OO00O0OO00OO0OO00 >0 :#line:653
                    OOOO0OO00OOO0O0O0 =bin (OOO00000OOOO0O0O0 ['ante']&OOO00000OOOO0O0O0 ['succ']&OOO00000OOOO0O0O0 ['cond']).count ("1")*1.0 /bin (OOO00000OOOO0O0O0 ['ante']&OOO00000OOOO0O0O0 ['cond']).count ("1")#line:654
                O00O000OOOOOOOO00 =1 <<OO00O0000000000OO .data ["rows_count"]#line:655
                OOOOOO00O0000OOOO =bin (OOO00000OOOO0O0O0 ['ante']&OOO00000OOOO0O0O0 ['succ']&OOO00000OOOO0O0O0 ['cond']).count ("1")#line:656
                O0O00OO000O0OO0O0 =bin (OOO00000OOOO0O0O0 ['ante']&~(O00O000OOOOOOOO00 |OOO00000OOOO0O0O0 ['succ'])&OOO00000OOOO0O0O0 ['cond']).count ("1")#line:657
                OOOO00O00OO0OO0OO =bin (~(O00O000OOOOOOOO00 |OOO00000OOOO0O0O0 ['ante'])&OOO00000OOOO0O0O0 ['succ']&OOO00000OOOO0O0O0 ['cond']).count ("1")#line:658
                OOOOOO0O0OOO0OO0O =bin (~(O00O000OOOOOOOO00 |OOO00000OOOO0O0O0 ['ante'])&~(O00O000OOOOOOOO00 |OOO00000OOOO0O0O0 ['succ'])&OOO00000OOOO0O0O0 ['cond']).count ("1")#line:659
                O0OOO0000O000OO0O =True #line:660
                for O00O0O0OO00O0OOO0 in OO00O0000000000OO .quantifiers .keys ():#line:661
                    if O00O0O0OO00O0OOO0 =='pim':#line:662
                        O0OOO0000O000OO0O =O0OOO0000O000OO0O and (OO00O0000000000OO .quantifiers .get (O00O0O0OO00O0OOO0 )<=OOOO0OO00OOO0O0O0 )#line:663
                    if not (O0OOO0000O000OO0O ):#line:664
                        print (f"...optimization : SUCC:  pim is {OOOO0OO00OOO0O0O0} for {OO00OO0O0000O0000['generated_string']}")#line:665
                    if O00O0O0OO00O0OOO0 =='aad':#line:667
                        if (OOOOOO00O0000OOOO +O0O00OO000O0OO0O0 )*(OOOOOO00O0000OOOO +OOOO00O00OO0OO0OO )>0 :#line:668
                            O0OOO0000O000OO0O =O0OOO0000O000OO0O and (OO00O0000000000OO .quantifiers .get (O00O0O0OO00O0OOO0 )<=OOOOOO00O0000OOOO *(OOOOOO00O0000OOOO +O0O00OO000O0OO0O0 +OOOO00O00OO0OO0OO +OOOOOO0O0OOO0OO0O )/(OOOOOO00O0000OOOO +O0O00OO000O0OO0O0 )/(OOOOOO00O0000OOOO +OOOO00O00OO0OO0OO )-1 )#line:669
                        else :#line:670
                            O0OOO0000O000OO0O =False #line:671
                        if not (O0OOO0000O000OO0O ):#line:672
                            O000OO0O0OOO000OO =OOOOOO00O0000OOOO *(OOOOOO00O0000OOOO +O0O00OO000O0OO0O0 +OOOO00O00OO0OO0OO +OOOOOO0O0OOO0OO0O )/(OOOOOO00O0000OOOO +O0O00OO000O0OO0O0 )/(OOOOOO00O0000OOOO +OOOO00O00OO0OO0OO )-1 #line:673
                            print (f"...optimization : SUCC:  aad is {O000OO0O0OOO000OO} for {OO00OO0O0000O0000['generated_string']}")#line:674
                    if O00O0O0OO00O0OOO0 =='bad':#line:675
                        if (OOOOOO00O0000OOOO +O0O00OO000O0OO0O0 )*(OOOOOO00O0000OOOO +OOOO00O00OO0OO0OO )>0 :#line:676
                            O0OOO0000O000OO0O =O0OOO0000O000OO0O and (OO00O0000000000OO .quantifiers .get (O00O0O0OO00O0OOO0 )<=1 -OOOOOO00O0000OOOO *(OOOOOO00O0000OOOO +O0O00OO000O0OO0O0 +OOOO00O00OO0OO0OO +OOOOOO0O0OOO0OO0O )/(OOOOOO00O0000OOOO +O0O00OO000O0OO0O0 )/(OOOOOO00O0000OOOO +OOOO00O00OO0OO0OO ))#line:677
                        else :#line:678
                            O0OOO0000O000OO0O =False #line:679
                        if not (O0OOO0000O000OO0O ):#line:680
                            OO000O00O00OOOO0O =1 -OOOOOO00O0000OOOO *(OOOOOO00O0000OOOO +O0O00OO000O0OO0O0 +OOOO00O00OO0OO0OO +OOOOOO0O0OOO0OO0O )/(OOOOOO00O0000OOOO +O0O00OO000O0OO0O0 )/(OOOOOO00O0000OOOO +OOOO00O00OO0OO0OO )#line:681
                            print (f"...optimization : SUCC:  bad is {OO000O00O00OOOO0O} for {OO00OO0O0000O0000['generated_string']}")#line:682
                OOO0OOO0OO00OOO00 =not (O0OOO0000O000OO0O )#line:683
        if (OOO0OOO0OO00OOO00 ):#line:684
            print (f"... OPTIMALIZATION - SKIPPING BRANCH at cedent {OO00OO0O0000O0000['cedent_type']}")#line:685
        return OOO0OOO0OO00OOO00 #line:686
    def _print (O000OO000OO0OO00O ,O0OOOO00O000OO0OO ,_OO00O0OO000O00O0O ,_O0O0OOOOOO0OO0O00 ):#line:689
        if (len (_OO00O0OO000O00O0O ))!=len (_O0O0OOOOOO0OO0O00 ):#line:690
            print ("DIFF IN LEN for following cedent : "+str (len (_OO00O0OO000O00O0O ))+" vs "+str (len (_O0O0OOOOOO0OO0O00 )))#line:691
            print ("trace cedent : "+str (_OO00O0OO000O00O0O )+", traces "+str (_O0O0OOOOOO0OO0O00 ))#line:692
        OO00OOO00O0OO0OOO =''#line:693
        for OO0O0OO0OO0O0O00O in range (len (_OO00O0OO000O00O0O )):#line:694
            OO0O0O00OOOO0OO00 =O000OO000OO0OO00O .data ["varname"].index (O0OOOO00O000OO0OO ['defi'].get ('attributes')[_OO00O0OO000O00O0O [OO0O0OO0OO0O0O00O ]].get ('name'))#line:695
            OO00OOO00O0OO0OOO =OO00OOO00O0OO0OOO +O000OO000OO0OO00O .data ["varname"][OO0O0O00OOOO0OO00 ]+'('#line:697
            for OO0O000O0OOO00O0O in _O0O0OOOOOO0OO0O00 [OO0O0OO0OO0O0O00O ]:#line:698
                OO00OOO00O0OO0OOO =OO00OOO00O0OO0OOO +O000OO000OO0OO00O .data ["catnames"][OO0O0O00OOOO0OO00 ][OO0O000O0OOO00O0O ]+" "#line:699
            OO00OOO00O0OO0OOO =OO00OOO00O0OO0OOO +')'#line:700
            if OO0O0OO0OO0O0O00O +1 <len (_OO00O0OO000O00O0O ):#line:701
                OO00OOO00O0OO0OOO =OO00OOO00O0OO0OOO +' & '#line:702
        return OO00OOO00O0OO0OOO #line:706
    def _print_hypo (OO00OOOOO0O0OOO0O ,O00000OOO0OO00OOO ):#line:708
        print ('Hypothesis info : '+str (O00000OOO0OO00OOO ['params']))#line:709
        for OO0O00O0OOO0O000O in OO00OOOOO0O0OOO0O .task_actinfo ['cedents']:#line:710
            print (OO0O00O0OOO0O000O ['cedent_type']+' = '+OO0O00O0OOO0O000O ['generated_string'])#line:711
    def _genvar (O0O00OOO00OO0OO0O ,O0O0OOOO00O00OO00 ,OOOO0OOO0O0000O0O ,_O0000OOOO000OOO00 ,_O00O000OO0OOO0OO0 ,_O0OO00000000OOOOO ,_OOOO0OO0O0O00OOOO ,_O0O00O000O00OOOO0 ):#line:713
        for OO0O00OO00O00O0OO in range (OOOO0OOO0O0000O0O ['num_cedent']):#line:714
            if len (_O0000OOOO000OOO00 )==0 or OO0O00OO00O00O0OO >_O0000OOOO000OOO00 [-1 ]:#line:715
                _O0000OOOO000OOO00 .append (OO0O00OO00O00O0OO )#line:716
                OO00OO0OO0O00O0OO =O0O00OOO00OO0OO0O .data ["varname"].index (OOOO0OOO0O0000O0O ['defi'].get ('attributes')[OO0O00OO00O00O0OO ].get ('name'))#line:717
                _OOO0OOO00OOO00000 =OOOO0OOO0O0000O0O ['defi'].get ('attributes')[OO0O00OO00O00O0OO ].get ('minlen')#line:718
                _O0O000O00O0000O0O =OOOO0OOO0O0000O0O ['defi'].get ('attributes')[OO0O00OO00O00O0OO ].get ('maxlen')#line:719
                _O0OOOOOO00000O0OO =OOOO0OOO0O0000O0O ['defi'].get ('attributes')[OO0O00OO00O00O0OO ].get ('type')#line:720
                O0O0O0000OO0O0OO0 =len (O0O00OOO00OO0OO0O .data ["dm"][OO00OO0OO0O00O0OO ])#line:721
                _OO0000000OO000OOO =[]#line:722
                _O00O000OO0OOO0OO0 .append (_OO0000000OO000OOO )#line:723
                _O0O0O00O0O0O0O0OO =int (0 )#line:724
                O0O00OOO00OO0OO0O ._gencomb (O0O0OOOO00O00OO00 ,OOOO0OOO0O0000O0O ,_O0000OOOO000OOO00 ,_O00O000OO0OOO0OO0 ,_OO0000000OO000OOO ,_O0OO00000000OOOOO ,_O0O0O00O0O0O0O0OO ,O0O0O0000OO0O0OO0 ,_O0OOOOOO00000O0OO ,_OOOO0OO0O0O00OOOO ,_O0O00O000O00OOOO0 ,_OOO0OOO00OOO00000 ,_O0O000O00O0000O0O )#line:725
                _O00O000OO0OOO0OO0 .pop ()#line:726
                _O0000OOOO000OOO00 .pop ()#line:727
    def _gencomb (O0OO00O0OOO0O0000 ,OOO0O00OO00OO00O0 ,O00000O0O00OOO0O0 ,_O00O0O0OO00000000 ,_OOO00O0O0OOO0000O ,_OO00000O000OOO000 ,_OOOOOOOOO00OO0O00 ,_OO00OOOOO0O0O0OOO ,O0OOOOO0O0O0OO00O ,_O000OOOOOO000000O ,_OO0OO0O000O000OOO ,_O00OO0OO0O00O0O00 ,_OO00O000OOOO00000 ,_OO0O000O0000O0OO0 ):#line:729
        _O0O000O0OOOOO00OO =[]#line:730
        if _O000OOOOOO000000O =="subset":#line:731
            if len (_OO00000O000OOO000 )==0 :#line:732
                _O0O000O0OOOOO00OO =range (O0OOOOO0O0O0OO00O )#line:733
            else :#line:734
                _O0O000O0OOOOO00OO =range (_OO00000O000OOO000 [-1 ]+1 ,O0OOOOO0O0O0OO00O )#line:735
        elif _O000OOOOOO000000O =="seq":#line:736
            if len (_OO00000O000OOO000 )==0 :#line:737
                _O0O000O0OOOOO00OO =range (O0OOOOO0O0O0OO00O -_OO00O000OOOO00000 +1 )#line:738
            else :#line:739
                if _OO00000O000OOO000 [-1 ]+1 ==O0OOOOO0O0O0OO00O :#line:740
                    return #line:741
                OOOOOOO0O0OOO0O00 =_OO00000O000OOO000 [-1 ]+1 #line:742
                _O0O000O0OOOOO00OO .append (OOOOOOO0O0OOO0O00 )#line:743
        elif _O000OOOOOO000000O =="lcut":#line:744
            if len (_OO00000O000OOO000 )==0 :#line:745
                OOOOOOO0O0OOO0O00 =0 ;#line:746
            else :#line:747
                if _OO00000O000OOO000 [-1 ]+1 ==O0OOOOO0O0O0OO00O :#line:748
                    return #line:749
                OOOOOOO0O0OOO0O00 =_OO00000O000OOO000 [-1 ]+1 #line:750
            _O0O000O0OOOOO00OO .append (OOOOOOO0O0OOO0O00 )#line:751
        elif _O000OOOOOO000000O =="rcut":#line:752
            if len (_OO00000O000OOO000 )==0 :#line:753
                OOOOOOO0O0OOO0O00 =O0OOOOO0O0O0OO00O -1 ;#line:754
            else :#line:755
                if _OO00000O000OOO000 [-1 ]==0 :#line:756
                    return #line:757
                OOOOOOO0O0OOO0O00 =_OO00000O000OOO000 [-1 ]-1 #line:758
            _O0O000O0OOOOO00OO .append (OOOOOOO0O0OOO0O00 )#line:760
        else :#line:761
            print ("Attribute type "+_O000OOOOOO000000O +" not supported.")#line:762
            return #line:763
        for O000O00000OOOO0OO in _O0O000O0OOOOO00OO :#line:766
                _OO00000O000OOO000 .append (O000O00000OOOO0OO )#line:768
                _OOO00O0O0OOO0000O .pop ()#line:769
                _OOO00O0O0OOO0000O .append (_OO00000O000OOO000 )#line:770
                _O0O0000OOOOO00000 =_OO00OOOOO0O0O0OOO |O0OO00O0OOO0O0000 .data ["dm"][O0OO00O0OOO0O0000 .data ["varname"].index (O00000O0O00OOO0O0 ['defi'].get ('attributes')[_O00O0O0OO00000000 [-1 ]].get ('name'))][O000O00000OOOO0OO ]#line:774
                _O0O0OO0OOOO0O00O0 =1 #line:776
                if (len (_O00O0O0OO00000000 )<_OO0OO0O000O000OOO ):#line:777
                    _O0O0OO0OOOO0O00O0 =0 #line:778
                if (len (_OOO00O0O0OOO0000O [-1 ])>=_OO00O000OOOO00000 ):#line:779
                    _OO00O000OO000O000 =0 #line:780
                    if O00000O0O00OOO0O0 ['defi'].get ('type')=='con':#line:781
                        _OO00O000OO000O000 =_OOOOOOOOO00OO0O00 &_O0O0000OOOOO00000 #line:782
                    else :#line:783
                        _OO00O000OO000O000 =_OOOOOOOOO00OO0O00 |_O0O0000OOOOO00000 #line:784
                    O00000O0O00OOO0O0 ['trace_cedent']=_O00O0O0OO00000000 #line:785
                    O00000O0O00OOO0O0 ['traces']=_OOO00O0O0OOO0000O #line:786
                    O00000O0O00OOO0O0 ['generated_string']=O0OO00O0OOO0O0000 ._print (O00000O0O00OOO0O0 ,_O00O0O0OO00000000 ,_OOO00O0O0OOO0000O )#line:787
                    O00000O0O00OOO0O0 ['filter_value']=_OO00O000OO000O000 #line:788
                    OOO0O00OO00OO00O0 ['cedents'].append (O00000O0O00OOO0O0 )#line:789
                    O000OO0O0O00000OO =O0OO00O0OOO0O0000 ._verify_opt (OOO0O00OO00OO00O0 ,O00000O0O00OOO0O0 )#line:790
                    if not (O000OO0O0O00000OO ):#line:791
                        if _O0O0OO0OOOO0O00O0 ==1 :#line:792
                            if len (OOO0O00OO00OO00O0 ['cedents_to_do'])==len (OOO0O00OO00OO00O0 ['cedents']):#line:793
                                if O0OO00O0OOO0O0000 .proc =='CFMiner':#line:794
                                    O000000OOO00OOO00 ,OOOO0OOO0O0O00OOO =O0OO00O0OOO0O0000 ._verifyCF (_OO00O000OO000O000 )#line:795
                                elif O0OO00O0OOO0O0000 .proc =='4ftMiner':#line:796
                                    O000000OOO00OOO00 ,OOOO0OOO0O0O00OOO =O0OO00O0OOO0O0000 ._verify4ft (_O0O0000OOOOO00000 )#line:797
                                elif O0OO00O0OOO0O0000 .proc =='SD4ftMiner':#line:798
                                    O000000OOO00OOO00 ,OOOO0OOO0O0O00OOO =O0OO00O0OOO0O0000 ._verifysd4ft (_O0O0000OOOOO00000 )#line:799
                                elif O0OO00O0OOO0O0000 .proc =='NewAct4ftMiner':#line:800
                                    O000000OOO00OOO00 ,OOOO0OOO0O0O00OOO =O0OO00O0OOO0O0000 ._verifynewact4ft (_O0O0000OOOOO00000 )#line:801
                                elif O0OO00O0OOO0O0000 .proc =='Act4ftMiner':#line:802
                                    O000000OOO00OOO00 ,OOOO0OOO0O0O00OOO =O0OO00O0OOO0O0000 ._verifyact4ft (_O0O0000OOOOO00000 )#line:803
                                else :#line:804
                                    print ("Unsupported procedure : "+O0OO00O0OOO0O0000 .proc )#line:805
                                    exit (0 )#line:806
                                if O000000OOO00OOO00 ==True :#line:807
                                    O000OO000OOOOOO00 ={}#line:808
                                    O000OO000OOOOOO00 ["hypo_id"]=O0OO00O0OOO0O0000 .stats ['total_valid']#line:809
                                    O000OO000OOOOOO00 ["cedents"]={}#line:810
                                    for O0O00O0000OOO000O in OOO0O00OO00OO00O0 ['cedents']:#line:811
                                        O000OO000OOOOOO00 ['cedents'][O0O00O0000OOO000O ['cedent_type']]=O0O00O0000OOO000O ['generated_string']#line:812
                                    O000OO000OOOOOO00 ["params"]=OOOO0OOO0O0O00OOO #line:814
                                    O000OO000OOOOOO00 ["trace_cedent"]=_O00O0O0OO00000000 #line:815
                                    O0OO00O0OOO0O0000 ._print_hypo (O000OO000OOOOOO00 )#line:816
                                    O000OO000OOOOOO00 ["traces"]=_OOO00O0O0OOO0000O #line:819
                                    O0OO00O0OOO0O0000 .hypolist .append (O000OO000OOOOOO00 )#line:820
                            else :#line:821
                                O0OO00O0OOO0O0000 ._start_cedent (OOO0O00OO00OO00O0 )#line:822
                            OOO0O00OO00OO00O0 ['cedents'].pop ()#line:823
                        if (len (_O00O0O0OO00000000 )<_O00OO0OO0O00O0O00 ):#line:824
                            O0OO00O0OOO0O0000 ._genvar (OOO0O00OO00OO00O0 ,O00000O0O00OOO0O0 ,_O00O0O0OO00000000 ,_OOO00O0O0OOO0000O ,_OO00O000OO000O000 ,_OO0OO0O000O000OOO ,_O00OO0OO0O00O0O00 )#line:825
                    else :#line:826
                        OOO0O00OO00OO00O0 ['cedents'].pop ()#line:827
                O0OO00O0OOO0O0000 .stats ['total_cnt']+=1 #line:828
                if len (_OO00000O000OOO000 )<_OO0O000O0000O0OO0 :#line:829
                    O0OO00O0OOO0O0000 ._gencomb (OOO0O00OO00OO00O0 ,O00000O0O00OOO0O0 ,_O00O0O0OO00000000 ,_OOO00O0O0OOO0000O ,_OO00000O000OOO000 ,_OOOOOOOOO00OO0O00 ,_O0O0000OOOOO00000 ,O0OOOOO0O0O0OO00O ,_O000OOOOOO000000O ,_OO0OO0O000O000OOO ,_O00OO0OO0O00O0O00 ,_OO00O000OOOO00000 ,_OO0O000O0000O0OO0 )#line:830
                _OO00000O000OOO000 .pop ()#line:831
    def _start_cedent (OOOOOO0O0O0OOO00O ,OO0000O0O0O0OO00O ):#line:833
        if len (OO0000O0O0O0OO00O ['cedents_to_do'])>len (OO0000O0O0O0OO00O ['cedents']):#line:834
            _O0000000000OOO00O =[]#line:835
            _OO0OO0OO00O0000O0 =[]#line:836
            O0OO00O00000000O0 ={}#line:837
            O0OO00O00000000O0 ['cedent_type']=OO0000O0O0O0OO00O ['cedents_to_do'][len (OO0000O0O0O0OO00O ['cedents'])]#line:838
            O0OOO00O0OO00O00O =O0OO00O00000000O0 ['cedent_type']#line:839
            if ((O0OOO00O0OO00O00O [-1 ]=='-')|(O0OOO00O0OO00O00O [-1 ]=='+')):#line:840
                O0OOO00O0OO00O00O =O0OOO00O0OO00O00O [:-1 ]#line:841
            O0OO00O00000000O0 ['defi']=OOOOOO0O0O0OOO00O .kwargs .get (O0OOO00O0OO00O00O )#line:843
            if (O0OO00O00000000O0 ['defi']==None ):#line:844
                print ("Error getting cedent ",O0OO00O00000000O0 ['cedent_type'])#line:845
            _O00O00O000OOO0O00 =int (0 )#line:846
            O0OO00O00000000O0 ['num_cedent']=len (O0OO00O00000000O0 ['defi'].get ('attributes'))#line:851
            if (O0OO00O00000000O0 ['defi'].get ('type')=='con'):#line:852
                _O00O00O000OOO0O00 =(1 <<OOOOOO0O0O0OOO00O .data ["rows_count"])-1 #line:853
            OOOOOO0O0O0OOO00O ._genvar (OO0000O0O0O0OO00O ,O0OO00O00000000O0 ,_O0000000000OOO00O ,_OO0OO0OO00O0000O0 ,_O00O00O000OOO0O00 ,O0OO00O00000000O0 ['defi'].get ('minlen'),O0OO00O00000000O0 ['defi'].get ('maxlen'))#line:854
    def _calc_all (OO0OO0000O0O00000 ,**O00O0O0O0O0OOOOOO ):#line:857
        OO0OO0000O0O00000 ._prep_data (OO0OO0000O0O00000 .kwargs .get ("df"))#line:858
        OO0OO0000O0O00000 ._calculate (**O00O0O0O0O0OOOOOO )#line:859
    def _check_cedents (O0OOO00OO000OO0OO ,O0OO000000OOOO0OO ,**OOOO0O0O0OO0OO00O ):#line:861
        OOOO00OO0OOO0OO0O =True #line:862
        if (OOOO0O0O0OO0OO00O .get ('quantifiers',None )==None ):#line:863
            print (f"Error: missing quantifiers.")#line:864
            OOOO00OO0OOO0OO0O =False #line:865
            return OOOO00OO0OOO0OO0O #line:866
        if (type (OOOO0O0O0OO0OO00O .get ('quantifiers'))!=dict ):#line:867
            print (f"Error: quantifiers are not dictionary type.")#line:868
            OOOO00OO0OOO0OO0O =False #line:869
            return OOOO00OO0OOO0OO0O #line:870
        for OOO0000OOO000O0OO in O0OO000000OOOO0OO :#line:872
            if (OOOO0O0O0OO0OO00O .get (OOO0000OOO000O0OO ,None )==None ):#line:873
                print (f"Error: cedent {OOO0000OOO000O0OO} is missing in parameters.")#line:874
                OOOO00OO0OOO0OO0O =False #line:875
                return OOOO00OO0OOO0OO0O #line:876
            O0OO00OOOO000000O =OOOO0O0O0OO0OO00O .get (OOO0000OOO000O0OO )#line:877
            if (O0OO00OOOO000000O .get ('minlen'),None )==None :#line:878
                print (f"Error: cedent {OOO0000OOO000O0OO} has no minimal length specified.")#line:879
                OOOO00OO0OOO0OO0O =False #line:880
                return OOOO00OO0OOO0OO0O #line:881
            if not (type (O0OO00OOOO000000O .get ('minlen'))is int ):#line:882
                print (f"Error: cedent {OOO0000OOO000O0OO} has invalid type of minimal length ({type(O0OO00OOOO000000O.get('minlen'))}).")#line:883
                OOOO00OO0OOO0OO0O =False #line:884
                return OOOO00OO0OOO0OO0O #line:885
            if (O0OO00OOOO000000O .get ('maxlen'),None )==None :#line:886
                print (f"Error: cedent {OOO0000OOO000O0OO} has no maximal length specified.")#line:887
                OOOO00OO0OOO0OO0O =False #line:888
                return OOOO00OO0OOO0OO0O #line:889
            if not (type (O0OO00OOOO000000O .get ('maxlen'))is int ):#line:890
                print (f"Error: cedent {OOO0000OOO000O0OO} has invalid type of maximal length.")#line:891
                OOOO00OO0OOO0OO0O =False #line:892
                return OOOO00OO0OOO0OO0O #line:893
            if (O0OO00OOOO000000O .get ('type'),None )==None :#line:894
                print (f"Error: cedent {OOO0000OOO000O0OO} has no type specified.")#line:895
                OOOO00OO0OOO0OO0O =False #line:896
                return OOOO00OO0OOO0OO0O #line:897
            if not ((O0OO00OOOO000000O .get ('type'))in (['con','dis'])):#line:898
                print (f"Error: cedent {OOO0000OOO000O0OO} has invalid type. Allowed values are 'con' and 'dis'.")#line:899
                OOOO00OO0OOO0OO0O =False #line:900
                return OOOO00OO0OOO0OO0O #line:901
            if (O0OO00OOOO000000O .get ('attributes'),None )==None :#line:902
                print (f"Error: cedent {OOO0000OOO000O0OO} has no attributes specified.")#line:903
                OOOO00OO0OOO0OO0O =False #line:904
                return OOOO00OO0OOO0OO0O #line:905
            for OOO0OOO0O000O000O in O0OO00OOOO000000O .get ('attributes'):#line:906
                if (OOO0OOO0O000O000O .get ('name'),None )==None :#line:907
                    print (f"Error: cedent {OOO0000OOO000O0OO} / attribute {OOO0OOO0O000O000O} has no 'name' attribute specified.")#line:908
                    OOOO00OO0OOO0OO0O =False #line:909
                    return OOOO00OO0OOO0OO0O #line:910
                if not ((OOO0OOO0O000O000O .get ('name'))in O0OOO00OO000OO0OO .data ["varname"]):#line:911
                    print (f"Error: cedent {OOO0000OOO000O0OO} / attribute {OOO0OOO0O000O000O.get('name')} not in variable list. Please check spelling.")#line:912
                    OOOO00OO0OOO0OO0O =False #line:913
                    return OOOO00OO0OOO0OO0O #line:914
                if (OOO0OOO0O000O000O .get ('type'),None )==None :#line:915
                    print (f"Error: cedent {OOO0000OOO000O0OO} / attribute {OOO0OOO0O000O000O.get('name')} has no 'type' attribute specified.")#line:916
                    OOOO00OO0OOO0OO0O =False #line:917
                    return OOOO00OO0OOO0OO0O #line:918
                if not ((OOO0OOO0O000O000O .get ('type'))in (['rcut','lcut','seq','subset'])):#line:919
                    print (f"Error: cedent {OOO0000OOO000O0OO} / attribute {OOO0OOO0O000O000O.get('name')} has unsupported type {OOO0OOO0O000O000O.get('type')}. Supported types are 'subset','seq','lcut','rcut'.")#line:920
                    OOOO00OO0OOO0OO0O =False #line:921
                    return OOOO00OO0OOO0OO0O #line:922
                if (OOO0OOO0O000O000O .get ('minlen'),None )==None :#line:923
                    print (f"Error: cedent {OOO0000OOO000O0OO} / attribute {OOO0OOO0O000O000O.get('name')} has no minimal length specified.")#line:924
                    OOOO00OO0OOO0OO0O =False #line:925
                    return OOOO00OO0OOO0OO0O #line:926
                if not (type (OOO0OOO0O000O000O .get ('minlen'))is int ):#line:927
                    print (f"Error: cedent {OOO0000OOO000O0OO} / attribute {OOO0OOO0O000O000O.get('name')} has invalid type of minimal length.")#line:928
                    OOOO00OO0OOO0OO0O =False #line:929
                    return OOOO00OO0OOO0OO0O #line:930
                if (OOO0OOO0O000O000O .get ('maxlen'),None )==None :#line:931
                    print (f"Error: cedent {OOO0000OOO000O0OO} / attribute {OOO0OOO0O000O000O.get('name')} has no maximal length specified.")#line:932
                    OOOO00OO0OOO0OO0O =False #line:933
                    return OOOO00OO0OOO0OO0O #line:934
                if not (type (OOO0OOO0O000O000O .get ('maxlen'))is int ):#line:935
                    print (f"Error: cedent {OOO0000OOO000O0OO} / attribute {OOO0OOO0O000O000O.get('name')} has invalid type of maximal length.")#line:936
                    OOOO00OO0OOO0OO0O =False #line:937
                    return OOOO00OO0OOO0OO0O #line:938
        return OOOO00OO0OOO0OO0O #line:939
    def _calculate (OOOOO0O0OOOOOO000 ,**O0OOOO000O000O00O ):#line:941
        if OOOOO0O0OOOOOO000 .data ["data_prepared"]==0 :#line:942
            print ("Error: data not prepared")#line:943
            return #line:944
        OOOOO0O0OOOOOO000 .kwargs =O0OOOO000O000O00O #line:945
        OOOOO0O0OOOOOO000 .proc =O0OOOO000O000O00O .get ('proc')#line:946
        OOOOO0O0OOOOOO000 .quantifiers =O0OOOO000O000O00O .get ('quantifiers')#line:947
        OOOOO0O0OOOOOO000 ._init_task ()#line:949
        OOOOO0O0OOOOOO000 .stats ['start_proc_time']=time .time ()#line:950
        OOOOO0O0OOOOOO000 .task_actinfo ['cedents_to_do']=[]#line:951
        OOOOO0O0OOOOOO000 .task_actinfo ['cedents']=[]#line:952
        if O0OOOO000O000O00O .get ("proc")=='CFMiner':#line:955
            OOOOO0O0OOOOOO000 .task_actinfo ['cedents_to_do']=['cond']#line:956
            if O0OOOO000O000O00O .get ('target',None )==None :#line:957
                print ("ERROR: no target variable defined for CF Miner")#line:958
                return #line:959
            if not (OOOOO0O0OOOOOO000 ._check_cedents (['cond'],**O0OOOO000O000O00O )):#line:960
                return #line:961
            if not (O0OOOO000O000O00O .get ('target')in OOOOO0O0OOOOOO000 .data ["varname"]):#line:962
                print ("ERROR: target parameter is not variable. Please check spelling of variable name in parameter 'target'.")#line:963
                return #line:964
        elif O0OOOO000O000O00O .get ("proc")=='4ftMiner':#line:966
            if not (OOOOO0O0OOOOOO000 ._check_cedents (['ante','succ'],**O0OOOO000O000O00O )):#line:967
                return #line:968
            _O0O0O0OO0OOOOO000 =O0OOOO000O000O00O .get ("cond")#line:970
            if _O0O0O0OO0OOOOO000 !=None :#line:971
                OOOOO0O0OOOOOO000 .task_actinfo ['cedents_to_do'].append ('cond')#line:972
            else :#line:973
                OO000000OO0OOO000 =OOOOO0O0OOOOOO000 .cedent #line:974
                OO000000OO0OOO000 ['cedent_type']='cond'#line:975
                OO000000OO0OOO000 ['filter_value']=(1 <<OOOOO0O0OOOOOO000 .data ["rows_count"])-1 #line:976
                OO000000OO0OOO000 ['generated_string']='---'#line:977
                OOOOO0O0OOOOOO000 .task_actinfo ['cedents_to_do'].append ('cond')#line:979
                OOOOO0O0OOOOOO000 .task_actinfo ['cedents'].append (OO000000OO0OOO000 )#line:980
            OOOOO0O0OOOOOO000 .task_actinfo ['cedents_to_do'].append ('ante')#line:984
            OOOOO0O0OOOOOO000 .task_actinfo ['cedents_to_do'].append ('succ')#line:985
        elif O0OOOO000O000O00O .get ("proc")=='NewAct4ftMiner':#line:986
            _O0O0O0OO0OOOOO000 =O0OOOO000O000O00O .get ("cond")#line:989
            if _O0O0O0OO0OOOOO000 !=None :#line:990
                OOOOO0O0OOOOOO000 .task_actinfo ['cedents_to_do'].append ('cond')#line:991
            else :#line:992
                OO000000OO0OOO000 =OOOOO0O0OOOOOO000 .cedent #line:993
                OO000000OO0OOO000 ['cedent_type']='cond'#line:994
                OO000000OO0OOO000 ['filter_value']=(1 <<OOOOO0O0OOOOOO000 .data ["rows_count"])-1 #line:995
                OO000000OO0OOO000 ['generated_string']='---'#line:996
                print (OO000000OO0OOO000 ['filter_value'])#line:997
                OOOOO0O0OOOOOO000 .task_actinfo ['cedents_to_do'].append ('cond')#line:998
                OOOOO0O0OOOOOO000 .task_actinfo ['cedents'].append (OO000000OO0OOO000 )#line:999
            OOOOO0O0OOOOOO000 .task_actinfo ['cedents_to_do'].append ('antv')#line:1000
            OOOOO0O0OOOOOO000 .task_actinfo ['cedents_to_do'].append ('sucv')#line:1001
            OOOOO0O0OOOOOO000 .task_actinfo ['cedents_to_do'].append ('ante')#line:1002
            OOOOO0O0OOOOOO000 .task_actinfo ['cedents_to_do'].append ('succ')#line:1003
        elif O0OOOO000O000O00O .get ("proc")=='Act4ftMiner':#line:1004
            _O0O0O0OO0OOOOO000 =O0OOOO000O000O00O .get ("cond")#line:1007
            if _O0O0O0OO0OOOOO000 !=None :#line:1008
                OOOOO0O0OOOOOO000 .task_actinfo ['cedents_to_do'].append ('cond')#line:1009
            else :#line:1010
                OO000000OO0OOO000 =OOOOO0O0OOOOOO000 .cedent #line:1011
                OO000000OO0OOO000 ['cedent_type']='cond'#line:1012
                OO000000OO0OOO000 ['filter_value']=(1 <<OOOOO0O0OOOOOO000 .data ["rows_count"])-1 #line:1013
                OO000000OO0OOO000 ['generated_string']='---'#line:1014
                print (OO000000OO0OOO000 ['filter_value'])#line:1015
                OOOOO0O0OOOOOO000 .task_actinfo ['cedents_to_do'].append ('cond')#line:1016
                OOOOO0O0OOOOOO000 .task_actinfo ['cedents'].append (OO000000OO0OOO000 )#line:1017
            OOOOO0O0OOOOOO000 .task_actinfo ['cedents_to_do'].append ('antv-')#line:1018
            OOOOO0O0OOOOOO000 .task_actinfo ['cedents_to_do'].append ('antv+')#line:1019
            OOOOO0O0OOOOOO000 .task_actinfo ['cedents_to_do'].append ('sucv-')#line:1020
            OOOOO0O0OOOOOO000 .task_actinfo ['cedents_to_do'].append ('sucv+')#line:1021
            OOOOO0O0OOOOOO000 .task_actinfo ['cedents_to_do'].append ('ante')#line:1022
            OOOOO0O0OOOOOO000 .task_actinfo ['cedents_to_do'].append ('succ')#line:1023
        elif O0OOOO000O000O00O .get ("proc")=='SD4ftMiner':#line:1024
            if not (OOOOO0O0OOOOOO000 ._check_cedents (['ante','succ','frst','scnd'],**O0OOOO000O000O00O )):#line:1027
                return #line:1028
            _O0O0O0OO0OOOOO000 =O0OOOO000O000O00O .get ("cond")#line:1029
            if _O0O0O0OO0OOOOO000 !=None :#line:1030
                OOOOO0O0OOOOOO000 .task_actinfo ['cedents_to_do'].append ('cond')#line:1031
            else :#line:1032
                OO000000OO0OOO000 =OOOOO0O0OOOOOO000 .cedent #line:1033
                OO000000OO0OOO000 ['cedent_type']='cond'#line:1034
                OO000000OO0OOO000 ['filter_value']=(1 <<OOOOO0O0OOOOOO000 .data ["rows_count"])-1 #line:1035
                OO000000OO0OOO000 ['generated_string']='---'#line:1036
                print (OO000000OO0OOO000 ['filter_value'])#line:1037
                OOOOO0O0OOOOOO000 .task_actinfo ['cedents_to_do'].append ('cond')#line:1038
                OOOOO0O0OOOOOO000 .task_actinfo ['cedents'].append (OO000000OO0OOO000 )#line:1039
            OOOOO0O0OOOOOO000 .task_actinfo ['cedents_to_do'].append ('frst')#line:1040
            OOOOO0O0OOOOOO000 .task_actinfo ['cedents_to_do'].append ('scnd')#line:1041
            OOOOO0O0OOOOOO000 .task_actinfo ['cedents_to_do'].append ('ante')#line:1042
            OOOOO0O0OOOOOO000 .task_actinfo ['cedents_to_do'].append ('succ')#line:1043
        else :#line:1044
            print ("Unsupported procedure")#line:1045
            return #line:1046
        print ("Will go for ",O0OOOO000O000O00O .get ("proc"))#line:1047
        OOOOO0O0OOOOOO000 .task_actinfo ['optim']={}#line:1050
        OOOO000O000OOOO0O =True #line:1051
        for OOOO0OOO0OO00O000 in OOOOO0O0OOOOOO000 .task_actinfo ['cedents_to_do']:#line:1052
            try :#line:1053
                OO0000OOOO00O000O =OOOOO0O0OOOOOO000 .kwargs .get (OOOO0OOO0OO00O000 )#line:1054
                if OO0000OOOO00O000O .get ('type')!='con':#line:1057
                    OOOO000O000OOOO0O =False #line:1058
            except :#line:1059
                OO00OOO0O000O0O0O =1 <2 #line:1060
        OOOO00O0000000OO0 ={}#line:1061
        OOOO00O0000000OO0 ['only_con']=OOOO000O000OOOO0O #line:1062
        OOOOO0O0OOOOOO000 .task_actinfo ['optim']=OOOO00O0000000OO0 #line:1063
        print ("Starting to mine rules.")#line:1071
        OOOOO0O0OOOOOO000 ._start_cedent (OOOOO0O0OOOOOO000 .task_actinfo )#line:1072
        OOOOO0O0OOOOOO000 .stats ['end_proc_time']=time .time ()#line:1074
        print ("Done. Total verifications : "+str (OOOOO0O0OOOOOO000 .stats ['total_cnt'])+", hypotheses "+str (OOOOO0O0OOOOOO000 .stats ['total_valid'])+",control number:"+str (OOOOO0O0OOOOOO000 .stats ['control_number'])+", times: prep "+str (OOOOO0O0OOOOOO000 .stats ['end_prep_time']-OOOOO0O0OOOOOO000 .stats ['start_prep_time'])+", processing "+str (OOOOO0O0OOOOOO000 .stats ['end_proc_time']-OOOOO0O0OOOOOO000 .stats ['start_proc_time']))#line:1077
        OOO0000OO0OO0OO00 ={}#line:1078
        O00OOO0000O0O0OOO ={}#line:1079
        O00OOO0000O0O0OOO ["task_type"]=O0OOOO000O000O00O .get ('proc')#line:1080
        O00OOO0000O0O0OOO ["target"]=O0OOOO000O000O00O .get ('target')#line:1082
        O00OOO0000O0O0OOO ["self.quantifiers"]=OOOOO0O0OOOOOO000 .quantifiers #line:1083
        if O0OOOO000O000O00O .get ('cond')!=None :#line:1085
            O00OOO0000O0O0OOO ['cond']=O0OOOO000O000O00O .get ('cond')#line:1086
        if O0OOOO000O000O00O .get ('ante')!=None :#line:1087
            O00OOO0000O0O0OOO ['ante']=O0OOOO000O000O00O .get ('ante')#line:1088
        if O0OOOO000O000O00O .get ('succ')!=None :#line:1089
            O00OOO0000O0O0OOO ['succ']=O0OOOO000O000O00O .get ('succ')#line:1090
        OOO0000OO0OO0OO00 ["taskinfo"]=O00OOO0000O0O0OOO #line:1091
        O0O0O0OOOO0OOO0OO ={}#line:1092
        O0O0O0OOOO0OOO0OO ["total_verifications"]=OOOOO0O0OOOOOO000 .stats ['total_cnt']#line:1093
        O0O0O0OOOO0OOO0OO ["valid_hypotheses"]=OOOOO0O0OOOOOO000 .stats ['total_valid']#line:1094
        O0O0O0OOOO0OOO0OO ["time_prep"]=OOOOO0O0OOOOOO000 .stats ['end_prep_time']-OOOOO0O0OOOOOO000 .stats ['start_prep_time']#line:1095
        O0O0O0OOOO0OOO0OO ["time_processing"]=OOOOO0O0OOOOOO000 .stats ['end_proc_time']-OOOOO0O0OOOOOO000 .stats ['start_proc_time']#line:1096
        O0O0O0OOOO0OOO0OO ["time_total"]=OOOOO0O0OOOOOO000 .stats ['end_prep_time']-OOOOO0O0OOOOOO000 .stats ['start_prep_time']+OOOOO0O0OOOOOO000 .stats ['end_proc_time']-OOOOO0O0OOOOOO000 .stats ['start_proc_time']#line:1097
        OOO0000OO0OO0OO00 ["summary_statistics"]=O0O0O0OOOO0OOO0OO #line:1098
        OOO0000OO0OO0OO00 ["hypotheses"]=OOOOO0O0OOOOOO000 .hypolist #line:1099
        O00O00O0O00O000OO ={}#line:1100
        O00O00O0O00O000OO ["varname"]=OOOOO0O0OOOOOO000 .data ["varname"]#line:1101
        O00O00O0O00O000OO ["catnames"]=OOOOO0O0OOOOOO000 .data ["catnames"]#line:1102
        OOO0000OO0OO0OO00 ["datalabels"]=O00O00O0O00O000OO #line:1103
        OOOOO0O0OOOOOO000 .result =OOO0000OO0OO0OO00 #line:1105
