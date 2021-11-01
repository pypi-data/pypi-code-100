# -*- coding: mbcs -*-
# Created by makepy.py version 0.5.01
# By python version 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# From type library 'KGAX.tlb'
# On Mon Nov  1 14:49:13 2021
'KGAX ActiveX Control module'
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

CLSID = IID('{B97871C2-BB9B-49E7-8FD3-C1201922EDD8}')
MajorVersion = 1
MinorVersion = 0
LibraryFlags = 10
LCID = 0x0

class constants:
	vt_HiddenRemovedMode          =1          # from enum KDocument3DDrawMode
	vt_HiddenThinMode             =2          # from enum KDocument3DDrawMode
	vt_ShadedMode                 =3          # from enum KDocument3DDrawMode
	vt_WireframeMode              =0          # from enum KDocument3DDrawMode
	vt_3DAssembly                 =6          # from enum KDocumentType
	vt_3DPart                     =5          # from enum KDocumentType
	vt_Fragment                   =3          # from enum KDocumentType
	vt_SheetStandart              =1          # from enum KDocumentType
	vt_SheetUser                  =2          # from enum KDocumentType
	vt_Spc                        =4          # from enum KDocumentType
	vt_SpcUser                    =9          # from enum KDocumentType
	vt_TextStandart               =7          # from enum KDocumentType
	vt_TextUser                   =8          # from enum KDocumentType
	vt_CurrentLibManager          =1          # from enum KLibManagerMode
	vt_Default                    =0          # from enum KLibManagerMode
	vt_MainLibManager             =-1         # from enum KLibManagerMode
	vt_Refresh                    =6          # from enum KZoomType
	vt_ZoomEntureDocument         =5          # from enum KZoomType
	vt_ZoomIn                     =2          # from enum KZoomType
	vt_ZoomOut                    =3          # from enum KZoomType
	vt_ZoomSelected               =4          # from enum KZoomType
	vt_ZoomWindow                 =1          # from enum KZoomType

