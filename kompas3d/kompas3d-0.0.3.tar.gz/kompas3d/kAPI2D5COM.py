# -*- coding: mbcs -*-
# Created by makepy.py version 0.5.01
# By python version 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# From type library 'kAPI2D5COM.tlb'
# On Mon Nov  1 14:47:32 2021
''
makepy_version = '0.5.01'
python_version = 0x30802f0

import win32com.client.CLSIDToClass, pythoncom, pywintypes
import win32com.client.util
from pywintypes import IID
from win32com.client import Dispatch

# The following 3 lines may need tweaking for the particular server
# Candidates are pythoncom.Missing, .Empty and .ArgNotFound
defaultNamedOptArg=pythoncom.Empty
defaultNamedNotOptArg=pythoncom.Empty
defaultUnnamedArg=pythoncom.Empty

CLSID = IID('{0F4AB6C5-1420-4848-AFCE-18CBE701BE1A}')
MajorVersion = 1
MinorVersion = 0
LibraryFlags = 8
LCID = 0x0

IDocument2DNotify_vtables_dispatch_ = 0
IDocument2DNotify_vtables_ = [
	(( 'BeginRebuild' , ), 1610743808, (1610743808, (), [ ], 1 , 1 , 4 , 0 , 32 , (11, 0, None, None) , 0 , )),
	(( 'Rebuild' , ), 1610743809, (1610743809, (), [ ], 1 , 1 , 4 , 0 , 40 , (11, 0, None, None) , 0 , )),
	(( 'BeginChoiceMaterial' , ), 1610743810, (1610743810, (), [ ], 1 , 1 , 4 , 0 , 48 , (11, 0, None, None) , 0 , )),
	(( 'ChoiceMaterial' , 'material' , 'density' , ), 1610743811, (1610743811, (), [ (30, 0, None, None) , 
			 (5, 0, None, None) , ], 1 , 1 , 4 , 0 , 56 , (11, 0, None, None) , 0 , )),
	(( 'BeginInsertFragment' , ), 1610743812, (1610743812, (), [ ], 1 , 1 , 4 , 0 , 64 , (11, 0, None, None) , 0 , )),
	(( 'LocalFragmentEdit' , 'pDoc' , 'newFrw' , ), 1610743813, (1610743813, (), [ (3, 0, None, None) , 
			 (11, 0, None, None) , ], 1 , 1 , 4 , 0 , 72 , (11, 0, None, None) , 0 , )),
	(( 'BeginChoiceProperty' , 'objRef' , 'propID' , ), 1610743814, (1610743814, (), [ (3, 0, None, None) , 
			 (5, 0, None, None) , ], 1 , 1 , 4 , 0 , 80 , (11, 0, None, None) , 0 , )),
	(( 'ChoiceProperty' , 'objRef' , 'propID' , ), 1610743815, (1610743815, (), [ (3, 0, None, None) , 
			 (5, 0, None, None) , ], 1 , 1 , 4 , 0 , 88 , (11, 0, None, None) , 0 , )),
]

IDocumentFileNotify_vtables_dispatch_ = 0
IDocumentFileNotify_vtables_ = [
	(( 'BeginCloseDocument' , ), 1610743808, (1610743808, (), [ ], 1 , 1 , 4 , 0 , 32 , (11, 0, None, None) , 0 , )),
	(( 'CloseDocument' , ), 1610743809, (1610743809, (), [ ], 1 , 1 , 4 , 0 , 40 , (11, 0, None, None) , 0 , )),
	(( 'BeginSaveDocument' , 'docName' , ), 1610743810, (1610743810, (), [ (30, 0, None, None) , ], 1 , 1 , 4 , 0 , 48 , (11, 0, None, None) , 0 , )),
	(( 'SaveDocument' , ), 1610743811, (1610743811, (), [ ], 1 , 1 , 4 , 0 , 56 , (11, 0, None, None) , 0 , )),
	(( 'Activate' , ), 1610743812, (1610743812, (), [ ], 1 , 1 , 4 , 0 , 64 , (11, 0, None, None) , 0 , )),
	(( 'Deactivate' , ), 1610743813, (1610743813, (), [ ], 1 , 1 , 4 , 0 , 72 , (11, 0, None, None) , 0 , )),
	(( 'BeginSaveAsDocument' , ), 1610743814, (1610743814, (), [ ], 1 , 1 , 4 , 0 , 80 , (11, 0, None, None) , 0 , )),
	(( 'DocumentFrameOpen' , 'v' , ), 1610743815, (1610743815, (), [ (13, 0, None, None) , ], 1 , 1 , 4 , 0 , 88 , (11, 0, None, None) , 0 , )),
	(( 'ProcessActivate' , 'Id' , ), 1610743816, (1610743816, (), [ (3, 0, None, None) , ], 1 , 1 , 4 , 0 , 96 , (11, 0, None, None) , 0 , )),
	(( 'ProcessDeactivate' , 'Id' , ), 1610743817, (1610743817, (), [ (3, 0, None, None) , ], 1 , 1 , 4 , 0 , 104 , (11, 0, None, None) , 0 , )),
	(( 'BeginProcess' , 'Id' , ), 1610743818, (1610743818, (), [ (3, 0, None, None) , ], 1 , 1 , 4 , 0 , 112 , (11, 0, None, None) , 0 , )),
	(( 'EndProcess' , 'Id' , 'Success' , ), 1610743819, (1610743819, (), [ (3, 0, None, None) , 
			 (11, 0, None, None) , ], 1 , 1 , 4 , 0 , 120 , (11, 0, None, None) , 0 , )),
	(( 'BeginAutoSaveDocument' , 'docName' , ), 1610743820, (1610743820, (), [ (30, 0, None, None) , ], 1 , 1 , 4 , 0 , 128 , (11, 0, None, None) , 0 , )),
	(( 'AutoSaveDocument' , ), 1610743821, (1610743821, (), [ ], 1 , 1 , 4 , 0 , 136 , (11, 0, None, None) , 0 , )),
]

