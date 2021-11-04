import datetime as dt, pickle, time, os,re,pandas as pd
import dash, dash_core_components as dcc, dash_html_components as html, dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
import plotly.express as px, plotly.graph_objects as go
# import matplotlib.pyplot as plt, matplotlib.colors as mtpcl
# from pylab import cm
from dorianUtils.utilsD import Utils
from dorianUtils.dccExtendedD import DccExtended
import dorianUtils.dashTabsD as tabsD
import smallPowerDash.configFilesSmallPower as cfs

class SmallPowerTab():
    def __init__(self,app,baseId):
        self.baseId=baseId
        self.app = app
        self.utils = Utils()
        self.dccE = DccExtended()
        self.listModules = ['repartitions puissances(groups)','repartitions puissances(tags)','rendement GV','bilan valo','bilan condenseur','pertes stack','rendement blowers','cosphi']

    def selectGraph(self,indicator,timeRange,**kwargs):
        if indicator == 'rendement GV':
            fig = self.cfg.checkRendementGV(timeRange,**kwargs)
        if indicator == 'bilan condenseur':
            fig = self.cfg.checkCondenseur(timeRange,**kwargs)
        if indicator == 'bilan valo':
            fig = self.cfg.checkValo(timeRange,**kwargs)
        if indicator == 'pertes stack':
            fig = self.cfg.checkPertesStack(timeRange,**kwargs)
        if indicator == 'rendement blowers':
            fig = self.cfg.checkBlowers(timeRange,**kwargs)
        if indicator == 'cosphi':
            fig = self.cfg.checkCosphi(timeRange,**kwargs)
        if indicator == 'repartitions puissances(groups)':
            fig = self.cfg.plotGraphPowerArea(timeRange,expand='groups',**kwargs)
        if indicator == 'repartitions puissances(tags)':
            fig = self.cfg.plotGraphPowerArea(timeRange,expand='tags',**kwargs)
        return fig

    def plotIndicator(self,indicator,timeRange,updateBtn,style,previousFig,rs,rsMethod):
        ctx = dash.callback_context
        trigId = ctx.triggered[0]['prop_id'].split('.')[0]
        # to ensure that action on graphs only without computation do not
        # trigger computing the dataframe again
        triggerList=['dd_indicator','btn_update','pdr_timeBtn','dd_resampleMethod']
        if not updateBtn or trigId in [self.baseId+k for k in triggerList]:
            fig  = self.selectGraph(indicator,timeRange,rs=rs,applyMethod=rsMethod)
        else :fig = go.Figure(previousFig)
        try :
            fig = self.utils.legendPersistant(previousFig,fig)
            fig.update_layout(height=800)
            fig.update_traces(mode=style)
        except:print('skip and update for next graph')
        return fig

