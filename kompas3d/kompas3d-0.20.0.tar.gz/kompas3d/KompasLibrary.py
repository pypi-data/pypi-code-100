# -*- coding: mbcs -*-
# Created by makepy.py version 0.5.01
# By python version 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# From type library 'KompasLibrary.tlb'
# On Fri Nov  5 08:14:41 2021
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

CLSID = IID('{C1633829-7BB0-4E69-8ED4-043ADB7E8090}')
MajorVersion = 1
MinorVersion = 0
LibraryFlags = 8
LCID = 0x0

class constants:
	ksLFBeginUnloadLibrary        =17010      # from enum ksKompasLibraryFunctionEnum
	ksLFContextPanelStyleComboChanged=17015      # from enum ksKompasLibraryFunctionEnum
	ksLFCreateMacroFromSample     =17017      # from enum ksKompasLibraryFunctionEnum
	ksLFDisplayLibraryName        =17004      # from enum ksKompasLibraryFunctionEnum
	ksLFFillContextPanel          =17014      # from enum ksKompasLibraryFunctionEnum
	ksLFFillLibraryMenu           =17011      # from enum ksKompasLibraryFunctionEnum
	ksLFGetDisableReason          =17013      # from enum ksKompasLibraryFunctionEnum
	ksLFGetKompasConverter        =17016      # from enum ksKompasLibraryFunctionEnum
	ksLFGetLibraryCommandState    =17012      # from enum ksKompasLibraryFunctionEnum
	ksLFInitLibrary               =17009      # from enum ksKompasLibraryFunctionEnum
	ksLFIsFunctionEnable          =17002      # from enum ksKompasLibraryFunctionEnum
	ksLFIsOnApplication7          =17008      # from enum ksKompasLibraryFunctionEnum
	ksLFLibraryHelpFile           =17005      # from enum ksKompasLibraryFunctionEnum
	ksLFLibraryName               =17003      # from enum ksKompasLibraryFunctionEnum
	ksLFProtectNumber             =17006      # from enum ksKompasLibraryFunctionEnum
	ksLFRunLibraryCommand         =17007      # from enum ksKompasLibraryFunctionEnum
	ksLFVersion                   =17001      # from enum ksKompasLibraryFunctionEnum

