# -*- coding: mbcs -*-
# Created by makepy.py version 0.5.01
# By python version 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# From type library 'TxtTable.tlb'
# On Mon Nov  1 14:51:36 2021
'TxtTable 1.0 Type Library'
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

CLSID = IID('{5729C561-E8A7-48F6-AFB5-B824C7CFB75F}')
MajorVersion = 1
MinorVersion = 0
LibraryFlags = 8
LCID = 0x0

from win32com.client import DispatchBaseClass
class IBendTableFile(DispatchBaseClass):
	'IBendTableFile - интерфейс таблицы гиба, хранимой в файле'
	CLSID = IID('{751CA9B5-5E04-4FF5-A5A4-341C0603A61C}')
	coclass_clsid = IID('{7F676D97-50B6-4D42-87BA-1510B1DF3E19}')

	def BeginSave(self):
		'открыть файл'
		return self._oleobj_.InvokeTypes(3, LCID, 1, (24, 0), (),)

	def EndSave(self):
		'открыть файл'
		return self._oleobj_.InvokeTypes(5, LCID, 1, (24, 0), (),)

	def GetDefFileExtension(self):
		'расширение по умолчанию'
		# Result is a Unicode object
		return self._oleobj_.InvokeTypes(6, LCID, 1, (8, 0), (),)

	def Save(self):
		'сохранить в файл'
		return self._oleobj_.InvokeTypes(4, LCID, 1, (24, 0), (),)

	def SaveAs(self, FileName=defaultNamedNotOptArg):
		'открыть файл'
		return self._oleobj_.InvokeTypes(2, LCID, 1, (24, 0), ((8, 1),),FileName
			)

	_prop_map_get_ = {
		"FileName": (1, 2, (8, 0), (), "FileName", None),
	}
	_prop_map_put_ = {
		"FileName": ((1, LCID, 4, 0),()),
	}
	def __iter__(self):
		"Return a Python iterator for this object"
		try:
			ob = self._oleobj_.InvokeTypes(-4,LCID,3,(13, 10),())
		except pythoncom.error:
			raise TypeError("This object does not support enumeration")
		return win32com.client.util.Iterator(ob, None)

class IGeneralBendTable(DispatchBaseClass):
	'IGeneralBendTable - общий интерфейс данных, запрашиваемых у таблицы гиба'
	CLSID = IID('{DF5795A0-0787-4063-BB17-500587C870F8}')
	coclass_clsid = IID('{7F676D97-50B6-4D42-87BA-1510B1DF3E19}')

	def DoInterpolate(self):
		return self._oleobj_.InvokeTypes(1610743813, LCID, 1, (11, 0), (),)

	def GetParams(self, rad=defaultNamedNotOptArg, angle=defaultNamedNotOptArg, pVal=pythoncom.Missing):
		'выдать значение для угла и радиуса'
		return self._ApplyTypes_(3, 1, (11, 0), ((5, 1), (5, 1), (16389, 2)), 'GetParams', None,rad
			, angle, pVal)

	def SetThickness(self, Thickness=defaultNamedNotOptArg):
		'толщина листа'
		return self._oleobj_.InvokeTypes(4, LCID, 1, (11, 0), ((5, 1),),Thickness
			)

	_prop_map_get_ = {
		"Thickness": (1, 2, (5, 0), (), "Thickness", None),
		"UnfoldType": (2, 2, (2, 0), (), "UnfoldType", None),
	}
	_prop_map_put_ = {
		"UnfoldType": ((2, LCID, 4, 0),()),
	}
	def __iter__(self):
		"Return a Python iterator for this object"
		try:
			ob = self._oleobj_.InvokeTypes(-4,LCID,3,(13, 10),())
		except pythoncom.error:
			raise TypeError("This object does not support enumeration")
		return win32com.client.util.Iterator(ob, None)

from win32com.client import CoClassBaseClass
# This CoClass is known by the name 'KOMPAS.ShMtTxtTable.1'
class ShMtTxtTable(CoClassBaseClass): # A CoClass
	# Текстовые таблицы гибов
	CLSID = IID('{7F676D97-50B6-4D42-87BA-1510B1DF3E19}')
	coclass_sources = [
	]
	coclass_interfaces = [
		IGeneralBendTable,
		IBendTableFile,
	]
	default_interface = IGeneralBendTable