# ==============================================================================
#                        POST-PROCESSING TABS
# ==============================================================================
class ComputationTab(SmallPowerTab):
    def __init__(self,folderPkl,app,baseId='ct0_'):
        super().__init__(app,baseId)
        self.cfg = cfs.ConfigFilesSmallPower(folderPkl)
        self.computationGraphs=['power repartition']
        self.tabLayout = self._buildComputeLayout()
        self.tabname = 'computation'
        self._define_callbacks()

    def plotGraphComputation(self,timeRange,computation,params):
        start     = time.time()
        if computation == 'power repartition' :
            fig = self.cfg.plotGraphPowerArea(timeRange,rs=params['rs'],applyMethod=params['method'],expand=params['expand'])
            fig.update_layout(yaxis_title='power in W')
        self.utils.printCTime(start,'computation time : ')
        return fig

    def _buildComputeLayout(self,widthG=85):
        dicWidgets = {'pdr_time' : {'tmin':self.cfg.listFilesPkl[0],'tmax':self.cfg.listFilesPkl[-1]},
                    'in_timeRes':str(60*10)+'s','dd_resampleMethod':'mean',
                    'dd_style':'lines+markers','dd_cmap':'jet','btn_export':0}
        basicWidgets = self.dccE.basicComponents(dicWidgets,self.baseId)
        ddCompute = self.dccE.dropDownFromList(self.baseId+'dd_computation',self.computationGraphs,
                            'what should be computed ?',value = 'power repartition')

        ddExpand = self.dccE.dropDownFromList(self.baseId+'dd_expand',['groups','tags'],'Select the option : ',value = 'groups')
        widgetLayout = basicWidgets + ddCompute + ddExpand
        return self.dccE.buildGraphLayout(widgetLayout,self.baseId,widthG=widthG)

    def _define_callbacks(self):
        listInputsGraph = {
            'dd_computation':'value',
            'pdr_timeBtn':'n_clicks',
            'dd_resampleMethod' : 'value',
            'dd_expand' : 'value',
            'dd_cmap':'value',
            'dd_style':'value'
            }
        listStatesGraph = {
            'graph':'figure',
            'in_timeRes' : 'value',
            'pdr_timeStart' : 'value',
            'pdr_timeEnd':'value',
            'pdr_timePdr':'start_date',
                            }

        @self.app.callback(
        Output(self.baseId + 'graph', 'figure'),
        [Input(self.baseId + k,v) for k,v in listInputsGraph.items()],
        [State(self.baseId + k,v) for k,v in listStatesGraph.items()],
        State(self.baseId+'pdr_timePdr','end_date')
        )
        def updateGraph(computation,timeBtn,rsmethod,expand,colmap,style,fig,rs,date0,date1,t0,t1):
            ctx = dash.callback_context
            trigId = ctx.triggered[0]['prop_id'].split('.')[0]
            # to ensure that action on graphs only without computation do not
            # trigger computing the dataframe again
            triglist=['dd_computation','pdr_timeBtn','dd_typeGraph','dd_expand','dd_resampleMethod']
            if trigId in [self.baseId+k for k in triglist] :
                timeRange = [date0+' '+t0,date1+' '+t1]
                params,params['rs'],params['method'],params['expand']={},rs,rsmethod,expand
                fig   = self.plotGraphComputation(timeRange,computation,params)
            else :fig = go.Figure(fig)
            fig = self.utils.updateStyleGraph(fig,style,colmap)
            return fig

        @self.app.callback(
                Output(self.baseId + 'dl','data'),
                Input(self.baseId + 'btn_export', 'n_clicks'),
                State(self.baseId + 'graph','figure'),
                prevent_initial_call=True
                )
        def exportClick(btn,fig):
            df,filename =  self.utils.exportDataOnClick(fig)
            return dcc.send_data_frame(df.to_csv, filename+'.csv')

