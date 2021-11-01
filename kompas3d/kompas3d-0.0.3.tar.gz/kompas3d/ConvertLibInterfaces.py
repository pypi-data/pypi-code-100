# -*- coding: mbcs -*-
# Created by makepy.py version 0.5.01
# By python version 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# From type library 'ConvertLibInterfaces.tlb'
# On Mon Nov  1 14:44:28 2021
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

CLSID = IID('{BC89C6E1-8016-429C-A093-300B3F18DB21}')
MajorVersion = 1
MinorVersion = 0
LibraryFlags = 8
LCID = 0x0

class constants:
	ksECRChangeSection            =4          # from enum ksExecuteCommandResult
	ksECRNeedRefreshTree          =1          # from enum ksExecuteCommandResult
	ksECRRepeatCommand            =2          # from enum ksExecuteCommandResult
	ksECRSuccess                  =0          # from enum ksExecuteCommandResult

from win32com.client import DispatchBaseClass
class IExternalElementsBase(DispatchBaseClass):
	'Внешняя база элементов.'
	CLSID = IID('{A4FBAA00-BAA1-4D26-AFF3-91B3FBC76F13}')
	coclass_clsid = None

	def DrawElement(self, HWnd=defaultNamedNotOptArg):
		'Отрисовать в окне просмотра выбранный элемент.'
		return self._oleobj_.InvokeTypes(13, LCID, 1, (11, 0), ((3, 1),),HWnd
			)

	def ExecuteCommand(self, CommandID=defaultNamedNotOptArg):
		'Выполнить комманду.'
		return self._oleobj_.InvokeTypes(11, LCID, 1, (3, 0), ((3, 1),),CommandID
			)

	def GetCommandState(self, CommandID=defaultNamedNotOptArg, Enable=pythoncom.Missing, Checked=pythoncom.Missing):
		'Получить состояние команд панели и меню.'
		return self._ApplyTypes_(10, 1, (11, 0), ((3, 1), (16395, 2), (16395, 2)), 'GetCommandState', None,CommandID
			, Enable, Checked)

	def GetLibPropertyObject(self):
		'Получить указатель на интерфейс параметров текущего элемента - ILibPropertyObject.'
		ret = self._oleobj_.InvokeTypes(7, LCID, 1, (13, 0), (),)
		if ret is not None:
			# See if this IUnknown is really an IDispatch
			try:
				ret = ret.QueryInterface(pythoncom.IID_IDispatch)
			except pythoncom.error:
				return ret
			ret = Dispatch(ret, 'GetLibPropertyObject', None)
		return ret

	def GetMenuId(self):
		'Получить идентификатор меню для текущего листа дерева.'
		return self._oleobj_.InvokeTypes(12, LCID, 1, (3, 0), (),)

	def OnSelectNode(self, NodeId=defaultNamedNotOptArg):
		'Событие установки текущего листа дерева.'
		return self._oleobj_.InvokeTypes(6, LCID, 1, (11, 0), ((8, 1),),NodeId
			)

	# The method TreeImageList is actually a property, but must be used as a method to correctly pass the arguments
	def TreeImageList(self, Size=defaultNamedNotOptArg):
		'Получить линейку иконок для дерева.'
		return self._ApplyTypes_(8, 2, (12, 0), ((3, 1),), 'TreeImageList', None,Size
			)

	_prop_map_get_ = {
		"CurrentNode": (5, 2, (8, 0), (), "CurrentNode", None),
		"CurrentSection": (3, 2, (8, 0), (), "CurrentSection", None),
		"ElementsTree": (4, 2, (8, 0), (), "ElementsTree", None),
		"Note": (14, 2, (8, 0), (), "Note", None),
		"Sections": (2, 2, (12, 0), (), "Sections", None),
		"ToolBarId": (9, 2, (3, 0), (), "ToolBarId", None),
		"Version": (1, 2, (3, 0), (), "Version", None),
	}
	_prop_map_put_ = {
		"CurrentSection": ((3, LCID, 4, 0),()),
	}
	def __iter__(self):
		"Return a Python iterator for this object"
		try:
			ob = self._oleobj_.InvokeTypes(-4,LCID,3,(13, 10),())
		except pythoncom.error:
			raise TypeError("This object does not support enumeration")
		return win32com.client.util.Iterator(ob, None)