IDocumentFrameNotify_vtables_dispatch_ = 0
IDocumentFrameNotify_vtables_ = [
	(( 'BeginPaint' , 'paintObj' , ), 1610743808, (1610743808, (), [ (13, 0, None, None) , ], 1 , 1 , 4 , 0 , 32 , (11, 0, None, None) , 0 , )),
	(( 'ClosePaint' , 'paintObj' , ), 1610743809, (1610743809, (), [ (13, 0, None, None) , ], 1 , 1 , 4 , 0 , 40 , (11, 0, None, None) , 0 , )),
	(( 'MouseDown' , 'nButton' , 'nShiftState' , 'x' , 'y' , 
			 ), 1610743810, (1610743810, (), [ (2, 0, None, None) , (2, 0, None, None) , (3, 0, None, None) , (3, 0, None, None) , ], 1 , 1 , 4 , 0 , 48 , (11, 0, None, None) , 0 , )),
	(( 'MouseUp' , 'nButton' , 'nShiftState' , 'x' , 'y' , 
			 ), 1610743811, (1610743811, (), [ (2, 0, None, None) , (2, 0, None, None) , (3, 0, None, None) , (3, 0, None, None) , ], 1 , 1 , 4 , 0 , 56 , (11, 0, None, None) , 0 , )),
	(( 'MouseDblClick' , 'nButton' , 'nShiftState' , 'x' , 'y' , 
			 ), 1610743812, (1610743812, (), [ (2, 0, None, None) , (2, 0, None, None) , (3, 0, None, None) , (3, 0, None, None) , ], 1 , 1 , 4 , 0 , 64 , (11, 0, None, None) , 0 , )),
	(( 'BeginPaintGL' , 'drawMode' , ), 1610743813, (1610743813, (), [ (3, 0, None, None) , ], 1 , 1 , 4 , 0 , 72 , (11, 0, None, None) , 0 , )),
	(( 'ClosePaintGL' , 'drawMode' , ), 1610743814, (1610743814, (), [ (3, 0, None, None) , ], 1 , 1 , 4 , 0 , 80 , (11, 0, None, None) , 0 , )),
	(( 'AddGabarit' , 'gabObj' , ), 1610743815, (1610743815, (), [ (13, 0, None, None) , ], 1 , 1 , 4 , 0 , 88 , (11, 0, None, None) , 0 , )),
	(( 'Activate' , ), 1610743816, (1610743816, (), [ ], 1 , 1 , 4 , 0 , 96 , (11, 0, None, None) , 0 , )),
	(( 'Deactivate' , ), 1610743817, (1610743817, (), [ ], 1 , 1 , 4 , 0 , 104 , (11, 0, None, None) , 0 , )),
	(( 'CloseFrame' , ), 1610743818, (1610743818, (), [ ], 1 , 1 , 4 , 0 , 112 , (11, 0, None, None) , 0 , )),
	(( 'MouseMove' , 'nShiftState' , 'x' , 'y' , ), 1610743819, (1610743819, (), [ 
			 (2, 0, None, None) , (3, 0, None, None) , (3, 0, None, None) , ], 1 , 1 , 4 , 0 , 120 , (11, 0, None, None) , 0 , )),
	(( 'ShowOcxTree' , 'tree' , 'show' , ), 1610743820, (1610743820, (), [ (13, 0, None, None) , 
			 (11, 0, None, None) , ], 1 , 1 , 4 , 0 , 128 , (11, 0, None, None) , 0 , )),
	(( 'BeginPaintTmpObjects' , ), 1610743821, (1610743821, (), [ ], 1 , 1 , 4 , 0 , 136 , (11, 0, None, None) , 0 , )),
	(( 'ClosePaintTmpObjects' , ), 1610743822, (1610743822, (), [ ], 1 , 1 , 4 , 0 , 144 , (11, 0, None, None) , 0 , )),
]

IKompasNotify_vtables_dispatch_ = 0
IKompasNotify_vtables_ = [
	(( 'IsNotifyProcess' , 'notifyType' , ), 1610678272, (1610678272, (), [ (3, 0, None, None) , ], 1 , 1 , 4 , 0 , 24 , (11, 0, None, None) , 0 , )),
]

IKompasObjectNotify_vtables_dispatch_ = 0
IKompasObjectNotify_vtables_ = [
	(( 'CreateDocument' , 'pDoc' , 'docType' , ), 1610743808, (1610743808, (), [ (3, 0, None, None) , 
			 (3, 0, None, None) , ], 1 , 1 , 4 , 0 , 32 , (11, 0, None, None) , 0 , )),
	(( 'BeginOpenDocument' , 'docName' , ), 1610743809, (1610743809, (), [ (30, 0, None, None) , ], 1 , 1 , 4 , 0 , 40 , (11, 0, None, None) , 0 , )),
	(( 'OpenDocument' , 'pDoc' , 'docType' , ), 1610743810, (1610743810, (), [ (3, 0, None, None) , 
			 (3, 0, None, None) , ], 1 , 1 , 4 , 0 , 48 , (11, 0, None, None) , 0 , )),
	(( 'ChangeActiveDocument' , 'pDoc' , 'docType' , ), 1610743811, (1610743811, (), [ (3, 0, None, None) , 
			 (3, 0, None, None) , ], 1 , 1 , 4 , 0 , 56 , (11, 0, None, None) , 0 , )),
	(( 'ApplicationDestroy' , ), 1610743812, (1610743812, (), [ ], 1 , 1 , 4 , 0 , 64 , (11, 0, None, None) , 0 , )),
	(( 'BeginCreate' , 'docType' , ), 1610743813, (1610743813, (), [ (3, 0, None, None) , ], 1 , 1 , 4 , 0 , 72 , (11, 0, None, None) , 0 , )),
	(( 'BeginOpenFile' , ), 1610743814, (1610743814, (), [ ], 1 , 1 , 4 , 0 , 80 , (11, 0, None, None) , 0 , )),
	(( 'BeginCloseAllDocument' , ), 1610743815, (1610743815, (), [ ], 1 , 1 , 4 , 0 , 88 , (11, 0, None, None) , 0 , )),
	(( 'KeyDown' , 'key' , 'flags' , 'sysKey' , ), 1610743816, (1610743816, (), [ 
			 (16387, 3, None, None) , (3, 1, None, None) , (11, 1, None, None) , ], 1 , 1 , 4 , 0 , 96 , (11, 0, None, None) , 0 , )),
	(( 'KeyUp' , 'key' , 'flags' , 'sysKey' , ), 1610743817, (1610743817, (), [ 
			 (16387, 3, None, None) , (3, 1, None, None) , (11, 1, None, None) , ], 1 , 1 , 4 , 0 , 104 , (11, 0, None, None) , 0 , )),
	(( 'KeyPress' , 'key' , 'sysKey' , ), 1610743818, (1610743818, (), [ (16387, 3, None, None) , 
			 (11, 1, None, None) , ], 1 , 1 , 4 , 0 , 112 , (11, 0, None, None) , 0 , )),
	(( 'BeginRequestFiles' , 'requestID' , 'files' , ), 1610743819, (1610743819, (), [ (3, 1, None, None) , 
			 (16396, 3, None, None) , ], 1 , 1 , 4 , 0 , 120 , (11, 0, None, None) , 0 , )),
	(( 'BeginChoiceMaterial' , 'MaterialPropertyId' , ), 1610743820, (1610743820, (), [ (3, 0, None, None) , ], 1 , 1 , 4 , 0 , 128 , (11, 0, None, None) , 0 , )),
	(( 'ChoiceMaterial' , 'MaterialPropertyId' , 'material' , 'density' , ), 1610743821, (1610743821, (), [ 
			 (3, 0, None, None) , (30, 0, None, None) , (5, 0, None, None) , ], 1 , 1 , 4 , 0 , 136 , (11, 0, None, None) , 0 , )),
	(( 'IsNeedConvertToSavePrevious' , 'pDoc' , 'docType' , 'saveVersion' , 'saveToPreviusParam' , 
			 'needConvert' , ), 1610743822, (1610743822, (), [ (3, 1, None, None) , (3, 1, None, None) , (3, 1, None, None) , 
			 (13, 1, None, None) , (16395, 3, None, None) , ], 1 , 1 , 4 , 0 , 144 , (11, 0, None, None) , 0 , )),
	(( 'BeginConvertToSavePrevious' , 'pDoc' , 'docType' , 'saveVersion' , 'saveToPreviusParam' , 
			 ), 1610743823, (1610743823, (), [ (3, 0, None, None) , (3, 0, None, None) , (3, 0, None, None) , (13, 0, None, None) , ], 1 , 1 , 4 , 0 , 152 , (11, 0, None, None) , 0 , )),
	(( 'EndConvertToSavePrevious' , 'pDoc' , 'docType' , 'saveVersion' , 'saveToPreviusParam' , 
			 ), 1610743824, (1610743824, (), [ (3, 0, None, None) , (3, 0, None, None) , (3, 0, None, None) , (13, 0, None, None) , ], 1 , 1 , 4 , 0 , 160 , (11, 0, None, None) , 0 , )),
	(( 'ChangeTheme' , 'newTheme' , ), 1610743825, (1610743825, (), [ (3, 0, None, None) , ], 1 , 1 , 4 , 0 , 168 , (11, 0, None, None) , 0 , )),
]

