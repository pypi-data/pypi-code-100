# -*- coding: mbcs -*-
# Created by makepy.py version 0.5.01
# By python version 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# From type library 'IFCConverter.tlb'
# On Fri Nov  5 08:12:38 2021
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

CLSID = IID('{31EBF650-BD38-43EC-892B-1F8AC6C14431}')
MajorVersion = 1
MinorVersion = 0
LibraryFlags = 8
LCID = 0x0

from win32com.client import DispatchBaseClass
class IIFCConverterParam(DispatchBaseClass):
	'Параметры конвертера'
	CLSID = IID('{1BF78A7C-E274-4B61-8771-EBD0542E8F05}')
	coclass_clsid = None

	_prop_map_get_ = {
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

IIFCConverterParam_vtables_dispatch_ = 1
IIFCConverterParam_vtables_ = [
]

RecordMap = {
}

CLSIDToClassMap = {
	'{1BF78A7C-E274-4B61-8771-EBD0542E8F05}' : IIFCConverterParam,
}
CLSIDToPackageMap = {}
win32com.client.CLSIDToClass.RegisterCLSIDsFromDict( CLSIDToClassMap )
VTablesToPackageMap = {}
VTablesToClassMap = {
	'{1BF78A7C-E274-4B61-8771-EBD0542E8F05}' : 'IIFCConverterParam',
}


NamesToIIDMap = {
	'IIFCConverterParam' : '{1BF78A7C-E274-4B61-8771-EBD0542E8F05}',
}


