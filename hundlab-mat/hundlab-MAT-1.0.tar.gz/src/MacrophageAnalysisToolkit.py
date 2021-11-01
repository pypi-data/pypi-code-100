# -*- coding: utf-8 -*-
"""
Created on Mon Oct  1 16:06:47 2018

@author: alexj
"""

import sys
import csv
import xlrd
import xlsxwriter
import numpy as np
from PyQt5.QtGui import QIcon
from PIL import Image
from PyQt5.QtWidgets import QAction, QMenu, QTabWidget, QWidget, QDesktopWidget, QFileDialog, QMessageBox
from matplotlib.backends.qt_compat import QtCore, QtWidgets

from MAT.RegionSel import RegionSel
from MAT.SelWin import SelWin
from MAT.Runner import Runner
from MAT.BDD import FindNuclei, FindBrownDots, Colocalize
from MAT.BDDPlotter import BDDPlotter
from MAT.Calibrator import Calibrator

Image.MAX_IMAGE_PIXELS = 1e90

class ApplicationWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(QWidget, self).__init__()
        self.threadpool = QtCore.QThreadPool()
        self._main = QtWidgets.QWidget()
        self.setCentralWidget(self._main)
        layout = QtWidgets.QVBoxLayout(self._main)
        self.imarr_rgb = None
        self.tabs = QTabWidget()
        self.tabsList = []
        self.tol = 0.5*np.array([0, 0, 0])
        self.RGB = np.array([0, 0, 0])
        self.Brightness = 0
        self.calibB = Calibrator('Calibrating Macrophages')
        self.calibN = Calibrator('Calibrating Nuclei')
        self.centroidsB = []
        self.centroidsN = []
        self.sel = []
        layout.addWidget(self.tabs)
        menubar = self.menuBar()
        fileMenu = menubar.addMenu('File')
        toolsMenu = menubar.addMenu('Tools')
        OpenI = QAction('Open Image', self)
        OpenI.setShortcut('Ctrl+O')
        OpenI.triggered.connect(self.Open)
        OpenCal = QMenu('Open Calibration', self)
        OpenCalB = QAction('Macrophage Data', self)
        OpenCalB.triggered.connect(self.open_calibB)
        OpenCalN = QAction('Nucleus Data', self)
        OpenCalN.triggered.connect(self.open_calibN)
#        OpenAnalysis = QMenu('Open Analysis', self)
#        OpenAnalysisB = QAction('Macrophages', self)
#        OpenAnalysisB.triggered.connect(self.open_centroidsB)
#        OpenAnalysisN = QAction('Nuclei', self)
#        OpenAnalysisN.triggered.connect(self.open_centroidsN)
#        OpenAnalysisC = QAction('Colocalized Cells', self)
#        OpenAnalysisC.triggered.connect(self.open_coloc)
#        OpenWkbk = QAction('Open Workbook', self)
        OpenCal.addAction(OpenCalB)
        OpenCal.addAction(OpenCalN)
#        OpenAnalysis.addAction(OpenAnalysisB)
#        OpenAnalysis.addAction(OpenAnalysisN)
#        OpenAnalysis.addAction(OpenAnalysisC)
        openMenu = QMenu('Open',self)
        openMenu.addAction(OpenI)
        openMenu.addMenu(OpenCal)
