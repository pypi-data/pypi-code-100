import time #line:1
import pandas as pd #line:3
class cleverminer :#line:5
    version_string ="0.0.84"#line:7
    def __init__ (OO000O0O00000000O ,**O0OOOOOO0O0OO000O ):#line:9
        OO000O0O00000000O ._print_disclaimer ()#line:10
        OO000O0O00000000O .stats ={'total_cnt':0 ,'total_valid':0 ,'control_number':0 ,'start_prep_time':time .time (),'end_prep_time':time .time (),'start_proc_time':time .time (),'end_proc_time':time .time ()}#line:18
        OO000O0O00000000O ._init_data ()#line:19
        OO000O0O00000000O ._init_task ()#line:20
        if len (O0OOOOOO0O0OO000O )>0 :#line:21
            OO000O0O00000000O .kwargs =O0OOOOOO0O0OO000O #line:22
            OO000O0O00000000O ._calc_all (**O0OOOOOO0O0OO000O )#line:23
    def _init_data (OO0O00OO0000OO00O ):#line:25
        OO0O00OO0000OO00O .data ={}#line:27
        OO0O00OO0000OO00O .data ["varname"]=[]#line:28
        OO0O00OO0000OO00O .data ["catnames"]=[]#line:29
        OO0O00OO0000OO00O .data ["vtypes"]=[]#line:30
        OO0O00OO0000OO00O .data ["dm"]=[]#line:31
        OO0O00OO0000OO00O .data ["rows_count"]=int (0 )#line:32
        OO0O00OO0000OO00O .data ["data_prepared"]=0 #line:33
    def _init_task (OOOO00O0O0O00OO00 ):#line:35
        OOOO00O0O0O00OO00 .cedent ={'cedent_type':'none','defi':{},'num_cedent':0 ,'trace_cedent':[],'traces':[],'generated_string':'','filter_value':int (0 )}#line:44
        OOOO00O0O0O00OO00 .task_actinfo ={'proc':'','cedents_to_do':[],'cedents':[]}#line:48
        OOOO00O0O0O00OO00 .hypolist =[]#line:49
        OOOO00O0O0O00OO00 .stats ['total_cnt']=0 #line:51
        OOOO00O0O0O00OO00 .stats ['total_valid']=0 #line:52
        OOOO00O0O0O00OO00 .stats ['control_number']=0 #line:53
        OOOO00O0O0O00OO00 .result ={}#line:54
    def _get_ver (O00O0O000OOOO000O ):#line:56
        return O00O0O000OOOO000O .version_string #line:57
    def _print_disclaimer (O00OO000O00O0OO0O ):#line:59
        print ("***********************************************************************************************************************************************************************")#line:60
        print ("Cleverminer version ",O00OO000O00O0OO0O ._get_ver ())#line:61
        print ("IMPORTANT NOTE: this is preliminary development version of CleverMiner procedure. This procedure is under intensive development and early released for educational use,")#line:62
        print ("    so there is ABSOLUTELY no guarantee of results, possible gaps in functionality and no guarantee of keeping syntax and parameters as in current version.")#line:63
        print ("    (That means we need to tidy up and make proper design, input validation, documentation and instrumentation before launch)")#line:64
        print ("This version is for personal and educational use only.")#line:65
        print ("***********************************************************************************************************************************************************************")#line:66
    def _prep_data (OOOOOOOO0O0000OO0 ,O00O0OO0OO000OO0O ):#line:68
        print ("Starting data preparation ...")#line:69
        OOOOOOOO0O0000OO0 ._init_data ()#line:70
        OOOOOOOO0O0000OO0 .stats ['start_prep_time']=time .time ()#line:71
        OOOOOOOO0O0000OO0 .data ["rows_count"]=O00O0OO0OO000OO0O .shape [0 ]#line:72
        for OOOOO0OO0O00O0OOO in O00O0OO0OO000OO0O .select_dtypes (include =['object']).columns :#line:73
            O00O0OO0OO000OO0O [OOOOO0OO0O00O0OOO ]=O00O0OO0OO000OO0O [OOOOO0OO0O00O0OOO ].apply (str )#line:74
        O00000O000OO0OO0O =pd .DataFrame .from_records ([(O0O0O0O0000OO0O00 ,O00O0OO0OO000OO0O [O0O0O0O0000OO0O00 ].nunique ())for O0O0O0O0000OO0O00 in O00O0OO0OO000OO0O .columns ],columns =['Column_Name','Num_Unique']).sort_values (by =['Num_Unique'])#line:76
        print ("Unique value counts are:")#line:77
        print (O00000O000OO0OO0O )#line:78
        for OOOOO0OO0O00O0OOO in O00O0OO0OO000OO0O .columns :#line:79
            if O00O0OO0OO000OO0O [OOOOO0OO0O00O0OOO ].nunique ()<100 :#line:80
                O00O0OO0OO000OO0O [OOOOO0OO0O00O0OOO ]=O00O0OO0OO000OO0O [OOOOO0OO0O00O0OOO ].astype ('category')#line:81
            else :#line:82
                print (f"WARNING: attribute {OOOOO0OO0O00O0OOO} has more than 100 values, will be ignored.")#line:83
                del O00O0OO0OO000OO0O [OOOOO0OO0O00O0OOO ]#line:84
        OOOOOOO0OO00OOO00 =0 #line:85
        OOO00O0O000OOOOO0 =0 #line:86
        for O00000000O000OOOO in O00O0OO0OO000OO0O :#line:87
            print ('Column: '+O00000000O000OOOO )#line:89
            OOOOOOOO0O0000OO0 .data ["varname"].append (O00000000O000OOOO )#line:90
            O000OO0OO0O0O000O =pd .get_dummies (O00O0OO0OO000OO0O [O00000000O000OOOO ])#line:91
            OOO0000O0O0000O0O =0 #line:92
            if (O00O0OO0OO000OO0O .dtypes [O00000000O000OOOO ].name =='category'):#line:93
                OOO0000O0O0000O0O =1 #line:94
            OOOOOOOO0O0000OO0 .data ["vtypes"].append (OOO0000O0O0000O0O )#line:95
            OOOOO0OO0OOOO0000 =0 #line:98
            OO0OOOO0000O0OOO0 =[]#line:99
            O0OO00O00000OO0OO =[]#line:100
            for OOO000000OOO00OO0 in O000OO0OO0O0O000O :#line:102
                print ('....category : '+str (OOO000000OOO00OO0 )+" @ "+str (time .time ()))#line:104
                OO0OOOO0000O0OOO0 .append (OOO000000OOO00OO0 )#line:105
                O0O0O00OOOO0O00OO =int (0 )#line:106
                O00O0OOO000OOO00O =O000OO0OO0O0O000O [OOO000000OOO00OO0 ].values #line:107
                for O0OOO00OO00OO0O00 in range (OOOOOOOO0O0000OO0 .data ["rows_count"]):#line:109
                    if O00O0OOO000OOO00O [O0OOO00OO00OO0O00 ]>0 :#line:110
                        O0O0O00OOOO0O00OO +=1 <<O0OOO00OO00OO0O00 #line:111
                O0OO00O00000OO0OO .append (O0O0O00OOOO0O00OO )#line:112
                OOOOO0OO0OOOO0000 +=1 #line:122
                OOO00O0O000OOOOO0 +=1 #line:123
            OOOOOOOO0O0000OO0 .data ["catnames"].append (OO0OOOO0000O0OOO0 )#line:125
            OOOOOOOO0O0000OO0 .data ["dm"].append (O0OO00O00000OO0OO )#line:126
        print (OOOOOOOO0O0000OO0 .data ["varname"])#line:128
        print (OOOOOOOO0O0000OO0 .data ["catnames"])#line:129
        print (OOOOOOOO0O0000OO0 .data ["vtypes"])#line:130
        OOOOOOOO0O0000OO0 .data ["data_prepared"]=1 #line:132
        print ("Data preparation finished ...")#line:133
        print ('Number of variables : '+str (len (OOOOOOOO0O0000OO0 .data ["dm"])))#line:134
        print ('Total number of categories in all variables : '+str (OOO00O0O000OOOOO0 ))#line:135
        OOOOOOOO0O0000OO0 .stats ['end_prep_time']=time .time ()#line:136
        print ('Time needed for data preparation : ',str (OOOOOOOO0O0000OO0 .stats ['end_prep_time']-OOOOOOOO0O0000OO0 .stats ['start_prep_time']))#line:137
    def bitcount (OO0O00OOOO00OOOO0 ,O0O00OOOO0000OO00 ):#line:140
        OOOOO00OOOOOOO000 =0 #line:141
        while O0O00OOOO0000OO00 >0 :#line:142
            if (O0O00OOOO0000OO00 &1 ==1 ):OOOOO00OOOOOOO000 +=1 #line:143
            O0O00OOOO0000OO00 >>=1 #line:144
        return OOOOO00OOOOOOO000 #line:145
    def _verifyCF (O000OO00OOO00O0OO ,_OO0000O0OO0OO0OOO ):#line:148
        O0000O0OOOOOOO0OO =bin (_OO0000O0OO0OO0OOO ).count ("1")#line:149
        O0OO0O0O000OO0O0O =[]#line:150
        O0OO00O0O000OO00O =[]#line:151
        OOOO00O0O0O0O00OO =0 #line:152
        O00OOOO0O000O0O00 =0 #line:153
        OOOO00O00O000000O =0 #line:154
        O0OO0OOO0O00O00O0 =0 #line:155
        O00O00OO00O0O00O0 =0 #line:156
        OOOOO000O00O000O0 =0 #line:157
        OOO0000O0O0OO0000 =0 #line:158
        O000O0OOO0O0000O0 =0 #line:159
        O00O0O000OOO00OOO =0 #line:160
        OOO0OOO00O0OOO000 =O000OO00OOO00O0OO .data ["dm"][O000OO00OOO00O0OO .data ["varname"].index (O000OO00OOO00O0OO .kwargs .get ('target'))]#line:161
        for OO0OO0OO00O0OOOO0 in range (len (OOO0OOO00O0OOO000 )):#line:162
            O00OOOO0O000O0O00 =OOOO00O0O0O0O00OO #line:163
            OOOO00O0O0O0O00OO =bin (_OO0000O0OO0OO0OOO &OOO0OOO00O0OOO000 [OO0OO0OO00O0OOOO0 ]).count ("1")#line:164
            O0OO0O0O000OO0O0O .append (OOOO00O0O0O0O00OO )#line:165
            if OO0OO0OO00O0OOOO0 >0 :#line:166
                if (OOOO00O0O0O0O00OO >O00OOOO0O000O0O00 ):#line:167
                    if (OOOO00O00O000000O ==1 ):#line:168
                        O000O0OOO0O0000O0 +=1 #line:169
                    else :#line:170
                        O000O0OOO0O0000O0 =1 #line:171
                    if O000O0OOO0O0000O0 >O0OO0OOO0O00O00O0 :#line:172
                        O0OO0OOO0O00O00O0 =O000O0OOO0O0000O0 #line:173
                    OOOO00O00O000000O =1 #line:174
                    OOOOO000O00O000O0 +=1 #line:175
                if (OOOO00O0O0O0O00OO <O00OOOO0O000O0O00 ):#line:176
                    if (OOOO00O00O000000O ==-1 ):#line:177
                        O00O0O000OOO00OOO +=1 #line:178
                    else :#line:179
                        O00O0O000OOO00OOO =1 #line:180
                    if O00O0O000OOO00OOO >O00O00OO00O0O00O0 :#line:181
                        O00O00OO00O0O00O0 =O00O0O000OOO00OOO #line:182
                    OOOO00O00O000000O =-1 #line:183
                    OOO0000O0O0OO0000 +=1 #line:184
                if (OOOO00O0O0O0O00OO ==O00OOOO0O000O0O00 ):#line:185
                    OOOO00O00O000000O =0 #line:186
                    O00O0O000OOO00OOO =0 #line:187
                    O000O0OOO0O0000O0 =0 #line:188
        OO0000OOO0O00O00O =True #line:191
        for O000OOOOO0OOOO0OO in O000OO00OOO00O0OO .quantifiers .keys ():#line:192
            if O000OOOOO0OOOO0OO =='Base':#line:193
                OO0000OOO0O00O00O =OO0000OOO0O00O00O and (O000OO00OOO00O0OO .quantifiers .get (O000OOOOO0OOOO0OO )<=O0000O0OOOOOOO0OO )#line:194
            if O000OOOOO0OOOO0OO =='RelBase':#line:195
                OO0000OOO0O00O00O =OO0000OOO0O00O00O and (O000OO00OOO00O0OO .quantifiers .get (O000OOOOO0OOOO0OO )<=O0000O0OOOOOOO0OO *1.0 /O000OO00OOO00O0OO .data ["rows_count"])#line:196
            if O000OOOOO0OOOO0OO =='S_Up':#line:197
                OO0000OOO0O00O00O =OO0000OOO0O00O00O and (O000OO00OOO00O0OO .quantifiers .get (O000OOOOO0OOOO0OO )<=O0OO0OOO0O00O00O0 )#line:198
            if O000OOOOO0OOOO0OO =='S_Down':#line:199
                OO0000OOO0O00O00O =OO0000OOO0O00O00O and (O000OO00OOO00O0OO .quantifiers .get (O000OOOOO0OOOO0OO )<=O00O00OO00O0O00O0 )#line:200
            if O000OOOOO0OOOO0OO =='S_Any_Up':#line:201
                OO0000OOO0O00O00O =OO0000OOO0O00O00O and (O000OO00OOO00O0OO .quantifiers .get (O000OOOOO0OOOO0OO )<=O0OO0OOO0O00O00O0 )#line:202
            if O000OOOOO0OOOO0OO =='S_Any_Down':#line:203
                OO0000OOO0O00O00O =OO0000OOO0O00O00O and (O000OO00OOO00O0OO .quantifiers .get (O000OOOOO0OOOO0OO )<=O00O00OO00O0O00O0 )#line:204
            if O000OOOOO0OOOO0OO =='Max':#line:205
                OO0000OOO0O00O00O =OO0000OOO0O00O00O and (O000OO00OOO00O0OO .quantifiers .get (O000OOOOO0OOOO0OO )<=max (O0OO0O0O000OO0O0O ))#line:206
            if O000OOOOO0OOOO0OO =='Min':#line:207
                OO0000OOO0O00O00O =OO0000OOO0O00O00O and (O000OO00OOO00O0OO .quantifiers .get (O000OOOOO0OOOO0OO )<=min (O0OO0O0O000OO0O0O ))#line:208
            if O000OOOOO0OOOO0OO =='Relmax':#line:209
                OO0000OOO0O00O00O =OO0000OOO0O00O00O and (O000OO00OOO00O0OO .quantifiers .get (O000OOOOO0OOOO0OO )<=max (O0OO0O0O000OO0O0O )*1.0 /O000OO00OOO00O0OO .data ["rows_count"])#line:210
            if O000OOOOO0OOOO0OO =='Relmin':#line:211
                OO0000OOO0O00O00O =OO0000OOO0O00O00O and (O000OO00OOO00O0OO .quantifiers .get (O000OOOOO0OOOO0OO )<=min (O0OO0O0O000OO0O0O )*1.0 /O000OO00OOO00O0OO .data ["rows_count"])#line:212
        O00000O0O0OOOOOOO ={}#line:213
        if OO0000OOO0O00O00O ==True :#line:214
            O000OO00OOO00O0OO .stats ['total_valid']+=1 #line:216
            O00000O0O0OOOOOOO ["base"]=O0000O0OOOOOOO0OO #line:217
            O00000O0O0OOOOOOO ["rel_base"]=O0000O0OOOOOOO0OO *1.0 /O000OO00OOO00O0OO .data ["rows_count"]#line:218
            O00000O0O0OOOOOOO ["s_up"]=O0OO0OOO0O00O00O0 #line:219
            O00000O0O0OOOOOOO ["s_down"]=O00O00OO00O0O00O0 #line:220
            O00000O0O0OOOOOOO ["s_any_up"]=OOOOO000O00O000O0 #line:221
            O00000O0O0OOOOOOO ["s_any_down"]=OOO0000O0O0OO0000 #line:222
            O00000O0O0OOOOOOO ["max"]=max (O0OO0O0O000OO0O0O )#line:223
            O00000O0O0OOOOOOO ["min"]=min (O0OO0O0O000OO0O0O )#line:224
            O00000O0O0OOOOOOO ["rel_max"]=max (O0OO0O0O000OO0O0O )*1.0 /O000OO00OOO00O0OO .data ["rows_count"]#line:225
            O00000O0O0OOOOOOO ["rel_min"]=min (O0OO0O0O000OO0O0O )*1.0 /O000OO00OOO00O0OO .data ["rows_count"]#line:226
            O00000O0O0OOOOOOO ["hist"]=O0OO0O0O000OO0O0O #line:227
        return OO0000OOO0O00O00O ,O00000O0O0OOOOOOO #line:229
    def _verify4ft (OOO000O00O0OOO0O0 ,_OO0O0O0O0O0OOOOO0 ):#line:231
        OOOO0000O00O0OO00 ={}#line:232
        O0OO0OO000O00OOO0 =0 #line:233
        for OOOOOOO0OOOOO0O0O in OOO000O00O0OOO0O0 .task_actinfo ['cedents']:#line:234
            OOOO0000O00O0OO00 [OOOOOOO0OOOOO0O0O ['cedent_type']]=OOOOOOO0OOOOO0O0O ['filter_value']#line:236
            O0OO0OO000O00OOO0 =O0OO0OO000O00OOO0 +1 #line:237
        OOOO0O0OO00OO0OO0 =bin (OOOO0000O00O0OO00 ['ante']&OOOO0000O00O0OO00 ['succ']&OOOO0000O00O0OO00 ['cond']).count ("1")#line:239
        O00O0OOOO00OOOOOO =None #line:240
        O00O0OOOO00OOOOOO =0 #line:241
        if OOOO0O0OO00OO0OO0 >0 :#line:250
            O00O0OOOO00OOOOOO =bin (OOOO0000O00O0OO00 ['ante']&OOOO0000O00O0OO00 ['succ']&OOOO0000O00O0OO00 ['cond']).count ("1")*1.0 /bin (OOOO0000O00O0OO00 ['ante']&OOOO0000O00O0OO00 ['cond']).count ("1")#line:251
        O00O0000OOOOO0O0O =1 <<OOO000O00O0OOO0O0 .data ["rows_count"]#line:253
        OOOOO000OO0O00000 =bin (OOOO0000O00O0OO00 ['ante']&OOOO0000O00O0OO00 ['succ']&OOOO0000O00O0OO00 ['cond']).count ("1")#line:254
        OOO0000O0OO0OOOO0 =bin (OOOO0000O00O0OO00 ['ante']&~(O00O0000OOOOO0O0O |OOOO0000O00O0OO00 ['succ'])&OOOO0000O00O0OO00 ['cond']).count ("1")#line:255
        OOOOOOO0OOOOO0O0O =bin (~(O00O0000OOOOO0O0O |OOOO0000O00O0OO00 ['ante'])&OOOO0000O00O0OO00 ['succ']&OOOO0000O00O0OO00 ['cond']).count ("1")#line:256
        OOOO000O0O0O0O0OO =bin (~(O00O0000OOOOO0O0O |OOOO0000O00O0OO00 ['ante'])&~(O00O0000OOOOO0O0O |OOOO0000O00O0OO00 ['succ'])&OOOO0000O00O0OO00 ['cond']).count ("1")#line:257
        OO0O00O000O0OO0OO =0 #line:258
        if (OOOOO000OO0O00000 +OOO0000O0OO0OOOO0 )*(OOOOO000OO0O00000 +OOOOOOO0OOOOO0O0O )>0 :#line:259
            OO0O00O000O0OO0OO =OOOOO000OO0O00000 *(OOOOO000OO0O00000 +OOO0000O0OO0OOOO0 +OOOOOOO0OOOOO0O0O +OOOO000O0O0O0O0OO )/(OOOOO000OO0O00000 +OOO0000O0OO0OOOO0 )/(OOOOO000OO0O00000 +OOOOOOO0OOOOO0O0O )-1 #line:260
        else :#line:261
            OO0O00O000O0OO0OO =None #line:262
        O0OO0O00OO00O00OO =0 #line:263
        if (OOOOO000OO0O00000 +OOO0000O0OO0OOOO0 )*(OOOOO000OO0O00000 +OOOOOOO0OOOOO0O0O )>0 :#line:264
            O0OO0O00OO00O00OO =1 -OOOOO000OO0O00000 *(OOOOO000OO0O00000 +OOO0000O0OO0OOOO0 +OOOOOOO0OOOOO0O0O +OOOO000O0O0O0O0OO )/(OOOOO000OO0O00000 +OOO0000O0OO0OOOO0 )/(OOOOO000OO0O00000 +OOOOOOO0OOOOO0O0O )#line:265
        else :#line:266
            O0OO0O00OO00O00OO =None #line:267
        O0OOOO0OO0O0OOO0O =True #line:268
        for O00O00OO0000OOO00 in OOO000O00O0OOO0O0 .quantifiers .keys ():#line:269
            if O00O00OO0000OOO00 =='Base':#line:270
                O0OOOO0OO0O0OOO0O =O0OOOO0OO0O0OOO0O and (OOO000O00O0OOO0O0 .quantifiers .get (O00O00OO0000OOO00 )<=OOOO0O0OO00OO0OO0 )#line:271
            if O00O00OO0000OOO00 =='RelBase':#line:272
                O0OOOO0OO0O0OOO0O =O0OOOO0OO0O0OOO0O and (OOO000O00O0OOO0O0 .quantifiers .get (O00O00OO0000OOO00 )<=OOOO0O0OO00OO0OO0 *1.0 /OOO000O00O0OOO0O0 .data ["rows_count"])#line:273
            if O00O00OO0000OOO00 =='pim':#line:274
                O0OOOO0OO0O0OOO0O =O0OOOO0OO0O0OOO0O and (OOO000O00O0OOO0O0 .quantifiers .get (O00O00OO0000OOO00 )<=O00O0OOOO00OOOOOO )#line:275
            if O00O00OO0000OOO00 =='aad':#line:276
                if OO0O00O000O0OO0OO !=None :#line:277
                    O0OOOO0OO0O0OOO0O =O0OOOO0OO0O0OOO0O and (OOO000O00O0OOO0O0 .quantifiers .get (O00O00OO0000OOO00 )<=OO0O00O000O0OO0OO )#line:278
                else :#line:279
                    O0OOOO0OO0O0OOO0O =False #line:280
            if O00O00OO0000OOO00 =='bad':#line:281
                if O0OO0O00OO00O00OO !=None :#line:282
                    O0OOOO0OO0O0OOO0O =O0OOOO0OO0O0OOO0O and (OOO000O00O0OOO0O0 .quantifiers .get (O00O00OO0000OOO00 )<=O0OO0O00OO00O00OO )#line:283
                else :#line:284
                    O0OOOO0OO0O0OOO0O =False #line:285
            O00000O0000OO0OO0 ={}#line:286
        if O0OOOO0OO0O0OOO0O ==True :#line:287
            OOO000O00O0OOO0O0 .stats ['total_valid']+=1 #line:289
            O00000O0000OO0OO0 ["base"]=OOOO0O0OO00OO0OO0 #line:290
            O00000O0000OO0OO0 ["rel_base"]=OOOO0O0OO00OO0OO0 *1.0 /OOO000O00O0OOO0O0 .data ["rows_count"]#line:291
            O00000O0000OO0OO0 ["pim"]=O00O0OOOO00OOOOOO #line:292
            O00000O0000OO0OO0 ["aad"]=OO0O00O000O0OO0OO #line:293
            O00000O0000OO0OO0 ["bad"]=O0OO0O00OO00O00OO #line:294
            O00000O0000OO0OO0 ["fourfold"]=[OOOOO000OO0O00000 ,OOO0000O0OO0OOOO0 ,OOOOOOO0OOOOO0O0O ,OOOO000O0O0O0O0OO ]#line:295
        return O0OOOO0OO0O0OOO0O ,O00000O0000OO0OO0 #line:299
    def _verifysd4ft (OO0O00O0OOOO00OOO ,_OOO000OO00OOO0O00 ):#line:301
        O00OOO0O00O000OOO ={}#line:302
        O0OO0OO0OOO0O000O =0 #line:303
        for OO0OOOOOO00O0OO0O in OO0O00O0OOOO00OOO .task_actinfo ['cedents']:#line:304
            O00OOO0O00O000OOO [OO0OOOOOO00O0OO0O ['cedent_type']]=OO0OOOOOO00O0OO0O ['filter_value']#line:306
            O0OO0OO0OOO0O000O =O0OO0OO0OOO0O000O +1 #line:307
        OO0O0O0OOO000OO0O =bin (O00OOO0O00O000OOO ['ante']&O00OOO0O00O000OOO ['succ']&O00OOO0O00O000OOO ['cond']&O00OOO0O00O000OOO ['frst']).count ("1")#line:309
        OO000OOOOOOOO0OOO =bin (O00OOO0O00O000OOO ['ante']&O00OOO0O00O000OOO ['succ']&O00OOO0O00O000OOO ['cond']&O00OOO0O00O000OOO ['scnd']).count ("1")#line:310
        OOOO0O00000OO00O0 =None #line:311
        OOO000OO000OO00OO =0 #line:312
        OO0O000O00O00OO00 =0 #line:313
        if OO0O0O0OOO000OO0O >0 :#line:322
            OOO000OO000OO00OO =bin (O00OOO0O00O000OOO ['ante']&O00OOO0O00O000OOO ['succ']&O00OOO0O00O000OOO ['cond']&O00OOO0O00O000OOO ['frst']).count ("1")*1.0 /bin (O00OOO0O00O000OOO ['ante']&O00OOO0O00O000OOO ['cond']&O00OOO0O00O000OOO ['frst']).count ("1")#line:323
        if OO000OOOOOOOO0OOO >0 :#line:324
            OO0O000O00O00OO00 =bin (O00OOO0O00O000OOO ['ante']&O00OOO0O00O000OOO ['succ']&O00OOO0O00O000OOO ['cond']&O00OOO0O00O000OOO ['scnd']).count ("1")*1.0 /bin (O00OOO0O00O000OOO ['ante']&O00OOO0O00O000OOO ['cond']&O00OOO0O00O000OOO ['scnd']).count ("1")#line:325
        OOO0OOOOOOO00OO00 =1 <<OO0O00O0OOOO00OOO .data ["rows_count"]#line:327
        OO000O00O0O0O00O0 =bin (O00OOO0O00O000OOO ['ante']&O00OOO0O00O000OOO ['succ']&O00OOO0O00O000OOO ['cond']&O00OOO0O00O000OOO ['frst']).count ("1")#line:328
        OO0OOO0OOO0OO0O00 =bin (O00OOO0O00O000OOO ['ante']&~(OOO0OOOOOOO00OO00 |O00OOO0O00O000OOO ['succ'])&O00OOO0O00O000OOO ['cond']&O00OOO0O00O000OOO ['frst']).count ("1")#line:329
        OOO0O0OO0000000OO =bin (~(OOO0OOOOOOO00OO00 |O00OOO0O00O000OOO ['ante'])&O00OOO0O00O000OOO ['succ']&O00OOO0O00O000OOO ['cond']&O00OOO0O00O000OOO ['frst']).count ("1")#line:330
        O0OO0O0OO0O0O0OOO =bin (~(OOO0OOOOOOO00OO00 |O00OOO0O00O000OOO ['ante'])&~(OOO0OOOOOOO00OO00 |O00OOO0O00O000OOO ['succ'])&O00OOO0O00O000OOO ['cond']&O00OOO0O00O000OOO ['frst']).count ("1")#line:331
        O00O0O00O0OO0000O =bin (O00OOO0O00O000OOO ['ante']&O00OOO0O00O000OOO ['succ']&O00OOO0O00O000OOO ['cond']&O00OOO0O00O000OOO ['scnd']).count ("1")#line:332
        OOO0O0OO0OO00OO00 =bin (O00OOO0O00O000OOO ['ante']&~(OOO0OOOOOOO00OO00 |O00OOO0O00O000OOO ['succ'])&O00OOO0O00O000OOO ['cond']&O00OOO0O00O000OOO ['scnd']).count ("1")#line:333
        O00OO000O0OOO00O0 =bin (~(OOO0OOOOOOO00OO00 |O00OOO0O00O000OOO ['ante'])&O00OOO0O00O000OOO ['succ']&O00OOO0O00O000OOO ['cond']&O00OOO0O00O000OOO ['scnd']).count ("1")#line:334
        O00O00O0O000O000O =bin (~(OOO0OOOOOOO00OO00 |O00OOO0O00O000OOO ['ante'])&~(OOO0OOOOOOO00OO00 |O00OOO0O00O000OOO ['succ'])&O00OOO0O00O000OOO ['cond']&O00OOO0O00O000OOO ['scnd']).count ("1")#line:335
        OO0O0O0O000O0O000 =True #line:336
        for OO0OOOO0OO000OOO0 in OO0O00O0OOOO00OOO .quantifiers .keys ():#line:337
            if (OO0OOOO0OO000OOO0 =='FrstBase')|(OO0OOOO0OO000OOO0 =='Base1'):#line:338
                OO0O0O0O000O0O000 =OO0O0O0O000O0O000 and (OO0O00O0OOOO00OOO .quantifiers .get (OO0OOOO0OO000OOO0 )<=OO0O0O0OOO000OO0O )#line:339
            if (OO0OOOO0OO000OOO0 =='ScndBase')|(OO0OOOO0OO000OOO0 =='Base2'):#line:340
                OO0O0O0O000O0O000 =OO0O0O0O000O0O000 and (OO0O00O0OOOO00OOO .quantifiers .get (OO0OOOO0OO000OOO0 )<=OO000OOOOOOOO0OOO )#line:341
            if (OO0OOOO0OO000OOO0 =='FrstRelBase')|(OO0OOOO0OO000OOO0 =='RelBase1'):#line:342
                OO0O0O0O000O0O000 =OO0O0O0O000O0O000 and (OO0O00O0OOOO00OOO .quantifiers .get (OO0OOOO0OO000OOO0 )<=OO0O0O0OOO000OO0O *1.0 /OO0O00O0OOOO00OOO .data ["rows_count"])#line:343
            if (OO0OOOO0OO000OOO0 =='ScndRelBase')|(OO0OOOO0OO000OOO0 =='RelBase2'):#line:344
                OO0O0O0O000O0O000 =OO0O0O0O000O0O000 and (OO0O00O0OOOO00OOO .quantifiers .get (OO0OOOO0OO000OOO0 )<=OO000OOOOOOOO0OOO *1.0 /OO0O00O0OOOO00OOO .data ["rows_count"])#line:345
            if (OO0OOOO0OO000OOO0 =='Frstpim')|(OO0OOOO0OO000OOO0 =='pim1'):#line:346
                OO0O0O0O000O0O000 =OO0O0O0O000O0O000 and (OO0O00O0OOOO00OOO .quantifiers .get (OO0OOOO0OO000OOO0 )<=OOO000OO000OO00OO )#line:347
            if (OO0OOOO0OO000OOO0 =='Scndpim')|(OO0OOOO0OO000OOO0 =='pim2'):#line:348
                OO0O0O0O000O0O000 =OO0O0O0O000O0O000 and (OO0O00O0OOOO00OOO .quantifiers .get (OO0OOOO0OO000OOO0 )<=OO0O000O00O00OO00 )#line:349
            if OO0OOOO0OO000OOO0 =='Deltapim':#line:350
                OO0O0O0O000O0O000 =OO0O0O0O000O0O000 and (OO0O00O0OOOO00OOO .quantifiers .get (OO0OOOO0OO000OOO0 )<=OOO000OO000OO00OO -OO0O000O00O00OO00 )#line:351
            if OO0OOOO0OO000OOO0 =='Ratiopim':#line:354
                if (OO0O000O00O00OO00 >0 ):#line:355
                    OO0O0O0O000O0O000 =OO0O0O0O000O0O000 and (OO0O00O0OOOO00OOO .quantifiers .get (OO0OOOO0OO000OOO0 )<=OOO000OO000OO00OO *1.0 /OO0O000O00O00OO00 )#line:356
                else :#line:357
                    OO0O0O0O000O0O000 =False #line:358
        O0OOO00O0000O0O00 ={}#line:359
        if OO0O0O0O000O0O000 ==True :#line:360
            OO0O00O0OOOO00OOO .stats ['total_valid']+=1 #line:362
            O0OOO00O0000O0O00 ["base1"]=OO0O0O0OOO000OO0O #line:363
            O0OOO00O0000O0O00 ["base2"]=OO000OOOOOOOO0OOO #line:364
            O0OOO00O0000O0O00 ["rel_base1"]=OO0O0O0OOO000OO0O *1.0 /OO0O00O0OOOO00OOO .rows_count #line:365
            O0OOO00O0000O0O00 ["rel_base2"]=OO000OOOOOOOO0OOO *1.0 /OO0O00O0OOOO00OOO .rows_count #line:366
            O0OOO00O0000O0O00 ["pim1"]=OOO000OO000OO00OO #line:367
            O0OOO00O0000O0O00 ["pim2"]=OO0O000O00O00OO00 #line:368
            O0OOO00O0000O0O00 ["deltapim"]=OOO000OO000OO00OO -OO0O000O00O00OO00 #line:369
            if (OO0O000O00O00OO00 >0 ):#line:370
                O0OOO00O0000O0O00 ["ratiopim"]=OOO000OO000OO00OO *1.0 /OO0O000O00O00OO00 #line:371
            else :#line:372
                O0OOO00O0000O0O00 ["ratiopim"]=None #line:373
            O0OOO00O0000O0O00 ["fourfold1"]=[OO000O00O0O0O00O0 ,OO0OOO0OOO0OO0O00 ,OOO0O0OO0000000OO ,O0OO0O0OO0O0O0OOO ]#line:374
            O0OOO00O0000O0O00 ["fourfold2"]=[O00O0O00O0OO0000O ,OOO0O0OO0OO00OO00 ,O00OO000O0OOO00O0 ,O00O00O0O000O000O ]#line:375
        if OO0O0O0O000O0O000 :#line:377
            print (f"DEBUG : ii = {O0OO0OO0OOO0O000O}")#line:378
        return OO0O0O0O000O0O000 ,O0OOO00O0000O0O00 #line:379
    def _verifynewact4ft (OOO00O0OO00000O0O ,_O0O0O0OO0O00OOOO0 ):#line:381
        O0000O0O0000OO000 ={}#line:382
        for O0OO0O0O00OOOOO00 in OOO00O0OO00000O0O .task_actinfo ['cedents']:#line:383
            O0000O0O0000OO000 [O0OO0O0O00OOOOO00 ['cedent_type']]=O0OO0O0O00OOOOO00 ['filter_value']#line:385
        OO0OO000O0OO00OO0 =bin (O0000O0O0000OO000 ['ante']&O0000O0O0000OO000 ['succ']&O0000O0O0000OO000 ['cond']).count ("1")#line:387
        O0000O0OO0O00O00O =bin (O0000O0O0000OO000 ['ante']&O0000O0O0000OO000 ['succ']&O0000O0O0000OO000 ['cond']&O0000O0O0000OO000 ['antv']&O0000O0O0000OO000 ['sucv']).count ("1")#line:388
        O0OOOOOOO000OO00O =None #line:389
        OOOO0OO00OOOOOO0O =0 #line:390
        OOOOO0O0O0000000O =0 #line:391
        if OO0OO000O0OO00OO0 >0 :#line:400
            OOOO0OO00OOOOOO0O =bin (O0000O0O0000OO000 ['ante']&O0000O0O0000OO000 ['succ']&O0000O0O0000OO000 ['cond']).count ("1")*1.0 /bin (O0000O0O0000OO000 ['ante']&O0000O0O0000OO000 ['cond']).count ("1")#line:402
        if O0000O0OO0O00O00O >0 :#line:403
            OOOOO0O0O0000000O =bin (O0000O0O0000OO000 ['ante']&O0000O0O0000OO000 ['succ']&O0000O0O0000OO000 ['cond']&O0000O0O0000OO000 ['antv']&O0000O0O0000OO000 ['sucv']).count ("1")*1.0 /bin (O0000O0O0000OO000 ['ante']&O0000O0O0000OO000 ['cond']&O0000O0O0000OO000 ['antv']).count ("1")#line:405
        O000OOOOO0OO0O00O =1 <<OOO00O0OO00000O0O .rows_count #line:407
        O00000OOOOO000O0O =bin (O0000O0O0000OO000 ['ante']&O0000O0O0000OO000 ['succ']&O0000O0O0000OO000 ['cond']).count ("1")#line:408
        O000OOOO00OO0OOO0 =bin (O0000O0O0000OO000 ['ante']&~(O000OOOOO0OO0O00O |O0000O0O0000OO000 ['succ'])&O0000O0O0000OO000 ['cond']).count ("1")#line:409
        O00O0OO0O0O0OOO0O =bin (~(O000OOOOO0OO0O00O |O0000O0O0000OO000 ['ante'])&O0000O0O0000OO000 ['succ']&O0000O0O0000OO000 ['cond']).count ("1")#line:410
        O0O0OO00OO000OOOO =bin (~(O000OOOOO0OO0O00O |O0000O0O0000OO000 ['ante'])&~(O000OOOOO0OO0O00O |O0000O0O0000OO000 ['succ'])&O0000O0O0000OO000 ['cond']).count ("1")#line:411
        OO0000000OO0OOOOO =bin (O0000O0O0000OO000 ['ante']&O0000O0O0000OO000 ['succ']&O0000O0O0000OO000 ['cond']&O0000O0O0000OO000 ['antv']&O0000O0O0000OO000 ['sucv']).count ("1")#line:412
        OO0OO000O0OO00000 =bin (O0000O0O0000OO000 ['ante']&~(O000OOOOO0OO0O00O |(O0000O0O0000OO000 ['succ']&O0000O0O0000OO000 ['sucv']))&O0000O0O0000OO000 ['cond']).count ("1")#line:413
        O00000O0OOOO0OO0O =bin (~(O000OOOOO0OO0O00O |(O0000O0O0000OO000 ['ante']&O0000O0O0000OO000 ['antv']))&O0000O0O0000OO000 ['succ']&O0000O0O0000OO000 ['cond']&O0000O0O0000OO000 ['sucv']).count ("1")#line:414
        OOO00000OOO0OO0O0 =bin (~(O000OOOOO0OO0O00O |(O0000O0O0000OO000 ['ante']&O0000O0O0000OO000 ['antv']))&~(O000OOOOO0OO0O00O |(O0000O0O0000OO000 ['succ']&O0000O0O0000OO000 ['sucv']))&O0000O0O0000OO000 ['cond']).count ("1")#line:415
        OO000000O0O00OO0O =True #line:416
        for O0O000OO00O0OO000 in OOO00O0OO00000O0O .quantifiers .keys ():#line:417
            if (O0O000OO00O0OO000 =='PreBase')|(O0O000OO00O0OO000 =='Base1'):#line:418
                OO000000O0O00OO0O =OO000000O0O00OO0O and (OOO00O0OO00000O0O .quantifiers .get (O0O000OO00O0OO000 )<=OO0OO000O0OO00OO0 )#line:419
            if (O0O000OO00O0OO000 =='PostBase')|(O0O000OO00O0OO000 =='Base2'):#line:420
                OO000000O0O00OO0O =OO000000O0O00OO0O and (OOO00O0OO00000O0O .quantifiers .get (O0O000OO00O0OO000 )<=O0000O0OO0O00O00O )#line:421
            if (O0O000OO00O0OO000 =='PreRelBase')|(O0O000OO00O0OO000 =='RelBase1'):#line:422
                OO000000O0O00OO0O =OO000000O0O00OO0O and (OOO00O0OO00000O0O .quantifiers .get (O0O000OO00O0OO000 )<=OO0OO000O0OO00OO0 *1.0 /OOO00O0OO00000O0O .data ["rows_count"])#line:423
            if (O0O000OO00O0OO000 =='PostRelBase')|(O0O000OO00O0OO000 =='RelBase2'):#line:424
                OO000000O0O00OO0O =OO000000O0O00OO0O and (OOO00O0OO00000O0O .quantifiers .get (O0O000OO00O0OO000 )<=O0000O0OO0O00O00O *1.0 /OOO00O0OO00000O0O .data ["rows_count"])#line:425
            if (O0O000OO00O0OO000 =='Prepim')|(O0O000OO00O0OO000 =='pim1'):#line:426
                OO000000O0O00OO0O =OO000000O0O00OO0O and (OOO00O0OO00000O0O .quantifiers .get (O0O000OO00O0OO000 )<=OOOO0OO00OOOOOO0O )#line:427
            if (O0O000OO00O0OO000 =='Postpim')|(O0O000OO00O0OO000 =='pim2'):#line:428
                OO000000O0O00OO0O =OO000000O0O00OO0O and (OOO00O0OO00000O0O .quantifiers .get (O0O000OO00O0OO000 )<=OOOOO0O0O0000000O )#line:429
            if O0O000OO00O0OO000 =='Deltapim':#line:430
                OO000000O0O00OO0O =OO000000O0O00OO0O and (OOO00O0OO00000O0O .quantifiers .get (O0O000OO00O0OO000 )<=OOOO0OO00OOOOOO0O -OOOOO0O0O0000000O )#line:431
            if O0O000OO00O0OO000 =='Ratiopim':#line:434
                if (OOOOO0O0O0000000O >0 ):#line:435
                    OO000000O0O00OO0O =OO000000O0O00OO0O and (OOO00O0OO00000O0O .quantifiers .get (O0O000OO00O0OO000 )<=OOOO0OO00OOOOOO0O *1.0 /OOOOO0O0O0000000O )#line:436
                else :#line:437
                    OO000000O0O00OO0O =False #line:438
        OO0000OOO0O000000 ={}#line:439
        if OO000000O0O00OO0O ==True :#line:440
            OOO00O0OO00000O0O .stats ['total_valid']+=1 #line:442
            OO0000OOO0O000000 ["base1"]=OO0OO000O0OO00OO0 #line:443
            OO0000OOO0O000000 ["base2"]=O0000O0OO0O00O00O #line:444
            OO0000OOO0O000000 ["rel_base1"]=OO0OO000O0OO00OO0 *1.0 /OOO00O0OO00000O0O .data ["rows_count"]#line:445
            OO0000OOO0O000000 ["rel_base2"]=O0000O0OO0O00O00O *1.0 /OOO00O0OO00000O0O .data ["rows_count"]#line:446
            OO0000OOO0O000000 ["pim1"]=OOOO0OO00OOOOOO0O #line:447
            OO0000OOO0O000000 ["pim2"]=OOOOO0O0O0000000O #line:448
            OO0000OOO0O000000 ["deltapim"]=OOOO0OO00OOOOOO0O -OOOOO0O0O0000000O #line:449
            if (OOOOO0O0O0000000O >0 ):#line:450
                OO0000OOO0O000000 ["ratiopim"]=OOOO0OO00OOOOOO0O *1.0 /OOOOO0O0O0000000O #line:451
            else :#line:452
                OO0000OOO0O000000 ["ratiopim"]=None #line:453
            OO0000OOO0O000000 ["fourfoldpre"]=[O00000OOOOO000O0O ,O000OOOO00OO0OOO0 ,O00O0OO0O0O0OOO0O ,O0O0OO00OO000OOOO ]#line:454
            OO0000OOO0O000000 ["fourfoldpost"]=[OO0000000OO0OOOOO ,OO0OO000O0OO00000 ,O00000O0OOOO0OO0O ,OOO00000OOO0OO0O0 ]#line:455
        return OO000000O0O00OO0O ,OO0000OOO0O000000 #line:457
    def _verifyact4ft (OOO0OOOO0O0O00000 ,_O0O00OO0OOO00OO0O ):#line:459
        OO0O00OOO00OOO00O ={}#line:460
        for O00OO0O00OO00OO00 in OOO0OOOO0O0O00000 .task_actinfo ['cedents']:#line:461
            OO0O00OOO00OOO00O [O00OO0O00OO00OO00 ['cedent_type']]=O00OO0O00OO00OO00 ['filter_value']#line:463
        OO0OOO000O00OO0O0 =bin (OO0O00OOO00OOO00O ['ante']&OO0O00OOO00OOO00O ['succ']&OO0O00OOO00OOO00O ['cond']&OO0O00OOO00OOO00O ['antv-']&OO0O00OOO00OOO00O ['sucv-']).count ("1")#line:465
        OO00O0OOO0000O0OO =bin (OO0O00OOO00OOO00O ['ante']&OO0O00OOO00OOO00O ['succ']&OO0O00OOO00OOO00O ['cond']&OO0O00OOO00OOO00O ['antv+']&OO0O00OOO00OOO00O ['sucv+']).count ("1")#line:466
        O00000O0OOOOO0OO0 =None #line:467
        OO0OOO000O0O000OO =0 #line:468
        OOO00O0OOOOO000OO =0 #line:469
        if OO0OOO000O00OO0O0 >0 :#line:478
            OO0OOO000O0O000OO =bin (OO0O00OOO00OOO00O ['ante']&OO0O00OOO00OOO00O ['succ']&OO0O00OOO00OOO00O ['cond']&OO0O00OOO00OOO00O ['antv-']&OO0O00OOO00OOO00O ['sucv-']).count ("1")*1.0 /bin (OO0O00OOO00OOO00O ['ante']&OO0O00OOO00OOO00O ['cond']&OO0O00OOO00OOO00O ['antv-']).count ("1")#line:480
        if OO00O0OOO0000O0OO >0 :#line:481
            OOO00O0OOOOO000OO =bin (OO0O00OOO00OOO00O ['ante']&OO0O00OOO00OOO00O ['succ']&OO0O00OOO00OOO00O ['cond']&OO0O00OOO00OOO00O ['antv+']&OO0O00OOO00OOO00O ['sucv+']).count ("1")*1.0 /bin (OO0O00OOO00OOO00O ['ante']&OO0O00OOO00OOO00O ['cond']&OO0O00OOO00OOO00O ['antv+']).count ("1")#line:483
        OO0OOOOOO0O0000OO =1 <<OOO0OOOO0O0O00000 .data ["rows_count"]#line:485
        OO00OO0O000O0OOO0 =bin (OO0O00OOO00OOO00O ['ante']&OO0O00OOO00OOO00O ['succ']&OO0O00OOO00OOO00O ['cond']&OO0O00OOO00OOO00O ['antv-']&OO0O00OOO00OOO00O ['sucv-']).count ("1")#line:486
        O0OO0O0OO0OO0OOO0 =bin (OO0O00OOO00OOO00O ['ante']&OO0O00OOO00OOO00O ['antv-']&~(OO0OOOOOO0O0000OO |(OO0O00OOO00OOO00O ['succ']&OO0O00OOO00OOO00O ['sucv-']))&OO0O00OOO00OOO00O ['cond']).count ("1")#line:487
        OO0O00O00OOO0000O =bin (~(OO0OOOOOO0O0000OO |(OO0O00OOO00OOO00O ['ante']&OO0O00OOO00OOO00O ['antv-']))&OO0O00OOO00OOO00O ['succ']&OO0O00OOO00OOO00O ['cond']&OO0O00OOO00OOO00O ['sucv-']).count ("1")#line:488
        OOOO0O0OOOOOO0OO0 =bin (~(OO0OOOOOO0O0000OO |(OO0O00OOO00OOO00O ['ante']&OO0O00OOO00OOO00O ['antv-']))&~(OO0OOOOOO0O0000OO |(OO0O00OOO00OOO00O ['succ']&OO0O00OOO00OOO00O ['sucv-']))&OO0O00OOO00OOO00O ['cond']).count ("1")#line:489
        O0O000O00O0OOO00O =bin (OO0O00OOO00OOO00O ['ante']&OO0O00OOO00OOO00O ['succ']&OO0O00OOO00OOO00O ['cond']&OO0O00OOO00OOO00O ['antv+']&OO0O00OOO00OOO00O ['sucv+']).count ("1")#line:490
        OO0000O000O0OOO00 =bin (OO0O00OOO00OOO00O ['ante']&OO0O00OOO00OOO00O ['antv+']&~(OO0OOOOOO0O0000OO |(OO0O00OOO00OOO00O ['succ']&OO0O00OOO00OOO00O ['sucv+']))&OO0O00OOO00OOO00O ['cond']).count ("1")#line:491
        OOO00OO00OOO0OO00 =bin (~(OO0OOOOOO0O0000OO |(OO0O00OOO00OOO00O ['ante']&OO0O00OOO00OOO00O ['antv+']))&OO0O00OOO00OOO00O ['succ']&OO0O00OOO00OOO00O ['cond']&OO0O00OOO00OOO00O ['sucv+']).count ("1")#line:492
        OOOOO00O00O00000O =bin (~(OO0OOOOOO0O0000OO |(OO0O00OOO00OOO00O ['ante']&OO0O00OOO00OOO00O ['antv+']))&~(OO0OOOOOO0O0000OO |(OO0O00OOO00OOO00O ['succ']&OO0O00OOO00OOO00O ['sucv+']))&OO0O00OOO00OOO00O ['cond']).count ("1")#line:493
        OOOOO00O0OOOO000O =True #line:494
        for O00O0OO00OOOO0O0O in OOO0OOOO0O0O00000 .quantifiers .keys ():#line:495
            if (O00O0OO00OOOO0O0O =='PreBase')|(O00O0OO00OOOO0O0O =='Base1'):#line:496
                OOOOO00O0OOOO000O =OOOOO00O0OOOO000O and (OOO0OOOO0O0O00000 .quantifiers .get (O00O0OO00OOOO0O0O )<=OO0OOO000O00OO0O0 )#line:497
            if (O00O0OO00OOOO0O0O =='PostBase')|(O00O0OO00OOOO0O0O =='Base2'):#line:498
                OOOOO00O0OOOO000O =OOOOO00O0OOOO000O and (OOO0OOOO0O0O00000 .quantifiers .get (O00O0OO00OOOO0O0O )<=OO00O0OOO0000O0OO )#line:499
            if (O00O0OO00OOOO0O0O =='PreRelBase')|(O00O0OO00OOOO0O0O =='RelBase1'):#line:500
                OOOOO00O0OOOO000O =OOOOO00O0OOOO000O and (OOO0OOOO0O0O00000 .quantifiers .get (O00O0OO00OOOO0O0O )<=OO0OOO000O00OO0O0 *1.0 /OOO0OOOO0O0O00000 .data ["rows_count"])#line:501
            if (O00O0OO00OOOO0O0O =='PostRelBase')|(O00O0OO00OOOO0O0O =='RelBase2'):#line:502
                OOOOO00O0OOOO000O =OOOOO00O0OOOO000O and (OOO0OOOO0O0O00000 .quantifiers .get (O00O0OO00OOOO0O0O )<=OO00O0OOO0000O0OO *1.0 /OOO0OOOO0O0O00000 .data ["rows_count"])#line:503
            if (O00O0OO00OOOO0O0O =='Prepim')|(O00O0OO00OOOO0O0O =='pim1'):#line:504
                OOOOO00O0OOOO000O =OOOOO00O0OOOO000O and (OOO0OOOO0O0O00000 .quantifiers .get (O00O0OO00OOOO0O0O )<=OO0OOO000O0O000OO )#line:505
            if (O00O0OO00OOOO0O0O =='Postpim')|(O00O0OO00OOOO0O0O =='pim2'):#line:506
                OOOOO00O0OOOO000O =OOOOO00O0OOOO000O and (OOO0OOOO0O0O00000 .quantifiers .get (O00O0OO00OOOO0O0O )<=OOO00O0OOOOO000OO )#line:507
            if O00O0OO00OOOO0O0O =='Deltapim':#line:508
                OOOOO00O0OOOO000O =OOOOO00O0OOOO000O and (OOO0OOOO0O0O00000 .quantifiers .get (O00O0OO00OOOO0O0O )<=OO0OOO000O0O000OO -OOO00O0OOOOO000OO )#line:509
            if O00O0OO00OOOO0O0O =='Ratiopim':#line:512
                if (OO0OOO000O0O000OO >0 ):#line:513
                    OOOOO00O0OOOO000O =OOOOO00O0OOOO000O and (OOO0OOOO0O0O00000 .quantifiers .get (O00O0OO00OOOO0O0O )<=OOO00O0OOOOO000OO *1.0 /OO0OOO000O0O000OO )#line:514
                else :#line:515
                    OOOOO00O0OOOO000O =False #line:516
        O0OO0OO0O00OO00OO ={}#line:517
        if OOOOO00O0OOOO000O ==True :#line:518
            OOO0OOOO0O0O00000 .stats ['total_valid']+=1 #line:520
            O0OO0OO0O00OO00OO ["base1"]=OO0OOO000O00OO0O0 #line:521
            O0OO0OO0O00OO00OO ["base2"]=OO00O0OOO0000O0OO #line:522
            O0OO0OO0O00OO00OO ["rel_base1"]=OO0OOO000O00OO0O0 *1.0 /OOO0OOOO0O0O00000 .data ["rows_count"]#line:523
            O0OO0OO0O00OO00OO ["rel_base2"]=OO00O0OOO0000O0OO *1.0 /OOO0OOOO0O0O00000 .data ["rows_count"]#line:524
            O0OO0OO0O00OO00OO ["pim1"]=OO0OOO000O0O000OO #line:525
            O0OO0OO0O00OO00OO ["pim2"]=OOO00O0OOOOO000OO #line:526
            O0OO0OO0O00OO00OO ["deltapim"]=OO0OOO000O0O000OO -OOO00O0OOOOO000OO #line:527
            if (OO0OOO000O0O000OO >0 ):#line:528
                O0OO0OO0O00OO00OO ["ratiopim"]=OOO00O0OOOOO000OO *1.0 /OO0OOO000O0O000OO #line:529
            else :#line:530
                O0OO0OO0O00OO00OO ["ratiopim"]=None #line:531
            O0OO0OO0O00OO00OO ["fourfoldpre"]=[OO00OO0O000O0OOO0 ,O0OO0O0OO0OO0OOO0 ,OO0O00O00OOO0000O ,OOOO0O0OOOOOO0OO0 ]#line:532
            O0OO0OO0O00OO00OO ["fourfoldpost"]=[O0O000O00O0OOO00O ,OO0000O000O0OOO00 ,OOO00OO00OOO0OO00 ,OOOOO00O00O00000O ]#line:533
        return OOOOO00O0OOOO000O ,O0OO0OO0O00OO00OO #line:535
    def _verify_opt (OO0O0O0O000O00000 ,O0O0OOOOO0OOO0OO0 ,OO00O000OO0O00000 ):#line:537
        O000O0O000O00OO0O =False #line:538
        if not (O0O0OOOOO0OOO0OO0 ['optim'].get ('only_con')):#line:541
            return False #line:542
        O0OO0O00O0O0OOO00 ={}#line:543
        for O00O00OOO0O000OO0 in OO0O0O0O000O00000 .task_actinfo ['cedents']:#line:544
            O0OO0O00O0O0OOO00 [O00O00OOO0O000OO0 ['cedent_type']]=O00O00OOO0O000OO0 ['filter_value']#line:546
        OO0O00O0OOOOO0000 =1 <<OO0O0O0O000O00000 .data ["rows_count"]#line:548
        OO0OOO0O00OOO0OO0 =OO0O00O0OOOOO0000 -1 #line:549
        O00OOO00O0OO00O0O =""#line:550
        OOO0O00000000OO0O =0 #line:551
        if (O0OO0O00O0O0OOO00 .get ('ante')!=None ):#line:552
            OO0OOO0O00OOO0OO0 =OO0OOO0O00OOO0OO0 &O0OO0O00O0O0OOO00 ['ante']#line:553
        if (O0OO0O00O0O0OOO00 .get ('succ')!=None ):#line:554
            OO0OOO0O00OOO0OO0 =OO0OOO0O00OOO0OO0 &O0OO0O00O0O0OOO00 ['succ']#line:555
        if (O0OO0O00O0O0OOO00 .get ('cond')!=None ):#line:556
            OO0OOO0O00OOO0OO0 =OO0OOO0O00OOO0OO0 &O0OO0O00O0O0OOO00 ['cond']#line:557
        OOO00OOOO0O0OOOOO =None #line:560
        if (OO0O0O0O000O00000 .proc =='CFMiner')|(OO0O0O0O000O00000 .proc =='4ftMiner'):#line:585
            OO0O0000O00OO0000 =bin (OO0OOO0O00OOO0OO0 ).count ("1")#line:586
            for OO0000O00000O0000 in OO0O0O0O000O00000 .quantifiers .keys ():#line:587
                if OO0000O00000O0000 =='Base':#line:588
                    if not (OO0O0O0O000O00000 .quantifiers .get (OO0000O00000O0000 )<=OO0O0000O00OO0000 ):#line:589
                        O000O0O000O00OO0O =True #line:590
                if OO0000O00000O0000 =='RelBase':#line:592
                    if not (OO0O0O0O000O00000 .quantifiers .get (OO0000O00000O0000 )<=OO0O0000O00OO0000 *1.0 /OO0O0O0O000O00000 .data ["rows_count"]):#line:593
                        O000O0O000O00OO0O =True #line:594
        return O000O0O000O00OO0O #line:597
        if OO0O0O0O000O00000 .proc =='CFMiner':#line:600
            if (OO00O000OO0O00000 ['cedent_type']=='cond')&(OO00O000OO0O00000 ['defi'].get ('type')=='con'):#line:601
                OO0O0000O00OO0000 =bin (O0OO0O00O0O0OOO00 ['cond']).count ("1")#line:602
                O000OO0OOO0OO0OOO =True #line:603
                for OO0000O00000O0000 in OO0O0O0O000O00000 .quantifiers .keys ():#line:604
                    if OO0000O00000O0000 =='Base':#line:605
                        O000OO0OOO0OO0OOO =O000OO0OOO0OO0OOO and (OO0O0O0O000O00000 .quantifiers .get (OO0000O00000O0000 )<=OO0O0000O00OO0000 )#line:606
                        if not (O000OO0OOO0OO0OOO ):#line:607
                            print (f"...optimization : base is {OO0O0000O00OO0000} for {OO00O000OO0O00000['generated_string']}")#line:608
                    if OO0000O00000O0000 =='RelBase':#line:609
                        O000OO0OOO0OO0OOO =O000OO0OOO0OO0OOO and (OO0O0O0O000O00000 .quantifiers .get (OO0000O00000O0000 )<=OO0O0000O00OO0000 *1.0 /OO0O0O0O000O00000 .data ["rows_count"])#line:610
                        if not (O000OO0OOO0OO0OOO ):#line:611
                            print (f"...optimization : base is {OO0O0000O00OO0000} for {OO00O000OO0O00000['generated_string']}")#line:612
                O000O0O000O00OO0O =not (O000OO0OOO0OO0OOO )#line:613
        elif OO0O0O0O000O00000 .proc =='4ftMiner':#line:614
            if (OO00O000OO0O00000 ['cedent_type']=='cond')&(OO00O000OO0O00000 ['defi'].get ('type')=='con'):#line:615
                OO0O0000O00OO0000 =bin (O0OO0O00O0O0OOO00 ['cond']).count ("1")#line:616
                O000OO0OOO0OO0OOO =True #line:617
                for OO0000O00000O0000 in OO0O0O0O000O00000 .quantifiers .keys ():#line:618
                    if OO0000O00000O0000 =='Base':#line:619
                        O000OO0OOO0OO0OOO =O000OO0OOO0OO0OOO and (OO0O0O0O000O00000 .quantifiers .get (OO0000O00000O0000 )<=OO0O0000O00OO0000 )#line:620
                        if not (O000OO0OOO0OO0OOO ):#line:621
                            print (f"...optimization : base is {OO0O0000O00OO0000} for {OO00O000OO0O00000['generated_string']}")#line:622
                    if OO0000O00000O0000 =='RelBase':#line:623
                        O000OO0OOO0OO0OOO =O000OO0OOO0OO0OOO and (OO0O0O0O000O00000 .quantifiers .get (OO0000O00000O0000 )<=OO0O0000O00OO0000 *1.0 /OO0O0O0O000O00000 .data ["rows_count"])#line:624
                        if not (O000OO0OOO0OO0OOO ):#line:625
                            print (f"...optimization : base is {OO0O0000O00OO0000} for {OO00O000OO0O00000['generated_string']}")#line:626
                O000O0O000O00OO0O =not (O000OO0OOO0OO0OOO )#line:627
            if (OO00O000OO0O00000 ['cedent_type']=='ante')&(OO00O000OO0O00000 ['defi'].get ('type')=='con'):#line:628
                OO0O0000O00OO0000 =bin (O0OO0O00O0O0OOO00 ['ante']&O0OO0O00O0O0OOO00 ['cond']).count ("1")#line:629
                O000OO0OOO0OO0OOO =True #line:630
                for OO0000O00000O0000 in OO0O0O0O000O00000 .quantifiers .keys ():#line:631
                    if OO0000O00000O0000 =='Base':#line:632
                        O000OO0OOO0OO0OOO =O000OO0OOO0OO0OOO and (OO0O0O0O000O00000 .quantifiers .get (OO0000O00000O0000 )<=OO0O0000O00OO0000 )#line:633
                        if not (O000OO0OOO0OO0OOO ):#line:634
                            print (f"...optimization : ANTE: base is {OO0O0000O00OO0000} for {OO00O000OO0O00000['generated_string']}")#line:635
                    if OO0000O00000O0000 =='RelBase':#line:636
                        O000OO0OOO0OO0OOO =O000OO0OOO0OO0OOO and (OO0O0O0O000O00000 .quantifiers .get (OO0000O00000O0000 )<=OO0O0000O00OO0000 *1.0 /OO0O0O0O000O00000 .data ["rows_count"])#line:637
                        if not (O000OO0OOO0OO0OOO ):#line:638
                            print (f"...optimization : ANTE:  base is {OO0O0000O00OO0000} for {OO00O000OO0O00000['generated_string']}")#line:639
                O000O0O000O00OO0O =not (O000OO0OOO0OO0OOO )#line:640
            if (OO00O000OO0O00000 ['cedent_type']=='succ')&(OO00O000OO0O00000 ['defi'].get ('type')=='con'):#line:641
                OO0O0000O00OO0000 =bin (O0OO0O00O0O0OOO00 ['ante']&O0OO0O00O0O0OOO00 ['cond']&O0OO0O00O0O0OOO00 ['succ']).count ("1")#line:642
                OOO00OOOO0O0OOOOO =0 #line:643
                if OO0O0000O00OO0000 >0 :#line:644
                    OOO00OOOO0O0OOOOO =bin (O0OO0O00O0O0OOO00 ['ante']&O0OO0O00O0O0OOO00 ['succ']&O0OO0O00O0O0OOO00 ['cond']).count ("1")*1.0 /bin (O0OO0O00O0O0OOO00 ['ante']&O0OO0O00O0O0OOO00 ['cond']).count ("1")#line:645
                OO0O00O0OOOOO0000 =1 <<OO0O0O0O000O00000 .data ["rows_count"]#line:646
                O0OO0O0000000OOO0 =bin (O0OO0O00O0O0OOO00 ['ante']&O0OO0O00O0O0OOO00 ['succ']&O0OO0O00O0O0OOO00 ['cond']).count ("1")#line:647
                O0O00O0OOO0OOOO00 =bin (O0OO0O00O0O0OOO00 ['ante']&~(OO0O00O0OOOOO0000 |O0OO0O00O0O0OOO00 ['succ'])&O0OO0O00O0O0OOO00 ['cond']).count ("1")#line:648
                O00O00OOO0O000OO0 =bin (~(OO0O00O0OOOOO0000 |O0OO0O00O0O0OOO00 ['ante'])&O0OO0O00O0O0OOO00 ['succ']&O0OO0O00O0O0OOO00 ['cond']).count ("1")#line:649
                O0OO00O0O00O000O0 =bin (~(OO0O00O0OOOOO0000 |O0OO0O00O0O0OOO00 ['ante'])&~(OO0O00O0OOOOO0000 |O0OO0O00O0O0OOO00 ['succ'])&O0OO0O00O0O0OOO00 ['cond']).count ("1")#line:650
                O000OO0OOO0OO0OOO =True #line:651
                for OO0000O00000O0000 in OO0O0O0O000O00000 .quantifiers .keys ():#line:652
                    if OO0000O00000O0000 =='pim':#line:653
                        O000OO0OOO0OO0OOO =O000OO0OOO0OO0OOO and (OO0O0O0O000O00000 .quantifiers .get (OO0000O00000O0000 )<=OOO00OOOO0O0OOOOO )#line:654
                    if not (O000OO0OOO0OO0OOO ):#line:655
                        print (f"...optimization : SUCC:  pim is {OOO00OOOO0O0OOOOO} for {OO00O000OO0O00000['generated_string']}")#line:656
                    if OO0000O00000O0000 =='aad':#line:658
                        if (O0OO0O0000000OOO0 +O0O00O0OOO0OOOO00 )*(O0OO0O0000000OOO0 +O00O00OOO0O000OO0 )>0 :#line:659
                            O000OO0OOO0OO0OOO =O000OO0OOO0OO0OOO and (OO0O0O0O000O00000 .quantifiers .get (OO0000O00000O0000 )<=O0OO0O0000000OOO0 *(O0OO0O0000000OOO0 +O0O00O0OOO0OOOO00 +O00O00OOO0O000OO0 +O0OO00O0O00O000O0 )/(O0OO0O0000000OOO0 +O0O00O0OOO0OOOO00 )/(O0OO0O0000000OOO0 +O00O00OOO0O000OO0 )-1 )#line:660
                        else :#line:661
                            O000OO0OOO0OO0OOO =False #line:662
                        if not (O000OO0OOO0OO0OOO ):#line:663
                            O0OOOO0OO0000O0O0 =O0OO0O0000000OOO0 *(O0OO0O0000000OOO0 +O0O00O0OOO0OOOO00 +O00O00OOO0O000OO0 +O0OO00O0O00O000O0 )/(O0OO0O0000000OOO0 +O0O00O0OOO0OOOO00 )/(O0OO0O0000000OOO0 +O00O00OOO0O000OO0 )-1 #line:664
                            print (f"...optimization : SUCC:  aad is {O0OOOO0OO0000O0O0} for {OO00O000OO0O00000['generated_string']}")#line:665
                    if OO0000O00000O0000 =='bad':#line:666
                        if (O0OO0O0000000OOO0 +O0O00O0OOO0OOOO00 )*(O0OO0O0000000OOO0 +O00O00OOO0O000OO0 )>0 :#line:667
                            O000OO0OOO0OO0OOO =O000OO0OOO0OO0OOO and (OO0O0O0O000O00000 .quantifiers .get (OO0000O00000O0000 )<=1 -O0OO0O0000000OOO0 *(O0OO0O0000000OOO0 +O0O00O0OOO0OOOO00 +O00O00OOO0O000OO0 +O0OO00O0O00O000O0 )/(O0OO0O0000000OOO0 +O0O00O0OOO0OOOO00 )/(O0OO0O0000000OOO0 +O00O00OOO0O000OO0 ))#line:668
                        else :#line:669
                            O000OO0OOO0OO0OOO =False #line:670
                        if not (O000OO0OOO0OO0OOO ):#line:671
                            OO000OOO0OOO000OO =1 -O0OO0O0000000OOO0 *(O0OO0O0000000OOO0 +O0O00O0OOO0OOOO00 +O00O00OOO0O000OO0 +O0OO00O0O00O000O0 )/(O0OO0O0000000OOO0 +O0O00O0OOO0OOOO00 )/(O0OO0O0000000OOO0 +O00O00OOO0O000OO0 )#line:672
                            print (f"...optimization : SUCC:  bad is {OO000OOO0OOO000OO} for {OO00O000OO0O00000['generated_string']}")#line:673
                O000O0O000O00OO0O =not (O000OO0OOO0OO0OOO )#line:674
        if (O000O0O000O00OO0O ):#line:675
            print (f"... OPTIMALIZATION - SKIPPING BRANCH at cedent {OO00O000OO0O00000['cedent_type']}")#line:676
        return O000O0O000O00OO0O #line:677
    def _print (O0O0O000OO0O0O00O ,OO00O00O00O0O0O0O ,_OO0O00000OOO00O0O ,_O0000OOO000OOOO0O ):#line:680
        if (len (_OO0O00000OOO00O0O ))!=len (_O0000OOO000OOOO0O ):#line:681
            print ("DIFF IN LEN for following cedent : "+str (len (_OO0O00000OOO00O0O ))+" vs "+str (len (_O0000OOO000OOOO0O )))#line:682
            print ("trace cedent : "+str (_OO0O00000OOO00O0O )+", traces "+str (_O0000OOO000OOOO0O ))#line:683
        O000OOOOOOO00O0OO =''#line:684
        for O0OO0O0O0O0OOOO00 in range (len (_OO0O00000OOO00O0O )):#line:685
            OO00OOOO0O0OOO000 =O0O0O000OO0O0O00O .data ["varname"].index (OO00O00O00O0O0O0O ['defi'].get ('attributes')[_OO0O00000OOO00O0O [O0OO0O0O0O0OOOO00 ]].get ('name'))#line:686
            O000OOOOOOO00O0OO =O000OOOOOOO00O0OO +O0O0O000OO0O0O00O .data ["varname"][OO00OOOO0O0OOO000 ]+'('#line:688
            for O00OO00000O000OOO in _O0000OOO000OOOO0O [O0OO0O0O0O0OOOO00 ]:#line:689
                O000OOOOOOO00O0OO =O000OOOOOOO00O0OO +O0O0O000OO0O0O00O .data ["catnames"][OO00OOOO0O0OOO000 ][O00OO00000O000OOO ]+" "#line:690
            O000OOOOOOO00O0OO =O000OOOOOOO00O0OO +')'#line:691
            if O0OO0O0O0O0OOOO00 +1 <len (_OO0O00000OOO00O0O ):#line:692
                O000OOOOOOO00O0OO =O000OOOOOOO00O0OO +' & '#line:693
        return O000OOOOOOO00O0OO #line:697
    def _print_hypo (OO00OOOO0000OOO00 ,O0OOO000OOO0OOO00 ):#line:699
        print ('Hypothesis info : '+str (O0OOO000OOO0OOO00 ['params']))#line:700
        for OO0OOO00OOO000OOO in OO00OOOO0000OOO00 .task_actinfo ['cedents']:#line:701
            print (OO0OOO00OOO000OOO ['cedent_type']+' = '+OO0OOO00OOO000OOO ['generated_string'])#line:702
    def _genvar (OOO000O00O000OO00 ,O000O0OO00O00O0OO ,O000O0O0OOO00OOO0 ,_O00OOOOOOO00O0O00 ,_OOO000O000OOO000O ,_OOO0OOO000OOOO000 ,_O000O0O000O0000OO ,_O0OO00O000O00O00O ):#line:704
        for OOOOOOOOOOOOO0O00 in range (O000O0O0OOO00OOO0 ['num_cedent']):#line:705
            if len (_O00OOOOOOO00O0O00 )==0 or OOOOOOOOOOOOO0O00 >_O00OOOOOOO00O0O00 [-1 ]:#line:706
                _O00OOOOOOO00O0O00 .append (OOOOOOOOOOOOO0O00 )#line:707
                O0OOOOO0000O00O0O =OOO000O00O000OO00 .data ["varname"].index (O000O0O0OOO00OOO0 ['defi'].get ('attributes')[OOOOOOOOOOOOO0O00 ].get ('name'))#line:708
                _O000OOO0O0OOO00O0 =O000O0O0OOO00OOO0 ['defi'].get ('attributes')[OOOOOOOOOOOOO0O00 ].get ('minlen')#line:709
                _OO00000OO0OO00000 =O000O0O0OOO00OOO0 ['defi'].get ('attributes')[OOOOOOOOOOOOO0O00 ].get ('maxlen')#line:710
                _OOO00O00OO0OO0O0O =O000O0O0OOO00OOO0 ['defi'].get ('attributes')[OOOOOOOOOOOOO0O00 ].get ('type')#line:711
                OOO00OOO0OO00000O =len (OOO000O00O000OO00 .data ["dm"][O0OOOOO0000O00O0O ])#line:712
                _OOOO0000O0O0O0OO0 =[]#line:713
                _OOO000O000OOO000O .append (_OOOO0000O0O0O0OO0 )#line:714
                _O0O0OOOOOO0OO00O0 =int (0 )#line:715
                OOO000O00O000OO00 ._gencomb (O000O0OO00O00O0OO ,O000O0O0OOO00OOO0 ,_O00OOOOOOO00O0O00 ,_OOO000O000OOO000O ,_OOOO0000O0O0O0OO0 ,_OOO0OOO000OOOO000 ,_O0O0OOOOOO0OO00O0 ,OOO00OOO0OO00000O ,_OOO00O00OO0OO0O0O ,_O000O0O000O0000OO ,_O0OO00O000O00O00O ,_O000OOO0O0OOO00O0 ,_OO00000OO0OO00000 )#line:716
                _OOO000O000OOO000O .pop ()#line:717
                _O00OOOOOOO00O0O00 .pop ()#line:718
    def _gencomb (OOOOOOO00OOOOO0OO ,OOO0O000OOOOO0O00 ,O0OO00OOOO00O0OOO ,_OO00OO0OO0OOO0OOO ,_O0OO00OO00O0O0000 ,_O0O00O0OOOOOO0OO0 ,_O0O0OOO0000OOO0O0 ,_OO0O00O0OO0O000O0 ,OO00OO0OOOOOOO0O0 ,_OO0O00000OOO0OOOO ,_OOO0OOO0000OOOO0O ,_OO0OOOO0O00OOO0O0 ,_O00OO0O0O000O0OOO ,_OO000OO0OOOOOOOOO ):#line:720
        _OOOOO00O0OOO00OOO =[]#line:721
        if _OO0O00000OOO0OOOO =="subset":#line:722
            if len (_O0O00O0OOOOOO0OO0 )==0 :#line:723
                _OOOOO00O0OOO00OOO =range (OO00OO0OOOOOOO0O0 )#line:724
            else :#line:725
                _OOOOO00O0OOO00OOO =range (_O0O00O0OOOOOO0OO0 [-1 ]+1 ,OO00OO0OOOOOOO0O0 )#line:726
        elif _OO0O00000OOO0OOOO =="seq":#line:727
            if len (_O0O00O0OOOOOO0OO0 )==0 :#line:728
                _OOOOO00O0OOO00OOO =range (OO00OO0OOOOOOO0O0 -_O00OO0O0O000O0OOO +1 )#line:729
            else :#line:730
                if _O0O00O0OOOOOO0OO0 [-1 ]+1 ==OO00OO0OOOOOOO0O0 :#line:731
                    return #line:732
                O0OO0OOOOO0OO0OOO =_O0O00O0OOOOOO0OO0 [-1 ]+1 #line:733
                _OOOOO00O0OOO00OOO .append (O0OO0OOOOO0OO0OOO )#line:734
        elif _OO0O00000OOO0OOOO =="lcut":#line:735
            if len (_O0O00O0OOOOOO0OO0 )==0 :#line:736
                O0OO0OOOOO0OO0OOO =0 ;#line:737
            else :#line:738
                if _O0O00O0OOOOOO0OO0 [-1 ]+1 ==OO00OO0OOOOOOO0O0 :#line:739
                    return #line:740
                O0OO0OOOOO0OO0OOO =_O0O00O0OOOOOO0OO0 [-1 ]+1 #line:741
            _OOOOO00O0OOO00OOO .append (O0OO0OOOOO0OO0OOO )#line:742
        elif _OO0O00000OOO0OOOO =="rcut":#line:743
            if len (_O0O00O0OOOOOO0OO0 )==0 :#line:744
                O0OO0OOOOO0OO0OOO =OO00OO0OOOOOOO0O0 -1 ;#line:745
            else :#line:746
                if _O0O00O0OOOOOO0OO0 [-1 ]==0 :#line:747
                    return #line:748
                O0OO0OOOOO0OO0OOO =_O0O00O0OOOOOO0OO0 [-1 ]-1 #line:749
            _OOOOO00O0OOO00OOO .append (O0OO0OOOOO0OO0OOO )#line:751
        else :#line:752
            print ("Attribute type "+_OO0O00000OOO0OOOO +" not supported.")#line:753
            return #line:754
        for O0OO0OOO00O000000 in _OOOOO00O0OOO00OOO :#line:757
                _O0O00O0OOOOOO0OO0 .append (O0OO0OOO00O000000 )#line:759
                _O0OO00OO00O0O0000 .pop ()#line:760
                _O0OO00OO00O0O0000 .append (_O0O00O0OOOOOO0OO0 )#line:761
                _O00O00000OOO0O00O =_OO0O00O0OO0O000O0 |OOOOOOO00OOOOO0OO .data ["dm"][OOOOOOO00OOOOO0OO .data ["varname"].index (O0OO00OOOO00O0OOO ['defi'].get ('attributes')[_OO00OO0OO0OOO0OOO [-1 ]].get ('name'))][O0OO0OOO00O000000 ]#line:765
                _O0O0OOOOOOOO000O0 =1 #line:767
                if (len (_OO00OO0OO0OOO0OOO )<_OOO0OOO0000OOOO0O ):#line:768
                    _O0O0OOOOOOOO000O0 =0 #line:769
                if (len (_O0OO00OO00O0O0000 [-1 ])>=_O00OO0O0O000O0OOO ):#line:770
                    _OO00000OOOO0OOO0O =0 #line:771
                    if O0OO00OOOO00O0OOO ['defi'].get ('type')=='con':#line:772
                        _OO00000OOOO0OOO0O =_O0O0OOO0000OOO0O0 &_O00O00000OOO0O00O #line:773
                    else :#line:774
                        _OO00000OOOO0OOO0O =_O0O0OOO0000OOO0O0 |_O00O00000OOO0O00O #line:775
                    O0OO00OOOO00O0OOO ['trace_cedent']=_OO00OO0OO0OOO0OOO #line:776
                    O0OO00OOOO00O0OOO ['traces']=_O0OO00OO00O0O0000 #line:777
                    O0OO00OOOO00O0OOO ['generated_string']=OOOOOOO00OOOOO0OO ._print (O0OO00OOOO00O0OOO ,_OO00OO0OO0OOO0OOO ,_O0OO00OO00O0O0000 )#line:778
                    O0OO00OOOO00O0OOO ['filter_value']=_OO00000OOOO0OOO0O #line:779
                    OOO0O000OOOOO0O00 ['cedents'].append (O0OO00OOOO00O0OOO )#line:780
                    OO0OO000OO000OOO0 =OOOOOOO00OOOOO0OO ._verify_opt (OOO0O000OOOOO0O00 ,O0OO00OOOO00O0OOO )#line:781
                    if not (OO0OO000OO000OOO0 ):#line:782
                        if _O0O0OOOOOOOO000O0 ==1 :#line:783
                            if len (OOO0O000OOOOO0O00 ['cedents_to_do'])==len (OOO0O000OOOOO0O00 ['cedents']):#line:784
                                if OOOOOOO00OOOOO0OO .proc =='CFMiner':#line:785
                                    OO000000000O0O000 ,O0O0OOO0O0OOOOO0O =OOOOOOO00OOOOO0OO ._verifyCF (_OO00000OOOO0OOO0O )#line:786
                                elif OOOOOOO00OOOOO0OO .proc =='4ftMiner':#line:787
                                    OO000000000O0O000 ,O0O0OOO0O0OOOOO0O =OOOOOOO00OOOOO0OO ._verify4ft (_O00O00000OOO0O00O )#line:788
                                elif OOOOOOO00OOOOO0OO .proc =='SD4ftMiner':#line:789
                                    OO000000000O0O000 ,O0O0OOO0O0OOOOO0O =OOOOOOO00OOOOO0OO ._verifysd4ft (_O00O00000OOO0O00O )#line:790
                                elif OOOOOOO00OOOOO0OO .proc =='NewAct4ftMiner':#line:791
                                    OO000000000O0O000 ,O0O0OOO0O0OOOOO0O =OOOOOOO00OOOOO0OO ._verifynewact4ft (_O00O00000OOO0O00O )#line:792
                                elif OOOOOOO00OOOOO0OO .proc =='Act4ftMiner':#line:793
                                    OO000000000O0O000 ,O0O0OOO0O0OOOOO0O =OOOOOOO00OOOOO0OO ._verifyact4ft (_O00O00000OOO0O00O )#line:794
                                else :#line:795
                                    print ("Unsupported procedure : "+OOOOOOO00OOOOO0OO .proc )#line:796
                                    exit (0 )#line:797
                                if OO000000000O0O000 ==True :#line:798
                                    O0OOOO00OO0000OO0 ={}#line:799
                                    O0OOOO00OO0000OO0 ["hypo_id"]=OOOOOOO00OOOOO0OO .stats ['total_valid']#line:800
                                    O0OOOO00OO0000OO0 ["cedents"]={}#line:801
                                    for O0000O0000O0OOOO0 in OOO0O000OOOOO0O00 ['cedents']:#line:802
                                        O0OOOO00OO0000OO0 ['cedents'][O0000O0000O0OOOO0 ['cedent_type']]=O0000O0000O0OOOO0 ['generated_string']#line:803
                                    O0OOOO00OO0000OO0 ["params"]=O0O0OOO0O0OOOOO0O #line:805
                                    O0OOOO00OO0000OO0 ["trace_cedent"]=_OO00OO0OO0OOO0OOO #line:806
                                    OOOOOOO00OOOOO0OO ._print_hypo (O0OOOO00OO0000OO0 )#line:807
                                    O0OOOO00OO0000OO0 ["traces"]=_O0OO00OO00O0O0000 #line:810
                                    OOOOOOO00OOOOO0OO .hypolist .append (O0OOOO00OO0000OO0 )#line:811
                            else :#line:812
                                OOOOOOO00OOOOO0OO ._start_cedent (OOO0O000OOOOO0O00 )#line:813
                            OOO0O000OOOOO0O00 ['cedents'].pop ()#line:814
                        if (len (_OO00OO0OO0OOO0OOO )<_OO0OOOO0O00OOO0O0 ):#line:815
                            OOOOOOO00OOOOO0OO ._genvar (OOO0O000OOOOO0O00 ,O0OO00OOOO00O0OOO ,_OO00OO0OO0OOO0OOO ,_O0OO00OO00O0O0000 ,_OO00000OOOO0OOO0O ,_OOO0OOO0000OOOO0O ,_OO0OOOO0O00OOO0O0 )#line:816
                    else :#line:817
                        OOO0O000OOOOO0O00 ['cedents'].pop ()#line:818
                OOOOOOO00OOOOO0OO .stats ['total_cnt']+=1 #line:819
                if len (_O0O00O0OOOOOO0OO0 )<_OO000OO0OOOOOOOOO :#line:820
                    OOOOOOO00OOOOO0OO ._gencomb (OOO0O000OOOOO0O00 ,O0OO00OOOO00O0OOO ,_OO00OO0OO0OOO0OOO ,_O0OO00OO00O0O0000 ,_O0O00O0OOOOOO0OO0 ,_O0O0OOO0000OOO0O0 ,_O00O00000OOO0O00O ,OO00OO0OOOOOOO0O0 ,_OO0O00000OOO0OOOO ,_OOO0OOO0000OOOO0O ,_OO0OOOO0O00OOO0O0 ,_O00OO0O0O000O0OOO ,_OO000OO0OOOOOOOOO )#line:821
                _O0O00O0OOOOOO0OO0 .pop ()#line:822
    def _start_cedent (OO00000O0OO000000 ,O0O0O0OOOO000OO00 ):#line:824
        if len (O0O0O0OOOO000OO00 ['cedents_to_do'])>len (O0O0O0OOOO000OO00 ['cedents']):#line:825
            _O00OO00OOOOO00O00 =[]#line:826
            _O0O0OOO0O0O000O00 =[]#line:827
            OOOO00000OO0000O0 ={}#line:828
            OOOO00000OO0000O0 ['cedent_type']=O0O0O0OOOO000OO00 ['cedents_to_do'][len (O0O0O0OOOO000OO00 ['cedents'])]#line:829
            OOO0O0OO0OO0O0000 =OOOO00000OO0000O0 ['cedent_type']#line:830
            if ((OOO0O0OO0OO0O0000 [-1 ]=='-')|(OOO0O0OO0OO0O0000 [-1 ]=='+')):#line:831
                OOO0O0OO0OO0O0000 =OOO0O0OO0OO0O0000 [:-1 ]#line:832
            OOOO00000OO0000O0 ['defi']=OO00000O0OO000000 .kwargs .get (OOO0O0OO0OO0O0000 )#line:834
            if (OOOO00000OO0000O0 ['defi']==None ):#line:835
                print ("Error getting cedent ",OOOO00000OO0000O0 ['cedent_type'])#line:836
            _O0000O0O0OOOOO0O0 =int (0 )#line:837
            OOOO00000OO0000O0 ['num_cedent']=len (OOOO00000OO0000O0 ['defi'].get ('attributes'))#line:842
            if (OOOO00000OO0000O0 ['defi'].get ('type')=='con'):#line:843
                _O0000O0O0OOOOO0O0 =(1 <<OO00000O0OO000000 .data ["rows_count"])-1 #line:844
            OO00000O0OO000000 ._genvar (O0O0O0OOOO000OO00 ,OOOO00000OO0000O0 ,_O00OO00OOOOO00O00 ,_O0O0OOO0O0O000O00 ,_O0000O0O0OOOOO0O0 ,OOOO00000OO0000O0 ['defi'].get ('minlen'),OOOO00000OO0000O0 ['defi'].get ('maxlen'))#line:845
    def _calc_all (O0OOOOO0OOO00O00O ,**O0O0OOO0O0O000000 ):#line:848
        O0OOOOO0OOO00O00O ._prep_data (O0OOOOO0OOO00O00O .kwargs .get ("df"))#line:849
        O0OOOOO0OOO00O00O ._calculate (**O0O0OOO0O0O000000 )#line:850
    def _calculate (OOO00O00O00O0O000 ,**O00000OOOO0000OO0 ):#line:852
        if OOO00O00O00O0O000 .data ["data_prepared"]==0 :#line:853
            print ("Error: data not prepared")#line:854
            return #line:855
        OOO00O00O00O0O000 .kwargs =O00000OOOO0000OO0 #line:856
        OOO00O00O00O0O000 .proc =O00000OOOO0000OO0 .get ('proc')#line:857
        OOO00O00O00O0O000 .quantifiers =O00000OOOO0000OO0 .get ('quantifiers')#line:858
        OOO00O00O00O0O000 ._init_task ()#line:860
        OOO00O00O00O0O000 .stats ['start_proc_time']=time .time ()#line:861
        OOO00O00O00O0O000 .task_actinfo ['cedents_to_do']=[]#line:862
        OOO00O00O00O0O000 .task_actinfo ['cedents']=[]#line:863
        if O00000OOOO0000OO0 .get ("proc")=='CFMiner':#line:866
            OOO00O00O00O0O000 .task_actinfo ['cedents_to_do']=['cond']#line:867
        elif O00000OOOO0000OO0 .get ("proc")=='4ftMiner':#line:868
            _OO0O0OO0O00O00O0O =O00000OOOO0000OO0 .get ("cond")#line:869
            if _OO0O0OO0O00O00O0O !=None :#line:870
                OOO00O00O00O0O000 .task_actinfo ['cedents_to_do'].append ('cond')#line:871
            else :#line:872
                OOOOOOOO00O00O0OO =OOO00O00O00O0O000 .cedent #line:873
                OOOOOOOO00O00O0OO ['cedent_type']='cond'#line:874
                OOOOOOOO00O00O0OO ['filter_value']=(1 <<OOO00O00O00O0O000 .data ["rows_count"])-1 #line:875
                OOOOOOOO00O00O0OO ['generated_string']='---'#line:876
                OOO00O00O00O0O000 .task_actinfo ['cedents_to_do'].append ('cond')#line:878
                OOO00O00O00O0O000 .task_actinfo ['cedents'].append (OOOOOOOO00O00O0OO )#line:879
            OOO00O00O00O0O000 .task_actinfo ['cedents_to_do'].append ('ante')#line:883
            OOO00O00O00O0O000 .task_actinfo ['cedents_to_do'].append ('succ')#line:884
        elif O00000OOOO0000OO0 .get ("proc")=='NewAct4ftMiner':#line:885
            _OO0O0OO0O00O00O0O =O00000OOOO0000OO0 .get ("cond")#line:888
            if _OO0O0OO0O00O00O0O !=None :#line:889
                OOO00O00O00O0O000 .task_actinfo ['cedents_to_do'].append ('cond')#line:890
            else :#line:891
                OOOOOOOO00O00O0OO =OOO00O00O00O0O000 .cedent #line:892
                OOOOOOOO00O00O0OO ['cedent_type']='cond'#line:893
                OOOOOOOO00O00O0OO ['filter_value']=(1 <<OOO00O00O00O0O000 .data ["rows_count"])-1 #line:894
                OOOOOOOO00O00O0OO ['generated_string']='---'#line:895
                print (OOOOOOOO00O00O0OO ['filter_value'])#line:896
                OOO00O00O00O0O000 .task_actinfo ['cedents_to_do'].append ('cond')#line:897
                OOO00O00O00O0O000 .task_actinfo ['cedents'].append (OOOOOOOO00O00O0OO )#line:898
            OOO00O00O00O0O000 .task_actinfo ['cedents_to_do'].append ('antv')#line:899
            OOO00O00O00O0O000 .task_actinfo ['cedents_to_do'].append ('sucv')#line:900
            OOO00O00O00O0O000 .task_actinfo ['cedents_to_do'].append ('ante')#line:901
            OOO00O00O00O0O000 .task_actinfo ['cedents_to_do'].append ('succ')#line:902
        elif O00000OOOO0000OO0 .get ("proc")=='Act4ftMiner':#line:903
            _OO0O0OO0O00O00O0O =O00000OOOO0000OO0 .get ("cond")#line:906
            if _OO0O0OO0O00O00O0O !=None :#line:907
                OOO00O00O00O0O000 .task_actinfo ['cedents_to_do'].append ('cond')#line:908
            else :#line:909
                OOOOOOOO00O00O0OO =OOO00O00O00O0O000 .cedent #line:910
                OOOOOOOO00O00O0OO ['cedent_type']='cond'#line:911
                OOOOOOOO00O00O0OO ['filter_value']=(1 <<OOO00O00O00O0O000 .data ["rows_count"])-1 #line:912
                OOOOOOOO00O00O0OO ['generated_string']='---'#line:913
                print (OOOOOOOO00O00O0OO ['filter_value'])#line:914
                OOO00O00O00O0O000 .task_actinfo ['cedents_to_do'].append ('cond')#line:915
                OOO00O00O00O0O000 .task_actinfo ['cedents'].append (OOOOOOOO00O00O0OO )#line:916
            OOO00O00O00O0O000 .task_actinfo ['cedents_to_do'].append ('antv-')#line:917
            OOO00O00O00O0O000 .task_actinfo ['cedents_to_do'].append ('antv+')#line:918
            OOO00O00O00O0O000 .task_actinfo ['cedents_to_do'].append ('sucv-')#line:919
            OOO00O00O00O0O000 .task_actinfo ['cedents_to_do'].append ('sucv+')#line:920
            OOO00O00O00O0O000 .task_actinfo ['cedents_to_do'].append ('ante')#line:921
            OOO00O00O00O0O000 .task_actinfo ['cedents_to_do'].append ('succ')#line:922
        elif O00000OOOO0000OO0 .get ("proc")=='SD4ftMiner':#line:923
            _OO0O0OO0O00O00O0O =O00000OOOO0000OO0 .get ("cond")#line:926
            if _OO0O0OO0O00O00O0O !=None :#line:927
                OOO00O00O00O0O000 .task_actinfo ['cedents_to_do'].append ('cond')#line:928
            else :#line:929
                OOOOOOOO00O00O0OO =OOO00O00O00O0O000 .cedent #line:930
                OOOOOOOO00O00O0OO ['cedent_type']='cond'#line:931
                OOOOOOOO00O00O0OO ['filter_value']=(1 <<OOO00O00O00O0O000 .data ["rows_count"])-1 #line:932
                OOOOOOOO00O00O0OO ['generated_string']='---'#line:933
                print (OOOOOOOO00O00O0OO ['filter_value'])#line:934
                OOO00O00O00O0O000 .task_actinfo ['cedents_to_do'].append ('cond')#line:935
                OOO00O00O00O0O000 .task_actinfo ['cedents'].append (OOOOOOOO00O00O0OO )#line:936
            OOO00O00O00O0O000 .task_actinfo ['cedents_to_do'].append ('frst')#line:937
            OOO00O00O00O0O000 .task_actinfo ['cedents_to_do'].append ('scnd')#line:938
            OOO00O00O00O0O000 .task_actinfo ['cedents_to_do'].append ('ante')#line:939
            OOO00O00O00O0O000 .task_actinfo ['cedents_to_do'].append ('succ')#line:940
        else :#line:941
            print ("Unsupported procedure")#line:942
            return #line:943
        print ("Will go for ",O00000OOOO0000OO0 .get ("proc"))#line:944
        OOO00O00O00O0O000 .task_actinfo ['optim']={}#line:947
        O0OO0O000OO0O0O0O =True #line:948
        for O0000OO0000OO0O0O in OOO00O00O00O0O000 .task_actinfo ['cedents_to_do']:#line:949
            try :#line:950
                OO0OO00O0O00O00OO =OOO00O00O00O0O000 .kwargs .get (O0000OO0000OO0O0O )#line:951
                if OO0OO00O0O00O00OO .get ('type')!='con':#line:954
                    O0OO0O000OO0O0O0O =False #line:955
            except :#line:956
                O0O0O0OO00OOOOOO0 =1 <2 #line:957
        OOOO0O0000OOOO0OO ={}#line:958
        OOOO0O0000OOOO0OO ['only_con']=O0OO0O000OO0O0O0O #line:959
        OOO00O00O00O0O000 .task_actinfo ['optim']=OOOO0O0000OOOO0OO #line:960
        print ("Starting to mine rules.")#line:967
        OOO00O00O00O0O000 ._start_cedent (OOO00O00O00O0O000 .task_actinfo )#line:968
        OOO00O00O00O0O000 .stats ['end_proc_time']=time .time ()#line:970
        print ("Done. Total verifications : "+str (OOO00O00O00O0O000 .stats ['total_cnt'])+", hypotheses "+str (OOO00O00O00O0O000 .stats ['total_valid'])+",control number:"+str (OOO00O00O00O0O000 .stats ['control_number'])+", times: prep "+str (OOO00O00O00O0O000 .stats ['end_prep_time']-OOO00O00O00O0O000 .stats ['start_prep_time'])+", processing "+str (OOO00O00O00O0O000 .stats ['end_proc_time']-OOO00O00O00O0O000 .stats ['start_proc_time']))#line:973
        OO0000OO0O0O0OO0O ={}#line:974
        O00O0O00O0O0OOO00 ={}#line:975
        O00O0O00O0O0OOO00 ["task_type"]=O00000OOOO0000OO0 .get ('proc')#line:976
        O00O0O00O0O0OOO00 ["target"]=O00000OOOO0000OO0 .get ('target')#line:978
        O00O0O00O0O0OOO00 ["self.quantifiers"]=OOO00O00O00O0O000 .quantifiers #line:979
        if O00000OOOO0000OO0 .get ('cond')!=None :#line:981
            O00O0O00O0O0OOO00 ['cond']=O00000OOOO0000OO0 .get ('cond')#line:982
        if O00000OOOO0000OO0 .get ('ante')!=None :#line:983
            O00O0O00O0O0OOO00 ['ante']=O00000OOOO0000OO0 .get ('ante')#line:984
        if O00000OOOO0000OO0 .get ('succ')!=None :#line:985
            O00O0O00O0O0OOO00 ['succ']=O00000OOOO0000OO0 .get ('succ')#line:986
        OO0000OO0O0O0OO0O ["taskinfo"]=O00O0O00O0O0OOO00 #line:987
        OOO00O0OOO0O0OOOO ={}#line:988
        OOO00O0OOO0O0OOOO ["total_verifications"]=OOO00O00O00O0O000 .stats ['total_cnt']#line:989
        OOO00O0OOO0O0OOOO ["valid_hypotheses"]=OOO00O00O00O0O000 .stats ['total_valid']#line:990
        OOO00O0OOO0O0OOOO ["time_prep"]=OOO00O00O00O0O000 .stats ['end_prep_time']-OOO00O00O00O0O000 .stats ['start_prep_time']#line:991
        OOO00O0OOO0O0OOOO ["time_processing"]=OOO00O00O00O0O000 .stats ['end_proc_time']-OOO00O00O00O0O000 .stats ['start_proc_time']#line:992
        OOO00O0OOO0O0OOOO ["time_total"]=OOO00O00O00O0O000 .stats ['end_prep_time']-OOO00O00O00O0O000 .stats ['start_prep_time']+OOO00O00O00O0O000 .stats ['end_proc_time']-OOO00O00O00O0O000 .stats ['start_proc_time']#line:993
        OO0000OO0O0O0OO0O ["summary_statistics"]=OOO00O0OOO0O0OOOO #line:994
        OO0000OO0O0O0OO0O ["hypotheses"]=OOO00O00O00O0O000 .hypolist #line:995
        OO0O0OO00OO00O0O0 ={}#line:996
        OO0O0OO00OO00O0O0 ["varname"]=OOO00O00O00O0O000 .data ["varname"]#line:997
        OO0O0OO00OO00O0O0 ["catnames"]=OOO00O00O00O0O000 .data ["catnames"]#line:998
        OO0000OO0O0O0OO0O ["datalabels"]=OO0O0OO00OO00O0O0 #line:999
        OOO00O00O00O0O000 .result =OO0000OO0O0O0OO0O #line:1001