class IKompasConverter(DispatchBaseClass):
	CLSID = IID('{735140E9-F6B5-42E9-9008-71730C617067}')
	coclass_clsid = None

	def Convert(self, inputFile=defaultNamedNotOptArg, outfile=defaultNamedNotOptArg, command=defaultNamedNotOptArg, showParam=defaultNamedNotOptArg):
		'Запустить процесс конвертации'
		return self._oleobj_.InvokeTypes(4, LCID, 1, (3, 0), ((8, 1), (8, 1), (3, 1), (11, 1)),inputFile
			, outfile, command, showParam)

	def ConverterParameters(self, command=defaultNamedNotOptArg):
		'Параметры конвертора'
		ret = self._oleobj_.InvokeTypes(1, LCID, 1, (13, 0), ((3, 1),),command
			)
		if ret is not None:
			# See if this IUnknown is really an IDispatch
			try:
				ret = ret.QueryInterface(pythoncom.IID_IDispatch)
			except pythoncom.error:
				return ret
			ret = Dispatch(ret, 'ConverterParameters', None)
		return ret

	def GetFilter(self, docType=defaultNamedNotOptArg, saveAs=defaultNamedNotOptArg, command=pythoncom.Missing):
		"Получить фильтр и номер команды по типу документа 'КОМПАС-Фрагменты (*.frw)|*.frw|'"
		return self._ApplyTypes_(3, 1, (8, 0), ((3, 1), (11, 1), (16387, 2)), 'GetFilter', None,docType
			, saveAs, command)

	def VisualEditConvertParam(self, parentHwnd=defaultNamedNotOptArg, command=defaultNamedNotOptArg):
		'Запустить визуальное редактирование параметров конвертации'
		return self._oleobj_.InvokeTypes(5, LCID, 1, (11, 0), ((3, 1), (3, 1)),parentHwnd
			, command)

	_prop_map_get_ = {
		"CanUnloadLibrary": (2, 2, (11, 0), (), "CanUnloadLibrary", None),
	}
	_prop_map_put_ = {
	}
	def __iter__(self):
		"Return a Python iterator for this object"
		try:
			ob = self._oleobj_.InvokeTypes(-4,LCID,3,(13, 10),())
		except pythoncom.error:
			raise TypeError("This object does not support enumeration")
		return win32com.client.util.Iterator(ob, None)

IExternalElementsBase_vtables_dispatch_ = 1
IExternalElementsBase_vtables_ = [
	(( 'Version' , 'Result' , ), 1, (1, (), [ (16387, 10, None, None) , ], 1 , 2 , 4 , 0 , 56 , (3, 0, None, None) , 0 , )),
	(( 'Sections' , 'Result' , ), 2, (2, (), [ (16396, 10, None, None) , ], 1 , 2 , 4 , 0 , 64 , (3, 0, None, None) , 0 , )),
	(( 'CurrentSection' , 'Result' , ), 3, (3, (), [ (16392, 10, None, None) , ], 1 , 2 , 4 , 0 , 72 , (3, 0, None, None) , 0 , )),
	(( 'CurrentSection' , 'Result' , ), 3, (3, (), [ (8, 1, None, None) , ], 1 , 4 , 4 , 0 , 80 , (3, 0, None, None) , 0 , )),
	(( 'ElementsTree' , 'Result' , ), 4, (4, (), [ (16392, 10, None, None) , ], 1 , 2 , 4 , 0 , 88 , (3, 0, None, None) , 0 , )),
	(( 'CurrentNode' , 'NodeId' , ), 5, (5, (), [ (16392, 10, None, None) , ], 1 , 2 , 4 , 0 , 96 , (3, 0, None, None) , 0 , )),
	(( 'OnSelectNode' , 'NodeId' , 'Result' , ), 6, (6, (), [ (8, 1, None, None) , 
			 (16395, 10, None, None) , ], 1 , 1 , 4 , 0 , 104 , (3, 0, None, None) , 0 , )),
	(( 'GetLibPropertyObject' , 'Result' , ), 7, (7, (), [ (16397, 10, None, None) , ], 1 , 1 , 4 , 0 , 112 , (3, 0, None, None) , 0 , )),
	(( 'TreeImageList' , 'Size' , 'Result' , ), 8, (8, (), [ (3, 1, None, None) , 
			 (16396, 10, None, None) , ], 1 , 2 , 4 , 0 , 120 , (3, 0, None, None) , 0 , )),
	(( 'ToolBarId' , 'Result' , ), 9, (9, (), [ (16387, 10, None, None) , ], 1 , 2 , 4 , 0 , 128 , (3, 0, None, None) , 0 , )),
	(( 'GetCommandState' , 'CommandID' , 'Enable' , 'Checked' , 'Result' , 
			 ), 10, (10, (), [ (3, 1, None, None) , (16395, 2, None, None) , (16395, 2, None, None) , (16395, 10, None, None) , ], 1 , 1 , 4 , 0 , 136 , (3, 0, None, None) , 0 , )),
	(( 'ExecuteCommand' , 'CommandID' , 'Result' , ), 11, (11, (), [ (3, 1, None, None) , 
			 (16387, 10, None, None) , ], 1 , 1 , 4 , 0 , 144 , (3, 0, None, None) , 0 , )),
	(( 'GetMenuId' , 'Result' , ), 12, (12, (), [ (16387, 10, None, None) , ], 1 , 1 , 4 , 0 , 152 , (3, 0, None, None) , 0 , )),
	(( 'DrawElement' , 'HWnd' , 'Result' , ), 13, (13, (), [ (3, 1, None, None) , 
			 (16395, 10, None, None) , ], 1 , 1 , 4 , 0 , 160 , (3, 0, None, None) , 0 , )),
	(( 'Note' , 'Result' , ), 14, (14, (), [ (16392, 10, None, None) , ], 1 , 2 , 4 , 0 , 168 , (3, 0, None, None) , 0 , )),
]

