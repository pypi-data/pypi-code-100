# -*- coding: mbcs -*-
# Created by makepy.py version 0.5.01
# By python version 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# From type library 'ksTreeView.tlb'
# On Mon Nov  1 14:50:15 2021
'ksTreeView ActiveX Control module'
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

CLSID = IID('{583EF606-0355-4170-9EA7-EE3D62FD9681}')
MajorVersion = 1
MinorVersion = 0
LibraryFlags = 10
LCID = 0x0

class constants:
	ksTVGN_IDCM_MAX               =6500       # from enum ksTreeViewIDEnum
	ksTVGN_IDCM_MIN               =3501       # from enum ksTreeViewIDEnum
	ksTVGN_IDM_MAX                =3500       # from enum ksTreeViewIDEnum
	ksTVGN_IDM_MIN                =500        # from enum ksTreeViewIDEnum
	ksTVGN_CARET                  =9          # from enum ksTreeViewNextItemEnum
	ksTVGN_CHILD                  =4          # from enum ksTreeViewNextItemEnum
	ksTVGN_DROPHILITE             =8          # from enum ksTreeViewNextItemEnum
	ksTVGN_FIRSTVISIBLE           =5          # from enum ksTreeViewNextItemEnum
	ksTVGN_NEXT                   =1          # from enum ksTreeViewNextItemEnum
	ksTVGN_NEXTVISIBLE            =6          # from enum ksTreeViewNextItemEnum
	ksTVGN_PARENT                 =3          # from enum ksTreeViewNextItemEnum
	ksTVGN_PREVIOUS               =2          # from enum ksTreeViewNextItemEnum
	ksTVGN_PREVIOUSVISIBLE        =7          # from enum ksTreeViewNextItemEnum
	ksTVGN_ROOT                   =0          # from enum ksTreeViewNextItemEnum

