import pandas as pd, numpy as np, plotly.express as px
from dorianUtils.configFilesD import ConfigDashTagUnitTimestamp
from dorianUtils.configFilesD import ConfigDashRealTime
from dorianUtils.configFilesD import ConfigDashSpark
import subprocess as sp, os,re,glob, datetime as dt
from dateutil import parser
from scipy import linalg,integrate
pd.options.mode.chained_assignment = None  # default='warn'
class EmptyClass():pass


class SmallPowerMaster():
    def __init__(self):
        self.appDir  = os.path.dirname(os.path.realpath(__file__))
        self.confFolder = self.appDir + '/confFiles/'
        from PIL import Image # new import
        self._loadcolorPalettes()
        self.imgpeintre  = Image.open(self.confFolder + 'peintrepalette.jpeg')
        self.sylfenlogo  = Image.open(self.confFolder +  'logo_sylfen.png')
        self._loadConstants()

    def _loadConstants(self):
        self.cst = EmptyClass()
        dfConstants=pd.read_excel(self.confFolder + 'materialConstants.xlsx',sheet_name='thermo')
        dfConstants.columns=['description','variableName','value','unit']
        dfConstants = dfConstants.set_index('variableName')
        dfConstants = dfConstants[['value','description','unit']]
        self.dfConstants = dfConstants.dropna()
        for k in self.dfConstants.index:
            setattr(self.cst,k,self.dfConstants.loc[k].value)

    def _loadcolorPalettes(self):
        import pickle
        colPal = pickle.load(open(self.confFolder+'palettes.pkl','rb'))
        colPal['reds']     = colPal['reds'].drop(['Misty rose',])
        colPal['greens']   = colPal['greens'].drop(['Honeydew',])
        colPal['blues']    = colPal['blues'].drop(['Blue (Munsell)','Powder Blue','Duck Blue','Teal blue'])
        colPal['magentas'] = colPal['magentas'].drop(['Pale Purple','English Violet'])
        colPal['cyans']    = colPal['cyans'].drop(['Azure (web)',])
        colPal['yellows']  = colPal['yellows'].drop(['Light Yellow',])
        self.colorPalettes = colPal
        self.colorshades = ['greens','blues','reds','magentas','oranges','yellows','cyans','blacks']
        for c in self.colorshades:
            self.colorPalettes[c]=self.colorPalettes[c].sample(frac=1)


    # ==============================================================================
    #                   computation functions
    # ==============================================================================
    def DF_allPower(self,timeRange=None,whichPower='HE10',**kwargs):
        dfs=[]
        for group in self.powerGroups.index[:-1]:
            listTags = self.getTagsTU(self.powerGroups.loc[group].pattern)
            tagsHE = [k for k in listTags if len(re.findall('\.HE1\d{1}$',k))>0]
            tagsnotHE = [l for l in listTags if l not in tagsHE]
            listTags = tagsnotHE + [k for k in tagsHE if whichPower in k]
            print(listTags)
            df = self.DF_loadTimeRangeTags(timeRange,listTags,**kwargs)
            if not df.empty:
                if 'courant' in group.lower():
                    df=df*self.powerGroups.loc[group].voltage
                df=df.abs()# take absolute value of the power
                df['timestamp'] = df.index
                df=df.melt(id_vars='timestamp',ignore_index=True)
                df['Power group'] = group
                dfs.append(df)

        dfPtotal = self.DF_loadTimeRangeTags(timeRange,self.getTagsTU('SEH0\.JT_01\.'+whichPower),**kwargs)
        # dfPtotal = dfPtotal.ffill().bfill()
        df = pd.concat(dfs,axis=0)
        return df,dfPtotal

    def rendementCondenseur(self,timeRange_Window,fuites=0,nb='01',wholeDF=False,**kwargs):
        '''
        - timeRange_Window : int if realTime==True --> ex : 60*30*2
        [str,str] if not realtime --> ex : ['2021-08-12 9:00','2020-08-13 18:00']'''
        debit_eau = 'SEH1.L219_H2OP_FT_01.HM05'#g/min
        t_entree_condenseur='SEH1.HPB_CND_'+ nb +'_TT_01.HM05'
        t_sortie_condenseur='SEH1.HPB_CND_'+ nb +'_TT_03.HM05'
        listTags = [debit_eau,t_entree_condenseur,t_sortie_condenseur]
        if isinstance(timeRange_Window,list) :
            df   = self.DF_loadTimeRangeTags(timeRange_Window,listTags,**kwargs)
        else :
            df   = self.realtimeTagsDF(listTags,timeWindow=timeRange_Window,**kwargs)
        if not df.empty:
            df = df[listTags]
            df.columns =['debit_eau(g/min)','t_entree_condenseur','t_sortie_condenseur']

            dfTh=pd.DataFrame()
            dfTh['debit eau(g/s)'] = df['debit_eau(g/min)']/60
            dfTh['debit g/s(yc fuites)'] = dfTh['debit eau(g/s)']*(1-fuites)
            dfTh['refroidissement vapeur'] = (dfTh['debit g/s(yc fuites)']*self.cst.Cp_eau_vap*(df['t_entree_condenseur']-100)).apply(lambda x :max(0,x))
            dfTh['condensation'] = dfTh['debit g/s(yc fuites)']*self.cst.Cl_H2O
            dfTh['Refroidissement eau condensée'] = (dfTh['debit g/s(yc fuites)']*self.cst.Cp_eau_liq*(100-df['t_sortie_condenseur'])).apply(lambda x :max(0,x))
            dfTh['thermique azote'] = 3.9/60/22.4*self.cst.Mmol_N2*self.cst.Cp_N2*(df['t_entree_condenseur']-df['t_sortie_condenseur'])*(1-fuites)

            dfTh['total thermique'] = dfTh.sum(axis=1)
            df.columns=[k + ' : ' + l  for k,l in zip(df.columns,listTags)]
            df = pd.concat([df,dfTh],axis=1)
            if wholeDF:return df
            else :return df['total thermique']
        else : return df

    def bilanValo(self,timeRange_Window,nb='01',wholeDF=False,**kwargs):
        '''
        - timeRange_Window : int if realTime==True --> ex : 60*30*2
        [str,str] if not realtime --> ex : ['2021-08-12 9:00','2020-08-13 18:00']'''
        debit_eau = 'SEH1.L408_H2OR_FT_01.HM05'#g/min
        t_entree_valo='SEH1.HPB_CND_'+ nb +'_TT_02.HM05'
        t_sortie_valo='SEH1.HPB_CND_'+ nb +'_TT_04.HM05'
        listTags = [debit_eau,t_entree_valo,t_sortie_valo]
        if isinstance(timeRange_Window,list) :
            df   = self.DF_loadTimeRangeTags(timeRange_Window,listTags,**kwargs)
        else :
            df   = self.realtimeTagsDF(listTags,timeWindow=timeRange_Window,**kwargs)
        if not df.empty:
            df.columns = ['debit_eau(kg/h)','t_entree_valo','t_sortie_valo']

            dfValo = pd.DataFrame()
            dfValo['debit eau(g/s)'] = df['debit_eau(kg/h)']*1000/3600
            dfValo['echange valo'] = dfValo['debit eau(g/s)']*self.cst.Cp_eau_liq*(df['t_sortie_valo']-df['t_entree_valo'])
            df.columns=[k + ' : ' + l  for k,l in zip(df.columns,listTags)]
            df = pd.concat([df,dfValo],axis=1)
            if wholeDF:return df
            else :return df['echange valo']
        else : return df

    def rendement_GV(self,timeRange_Window,activePower=True,wholeDF=False,**kwargs):
        '''
        - activePower : active or apparente power
        - timeRange_Window : int if realTime==True --> ex : 60*30*2
        [str,str] if not realtime --> ex : ['2021-08-12 9:00','2020-08-13 18:00']'''

        debit_eau = 'SEH1.L213_H2OPa_FT_01.HM05'#g/min
        if activePower:p_chauffants = self.getTagsTU('HPB_STG_01a.*JT.*HE10')
        else: p_chauffants = self.getTagsTU('HPB_STG_01a.*JT.*HE16')
        t_entree_GV = 'SEH1.L211_H2OP_TT_01.HM05'
        t_sortie_GV = 'SEH1.L036_FUEL_TT_01.HM05'

        listTags = [debit_eau]+p_chauffants+[t_entree_GV,t_sortie_GV]
        if isinstance(timeRange_Window,list) :
            df   = self.DF_loadTimeRangeTags(timeRange_Window,listTags,**kwargs)
        else :
            df   = self.realtimeTagsDF(listTags,timeWindow=timeRange_Window,**kwargs)
        if not df.empty:
            df = df[listTags]
            df.columns = ['debit_eau(g/min)','power_gv1','power_gv2','power_gv3','t_entree_GV','t_sortie_GV']

            dfGV = pd.DataFrame()
            dfGV['debit eau(g/s)'] = df['debit_eau(g/min)']/60

            dfGV['power chauffe eau liq']  = (dfGV['debit eau(g/s)']*self.cst.Cp_eau_liq*(100-df['t_entree_GV'])).apply(lambda x :max(0,x))
            dfGV['power vaporisation eau'] = dfGV['debit eau(g/s)']*self.cst.Cl_H2O
            dfGV['power chauffe vapeur']   = (dfGV['debit eau(g/s)']*self.cst.Cp_eau_vap*(df['t_sortie_GV']-100)).apply(lambda x :max(0,x))
            dfGV['power total chauffe']   = dfGV.sum(axis=1)
            dfGV['power elec chauffe'] = df['power_gv1']+df['power_gv2']+df['power_gv3']
            dfGV['rendement GV'] = dfGV['power total chauffe']/dfGV['power elec chauffe']
            gv = dfGV['rendement GV']
            gv[dfGV['power elec chauffe']<20]=np.nan
            dfGV['rendement GV'] = gv*100
            df.columns=[k + ' : ' + l  for k,l in zip(df.columns,listTags)]
            df = pd.concat([df,dfGV],axis=1)
            if wholeDF:return df
            else :return df['rendement GV']
        else : return df

    def pertesThermiquesStack(self,timeRange_Window,fuel='N2',wholeDF=False,activePower=True,**kwargs):
        air_entreeStack = 'SEH1.HTBA_HEX_02_TT_01.HM05'
        air_balayage = 'SEH1.HPB_HEX_02_TT_02.HM05'
        fuel_entreeStack = 'SEH1.HTBF_HEX_01_TT_01.HM05'
        TstackAir = 'SEH1.STB_GFC_02_TT_01.HM05'
        TstackFuel = 'SEH1.STB_GFC_01_TT_01.HM05'
        debitAir = 'SEH01.L138_O2_FT_01.HM05'
        debitFuel = 'SEH1.L032_FUEL_FT_01.HM05'
        if activePower:p_chauffants = self.getTagsTU('STK_HER.*JT.*HE10')
        else :p_chauffants = self.getTagsTU('STK_HER.*JT.*HE16')

        # debitFuel = 'SEH1.L034_H2_FT_01.HM05'
        listTags = [air_entreeStack,air_balayage,fuel_entreeStack,TstackAir,TstackFuel,debitAir,debitFuel]+p_chauffants
        if isinstance(timeRange_Window,list) :
            df   = self.DF_loadTimeRangeTags(timeRange_Window,listTags,**kwargs)
        else :
            df   = self.realtimeTagsDF(listTags,timeWindow=timeRange_Window,**kwargs)
        if not df.empty:
            df = df[listTags]
            df.columns = ['air_entreeStack','air_balayage','fuel_entreeStack',
                        'TstackAir','TstackFuel','debitAir(Nl/mn)','debitFuel(Nl/mn)','p_her1','p_her2','p_her3']
            dfPertes = pd.DataFrame()
            cp_fuel,M_fuel = self.dfConstants.loc['Cp_' + fuel,'value'],self.dfConstants.loc['Mmol_' + fuel,'value']
            dfPertes['surchauffe_Air']  = (df['TstackAir']-df['air_entreeStack'])*self.cst.Cp_air*self.cst.Mmol_Air*df['debitAir(Nl/mn)']/22.4/60
            dfPertes['surchauffe_Fuel'] = (df['TstackFuel']-df['fuel_entreeStack'])*cp_fuel*M_fuel*df['debitFuel(Nl/mn)']/22.4/60
            dfPertes['surchauffe_AirBalayage'] = (df['TstackAir']-df['air_entreeStack'])*self.cst.Cp_air*self.cst.Mmol_Air*df['debitAir(Nl/mn)']/22.4/60
            dfPertes['total puissance surchauffe gaz']=dfPertes.sum(axis=1)
            dfPertes['puissance four(W)'] = df['p_her1']+df['p_her2']+df['p_her3']
            dfPertes['pertes stack'] = dfPertes['puissance four(W)']-dfPertes['total puissance surchauffe gaz']

            df.columns=[k + ' : ' + l  for k,l in zip(df.columns,listTags)]
            df = pd.concat([df,dfPertes],axis=1)
            if wholeDF : return df
            else : return df['pertes stack']
        else :
            return df

    def rendement_blower(self,timeRange_Window,wholeDF=True,activePower=True,**kwargs):
        debitAir = self.getTagsTU('138.*FT')
        pressionAmont = self.getTagsTU('131.*PT')
        pressionAval = self.getTagsTU('138.*PT')
        puissanceBlowers = self.getTagsTU('blr.*02.*JT')
        t_aval = self.getTagsTU('l126')
        listTags = debitAir+pressionAmont+pressionAval+t_aval+puissanceBlowers

        if isinstance(timeRange_Window,list) :
            df   = self.DF_loadTimeRangeTags(timeRange_Window,listTags,**kwargs)
        else :
            df   = self.realtimeTagsDF(listTags,timeWindow=timeRange_Window,**kwargs)
        if not df.empty:
            df = df[listTags]
            df.columns = ['debitAir(Nl/min)','pressionAmont2a(mbarg)','pressionAmont2b(mbarg)','pressionAval(mbarg)',
                            'temperature aval','puissance blower 2a','puissance blower 2b']
            dfBlower = pd.DataFrame()
            dfBlower['debit air(Nm3/s)'] = df['debitAir(Nl/min)']/1000/60
            dfBlower['deltaP2a(Pa)'] = (df['pressionAval(mbarg)']-df['pressionAmont2a(mbarg)'])*100
            dfBlower['deltaP2b(Pa)'] = (df['pressionAval(mbarg)']-df['pressionAmont2b(mbarg)'])*100
            dfBlower['deltaP2mean(Pa)'] = (dfBlower['deltaP2a(Pa)']+dfBlower['deltaP2b(Pa)'])/2
            dfBlower['puissance hydraulique(W)'] = dfBlower['debit air(Nm3/s)']*dfBlower['deltaP2mean(Pa)']
            dfBlower['puissance electrique(W)'] = df['puissance blower 2a']+df['puissance blower 2b']
            dfBlower['rendement blower'] = dfBlower['puissance hydraulique(W)']/dfBlower['puissance electrique(W)']*100

            df.columns=[k + ' : ' + l  for k,l in zip(df.columns,listTags)]
            df = pd.concat([df,dfBlower],axis=1)
            if wholeDF : return df
            else : return df['rendement blower']
        else : return df

    def rendement_pumps(self,timeRange_Window,wholeDF=True,activePower=True,**kwargs):
        debit_eau_1  = 'SEH1.L213_H2OPa_FT_01.HM05'
        debit_eau_2  = 'SEH1.L213_H2OPb_FT_01.HM05'
        t_aval       = 'SEH1.L036_FUEL_TT_01.HM05'
        pressionAval = 'SEH1.L036_FUEL_PT_01.HM05'
        puissancePump = 'SEH0.GWPBC_PMP_01_JT_01.HE10'
        puissancePump_var = 'SEH0.GWPBC_PMP_01_JT_01.HE13'
        listTags = [debit_eau_1,debit_eau_2,t_aval,pressionAval,puissancePump,puissancePump_var]

        if isinstance(timeRange_Window,list) :
            df   = self.DF_loadTimeRangeTags(timeRange_Window,listTags,**kwargs)
        else :
            df   = self.realtimeTagsDF(listTags,timeWindow=timeRange_Window,**kwargs)
        if not df.empty:
            df = df[listTags]
            df.columns = ['debit eau1(g/min)','debit eau2(g/min)','temperature aval',
            'pressionAval(mbarg)','puissance pump(W)','puissance pump reactive (VAR)']
            dfPump = pd.DataFrame()
            dfPump['debit eau total(Nm3/s)'] = (df['debit eau1(g/min)']+df['debit eau2(g/min)'])/1000000/60
            dfPump['pression sortie(Pa)'] = (df['pressionAval(mbarg)'])*100
            dfPump['puissance hydraulique(W)'] = dfPump['debit eau total(Nm3/s)']*dfPump['pression sortie(Pa)']
            dfPump['rendement pompe'] = dfPump['puissance hydraulique(W)']/df['puissance pump(W)']*100
            dfPump['cosphiPmp'] = df['puissance pump(W)']/(df['puissance pump(W)']+df['puissance pump reactive (VAR)'])

            df.columns=[k + ' : ' + l  for k,l in zip(df.columns,listTags)]
            df = pd.concat([df,dfPump],axis=1)
            if wholeDF : return df
            else : return df['rendement blower']
        else : return df

    def cosphi(self,timeRange_Window,**kwargs):
        lreactive = self.getTagsTU('HE13')
        lapparente = self.getTagsTU('HE16')
        listTags = self.getTagsTU('HE1')
        if isinstance(timeRange_Window,list):
            df = self.DF_loadTimeRangeTags(timeRange_Window,listTags,**kwargs)
        else:
            df = self.realtimeTagsDF(listTags,timeWindow=timeRange_Window,**kwargs)
        if not df.empty:
            dfcosphi = pd.DataFrame()
            for k in lreactive : dfcosphi['cosphi' + k] = df[k[:-1]+'0']/(df[k[:-1]+'0']+df[k])
            for k in lapparente : dfcosphi['cosphi' + k] = df[k[:-1]+'0']/df[k]
        return dfcosphi

    # ==============================================================================
    #                   plot functions
    # ==============================================================================
    def plotGraphPowerArea(self,timeRange,whichPower='HE10',expand='groups',groupnorm='',**kwargs):
        import plotly.express as px
        import plotly.graph_objects as go
        # df,dfPtotal,dicPowerGroups = self.DF_allPower(timeRange,melt=True,**kwargs)
        df,dfPtotal = self.DF_allPower(timeRange,whichPower=whichPower,**kwargs)

        if expand=='tags' :fig=px.area(df,x='timestamp',y='value',color='tag',groupnorm=groupnorm)
        elif expand=='groups' :
            fig=px.area(df,x='timestamp',y='value',color='Power group',groupnorm=groupnorm,line_group='tag')
            fig.update_layout(legend=dict(orientation="h"))
        try:
            traceP = go.Scatter(x=dfPtotal.index,y=dfPtotal.iloc[:,0],name='SEH0.JT_01.'+ whichPower+'(puissance totale)',
                mode='lines+markers',marker=dict(color='blue'))
            fig.add_trace(traceP)
        except:print('total power SEH0.JT_01.'+ whichPower +'IS EMPTY')
        fig.update_layout(yaxis_title='power in W')
        return fig

    def updateLayoutMultiUnitGraph(self,fig,sizeDots=10):
        fig.update_yaxes(showgrid=False)
        fig.update_traces(marker=dict(size=sizeDots))
        fig.update_layout(height=900)
        fig.update_traces(hovertemplate='<b>%{y:.1f}')
        return fig

    def plotMultiUnitGraph(self,timeRange,listTags=[],**kwargs):
        if not listTags : listTags=self.get_randomListTags()
        tagMapping = {t:self.getUnitofTag(t) for t in listTags}
        df  = self.DF_loadTimeRangeTags(timeRange,listTags,**kwargs)
        return self.utils.multiUnitGraph(df,tagMapping)

    def checkCondenseur(self,timeRange_Window,**kwargs):
        df = self.rendementCondenseur(timeRange_Window,wholeDF=True,**kwargs)
        dictGroups={t:v for t,v in zip(df.columns,['g/min','C','C','g/s','g/s','W','W','W','W','W'])}
        fig = self.utils.multiUnitGraph(df,dictGroups)
        fig.update_traces(marker_size=5)
        fig.update_yaxes(showgrid=False)
        fig.update_traces(hovertemplate="%{y:.2f}")
        return fig

    def checkValo(self,timeRange_Window,**kwargs):
        df = self.bilanValo(timeRange_Window,wholeDF=True,**kwargs)
        dictGroups={t:v for t,v in zip(df.columns,['kg/h','C','C','g/s','W'])}
        fig = self.utils.multiUnitGraph(df,dictGroups)
        fig.update_traces(marker_size=5)
        fig.update_yaxes(showgrid=False)
        fig.update_traces(hovertemplate="%{y:.2f}")
        return fig

    def checkRendementGV(self,timeRange_Window,subplot=False,**kwargs):
        df = self.rendement_GV(timeRange_Window,wholeDF=True,**kwargs)

        if subplot:
            dictdictGroups ={}
            dictdictGroups['tags'] = {t:v for t,v in zip(df.columns[:6],['W','W','W','C','C','g/min'])}
            dictdictGroups['calculated'] = {t:v for t,v in zip(df.columns[6:],['C','g/s','W','W','W','W','W','%'])}
            fig=utils.multiUnitGraphSubPlots(df,dictdictGroups)
        else :
            dictGroups={t:v for t,v in zip(df.columns,['g/min','W','W','W','C','C','g/s','W','W','W','W','W','%'])}
            fig = self.utils.multiUnitGraph(df,dictGroups)

        fig.update_traces(marker_size=5)
        fig.update_yaxes(showgrid=False)
        fig.update_traces(hovertemplate="%{y:.2f}")
        return fig

    def checkPertesStack(self,timeRange_Window,**kwargs):
        df = self.pertesThermiquesStack(timeRange_Window,wholeDF=True,**kwargs)
        dictGroups={t:v for t,v in zip(df.columns,['°C','°C','°C','°C','°C','Nl/mn','Nl/mn','W','W','W','W','W','W','W','W','W',])}
        fig = self.utils.multiUnitGraph(df,dictGroups)
        fig.update_traces(marker_size=5)
        fig.update_yaxes(showgrid=False)
        fig.update_traces(hovertemplate="%{y:.2f}")
        return fig

    def checkBlowers(self,timeRange_Window,**kwargs):
        df = self.rendement_blower(timeRange_Window,wholeDF=True,**kwargs)
        dictGroups={t:v for t,v in zip(df.columns,['Nl/mn','mbarg','mbarg','mbarg','°C','W','W','Nm3/s','Pa','Pa','Pa','W','W','%'])}
        fig = self.utils.multiUnitGraph(df,dictGroups)
        fig.update_traces(marker_size=5)
        fig.update_yaxes(showgrid=False)
        fig.update_traces(hovertemplate="%{y:.2f}")
        return fig

    def checkCosphi(self,timeRange_Window,**kwargs):
        df = self.cosphi(timeRange_Window,**kwargs)
        fig = px.scatter(df)
        fig.update_traces(mode='lines+markers',hovertemplate="%{y:.2f}")
        return fig

    def multiUnitGraphShades(self,df):
        tagMapping = {t:self.getUnitofTag(t) for t in df.columns}
        fig = self.utils.multiUnitGraph(df,tagMapping)
        dfGroups = self.utils.getLayoutMultiUnit(tagMapping)[1]
        listCols = dfGroups.color.unique()
        for k1,g in enumerate(listCols):
            colname = self.colorshades[k1]
            shades = self.colorPalettes[colname]['hex']
            names2change = dfGroups[dfGroups.color==g].index
            fig.update_yaxes(selector={'gridcolor':g},
                        title_font_color=colname[:-1],gridcolor=colname[:-1],tickfont_color=colname[:-1])
            shade=0
            for d in fig.data:
                if d.name in names2change:
                    d['marker']['color'] = shades[shade]
                    d['line']['color']   = shades[shade]
                    shade+=1
            fig.update_yaxes(showgrid=False)
            fig.update_traces(marker=dict(size=7))
            fig.update_layout(height=800)
            fig.update_xaxes(showgrid=False)
            fig.update_traces(hovertemplate='<b>%{y:.1f}')

        fig.add_layout_image(dict(source=self.imgpeintre,xref="paper",yref="paper",x=0.05,y=1,
                                    sizex=0.9,sizey=1,sizing="stretch",opacity=0.5,layer="below"))
        # fig.update_layout(template="plotly_white")
        fig.add_layout_image(
            dict(
                source=self.sylfenlogo,
                xref="paper", yref="paper",
                x=0., y=1.02,
                sizex=0.12, sizey=0.12,
                xanchor="left", yanchor="bottom"
            )
        )
        return fig

