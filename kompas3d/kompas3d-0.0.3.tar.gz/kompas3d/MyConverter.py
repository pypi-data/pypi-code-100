# -*- coding: mbcs -*-
# Created by makepy.py version 0.5.01
# By python version 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# From type library 'MyConverter.tlb'
# On Mon Nov  1 14:50:34 2021
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

CLSID = IID('{ADEFA6C7-CF88-4A79-AAC9-69C37740FFC8}')
MajorVersion = 1
MinorVersion = 0
LibraryFlags = 8
LCID = 0x0

class constants:
	libConv_Exp_a3d               =2          # from enum LibConvEnum
	libConv_Exp_cdw               =4          # from enum LibConvEnum
	libConv_Exp_frw               =3          # from enum LibConvEnum
	libConv_Exp_kdw               =6          # from enum LibConvEnum
	libConv_Exp_m3d               =1          # from enum LibConvEnum
	libConv_Exp_spw               =5          # from enum LibConvEnum
	libConv_Imp_a3d               =8          # from enum LibConvEnum
	libConv_Imp_cdw               =10         # from enum LibConvEnum
	libConv_Imp_frw               =9          # from enum LibConvEnum
	libConv_Imp_kdw               =12         # from enum LibConvEnum
	libConv_Imp_m3d               =7          # from enum LibConvEnum
	libConv_Imp_spw               =11         # from enum LibConvEnum

from win32com.client import DispatchBaseClass
class ILibConverterParam(DispatchBaseClass):
	'Параметры конвертора'
	CLSID = IID('{35ED8E66-7F20-4D27-A888-0819152350B5}')
	coclass_clsid = None

	_prop_map_get_ = {
		"SaveLineStyle": (1, 2, (11, 0), (), "SaveLineStyle", None),
	}
	_prop_map_put_ = {
		"SaveLineStyle": ((1, LCID, 4, 0),()),
	}
	def __iter__(self):
		"Return a Python iterator for this object"
		try:
			ob = self._oleobj_.InvokeTypes(-4,LCID,3,(13, 10),())
		except pythoncom.error:
			raise TypeError("This object does not support enumeration")
		return win32com.client.util.Iterator(ob, None)

ILibConverterParam_vtables_dispatch_ = 1
ILibConverterParam_vtables_ = [
	(( 'SaveLineStyle' , 'PVal' , ), 1, (1, (), [ (16395, 10, None, None) , ], 1 , 2 , 4 , 0 , 56 , (3, 0, None, None) , 0 , )),
	(( 'SaveLineStyle' , 'PVal' , ), 1, (1, (), [ (11, 49, 'True', None) , ], 1 , 4 , 4 , 0 , 64 , (3, 0, None, None) , 0 , )),
]

RecordMap = {
}

CLSIDToClassMap = {
	'{35ED8E66-7F20-4D27-A888-0819152350B5}' : ILibConverterParam,
}
CLSIDToPackageMap = {}
win32com.client.CLSIDToClass.RegisterCLSIDsFromDict( CLSIDToClassMap )
VTablesToPackageMap = {}
VTablesToClassMap = {
	'{35ED8E66-7F20-4D27-A888-0819152350B5}' : 'ILibConverterParam',
}


NamesToIIDMap = {
	'ILibConverterParam' : '{35ED8E66-7F20-4D27-A888-0819152350B5}',
}

win32com.client.constants.__dicts__.append(constants.__dict__)