ILibraryManagerNotify_vtables_dispatch_ = 0
ILibraryManagerNotify_vtables_ = [
	(( 'BeginAttach' , 'PLibrary' , ), 1610743808, (1610743808, (), [ (13, 0, None, None) , ], 1 , 1 , 4 , 0 , 32 , (11, 0, None, None) , 0 , )),
	(( 'Attach' , 'PLibrary' , ), 1610743809, (1610743809, (), [ (13, 0, None, None) , ], 1 , 1 , 4 , 0 , 40 , (11, 0, None, None) , 0 , )),
	(( 'BeginDetach' , 'PLibrary' , ), 1610743810, (1610743810, (), [ (13, 0, None, None) , ], 1 , 1 , 4 , 0 , 48 , (11, 0, None, None) , 0 , )),
	(( 'Detach' , 'PLibrary' , ), 1610743811, (1610743811, (), [ (13, 0, None, None) , ], 1 , 1 , 4 , 0 , 56 , (11, 0, None, None) , 0 , )),
	(( 'BeginExecute' , 'PLibrary' , ), 1610743812, (1610743812, (), [ (13, 0, None, None) , ], 1 , 1 , 4 , 0 , 64 , (11, 0, None, None) , 0 , )),
	(( 'EndExecute' , 'PLibrary' , ), 1610743813, (1610743813, (), [ (13, 0, None, None) , ], 1 , 1 , 4 , 0 , 72 , (11, 0, None, None) , 0 , )),
	(( 'SystemControlStop' , 'PLibrary' , ), 1610743814, (1610743814, (), [ (13, 0, None, None) , ], 1 , 1 , 4 , 0 , 80 , (11, 0, None, None) , 0 , )),
	(( 'SystemControlStart' , 'PLibrary' , ), 1610743815, (1610743815, (), [ (13, 0, None, None) , ], 1 , 1 , 4 , 0 , 88 , (11, 0, None, None) , 0 , )),
	(( 'AddLibraryDescription' , 'PLibrary' , ), 1610743816, (1610743816, (), [ (13, 0, None, None) , ], 1 , 1 , 4 , 0 , 96 , (11, 0, None, None) , 0 , )),
	(( 'DeleteLibraryDescription' , 'PLibrary' , ), 1610743817, (1610743817, (), [ (13, 0, None, None) , ], 1 , 1 , 4 , 0 , 104 , (11, 0, None, None) , 0 , )),
	(( 'AddInsert' , 'PInsert' , 'create' , ), 1610743818, (1610743818, (), [ (13, 0, None, None) , 
			 (11, 0, None, None) , ], 1 , 1 , 4 , 0 , 112 , (11, 0, None, None) , 0 , )),
	(( 'DeleteInsert' , 'PInsert' , ), 1610743819, (1610743819, (), [ (13, 0, None, None) , ], 1 , 1 , 4 , 0 , 120 , (11, 0, None, None) , 0 , )),
	(( 'EditInsert' , 'PLibrary' , 'pDoc' , 'newFrw' , ), 1610743820, (1610743820, (), [ 
			 (13, 0, None, None) , (3, 0, None, None) , (11, 0, None, None) , ], 1 , 1 , 4 , 0 , 128 , (11, 0, None, None) , 0 , )),
	(( 'TryExecute' , 'PLibrary' , 'commandId' , ), 1610743821, (1610743821, (), [ (13, 0, None, None) , 
			 (3, 0, None, None) , ], 1 , 1 , 4 , 0 , 136 , (11, 0, None, None) , 0 , )),
	(( 'BeginInsertDocument' , 'PLibrary' , 'InsertionType' , 'Insertion' , ), 1610743822, (1610743822, (), [ 
			 (13, 0, None, None) , (3, 0, None, None) , (8, 0, None, None) , ], 1 , 1 , 4 , 0 , 144 , (11, 0, None, None) , 0 , )),
]

IMouseEnterLeaveParameters_vtables_dispatch_ = 0
IMouseEnterLeaveParameters_vtables_ = [
	(( 'GetX' , ), 1610678272, (1610678272, (), [ ], 1 , 1 , 4 , 0 , 24 , (5, 0, None, None) , 0 , )),
	(( 'SetX' , 'NewVal' , ), 1610678273, (1610678273, (), [ (5, 0, None, None) , ], 1 , 1 , 4 , 0 , 32 , (24, 0, None, None) , 0 , )),
	(( 'GetY' , ), 1610678274, (1610678274, (), [ ], 1 , 1 , 4 , 0 , 40 , (5, 0, None, None) , 0 , )),
	(( 'SetY' , 'NewVal' , ), 1610678275, (1610678275, (), [ (5, 0, None, None) , ], 1 , 1 , 4 , 0 , 48 , (24, 0, None, None) , 0 , )),
	(( 'GetOffset' , ), 1610678276, (1610678276, (), [ ], 1 , 1 , 4 , 0 , 56 , (5, 0, None, None) , 0 , )),
	(( 'SetOffset' , 'NewVal' , ), 1610678277, (1610678277, (), [ (5, 0, None, None) , ], 1 , 1 , 4 , 0 , 64 , (24, 0, None, None) , 0 , )),
	(( 'GetOffsetAngle' , ), 1610678278, (1610678278, (), [ ], 1 , 1 , 4 , 0 , 72 , (5, 0, None, None) , 0 , )),
	(( 'SetOffsetAngle' , 'NewVal' , ), 1610678279, (1610678279, (), [ (5, 0, None, None) , ], 1 , 1 , 4 , 0 , 80 , (24, 0, None, None) , 0 , )),
	(( 'GetSymbol' , ), 1610678280, (1610678280, (), [ ], 1 , 1 , 4 , 0 , 88 , (3, 0, None, None) , 0 , )),
	(( 'SetSymbol' , 'NewVal' , ), 1610678281, (1610678281, (), [ (3, 0, None, None) , ], 1 , 1 , 4 , 0 , 96 , (24, 0, None, None) , 0 , )),
	(( 'GetSymbolFont' , ), 1610678282, (1610678282, (), [ ], 1 , 1 , 4 , 0 , 104 , (8, 0, None, None) , 0 , )),
	(( 'SetSymbolFont' , 'NewVal' , ), 1610678283, (1610678283, (), [ (8, 0, None, None) , ], 1 , 1 , 4 , 0 , 112 , (24, 0, None, None) , 0 , )),
	(( 'GetSymbolColor' , ), 1610678284, (1610678284, (), [ ], 1 , 1 , 4 , 0 , 120 , (3, 0, None, None) , 0 , )),
	(( 'SetSymbolColor' , 'NewVal' , ), 1610678285, (1610678285, (), [ (3, 0, None, None) , ], 1 , 1 , 4 , 0 , 128 , (24, 0, None, None) , 0 , )),
	(( 'GetSymbolScale' , ), 1610678286, (1610678286, (), [ ], 1 , 1 , 4 , 0 , 136 , (5, 0, None, None) , 0 , )),
	(( 'SetSymbolScale' , 'NewVal' , ), 1610678287, (1610678287, (), [ (5, 0, None, None) , ], 1 , 1 , 4 , 0 , 144 , (24, 0, None, None) , 0 , )),
]