class ConfigFilesSmallPower(ConfigDashTagUnitTimestamp,SmallPowerMaster):
    # ==========================================================================
    #                       INIT FUNCTIONS
    # ==========================================================================

    def __init__(self,folderPkl,encode='utf-8'):
        SmallPowerMaster.__init__(self)
        ConfigDashTagUnitTimestamp.__init__(self,folderPkl,self.confFolder)
        self.dfPLC      = self.__buildPLC(ds=False)
        self.legendTags = pd.read_csv(self.confFolder + 'tagLegend.csv')
        self.powerGroups = pd.read_csv(self.confFolder +'powerGroups.csv',index_col=0)

    def __buildPLC(self,ds=True):
        if ds:return self.dfPLC[self.dfPLC.DATASCIENTISM==True]
        else : return self.dfPLC

    def getListTagsPower(self):
        return self.utils.flattenList([self.getTagsTU(self.powerGroups.loc[k].pattern) for k in self.powerGroups.index])

    def _categorizeTagsPerUnit(self,df):
        dfPLC1 = self.dfPLC[self.dfPLC.TAG.isin(df.columns)]
        unitGroups={}
        for u in dfPLC1.UNITE.unique():
            unitGroups[u]=list(dfPLC1[dfPLC1.UNITE==u].TAG)
        return unitGroups