from win32com.client import DispatchBaseClass
class IKompasLibrary(DispatchBaseClass):
	'Интерфейс приложения Компас 3D.'
	CLSID = IID('{025A21B0-0192-4A7C-A3F0-CA54AAA4FADB}')
	coclass_clsid = None

	def BeginUnloadLibrary(self):
		'Завершающие действия перед отключением библиотеки, отписка от событий.'
		return self._oleobj_.InvokeTypes(17010, LCID, 1, (11, 0), (),)

	def ContextPanelStyleComboChanged(self, StyleComboID=defaultNamedNotOptArg, styleType=defaultNamedNotOptArg, newValue=defaultNamedNotOptArg):
		'Изменение значения в стилевом комбобоксе контекстной панели.'
		return self._oleobj_.InvokeTypes(17015, LCID, 1, (11, 0), ((8, 1), (3, 1), (3, 1)),StyleComboID
			, styleType, newValue)

	def CreateMacroFromSample(self, MacroReference=defaultNamedNotOptArg):
		'Создать объект по образцу.'
		return self._oleobj_.InvokeTypes(17017, LCID, 1, (11, 0), ((3, 1),),MacroReference
			)

	def FillContextPanel(self, ContextPanel=defaultNamedNotOptArg):
		'Накачка всплывающей панели для библиотечных элементов.'
		return self._oleobj_.InvokeTypes(17014, LCID, 1, (11, 0), ((9, 1),),ContextPanel
			)

	def FillLibraryMenu(self, Menu=defaultNamedNotOptArg):
		'Динамическая накачка меню.'
		return self._oleobj_.InvokeTypes(17011, LCID, 1, (11, 0), ((9, 1),),Menu
			)

	def GetDisableReason(self, Command=defaultNamedNotOptArg):
		'Получить описание причины недоступности команды.'
		# Result is a Unicode object
		return self._oleobj_.InvokeTypes(17013, LCID, 1, (8, 0), ((3, 1),),Command
			)

	def GetKompasConverter(self):
		'Получить интерфейс конвертора.'
		ret = self._oleobj_.InvokeTypes(17016, LCID, 1, (9, 0), (),)
		if ret is not None:
			ret = Dispatch(ret, 'GetKompasConverter', None)
		return ret

	def GetLibraryCommandState(self, Command=defaultNamedNotOptArg, Enable=pythoncom.Missing, Checked=pythoncom.Missing):
		'Получить текущее состояние команды.'
		return self._ApplyTypes_(17012, 1, (11, 0), ((3, 1), (16395, 2), (16387, 2)), 'GetLibraryCommandState', None,Command
			, Enable, Checked)

	def InitLibrary(self, ApplicationInterface=defaultNamedNotOptArg):
		'Инициализация библиотеки, подписка на события.'
		return self._oleobj_.InvokeTypes(17009, LCID, 1, (11, 0), ((9, 1),),ApplicationInterface
			)

	# The method IsFunctionEnable is actually a property, but must be used as a method to correctly pass the arguments
	def IsFunctionEnable(self, FunctionID=defaultNamedNotOptArg):
		'Признак поддержки библиотекой функций.'
		return self._oleobj_.InvokeTypes(17002, LCID, 2, (11, 0), ((3, 1),),FunctionID
			)

	def RunLibraryCommand(self, Command=defaultNamedNotOptArg, DemoMode=defaultNamedNotOptArg):
		'Выполнить команду библиотеки.'
		return self._oleobj_.InvokeTypes(17007, LCID, 1, (3, 0), ((3, 1), (3, 1)),Command
			, DemoMode)

	_prop_map_get_ = {
		"DisplayLibraryName": (17004, 2, (8, 0), (), "DisplayLibraryName", None),
		"IsOnApplication7": (17008, 2, (11, 0), (), "IsOnApplication7", None),
		"LibraryHelpFile": (17005, 2, (8, 0), (), "LibraryHelpFile", None),
		"LibraryName": (17003, 2, (8, 0), (), "LibraryName", None),
		"ProtectNumber": (17006, 2, (3, 0), (), "ProtectNumber", None),
		"Version": (17001, 2, (3, 0), (), "Version", None),
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

class IKompasLibraryMenu(DispatchBaseClass):
	'Меню библиотеки.'
	CLSID = IID('{C35D07D7-0248-40C5-A335-1D4FF1610F0A}')
	coclass_clsid = None

	def AddMenuCommand(self, Id=defaultNamedNotOptArg, Title=defaultNamedNotOptArg):
		'Добавить пункт меню.'
		return self._oleobj_.InvokeTypes(18001, LCID, 1, (11, 0), ((3, 1), (8, 1)),Id
			, Title)

	def AddSeparator(self):
		'Добавить разделитель.'
		return self._oleobj_.InvokeTypes(18002, LCID, 1, (11, 0), (),)

	def AddSubMenu(self, Title=defaultNamedNotOptArg):
		'Добавить подменю.'
		return self._oleobj_.InvokeTypes(18003, LCID, 1, (11, 0), ((8, 1),),Title
			)

	def EndSubMenu(self):
		'Добавить подменю.'
		return self._oleobj_.InvokeTypes(18004, LCID, 1, (11, 0), (),)

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

class ksKompasLibrary(DispatchBaseClass):
	'Интерфейс приложения КОМПАС 3D.'
	CLSID = IID('{C222614E-AB59-4FEE-9F4A-1EAB7C1D4C5E}')
	coclass_clsid = None

	def ContextPanelStyleComboChanged(self, StyleComboID=defaultNamedNotOptArg, styleType=defaultNamedNotOptArg, newValue=defaultNamedNotOptArg):
		'Изменение значения в стилевом комбобоксе контекстной панели.'
		return self._oleobj_.InvokeTypes(16015, LCID, 1, (11, 0), ((8, 1), (3, 1), (3, 1)),StyleComboID
			, styleType, newValue)

	def CreateMacroFromSample(self, MacroReference=defaultNamedNotOptArg):
		'Создать объект по оброзцу.'
		return self._oleobj_.InvokeTypes(16016, LCID, 1, (11, 0), ((3, 1),),MacroReference
			)

	def DisplayLibraryName(self):
		'Отображаемое имя приложения.'
		# Result is a Unicode object
		return self._oleobj_.InvokeTypes(16002, LCID, 1, (8, 0), (),)

	def ExternalGetMenu(self):
		'Получить меню библиотеки.'
		return self._oleobj_.InvokeTypes(16009, LCID, 1, (3, 0), (),)

	def ExternalMenuItem(self, Index=defaultNamedNotOptArg, ItemType=pythoncom.Missing, Command=pythoncom.Missing):
		'Динамическая накачка меню.'
		return self._ApplyTypes_(16010, 1, (8, 0), ((2, 1), (16386, 2), (16386, 2)), 'ExternalMenuItem', None,Index
			, ItemType, Command)

	def ExternalRunCommand(self, Command=defaultNamedNotOptArg, mode=defaultNamedNotOptArg, ApplicationInterface=defaultNamedNotOptArg):
		'Выполнить команду библиотеки.'
		return self._oleobj_.InvokeTypes(16005, LCID, 1, (24, 0), ((2, 1), (2, 1), (9, 0)),Command
			, mode, ApplicationInterface)

	def FillContextPanel(self, ContextPanel=defaultNamedNotOptArg):
		'Накачка всплывающей панели для библиотечных элементов.'
		return self._oleobj_.InvokeTypes(16014, LCID, 1, (11, 0), ((9, 1),),ContextPanel
			)

	def GetDisableReason(self, Command=defaultNamedNotOptArg):
		'Получить описание причины недоступности команды.'
		# Result is a Unicode object
		return self._oleobj_.InvokeTypes(16013, LCID, 1, (8, 0), ((3, 1),),Command
			)

	def GetHelpFile(self):
		'Файл справки.'
		# Result is a Unicode object
		return self._oleobj_.InvokeTypes(16003, LCID, 1, (8, 0), (),)

	def GetIKompasConverter(self):
		'Получить интерфейс конвертора.'
		ret = self._oleobj_.InvokeTypes(16011, LCID, 1, (9, 0), (),)
		if ret is not None:
			ret = Dispatch(ret, 'GetIKompasConverter', None)
		return ret

	def GetLibraryName(self):
		'Имя приложения.'
		# Result is a Unicode object
		return self._oleobj_.InvokeTypes(16001, LCID, 1, (8, 0), (),)

	def GetProtectNumber(self):
		'Номер ключа защиты.'
		return self._oleobj_.InvokeTypes(16004, LCID, 1, (2, 0), (),)

	def IsOnApplication7(self):
		'Получить тип версии API используемого библиотекой.'
		return self._oleobj_.InvokeTypes(16006, LCID, 1, (11, 0), (),)

	def LibInterfaceNotifyDisconnect(self):
		'Завершающие действия перед отключением библиотеки, отписка от событий.'
		return self._oleobj_.InvokeTypes(16008, LCID, 1, (11, 0), (),)

	def LibInterfaceNotifyEntry(self, ApplicationInterface=defaultNamedNotOptArg):
		'Инициализация библиотеки, подписка на события.'
		return self._oleobj_.InvokeTypes(16007, LCID, 1, (11, 0), ((9, 1),),ApplicationInterface
			)

	def LibraryCommandState(self, Command=defaultNamedNotOptArg, Enable=pythoncom.Missing, Checked=pythoncom.Missing):
		'Получить текущее состояние команды.'
		return self._ApplyTypes_(16012, 1, (11, 0), ((3, 1), (16395, 2), (16387, 2)), 'LibraryCommandState', None,Command
			, Enable, Checked)

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

IKompasLibrary_vtables_dispatch_ = 1
IKompasLibrary_vtables_ = [
	(( 'Version' , 'Result' , ), 17001, (17001, (), [ (16387, 10, None, None) , ], 1 , 2 , 4 , 0 , 56 , (3, 0, None, None) , 0 , )),
	(( 'IsFunctionEnable' , 'FunctionID' , 'Result' , ), 17002, (17002, (), [ (3, 1, None, None) , 
			 (16395, 10, None, None) , ], 1 , 2 , 4 , 0 , 64 , (3, 0, None, None) , 0 , )),
	(( 'LibraryName' , 'Result' , ), 17003, (17003, (), [ (16392, 10, None, None) , ], 1 , 2 , 4 , 0 , 72 , (3, 0, None, None) , 0 , )),
	(( 'DisplayLibraryName' , 'Result' , ), 17004, (17004, (), [ (16392, 10, None, None) , ], 1 , 2 , 4 , 0 , 80 , (3, 0, None, None) , 0 , )),
	(( 'LibraryHelpFile' , 'Result' , ), 17005, (17005, (), [ (16392, 10, None, None) , ], 1 , 2 , 4 , 0 , 88 , (3, 0, None, None) , 0 , )),
	(( 'ProtectNumber' , 'Result' , ), 17006, (17006, (), [ (16387, 10, None, None) , ], 1 , 2 , 4 , 0 , 96 , (3, 0, None, None) , 0 , )),
	(( 'RunLibraryCommand' , 'Command' , 'DemoMode' , 'Result' , ), 17007, (17007, (), [ 
			 (3, 1, None, None) , (3, 1, None, None) , (16387, 10, None, None) , ], 1 , 1 , 4 , 0 , 104 , (3, 0, None, None) , 0 , )),
	(( 'IsOnApplication7' , 'Result' , ), 17008, (17008, (), [ (16395, 10, None, None) , ], 1 , 2 , 4 , 0 , 112 , (3, 0, None, None) , 0 , )),
	(( 'InitLibrary' , 'ApplicationInterface' , 'Result' , ), 17009, (17009, (), [ (9, 1, None, None) , 
			 (16395, 10, None, None) , ], 1 , 1 , 4 , 0 , 120 , (3, 0, None, None) , 0 , )),
	(( 'BeginUnloadLibrary' , 'Result' , ), 17010, (17010, (), [ (16395, 10, None, None) , ], 1 , 1 , 4 , 0 , 128 , (3, 0, None, None) , 0 , )),
	(( 'FillLibraryMenu' , 'Menu' , 'Result' , ), 17011, (17011, (), [ (9, 1, None, "IID('{C35D07D7-0248-40C5-A335-1D4FF1610F0A}')") , 
			 (16395, 10, None, None) , ], 1 , 1 , 4 , 0 , 136 , (3, 0, None, None) , 0 , )),
	(( 'GetLibraryCommandState' , 'Command' , 'Enable' , 'Checked' , 'Result' , 
			 ), 17012, (17012, (), [ (3, 1, None, None) , (16395, 2, None, None) , (16387, 2, None, None) , (16395, 10, None, None) , ], 1 , 1 , 4 , 0 , 144 , (3, 0, None, None) , 0 , )),
	(( 'GetDisableReason' , 'Command' , 'Result' , ), 17013, (17013, (), [ (3, 1, None, None) , 
			 (16392, 10, None, None) , ], 1 , 1 , 4 , 0 , 152 , (3, 0, None, None) , 0 , )),
	(( 'FillContextPanel' , 'ContextPanel' , 'Result' , ), 17014, (17014, (), [ (9, 1, None, None) , 
			 (16395, 10, None, None) , ], 1 , 1 , 4 , 0 , 160 , (3, 0, None, None) , 0 , )),
	(( 'ContextPanelStyleComboChanged' , 'StyleComboID' , 'styleType' , 'newValue' , 'Result' , 
			 ), 17015, (17015, (), [ (8, 1, None, None) , (3, 1, None, None) , (3, 1, None, None) , (16395, 10, None, None) , ], 1 , 1 , 4 , 0 , 168 , (3, 0, None, None) , 0 , )),
	(( 'GetKompasConverter' , 'Result' , ), 17016, (17016, (), [ (16393, 10, None, None) , ], 1 , 1 , 4 , 0 , 176 , (3, 0, None, None) , 0 , )),
	(( 'CreateMacroFromSample' , 'MacroReference' , 'Result' , ), 17017, (17017, (), [ (3, 1, None, None) , 
			 (16395, 10, None, None) , ], 1 , 1 , 4 , 0 , 184 , (3, 0, None, None) , 0 , )),
]

IKompasLibraryMenu_vtables_dispatch_ = 1
IKompasLibraryMenu_vtables_ = [
	(( 'AddMenuCommand' , 'Id' , 'Title' , 'Result' , ), 18001, (18001, (), [ 
			 (3, 1, None, None) , (8, 1, None, None) , (16395, 10, None, None) , ], 1 , 1 , 4 , 0 , 56 , (3, 0, None, None) , 0 , )),
	(( 'AddSeparator' , 'Result' , ), 18002, (18002, (), [ (16395, 10, None, None) , ], 1 , 1 , 4 , 0 , 64 , (3, 0, None, None) , 0 , )),
	(( 'AddSubMenu' , 'Title' , 'Result' , ), 18003, (18003, (), [ (8, 1, None, None) , 
			 (16395, 10, None, None) , ], 1 , 1 , 4 , 0 , 72 , (3, 0, None, None) , 0 , )),
	(( 'EndSubMenu' , 'Result' , ), 18004, (18004, (), [ (16395, 10, None, None) , ], 1 , 1 , 4 , 0 , 80 , (3, 0, None, None) , 0 , )),
]

RecordMap = {
}

CLSIDToClassMap = {
	'{025A21B0-0192-4A7C-A3F0-CA54AAA4FADB}' : IKompasLibrary,
	'{C35D07D7-0248-40C5-A335-1D4FF1610F0A}' : IKompasLibraryMenu,
	'{C222614E-AB59-4FEE-9F4A-1EAB7C1D4C5E}' : ksKompasLibrary,
}
CLSIDToPackageMap = {}
win32com.client.CLSIDToClass.RegisterCLSIDsFromDict( CLSIDToClassMap )
VTablesToPackageMap = {}
VTablesToClassMap = {
	'{025A21B0-0192-4A7C-A3F0-CA54AAA4FADB}' : 'IKompasLibrary',
	'{C35D07D7-0248-40C5-A335-1D4FF1610F0A}' : 'IKompasLibraryMenu',
}


NamesToIIDMap = {
	'IKompasLibrary' : '{025A21B0-0192-4A7C-A3F0-CA54AAA4FADB}',
	'IKompasLibraryMenu' : '{C35D07D7-0248-40C5-A335-1D4FF1610F0A}',
	'ksKompasLibrary' : '{C222614E-AB59-4FEE-9F4A-1EAB7C1D4C5E}',
}

win32com.client.constants.__dicts__.append(constants.__dict__)