IObject2DNotify_vtables_dispatch_ = 0
IObject2DNotify_vtables_ = [
	(( 'ChangeActive' , 'objRef' , ), 1610743808, (1610743808, (), [ (3, 0, None, None) , ], 1 , 1 , 4 , 0 , 32 , (11, 0, None, None) , 0 , )),
	(( 'BeginDelete' , 'objRef' , ), 1610743809, (1610743809, (), [ (3, 0, None, None) , ], 1 , 1 , 4 , 0 , 40 , (11, 0, None, None) , 0 , )),
	(( 'Delete' , 'objRef' , ), 1610743810, (1610743810, (), [ (3, 0, None, None) , ], 1 , 1 , 4 , 0 , 48 , (11, 0, None, None) , 0 , )),
	(( 'BeginMove' , 'objRef' , ), 1610743811, (1610743811, (), [ (3, 0, None, None) , ], 1 , 1 , 4 , 0 , 56 , (11, 0, None, None) , 0 , )),
	(( 'Move' , 'objRef' , ), 1610743812, (1610743812, (), [ (3, 0, None, None) , ], 1 , 1 , 4 , 0 , 64 , (11, 0, None, None) , 0 , )),
	(( 'BeginRotate' , 'obgRef' , ), 1610743813, (1610743813, (), [ (3, 0, None, None) , ], 1 , 1 , 4 , 0 , 72 , (11, 0, None, None) , 0 , )),
	(( 'Rotate' , 'objRef' , ), 1610743814, (1610743814, (), [ (3, 0, None, None) , ], 1 , 1 , 4 , 0 , 80 , (11, 0, None, None) , 0 , )),
	(( 'BeginScale' , 'obgRef' , ), 1610743815, (1610743815, (), [ (3, 0, None, None) , ], 1 , 1 , 4 , 0 , 88 , (11, 0, None, None) , 0 , )),
	(( 'Scale' , 'objRef' , ), 1610743816, (1610743816, (), [ (3, 0, None, None) , ], 1 , 1 , 4 , 0 , 96 , (11, 0, None, None) , 0 , )),
	(( 'BeginTransform' , 'objRef' , ), 1610743817, (1610743817, (), [ (3, 0, None, None) , ], 1 , 1 , 4 , 0 , 104 , (11, 0, None, None) , 0 , )),
	(( 'Transform' , 'objRef' , ), 1610743818, (1610743818, (), [ (3, 0, None, None) , ], 1 , 1 , 4 , 0 , 112 , (11, 0, None, None) , 0 , )),
	(( 'BeginCopy' , 'objRef' , ), 1610743819, (1610743819, (), [ (3, 0, None, None) , ], 1 , 1 , 4 , 0 , 120 , (11, 0, None, None) , 0 , )),
	(( 'Copy' , 'objRef' , ), 1610743820, (1610743820, (), [ (3, 0, None, None) , ], 1 , 1 , 4 , 0 , 128 , (11, 0, None, None) , 0 , )),
	(( 'BeginSymmetry' , 'objRef' , ), 1610743821, (1610743821, (), [ (3, 0, None, None) , ], 1 , 1 , 4 , 0 , 136 , (11, 0, None, None) , 0 , )),
	(( 'Symmetry' , 'objRef' , ), 1610743822, (1610743822, (), [ (3, 0, None, None) , ], 1 , 1 , 4 , 0 , 144 , (11, 0, None, None) , 0 , )),
	(( 'BeginProcess' , 'pType' , 'objRef' , ), 1610743823, (1610743823, (), [ (3, 0, None, None) , 
			 (3, 0, None, None) , ], 1 , 1 , 4 , 0 , 152 , (11, 0, None, None) , 0 , )),
	(( 'EndProcess' , 'pType' , ), 1610743824, (1610743824, (), [ (3, 0, None, None) , ], 1 , 1 , 4 , 0 , 160 , (11, 0, None, None) , 0 , )),
	(( 'CreateObject' , 'objRef' , ), 1610743825, (1610743825, (), [ (3, 0, None, None) , ], 1 , 1 , 4 , 0 , 168 , (11, 0, None, None) , 0 , )),
	(( 'UpdateObject' , 'objRef' , ), 1610743826, (1610743826, (), [ (3, 0, None, None) , ], 1 , 1 , 4 , 0 , 176 , (11, 0, None, None) , 0 , )),
	(( 'BeginDestroyObject' , 'objRef' , ), 1610743827, (1610743827, (), [ (3, 0, None, None) , ], 1 , 1 , 4 , 0 , 184 , (11, 0, None, None) , 0 , )),
	(( 'DestroyObject' , 'objRef' , ), 1610743828, (1610743828, (), [ (3, 0, None, None) , ], 1 , 1 , 4 , 0 , 192 , (11, 0, None, None) , 0 , )),
	(( 'BeginPropertyChanged' , 'objRef' , ), 1610743829, (1610743829, (), [ (3, 0, None, None) , ], 1 , 1 , 4 , 0 , 200 , (11, 0, None, None) , 0 , )),
	(( 'PropertyChanged' , 'objRef' , ), 1610743830, (1610743830, (), [ (3, 0, None, None) , ], 1 , 1 , 4 , 0 , 208 , (11, 0, None, None) , 0 , )),
]