class ModuleTab(SmallPowerTab):
    def __init__(self,folderPkl,app,baseId='tmo0_',widthGraph=86):
        super().__init__(app,baseId)
        self.cfg = cfs.AnalysisPerModule(folderPkl)
        self.widthGraph = widthGraph
        self.tabLayout = self._buildModuleLayout()
        self.tabname = 'modules'
        self._define_callbacks()

    def _buildModuleLayout(self):
        dicWidgets = {
                    'pdr_time' : {'tmin':self.cfg.listFilesPkl[0],'tmax':self.cfg.listFilesPkl[-1]},
                    'in_timeRes':'auto','dd_resampleMethod':'mean',
                    'dd_style':'lines','dd_cmap':'prism',
                    'btn_export':0,
                    'block_multiAxisSettings':None
                    }
        basicWidgets = self.dccE.basicComponents(dicWidgets,self.baseId)

        dd_modules = self.dccE.dropDownFromList(self.baseId+'dd_modules',
                        list(self.cfg.modules.keys()),'Select your module: ',value = 'GV')

        dd_moduleGroup = self.dccE.dropDownFromList(self.baseId+'dd_moduleGroup',[],
                            'Select the graphs to display: ',value = 0,multi=True)

        cl_units = [dcc.Checklist(id=self.baseId+'check_unit',
                        options=[{'label': 'unit', 'value':'unit'}],value= 'unit')]

        widgetLayout = basicWidgets + dd_modules+dd_moduleGroup+cl_units
        return self.dccE.buildGraphLayout(widgetLayout,self.baseId,widthG=self.widthGraph)

    def _define_callbacks(self):
        @self.app.callback(
        Output(self.baseId + 'dd_moduleGroup', 'options'),
        Input(self.baseId + 'dd_modules','value'),
        Input(self.baseId + 'check_unit','value'),
        )
        def updateGraph(module,unitGroup):
            if not unitGroup : l = self.cfg.listTagsAllModules(module)[1]
            else : l= list(self.cfg._categorizeTagsPerUnit(module).keys())
            options = [{'label':t,'value':t} for t in l]
            return options

        listInputsGraph = {
            'pdr_timeBtn':'n_clicks',
            'dd_resampleMethod' : 'value',
            'dd_cmap':'value',
            'dd_style':'value',
            'in_heightGraph':'value',
            'in_axisSp':'value',
            'in_hspace':'value',
            'in_vspace':'value',
            }
        listStatesGraph = {
            'graph':'figure',
            'dd_modules':'value',
            'check_unit':'value',
            'dd_moduleGroup':'value',
            'in_timeRes' : 'value',
            'pdr_timeStart' : 'value',
            'pdr_timeEnd':'value',
            'pdr_timePdr':'start_date',
        }
        @self.app.callback(
        Output(self.baseId + 'graph', 'figure'),
        Output(self.baseId + 'pdr_timeBtn', 'n_clicks'),
        [Input(self.baseId + k,v) for k,v in listInputsGraph.items()],
        [State(self.baseId + k,v) for k,v in listStatesGraph.items()],
        State(self.baseId+'pdr_timePdr','end_date'))
        def updateGraph(timeBtn,rsmethod,colmap,style,hg,axsp,hs,vs,fig,module,unitGroup,listGroups,rs,date0,date1,t0,t1):
            ctx = dash.callback_context
            trigId = ctx.triggered[0]['prop_id'].split('.')[0]
            # triggerList = ['dd_modules','dd_moduleGroup','pdr_timeBtn','dd_resampleMethod']
            triggerList = ['pdr_timeBtn','dd_resampleMethod']
            if not timeBtn or trigId in [self.baseId+k for k in triggerList] :
                timeRange = [date0+' '+t0,date1+' '+t1]
                if not unitGroup :
                    fig = self.cfg.figureModule(module,timeRange,groupsOfModule=listGroups,rs=rs,applyMethod=rsmethod)
                else :
                    fig = self.cfg.figureModuleUnits(module,timeRange,listUnits=listGroups,rs=rs,applyMethod=rsmethod)
            else :fig = go.Figure(fig)
            if not unitGroup :fig = self.cfg.updateFigureModule(fig,module,listGroups,hg,hs,vs,axsp)
            else : fig = fig.update_layout(height=hg)
            # fig = self.updateLegend(fig,lgd)
            return fig,timeBtn

        @self.app.callback(
        Output(self.baseId + 'btn_export','children'),
        Input(self.baseId + 'btn_export', 'n_clicks'),
        State(self.baseId + 'graph','figure'))
        def exportClick(btn,fig):
            fig = go.Figure(fig)
            if btn>0:self.utils.exportDataOnClick(fig,baseName='proof')
            return 'export Data'

class MultiUnitSmallPowerTab(tabsD.TabMultiUnits):
    def __init__(self,folderPkl,app,baseId='mut0_'):
        self.cfg = cfs.ConfigFilesSmallPower(folderPkl)
        tabsD.TabMultiUnits.__init__(self,self.cfg,app,baseId)
        defaultTags = self.cfg.getTagsTU('L03[26]')
        self.tabLayout = self._buildLayout(widthG=85,initialTags=defaultTags)
        self._define_callbacks()

class TagSelectedSmallPowerTab(tabsD.TabSelectedTags):
    def __init__(self,folderPkl,app,baseId='tst0_'):
        self.cfg = cfs.ConfigFilesSmallPower(folderPkl)
        tabsD.TabSelectedTags.__init__(self,self.cfg,app,baseId)
        self.tabLayout = self._buildLayout(widthG=84,tagCatDefault='Temperatures du gv1a')
        self._define_callbacks()

class UnitSelectorSmallPowerTab(tabsD.TabUnitSelector):
    def __init__(self,folderPkl,app,baseId='tust0_'):
        self.cfg = cfs.ConfigFilesSmallPower(folderPkl)
        tabsD.TabUnitSelector.__init__(self,self.cfg,app,baseId)
        self.tabLayout = self._buildLayout(widthG=87,unitInit='W AC',patTagInit='')
        self._define_callbacks()

