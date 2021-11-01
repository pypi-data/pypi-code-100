# -*- coding: mbcs -*-
# Created by makepy.py version 0.5.01
# By python version 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# From type library 'Pdf2d.tlb'
# On Mon Nov  1 14:51:00 2021
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

CLSID = IID('{31EBF650-BD38-43EC-892B-1F8AC6C14430}')
MajorVersion = 1
MinorVersion = 0
LibraryFlags = 8
LCID = 0x0

from win32com.client import DispatchBaseClass
class IPdf2dParam(DispatchBaseClass):
	'Параметры конвертера'
	CLSID = IID('{1BF78A7C-E274-4B61-8771-EBD0542E8F04}')
	coclass_clsid = None

	_prop_map_get_ = {
		"ColorType": (5, 2, (3, 0), (), "ColorType", None),
		"CutByFormat": (21, 2, (11, 0), (), "CutByFormat", None),
		"DrawQuality": (17, 2, (3, 0), (), "DrawQuality", None),
		"EmbedFonts": (1, 2, (11, 0), (), "EmbedFonts", None),
		"FilterDisable": (18, 2, (11, 0), (), "FilterDisable", None),
		"FilterFlags": (19, 2, (3, 0), (), "FilterFlags", None),
		"FilterStyles": (20, 2, (3, 0), (), "FilterStyles", None),
		"GrayScale": (2, 2, (11, 0), (), "GrayScale", None),
		"HeightUserSheet": (16, 2, (5, 0), (), "HeightUserSheet", None),
		"HorizontOrientation": (12, 2, (11, 0), (), "HorizontOrientation", None),
		"ISOid": (13, 2, (3, 0), (), "ISOid", None),
		"MultiPageOutput": (7, 2, (11, 0), (), "MultiPageOutput", None),
		"MultipleFormat": (14, 2, (3, 0), (), "MultipleFormat", None),
		"OnlyThinLine": (6, 2, (11, 0), (), "OnlyThinLine", None),
		"PageOddEven": (10, 2, (3, 0), (), "PageOddEven", None),
		"PageRange": (8, 2, (3, 0), (), "PageRange", None),
		"PageRangeStr": (9, 2, (8, 0), (), "PageRangeStr", None),
		"Resolution": (3, 2, (3, 0), (), "Resolution", None),
		"Scale": (4, 2, (5, 0), (), "Scale", None),
		"UserFormat": (11, 2, (11, 0), (), "UserFormat", None),
		"WidthUserSheet": (15, 2, (5, 0), (), "WidthUserSheet", None),
	}
	_prop_map_put_ = {
		"ColorType": ((5, LCID, 4, 0),()),
		"CutByFormat": ((21, LCID, 4, 0),()),
		"DrawQuality": ((17, LCID, 4, 0),()),
		"EmbedFonts": ((1, LCID, 4, 0),()),
		"FilterDisable": ((18, LCID, 4, 0),()),
		"FilterFlags": ((19, LCID, 4, 0),()),
		"FilterStyles": ((20, LCID, 4, 0),()),
		"GrayScale": ((2, LCID, 4, 0),()),
		"HeightUserSheet": ((16, LCID, 4, 0),()),
		"HorizontOrientation": ((12, LCID, 4, 0),()),
		"ISOid": ((13, LCID, 4, 0),()),
		"MultiPageOutput": ((7, LCID, 4, 0),()),
		"MultipleFormat": ((14, LCID, 4, 0),()),
		"OnlyThinLine": ((6, LCID, 4, 0),()),
		"PageOddEven": ((10, LCID, 4, 0),()),
		"PageRange": ((8, LCID, 4, 0),()),
		"PageRangeStr": ((9, LCID, 4, 0),()),
		"Resolution": ((3, LCID, 4, 0),()),
		"Scale": ((4, LCID, 4, 0),()),
		"UserFormat": ((11, LCID, 4, 0),()),
		"WidthUserSheet": ((15, LCID, 4, 0),()),
	}
	def __iter__(self):
		"Return a Python iterator for this object"
		try:
			ob = self._oleobj_.InvokeTypes(-4,LCID,3,(13, 10),())
		except pythoncom.error:
			raise TypeError("This object does not support enumeration")
		return win32com.client.util.Iterator(ob, None)