IObject2DNotifyResult_vtables_dispatch_ = 0
IObject2DNotifyResult_vtables_ = [
	(( 'GetNotifyType' , ), 1610678272, (1610678272, (), [ ], 1 , 1 , 4 , 0 , 24 , (3, 0, None, None) , 0 , )),
	(( 'IsCopy' , ), 1610678273, (1610678273, (), [ ], 1 , 1 , 4 , 0 , 32 , (11, 0, None, None) , 0 , )),
	(( 'GetSheetPoint' , 'from' , 'x' , 'y' , ), 1610678274, (1610678274, (), [ 
			 (11, 1, None, None) , (16389, 2, None, None) , (16389, 2, None, None) , ], 1 , 1 , 4 , 0 , 40 , (11, 0, None, None) , 0 , )),
	(( 'GetCopyObject' , ), 1610678275, (1610678275, (), [ ], 1 , 1 , 4 , 0 , 48 , (3, 0, None, None) , 0 , )),
	(( 'GetAngle' , ), 1610678276, (1610678276, (), [ ], 1 , 1 , 4 , 0 , 56 , (5, 0, None, None) , 0 , )),
	(( 'GetScale' , 'sx' , 'sy' , ), 1610678277, (1610678277, (), [ (16389, 2, None, None) , 
			 (16389, 2, None, None) , ], 1 , 1 , 4 , 0 , 64 , (11, 0, None, None) , 0 , )),
	(( 'GetProcessType' , ), 1610678278, (1610678278, (), [ ], 1 , 1 , 4 , 0 , 72 , (3, 0, None, None) , 0 , )),
	(( 'IsUndoMode' , ), 1610678279, (1610678279, (), [ ], 1 , 1 , 4 , 0 , 80 , (11, 0, None, None) , 0 , )),
	(( 'IsRedoMode' , ), 1610678280, (1610678280, (), [ ], 1 , 1 , 4 , 0 , 88 , (11, 0, None, None) , 0 , )),
]

IParametrizationParam_vtables_dispatch_ = 0
IParametrizationParam_vtables_ = [
	(( 'GetNearestPoints' , ), 1610678272, (1610678272, (), [ ], 1 , 1 , 4 , 0 , 24 , (11, 0, None, None) , 0 , )),
	(( 'SetNearestPoints' , 'value' , ), 1610678273, (1610678273, (), [ (11, 0, None, None) , ], 1 , 1 , 4 , 0 , 32 , (11, 0, None, None) , 0 , )),
	(( 'GetPointsLimit' , ), 1610678274, (1610678274, (), [ ], 1 , 1 , 4 , 0 , 40 , (5, 0, None, None) , 0 , )),
	(( 'SetPointsLimit' , 'value' , ), 1610678275, (1610678275, (), [ (5, 0, None, None) , ], 1 , 1 , 4 , 0 , 48 , (11, 0, None, None) , 0 , )),
	(( 'GetHorizontal' , ), 1610678276, (1610678276, (), [ ], 1 , 1 , 4 , 0 , 56 , (11, 0, None, None) , 0 , )),
	(( 'SetHorizontal' , 'value' , ), 1610678277, (1610678277, (), [ (11, 0, None, None) , ], 1 , 1 , 4 , 0 , 64 , (11, 0, None, None) , 0 , )),
	(( 'GetVertical' , ), 1610678278, (1610678278, (), [ ], 1 , 1 , 4 , 0 , 72 , (11, 0, None, None) , 0 , )),
	(( 'SetVertical' , 'value' , ), 1610678279, (1610678279, (), [ (11, 0, None, None) , ], 1 , 1 , 4 , 0 , 80 , (11, 0, None, None) , 0 , )),
	(( 'GetParallel' , ), 1610678280, (1610678280, (), [ ], 1 , 1 , 4 , 0 , 88 , (11, 0, None, None) , 0 , )),
	(( 'SetParallel' , 'value' , ), 1610678281, (1610678281, (), [ (11, 0, None, None) , ], 1 , 1 , 4 , 0 , 96 , (11, 0, None, None) , 0 , )),
	(( 'GetPerpendicular' , ), 1610678282, (1610678282, (), [ ], 1 , 1 , 4 , 0 , 104 , (11, 0, None, None) , 0 , )),
	(( 'SetPerpendicular' , 'value' , ), 1610678283, (1610678283, (), [ (11, 0, None, None) , ], 1 , 1 , 4 , 0 , 112 , (11, 0, None, None) , 0 , )),
	(( 'GetAngleLimit' , ), 1610678284, (1610678284, (), [ ], 1 , 1 , 4 , 0 , 120 , (5, 0, None, None) , 0 , )),
	(( 'SetAngleLimit' , 'value' , ), 1610678285, (1610678285, (), [ (5, 0, None, None) , ], 1 , 1 , 4 , 0 , 128 , (11, 0, None, None) , 0 , )),
	(( 'Init' , ), 1610678286, (1610678286, (), [ ], 1 , 1 , 4 , 0 , 136 , (11, 0, None, None) , 0 , )),
]

IProcess2DNotify_vtables_dispatch_ = 0
IProcess2DNotify_vtables_ = [
	(( 'PlacementChange' , 'x' , 'y' , 'angle' , 'dynamic' , 
			 ), 1610743808, (1610743808, (), [ (5, 0, None, None) , (5, 0, None, None) , (5, 0, None, None) , (11, 0, None, None) , ], 1 , 1 , 4 , 0 , 32 , (11, 0, None, None) , 0 , )),
	(( 'ExecuteCommand' , 'command' , ), 1610743809, (1610743809, (), [ (3, 0, None, None) , ], 1 , 1 , 4 , 0 , 40 , (11, 0, None, None) , 0 , )),
	(( 'Run' , ), 1610743810, (1610743810, (), [ ], 1 , 1 , 4 , 0 , 48 , (11, 0, None, None) , 0 , )),
	(( 'Stop' , ), 1610743811, (1610743811, (), [ ], 1 , 1 , 4 , 0 , 56 , (11, 0, None, None) , 0 , )),
	(( 'Activate' , ), 1610743812, (1610743812, (), [ ], 1 , 1 , 4 , 0 , 64 , (11, 0, None, None) , 0 , )),
	(( 'Deactivate' , ), 1610743813, (1610743813, (), [ ], 1 , 1 , 4 , 0 , 72 , (11, 0, None, None) , 0 , )),
	(( 'EndProcess' , ), 1610743814, (1610743814, (), [ ], 1 , 1 , 4 , 0 , 80 , (11, 0, None, None) , 0 , )),
	(( 'GetMouseEnterLeavePoint' , 'Control' , 'btnID' , 'pointIndex' , 'parameters' , 
			 ), 1610743815, (1610743815, (), [ (13, 0, None, None) , (3, 0, None, None) , (3, 0, None, None) , (13, 0, None, None) , ], 1 , 1 , 4 , 0 , 88 , (11, 0, None, None) , 0 , )),
]