class IndicatorTab(SmallPowerTab):
    def __init__(self,folderPkl,app,baseId='ti0_'):
        SmallPowerTab.__init__(self,app,baseId)
        self.cfg = cfs.ConfigFilesSmallPower(folderPkl)
        self.tabname = 'indicators'
        self.tabLayout = self._buildLayout(valIndicator='rendement blowers')
        self._define_callbacks()

    def _buildLayout(self,widthG=85,valIndicator=None):
        dicWidgets = {'pdr_time' : {'tmin':self.cfg.listFilesPkl[0],'tmax':self.cfg.listFilesPkl[-1]},
                        'in_timeRes':'auto','dd_resampleMethod' : 'mean',
                        'dd_style':'lines+markers',
                        'btn_export':0}
        basicWidgets = self.dccE.basicComponents(dicWidgets,self.baseId)
        # reodrer widgets
        widgetLayout = basicWidgets + self.dccE.dropDownFromList(self.baseId+'dd_indicator',
                                        self.listModules,'chose indicator : ',value=valIndicator)
        return self.dccE.buildGraphLayout(widgetLayout,self.baseId,widthG=widthG)

    def _define_callbacks(self):
        listInputsGraph = {
                        'dd_indicator':'value',
                        'pdr_timeBtn':'n_clicks',
                        'dd_resampleMethod':'value',
                        'dd_style':'value',
                        }
        listStatesGraph = {
                            'graph':'figure',
                            'in_timeRes' : 'value',
                            'pdr_timeStart' : 'value',
                            'pdr_timeEnd':'value',
                            'pdr_timePdr':'start_date',
                            }

        @self.app.callback(
            Output(self.baseId + 'graph', 'figure'),
            [Input(self.baseId + k,v) for k,v in listInputsGraph.items()],
            [State(self.baseId + k,v) for k,v in listStatesGraph.items()],
            State(self.baseId+'pdr_timePdr','end_date'))
        def updateIndGraph(indicator,timeBtn,rsMethod,style,previousFig,rs,date0,date1,t0,t1):
            timeRange = [date0+' '+t0,date1+' '+t1]
            return self.plotIndicator(indicator,timeRange,timeBtn,style,previousFig,rs,rsMethod)

        @self.app.callback(
                Output(self.baseId + 'dl','data'),
                Input(self.baseId + 'btn_export', 'n_clicks'),
                State(self.baseId + 'graph','figure'),
                prevent_initial_call=True
                )
        def exportClickMUG(btn,fig):
            df,filename =  self.utils.exportDataOnClick(fig)
            return dcc.send_data_frame(df.to_csv, filename+'.csv')

# ==============================================================================
#                        REAL TIME TABS
# ==============================================================================
class RealTimeTagSmallPowerSelectorTab(tabsD.RealTimeTagSelectorTab):
    def __init__(self,app,connParameters=None,baseId='rttsp_'):
        self.cfg = cfs.ConfigFilesSmallPower_RealTime(connParameters=connParameters)
        tabsD.RealTimeTagSelectorTab.__init__(self,app,self.cfg,baseId=baseId)
        self.tabLayout = self._buildLayout(widthG=85,defaultCat='Temperatures du gv1a',
                        val_window=60*2,val_refresh=20,min_refresh=5,min_window=1)

class RealTimeSmallPowerMultiUnit(tabsD.RealTimeTagMultiUnit):
    def __init__(self,app,connParameters=None,baseId='rtmsp_'):
        self.cfg = cfs.ConfigFilesSmallPower_RealTime(connParameters=connParameters)
        tabsD.RealTimeTagMultiUnit.__init__(self,app,self.cfg,baseId)
        self.tabLayout = self._buildLayout(widthG=85,
                    defaultTags=self.cfg.getTagsTU('L036'),
                    val_window=2*1,
                    val_refresh=20,
                    min_refresh=5,
                    min_window=1,
                    val_res='1s')