class ConfigFilesSmallPowerSpark(ConfigDashSpark,SmallPowerMaster):
    def __init__(self,sparkData,sparkConfFile,confFile=None,encode='utf-8'):
        SmallPowerMaster.__init__(self)
        ConfigDashSpark.__init__(sparkData,sparkConfFile,confFile=confFile)
        self.usefulTags = pd.read_csv(self.appDir+'/confFiles/predefinedCategories.csv',index_col=0)
        self.dfPLC = self.__buildPLC()

    def __buildPLC(self):
        return self.dfPLC[self.dfPLC.DATASCIENTISM==True]

class AnalysisPerModule(ConfigFilesSmallPower):
    def __init__(self,folderPkl,encode='utf-8'):
        ConfigFilesSmallPower.__init__(self,folderPkl,encode)
        self.modules = self._loadModules()
        self.listModules = list(self.modules.keys())

    def _buildEauProcess(self):
        eauProcess={}
        eauProcess['pompes']=['PMP_04','PMP_05']
        eauProcess['TNK01'] = ['L219','L221','L200','L205','GWPBC_TNK_01']
        eauProcess['pompe purge'] = ['GWPBC_PMP_01','L202','L210']
        eauProcess['toStack'] = ['L036','L020','GFD_01']
        return eauProcess

    def _buildGV(self):
        GV = {}
        GV['temperatures GV1a'] = ['STG_01a_TT']
        GV['commande GV1a'] = ['STG_01a_HER']
        GV['commande GV1b'] = ['STG_01b_HER']
        GV['ligne gv1a'] = ['L211','L213_H2OPa']
        GV['ligne gv1b'] = ['L211','L213_H2OPb']
        GV['temperatures GV1b'] = ['STG_01b_TT']
        return GV

    def _buildValo(self):
        Valo = {}
        Valo['amont-retour'] = ['GWPBC_PMP_02','L400','L416','L413']
        Valo['echangeur 1'] = ['HPB_HEX_01','L402','L114','L117']
        Valo['condenseur 1'] = ['HPB_CND_01','L408','L404','L021','L022']
        Valo['echangeur 2'] = ['HPB_HEX_02','L404','L115','L116']
        Valo['condenseur 2'] = ['HPB_CND_02','L406','L046','L045']
        Valo['batiment'] = ['GWPBC-HEX-01','L414','L415']
        return Valo

    def _buildGroupeFroid(self):
        groupFroid = {}
        groupFroid['groupe froid'] = ['HPB_CND_03','L417','L418','L056','L057']
        return groupFroid

    def _buildBalayage(self):
        Balayage = {}
        Balayage['echangeur'] = ['HTBA_HEX_01','L133','L134','L135','HPB_RD_01']
        Balayage['stack'] = ['STB_TT_01','STB_TT_02']
        Balayage['blowers'] = ['GWPBH_BLR','L136']
        Balayage['explosimetre'] = ['SFTB_AT_01']
        return Balayage

    def _buildStackBox(self):
        stackBox = {}
        stackBox['chauffants enceinte'] = ['SEH1.STB_HER']
        stackBox['chauffants stacks'] = ['SEH1.STB_STK_0[1-4]_HER']
        stackBox['stack 1'] = ['STB_STK_01']
        stackBox['stack 2'] = ['STB_STK_02']
        stackBox['stack 3'] = ['STB_STK_03']
        stackBox['stack 4'] = ['STB_STK_04']
        stackBox['debits'] = ['STB_GFD','STB_FUEL','STB_GFC','STB_GDC']
        return stackBox

    def _loadModules(self):
        modules = {}
        modules['eau process']=self._buildEauProcess()
        modules['GV']=self._buildGV()
        modules['groupe froid']=self._buildGroupeFroid()
        modules['valo']=self._buildValo()
        modules['balayage']=self._buildBalayage()
        modules['stackbox']=self._buildStackBox()
        return modules

    def _categorizeTagsPerUnit(self,module):
        '''module : {'eauProcess','groupe froid','GV','valo'...} given by self.listModules'''
        mod=self.modules[module]
        ll = self.utils.flattenList([self.listTagsModule(mod,g)[1] for g in mod])
        dfPLC1 = self.dfPLC[self.dfPLC.TAG.isin(ll)]
        unitGroups={}
        for u in dfPLC1.UNITE.unique():
            unitGroups[u]=list(dfPLC1[dfPLC1.UNITE==u].TAG)
        return unitGroups

    # ==========================================================================
    #                     Global module functions
    # ==========================================================================

    def listTagsModule(self,module,group):
        groupList=module[group]
        lplc=pd.concat([self.getTagsTU(pat,ds=False,cols='tdu') for pat in groupList])
        lds=self.utils.flattenList([self.getTagsTU(pat,ds=True) for pat in groupList])
        return lplc,lds

    def listTagsAllModules(self,module,groups=[]):
        mod=self.modules[module]
        LPLC = {g:self.listTagsModule(mod,g)[0] for g in mod}
        LDS = {g:self.listTagsModule(mod,g)[1] for g in mod}
        return LPLC,LDS

    def getDictGroupUnit(self,module,groupsOfModule):
        dictdictGroups = {}
        allgroupsofModule = self.listTagsAllModules(module)[1]
        if not groupsOfModule:groupsOfModule=list(allgroupsofModule.keys())
        groupsOfModule={g:allgroupsofModule[g] for g in groupsOfModule}
        for group,listTags in groupsOfModule.items():
            dictdictGroups[group] = {t:self.utils.detectUnit(self.getUnitofTag(t)) + ' in ' + self.getUnitofTag(t) for t in listTags}

        listTags=self.utils.flattenList([v for v in groupsOfModule.values()])
        return dictdictGroups,listTags
    # ==========================================================================
    #                           GRAPH FUNCTIONS
    # ==========================================================================
    def figureModule(self,module,timeRange,groupsOfModule=None,axisSpace=0.04,hspace=0.02,vspace=0.1,colmap='jet',**kwargs):
        '''
        module : name of the module
        groupsOfModule : list of names of subgroups from the module
        '''
        dictdictGroups,listTags=self.getDictGroupUnit(module,groupsOfModule)
        df  = self.DF_loadTimeRangeTags(timeRange,listTags,**kwargs)
        fig = self.utils.multiUnitGraphSubPlots(df,dictdictGroups,
                        axisSpace=axisSpace,horizontal_spacing=hspace,vertical_spacing=vspace,colormap='jet',
                        subplot_titles=groupsOfModule)
        return fig

    def figureModuleUnits(self,module,timeRange,listUnits=[],grid=None,**kwargs):
        from plotly.subplots import make_subplots
        unitGroups=self._categorizeTagsPerUnit(module)
        if not listUnits: listUnits = list(unitGroups.keys())
        if not grid:grid=self.utils.optimalGrid(len(listUnits))
        fig = make_subplots(rows=grid[0], cols=grid[1],
                                vertical_spacing=0.01,horizontal_spacing=0.1,shared_xaxes=True)
        rows,cols=self.utils.rowsColsFromGrid(len(listUnits),grid)
        for k,r,c in zip(listUnits,rows,cols):
            print(k)
            listTags = unitGroups[k]
            df = self.DF_loadTimeRangeTags(timeRange,listTags,**kwargs)
            df=df.ffill().bfill()
            for l in df.columns:
                fig.add_scatter(y=df[l],x=df.index, mode="lines",
                                name=l, row=r, col=c)
            fig.update_yaxes(title_text=self.utils.detectUnit(k) + ' ( '+ k + ' ) ', row=r, col=c)
            # fig.update_yaxes(color='#FF0000')

        fig.update_xaxes(matches='x')
        fig.update_traces(hovertemplate='<b>%{y:.1f}',)
        fig.update_layout(title={"text": module})
        return fig

    def updateFigureModule(self,fig,module,groupsOfModule,hg,hs,vs,axSP,lgd=False):
        self.utils.printListArgs(module,groupsOfModule,hg,hs,vs,axSP)
        dictdictGroups = self.getDictGroupUnit(module,groupsOfModule)[0]
        figLayout = self.utils.getLayoutMultiUnitSubPlots(dictdictGroups,axisSpace=axSP,
                                                        horizontal_spacing=hs,vertical_spacing=vs)
        fig.layout = figLayout[0].layout
        fig.update_traces(marker=dict(size=5))
        fig.update_traces(hovertemplate='<b>%{y:.1f}')
        fig.update_yaxes(showgrid=False)
        fig.update_layout(height=hg)
        fig.update_layout(showlegend=lgd)
        fig.update_xaxes(matches='x')

        return fig

    def plotQuick(self,df,duration='short',title='',form='df'):
        df=df.ffill().bfill()
        if form=='step': plt.step(x=df.index,y=df.iloc[:,0],)
        if form=='multi': mpl.multiYmpl(df)
        if form=='df': df.plot(colormap='jet')
        datenums=md.date2num(df.index)
        if duration=='short': xfmt = md.DateFormatter('%H:%M')
        else: xfmt = md.DateFormatter('%b-%d')
        ax=plt.gca()
        plt.xticks( rotation=25 )
        # ax.xaxis.set_major_formatter(xfmt)
        # ax.set_ylabel('timestamp')
        mpl.plt.title(title)

class ConfigFilesSmallPower_RealTime(ConfigDashRealTime,SmallPowerMaster):
    # ==========================================================================
    #                       INIT FUNCTIONS
    # ==========================================================================

    def __init__(self,connParameters=None,encode='utf-8'):
        if not connParameters : connParameters ={
            'host'     : "192.168.1.44",
            'port'     : "5434",
            'dbname'   : "Jules",
            'user'     : "postgres",
            'password' : "SylfenBDD"
        }
        SmallPowerMaster.__init__(self)
        ConfigDashRealTime.__init__(self,self.confFolder,connParameters)