IPropertyManagerNotify_vtables_dispatch_ = 0
IPropertyManagerNotify_vtables_ = [
	(( 'ButtonClick' , 'buttonID' , ), 1610743808, (1610743808, (), [ (3, 0, None, None) , ], 1 , 1 , 4 , 0 , 32 , (11, 0, None, None) , 0 , )),
	(( 'ChangeControlValue' , 'ctrl' , ), 1610743809, (1610743809, (), [ (13, 0, None, None) , ], 1 , 1 , 4 , 0 , 40 , (11, 0, None, None) , 0 , )),
	(( 'ControlCommand' , 'ctrl' , 'buttonID' , ), 1610743810, (1610743810, (), [ (13, 0, None, None) , 
			 (3, 0, None, None) , ], 1 , 1 , 4 , 0 , 48 , (11, 0, None, None) , 0 , )),
	(( 'ButtonUpdate' , 'buttonID' , 'check' , '_enable' , ), 1610743811, (1610743811, (), [ 
			 (3, 1, None, None) , (16387, 3, None, None) , (16395, 3, None, None) , ], 1 , 1 , 4 , 0 , 56 , (11, 0, None, None) , 0 , )),
	(( 'ProcessActivate' , ), 1610743812, (1610743812, (), [ ], 1 , 1 , 4 , 0 , 64 , (11, 0, None, None) , 0 , )),
	(( 'ProcessDeactivate' , ), 1610743813, (1610743813, (), [ ], 1 , 1 , 4 , 0 , 72 , (11, 0, None, None) , 0 , )),
	(( 'CommandHelp' , 'Id' , ), 1610743814, (1610743814, (), [ (3, 0, None, None) , ], 1 , 1 , 4 , 0 , 80 , (11, 0, None, None) , 0 , )),
	(( 'SelectItem' , 'Control' , 'Index' , 'Select' , ), 1610743815, (1610743815, (), [ 
			 (13, 0, None, None) , (3, 0, None, None) , (11, 0, None, None) , ], 1 , 1 , 4 , 0 , 88 , (11, 0, None, None) , 0 , )),
	(( 'CheckItem' , 'Control' , 'Index' , 'check' , ), 1610743816, (1610743816, (), [ 
			 (13, 0, None, None) , (3, 0, None, None) , (11, 0, None, None) , ], 1 , 1 , 4 , 0 , 96 , (11, 0, None, None) , 0 , )),
	(( 'ChangeActiveTab' , 'TabIndex' , ), 1610743817, (1610743817, (), [ (3, 0, None, None) , ], 1 , 1 , 4 , 0 , 104 , (11, 0, None, None) , 0 , )),
	(( 'EditFocus' , 'ctrl' , 'Set' , ), 1610743818, (1610743818, (), [ (13, 0, None, None) , 
			 (11, 0, None, None) , ], 1 , 1 , 4 , 0 , 112 , (11, 0, None, None) , 0 , )),
	(( 'UserMenuCommand' , 'ctrl' , 'menuID' , ), 1610743819, (1610743819, (), [ (13, 0, None, None) , 
			 (3, 0, None, None) , ], 1 , 1 , 4 , 0 , 120 , (11, 0, None, None) , 0 , )),
	(( 'LayoutChanged' , ), 1610743820, (1610743820, (), [ ], 1 , 1 , 4 , 0 , 128 , (11, 0, None, None) , 0 , )),
	(( 'GetContextMenuType' , 'LX' , 'LY' , 'ContextMenuType' , ), 1610743821, (1610743821, (), [ 
			 (3, 1, None, None) , (3, 1, None, None) , (16387, 3, None, None) , ], 1 , 1 , 4 , 0 , 136 , (11, 0, None, None) , 0 , )),
	(( 'FillContextPanel' , 'ContextPanel' , ), 1610743822, (1610743822, (), [ (13, 0, None, None) , ], 1 , 1 , 4 , 0 , 144 , (11, 0, None, None) , 0 , )),
	(( 'FillContextIconMenu' , 'menu' , ), 1610743823, (1610743823, (), [ (13, 0, None, None) , ], 1 , 1 , 4 , 0 , 152 , (11, 0, None, None) , 0 , )),
	(( 'EndEditItem' , 'ctrl' , 'Index' , ), 1610743824, (1610743824, (), [ (13, 0, None, None) , 
			 (3, 0, None, None) , ], 1 , 1 , 4 , 0 , 160 , (11, 0, None, None) , 0 , )),
	(( 'ChangeTabExpanded' , 'TabIndex' , ), 1610743825, (1610743825, (), [ (3, 0, None, None) , ], 1 , 1 , 4 , 0 , 168 , (11, 0, None, None) , 0 , )),
]

ISaveToPreviusParam_vtables_dispatch_ = 0
ISaveToPreviusParam_vtables_ = [
	(( 'AddWarning' , 'uniqueID' , 'optionName' , 'text' , ), 1610678272, (1610678272, (), [ 
			 (8, 0, None, None) , (8, 0, None, None) , (8, 0, None, None) , ], 1 , 1 , 4 , 0 , 24 , (11, 0, None, None) , 0 , )),
	(( 'AddOption' , 'uniqueID' , 'optionName' , 'options' , 'defaultValue' , 
			 ), 1610678273, (1610678273, (), [ (8, 0, None, None) , (8, 0, None, None) , (12, 0, None, None) , (8, 0, None, None) , ], 1 , 1 , 4 , 0 , 32 , (11, 0, None, None) , 0 , )),
	(( 'GetCurrentOptionValue' , 'uniqueID' , ), 1610678274, (1610678274, (), [ (8, 0, None, None) , ], 1 , 1 , 4 , 0 , 40 , (8, 0, None, None) , 0 , )),
]

ISelectionMngNotify_vtables_dispatch_ = 0
ISelectionMngNotify_vtables_ = [
	(( 'Select' , 'obj' , ), 1610743808, (1610743808, (), [ (12, 0, None, None) , ], 1 , 1 , 4 , 0 , 32 , (11, 0, None, None) , 0 , )),
	(( 'Unselect' , 'obj' , ), 1610743809, (1610743809, (), [ (12, 0, None, None) , ], 1 , 1 , 4 , 0 , 40 , (11, 0, None, None) , 0 , )),
	(( 'UnselectAll' , ), 1610743810, (1610743810, (), [ ], 1 , 1 , 4 , 0 , 48 , (11, 0, None, None) , 0 , )),
]

ISnapInfo_vtables_dispatch_ = 0
ISnapInfo_vtables_ = [
	(( 'GetSnapType1' , ), 1610678272, (1610678272, (), [ ], 1 , 1 , 4 , 0 , 24 , (3, 0, None, None) , 0 , )),
	(( 'GetObject1' , ), 1610678273, (1610678273, (), [ ], 1 , 1 , 4 , 0 , 32 , (3, 0, None, None) , 0 , )),
	(( 'GetSnapType2' , ), 1610678274, (1610678274, (), [ ], 1 , 1 , 4 , 0 , 40 , (3, 0, None, None) , 0 , )),
	(( 'GetObject2' , ), 1610678275, (1610678275, (), [ ], 1 , 1 , 4 , 0 , 48 , (3, 0, None, None) , 0 , )),
	(( 'GetPoint' , 'x' , 'y' , ), 1610678276, (1610678276, (), [ (16389, 2, None, None) , 
			 (16389, 2, None, None) , ], 1 , 1 , 4 , 0 , 56 , (11, 0, None, None) , 0 , )),
]

ISpcDocumentNotify_vtables_dispatch_ = 0
ISpcDocumentNotify_vtables_ = [
	(( 'DocumentBeginAdd' , ), 1610743808, (1610743808, (), [ ], 1 , 1 , 4 , 0 , 32 , (11, 0, None, None) , 0 , )),
	(( 'DocumentAdd' , 'docName' , ), 1610743809, (1610743809, (), [ (30, 0, None, None) , ], 1 , 1 , 4 , 0 , 40 , (11, 0, None, None) , 0 , )),
	(( 'DocumentBeginRemove' , 'docName' , ), 1610743810, (1610743810, (), [ (30, 0, None, None) , ], 1 , 1 , 4 , 0 , 48 , (11, 0, None, None) , 0 , )),
	(( 'DocumentRemove' , 'docName' , ), 1610743811, (1610743811, (), [ (30, 0, None, None) , ], 1 , 1 , 4 , 0 , 56 , (11, 0, None, None) , 0 , )),
	(( 'SpcStyleBeginChange' , 'libName' , 'numb' , ), 1610743812, (1610743812, (), [ (30, 0, None, None) , 
			 (3, 0, None, None) , ], 1 , 1 , 4 , 0 , 64 , (11, 0, None, None) , 0 , )),
	(( 'SpcStyleChange' , 'libName' , 'numb' , ), 1610743813, (1610743813, (), [ (30, 0, None, None) , 
			 (3, 0, None, None) , ], 1 , 1 , 4 , 0 , 72 , (11, 0, None, None) , 0 , )),
]