class RealTimeIndicatorTab(SmallPowerTab):
    def __init__(self,app,connParameters,baseId='rtisp_'):
        SmallPowerTab.__init__(self,app,baseId)
        self.connParameters = connParameters
        self.cfg = cfs.ConfigFilesSmallPower_RealTime(self.connParameters)
        self.listModules = ['rendement GV','bilan valo','bilan condenseur','pertes stack','rendement blowers','cosphi']
        self.tabname = 'indicators'
        self.tabLayout = self._buildLayout()
        self._define_callbacks()

    def selectGraph(self,indicator,timeRange,**kwargs):
        if indicator == 'rendement GV':
            fig = self.cfg.checkRendementGV(timeRange,**kwargs)
        if indicator == 'bilan condenseur':
            fig = self.cfg.checkCondenseur(timeRange,**kwargs)
        if indicator == 'bilan valo':
            fig = self.cfg.checkValo(timeRange,**kwargs)
        if indicator == 'pertes stack':
            fig = self.cfg.checkPertesStack(timeRange,**kwargs)
        if indicator == 'rendement blowers':
            fig = self.cfg.checkBlowers(timeRange,**kwargs)
        if indicator == 'cosphi':
            fig = self.cfg.checkCosphi(timeRange,**kwargs)
        return fig

    def _buildLayout(self,widthG=85,initialInd='rendement blowers',val_window=60*2,val_refresh=20,min_refresh=5,min_window=1,val_res='auto'):
        dicWidgets = {'block_refresh':{'val_window':val_window,'val_refresh':val_refresh,
                            'min_refresh':min_refresh,'min_window':min_window},
                        'btn_update':0,
                        'block_resample':{'val_res':val_res,'val_method' : 'mean'},
                        'dd_style':'lines+markers',
                        'btn_export':0,
                        'in_axisSp':0.05,
                        }
        basicWidgets = self.dccE.basicComponents(dicWidgets,self.baseId)
        ddIndicator = self.dccE.dropDownFromList(self.baseId+'dd_indicator',
                        self.listModules,'chose indicator : ',value=initialInd)
        widgetLayout = basicWidgets + ddIndicator
        return self.dccE.buildGraphLayout(widgetLayout,self.baseId,widthG=widthG)


    def _define_callbacks(self):
        listInputsGraph = {
                        'interval':'n_intervals',
                        'btn_update':'n_clicks',
                        'dd_indicator':'value',
                        'dd_resampleMethod':'value',
                        'dd_style':'value',
                        'in_axisSp':'value',
                        }
        listStatesGraph = {
                            'graph':'figure',
                            'in_timeWindow':'value',
                            'in_timeRes':'value'
                            }
        @self.app.callback(
        Output(self.baseId + 'graph', 'figure'),
        [Input(self.baseId + k,v) for k,v in listInputsGraph.items()],
        [State(self.baseId + k,v) for k,v in listStatesGraph.items()],
        )
        def updateGraph(n,updateBtn ,indicator,rsMethod,style,axSP,previousFig,tw,rs):
            # self.utils.printListArgs(n,updateBtn,indicator,rsMethod,style,axSP,previousFig,tw,rs)
            ctx = dash.callback_context
            trigId = ctx.triggered[0]['prop_id'].split('.')[0]
            # to ensure that action on graphs only without computation do not
            # trigger computing the dataframe again
            triggerList=['dd_indicator','btn_update','dd_resampleMethod']
            if not updateBtn or trigId in [self.baseId+k for k in triggerList]:
                fig  = self.selectGraph(indicator,tw*60,rs=rs,applyMethod=rsMethod)
            else :fig = go.Figure(previousFig)
            try :
                fig = self.utils.legendPersistant(previousFig,fig)
                fig.update_layout(height=800)
                fig.update_traces(mode=style)
            except:print('skip and update for next graph')
            return fig

        @self.app.callback(
                Output(self.baseId + 'dl','data'),
                Input(self.baseId + 'btn_export', 'n_clicks'),
                State(self.baseId + 'graph','figure'),
                prevent_initial_call=True
                )
        def exportClickMUG(btn,fig):
            df,filename =  self.utils.exportDataOnClick(fig)
            return dcc.send_data_frame(df.to_csv, filename+'.csv')

class RT_SP_MultiUnitSelectedTags(tabsD.RealTimeMultiUnitSelectedTags):
    def __init__(self,app,connParameters=None,baseId='rtmssp_'):
        self.cfg = cfs.ConfigFilesSmallPower_RealTime(connParameters=connParameters)
        tabsD.RealTimeMultiUnitSelectedTags.__init__(self,app,self.cfg,baseId,graphfunction='multiunitshades')
        self.tabLayout = self._buildLayout(widthG=85,
                        defaultSelTags = 'Temperatures du gv1a',
                        defaultTags = self.cfg.getTagsTU('L036'),
                        val_window=30*1,
                        val_res='10s',
                        val_refresh=20,
                        min_refresh=5,
                        min_window=1)

class RT_SP_doubleMultiUnit(tabsD.RealTimeDoubleMultiUnits):
    def __init__(self,app,connParameters=None,baseId='rtdmsp_'):
        self.cfg = cfs.ConfigFilesSmallPower_RealTime(connParameters=connParameters)
        tabsD.RealTimeDoubleMultiUnits.__init__(self,app,self.cfg,baseId)
        self.tabLayout = self._buildLayout(widthG=85,
                        defaultTags1 = self.cfg.getUsefulTags('Temperatures du gv1a')[:4],
                        defaultTags2 = self.cfg.getTagsTU('L036'),
                        val_window=30*1,
                        val_res='10s',
                        val_refresh=20,
                        min_refresh=5,
                        min_window=1)