#        openMenu.addMenu(OpenAnalysis)
#        openMenu.addAction(OpenWkbk)
        saveMenu = QMenu('Save', self)
        saveAct = QAction('Save All CSV Files', self)
        expAct = QAction('Export Spreadsheet', self)
        saveAct.setShortcut('Ctrl+S')
        expAct.setShortcut('Ctrl+E')
        saveIndMenu = QMenu('Save Individual CSV', self)
        saveCalibB = QAction('Save Macrophage Calibration', self)
        saveCalibN = QAction('Save Nucleus Calibration', self)
        saveBDD = QAction('Save Identified Macrophages', self)
        saveNuclei = QAction('Save Identified Nuclei', self)
        saveColoc = QAction('Save Colocalized Cells', self)
        saveIndMenu.addAction(saveCalibB)
        saveIndMenu.addAction(saveCalibN)
        saveIndMenu.addAction(saveBDD)
        saveIndMenu.addAction(saveNuclei)
        saveIndMenu.addAction(saveColoc)
        saveMenu.addMenu(saveIndMenu)
        saveAct.triggered.connect(self.save_all)
        expAct.triggered.connect(self.export_workbook)
        saveCalibB.triggered.connect(self.save_calibrationB)
        saveCalibN.triggered.connect(self.save_calibrationN)
        saveBDD.triggered.connect(self.save_pointsB)
        saveNuclei.triggered.connect(self.save_pointsN)
        saveColoc.triggered.connect(self.save_pointsC)
        exitAct = QAction(QIcon('exit.png'), '&Exit', self)
        exitAct.setShortcut('Ctrl+Q')
        exitAct.triggered.connect(self.close)
        fileMenu.addMenu(openMenu)
        fileMenu.addMenu(saveMenu)
        fileMenu.addAction(exitAct)
        Crop = QAction('Crop', self)
        Crop.triggered.connect(self.DefRegions)
        ProcessMenu = QMenu('Process', self)
        BDDAct = QAction('Macrophages', self)
        BDDAct.setShortcut('Ctrl+B')
        BDDAct.triggered.connect(self.bdd2)
        NucAct = QAction('Nuclei', self)
        NucAct.setShortcut('Ctrl+N')
        NucAct.triggered.connect(self.nuclei)
        ColocAct = QAction('Colocalize', self)
        ColocAct.setShortcut('Ctrl+L')
        ColocAct.triggered.connect(self.colocalize)
        saveMenu.addAction(saveAct)
        saveMenu.addAction(expAct)
        ProcessMenu.addAction(BDDAct)
        ProcessMenu.addAction(NucAct)
        ProcessMenu.addAction(ColocAct)
        CalibMenu = QMenu('Calibrate', self)
        CalibBAct = QAction('Macrophages', self)
        CalibNAct = QAction('Nuclei', self)
        CalibMenu.addAction(CalibBAct)
        CalibMenu.addAction(CalibNAct)
        CalibBAct.setShortcut('Ctrl+Shift+B')
        CalibBAct.triggered.connect(self.CalibrateB)
        CalibNAct.setShortcut('Ctrl+Shift+N')
        CalibNAct.triggered.connect(self.CalibrateN)
        toolsMenu.addAction(Crop)
        toolsMenu.addMenu(CalibMenu)
        toolsMenu.addMenu(ProcessMenu)
        self.resize(QDesktopWidget().availableGeometry(self).size() * 0.4)
        self.setWindowTitle('Macrophage Analysis Toolkit')