ISpcObjectNotify_vtables_dispatch_ = 0
ISpcObjectNotify_vtables_ = [
	(( 'BeginDelete' , 'objRef' , ), 1610743808, (1610743808, (), [ (3, 0, None, None) , ], 1 , 1 , 4 , 0 , 32 , (11, 0, None, None) , 0 , )),
	(( 'Delete' , 'objRef' , ), 1610743809, (1610743809, (), [ (3, 0, None, None) , ], 1 , 1 , 4 , 0 , 40 , (11, 0, None, None) , 0 , )),
	(( 'CellDblClick' , 'objRef' , 'number' , ), 1610743810, (1610743810, (), [ (3, 0, None, None) , 
			 (3, 0, None, None) , ], 1 , 1 , 4 , 0 , 48 , (11, 0, None, None) , 0 , )),
	(( 'CellBeginEdit' , 'objRef' , 'number' , ), 1610743811, (1610743811, (), [ (3, 0, None, None) , 
			 (3, 0, None, None) , ], 1 , 1 , 4 , 0 , 56 , (11, 0, None, None) , 0 , )),
	(( 'ChangeCurrent' , 'objRef' , ), 1610743812, (1610743812, (), [ (3, 0, None, None) , ], 1 , 1 , 4 , 0 , 64 , (11, 0, None, None) , 0 , )),
	(( 'DocumentBeginAdd' , 'objRef' , ), 1610743813, (1610743813, (), [ (3, 0, None, None) , ], 1 , 1 , 4 , 0 , 72 , (11, 0, None, None) , 0 , )),
	(( 'DocumentAdd' , 'objRef' , 'docName' , ), 1610743814, (1610743814, (), [ (3, 0, None, None) , 
			 (30, 0, None, None) , ], 1 , 1 , 4 , 0 , 80 , (11, 0, None, None) , 0 , )),
	(( 'DocumentRemove' , 'objRef' , 'docName' , ), 1610743815, (1610743815, (), [ (3, 0, None, None) , 
			 (30, 0, None, None) , ], 1 , 1 , 4 , 0 , 88 , (11, 0, None, None) , 0 , )),
	(( 'BeginGeomChange' , 'objRef' , ), 1610743816, (1610743816, (), [ (3, 0, None, None) , ], 1 , 1 , 4 , 0 , 96 , (11, 0, None, None) , 0 , )),
	(( 'GeomChange' , 'objRef' , ), 1610743817, (1610743817, (), [ (3, 0, None, None) , ], 1 , 1 , 4 , 0 , 104 , (11, 0, None, None) , 0 , )),
	(( 'BeginProcess' , 'pType' , 'objRef' , ), 1610743818, (1610743818, (), [ (3, 0, None, None) , 
			 (3, 0, None, None) , ], 1 , 1 , 4 , 0 , 112 , (11, 0, None, None) , 0 , )),
	(( 'EndProcess' , 'pType' , ), 1610743819, (1610743819, (), [ (3, 0, None, None) , ], 1 , 1 , 4 , 0 , 120 , (11, 0, None, None) , 0 , )),
	(( 'CreateObject' , 'objRef' , ), 1610743820, (1610743820, (), [ (3, 0, None, None) , ], 1 , 1 , 4 , 0 , 128 , (11, 0, None, None) , 0 , )),
	(( 'UpdateObject' , 'objRef' , ), 1610743821, (1610743821, (), [ (3, 0, None, None) , ], 1 , 1 , 4 , 0 , 136 , (11, 0, None, None) , 0 , )),
	(( 'BeginCopy' , 'objRef' , ), 1610743822, (1610743822, (), [ (3, 0, None, None) , ], 1 , 1 , 4 , 0 , 144 , (11, 0, None, None) , 0 , )),
	(( 'Copy' , 'objRef' , ), 1610743823, (1610743823, (), [ (3, 0, None, None) , ], 1 , 1 , 4 , 0 , 152 , (11, 0, None, None) , 0 , )),
]

ISpecificationNotify_vtables_dispatch_ = 0
ISpecificationNotify_vtables_ = [
	(( 'TuningSpcStyleBeginChange' , 'libName' , 'numb' , ), 1610743808, (1610743808, (), [ (30, 0, None, None) , 
			 (3, 0, None, None) , ], 1 , 1 , 4 , 0 , 32 , (11, 0, None, None) , 0 , )),
	(( 'TuningSpcStyleChange' , 'libName' , 'numb' , 'isOk' , ), 1610743809, (1610743809, (), [ 
			 (30, 0, None, None) , (3, 0, None, None) , (11, 0, None, None) , ], 1 , 1 , 4 , 0 , 40 , (11, 0, None, None) , 0 , )),
	(( 'ChangeCurrentSpcDescription' , 'libName' , 'numb' , ), 1610743810, (1610743810, (), [ (30, 0, None, None) , 
			 (3, 0, None, None) , ], 1 , 1 , 4 , 0 , 48 , (11, 0, None, None) , 0 , )),
	(( 'SpcDescriptionAdd' , 'libName' , 'numb' , ), 1610743811, (1610743811, (), [ (30, 0, None, None) , 
			 (3, 0, None, None) , ], 1 , 1 , 4 , 0 , 56 , (11, 0, None, None) , 0 , )),
	(( 'SpcDescriptionRemove' , 'libName' , 'numb' , ), 1610743812, (1610743812, (), [ (30, 0, None, None) , 
			 (3, 0, None, None) , ], 1 , 1 , 4 , 0 , 64 , (11, 0, None, None) , 0 , )),
	(( 'SpcDescriptionBeginEdit' , 'libName' , 'numb' , ), 1610743813, (1610743813, (), [ (30, 0, None, None) , 
			 (3, 0, None, None) , ], 1 , 1 , 4 , 0 , 72 , (11, 0, None, None) , 0 , )),
	(( 'SpcDescriptionEdit' , 'libName' , 'numb' , 'isOk' , ), 1610743814, (1610743814, (), [ 
			 (30, 0, None, None) , (3, 0, None, None) , (11, 0, None, None) , ], 1 , 1 , 4 , 0 , 80 , (11, 0, None, None) , 0 , )),
	(( 'SynchronizationBegin' , ), 1610743815, (1610743815, (), [ ], 1 , 1 , 4 , 0 , 88 , (11, 0, None, None) , 0 , )),
	(( 'Synchronization' , ), 1610743816, (1610743816, (), [ ], 1 , 1 , 4 , 0 , 96 , (11, 0, None, None) , 0 , )),
	(( 'BeginCalcPositions' , ), 1610743817, (1610743817, (), [ ], 1 , 1 , 4 , 0 , 104 , (11, 0, None, None) , 0 , )),
	(( 'CalcPositions' , ), 1610743818, (1610743818, (), [ ], 1 , 1 , 4 , 0 , 112 , (11, 0, None, None) , 0 , )),
	(( 'BeginCreateObject' , 'typeObj' , ), 1610743819, (1610743819, (), [ (3, 0, None, None) , ], 1 , 1 , 4 , 0 , 120 , (11, 0, None, None) , 0 , )),
]