from win32com.client import DispatchBaseClass
class GLObject(DispatchBaseClass):
	"Вспомогательные данные для event'а OnKgCreateGLList."
	CLSID = IID('{89D7DB83-B61E-4A0A-8317-CE2481FFF4BB}')
	coclass_clsid = None

	def glBegin(self, mode=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(1, LCID, 1, (11, 0), ((3, 1),),mode
			)

	def glColor3d(self, r=defaultNamedNotOptArg, g=defaultNamedNotOptArg, b=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(20, LCID, 1, (11, 0), ((5, 1), (5, 1), (5, 1)),r
			, g, b)

	def glDisable(self, cap=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(4, LCID, 1, (11, 0), ((3, 1),),cap
			)

	def glEnable(self, cap=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(3, LCID, 1, (11, 0), ((3, 1),),cap
			)

	def glEnd(self):
		return self._oleobj_.InvokeTypes(2, LCID, 1, (11, 0), (),)

	def glLineStipple(self, factor=defaultNamedNotOptArg, pattern=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(22, LCID, 1, (11, 0), ((3, 1), (2, 1)),factor
			, pattern)

	def glLineWidth(self, w=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(21, LCID, 1, (11, 0), ((5, 1),),w
			)

	def glPointSize(self, w=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(23, LCID, 1, (11, 0), ((5, 1),),w
			)

	def glPolygonMode(self, face=defaultNamedNotOptArg, mode=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(24, LCID, 1, (11, 0), ((3, 1), (3, 1)),face
			, mode)

	def glVertex2d(self, x=defaultNamedNotOptArg, y=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(40, LCID, 1, (11, 0), ((5, 1), (5, 1)),x
			, y)

	def glVertex2dv(self, pData=defaultNamedNotOptArg, countDouble=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(41, LCID, 1, (11, 0), ((16389, 1), (3, 1)),pData
			, countDouble)

	def glVertex3d(self, x=defaultNamedNotOptArg, y=defaultNamedNotOptArg, z=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(42, LCID, 1, (11, 0), ((5, 1), (5, 1), (5, 1)),x
			, y, z)

	def glVertex3dv(self, pData=defaultNamedNotOptArg, countDouble=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(43, LCID, 1, (11, 0), ((16389, 1), (3, 1)),pData
			, countDouble)

	def glVertex4d(self, x=defaultNamedNotOptArg, y=defaultNamedNotOptArg, z=defaultNamedNotOptArg, w=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(44, LCID, 1, (11, 0), ((5, 1), (5, 1), (5, 1), (5, 1)),x
			, y, z, w)

	def glVertex4dv(self, pData=defaultNamedNotOptArg, countDouble=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(45, LCID, 1, (11, 0), ((16389, 1), (3, 1)),pData
			, countDouble)

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

class GabaritObject(DispatchBaseClass):
	"Вспомогательные данные для event'а OnKgAddGabatit."
	CLSID = IID('{89D7DB83-B61E-4A0A-8317-CE2481FFF4BC}')
	coclass_clsid = None

	def AddGabarit(self, p1X=defaultNamedNotOptArg, p1Y=defaultNamedNotOptArg, p1Z=defaultNamedNotOptArg, p2X=defaultNamedNotOptArg
			, p2Y=defaultNamedNotOptArg, p2Z=defaultNamedNotOptArg):
		'Добавить дополнительный габарит к габариту документа.'
		return self._oleobj_.InvokeTypes(1, LCID, 1, (11, 0), ((5, 1), (5, 1), (5, 1), (5, 1), (5, 1), (5, 1)),p1X
			, p1Y, p1Z, p2X, p2Y, p2Z
			)

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

class PaintObject(DispatchBaseClass):
	"Вспомогательные данные для event'а OnKgPaint."
	CLSID = IID('{89D7DB83-B61E-4A0A-8317-CE2481FFF4BA}')
	coclass_clsid = None

	def GetDC(self):
		'Получить Handle контекста отображения.'
		return self._oleobj_.InvokeTypes(2, LCID, 1, (3, 0), (),)

	def GetHWND(self):
		'Получить Handle окна.'
		return self._oleobj_.InvokeTypes(1, LCID, 1, (3, 0), (),)

	def GetTransformMatrix(self, a11=pythoncom.Missing, a12=pythoncom.Missing, a13=pythoncom.Missing, a14=pythoncom.Missing
			, a21=pythoncom.Missing, a22=pythoncom.Missing, a23=pythoncom.Missing, a24=pythoncom.Missing):
		'Получить коэффициенты для матрицы преобразования координат.'
		return self._ApplyTypes_(4, 1, (11, 0), ((16389, 2), (16389, 2), (16389, 2), (16389, 2), (16389, 2), (16389, 2), (16389, 2), (16389, 2)), 'GetTransformMatrix', None,a11
			, a12, a13, a14, a21, a22
			, a23, a24)

	def ReleaseDC(self, dc=defaultNamedNotOptArg):
		'Закрыть Handle контекста отображения.'
		return self._oleobj_.InvokeTypes(3, LCID, 1, (11, 0), ((3, 1),),dc
			)

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

class _DKGAX(DispatchBaseClass):
	'Dispatch interface for KGAX Control'
	CLSID = IID('{92B3A942-4E70-463B-9462-6424D9CE40CB}')
	coclass_clsid = IID('{6B943E71-5CA2-435D-AFA3-D7817B13ACA2}')

	def ActivateDocument(self, index=defaultNamedNotOptArg):
		'Активизирует документ по имени, идентификатору или индексу или reference.'
		return self._oleobj_.InvokeTypes(15, LCID, 1, (11, 0), ((12, 1),),index
			)

	def AddDocument(self, fileName=defaultNamedNotOptArg):
		'Добавить документ. Возвращает уникальный идентификатор документа.'
		return self._oleobj_.InvokeTypes(10, LCID, 1, (3, 0), ((8, 1),),fileName
			)

	def AddNewDocument(self, type=defaultNamedNotOptArg):
		'Добавить документ. Возвращает уникальный идентификатор документа.'
		return self._oleobj_.InvokeTypes(11, LCID, 1, (3, 0), ((3, 1),),type
			)

	def CloseAll(self):
		'Закрыть все документы.'
		return self._oleobj_.InvokeTypes(16, LCID, 1, (3, 0), (),)

	def DrawToDC(self, dc=defaultNamedNotOptArg, left=defaultNamedNotOptArg, top=defaultNamedNotOptArg, width=defaultNamedNotOptArg
			, height=defaultNamedNotOptArg):
		'Отрисовать документ на заданном HDC.'
		return self._oleobj_.InvokeTypes(26, LCID, 1, (11, 0), ((3, 1), (3, 1), (3, 1), (3, 1), (3, 1)),dc
			, left, top, width, height)

	def GetActiveDocumentID(self):
		'Получает идентификатор активного документа.'
		return self._oleobj_.InvokeTypes(8, LCID, 1, (3, 0), (),)

	def GetDocumentID(self, index=defaultNamedNotOptArg):
		'Получить идентификатор документа по индексу. -1 - активный.'
		return self._oleobj_.InvokeTypes(29, LCID, 1, (3, 0), ((12, 1),),index
			)

	def GetDocumentInterface(self, index=defaultNamedNotOptArg, newAPI=defaultNamedNotOptArg):
		'Получить указатель на документ по индексу. -1 - активный.'
		ret = self._oleobj_.InvokeTypes(7, LCID, 1, (9, 0), ((12, 1), (3, 0)),index
			, newAPI)
		if ret is not None:
			ret = Dispatch(ret, 'GetDocumentInterface', None)
		return ret

	def GetDocumentType(self, index=defaultNamedNotOptArg):
		'Получить тип документа по индексу. -1 - активный.'
		return self._oleobj_.InvokeTypes(6, LCID, 1, (3, 0), ((12, 1),),index
			)

	def GetDocumentsCount(self):
		'Получить количество открытых в KGAX документов.'
		return self._oleobj_.InvokeTypes(9, LCID, 1, (3, 0), (),)

	# Result is of type KompasObject
	def GetKompasObject(self):
		'Получить интерфейс на API КОМПАС-3D.'
		ret = self._oleobj_.InvokeTypes(5, LCID, 1, (9, 0), (),)
		if ret is not None:
			ret = Dispatch(ret, 'GetKompasObject', '{E36BC97C-39D6-4402-9C25-C7008A217E02}')
		return ret

	def InsertDocument(self, fileName=defaultNamedNotOptArg, index=defaultNamedNotOptArg):
		'Открыть документ с заданным именем и индексом в KGAX.'
		return self._oleobj_.InvokeTypes(12, LCID, 1, (3, 0), ((8, 1), (12, 1)),fileName
			, index)

	def InsertNewDocument(self, type=defaultNamedNotOptArg, index=defaultNamedNotOptArg):
		'Открыть документ с заданным именем и индексом в KGAX.'
		return self._oleobj_.InvokeTypes(13, LCID, 1, (3, 0), ((3, 1), (12, 1)),type
			, index)

	def InvalidateActiveDocument(self, erase=defaultNamedNotOptArg):
		'Перерисовать окно активного документа.'
		return self._oleobj_.InvokeTypes(18, LCID, 1, (11, 0), ((11, 1),),erase
			)

	def MoveViewDocument(self):
		'Сдвинуть изображение.'
		return self._oleobj_.InvokeTypes(20, LCID, 1, (24, 0), (),)

	def OrientationDocument(self):
		'Ориентация изображения.'
		return self._oleobj_.InvokeTypes(23, LCID, 1, (24, 0), (),)

	def PanoramaViewDocument(self):
		'Приблизить/отдалить изображение.'
		return self._oleobj_.InvokeTypes(21, LCID, 1, (24, 0), (),)

	def RemoveDocument(self, index=defaultNamedNotOptArg):
		'Закрыть документ по имени, идентификатору или индексу. -1 - активный.'
		return self._oleobj_.InvokeTypes(14, LCID, 1, (11, 0), ((12, 1),),index
			)

	def RotateViewDocument(self):
		'Повернуть изображение.'
		return self._oleobj_.InvokeTypes(22, LCID, 1, (24, 0), (),)

	def SetCurrentLibManager(self, t=defaultNamedNotOptArg):
		'Установить текущий менеджер библиотек.'
		return self._oleobj_.InvokeTypes(27, LCID, 1, (24, 0), ((3, 1),),t
			)

	def SetGabaritModifying(self):
		'Взвести флаг изменения габарита документа для собственного рисования в окне.'
		return self._oleobj_.InvokeTypes(28, LCID, 1, (24, 0), (),)

	def StopCurrentProcess(self, cancel=False):
		'Завершить текущий процесс.'
		return self._oleobj_.InvokeTypes(25, LCID, 1, (24, 0), ((11, 49),),cancel
			)

	def TestLoadDocument(self, fileName=defaultNamedNotOptArg):
		'Проверить возможность добавления докумета в KGAX.'
		return self._oleobj_.InvokeTypes(17, LCID, 1, (3, 0), ((8, 1),),fileName
			)

	def ZoomEntireDocument(self):
		'Показать в окне весь документ.'
		return self._oleobj_.InvokeTypes(19, LCID, 1, (24, 0), (),)

	def ZoomWindow(self, type=1):
		'Macштабировать окно документа.'
		return self._oleobj_.InvokeTypes(24, LCID, 1, (24, 0), ((3, 49),),type
			)

	_prop_map_get_ = {
		"Caption": (-518, 2, (8, 0), (), "Caption", None),
		"DocumenFileName": (2, 2, (8, 0), (), "DocumenFileName", None),
		"Document3DDrawMode": (3, 2, (3, 0), (), "Document3DDrawMode", None),
		"Document3DWireframeShadedMode": (4, 2, (11, 0), (), "Document3DWireframeShadedMode", None),
		"DocumentType": (1, 2, (3, 0), (), "DocumentType", None),
		"Text": (-517, 2, (8, 0), (), "Text", None),
	}
	_prop_map_put_ = {
		"Caption" : ((-518, LCID, 4, 0),()),
		"DocumenFileName" : ((2, LCID, 4, 0),()),
		"Document3DDrawMode" : ((3, LCID, 4, 0),()),
		"Document3DWireframeShadedMode" : ((4, LCID, 4, 0),()),
		"DocumentType" : ((1, LCID, 4, 0),()),
		"Text" : ((-517, LCID, 4, 0),()),
	}
	def __iter__(self):
		"Return a Python iterator for this object"
		try:
			ob = self._oleobj_.InvokeTypes(-4,LCID,3,(13, 10),())
		except pythoncom.error:
			raise TypeError("This object does not support enumeration")
		return win32com.client.util.Iterator(ob, None)

class _DKGAXEvents:
	'Event interface for KGAX Control'
	CLSID = CLSID_Sink = IID('{464F746A-AC6D-4919-82E9-A7363E661ECF}')
	coclass_clsid = IID('{6B943E71-5CA2-435D-AFA3-D7817B13ACA2}')
	_public_methods_ = [] # For COM Server support
	_dispid_to_func_ = {
		        1 : "OnKgMouseDown",
		        2 : "OnKgMouseUp",
		        3 : "OnKgMouseDblClick",
		        4 : "OnKgStopCurrentProcess",
		        5 : "OnKgCreate",
		        6 : "OnKgPaint",
		        7 : "OnKgCreateGLList",
		        8 : "OnKgAddGabatit",
		        9 : "OnKgErrorLoadDocument",
		       10 : "OnKgKeyDown",
		       11 : "OnKgKeyUp",
		       12 : "OnKgKeyPress",
		}

	def __init__(self, oobj = None):
		if oobj is None:
			self._olecp = None
		else:
			import win32com.server.util
			from win32com.server.policy import EventHandlerPolicy
			cpc=oobj._oleobj_.QueryInterface(pythoncom.IID_IConnectionPointContainer)
			cp=cpc.FindConnectionPoint(self.CLSID_Sink)
			cookie=cp.Advise(win32com.server.util.wrap(self, usePolicy=EventHandlerPolicy))
			self._olecp,self._olecp_cookie = cp,cookie
	def __del__(self):
		try:
			self.close()
		except pythoncom.com_error:
			pass
	def close(self):
		if self._olecp is not None:
			cp,cookie,self._olecp,self._olecp_cookie = self._olecp,self._olecp_cookie,None,None
			cp.Unadvise(cookie)
	def _query_interface_(self, iid):
		import win32com.server.util
		if iid==self.CLSID_Sink: return win32com.server.util.wrap(self)

	# Event Handlers
	# If you create handlers, they should have the following prototypes:
#	def OnKgMouseDown(self, nButton=defaultNamedNotOptArg, nShiftState=defaultNamedNotOptArg, x=defaultNamedNotOptArg, y=defaultNamedNotOptArg
#			, proceed=pythoncom.Missing):
#		'Нажатие кнопки мыши.'
#	def OnKgMouseUp(self, nButton=defaultNamedNotOptArg, nShiftState=defaultNamedNotOptArg, x=defaultNamedNotOptArg, y=defaultNamedNotOptArg
#			, proceed=pythoncom.Missing):
#		'Отпускание кнопки мыши.'
#	def OnKgMouseDblClick(self, nButton=defaultNamedNotOptArg, nShiftState=defaultNamedNotOptArg, x=defaultNamedNotOptArg, y=defaultNamedNotOptArg
#			, proceed=pythoncom.Missing):
#		'Двойной клик кнопки мыши.'
#	def OnKgStopCurrentProcess(self):
#		'Окончание процесса панаромирования, поворота, сдвига и т.д.'
#	def OnKgCreate(self, docID=defaultNamedNotOptArg):
#		'Окончание создания окна.'
#	def OnKgPaint(self, paintObj=defaultNamedNotOptArg):
#		'Окончание отрисовки в окне.'
#	def OnKgCreateGLList(self, glObj=defaultNamedNotOptArg, drawMode=defaultNamedNotOptArg):
#		'Окончание создания листа в контекста OpenGL.'
#	def OnKgAddGabatit(self, gabObj=defaultNamedNotOptArg):
#		'Определение габаритов документа.'
#	def OnKgErrorLoadDocument(self, docID=defaultNamedNotOptArg, fileName=defaultNamedNotOptArg, errorID=defaultNamedNotOptArg):
#		'Событие ошибки загрузки документа.'
#	def OnKgKeyDown(self, key=defaultNamedNotOptArg, nShiftState=defaultNamedNotOptArg):
#		'Событие нажатия клавиатуры когда контрол находится в фокусе.'
#	def OnKgKeyUp(self, key=defaultNamedNotOptArg, nShiftState=defaultNamedNotOptArg):
#		'Событие нажатия клавиатуры когда контрол находится в фокусе.'
#	def OnKgKeyPress(self, key=defaultNamedNotOptArg):
#		'Событие нажатия клавиатуры когда контрол находится в фокусе.'


from win32com.client import CoClassBaseClass
# This CoClass is known by the name 'KGAX.KGAXCtrl.1'
class KGAX(CoClassBaseClass): # A CoClass
	# KGAX Control
	CLSID = IID('{6B943E71-5CA2-435D-AFA3-D7817B13ACA2}')
	coclass_sources = [
		_DKGAXEvents,
	]
	default_source = _DKGAXEvents
	coclass_interfaces = [
		_DKGAX,
	]
	default_interface = _DKGAX

RecordMap = {
}

CLSIDToClassMap = {
	'{89D7DB83-B61E-4A0A-8317-CE2481FFF4BA}' : PaintObject,
	'{89D7DB83-B61E-4A0A-8317-CE2481FFF4BB}' : GLObject,
	'{89D7DB83-B61E-4A0A-8317-CE2481FFF4BC}' : GabaritObject,
	'{92B3A942-4E70-463B-9462-6424D9CE40CB}' : _DKGAX,
	'{464F746A-AC6D-4919-82E9-A7363E661ECF}' : _DKGAXEvents,
	'{6B943E71-5CA2-435D-AFA3-D7817B13ACA2}' : KGAX,
}
CLSIDToPackageMap = {}
win32com.client.CLSIDToClass.RegisterCLSIDsFromDict( CLSIDToClassMap )
VTablesToPackageMap = {}
VTablesToClassMap = {
}


NamesToIIDMap = {
	'PaintObject' : '{89D7DB83-B61E-4A0A-8317-CE2481FFF4BA}',
	'GLObject' : '{89D7DB83-B61E-4A0A-8317-CE2481FFF4BB}',
	'GabaritObject' : '{89D7DB83-B61E-4A0A-8317-CE2481FFF4BC}',
	'_DKGAX' : '{92B3A942-4E70-463B-9462-6424D9CE40CB}',
	'_DKGAXEvents' : '{464F746A-AC6D-4919-82E9-A7363E661ECF}',
}

win32com.client.constants.__dicts__.append(constants.__dict__)