#        formatter = lambda **kwargs: ', '.join(kwargs['point_label'])
#        datacursor(hover=True, formatter=formatter, point_labels='text')
        self.regions = RegionSel()
        self.isopen = 0

    def Open(self):
        res = QtWidgets.QFileDialog.getOpenFileNames(caption='Select image file to Analyze')
        self.isopen = 1
        if len(res[0]) == 0:
            return
        for filename in res[0]:
            self.imrgb = Image.open(filename).convert('RGB')
            w,h = self.imrgb.size
            self.imarr_rgb = np.array(self.imrgb)
            tab = BDDPlotter()
            fname = filename.split('/')[-1].split('.')[0]
            self.tabs.addTab(tab, fname)
            tab.showImg(self.imarr_rgb)
            self.tabsList.append(tab)
            self.tabs.setCurrentWidget(tab)
            
    def DefRegions(self):
        res = QtWidgets.QFileDialog.getOpenFileNames(caption='Select image file to Analyze')
        if len(res[0]) == 0:
            return
        for filename in res[0]:
            self.imrgb = Image.open(filename).convert('RGB')
            w,h = self.imrgb.size
            self.imarr_rgb = np.array(self.imrgb)
            
            self.regions.show()
            
            self.regions.new(np.array(self.imrgb))
                
    def showSel(self, filename):        
            tab = BDDPlotter()
            fname = filename.split('/')[-1].split('.')[0]
            self.tabs.addTab(tab, fname)
            tab.showImg(self.imarr_rgb)
            self.tabsList.append(tab)
            self.tabs.setCurrentWidget(tab)

    def CalibrateB(self):
        if self.isopen == 1:
            self.calibB.show()
            self.calibB.imarr = self.imarr_rgb
        else:
            print('Must first open image')
        
    def CalibrateN(self):
        if self.isopen == 1:
            self.calibN.show()
            self.calibN.imarr = self.imarr_rgb
        else:
            print('Must first open image')

    def nuclei(self):
        self.calibB.Refresh()
        tab = self.tabsList[-1]
        self.tol = np.array([self.calibN.tol1.value(), self.calibN.tol2.value(), self.calibN.tol3.value()]) #np.array([0.0677, 0.0523, 0.1126])
        self.RGB = np.array([self.calibN.RGB1.value(), self.calibN.RGB2.value(), self.calibN.RGB3.value()])#np.array([0.8957, 0.8921, 1.2121])
        self.Brightness = self.calibN.BrightnessSpin.value() #153
        if self.tol[0] == 0 or self.tol[1] == 0 or self.tol[2] == 0\
            or self.RGB[0] == 0 or self.RGB[1] == 0 or self.RGB[2] == 0 or self.Brightness == 0:
            print('Check Calibration Values')
            return
        findNuclei = Runner(FindNuclei, [self.imarr_rgb, self.tol, self.RGB, self.Brightness])
        findNuclei.signals.finished.connect(tab.showNuclei)
        findNuclei.signals.finished.connect(self.saveNuclei)
        self.threadpool.start(findNuclei)

    def saveNuclei(self, centroidsN):
        self.centroidsN = centroidsN
        print('finished!')

    def colocalize(self):
        self.sel = []
        tab = self.tabsList[-1]
        finder = Runner(Colocalize, [self.centroidsB, self.centroidsN])
        finder.signals.finished.connect(tab.showColocalize)
        finder.signals.finished.connect(self.saveColocalize)
        self.threadpool.start(finder)

    def saveColocalize(self, sel):
        self.sel = sel
        print('finished!')

    def bdd2(self):
        self.calibB.Refresh()
        self.centroidsB = []
        tab = self.tabsList[-1]
        self.tol = np.array([self.calibB.tol1.value(), self.calibB.tol2.value(), self.calibB.tol3.value()])#self.calibB.tol #np.array([0.2745, 0.1173, 0.2842])
        self.RGB = np.array([self.calibB.RGB1.value(), self.calibB.RGB2.value(), self.calibB.RGB3.value()])#self.calibB.RGB #np.array([1.9273, 0.2783, 0.7944])
        self.Brightness = self.calibB.BrightnessSpin.value() #135
        if self.tol[0] == 0 or self.tol[1] == 0 or self.tol[2] == 0\
            or self.RGB[0] == 0 or self.RGB[1] == 0 or self.RGB[2] == 0 or self.Brightness == 0:
            print('Check Calibration Values')
            return
        finder = Runner(FindBrownDots, [self.imarr_rgb, self.tol, self.RGB, self.Brightness])
        finder.signals.finished.connect(tab.showBDD2)
        finder.signals.finished.connect(self.saveBDD)
        self.threadpool.start(finder)

    def saveBDD(self, centroidsB):
        self.centroidsB = centroidsB
        print('finished!')
           
    def save_calibrationB(self):
        file = QFileDialog.getSaveFileName(caption='Save CB As:')
        if len(file[0])==0:
            return
        filename = file[0] + '_CB.csv'
        self.calibB.Refresh()
        data = (self.calibB.CalData.RGB, self.calibB.CalData.tol, [self.calibB.CalData.brightness, 0, 0])
        self.save_Calibdata(data, filename)
        
    def save_calibrationN(self):
        file = QFileDialog.getSaveFileName(caption='Save CN As:')
        if len(file[0])==0:
            return
        filename = file[0] + '_CN.csv'
        self.calibN.Refresh()
        data = (self.calibN.CalData.RGB, self.calibN.CalData.tol, [self.calibN.CalData.brightness, 0, 0])
        self.save_Calibdata(data, filename)
        
    def save_pointsB(self):
        file = QFileDialog.getSaveFileName(caption='Save PB As:')
        if len(file[0])==0:
            return
        filename = file[0] + '_PB.csv'
        self.save_Pointdata(self.centroidsB, filename)
        
    def save_pointsN(self):
        file = QFileDialog.getSaveFileName(caption='Save PN As:')
        if len(file[0])==0:
            return
        filename = file[0] + '_PN.csv'
        self.save_Pointdata(self.centroidsN, filename)
        
    def save_pointsC(self):
        file = QFileDialog.getSaveFileName(caption='Save PC As:')
        if len(file[0])==0:
            return
        filename = file[0] + '_PC.csv'
        self.save_Pointdata(self.sel, filename)
        
    def save_Calibdata(self, data, filename):
        with open(filename, 'w', newline = '') as csvfile:
            data_writer = csv.writer(csvfile, delimiter=',')
            data_writer.writerow(['Red','Green','Blue'])
            data_writer.writerows(data)
            
    def save_Pointdata(self, data, filename):
        with open(filename, 'w', newline = '') as csvfile:
            data_writer = csv.writer(csvfile, delimiter=',')
            data_writer.writerow(['Xpos','Ypos','Radius'])
            data_writer.writerows(data)
            
    def save_all(self):
        file = QFileDialog.getSaveFileName(caption='Save All As:')
        if len(file[0])==0:
            return
        dataB = (self.calibB.CalData.RGB, self.calibB.CalData.tol, [self.calibB.CalData.brightness, 0, 0])
        dataN = (self.calibN.CalData.RGB, self.calibN.CalData.tol, [self.calibN.CalData.brightness, 0, 0])
        filenameCB = file[0] + '_CB.csv'
        filenameCN = file[0] + '_CN.csv'
        filenamePB = file[0] + '_PB.csv'
        filenamePN = file[0] + '_PN.csv'
        filenamePC = file[0] + '_PC.csv'
        self.save_Calibdata(dataB, filenameCB)
        self.save_Calibdata(dataN, filenameCN)
        self.save_Pointdata(self.centroidsB, filenamePB)
        self.save_Pointdata(self.centroidsN, filenamePN)
        self.save_Pointdata(self.sel, filenamePC)
        
    def export_workbook(self):
        file = QFileDialog.getSaveFileName(caption='Save All As:')
        if len(file[0])==0:
            return
        filename = file[0] + '.xlsx'
        workbook = xlsxwriter.Workbook(filename)
        CB = workbook.add_worksheet('Macrophage Calibration')
        CB.write_row(0,1,['Red','Green','Blue'])
        CB.write(1,0,'RGB Ratio')
        CB.write_row(1,1,self.calibB.CalData.RGB)
        CB.write(2,0,'Tolerance')
        CB.write_row(2,1,self.calibB.CalData.tol)
        CB.write_row(3,0,['Brightness:', self.calibB.CalData.brightness])
        CN = workbook.add_worksheet('Nucleus Calibration')
        CN.write_row(0,1,['Red','Green','Blue'])
        CN.write(1,0,'RGB Ratio')
        CN.write_row(1,1,self.calibN.CalData.RGB)
        CN.write(2,0,'Tolerance')
        CN.write_row(2,1,self.calibN.CalData.tol)
        CN.write_row(3,0,['Brightness:', self.calibN.CalData.brightness])
        PB = workbook.add_worksheet('Macrophages')
        PB.write_row(0,0,['Xpos','Ypos','Radius'])
        for i in range(len(self.centroidsB)-1):
            PB.write_row(i+1,0,self.centroidsB[i,:])
        PN = workbook.add_worksheet('Nuclei')
        PN.write_row(0,0,['Xpos','Ypos','Radius'])
        for i in range(len(self.centroidsN)-1):
            PN.write_row(i+1,0,self.centroidsN[i,:])
        PC = workbook.add_worksheet('Colocalized')
        PC.write_row(0,0,['Xpos','Ypos'])
        for i in range(len(self.sel)):
            PC.write_row(i+1,0,self.sel[i,:])
        workbook.close()
        print('Export Finished')

    def open_calibB(self):
        file = QtWidgets.QFileDialog.getOpenFileName(caption='Select Macrophage Calibration Data')
        if len(file[0]) == 0:
            return
        data = []
        with open(file[0], 'r') as csvfile:
            csvreader = csv.reader(csvfile)
            for row in csvreader:
                data.append(row)
        self.calibB.CalData.RGB = [float(data[1][0]), float(data[1][1]), float(data[1][2])]
        self.calibB.CalData.tol = [float(data[2][0]), float(data[2][1]), float(data[2][2])]
        self.calibB.CalData.brightness = float(data[3][0])
        self.calibB.RGB1.setValue(self.calibB.CalData.RGB[0])
        self.calibB.RGB2.setValue(self.calibB.CalData.RGB[1])
        self.calibB.RGB3.setValue(self.calibB.CalData.RGB[2])
        self.calibB.tol1.setValue(self.calibB.CalData.tol[0])
        self.calibB.tol2.setValue(self.calibB.CalData.tol[1])
        self.calibB.tol3.setValue(self.calibB.CalData.tol[2])
        self.calibB.BrightnessSpin.setValue(self.calibB.CalData.brightness)