IKompasConverter_vtables_dispatch_ = 1
IKompasConverter_vtables_ = [
	(( 'ConverterParameters' , 'command' , 'iParam' , ), 1, (1, (), [ (3, 1, None, None) , 
			 (16397, 10, None, None) , ], 1 , 1 , 4 , 0 , 56 , (3, 0, None, None) , 0 , )),
	(( 'CanUnloadLibrary' , 'val' , ), 2, (2, (), [ (16395, 10, None, None) , ], 1 , 2 , 4 , 0 , 64 , (3, 0, None, None) , 0 , )),
	(( 'GetFilter' , 'docType' , 'saveAs' , 'command' , 'Result' , 
			 ), 3, (3, (), [ (3, 1, None, None) , (11, 1, None, None) , (16387, 2, None, None) , (16392, 10, None, None) , ], 1 , 1 , 4 , 0 , 72 , (3, 0, None, None) , 0 , )),
	(( 'Convert' , 'inputFile' , 'outfile' , 'command' , 'showParam' , 
			 'Result' , ), 4, (4, (), [ (8, 1, None, None) , (8, 1, None, None) , (3, 1, None, None) , 
			 (11, 1, None, None) , (16387, 10, None, None) , ], 1 , 1 , 4 , 0 , 80 , (3, 0, None, None) , 0 , )),
	(( 'VisualEditConvertParam' , 'parentHwnd' , 'command' , 'val' , ), 5, (5, (), [ 
			 (3, 1, None, None) , (3, 1, None, None) , (16395, 10, None, None) , ], 1 , 1 , 4 , 0 , 88 , (3, 0, None, None) , 0 , )),
]

RecordMap = {
}

CLSIDToClassMap = {
	'{735140E9-F6B5-42E9-9008-71730C617067}' : IKompasConverter,
	'{A4FBAA00-BAA1-4D26-AFF3-91B3FBC76F13}' : IExternalElementsBase,
}
CLSIDToPackageMap = {}
win32com.client.CLSIDToClass.RegisterCLSIDsFromDict( CLSIDToClassMap )
VTablesToPackageMap = {}
VTablesToClassMap = {
	'{735140E9-F6B5-42E9-9008-71730C617067}' : 'IKompasConverter',
	'{A4FBAA00-BAA1-4D26-AFF3-91B3FBC76F13}' : 'IExternalElementsBase',
}


NamesToIIDMap = {
	'IKompasConverter' : '{735140E9-F6B5-42E9-9008-71730C617067}',
	'IExternalElementsBase' : '{A4FBAA00-BAA1-4D26-AFF3-91B3FBC76F13}',
}

win32com.client.constants.__dicts__.append(constants.__dict__)