from win32com.client import DispatchBaseClass
class IksTreeDlg(DispatchBaseClass):
	'ksTreeDlg Control - KSTREEDLG.ksTreeDlgCtrl.1'
	CLSID = IID('{A3D30516-5EBF-4A40-8483-29CA14B9CD66}')
	coclass_clsid = IID('{5C78F9EA-7618-43EB-934E-42D2A6B5D022}')

	def LoadToolBar(self, ResModule=defaultNamedNotOptArg, ToolbarId=defaultNamedNotOptArg):
		'Загрузка ToolBar-а.'
		return self._oleobj_.InvokeTypes(2, LCID, 1, (11, 0), ((12, 1), (12, 1)),ResModule
			, ToolbarId)

	_prop_map_get_ = {
		# Method 'TreeView' returns object of type 'IksTreeView'
		"TreeView": (1, 2, (9, 0), (), "TreeView", '{9F9E4600-03CA-4720-AACA-FDE955969B43}'),
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

class IksTreeView(DispatchBaseClass):
	'ksTreeView Control - KSTREEVIEW.ksTreeViewCtrl.1'
	CLSID = IID('{9F9E4600-03CA-4720-AACA-FDE955969B43}')
	coclass_clsid = IID('{241F4962-136B-4589-BBA4-F23F2A8D580D}')

	def AddItem(self, PatentItemID=defaultNamedNotOptArg, ItemText=defaultNamedNotOptArg, NImage=defaultNamedNotOptArg, NSelectImage=defaultNamedNotOptArg
			, HInsertAfter=defaultNamedNotOptArg):
		'Добавить элемент.'
		return self._oleobj_.InvokeTypes(2, LCID, 1, (20, 0), ((20, 1), (8, 1), (3, 1), (3, 1), (20, 1)),PatentItemID
			, ItemText, NImage, NSelectImage, HInsertAfter)

	def GetNextItem(self, HItem=defaultNamedNotOptArg, NCode=defaultNamedNotOptArg):
		'Установить ImageList.'
		return self._oleobj_.InvokeTypes(5, LCID, 1, (20, 0), ((20, 1), (3, 1)),HItem
			, NCode)

	def LoadFromFile(self, FileName=defaultNamedNotOptArg):
		'Загрузить из файла.'
		return self._oleobj_.InvokeTypes(6, LCID, 1, (11, 0), ((8, 1),),FileName
			)

	def SaveToFile(self, FileName=defaultNamedNotOptArg):
		'Загрузить из файла.'
		return self._oleobj_.InvokeTypes(7, LCID, 1, (11, 0), ((8, 1),),FileName
			)

	def SetContextMenu(self, Val=defaultNamedNotOptArg):
		'Установить меню.'
		return self._oleobj_.InvokeTypes(3, LCID, 1, (24, 0), ((3, 1),),Val
			)

	def SetImageList(self, Val=defaultNamedNotOptArg, NImageListType=defaultNamedNotOptArg):
		'Установить ImageList.'
		return self._oleobj_.InvokeTypes(4, LCID, 1, (24, 0), ((3, 1), (3, 1)),Val
			, NImageListType)

	_prop_map_get_ = {
		"Handle": (1, 2, (3, 0), (), "Handle", None),
		"Items": (8, 2, (12, 0), (), "Items", None),
		"ReadOnly": (9, 2, (11, 0), (), "ReadOnly", None),
	}
	_prop_map_put_ = {
		"Items": ((8, LCID, 4, 0),()),
		"ReadOnly": ((9, LCID, 4, 0),()),
	}
	def __iter__(self):
		"Return a Python iterator for this object"
		try:
			ob = self._oleobj_.InvokeTypes(-4,LCID,3,(13, 10),())
		except pythoncom.error:
			raise TypeError("This object does not support enumeration")
		return win32com.client.util.Iterator(ob, None)

class _DksTreeDlgEvents:
	'Event interface for ksTreeDlg Control'
	CLSID = CLSID_Sink = IID('{DD7463A6-8307-4205-8AA9-FD350818679A}')
	coclass_clsid = IID('{5C78F9EA-7618-43EB-934E-42D2A6B5D022}')
	_public_methods_ = [] # For COM Server support
	_dispid_to_func_ = {
		        1 : "OnToolBarCommand",
		        2 : "OnButtonUpdate",
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
#	def OnToolBarCommand(self, Id=defaultNamedNotOptArg):
#		'Запуск команды.'
#	def OnButtonUpdate(self, Id=defaultNamedNotOptArg, Enabled=defaultNamedNotOptArg, Checked=defaultNamedNotOptArg):
#		'Состояние команды.'


class _DksTreeViewEvents:
	'Event interface for ksTreeView Control KSTREEVIEW.ksTreeViewCtrl.1'
	CLSID = CLSID_Sink = IID('{1872133E-ECF9-4EBC-B59A-C39C4773582D}')
	coclass_clsid = IID('{241F4962-136B-4589-BBA4-F23F2A8D580D}')
	_public_methods_ = [] # For COM Server support
	_dispid_to_func_ = {
		        1 : "OnBeforeLabelEdit",
		        2 : "OnAfterLabelEdit",
		        3 : "OnCollapse",
		        4 : "OnExpand",
		        5 : "OnNodeClick",
		     -602 : "OnKeyDown",
		     -604 : "OnKeyUp",
		     -603 : "OnKeyPress",
		     -605 : "OnMouseDown",
		     -606 : "OnMouseMove",
		     -607 : "OnMouseUp",
		     -600 : "OnClick",
		     -601 : "OnDblClick",
		        7 : "OnMenuCommand",
		        8 : "OnMenuCommandUpdate",
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
#	def OnBeforeLabelEdit(self, Cancel=defaultNamedNotOptArg):
#		'Occurs when a user attempts to edit the label of the currently selected ListItem or Node object.'
#	def OnAfterLabelEdit(self, Cancel=defaultNamedNotOptArg, NewString=defaultNamedNotOptArg):
#		'Occurs after a user edits the label of the currently selected Node or ListItem object.'
#	def OnCollapse(self, NodeId=defaultNamedNotOptArg):
#		'Generated when any Node object in a TreeView control is collapsed.'
#	def OnExpand(self, NodeId=defaultNamedNotOptArg):
#		'Occurs when a Node object in a TreeView control is expanded; that is, when its child nodes become visible.'
#	def OnNodeClick(self, NodeId=defaultNamedNotOptArg):
#		'Occurs when a Node object is clicked.'
#	def OnKeyDown(self, KeyCode=defaultNamedNotOptArg, Shift=defaultNamedNotOptArg):
#		'Occurs when the user presses a key while an object has the focus.'
#	def OnKeyUp(self, KeyCode=defaultNamedNotOptArg, Shift=defaultNamedNotOptArg):
#		'Occurs when the user releases a key while an object has the focus.'
#	def OnKeyPress(self, KeyAscii=defaultNamedNotOptArg):
#		'Occurs when the user presses and releases an ANSI key.'
#	def OnMouseDown(self, Button=defaultNamedNotOptArg, Shift=defaultNamedNotOptArg, x=defaultNamedNotOptArg, y=defaultNamedNotOptArg):
#		'Occurs when the user presses the mouse button while an object has the focus.'
#	def OnMouseMove(self, Button=defaultNamedNotOptArg, Shift=defaultNamedNotOptArg, x=defaultNamedNotOptArg, y=defaultNamedNotOptArg):
#		'Occurs when the user moves the mouse.'
#	def OnMouseUp(self, Button=defaultNamedNotOptArg, Shift=defaultNamedNotOptArg, x=defaultNamedNotOptArg, y=defaultNamedNotOptArg):
#		'Occurs when the user releases the mouse button while an object has the focus.'
#	def OnClick(self):
#		'Occurs when the user presses and then releases a mouse button over an object.'
#	def OnDblClick(self):
#		'Occurs when you press and release a mouse button and then press and release it again over an object.'
#	def OnMenuCommand(self, Id=defaultNamedNotOptArg):
#		'Выбор пункта меню.'
#	def OnMenuCommandUpdate(self, Id=defaultNamedNotOptArg, Enabled=defaultNamedNotOptArg, Checked=defaultNamedNotOptArg):
#		'Состояние команды меню.'


from win32com.client import CoClassBaseClass
class ksTreeDlg(CoClassBaseClass): # A CoClass
	# ksTreeDlg Control
	CLSID = IID('{5C78F9EA-7618-43EB-934E-42D2A6B5D022}')
	coclass_sources = [
		_DksTreeDlgEvents,
	]
	default_source = _DksTreeDlgEvents
	coclass_interfaces = [
		IksTreeDlg,
	]
	default_interface = IksTreeDlg

class ksTreeView(CoClassBaseClass): # A CoClass
	# ksTreeView Control - KSTREEVIEW.ksTreeViewCtrl.1
	CLSID = IID('{241F4962-136B-4589-BBA4-F23F2A8D580D}')
	coclass_sources = [
		_DksTreeViewEvents,
	]
	default_source = _DksTreeViewEvents
	coclass_interfaces = [
		IksTreeView,
	]
	default_interface = IksTreeView

IksTreeDlg_vtables_dispatch_ = 1
IksTreeDlg_vtables_ = [
	(( 'TreeView' , 'Tree' , ), 1, (1, (), [ (16393, 10, None, "IID('{9F9E4600-03CA-4720-AACA-FDE955969B43}')") , ], 1 , 2 , 4 , 0 , 56 , (3, 0, None, None) , 0 , )),
	(( 'LoadToolBar' , 'ResModule' , 'ToolbarId' , 'Result' , ), 2, (2, (), [ 
			 (12, 1, None, None) , (12, 1, None, None) , (16395, 10, None, None) , ], 1 , 1 , 4 , 0 , 64 , (3, 0, None, None) , 0 , )),
]

IksTreeView_vtables_dispatch_ = 1
IksTreeView_vtables_ = [
	(( 'Handle' , 'ItemId' , ), 1, (1, (), [ (16387, 10, None, None) , ], 1 , 2 , 4 , 0 , 56 , (3, 0, None, None) , 0 , )),
	(( 'AddItem' , 'PatentItemID' , 'ItemText' , 'NImage' , 'NSelectImage' , 
			 'HInsertAfter' , 'ItemId' , ), 2, (2, (), [ (20, 1, None, None) , (8, 1, None, None) , 
			 (3, 1, None, None) , (3, 1, None, None) , (20, 1, None, None) , (16404, 10, None, None) , ], 1 , 1 , 4 , 0 , 64 , (3, 0, None, None) , 0 , )),
	(( 'SetContextMenu' , 'Val' , ), 3, (3, (), [ (3, 1, None, None) , ], 1 , 1 , 4 , 0 , 72 , (3, 0, None, None) , 0 , )),
	(( 'SetImageList' , 'Val' , 'NImageListType' , ), 4, (4, (), [ (3, 1, None, None) , 
			 (3, 1, None, None) , ], 1 , 1 , 4 , 0 , 80 , (3, 0, None, None) , 0 , )),
	(( 'GetNextItem' , 'HItem' , 'NCode' , 'NextItemId' , ), 5, (5, (), [ 
			 (20, 1, None, None) , (3, 1, None, None) , (16404, 10, None, None) , ], 1 , 1 , 4 , 0 , 88 , (3, 0, None, None) , 0 , )),
	(( 'LoadFromFile' , 'FileName' , 'Result' , ), 6, (6, (), [ (8, 1, None, None) , 
			 (16395, 10, None, None) , ], 1 , 1 , 4 , 0 , 96 , (3, 0, None, None) , 0 , )),
	(( 'SaveToFile' , 'FileName' , 'Result' , ), 7, (7, (), [ (8, 1, None, None) , 
			 (16395, 10, None, None) , ], 1 , 1 , 4 , 0 , 104 , (3, 0, None, None) , 0 , )),
	(( 'Items' , 'Items' , ), 8, (8, (), [ (16396, 10, None, None) , ], 1 , 2 , 4 , 0 , 112 , (3, 0, None, None) , 0 , )),
	(( 'Items' , 'Items' , ), 8, (8, (), [ (12, 1, None, None) , ], 1 , 4 , 4 , 0 , 120 , (3, 0, None, None) , 0 , )),
	(( 'ReadOnly' , 'pVal' , ), 9, (9, (), [ (16395, 10, None, None) , ], 1 , 2 , 4 , 0 , 128 , (3, 0, None, None) , 0 , )),
	(( 'ReadOnly' , 'pVal' , ), 9, (9, (), [ (11, 1, None, None) , ], 1 , 4 , 4 , 0 , 136 , (3, 0, None, None) , 0 , )),
]

RecordMap = {
}

CLSIDToClassMap = {
	'{9F9E4600-03CA-4720-AACA-FDE955969B43}' : IksTreeView,
	'{1872133E-ECF9-4EBC-B59A-C39C4773582D}' : _DksTreeViewEvents,
	'{241F4962-136B-4589-BBA4-F23F2A8D580D}' : ksTreeView,
	'{A3D30516-5EBF-4A40-8483-29CA14B9CD66}' : IksTreeDlg,
	'{DD7463A6-8307-4205-8AA9-FD350818679A}' : _DksTreeDlgEvents,
	'{5C78F9EA-7618-43EB-934E-42D2A6B5D022}' : ksTreeDlg,
}
CLSIDToPackageMap = {}
win32com.client.CLSIDToClass.RegisterCLSIDsFromDict( CLSIDToClassMap )
VTablesToPackageMap = {}
VTablesToClassMap = {
	'{9F9E4600-03CA-4720-AACA-FDE955969B43}' : 'IksTreeView',
	'{A3D30516-5EBF-4A40-8483-29CA14B9CD66}' : 'IksTreeDlg',
}


NamesToIIDMap = {
	'IksTreeView' : '{9F9E4600-03CA-4720-AACA-FDE955969B43}',
	'_DksTreeViewEvents' : '{1872133E-ECF9-4EBC-B59A-C39C4773582D}',
	'IksTreeDlg' : '{A3D30516-5EBF-4A40-8483-29CA14B9CD66}',
	'_DksTreeDlgEvents' : '{DD7463A6-8307-4205-8AA9-FD350818679A}',
}

win32com.client.constants.__dicts__.append(constants.__dict__)