IBendTableFile_vtables_dispatch_ = 1
IBendTableFile_vtables_ = [
	(( 'FileName' , 'FileName' , ), 1, (1, (), [ (16392, 10, None, None) , ], 1 , 2 , 4 , 0 , 56 , (3, 0, None, None) , 0 , )),
	(( 'FileName' , 'FileName' , ), 1, (1, (), [ (8, 1, None, None) , ], 1 , 4 , 4 , 0 , 64 , (3, 0, None, None) , 0 , )),
	(( 'SaveAs' , 'FileName' , ), 2, (2, (), [ (8, 1, None, None) , ], 1 , 1 , 4 , 0 , 72 , (3, 0, None, None) , 0 , )),
	(( 'BeginSave' , ), 3, (3, (), [ ], 1 , 1 , 4 , 0 , 80 , (3, 0, None, None) , 0 , )),
	(( 'Save' , ), 4, (4, (), [ ], 1 , 1 , 4 , 0 , 88 , (3, 0, None, None) , 0 , )),
	(( 'EndSave' , ), 5, (5, (), [ ], 1 , 1 , 4 , 0 , 96 , (3, 0, None, None) , 0 , )),
	(( 'GetDefFileExtension' , 'defExt' , ), 6, (6, (), [ (16392, 10, None, None) , ], 1 , 1 , 4 , 0 , 104 , (3, 0, None, None) , 0 , )),
]

IGeneralBendTable_vtables_dispatch_ = 1
IGeneralBendTable_vtables_ = [
	(( 'Thickness' , 'Thickness' , ), 1, (1, (), [ (16389, 10, None, None) , ], 1 , 2 , 4 , 0 , 56 , (3, 0, None, None) , 0 , )),
	(( 'UnfoldType' , 'pVal' , ), 2, (2, (), [ (16386, 10, None, None) , ], 1 , 2 , 4 , 0 , 64 , (3, 0, None, None) , 0 , )),
	(( 'UnfoldType' , 'pVal' , ), 2, (2, (), [ (2, 1, None, None) , ], 1 , 4 , 4 , 0 , 72 , (3, 0, None, None) , 0 , )),
	(( 'GetParams' , 'rad' , 'angle' , 'pVal' , 'pOk' , 
			 ), 3, (3, (), [ (5, 1, None, None) , (5, 1, None, None) , (16389, 2, None, None) , (16395, 10, None, None) , ], 1 , 1 , 4 , 0 , 80 , (3, 0, None, None) , 0 , )),
	(( 'SetThickness' , 'Thickness' , 'pOk' , ), 4, (4, (), [ (5, 1, None, None) , 
			 (16395, 10, None, None) , ], 1 , 1 , 4 , 0 , 88 , (3, 0, None, None) , 0 , )),
	(( 'DoInterpolate' , 'pOk' , ), 1610743813, (1610743813, (), [ (16395, 10, None, None) , ], 1 , 1 , 4 , 0 , 96 , (3, 0, None, None) , 0 , )),
]

RecordMap = {
}

CLSIDToClassMap = {
	'{DF5795A0-0787-4063-BB17-500587C870F8}' : IGeneralBendTable,
	'{751CA9B5-5E04-4FF5-A5A4-341C0603A61C}' : IBendTableFile,
	'{7F676D97-50B6-4D42-87BA-1510B1DF3E19}' : ShMtTxtTable,
}
CLSIDToPackageMap = {}
win32com.client.CLSIDToClass.RegisterCLSIDsFromDict( CLSIDToClassMap )
VTablesToPackageMap = {}
VTablesToClassMap = {
	'{DF5795A0-0787-4063-BB17-500587C870F8}' : 'IGeneralBendTable',
	'{751CA9B5-5E04-4FF5-A5A4-341C0603A61C}' : 'IBendTableFile',
}


NamesToIIDMap = {
	'IGeneralBendTable' : '{DF5795A0-0787-4063-BB17-500587C870F8}',
	'IBendTableFile' : '{751CA9B5-5E04-4FF5-A5A4-341C0603A61C}',
}


