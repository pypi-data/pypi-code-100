# -*- coding: mbcs -*-
# Created by makepy.py version 0.5.01
# By python version 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# From type library 'VCHatch.tlb'
# On Mon Nov  1 14:51:53 2021
'VCHatch ActiveX Control module'
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

CLSID = IID('{2AFD2EAF-A5DE-4A3D-95BA-D2C1E43C1088}')
MajorVersion = 1
MinorVersion = 0
LibraryFlags = 10
LCID = 0x0

from win32com.client import DispatchBaseClass
class _DVCHatch(DispatchBaseClass):
	'Dispatch interface for VCHatch Control'
	CLSID = IID('{3FFE9799-DF8D-4936-980C-BEA28964A3A7}')
	coclass_clsid = IID('{FFED03F1-481A-4ACD-A39E-C5D4A8828236}')

	_prop_map_get_ = {
		"Angle": (1, 2, (5, 0), (), "Angle", None),
		"Enable": (3, 2, (11, 0), (), "Enable", None),
		"Step": (2, 2, (5, 0), (), "Step", None),
	}
	_prop_map_put_ = {
		"Angle" : ((1, LCID, 4, 0),()),
		"Enable" : ((3, LCID, 4, 0),()),
		"Step" : ((2, LCID, 4, 0),()),
	}
	def __iter__(self):
		"Return a Python iterator for this object"
		try:
			ob = self._oleobj_.InvokeTypes(-4,LCID,3,(13, 10),())
		except pythoncom.error:
			raise TypeError("This object does not support enumeration")
		return win32com.client.util.Iterator(ob, None)

class _DVCHatchEvents:
	'Event interface for VCHatch Control'
	CLSID = CLSID_Sink = IID('{26776524-F601-42CE-A49E-90CF804111A5}')
	coclass_clsid = IID('{FFED03F1-481A-4ACD-A39E-C5D4A8828236}')
	_public_methods_ = [] # For COM Server support
	_dispid_to_func_ = {
		        1 : "OnChangeAngle",
		        2 : "OnChangeStep",
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
#	def OnChangeAngle(self):
#	def OnChangeStep(self):


from win32com.client import CoClassBaseClass
# This CoClass is known by the name 'VCHATCH.VCHatchCtrl.1'
class VCHatch(CoClassBaseClass): # A CoClass
	# VCHatch Control
	CLSID = IID('{FFED03F1-481A-4ACD-A39E-C5D4A8828236}')
	coclass_sources = [
		_DVCHatchEvents,
	]
	default_source = _DVCHatchEvents
	coclass_interfaces = [
		_DVCHatch,
	]
	default_interface = _DVCHatch

RecordMap = {
}

CLSIDToClassMap = {
	'{3FFE9799-DF8D-4936-980C-BEA28964A3A7}' : _DVCHatch,
	'{26776524-F601-42CE-A49E-90CF804111A5}' : _DVCHatchEvents,
	'{FFED03F1-481A-4ACD-A39E-C5D4A8828236}' : VCHatch,
}
CLSIDToPackageMap = {}
win32com.client.CLSIDToClass.RegisterCLSIDsFromDict( CLSIDToClassMap )
VTablesToPackageMap = {}
VTablesToClassMap = {
}


NamesToIIDMap = {
	'_DVCHatch' : '{3FFE9799-DF8D-4936-980C-BEA28964A3A7}',
	'_DVCHatchEvents' : '{26776524-F601-42CE-A49E-90CF804111A5}',
}