IPdf2dParam_vtables_dispatch_ = 1
IPdf2dParam_vtables_ = [
	(( 'EmbedFonts' , 'PVal' , ), 1, (1, (), [ (16395, 10, None, None) , ], 1 , 2 , 4 , 0 , 56 , (3, 0, None, None) , 0 , )),
	(( 'EmbedFonts' , 'PVal' , ), 1, (1, (), [ (11, 49, 'True', None) , ], 1 , 4 , 4 , 0 , 64 , (3, 0, None, None) , 0 , )),
	(( 'GrayScale' , 'PVal' , ), 2, (2, (), [ (16395, 10, None, None) , ], 1 , 2 , 4 , 0 , 72 , (3, 0, None, None) , 0 , )),
	(( 'GrayScale' , 'PVal' , ), 2, (2, (), [ (11, 49, 'False', None) , ], 1 , 4 , 4 , 0 , 80 , (3, 0, None, None) , 0 , )),
	(( 'Resolution' , 'PVal' , ), 3, (3, (), [ (16387, 10, None, None) , ], 1 , 2 , 4 , 0 , 88 , (3, 0, None, None) , 0 , )),
	(( 'Resolution' , 'PVal' , ), 3, (3, (), [ (3, 49, '300', None) , ], 1 , 4 , 4 , 0 , 96 , (3, 0, None, None) , 0 , )),
	(( 'Scale' , 'PVal' , ), 4, (4, (), [ (16389, 10, None, None) , ], 1 , 2 , 4 , 0 , 104 , (3, 0, None, None) , 0 , )),
	(( 'Scale' , 'PVal' , ), 4, (4, (), [ (5, 49, '1.0', None) , ], 1 , 4 , 4 , 0 , 112 , (3, 0, None, None) , 0 , )),
	(( 'ColorType' , 'PVal' , ), 5, (5, (), [ (16387, 10, None, None) , ], 1 , 2 , 4 , 0 , 120 , (3, 0, None, None) , 0 , )),
	(( 'ColorType' , 'PVal' , ), 5, (5, (), [ (3, 49, '3', None) , ], 1 , 4 , 4 , 0 , 128 , (3, 0, None, None) , 0 , )),
	(( 'OnlyThinLine' , 'PVal' , ), 6, (6, (), [ (16395, 10, None, None) , ], 1 , 2 , 4 , 0 , 136 , (3, 0, None, None) , 0 , )),
	(( 'OnlyThinLine' , 'PVal' , ), 6, (6, (), [ (11, 49, 'False', None) , ], 1 , 4 , 4 , 0 , 144 , (3, 0, None, None) , 0 , )),
	(( 'MultiPageOutput' , 'PVal' , ), 7, (7, (), [ (16395, 10, None, None) , ], 1 , 2 , 4 , 0 , 152 , (3, 0, None, None) , 0 , )),
	(( 'MultiPageOutput' , 'PVal' , ), 7, (7, (), [ (11, 49, 'True', None) , ], 1 , 4 , 4 , 0 , 160 , (3, 0, None, None) , 0 , )),
	(( 'PageRange' , 'PVal' , ), 8, (8, (), [ (16387, 10, None, None) , ], 1 , 2 , 4 , 0 , 168 , (3, 0, None, None) , 0 , )),
	(( 'PageRange' , 'PVal' , ), 8, (8, (), [ (3, 49, '0', None) , ], 1 , 4 , 4 , 0 , 176 , (3, 0, None, None) , 0 , )),
	(( 'PageRangeStr' , 'PVal' , ), 9, (9, (), [ (16392, 10, None, None) , ], 1 , 2 , 4 , 0 , 184 , (3, 0, None, None) , 0 , )),
	(( 'PageRangeStr' , 'PVal' , ), 9, (9, (), [ (8, 1, None, None) , ], 1 , 4 , 4 , 0 , 192 , (3, 0, None, None) , 0 , )),
	(( 'PageOddEven' , 'PVal' , ), 10, (10, (), [ (16387, 10, None, None) , ], 1 , 2 , 4 , 0 , 200 , (3, 0, None, None) , 0 , )),
	(( 'PageOddEven' , 'PVal' , ), 10, (10, (), [ (3, 49, '0', None) , ], 1 , 4 , 4 , 0 , 208 , (3, 0, None, None) , 0 , )),
	(( 'UserFormat' , 'PVal' , ), 11, (11, (), [ (16395, 10, None, None) , ], 1 , 2 , 4 , 0 , 216 , (3, 0, None, None) , 0 , )),
	(( 'UserFormat' , 'PVal' , ), 11, (11, (), [ (11, 49, 'False', None) , ], 1 , 4 , 4 , 0 , 224 , (3, 0, None, None) , 0 , )),
	(( 'HorizontOrientation' , 'PVal' , ), 12, (12, (), [ (16395, 10, None, None) , ], 1 , 2 , 4 , 0 , 232 , (3, 0, None, None) , 0 , )),
	(( 'HorizontOrientation' , 'PVal' , ), 12, (12, (), [ (11, 49, 'False', None) , ], 1 , 4 , 4 , 0 , 240 , (3, 0, None, None) , 0 , )),
	(( 'ISOid' , 'PVal' , ), 13, (13, (), [ (16387, 10, None, None) , ], 1 , 2 , 4 , 0 , 248 , (3, 0, None, None) , 0 , )),
	(( 'ISOid' , 'PVal' , ), 13, (13, (), [ (3, 49, '4', None) , ], 1 , 4 , 4 , 0 , 256 , (3, 0, None, None) , 0 , )),
	(( 'MultipleFormat' , 'PVal' , ), 14, (14, (), [ (16387, 10, None, None) , ], 1 , 2 , 4 , 0 , 264 , (3, 0, None, None) , 0 , )),
	(( 'MultipleFormat' , 'PVal' , ), 14, (14, (), [ (3, 49, '1', None) , ], 1 , 4 , 4 , 0 , 272 , (3, 0, None, None) , 0 , )),
	(( 'WidthUserSheet' , 'PVal' , ), 15, (15, (), [ (16389, 10, None, None) , ], 1 , 2 , 4 , 0 , 280 , (3, 0, None, None) , 0 , )),
	(( 'WidthUserSheet' , 'PVal' , ), 15, (15, (), [ (5, 49, '210.0', None) , ], 1 , 4 , 4 , 0 , 288 , (3, 0, None, None) , 0 , )),
	(( 'HeightUserSheet' , 'PVal' , ), 16, (16, (), [ (16389, 10, None, None) , ], 1 , 2 , 4 , 0 , 296 , (3, 0, None, None) , 0 , )),
	(( 'HeightUserSheet' , 'PVal' , ), 16, (16, (), [ (5, 49, '297.0', None) , ], 1 , 4 , 4 , 0 , 304 , (3, 0, None, None) , 0 , )),
	(( 'DrawQuality' , 'PVal' , ), 17, (17, (), [ (16387, 10, None, None) , ], 1 , 2 , 4 , 0 , 312 , (3, 0, None, None) , 0 , )),
	(( 'DrawQuality' , 'PVal' , ), 17, (17, (), [ (3, 49, '50', None) , ], 1 , 4 , 4 , 0 , 320 , (3, 0, None, None) , 0 , )),
	(( 'FilterDisable' , 'PVal' , ), 18, (18, (), [ (16395, 10, None, None) , ], 1 , 2 , 4 , 0 , 328 , (3, 0, None, None) , 0 , )),
	(( 'FilterDisable' , 'PVal' , ), 18, (18, (), [ (11, 49, 'True', None) , ], 1 , 4 , 4 , 0 , 336 , (3, 0, None, None) , 0 , )),
	(( 'FilterFlags' , 'PVal' , ), 19, (19, (), [ (16387, 10, None, None) , ], 1 , 2 , 4 , 0 , 344 , (3, 0, None, None) , 0 , )),
	(( 'FilterFlags' , 'PVal' , ), 19, (19, (), [ (3, 49, '36863', None) , ], 1 , 4 , 4 , 0 , 352 , (3, 0, None, None) , 0 , )),
	(( 'FilterStyles' , 'PVal' , ), 20, (20, (), [ (16387, 10, None, None) , ], 1 , 2 , 4 , 0 , 360 , (3, 0, None, None) , 0 , )),
	(( 'FilterStyles' , 'PVal' , ), 20, (20, (), [ (3, 49, '256', None) , ], 1 , 4 , 4 , 0 , 368 , (3, 0, None, None) , 0 , )),
	(( 'CutByFormat' , 'PVal' , ), 21, (21, (), [ (16395, 10, None, None) , ], 1 , 2 , 4 , 0 , 376 , (3, 0, None, None) , 0 , )),
	(( 'CutByFormat' , 'PVal' , ), 21, (21, (), [ (11, 49, 'True', None) , ], 1 , 4 , 4 , 0 , 384 , (3, 0, None, None) , 0 , )),
]

RecordMap = {
}

CLSIDToClassMap = {
	'{1BF78A7C-E274-4B61-8771-EBD0542E8F04}' : IPdf2dParam,
}
CLSIDToPackageMap = {}
win32com.client.CLSIDToClass.RegisterCLSIDsFromDict( CLSIDToClassMap )
VTablesToPackageMap = {}
VTablesToClassMap = {
	'{1BF78A7C-E274-4B61-8771-EBD0542E8F04}' : 'IPdf2dParam',
}


NamesToIIDMap = {
	'IPdf2dParam' : '{1BF78A7C-E274-4B61-8771-EBD0542E8F04}',
}