IStampNotify_vtables_dispatch_ = 0
IStampNotify_vtables_ = [
	(( 'BeginEditStamp' , ), 1610743808, (1610743808, (), [ ], 1 , 1 , 4 , 0 , 32 , (11, 0, None, None) , 0 , )),
	(( 'EndEditStamp' , 'editResult' , ), 1610743809, (1610743809, (), [ (11, 0, None, None) , ], 1 , 1 , 4 , 0 , 40 , (11, 0, None, None) , 0 , )),
	(( 'StampCellDblClick' , 'number' , ), 1610743810, (1610743810, (), [ (3, 0, None, None) , ], 1 , 1 , 4 , 0 , 48 , (11, 0, None, None) , 0 , )),
	(( 'StampCellBeginEdit' , 'number' , ), 1610743811, (1610743811, (), [ (3, 0, None, None) , ], 1 , 1 , 4 , 0 , 56 , (11, 0, None, None) , 0 , )),
	(( 'StampBeginClearCells' , 'numbers' , ), 1610743812, (1610743812, (), [ (12, 0, None, None) , ], 1 , 1 , 4 , 0 , 64 , (11, 0, None, None) , 0 , )),
]

IViewsAndLayersManagerNotify_vtables_dispatch_ = 0
IViewsAndLayersManagerNotify_vtables_ = [
	(( 'BeginEdit' , ), 1610743808, (1610743808, (), [ ], 1 , 1 , 4 , 0 , 32 , (11, 0, None, None) , 0 , )),
	(( 'EndEdit' , 'isOk' , ), 1610743809, (1610743809, (), [ (11, 0, None, None) , ], 1 , 1 , 4 , 0 , 40 , (11, 0, None, None) , 0 , )),
]

RecordMap = {
}

CLSIDToClassMap = {
}
CLSIDToPackageMap = {}
win32com.client.CLSIDToClass.RegisterCLSIDsFromDict( CLSIDToClassMap )
VTablesToPackageMap = {}
VTablesToClassMap = {
	'{C89A8C15-2DE0-408B-8C89-B1CF4EAE1263}' : 'IKompasNotify',
	'{EBF88CAE-07D4-4FD3-8069-A0EF15F56672}' : 'IKompasObjectNotify',
	'{0C11E121-22C4-40FB-9559-BECB12269DCB}' : 'IDocumentFileNotify',
	'{704FBFC9-7EDD-42D0-BDB5-C242D06C18F9}' : 'IStampNotify',
	'{1F02922E-EAF8-4462-AAFB-47273782FD31}' : 'IObject2DNotify',
	'{B17BA3C2-9697-493B-BAA5-1712F349EE53}' : 'IObject2DNotifyResult',
	'{BAF64B25-B405-478D-8019-65102E45E2D5}' : 'ISelectionMngNotify',
	'{926B6F36-0BAB-44C3-8CB8-2F89DE9DDCED}' : 'ISpcObjectNotify',
	'{05586FAB-FB5C-4E15-B7C0-6639106A005D}' : 'ISpcDocumentNotify',
	'{46D9F0CA-C094-41C8-B851-F86CF565481E}' : 'ISpecificationNotify',
	'{3A1D1701-BA12-4D88-9C29-7C0FAF7A2800}' : 'IDocument2DNotify',
	'{9AB42E3B-7437-407E-960A-4F509812AB11}' : 'IPropertyManagerNotify',
	'{A715A2F6-3210-4890-9EB4-327A06F90EB6}' : 'IDocumentFrameNotify',
	'{341D4571-16F4-4928-903E-6906E56DACD1}' : 'IViewsAndLayersManagerNotify',
	'{30265782-7631-4957-AF51-458CAA9A76EC}' : 'ILibraryManagerNotify',
	'{225DDE9A-A442-4CD5-8428-87612BC0677A}' : 'IProcess2DNotify',
	'{ABBA6CE0-CB4C-4A32-98B4-B639352C75CC}' : 'IParametrizationParam',
	'{90570C5F-3837-40D8-B9E4-563C166A4FD0}' : 'ISnapInfo',
	'{7C790DE5-BD3E-4F34-BF7A-7FA7250A87C0}' : 'ISaveToPreviusParam',
	'{C78AE949-84F6-4291-83E5-6AEBF90D2E09}' : 'IMouseEnterLeaveParameters',
}


NamesToIIDMap = {
	'IKompasNotify' : '{C89A8C15-2DE0-408B-8C89-B1CF4EAE1263}',
	'IKompasObjectNotify' : '{EBF88CAE-07D4-4FD3-8069-A0EF15F56672}',
	'IDocumentFileNotify' : '{0C11E121-22C4-40FB-9559-BECB12269DCB}',
	'IStampNotify' : '{704FBFC9-7EDD-42D0-BDB5-C242D06C18F9}',
	'IObject2DNotify' : '{1F02922E-EAF8-4462-AAFB-47273782FD31}',
	'IObject2DNotifyResult' : '{B17BA3C2-9697-493B-BAA5-1712F349EE53}',
	'ISelectionMngNotify' : '{BAF64B25-B405-478D-8019-65102E45E2D5}',
	'ISpcObjectNotify' : '{926B6F36-0BAB-44C3-8CB8-2F89DE9DDCED}',
	'ISpcDocumentNotify' : '{05586FAB-FB5C-4E15-B7C0-6639106A005D}',
	'ISpecificationNotify' : '{46D9F0CA-C094-41C8-B851-F86CF565481E}',
	'IDocument2DNotify' : '{3A1D1701-BA12-4D88-9C29-7C0FAF7A2800}',
	'IPropertyManagerNotify' : '{9AB42E3B-7437-407E-960A-4F509812AB11}',
	'IDocumentFrameNotify' : '{A715A2F6-3210-4890-9EB4-327A06F90EB6}',
	'IViewsAndLayersManagerNotify' : '{341D4571-16F4-4928-903E-6906E56DACD1}',
	'ILibraryManagerNotify' : '{30265782-7631-4957-AF51-458CAA9A76EC}',
	'IProcess2DNotify' : '{225DDE9A-A442-4CD5-8428-87612BC0677A}',
	'IParametrizationParam' : '{ABBA6CE0-CB4C-4A32-98B4-B639352C75CC}',
	'ISnapInfo' : '{90570C5F-3837-40D8-B9E4-563C166A4FD0}',
	'ISaveToPreviusParam' : '{7C790DE5-BD3E-4F34-BF7A-7FA7250A87C0}',
	'IMouseEnterLeaveParameters' : '{C78AE949-84F6-4291-83E5-6AEBF90D2E09}',
}


