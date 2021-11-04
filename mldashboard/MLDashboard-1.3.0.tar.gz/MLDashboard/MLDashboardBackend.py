#Module imports
from MLDashboard.DashboardModules.LossMetricsGraph import LossMetricsGraph
from MLDashboard.DashboardModules.LossMetricsNumerical import LossMetricsNumerical
from MLDashboard.DashboardModules.StatusModule import StatusModule
from MLDashboard.DashboardModules.ControlButtons import ControlButtons
from MLDashboard.DashboardModules.TrainingSetSampleImages import TrainingSetSampleImages
from MLDashboard.DashboardModules.PredImages import PredImages
from MLDashboard.DashboardModules.WrongPredImages import WrongPredImages
from MLDashboard.DashboardModules.EmptyModule import EmptyModule
from MLDashboard.DashboardModules.Module import Module

from MLDashboard.MLCommunicationBackend import Message, MessageMode
import matplotlib.pyplot as pyplot
from typing import List, Tuple
import multiprocessing
import json
import time

#region Dashboard
allModules = {'LossMetricsGraph': LossMetricsGraph,
              'LossMetricsNumerical': LossMetricsNumerical,
              'StatusModule': StatusModule,
              'ControlButtons': ControlButtons,
              'TrainingSetSampleImages': TrainingSetSampleImages,
              'PredImages': PredImages,
              'WrongPredImages': WrongPredImages,
              'EmptyModule': EmptyModule}

def dashboardProcess(configjson: dict, updatelist: list, returnlist: list, openatend):
    """Wrapper function to run dashboard in a seperate process. This should not be called manually."""
    print("Loading dashboard...")
    dashboard = Dashboard(configjson, updatelist, returnlist, openatend)
    print("Starting dashboard...")
    dashboard.runDashboardLoop()

def createDashboard(config='dashboard.json', waitforstart=True,
                    openatend=True) -> Tuple[multiprocessing.Process, List[Message], List[Message]]:
    """
    Creates a dashboard running in a seperate process.
    Returns the process, updatelist, and return list for communication
    :param config: The file to load the dashboard config from
    :param waitforstart: Should the main process halt while the dashboard starts
    :param openatend: Calls pyplot.show() at end of training
    """
    syncmanager = multiprocessing.Manager()
    updatelist: List[Message] = syncmanager.list()
    returnlist: List[Message] = syncmanager.list()

    with open(config) as f:
        configjson = json.load(f)
    process = multiprocessing.Process(target=dashboardProcess, args=(configjson, updatelist, returnlist, openatend,))
    process.start()

    if waitforstart:
        done = False
        rmindex = -1
        while not done:
            time.sleep(0.05)
            for index, item in enumerate(returnlist):
                if item.mode == MessageMode.Start:
                    rmindex = index
                    done = True
                    break

        returnlist.pop(rmindex)

    return process, updatelist, returnlist

def getModules(configjson):
    """Returns a list of module classes"""

    if "modules" not in configjson:
        raise Exception("Modules tag missing in config json.")
    modulelist = configjson["modules"]
    if len(modulelist) == 0:
        raise Exception("No modules found in config json.")

    sublistlen = len(modulelist[0])
    modules = []
    configs = []
    for sublist in modulelist:
        if len(sublist) != sublistlen:
            raise Exception("Modules do not form a grid.")
        for module, config in sublist:
            if module not in allModules:
                raise Exception("Module: " + str(module) + " not valid.")
            modules.append(allModules[module])
            configs.append(config)

    return modules, configs, sublistlen, len(modulelist)

def addRequests(reqs, outputlist):
    """Adds requests to output list if reqs is not none"""
    if reqs is not None:
        for item in reqs:
            outputlist.append(item)

class Dashboard:
    """
    Dashboard is a class that handles high level matplotlib interaction and sends data to sub modules.
    Dashbaords should be created with the createDashboard function.
    """
    def __init__(self, configjson: dict, updatelist: List[Message], returnlist: List[Message],
                 openatend:bool = False):
        self.configjson = configjson
        self.updatelist = updatelist
        self.returnlist = returnlist
        moduleclasslist, moduleconfiglist, self.width, self.height = getModules(configjson)
        self.modulelist: List[Module] = []


        self.fig = pyplot.figure()
        figManager = pyplot.get_current_fig_manager()
        figManager.window.state('zoomed')
        self.fig.suptitle("Tensorflow Dashboard")
        self.fig.canvas.manager.set_window_title("Tensorflow Dashboard")
        self.fig.set_tight_layout(True)
        for i, module in enumerate(moduleclasslist):
            ax = self.fig.add_subplot(self.height, self.width, i+1)
            c = moduleconfiglist[i]
            if 'config' in self.configjson:
                for key, value in self.configjson['config'].items():
                    if key not in c:
                        c[key] = value
            m = module(ax, c)
            addRequests(m.initialRequests(), self.returnlist)
            self.modulelist.append(m)

        # status metrics
        self.currentmode = "Live Render"  # are we rendering during training
        self.timer = 0  # time to do a full update loop
        self.modulestimer = [0.0] * len(self.modulelist) #how long does it take to render each module
        self.openatend = openatend

    def runDashboardLoop(self): #this function is designed to be run in a separate process
        """Continually updates modules"""
        done = False
        self.returnlist.append(Message(MessageMode.Start, {}))
        while not done:
            while len(self.updatelist) == 0:
                pyplot.draw()
                pyplot.pause(0.001) #only update when resting

            mostrecentupdate = self.updatelist.pop(0)
            if mostrecentupdate.mode == MessageMode.ForceUpdate:
                pyplot.draw()
                pyplot.pause(0.001)

            else:
                starttime = time.time()
                for i, module in enumerate(self.modulelist):
                    sTime = time.time()
                    self.updateModule(module, mostrecentupdate)
                    self.modulestimer[i] = round(time.time() - sTime, 3)
                self.timer = round(time.time() - starttime, 3)


            if mostrecentupdate.mode == MessageMode.End:
                done = True

        print("Dashboard exiting cleanly...")
        self.currentmode = 'Post Training View'
        for module in self.modulelist:
            self.updateModule(module, Message(MessageMode.End, {}))

        if self.openatend:
            pyplot.show()
        for module in self.modulelist:
            req = module.update(Message(MessageMode.End, {}))
            if req is not None:
                for item in req:
                    self.returnlist.append(item)

    def updateModule(self, module, mostrecentupdate: Message):
        if type(module) == StatusModule:
            reqs = module.update(Message(MessageMode.CustomData, {'autorendering': len(self.updatelist) <= 1,
                                                                  'currentmode': self.currentmode,
                                                                  'timer': self.timer,
                                                                  'modulestimer': self.modulestimer,
                                                                  'width': self.width,
                                                                  'height': self.height}))
        else:
            reqs = module.update(mostrecentupdate)

        addRequests(reqs, self.returnlist)

#endregion