#        self.calibB.Refresh()

        
    def open_calibN(self):
        file = QtWidgets.QFileDialog.getOpenFileName(caption='Select Nucleus Calibration Data')
        if len(file[0]) == 0:
            return
        data = []
        with open(file[0], 'r') as csvfile:
            csvreader = csv.reader(csvfile)
            for row in csvreader:
                data.append(row)
        self.calibN.CalData.RGB = [float(data[1][0]), float(data[1][1]), float(data[1][2])]
        self.calibN.CalData.tol = [float(data[2][0]), float(data[2][1]), float(data[2][2])]
        self.calibN.CalData.brightness = float(data[3][0])
        self.calibN.RGB1.setValue(self.calibN.CalData.RGB[0])
        self.calibN.RGB2.setValue(self.calibN.CalData.RGB[1])
        self.calibN.RGB3.setValue(self.calibN.CalData.RGB[2])
        self.calibN.tol1.setValue(self.calibN.CalData.tol[0])
        self.calibN.tol2.setValue(self.calibN.CalData.tol[1])
        self.calibN.tol3.setValue(self.calibN.CalData.tol[2])
        self.calibN.BrightnessSpin.setValue(self.calibN.CalData.brightness)
#        self.calibN.Refresh()
        
    def open_centroidsB(self):
        file = QtWidgets.QFileDialog.getOpenFileName(caption='Select Processed Macrophage Data')
        if len(file[0]) == 0:
            return
        data = []
        with open(file[0], 'r') as csvfile:
            csvreader = csv.reader(csvfile)
            for row in csvreader:
                data.append(row)
        self.centroidsB = np.array(data[1:len(data)]).astype(float)
        print(self.centroidsB)
        tab = self.tabslist[-1]
        tab.showBDD2(self.centroidsB)
        print(1)
        
    def open_centroidsN(self):
        file = QtWidgets.QFileDialog.getOpenFileName(caption='Select Processed Nuclei Data')
        if len(file[0]) == 0:
            return
        data = []
        with open(file[0], 'r') as csvfile:
            csvreader = csv.reader(csvfile)
            for row in csvreader:
                data.append(row)
        self.centroidsN = np.array(data[1:len(data)]).astype(float)
        
    def open_coloc(self):
        file = QtWidgets.QFileDialog.getOpenFileName(caption='Select Processed Colocalized Data')
        if len(file[0]) == 0:
            return
        data = []
        with open(file[0], 'r') as csvfile:
            csvreader = csv.reader(csvfile)
            for row in csvreader:
                data.append(row)
        self.sel = np.array(data[1:len(data)]).astype(float)
        
    def open_workbook(self):
        file = QtWidgets.QFileDialog.getOpenFileName(caption='Select Spreadsheet')
        if len(file[0]) == 0:
            return
        wb = xlrd.open_workbook(file[0])
        CBs = wb.sheet_by_index(0)
        
        CNs = wb.sheet_by_index(1)
        PBs = wb.sheet_by_index(2)
        PNs = wb.sheet_by_index(3)
        PCs = wb.sheet_by_index(4)
        
            

try:
    qapp
except NameError:
    qapp = QtWidgets.QApplication(sys.argv)

app = ApplicationWindow()
app.show()
qapp.exec_()
