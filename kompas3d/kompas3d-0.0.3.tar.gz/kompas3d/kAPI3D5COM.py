# -*- coding: mbcs -*-
# Created by makepy.py version 0.5.01
# By python version 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# From type library 'kAPI3D5COM.tlb'
# On Mon Nov  1 14:47:55 2021
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

CLSID = IID('{006C01C3-FA63-4F20-B930-CCE6DD3A9236}')
MajorVersion = 1
MinorVersion = 0
LibraryFlags = 8
LCID = 0x0

IAdditionFormatParam_vtables_dispatch_ = 0
IAdditionFormatParam_vtables_ = [
	(( 'GetFormat' , ), 1610678272, (1610678272, (), [ ], 1 , 1 , 4 , 0 , 24 , (2, 0, None, None) , 0 , )),
	(( 'SetFormat' , 'f' , ), 1610678273, (1610678273, (), [ (2, 0, None, None) , ], 1 , 1 , 4 , 0 , 32 , (3, 0, None, None) , 0 , )),
	(( 'GetFormatBinary' , ), 1610678274, (1610678274, (), [ ], 1 , 1 , 4 , 0 , 40 , (3, 0, None, None) , 0 , )),
	(( 'SetFormatBinary' , 'direction' , ), 1610678275, (1610678275, (), [ (3, 0, None, None) , ], 1 , 1 , 4 , 0 , 48 , (3, 0, None, None) , 0 , )),
	(( 'GetTopolgyIncluded' , ), 1610678276, (1610678276, (), [ ], 1 , 1 , 4 , 0 , 56 , (3, 0, None, None) , 0 , )),
	(( 'SetTopolgyIncluded' , 'direction' , ), 1610678277, (1610678277, (), [ (3, 0, None, None) , ], 1 , 1 , 4 , 0 , 64 , (3, 0, None, None) , 0 , )),
	(( 'Init' , ), 1610678278, (1610678278, (), [ ], 1 , 1 , 4 , 0 , 72 , (3, 0, None, None) , 0 , )),
	(( 'GetObjectsOptions' , 'option' , ), 1610678279, (1610678279, (), [ (3, 0, None, None) , ], 1 , 1 , 4 , 0 , 80 , (3, 0, None, None) , 0 , )),
	(( 'SetObjectsOptions' , 'option' , 'set' , ), 1610678280, (1610678280, (), [ (3, 0, None, None) , 
			 (3, 0, None, None) , ], 1 , 1 , 4 , 0 , 88 , (3, 0, None, None) , 0 , )),
	(( 'GetTextExportForm' , ), 1610678281, (1610678281, (), [ ], 1 , 1 , 4 , 0 , 96 , (3, 0, None, None) , 0 , )),
	(( 'SetTextExportForm' , 'set' , ), 1610678282, (1610678282, (), [ (3, 0, None, None) , ], 1 , 1 , 4 , 0 , 104 , (3, 0, None, None) , 0 , )),
	(( 'GetCreateLocalComponents' , ), 1610678283, (1610678283, (), [ ], 1 , 1 , 4 , 0 , 112 , (3, 0, None, None) , 0 , )),
	(( 'SetCreateLocalComponents' , 'set' , ), 1610678284, (1610678284, (), [ (3, 0, None, None) , ], 1 , 1 , 4 , 0 , 120 , (3, 0, None, None) , 0 , )),
	(( 'GetPlacement' , ), 1610678285, (1610678285, (), [ ], 1 , 1 , 4 , 0 , 128 , (13, 0, None, IID('{7AA0E540-0310-11D4-A30E-00C026EE094F}')) , 0 , )),
	(( 'SetPlacement' , 'p' , ), 1610678286, (1610678286, (), [ (13, 0, None, "IID('{7AA0E540-0310-11D4-A30E-00C026EE094F}')") , ], 1 , 1 , 4 , 0 , 136 , (3, 0, None, None) , 0 , )),
	(( 'GetStepType' , ), 1610678287, (1610678287, (), [ ], 1 , 1 , 4 , 0 , 144 , (3, 0, None, None) , 0 , )),
	(( 'SetStepType' , 'set' , ), 1610678288, (1610678288, (), [ (3, 0, None, None) , ], 1 , 1 , 4 , 0 , 152 , (3, 0, None, None) , 0 , )),
	(( 'GetStep' , ), 1610678289, (1610678289, (), [ ], 1 , 1 , 4 , 0 , 160 , (5, 0, None, None) , 0 , )),
	(( 'SetStep' , 'set' , ), 1610678290, (1610678290, (), [ (5, 0, None, None) , ], 1 , 1 , 4 , 0 , 168 , (3, 0, None, None) , 0 , )),
	(( 'GetAngle' , ), 1610678291, (1610678291, (), [ ], 1 , 1 , 4 , 0 , 176 , (5, 0, None, None) , 0 , )),
	(( 'SetAngle' , 'set' , ), 1610678292, (1610678292, (), [ (5, 0, None, None) , ], 1 , 1 , 4 , 0 , 184 , (3, 0, None, None) , 0 , )),
	(( 'GetLength' , ), 1610678293, (1610678293, (), [ ], 1 , 1 , 4 , 0 , 192 , (5, 0, None, None) , 0 , )),
	(( 'SetLength' , 'set' , ), 1610678294, (1610678294, (), [ (5, 0, None, None) , ], 1 , 1 , 4 , 0 , 200 , (3, 0, None, None) , 0 , )),
	(( 'GetMaxTeselationCellCount' , ), 1610678295, (1610678295, (), [ ], 1 , 1 , 4 , 0 , 208 , (3, 0, None, None) , 0 , )),
	(( 'SetMaxTeselationCellCount' , 'set' , ), 1610678296, (1610678296, (), [ (3, 0, None, None) , ], 1 , 1 , 4 , 0 , 216 , (3, 0, None, None) , 0 , )),
	(( 'GetLengthUnits' , ), 1610678297, (1610678297, (), [ ], 1 , 1 , 4 , 0 , 224 , (3, 0, None, None) , 0 , )),
	(( 'SetLengthUnits' , 'set' , ), 1610678298, (1610678298, (), [ (3, 0, None, None) , ], 1 , 1 , 4 , 0 , 232 , (3, 0, None, None) , 0 , )),
	(( 'GetStitchSurfaces' , ), 1610678299, (1610678299, (), [ ], 1 , 1 , 4 , 0 , 240 , (3, 0, None, None) , 0 , )),
	(( 'SetStitchSurfaces' , 'set' , ), 1610678300, (1610678300, (), [ (3, 0, None, None) , ], 1 , 1 , 4 , 0 , 248 , (3, 0, None, None) , 0 , )),
	(( 'GetStitchPrecision' , ), 1610678301, (1610678301, (), [ ], 1 , 1 , 4 , 0 , 256 , (5, 0, None, None) , 0 , )),
	(( 'SetStitchPrecision' , 'set' , ), 1610678302, (1610678302, (), [ (5, 0, None, None) , ], 1 , 1 , 4 , 0 , 264 , (3, 0, None, None) , 0 , )),
	(( 'GetAuthor' , ), 1610678303, (1610678303, (), [ ], 1 , 1 , 4 , 0 , 272 , (31, 0, None, None) , 0 , )),
	(( 'SetAuthor' , 'val' , ), 1610678304, (1610678304, (), [ (31, 0, None, None) , ], 1 , 1 , 4 , 0 , 280 , (3, 0, None, None) , 0 , )),
	(( 'GetOrganization' , ), 1610678305, (1610678305, (), [ ], 1 , 1 , 4 , 0 , 288 , (31, 0, None, None) , 0 , )),
	(( 'SetOrganization' , 'val' , ), 1610678306, (1610678306, (), [ (31, 0, None, None) , ], 1 , 1 , 4 , 0 , 296 , (3, 0, None, None) , 0 , )),
	(( 'GetComment' , ), 1610678307, (1610678307, (), [ ], 1 , 1 , 4 , 0 , 304 , (31, 0, None, None) , 0 , )),
	(( 'SetComment' , 'val' , ), 1610678308, (1610678308, (), [ (31, 0, None, None) , ], 1 , 1 , 4 , 0 , 312 , (3, 0, None, None) , 0 , )),
	(( 'GetPassword' , ), 1610678309, (1610678309, (), [ ], 1 , 1 , 4 , 0 , 320 , (31, 0, None, None) , 0 , )),
	(( 'SetPassword' , 'val' , ), 1610678310, (1610678310, (), [ (31, 0, None, None) , ], 1 , 1 , 4 , 0 , 328 , (3, 0, None, None) , 0 , )),
	(( 'GetNeedCreateComponentsFiles' , ), 1610678311, (1610678311, (), [ ], 1 , 1 , 4 , 0 , 336 , (3, 0, None, None) , 0 , )),
	(( 'SetNeedCreateComponentsFiles' , 'set' , ), 1610678312, (1610678312, (), [ (3, 0, None, None) , ], 1 , 1 , 4 , 0 , 344 , (3, 0, None, None) , 0 , )),
	(( 'GetSaveResultDocument' , ), 1610678313, (1610678313, (), [ ], 1 , 1 , 4 , 0 , 352 , (3, 0, None, None) , 0 , )),
	(( 'SetSaveResultDocument' , 'set' , ), 1610678314, (1610678314, (), [ (3, 0, None, None) , ], 1 , 1 , 4 , 0 , 360 , (3, 0, None, None) , 0 , )),
]

IAggregateDefinition_vtables_dispatch_ = 0
IAggregateDefinition_vtables_ = [
	(( 'SetBooleanType' , 'val' , ), 1610678272, (1610678272, (), [ (3, 0, None, None) , ], 1 , 1 , 4 , 0 , 24 , (3, 0, None, None) , 0 , )),
	(( 'GetBooleanType' , ), 1610678273, (1610678273, (), [ ], 1 , 1 , 4 , 0 , 32 , (3, 0, None, None) , 0 , )),
	(( 'BodyCollection' , ), 1610678274, (1610678274, (), [ ], 1 , 1 , 4 , 0 , 40 , (13, 0, None, IID('{64CBC7CB-005D-47DF-8B3E-53FD974C5A32}')) , 0 , )),
]

IArc3dParam_vtables_dispatch_ = 0
IArc3dParam_vtables_ = [
	(( 'GetPlacement' , ), 1610678272, (1610678272, (), [ ], 1 , 1 , 4 , 0 , 24 , (13, 0, None, IID('{7AA0E540-0310-11D4-A30E-00C026EE094F}')) , 0 , )),
	(( 'GetRadius' , ), 1610678273, (1610678273, (), [ ], 1 , 1 , 4 , 0 , 32 , (5, 0, None, None) , 0 , )),
	(( 'GetAngle' , ), 1610678274, (1610678274, (), [ ], 1 , 1 , 4 , 0 , 40 , (5, 0, None, None) , 0 , )),
]

IAttribute3D_vtables_dispatch_ = 0
IAttribute3D_vtables_ = [
	(( 'GetReference' , ), 1610678272, (1610678272, (), [ ], 1 , 1 , 4 , 0 , 24 , (3, 0, None, None) , 0 , )),
	(( 'FeatureCollection' , 'objType' , ), 1610678273, (1610678273, (), [ (3, 0, None, None) , ], 1 , 1 , 4 , 0 , 32 , (13, 0, None, IID('{CE5D4888-9006-43AC-9ACC-6D9E58B408B4}')) , 0 , )),
	(( 'GetNameType' , ), 1610678274, (1610678274, (), [ ], 1 , 1 , 4 , 0 , 40 , (31, 0, None, None) , 0 , )),
]

IAttribute3DCollection_vtables_dispatch_ = 0
IAttribute3DCollection_vtables_ = [
	(( 'Refresh' , ), 1610678272, (1610678272, (), [ ], 1 , 1 , 4 , 0 , 24 , (3, 0, None, None) , 0 , )),
	(( 'GetCount' , ), 1610678273, (1610678273, (), [ ], 1 , 1 , 4 , 0 , 32 , (3, 0, None, None) , 0 , )),
	(( 'First' , ), 1610678274, (1610678274, (), [ ], 1 , 1 , 4 , 0 , 40 , (13, 0, None, IID('{F5529801-EDF2-42AE-B0A4-8AB6F5650AE1}')) , 0 , )),
	(( 'Last' , ), 1610678275, (1610678275, (), [ ], 1 , 1 , 4 , 0 , 48 , (13, 0, None, IID('{F5529801-EDF2-42AE-B0A4-8AB6F5650AE1}')) , 0 , )),
	(( 'Next' , ), 1610678276, (1610678276, (), [ ], 1 , 1 , 4 , 0 , 56 , (13, 0, None, IID('{F5529801-EDF2-42AE-B0A4-8AB6F5650AE1}')) , 0 , )),
	(( 'Prev' , ), 1610678277, (1610678277, (), [ ], 1 , 1 , 4 , 0 , 64 , (13, 0, None, IID('{F5529801-EDF2-42AE-B0A4-8AB6F5650AE1}')) , 0 , )),
	(( 'GetByIndex' , 'index' , ), 1610678278, (1610678278, (), [ (3, 0, None, None) , ], 1 , 1 , 4 , 0 , 72 , (13, 0, None, IID('{F5529801-EDF2-42AE-B0A4-8AB6F5650AE1}')) , 0 , )),
	(( 'FindIt' , 'obj' , ), 1610678279, (1610678279, (), [ (13, 0, None, "IID('{F5529801-EDF2-42AE-B0A4-8AB6F5650AE1}')") , ], 1 , 1 , 4 , 0 , 80 , (19, 0, None, None) , 0 , )),
	(( 'Select' , 'key1' , 'key2' , 'key3' , 'key4' , 
			 'numb' , 'objType' , ), 1610678280, (1610678280, (), [ (3, 0, None, None) , (3, 0, None, None) , 
			 (3, 0, None, None) , (3, 0, None, None) , (5, 0, None, None) , (3, 0, None, None) , ], 1 , 1 , 4 , 0 , 88 , (3, 0, None, None) , 0 , )),
]

IAxis2PlanesDefinition_vtables_dispatch_ = 0
IAxis2PlanesDefinition_vtables_ = [
	(( 'GetPlane' , 'number' , ), 1610678272, (1610678272, (), [ (3, 0, None, None) , ], 1 , 1 , 4 , 0 , 24 , (13, 0, None, IID('{7AA0E540-0301-11D4-A30E-00C026EE094F}')) , 0 , )),
	(( 'SetPlane' , 'number' , 'plane' , ), 1610678273, (1610678273, (), [ (3, 0, None, None) , 
			 (13, 0, None, "IID('{7AA0E540-0301-11D4-A30E-00C026EE094F}')") , ], 1 , 1 , 4 , 0 , 32 , (3, 0, None, None) , 0 , )),
	(( 'GetCurve3D' , ), 1610678274, (1610678274, (), [ ], 1 , 1 , 4 , 0 , 40 , (13, 0, None, IID('{E5066490-773D-4289-A60B-2FC19865174A}')) , 0 , )),
]

IAxis2PointsDefinition_vtables_dispatch_ = 0
IAxis2PointsDefinition_vtables_ = [
	(( 'GetPoint' , 'number' , ), 1610678272, (1610678272, (), [ (3, 0, None, None) , ], 1 , 1 , 4 , 0 , 24 , (13, 0, None, IID('{7AA0E540-0301-11D4-A30E-00C026EE094F}')) , 0 , )),
	(( 'SetPoint' , 'number' , 'val' , ), 1610678273, (1610678273, (), [ (3, 0, None, None) , 
			 (13, 0, None, "IID('{7AA0E540-0301-11D4-A30E-00C026EE094F}')") , ], 1 , 1 , 4 , 0 , 32 , (3, 0, None, None) , 0 , )),
	(( 'GetCurve3D' , ), 1610678274, (1610678274, (), [ ], 1 , 1 , 4 , 0 , 40 , (13, 0, None, IID('{E5066490-773D-4289-A60B-2FC19865174A}')) , 0 , )),
]

IAxisConefaceDefinition_vtables_dispatch_ = 0
IAxisConefaceDefinition_vtables_ = [
	(( 'GetFace' , ), 1610678272, (1610678272, (), [ ], 1 , 1 , 4 , 0 , 24 , (13, 0, None, IID('{7AA0E540-0301-11D4-A30E-00C026EE094F}')) , 0 , )),
	(( 'SetFace' , 'val' , ), 1610678273, (1610678273, (), [ (13, 0, None, "IID('{7AA0E540-0301-11D4-A30E-00C026EE094F}')") , ], 1 , 1 , 4 , 0 , 32 , (3, 0, None, None) , 0 , )),
	(( 'GetCurve3D' , ), 1610678274, (1610678274, (), [ ], 1 , 1 , 4 , 0 , 40 , (13, 0, None, IID('{E5066490-773D-4289-A60B-2FC19865174A}')) , 0 , )),
]

IAxisEdgeDefinition_vtables_dispatch_ = 0
IAxisEdgeDefinition_vtables_ = [
	(( 'GetEdge' , ), 1610678272, (1610678272, (), [ ], 1 , 1 , 4 , 0 , 24 , (13, 0, None, IID('{7AA0E540-0301-11D4-A30E-00C026EE094F}')) , 0 , )),
	(( 'SetEdge' , 'val' , ), 1610678273, (1610678273, (), [ (13, 0, None, "IID('{7AA0E540-0301-11D4-A30E-00C026EE094F}')") , ], 1 , 1 , 4 , 0 , 32 , (3, 0, None, None) , 0 , )),
	(( 'GetCurve3D' , ), 1610678274, (1610678274, (), [ ], 1 , 1 , 4 , 0 , 40 , (13, 0, None, IID('{E5066490-773D-4289-A60B-2FC19865174A}')) , 0 , )),
]

IAxisOperationsDefinition_vtables_dispatch_ = 0
IAxisOperationsDefinition_vtables_ = [
	(( 'GetOperation' , ), 1610678272, (1610678272, (), [ ], 1 , 1 , 4 , 0 , 24 , (13, 0, None, IID('{7AA0E540-0301-11D4-A30E-00C026EE094F}')) , 0 , )),
	(( 'SetOperation' , 'val' , ), 1610678273, (1610678273, (), [ (13, 0, None, "IID('{7AA0E540-0301-11D4-A30E-00C026EE094F}')") , ], 1 , 1 , 4 , 0 , 32 , (3, 0, None, None) , 0 , )),
	(( 'GetCurve3D' , ), 1610678274, (1610678274, (), [ ], 1 , 1 , 4 , 0 , 40 , (13, 0, None, IID('{E5066490-773D-4289-A60B-2FC19865174A}')) , 0 , )),
]

IBaseEvolutionDefinition_vtables_dispatch_ = 0
IBaseEvolutionDefinition_vtables_ = [
	(( 'SetSketch' , 'sketch' , ), 1610678272, (1610678272, (), [ (13, 0, None, "IID('{7AA0E540-0301-11D4-A30E-00C026EE094F}')") , ], 1 , 1 , 4 , 0 , 24 , (3, 0, None, None) , 0 , )),
	(( 'GetSketch' , ), 1610678273, (1610678273, (), [ ], 1 , 1 , 4 , 0 , 32 , (13, 0, None, IID('{7AA0E540-0301-11D4-A30E-00C026EE094F}')) , 0 , )),
	(( 'PathPartArray' , ), 1610678274, (1610678274, (), [ ], 1 , 1 , 4 , 0 , 40 , (13, 0, None, IID('{7AA0E540-0303-11D4-A30E-00C026EE094F}')) , 0 , )),
	(( 'GetSketchShiftType' , ), 1610678275, (1610678275, (), [ ], 1 , 1 , 4 , 0 , 48 , (2, 0, None, None) , 0 , )),
	(( 'SetSketchShiftType' , 's' , ), 1610678276, (1610678276, (), [ (2, 0, None, None) , ], 1 , 1 , 4 , 0 , 56 , (3, 0, None, None) , 0 , )),
	(( 'GetThinParam' , 'thin' , 'thinType' , 'normalThickness' , 'reverseThickness' , 
			 ), 1610678277, (1610678277, (), [ (16387, 0, None, None) , (16401, 0, None, None) , (16389, 0, None, None) , (16389, 0, None, None) , ], 1 , 1 , 4 , 0 , 64 , (3, 0, None, None) , 0 , )),
	(( 'SetThinParam' , 'thin' , 'thinType' , 'normalThickness' , 'reverseThickness' , 
			 ), 1610678278, (1610678278, (), [ (3, 0, None, None) , (17, 0, None, None) , (5, 0, None, None) , (5, 0, None, None) , ], 1 , 1 , 4 , 0 , 72 , (24, 0, None, None) , 0 , )),
	(( 'ThinParam' , ), 1610678279, (1610678279, (), [ ], 1 , 1 , 4 , 0 , 80 , (13, 0, None, IID('{7AA0E540-0306-11D4-A30E-00C026EE094F}')) , 0 , )),
	(( 'GetPathLength' , 'bitVector' , ), 1610678280, (1610678280, (), [ (19, 0, None, None) , ], 1 , 1 , 4 , 0 , 88 , (5, 0, None, None) , 0 , )),
]

IBaseExtrusionDefinition_vtables_dispatch_ = 0
IBaseExtrusionDefinition_vtables_ = [
	(( 'SetSketch' , 'name' , ), 1610678272, (1610678272, (), [ (13, 0, None, "IID('{7AA0E540-0301-11D4-A30E-00C026EE094F}')") , ], 1 , 1 , 4 , 0 , 24 , (3, 0, None, None) , 0 , )),
	(( 'GetSketch' , ), 1610678273, (1610678273, (), [ ], 1 , 1 , 4 , 0 , 32 , (13, 0, None, IID('{7AA0E540-0301-11D4-A30E-00C026EE094F}')) , 0 , )),
	(( 'GetSideParam' , 'forward' , 'type' , 'depth' , 'draftValue' , 
			 'draftOutward' , ), 1610678274, (1610678274, (), [ (3, 0, None, None) , (16401, 0, None, None) , (16389, 0, None, None) , 
			 (16389, 0, None, None) , (16387, 0, None, None) , ], 1 , 1 , 4 , 0 , 40 , (3, 0, None, None) , 0 , )),
	(( 'SetSideParam' , 'forward' , 'type' , 'depth' , 'draftValue' , 
			 'draftOutward' , ), 1610678275, (1610678275, (), [ (3, 0, None, None) , (17, 0, None, None) , (5, 0, None, None) , 
			 (5, 0, None, None) , (3, 0, None, None) , ], 1 , 1 , 4 , 0 , 48 , (24, 0, None, None) , 0 , )),
	(( 'GetThinParam' , 'thin' , 'thinType' , 'normalThickness' , 'reverseThickness' , 
			 ), 1610678276, (1610678276, (), [ (16387, 0, None, None) , (16401, 0, None, None) , (16389, 0, None, None) , (16389, 0, None, None) , ], 1 , 1 , 4 , 0 , 56 , (3, 0, None, None) , 0 , )),
	(( 'SetThinParam' , 'thin' , 'thinType' , 'normalThickness' , 'reverseThickness' , 
			 ), 1610678277, (1610678277, (), [ (3, 0, None, None) , (17, 0, None, None) , (5, 0, None, None) , (5, 0, None, None) , ], 1 , 1 , 4 , 0 , 64 , (24, 0, None, None) , 0 , )),
	(( 'SetDirectionType' , 'dirType' , ), 1610678278, (1610678278, (), [ (3, 0, None, None) , ], 1 , 1 , 4 , 0 , 72 , (3, 0, None, None) , 0 , )),
	(( 'GetDirectionType' , ), 1610678279, (1610678279, (), [ ], 1 , 1 , 4 , 0 , 80 , (3, 0, None, None) , 0 , )),
	(( 'ThinParam' , ), 1610678280, (1610678280, (), [ ], 1 , 1 , 4 , 0 , 88 , (13, 0, None, IID('{7AA0E540-0306-11D4-A30E-00C026EE094F}')) , 0 , )),
	(( 'ExtrusionParam' , ), 1610678281, (1610678281, (), [ ], 1 , 1 , 4 , 0 , 96 , (13, 0, None, IID('{7AA0E540-0307-11D4-A30E-00C026EE094F}')) , 0 , )),
	(( 'GetDepthObject' , 'normal' , ), 1610678282, (1610678282, (), [ (3, 0, None, None) , ], 1 , 1 , 4 , 0 , 104 , (13, 0, None, IID('{7AA0E540-0301-11D4-A30E-00C026EE094F}')) , 0 , )),
	(( 'SetDepthObject' , 'normal' , 'obj' , ), 1610678283, (1610678283, (), [ (3, 0, None, None) , 
			 (13, 0, None, "IID('{7AA0E540-0301-11D4-A30E-00C026EE094F}')") , ], 1 , 1 , 4 , 0 , 112 , (3, 0, None, None) , 0 , )),
	(( 'ResetDepthObject' , 'normal' , ), 1610678284, (1610678284, (), [ (3, 0, None, None) , ], 1 , 1 , 4 , 0 , 120 , (3, 0, None, None) , 0 , )),
]

IBaseLoftDefinition_vtables_dispatch_ = 0
IBaseLoftDefinition_vtables_ = [
	(( 'GetLoftParam' , 'closed' , 'flipVertex' , 'autoPath' , ), 1610678272, (1610678272, (), [ 
			 (16387, 0, None, None) , (16387, 0, None, None) , (16387, 0, None, None) , ], 1 , 1 , 4 , 0 , 24 , (3, 0, None, None) , 0 , )),
	(( 'SetLoftParam' , 'closed' , 'flipVertex' , 'autoPath' , ), 1610678273, (1610678273, (), [ 
			 (3, 0, None, None) , (3, 0, None, None) , (3, 0, None, None) , ], 1 , 1 , 4 , 0 , 32 , (24, 0, None, None) , 0 , )),
	(( 'GetThinParam' , 'thin' , 'thinType' , 'normalThickness' , 'reverseThickness' , 
			 ), 1610678274, (1610678274, (), [ (16387, 0, None, None) , (16401, 0, None, None) , (16389, 0, None, None) , (16389, 0, None, None) , ], 1 , 1 , 4 , 0 , 40 , (3, 0, None, None) , 0 , )),
	(( 'SetThinParam' , 'thin' , 'thinType' , 'normalThickness' , 'reverseThickness' , 
			 ), 1610678275, (1610678275, (), [ (3, 0, None, None) , (17, 0, None, None) , (5, 0, None, None) , (5, 0, None, None) , ], 1 , 1 , 4 , 0 , 48 , (24, 0, None, None) , 0 , )),
	(( 'ThinParam' , ), 1610678276, (1610678276, (), [ ], 1 , 1 , 4 , 0 , 56 , (13, 0, None, IID('{7AA0E540-0306-11D4-A30E-00C026EE094F}')) , 0 , )),
	(( 'Sketchs' , ), 1610678277, (1610678277, (), [ ], 1 , 1 , 4 , 0 , 64 , (13, 0, None, IID('{7AA0E540-0303-11D4-A30E-00C026EE094F}')) , 0 , )),
]

IBaseRotatedDefinition_vtables_dispatch_ = 0
IBaseRotatedDefinition_vtables_ = [
	(( 'SetSketch' , 'name' , ), 1610678272, (1610678272, (), [ (13, 0, None, "IID('{7AA0E540-0301-11D4-A30E-00C026EE094F}')") , ], 1 , 1 , 4 , 0 , 24 , (3, 0, None, None) , 0 , )),
	(( 'GetSketch' , ), 1610678273, (1610678273, (), [ ], 1 , 1 , 4 , 0 , 32 , (13, 0, None, IID('{7AA0E540-0301-11D4-A30E-00C026EE094F}')) , 0 , )),
	(( 'GetSideParam' , 'forward' , 'angle' , ), 1610678274, (1610678274, (), [ (3, 0, None, None) , 
			 (16389, 0, None, None) , ], 1 , 1 , 4 , 0 , 40 , (3, 0, None, None) , 0 , )),
	(( 'SetSideParam' , 'forward' , 'angle' , ), 1610678275, (1610678275, (), [ (3, 0, None, None) , 
			 (5, 0, None, None) , ], 1 , 1 , 4 , 0 , 48 , (24, 0, None, None) , 0 , )),
	(( 'GetThinParam' , 'thin' , 'thinType' , 'normalThickness' , 'reverseThickness' , 
			 ), 1610678276, (1610678276, (), [ (16387, 0, None, None) , (16401, 0, None, None) , (16389, 0, None, None) , (16389, 0, None, None) , ], 1 , 1 , 4 , 0 , 56 , (3, 0, None, None) , 0 , )),
	(( 'SetThinParam' , 'thin' , 'thinType' , 'normalThickness' , 'reverseThickness' , 
			 ), 1610678277, (1610678277, (), [ (3, 0, None, None) , (17, 0, None, None) , (5, 0, None, None) , (5, 0, None, None) , ], 1 , 1 , 4 , 0 , 64 , (24, 0, None, None) , 0 , )),
	(( 'SetDirectionType' , 'dirType' , ), 1610678278, (1610678278, (), [ (3, 0, None, None) , ], 1 , 1 , 4 , 0 , 72 , (3, 0, None, None) , 0 , )),
	(( 'GetDirectionType' , ), 1610678279, (1610678279, (), [ ], 1 , 1 , 4 , 0 , 80 , (3, 0, None, None) , 0 , )),
	(( 'SetToroidShapeType' , 'dirType' , ), 1610678280, (1610678280, (), [ (3, 0, None, None) , ], 1 , 1 , 4 , 0 , 88 , (3, 0, None, None) , 0 , )),
	(( 'GetToroidShapeType' , ), 1610678281, (1610678281, (), [ ], 1 , 1 , 4 , 0 , 96 , (3, 0, None, None) , 0 , )),
	(( 'ThinParam' , ), 1610678282, (1610678282, (), [ ], 1 , 1 , 4 , 0 , 104 , (13, 0, None, IID('{7AA0E540-0306-11D4-A30E-00C026EE094F}')) , 0 , )),
	(( 'RotatedParam' , ), 1610678283, (1610678283, (), [ ], 1 , 1 , 4 , 0 , 112 , (13, 0, None, IID('{7AA0E540-0308-11D4-A30E-00C026EE094F}')) , 0 , )),
]

IBody_vtables_dispatch_ = 0
IBody_vtables_ = [
	(( 'GetGabarit' , 'x1' , 'y1' , 'z1' , 'x2' , 
			 'y2' , 'z2' , ), 1610678272, (1610678272, (), [ (16389, 0, None, None) , (16389, 0, None, None) , 
			 (16389, 0, None, None) , (16389, 0, None, None) , (16389, 0, None, None) , (16389, 0, None, None) , ], 1 , 1 , 4 , 0 , 24 , (3, 0, None, None) , 0 , )),
	(( 'FaceCollection' , ), 1610678273, (1610678273, (), [ ], 1 , 1 , 4 , 0 , 32 , (13, 0, None, IID('{D269AD47-B2CC-4152-A7BA-127242371208}')) , 0 , )),
	(( 'IsSolid' , ), 1610678274, (1610678274, (), [ ], 1 , 1 , 4 , 0 , 40 , (3, 0, None, None) , 0 , )),
	(( 'CalcMassInertiaProperties' , 'bitVector' , ), 1610678275, (1610678275, (), [ (19, 0, None, None) , ], 1 , 1 , 4 , 0 , 48 , (13, 0, None, IID('{74E97440-88A5-4D29-9543-59D775BC9A13}')) , 0 , )),
	(( 'CurveIntersection' , 'curve' , 'faces' , 'points' , ), 1610678276, (1610678276, (), [ 
			 (13, 0, None, "IID('{E5066490-773D-4289-A60B-2FC19865174A}')") , (13, 0, None, "IID('{D269AD47-B2CC-4152-A7BA-127242371208}')") , (13, 0, None, "IID('{A5E6E83E-1F33-4EAF-BAFC-A3F434F23BAA}')") , ], 1 , 1 , 4 , 0 , 56 , (3, 0, None, None) , 0 , )),
	(( 'CheckIntersectionWithBody' , 'otherBody' , 'checkTangent' , ), 1610678277, (1610678277, (), [ (13, 0, None, "IID('{BE70EEE5-1767-483E-9D18-79BCEC5AB837}')") , 
			 (3, 0, None, None) , ], 1 , 1 , 4 , 0 , 64 , (13, 0, None, IID('{66CBDD80-332C-40B5-9968-DD902EBAB55D}')) , 0 , )),
	(( 'GetMultiBodyParts' , ), 1610678278, (1610678278, (), [ ], 1 , 1 , 4 , 0 , 72 , (3, 0, None, None) , 0 , )),
	(( 'GetFeature' , ), 1610678279, (1610678279, (), [ ], 1 , 1 , 4 , 0 , 80 , (13, 0, None, IID('{1D15245B-695E-4F9F-AFCA-EACBC3A055BB}')) , 0 , )),
	(( 'GetIntersectionFacesWithBody' , 'otherBody' , 'intersectionFaces1' , 'intersectionFaces2' , 'connectedFaces1' , 
			 'connectedFaces2' , ), 1610678280, (1610678280, (), [ (13, 1, None, "IID('{BE70EEE5-1767-483E-9D18-79BCEC5AB837}')") , (16396, 3, None, None) , (16396, 3, None, None) , 
			 (16396, 3, None, None) , (16396, 3, None, None) , ], 1 , 1 , 4 , 0 , 88 , (3, 0, None, None) , 0 , )),
]

IBodyCollection_vtables_dispatch_ = 0
IBodyCollection_vtables_ = [
	(( 'Refresh' , ), 1610678272, (1610678272, (), [ ], 1 , 1 , 4 , 0 , 24 , (3, 0, None, None) , 0 , )),
	(( 'GetCount' , ), 1610678273, (1610678273, (), [ ], 1 , 1 , 4 , 0 , 32 , (3, 0, None, None) , 0 , )),
	(( 'First' , ), 1610678274, (1610678274, (), [ ], 1 , 1 , 4 , 0 , 40 , (13, 0, None, IID('{BE70EEE5-1767-483E-9D18-79BCEC5AB837}')) , 0 , )),
	(( 'Last' , ), 1610678275, (1610678275, (), [ ], 1 , 1 , 4 , 0 , 48 , (13, 0, None, IID('{BE70EEE5-1767-483E-9D18-79BCEC5AB837}')) , 0 , )),
	(( 'Next' , ), 1610678276, (1610678276, (), [ ], 1 , 1 , 4 , 0 , 56 , (13, 0, None, IID('{BE70EEE5-1767-483E-9D18-79BCEC5AB837}')) , 0 , )),
	(( 'Prev' , ), 1610678277, (1610678277, (), [ ], 1 , 1 , 4 , 0 , 64 , (13, 0, None, IID('{BE70EEE5-1767-483E-9D18-79BCEC5AB837}')) , 0 , )),
	(( 'GetByIndex' , 'index' , ), 1610678278, (1610678278, (), [ (3, 0, None, None) , ], 1 , 1 , 4 , 0 , 72 , (13, 0, None, IID('{BE70EEE5-1767-483E-9D18-79BCEC5AB837}')) , 0 , )),
	(( 'FindIt' , 'entity' , ), 1610678279, (1610678279, (), [ (13, 0, None, "IID('{BE70EEE5-1767-483E-9D18-79BCEC5AB837}')") , ], 1 , 1 , 4 , 0 , 80 , (19, 0, None, None) , 0 , )),
	(( 'Clear' , ), 1610678280, (1610678280, (), [ ], 1 , 1 , 4 , 0 , 88 , (3, 0, None, None) , 0 , )),
	(( 'Add' , 'entity' , ), 1610678281, (1610678281, (), [ (13, 0, None, "IID('{BE70EEE5-1767-483E-9D18-79BCEC5AB837}')") , ], 1 , 1 , 4 , 0 , 96 , (3, 0, None, None) , 0 , )),
	(( 'AddAt' , 'entity' , 'index' , ), 1610678282, (1610678282, (), [ (13, 0, None, "IID('{BE70EEE5-1767-483E-9D18-79BCEC5AB837}')") , 
			 (3, 0, None, None) , ], 1 , 1 , 4 , 0 , 104 , (3, 0, None, None) , 0 , )),
	(( 'AddBefore' , 'entity' , 'base' , ), 1610678283, (1610678283, (), [ (13, 0, None, "IID('{BE70EEE5-1767-483E-9D18-79BCEC5AB837}')") , 
			 (13, 0, None, "IID('{BE70EEE5-1767-483E-9D18-79BCEC5AB837}')") , ], 1 , 1 , 4 , 0 , 112 , (3, 0, None, None) , 0 , )),
	(( 'DetachByIndex' , 'index' , ), 1610678284, (1610678284, (), [ (3, 0, None, None) , ], 1 , 1 , 4 , 0 , 120 , (3, 0, None, None) , 0 , )),
	(( 'DetachByBody' , 'entity' , ), 1610678285, (1610678285, (), [ (13, 0, None, "IID('{BE70EEE5-1767-483E-9D18-79BCEC5AB837}')") , ], 1 , 1 , 4 , 0 , 128 , (3, 0, None, None) , 0 , )),
	(( 'SetByIndex' , 'entity' , 'index' , ), 1610678286, (1610678286, (), [ (13, 0, None, "IID('{BE70EEE5-1767-483E-9D18-79BCEC5AB837}')") , 
			 (3, 0, None, None) , ], 1 , 1 , 4 , 0 , 136 , (3, 0, None, None) , 0 , )),
]

IBodyParts_vtables_dispatch_ = 0
IBodyParts_vtables_ = [
	(( 'UserBodyPartsChoice' , ), 1610678272, (1610678272, (), [ ], 1 , 1 , 4 , 0 , 24 , (3, 0, None, None) , 0 , )),
	(( 'GetCount' , ), 1610678273, (1610678273, (), [ ], 1 , 1 , 4 , 0 , 32 , (3, 0, None, None) , 0 , )),
	(( 'GetAllSelected' , ), 1610678274, (1610678274, (), [ ], 1 , 1 , 4 , 0 , 40 , (3, 0, None, None) , 0 , )),
	(( 'SetAllSelected' , 'val' , ), 1610678275, (1610678275, (), [ (3, 0, None, None) , ], 1 , 1 , 4 , 0 , 48 , (3, 0, None, None) , 0 , )),
	(( 'SetPartSelected' , 'index' , 'Select' , ), 1610678276, (1610678276, (), [ (3, 0, None, None) , 
			 (3, 0, None, None) , ], 1 , 1 , 4 , 0 , 56 , (3, 0, None, None) , 0 , )),
	(( 'GetPartSelected' , 'index' , ), 1610678277, (1610678277, (), [ (3, 0, None, None) , ], 1 , 1 , 4 , 0 , 64 , (3, 0, None, None) , 0 , )),
	(( 'SetGreatPartsSelected' , ), 1610678278, (1610678278, (), [ ], 1 , 1 , 4 , 0 , 72 , (3, 0, None, None) , 0 , )),
]

IBossEvolutionDefinition_vtables_dispatch_ = 0
IBossEvolutionDefinition_vtables_ = [
	(( 'SetSketch' , 'sketch' , ), 1610678272, (1610678272, (), [ (13, 0, None, "IID('{7AA0E540-0301-11D4-A30E-00C026EE094F}')") , ], 1 , 1 , 4 , 0 , 24 , (3, 0, None, None) , 0 , )),
	(( 'GetSketch' , ), 1610678273, (1610678273, (), [ ], 1 , 1 , 4 , 0 , 32 , (13, 0, None, IID('{7AA0E540-0301-11D4-A30E-00C026EE094F}')) , 0 , )),
	(( 'PathPartArray' , ), 1610678274, (1610678274, (), [ ], 1 , 1 , 4 , 0 , 40 , (13, 0, None, IID('{7AA0E540-0303-11D4-A30E-00C026EE094F}')) , 0 , )),
	(( 'GetSketchShiftType' , ), 1610678275, (1610678275, (), [ ], 1 , 1 , 4 , 0 , 48 , (2, 0, None, None) , 0 , )),
	(( 'SetSketchShiftType' , 'sketchShiftType' , ), 1610678276, (1610678276, (), [ (2, 0, None, None) , ], 1 , 1 , 4 , 0 , 56 , (3, 0, None, None) , 0 , )),
	(( 'GetThinParam' , 'thin' , 'thinType' , 'normalThickness' , 'reverseThickness' , 
			 ), 1610678277, (1610678277, (), [ (16387, 0, None, None) , (16401, 0, None, None) , (16389, 0, None, None) , (16389, 0, None, None) , ], 1 , 1 , 4 , 0 , 64 , (3, 0, None, None) , 0 , )),
	(( 'SetThinParam' , 'thin' , 'thinType' , 'normalThickness' , 'reverseThickness' , 
			 ), 1610678278, (1610678278, (), [ (3, 0, None, None) , (17, 0, None, None) , (5, 0, None, None) , (5, 0, None, None) , ], 1 , 1 , 4 , 0 , 72 , (24, 0, None, None) , 0 , )),
	(( 'ThinParam' , ), 1610678279, (1610678279, (), [ ], 1 , 1 , 4 , 0 , 80 , (13, 0, None, IID('{7AA0E540-0306-11D4-A30E-00C026EE094F}')) , 0 , )),
	(( 'ChooseBodies' , ), 1610678280, (1610678280, (), [ ], 1 , 1 , 4 , 0 , 88 , (13, 0, None, IID('{67B417BA-F248-4B56-AD03-C4057C7F2EEE}')) , 0 , )),
	(( 'GetPathLength' , 'bitVector' , ), 1610678281, (1610678281, (), [ (19, 0, None, None) , ], 1 , 1 , 4 , 0 , 96 , (5, 0, None, None) , 0 , )),
	(( 'ChooseParts' , ), 1610678282, (1610678282, (), [ ], 1 , 1 , 4 , 0 , 104 , (13, 0, None, IID('{2920B89D-636E-4DCC-8E62-34D2F4B4BB00}')) , 0 , )),
	(( 'SetChooseType' , 'val' , ), 1610678283, (1610678283, (), [ (3, 0, None, None) , ], 1 , 1 , 4 , 0 , 112 , (3, 0, None, None) , 0 , )),
	(( 'GetChooseType' , ), 1610678284, (1610678284, (), [ ], 1 , 1 , 4 , 0 , 120 , (3, 0, None, None) , 0 , )),
]

IBossExtrusionDefinition_vtables_dispatch_ = 0
IBossExtrusionDefinition_vtables_ = [
	(( 'SetSketch' , 'name' , ), 1610678272, (1610678272, (), [ (13, 0, None, "IID('{7AA0E540-0301-11D4-A30E-00C026EE094F}')") , ], 1 , 1 , 4 , 0 , 24 , (3, 0, None, None) , 0 , )),
	(( 'GetSketch' , ), 1610678273, (1610678273, (), [ ], 1 , 1 , 4 , 0 , 32 , (13, 0, None, IID('{7AA0E540-0301-11D4-A30E-00C026EE094F}')) , 0 , )),
	(( 'GetSideParam' , 'forward' , 'type' , 'depth' , 'draftValue' , 
			 'draftOutward' , ), 1610678274, (1610678274, (), [ (3, 0, None, None) , (16401, 0, None, None) , (16389, 0, None, None) , 
			 (16389, 0, None, None) , (16387, 0, None, None) , ], 1 , 1 , 4 , 0 , 40 , (3, 0, None, None) , 0 , )),
	(( 'SetSideParam' , 'forward' , 'type' , 'depth' , 'depthToObj' , 
			 'draftOutward' , ), 1610678275, (1610678275, (), [ (3, 0, None, None) , (17, 0, None, None) , (5, 0, None, None) , 
			 (5, 0, None, None) , (3, 0, None, None) , ], 1 , 1 , 4 , 0 , 48 , (24, 0, None, None) , 0 , )),
	(( 'GetThinParam' , 'thin' , 'thinType' , 'normalThickness' , 'reverseThickness' , 
			 ), 1610678276, (1610678276, (), [ (16387, 0, None, None) , (16401, 0, None, None) , (16389, 0, None, None) , (16389, 0, None, None) , ], 1 , 1 , 4 , 0 , 56 , (3, 0, None, None) , 0 , )),
	(( 'SetThinParam' , 'thin' , 'thinType' , 'normalThickness' , 'reverseThickness' , 
			 ), 1610678277, (1610678277, (), [ (3, 0, None, None) , (17, 0, None, None) , (5, 0, None, None) , (5, 0, None, None) , ], 1 , 1 , 4 , 0 , 64 , (24, 0, None, None) , 0 , )),
	(( 'SetDirectionType' , 'dirType' , ), 1610678278, (1610678278, (), [ (3, 0, None, None) , ], 1 , 1 , 4 , 0 , 72 , (3, 0, None, None) , 0 , )),
	(( 'GetDirectionType' , ), 1610678279, (1610678279, (), [ ], 1 , 1 , 4 , 0 , 80 , (3, 0, None, None) , 0 , )),
	(( 'ThinParam' , ), 1610678280, (1610678280, (), [ ], 1 , 1 , 4 , 0 , 88 , (13, 0, None, IID('{7AA0E540-0306-11D4-A30E-00C026EE094F}')) , 0 , )),
	(( 'ExtrusionParam' , ), 1610678281, (1610678281, (), [ ], 1 , 1 , 4 , 0 , 96 , (13, 0, None, IID('{7AA0E540-0307-11D4-A30E-00C026EE094F}')) , 0 , )),
	(( 'GetDepthObject' , 'normal' , ), 1610678282, (1610678282, (), [ (3, 0, None, None) , ], 1 , 1 , 4 , 0 , 104 , (13, 0, None, IID('{7AA0E540-0301-11D4-A30E-00C026EE094F}')) , 0 , )),
	(( 'SetDepthObject' , 'normal' , 'obj' , ), 1610678283, (1610678283, (), [ (3, 0, None, None) , 
			 (13, 0, None, "IID('{7AA0E540-0301-11D4-A30E-00C026EE094F}')") , ], 1 , 1 , 4 , 0 , 112 , (3, 0, None, None) , 0 , )),
	(( 'ResetDepthObject' , 'normal' , ), 1610678284, (1610678284, (), [ (3, 0, None, None) , ], 1 , 1 , 4 , 0 , 120 , (3, 0, None, None) , 0 , )),
	(( 'ChooseBodies' , ), 1610678285, (1610678285, (), [ ], 1 , 1 , 4 , 0 , 128 , (13, 0, None, IID('{67B417BA-F248-4B56-AD03-C4057C7F2EEE}')) , 0 , )),
	(( 'ChooseParts' , ), 1610678286, (1610678286, (), [ ], 1 , 1 , 4 , 0 , 136 , (13, 0, None, IID('{2920B89D-636E-4DCC-8E62-34D2F4B4BB00}')) , 0 , )),
	(( 'SetChooseType' , 'val' , ), 1610678287, (1610678287, (), [ (3, 0, None, None) , ], 1 , 1 , 4 , 0 , 144 , (3, 0, None, None) , 0 , )),
	(( 'GetChooseType' , ), 1610678288, (1610678288, (), [ ], 1 , 1 , 4 , 0 , 152 , (3, 0, None, None) , 0 , )),
]

IBossLoftDefinition_vtables_dispatch_ = 0
IBossLoftDefinition_vtables_ = [
	(( 'GetLoftParam' , 'closed' , 'flipVertex' , 'autoPath' , ), 1610678272, (1610678272, (), [ 
			 (16387, 0, None, None) , (16387, 0, None, None) , (16387, 0, None, None) , ], 1 , 1 , 4 , 0 , 24 , (3, 0, None, None) , 0 , )),
	(( 'SetLoftParam' , 'closed' , 'flipVertex' , 'autoPath' , ), 1610678273, (1610678273, (), [ 
			 (3, 0, None, None) , (3, 0, None, None) , (3, 0, None, None) , ], 1 , 1 , 4 , 0 , 32 , (24, 0, None, None) , 0 , )),
	(( 'GetThinParam' , 'thin' , 'thinType' , 'normalThickness' , 'reverseThickness' , 
			 ), 1610678274, (1610678274, (), [ (16387, 0, None, None) , (16401, 0, None, None) , (16389, 0, None, None) , (16389, 0, None, None) , ], 1 , 1 , 4 , 0 , 40 , (3, 0, None, None) , 0 , )),
	(( 'SetThinParam' , 'thin' , 'thinType' , 'normalThickness' , 'reverseThickness' , 
			 ), 1610678275, (1610678275, (), [ (3, 0, None, None) , (17, 0, None, None) , (5, 0, None, None) , (5, 0, None, None) , ], 1 , 1 , 4 , 0 , 48 , (24, 0, None, None) , 0 , )),
	(( 'ThinParam' , ), 1610678276, (1610678276, (), [ ], 1 , 1 , 4 , 0 , 56 , (13, 0, None, IID('{7AA0E540-0306-11D4-A30E-00C026EE094F}')) , 0 , )),
	(( 'Sketchs' , ), 1610678277, (1610678277, (), [ ], 1 , 1 , 4 , 0 , 64 , (13, 0, None, IID('{7AA0E540-0303-11D4-A30E-00C026EE094F}')) , 0 , )),
	(( 'ChooseBodies' , ), 1610678278, (1610678278, (), [ ], 1 , 1 , 4 , 0 , 72 , (13, 0, None, IID('{67B417BA-F248-4B56-AD03-C4057C7F2EEE}')) , 0 , )),
	(( 'GetDirectionalLine' , ), 1610678279, (1610678279, (), [ ], 1 , 1 , 4 , 0 , 80 , (13, 0, None, IID('{7AA0E540-0301-11D4-A30E-00C026EE094F}')) , 0 , )),
	(( 'SetDirectionalLine' , 'sketch' , ), 1610678280, (1610678280, (), [ (13, 0, None, "IID('{7AA0E540-0301-11D4-A30E-00C026EE094F}')") , ], 1 , 1 , 4 , 0 , 88 , (3, 0, None, None) , 0 , )),
	(( 'ChooseParts' , ), 1610678281, (1610678281, (), [ ], 1 , 1 , 4 , 0 , 96 , (13, 0, None, IID('{2920B89D-636E-4DCC-8E62-34D2F4B4BB00}')) , 0 , )),
	(( 'SetChooseType' , 'val' , ), 1610678282, (1610678282, (), [ (3, 0, None, None) , ], 1 , 1 , 4 , 0 , 104 , (3, 0, None, None) , 0 , )),
	(( 'GetChooseType' , ), 1610678283, (1610678283, (), [ ], 1 , 1 , 4 , 0 , 112 , (3, 0, None, None) , 0 , )),
]

IBossRotatedDefinition_vtables_dispatch_ = 0
IBossRotatedDefinition_vtables_ = [
	(( 'SetSketch' , 'name' , ), 1610678272, (1610678272, (), [ (13, 0, None, "IID('{7AA0E540-0301-11D4-A30E-00C026EE094F}')") , ], 1 , 1 , 4 , 0 , 24 , (3, 0, None, None) , 0 , )),
	(( 'GetSketch' , ), 1610678273, (1610678273, (), [ ], 1 , 1 , 4 , 0 , 32 , (13, 0, None, IID('{7AA0E540-0301-11D4-A30E-00C026EE094F}')) , 0 , )),
	(( 'GetSideParam' , 'forward' , 'angle' , ), 1610678274, (1610678274, (), [ (3, 0, None, None) , 
			 (16389, 0, None, None) , ], 1 , 1 , 4 , 0 , 40 , (3, 0, None, None) , 0 , )),
	(( 'SetSideParam' , 'forward' , 'angle' , ), 1610678275, (1610678275, (), [ (3, 0, None, None) , 
			 (5, 0, None, None) , ], 1 , 1 , 4 , 0 , 48 , (24, 0, None, None) , 0 , )),
	(( 'GetThinParam' , 'thin' , 'thinType' , 'normalThickness' , 'reverseThickness' , 
			 ), 1610678276, (1610678276, (), [ (16387, 0, None, None) , (16401, 0, None, None) , (16389, 0, None, None) , (16389, 0, None, None) , ], 1 , 1 , 4 , 0 , 56 , (3, 0, None, None) , 0 , )),
	(( 'SetThinParam' , 'thin' , 'thinType' , 'normalThickness' , 'reverseThickness' , 
			 ), 1610678277, (1610678277, (), [ (3, 0, None, None) , (17, 0, None, None) , (5, 0, None, None) , (5, 0, None, None) , ], 1 , 1 , 4 , 0 , 64 , (24, 0, None, None) , 0 , )),
	(( 'SetDirectionType' , 'dirType' , ), 1610678278, (1610678278, (), [ (3, 0, None, None) , ], 1 , 1 , 4 , 0 , 72 , (3, 0, None, None) , 0 , )),
	(( 'GetDirectionType' , ), 1610678279, (1610678279, (), [ ], 1 , 1 , 4 , 0 , 80 , (3, 0, None, None) , 0 , )),
	(( 'SetToroidShapeType' , 'dirType' , ), 1610678280, (1610678280, (), [ (3, 0, None, None) , ], 1 , 1 , 4 , 0 , 88 , (3, 0, None, None) , 0 , )),
	(( 'GetToroidShapeType' , ), 1610678281, (1610678281, (), [ ], 1 , 1 , 4 , 0 , 96 , (3, 0, None, None) , 0 , )),
	(( 'ThinParam' , ), 1610678282, (1610678282, (), [ ], 1 , 1 , 4 , 0 , 104 , (13, 0, None, IID('{7AA0E540-0306-11D4-A30E-00C026EE094F}')) , 0 , )),
	(( 'RotatedParam' , ), 1610678283, (1610678283, (), [ ], 1 , 1 , 4 , 0 , 112 , (13, 0, None, IID('{7AA0E540-0308-11D4-A30E-00C026EE094F}')) , 0 , )),
	(( 'ChooseBodies' , ), 1610678284, (1610678284, (), [ ], 1 , 1 , 4 , 0 , 120 , (13, 0, None, IID('{67B417BA-F248-4B56-AD03-C4057C7F2EEE}')) , 0 , )),
	(( 'ChooseParts' , ), 1610678285, (1610678285, (), [ ], 1 , 1 , 4 , 0 , 128 , (13, 0, None, IID('{2920B89D-636E-4DCC-8E62-34D2F4B4BB00}')) , 0 , )),
	(( 'SetChooseType' , 'val' , ), 1610678286, (1610678286, (), [ (3, 0, None, None) , ], 1 , 1 , 4 , 0 , 136 , (3, 0, None, None) , 0 , )),
	(( 'GetChooseType' , ), 1610678287, (1610678287, (), [ ], 1 , 1 , 4 , 0 , 144 , (3, 0, None, None) , 0 , )),
]

IChamferDefinition_vtables_dispatch_ = 0
IChamferDefinition_vtables_ = [
	(( 'GetChamferParam' , 'transfer' , 'distance1' , 'distance2' , ), 1610678272, (1610678272, (), [ 
			 (16387, 0, None, None) , (16389, 0, None, None) , (16389, 0, None, None) , ], 1 , 1 , 4 , 0 , 24 , (3, 0, None, None) , 0 , )),
	(( 'SetChamferParam' , 'transfer' , 'distance1' , 'distance2' , ), 1610678273, (1610678273, (), [ 
			 (3, 0, None, None) , (5, 0, None, None) , (5, 0, None, None) , ], 1 , 1 , 4 , 0 , 32 , (24, 0, None, None) , 0 , )),
	(( 'GetTangent' , ), 1610678274, (1610678274, (), [ ], 1 , 1 , 4 , 0 , 40 , (3, 0, None, None) , 0 , )),
	(( 'SetTangent' , 'val' , ), 1610678275, (1610678275, (), [ (3, 0, None, None) , ], 1 , 1 , 4 , 0 , 48 , (24, 0, None, None) , 0 , )),
	(( 'Array' , ), 1610678276, (1610678276, (), [ ], 1 , 1 , 4 , 0 , 56 , (13, 0, None, IID('{7AA0E540-0303-11D4-A30E-00C026EE094F}')) , 0 , )),
]

IChooseBodies_vtables_dispatch_ = 0
IChooseBodies_vtables_ = [
	(( 'SetChooseBodiesType' , 'val' , ), 1610678272, (1610678272, (), [ (3, 0, None, None) , ], 1 , 1 , 4 , 0 , 24 , (3, 0, None, None) , 0 , )),
	(( 'GetChooseBodiesType' , ), 1610678273, (1610678273, (), [ ], 1 , 1 , 4 , 0 , 32 , (3, 0, None, None) , 0 , )),
	(( 'BodyCollection' , ), 1610678274, (1610678274, (), [ ], 1 , 1 , 4 , 0 , 40 , (13, 0, None, IID('{64CBC7CB-005D-47DF-8B3E-53FD974C5A32}')) , 0 , )),
]

IChooseMng_vtables_dispatch_ = 0
IChooseMng_vtables_ = [
	(( 'Choose' , 'obj' , ), 1610678272, (1610678272, (), [ (13, 0, None, None) , ], 1 , 1 , 4 , 0 , 24 , (3, 0, None, None) , 0 , )),
	(( 'UnChoose' , 'obj' , ), 1610678273, (1610678273, (), [ (13, 0, None, None) , ], 1 , 1 , 4 , 0 , 32 , (3, 0, None, None) , 0 , )),
	(( 'UnChooseAll' , ), 1610678274, (1610678274, (), [ ], 1 , 1 , 4 , 0 , 40 , (3, 0, None, None) , 0 , )),
	(( 'IsChoosen' , 'obj' , ), 1610678275, (1610678275, (), [ (13, 0, None, None) , ], 1 , 1 , 4 , 0 , 48 , (3, 0, None, None) , 0 , )),
	(( 'GetCount' , ), 1610678276, (1610678276, (), [ ], 1 , 1 , 4 , 0 , 56 , (3, 0, None, None) , 0 , )),
	(( 'First' , ), 1610678277, (1610678277, (), [ ], 1 , 1 , 4 , 0 , 64 , (13, 0, None, None) , 0 , )),
	(( 'Last' , ), 1610678278, (1610678278, (), [ ], 1 , 1 , 4 , 0 , 72 , (13, 0, None, None) , 0 , )),
	(( 'Next' , ), 1610678279, (1610678279, (), [ ], 1 , 1 , 4 , 0 , 80 , (13, 0, None, None) , 0 , )),
	(( 'Prev' , ), 1610678280, (1610678280, (), [ ], 1 , 1 , 4 , 0 , 88 , (13, 0, None, None) , 0 , )),
	(( 'GetObjectByIndex' , 'index' , ), 1610678281, (1610678281, (), [ (3, 0, None, None) , ], 1 , 1 , 4 , 0 , 96 , (13, 0, None, None) , 0 , )),
	(( 'GetObjectType' , 'index' , ), 1610678282, (1610678282, (), [ (3, 0, None, None) , ], 1 , 1 , 4 , 0 , 104 , (3, 0, None, None) , 0 , )),
	(( 'GetCurrentManagerType' , ), 1610678283, (1610678283, (), [ ], 1 , 1 , 4 , 0 , 112 , (3, 0, None, None) , 0 , )),
	(( 'SetCurrentManagerType' , 'type' , ), 1610678284, (1610678284, (), [ (3, 0, None, None) , ], 1 , 1 , 4 , 0 , 120 , (3, 0, None, None) , 0 , )),
	(( 'GetManagerIndex' , 'obj' , ), 1610678285, (1610678285, (), [ (13, 0, None, None) , ], 1 , 1 , 4 , 0 , 128 , (3, 0, None, None) , 0 , )),
]

IChooseParts_vtables_dispatch_ = 0
IChooseParts_vtables_ = [
	(( 'SetChoosePartsType' , 'val' , ), 1610678272, (1610678272, (), [ (3, 0, None, None) , ], 1 , 1 , 4 , 0 , 24 , (3, 0, None, None) , 0 , )),
	(( 'GetChoosePartsType' , ), 1610678273, (1610678273, (), [ ], 1 , 1 , 4 , 0 , 32 , (3, 0, None, None) , 0 , )),
	(( 'PartCollection' , ), 1610678274, (1610678274, (), [ ], 1 , 1 , 4 , 0 , 40 , (13, 0, None, IID('{7AA0E540-0317-11D4-A30E-00C026EE094F}')) , 0 , )),
]

ICircle3dParam_vtables_dispatch_ = 0
ICircle3dParam_vtables_ = [
	(( 'GetPlacement' , ), 1610678272, (1610678272, (), [ ], 1 , 1 , 4 , 0 , 24 , (13, 0, None, IID('{7AA0E540-0310-11D4-A30E-00C026EE094F}')) , 0 , )),
	(( 'GetRadius' , ), 1610678273, (1610678273, (), [ ], 1 , 1 , 4 , 0 , 32 , (5, 0, None, None) , 0 , )),
]

ICircularPartArrayDefinition_vtables_dispatch_ = 0
ICircularPartArrayDefinition_vtables_ = [
	(( 'PartArray' , ), 1610678272, (1610678272, (), [ ], 1 , 1 , 4 , 0 , 24 , (13, 0, None, IID('{7AA0E540-0317-11D4-A30E-00C026EE094F}')) , 0 , )),
	(( 'GetAxis' , ), 1610678273, (1610678273, (), [ ], 1 , 1 , 4 , 0 , 32 , (13, 0, None, IID('{7AA0E540-0301-11D4-A30E-00C026EE094F}')) , 0 , )),
	(( 'SetAxis' , 'axis' , ), 1610678274, (1610678274, (), [ (13, 0, None, "IID('{7AA0E540-0301-11D4-A30E-00C026EE094F}')") , ], 1 , 1 , 4 , 0 , 40 , (3, 0, None, None) , 0 , )),
	(( 'GetCount1' , ), 1610678275, (1610678275, (), [ ], 1 , 1 , 4 , 0 , 48 , (3, 0, None, None) , 0 , )),
	(( 'SetCount1' , 'count' , ), 1610678276, (1610678276, (), [ (3, 0, None, None) , ], 1 , 1 , 4 , 0 , 56 , (3, 0, None, None) , 0 , )),
	(( 'GetStep1' , ), 1610678277, (1610678277, (), [ ], 1 , 1 , 4 , 0 , 64 , (5, 0, None, None) , 0 , )),
	(( 'SetStep1' , 'step' , ), 1610678278, (1610678278, (), [ (5, 0, None, None) , ], 1 , 1 , 4 , 0 , 72 , (3, 0, None, None) , 0 , )),
	(( 'GetFactor1' , ), 1610678279, (1610678279, (), [ ], 1 , 1 , 4 , 0 , 80 , (3, 0, None, None) , 0 , )),
	(( 'SetFactor1' , 'factor' , ), 1610678280, (1610678280, (), [ (3, 0, None, None) , ], 1 , 1 , 4 , 0 , 88 , (3, 0, None, None) , 0 , )),
	(( 'GetCount2' , ), 1610678281, (1610678281, (), [ ], 1 , 1 , 4 , 0 , 96 , (3, 0, None, None) , 0 , )),
	(( 'SetCount2' , 'count' , ), 1610678282, (1610678282, (), [ (3, 0, None, None) , ], 1 , 1 , 4 , 0 , 104 , (3, 0, None, None) , 0 , )),
	(( 'GetStep2' , ), 1610678283, (1610678283, (), [ ], 1 , 1 , 4 , 0 , 112 , (5, 0, None, None) , 0 , )),
	(( 'SetStep2' , 'step' , ), 1610678284, (1610678284, (), [ (5, 0, None, None) , ], 1 , 1 , 4 , 0 , 120 , (3, 0, None, None) , 0 , )),
	(( 'GetFactor2' , ), 1610678285, (1610678285, (), [ ], 1 , 1 , 4 , 0 , 128 , (3, 0, None, None) , 0 , )),
	(( 'SetFactor2' , 'factor' , ), 1610678286, (1610678286, (), [ (3, 0, None, None) , ], 1 , 1 , 4 , 0 , 136 , (3, 0, None, None) , 0 , )),
	(( 'GetInverce' , ), 1610678287, (1610678287, (), [ ], 1 , 1 , 4 , 0 , 144 , (3, 0, None, None) , 0 , )),
	(( 'SetInverce' , 'inverce' , ), 1610678288, (1610678288, (), [ (3, 0, None, None) , ], 1 , 1 , 4 , 0 , 152 , (3, 0, None, None) , 0 , )),
	(( 'GetCopyParamAlongDir' , 'count' , 'step' , 'factor' , 'dir' , 
			 ), 1610678289, (1610678289, (), [ (16387, 0, None, None) , (16389, 0, None, None) , (16387, 0, None, None) , (3, 0, None, None) , ], 1 , 1 , 4 , 0 , 160 , (3, 0, None, None) , 0 , )),
	(( 'SetCopyParamAlongDir' , 'count' , 'step' , 'factor' , 'dir' , 
			 ), 1610678290, (1610678290, (), [ (3, 0, None, None) , (5, 0, None, None) , (3, 0, None, None) , (3, 0, None, None) , ], 1 , 1 , 4 , 0 , 168 , (3, 0, None, None) , 0 , )),
	(( 'DeletedCollection' , ), 1610678291, (1610678291, (), [ ], 1 , 1 , 4 , 0 , 176 , (13, 0, None, IID('{BEC3920D-6238-401A-86A3-A600570F47A4}')) , 0 , )),
	(( 'GetKeepAngle' , ), 1610678292, (1610678292, (), [ ], 1 , 1 , 4 , 0 , 184 , (3, 0, None, None) , 0 , )),
	(( 'SetKeepAngle' , 'keepAngle' , ), 1610678293, (1610678293, (), [ (3, 0, None, None) , ], 1 , 1 , 4 , 0 , 192 , (3, 0, None, None) , 0 , )),
]

IColorParam_vtables_dispatch_ = 0
IColorParam_vtables_ = [
	(( 'Clear' , ), 1610678272, (1610678272, (), [ ], 1 , 1 , 4 , 0 , 24 , (3, 0, None, None) , 0 , )),
	(( 'GetColor' , ), 1610678273, (1610678273, (), [ ], 1 , 1 , 4 , 0 , 32 , (19, 0, None, None) , 0 , )),
	(( 'SetColor' , 'val' , ), 1610678274, (1610678274, (), [ (19, 0, None, None) , ], 1 , 1 , 4 , 0 , 40 , (3, 0, None, None) , 0 , )),
	(( 'GetAmbient' , ), 1610678275, (1610678275, (), [ ], 1 , 1 , 4 , 0 , 48 , (5, 0, None, None) , 0 , )),
	(( 'SetAmbient' , 'val' , ), 1610678276, (1610678276, (), [ (5, 0, None, None) , ], 1 , 1 , 4 , 0 , 56 , (3, 0, None, None) , 0 , )),
	(( 'GetDiffuse' , ), 1610678277, (1610678277, (), [ ], 1 , 1 , 4 , 0 , 64 , (5, 0, None, None) , 0 , )),
	(( 'SetDiffuse' , 'val' , ), 1610678278, (1610678278, (), [ (5, 0, None, None) , ], 1 , 1 , 4 , 0 , 72 , (3, 0, None, None) , 0 , )),
	(( 'GetSpecularity' , ), 1610678279, (1610678279, (), [ ], 1 , 1 , 4 , 0 , 80 , (5, 0, None, None) , 0 , )),
	(( 'SetSpecularity' , 'val' , ), 1610678280, (1610678280, (), [ (5, 0, None, None) , ], 1 , 1 , 4 , 0 , 88 , (3, 0, None, None) , 0 , )),
	(( 'GetShininess' , ), 1610678281, (1610678281, (), [ ], 1 , 1 , 4 , 0 , 96 , (5, 0, None, None) , 0 , )),
	(( 'SetShininess' , 'val' , ), 1610678282, (1610678282, (), [ (5, 0, None, None) , ], 1 , 1 , 4 , 0 , 104 , (3, 0, None, None) , 0 , )),
	(( 'GetTransparency' , ), 1610678283, (1610678283, (), [ ], 1 , 1 , 4 , 0 , 112 , (5, 0, None, None) , 0 , )),
	(( 'SetTransparency' , 'val' , ), 1610678284, (1610678284, (), [ (5, 0, None, None) , ], 1 , 1 , 4 , 0 , 120 , (3, 0, None, None) , 0 , )),
	(( 'GetEmission' , ), 1610678285, (1610678285, (), [ ], 1 , 1 , 4 , 0 , 128 , (5, 0, None, None) , 0 , )),
	(( 'SetEmission' , 'val' , ), 1610678286, (1610678286, (), [ (5, 0, None, None) , ], 1 , 1 , 4 , 0 , 136 , (3, 0, None, None) , 0 , )),
	(( 'GetUseColor' , ), 1610678287, (1610678287, (), [ ], 1 , 1 , 4 , 0 , 144 , (3, 0, None, None) , 0 , )),
	(( 'SetUseColor' , 'useColor' , ), 1610678288, (1610678288, (), [ (3, 0, None, None) , ], 1 , 1 , 4 , 0 , 152 , (3, 0, None, None) , 0 , )),
]

IComponentPositioner_vtables_dispatch_ = 0
IComponentPositioner_vtables_ = [
	(( 'SetPlaneByPlacement' , 'plane' , ), 1610678272, (1610678272, (), [ (13, 0, None, "IID('{7AA0E540-0310-11D4-A30E-00C026EE094F}')") , ], 1 , 1 , 4 , 0 , 24 , (3, 0, None, None) , 0 , )),
	(( 'SetPlane' , 'plane' , ), 1610678273, (1610678273, (), [ (13, 0, None, None) , ], 1 , 1 , 4 , 0 , 32 , (3, 0, None, None) , 0 , )),
	(( 'SetPlaneByPoints' , 'x1' , 'y1' , 'z1' , 'x2' , 
			 'y2' , 'z2' , 'x3' , 'y3' , 'z3' , 
			 ), 1610678274, (1610678274, (), [ (5, 0, None, None) , (5, 0, None, None) , (5, 0, None, None) , (5, 0, None, None) , 
			 (5, 0, None, None) , (5, 0, None, None) , (5, 0, None, None) , (5, 0, None, None) , (5, 0, None, None) , ], 1 , 1 , 4 , 0 , 40 , (3, 0, None, None) , 0 , )),
	(( 'SetDragPoint' , 'x' , 'y' , 'z' , ), 1610678275, (1610678275, (), [ 
			 (5, 0, None, None) , (5, 0, None, None) , (5, 0, None, None) , ], 1 , 1 , 4 , 0 , 48 , (3, 0, None, None) , 0 , )),
	(( 'SetAxis' , 'axis' , ), 1610678276, (1610678276, (), [ (13, 0, None, None) , ], 1 , 1 , 4 , 0 , 56 , (3, 0, None, None) , 0 , )),
	(( 'SetAxisByPoints' , 'x1' , 'y1' , 'z1' , 'x2' , 
			 'y2' , 'z2' , ), 1610678277, (1610678277, (), [ (5, 0, None, None) , (5, 0, None, None) , 
			 (5, 0, None, None) , (5, 0, None, None) , (5, 0, None, None) , (5, 0, None, None) , ], 1 , 1 , 4 , 0 , 64 , (3, 0, None, None) , 0 , )),
	(( 'Prepare' , 'part' , 'positionerType' , ), 1610678278, (1610678278, (), [ (13, 0, None, "IID('{7AA0E540-0300-11D4-A30E-00C026EE094F}')") , 
			 (3, 0, None, None) , ], 1 , 1 , 4 , 0 , 72 , (3, 0, None, None) , 0 , )),
	(( 'MoveComponent' , 'x' , 'y' , 'z' , ), 1610678279, (1610678279, (), [ 
			 (5, 0, None, None) , (5, 0, None, None) , (5, 0, None, None) , ], 1 , 1 , 4 , 0 , 80 , (3, 0, None, None) , 0 , )),
	(( 'RotateComponent' , 'angl' , ), 1610678280, (1610678280, (), [ (5, 0, None, None) , ], 1 , 1 , 4 , 0 , 88 , (3, 0, None, None) , 0 , )),
	(( 'Finish' , ), 1610678281, (1610678281, (), [ ], 1 , 1 , 4 , 0 , 96 , (3, 0, None, None) , 0 , )),
]

IConeParam_vtables_dispatch_ = 0
IConeParam_vtables_ = [
	(( 'GetRadius' , ), 1610678272, (1610678272, (), [ ], 1 , 1 , 4 , 0 , 24 , (5, 0, None, None) , 0 , )),
	(( 'GetHeight' , ), 1610678273, (1610678273, (), [ ], 1 , 1 , 4 , 0 , 32 , (5, 0, None, None) , 0 , )),
	(( 'GetAngle' , ), 1610678274, (1610678274, (), [ ], 1 , 1 , 4 , 0 , 40 , (5, 0, None, None) , 0 , )),
	(( 'GetPlacement' , ), 1610678275, (1610678275, (), [ ], 1 , 1 , 4 , 0 , 48 , (13, 0, None, IID('{7AA0E540-0310-11D4-A30E-00C026EE094F}')) , 0 , )),
]

IConicSpiralDefinition_vtables_dispatch_ = 0
IConicSpiralDefinition_vtables_ = [
	(( 'GetTurn' , ), 1610678272, (1610678272, (), [ ], 1 , 1 , 4 , 0 , 24 , (5, 0, None, None) , 0 , )),
	(( 'SetTurn' , 'turn' , ), 1610678273, (1610678273, (), [ (5, 0, None, None) , ], 1 , 1 , 4 , 0 , 32 , (3, 0, None, None) , 0 , )),
	(( 'GetStep' , ), 1610678274, (1610678274, (), [ ], 1 , 1 , 4 , 0 , 40 , (5, 0, None, None) , 0 , )),
	(( 'SetStep' , 'step' , ), 1610678275, (1610678275, (), [ (5, 0, None, None) , ], 1 , 1 , 4 , 0 , 48 , (3, 0, None, None) , 0 , )),
	(( 'GetTurnDir' , ), 1610678276, (1610678276, (), [ ], 1 , 1 , 4 , 0 , 56 , (3, 0, None, None) , 0 , )),
	(( 'SetTurnDir' , 'turnDir' , ), 1610678277, (1610678277, (), [ (3, 0, None, None) , ], 1 , 1 , 4 , 0 , 64 , (3, 0, None, None) , 0 , )),
	(( 'GetPlane' , ), 1610678278, (1610678278, (), [ ], 1 , 1 , 4 , 0 , 72 , (13, 0, None, IID('{7AA0E540-0301-11D4-A30E-00C026EE094F}')) , 0 , )),
	(( 'SetPlane' , 'plane' , ), 1610678279, (1610678279, (), [ (13, 0, None, "IID('{7AA0E540-0301-11D4-A30E-00C026EE094F}')") , ], 1 , 1 , 4 , 0 , 80 , (3, 0, None, None) , 0 , )),
	(( 'GetLocation' , 'x' , 'y' , ), 1610678280, (1610678280, (), [ (16389, 0, None, None) , 
			 (16389, 0, None, None) , ], 1 , 1 , 4 , 0 , 88 , (3, 0, None, None) , 0 , )),
	(( 'SetLocation' , 'x' , 'y' , ), 1610678281, (1610678281, (), [ (5, 0, None, None) , 
			 (5, 0, None, None) , ], 1 , 1 , 4 , 0 , 96 , (3, 0, None, None) , 0 , )),
	(( 'GetBuildMode' , ), 1610678282, (1610678282, (), [ ], 1 , 1 , 4 , 0 , 104 , (2, 0, None, None) , 0 , )),
	(( 'SetBuildMode' , 'buildMode' , ), 1610678283, (1610678283, (), [ (2, 0, None, None) , ], 1 , 1 , 4 , 0 , 112 , (3, 0, None, None) , 0 , )),
	(( 'GetBuildDir' , ), 1610678284, (1610678284, (), [ ], 1 , 1 , 4 , 0 , 120 , (3, 0, None, None) , 0 , )),
	(( 'SetBuildDir' , 'buildDir' , ), 1610678285, (1610678285, (), [ (3, 0, None, None) , ], 1 , 1 , 4 , 0 , 128 , (3, 0, None, None) , 0 , )),
	(( 'GetHeight' , ), 1610678286, (1610678286, (), [ ], 1 , 1 , 4 , 0 , 136 , (5, 0, None, None) , 0 , )),
	(( 'SetHeight' , 'height' , ), 1610678287, (1610678287, (), [ (5, 0, None, None) , ], 1 , 1 , 4 , 0 , 144 , (3, 0, None, None) , 0 , )),
	(( 'GetHeightType' , ), 1610678288, (1610678288, (), [ ], 1 , 1 , 4 , 0 , 152 , (2, 0, None, None) , 0 , )),
	(( 'SetHeightType' , 'heightType' , ), 1610678289, (1610678289, (), [ (2, 0, None, None) , ], 1 , 1 , 4 , 0 , 160 , (3, 0, None, None) , 0 , )),
	(( 'GetHeightAdd' , ), 1610678290, (1610678290, (), [ ], 1 , 1 , 4 , 0 , 168 , (5, 0, None, None) , 0 , )),
	(( 'SetHeightAdd' , 'heightAdd' , ), 1610678291, (1610678291, (), [ (5, 0, None, None) , ], 1 , 1 , 4 , 0 , 176 , (3, 0, None, None) , 0 , )),
	(( 'GetHeightAddHow' , ), 1610678292, (1610678292, (), [ ], 1 , 1 , 4 , 0 , 184 , (3, 0, None, None) , 0 , )),
	(( 'SetHeightAddHow' , 'heightAddHow' , ), 1610678293, (1610678293, (), [ (3, 0, None, None) , ], 1 , 1 , 4 , 0 , 192 , (3, 0, None, None) , 0 , )),
	(( 'SetHeightObject' , 'heightObject' , ), 1610678294, (1610678294, (), [ (13, 0, None, "IID('{7AA0E540-0301-11D4-A30E-00C026EE094F}')") , ], 1 , 1 , 4 , 0 , 200 , (3, 0, None, None) , 0 , )),
	(( 'GetHeightObject' , ), 1610678295, (1610678295, (), [ ], 1 , 1 , 4 , 0 , 208 , (13, 0, None, IID('{7AA0E540-0301-11D4-A30E-00C026EE094F}')) , 0 , )),
	(( 'GetInitialDiam' , ), 1610678296, (1610678296, (), [ ], 1 , 1 , 4 , 0 , 216 , (5, 0, None, None) , 0 , )),
	(( 'SetInitialDiam' , 'diam1Type' , ), 1610678297, (1610678297, (), [ (5, 0, None, None) , ], 1 , 1 , 4 , 0 , 224 , (3, 0, None, None) , 0 , )),
	(( 'GetInitialDiamType' , ), 1610678298, (1610678298, (), [ ], 1 , 1 , 4 , 0 , 232 , (2, 0, None, None) , 0 , )),
	(( 'SetInitialDiamType' , 'diam1Type' , ), 1610678299, (1610678299, (), [ (2, 0, None, None) , ], 1 , 1 , 4 , 0 , 240 , (3, 0, None, None) , 0 , )),
	(( 'GetInitialDiamObject' , ), 1610678300, (1610678300, (), [ ], 1 , 1 , 4 , 0 , 248 , (13, 0, None, IID('{7AA0E540-0301-11D4-A30E-00C026EE094F}')) , 0 , )),
	(( 'SetInitialDiamObject' , 'diam1Object' , ), 1610678301, (1610678301, (), [ (13, 0, None, "IID('{7AA0E540-0301-11D4-A30E-00C026EE094F}')") , ], 1 , 1 , 4 , 0 , 256 , (3, 0, None, None) , 0 , )),
	(( 'GetTerminalDiam' , ), 1610678302, (1610678302, (), [ ], 1 , 1 , 4 , 0 , 264 , (5, 0, None, None) , 0 , )),
	(( 'SetTerminalDiam' , 'diam2' , ), 1610678303, (1610678303, (), [ (5, 0, None, None) , ], 1 , 1 , 4 , 0 , 272 , (3, 0, None, None) , 0 , )),
	(( 'GetTerminalDiamType' , ), 1610678304, (1610678304, (), [ ], 1 , 1 , 4 , 0 , 280 , (2, 0, None, None) , 0 , )),
	(( 'SetTerminalDiamType' , 'diam2Type' , ), 1610678305, (1610678305, (), [ (2, 0, None, None) , ], 1 , 1 , 4 , 0 , 288 , (3, 0, None, None) , 0 , )),
	(( 'GetTerminalDiamObject' , ), 1610678306, (1610678306, (), [ ], 1 , 1 , 4 , 0 , 296 , (13, 0, None, IID('{7AA0E540-0301-11D4-A30E-00C026EE094F}')) , 0 , )),
	(( 'SetTerminalDiamObject' , 'diam2Object' , ), 1610678307, (1610678307, (), [ (13, 0, None, "IID('{7AA0E540-0301-11D4-A30E-00C026EE094F}')") , ], 1 , 1 , 4 , 0 , 304 , (3, 0, None, None) , 0 , )),
	(( 'GetTiltAngle' , ), 1610678308, (1610678308, (), [ ], 1 , 1 , 4 , 0 , 312 , (5, 0, None, None) , 0 , )),
	(( 'SetTiltAngle' , 'tiltAngle' , ), 1610678309, (1610678309, (), [ (5, 0, None, None) , ], 1 , 1 , 4 , 0 , 320 , (3, 0, None, None) , 0 , )),
	(( 'GetTiltAngleHow' , ), 1610678310, (1610678310, (), [ ], 1 , 1 , 4 , 0 , 328 , (3, 0, None, None) , 0 , )),
	(( 'SetTiltAngleHow' , 'tiltAngleHow' , ), 1610678311, (1610678311, (), [ (3, 0, None, None) , ], 1 , 1 , 4 , 0 , 336 , (3, 0, None, None) , 0 , )),
	(( 'GetFirstAngle' , ), 1610678312, (1610678312, (), [ ], 1 , 1 , 4 , 0 , 344 , (5, 0, None, None) , 0 , )),
	(( 'SetFirstAngle' , 'firstAngle' , ), 1610678313, (1610678313, (), [ (5, 0, None, None) , ], 1 , 1 , 4 , 0 , 352 , (3, 0, None, None) , 0 , )),
	(( 'GetSketch' , ), 1610678314, (1610678314, (), [ ], 1 , 1 , 4 , 0 , 360 , (13, 0, None, IID('{7AA0E540-0301-11D4-A30E-00C026EE094F}')) , 0 , )),
	(( 'GetCurve3D' , ), 1610678315, (1610678315, (), [ ], 1 , 1 , 4 , 0 , 368 , (13, 0, None, IID('{E5066490-773D-4289-A60B-2FC19865174A}')) , 0 , )),
]

IConjunctivePointDefinition_vtables_dispatch_ = 0
IConjunctivePointDefinition_vtables_ = [
	(( 'GetVertex' , ), 1610678272, (1610678272, (), [ ], 1 , 1 , 4 , 0 , 24 , (13, 0, None, IID('{7AA0E540-0301-11D4-A30E-00C026EE094F}')) , 0 , )),
	(( 'SetVertex' , 'val' , ), 1610678273, (1610678273, (), [ (13, 0, None, "IID('{7AA0E540-0301-11D4-A30E-00C026EE094F}')") , ], 1 , 1 , 4 , 0 , 32 , (3, 0, None, None) , 0 , )),
	(( 'GetEdge' , ), 1610678274, (1610678274, (), [ ], 1 , 1 , 4 , 0 , 40 , (13, 0, None, IID('{7AA0E540-0301-11D4-A30E-00C026EE094F}')) , 0 , )),
	(( 'SetEdge' , 'val' , ), 1610678275, (1610678275, (), [ (13, 0, None, "IID('{7AA0E540-0301-11D4-A30E-00C026EE094F}')") , ], 1 , 1 , 4 , 0 , 48 , (3, 0, None, None) , 0 , )),
	(( 'GetDirection' , ), 1610678276, (1610678276, (), [ ], 1 , 1 , 4 , 0 , 56 , (3, 0, None, None) , 0 , )),
	(( 'SetDirection' , 'val' , ), 1610678277, (1610678277, (), [ (3, 0, None, None) , ], 1 , 1 , 4 , 0 , 64 , (3, 0, None, None) , 0 , )),
	(( 'GetPoint' , 'x' , 'y' , 'z' , ), 1610678278, (1610678278, (), [ 
			 (16389, 0, None, None) , (16389, 0, None, None) , (16389, 0, None, None) , ], 1 , 1 , 4 , 0 , 72 , (3, 0, None, None) , 0 , )),
]

IControlPointDefinition_vtables_dispatch_ = 0
IControlPointDefinition_vtables_ = [
	(( 'GetVertex' , ), 1610678272, (1610678272, (), [ ], 1 , 1 , 4 , 0 , 24 , (13, 0, None, IID('{7AA0E540-0301-11D4-A30E-00C026EE094F}')) , 0 , )),
	(( 'SetVertex' , 'val' , ), 1610678273, (1610678273, (), [ (13, 0, None, "IID('{7AA0E540-0301-11D4-A30E-00C026EE094F}')") , ], 1 , 1 , 4 , 0 , 32 , (3, 0, None, None) , 0 , )),
	(( 'GetPoint' , 'x' , 'y' , 'z' , ), 1610678274, (1610678274, (), [ 
			 (16389, 0, None, None) , (16389, 0, None, None) , (16389, 0, None, None) , ], 1 , 1 , 4 , 0 , 40 , (3, 0, None, None) , 0 , )),
]

ICoordinate3dCollection_vtables_dispatch_ = 0
ICoordinate3dCollection_vtables_ = [
	(( 'GetCount' , ), 1610678272, (1610678272, (), [ ], 1 , 1 , 4 , 0 , 24 , (3, 0, None, None) , 0 , )),
	(( 'GetByIndex' , 'index' , 'x' , 'y' , 'z' , 
			 ), 1610678273, (1610678273, (), [ (3, 1, None, None) , (16389, 2, None, None) , (16389, 2, None, None) , (16389, 2, None, None) , ], 1 , 1 , 4 , 0 , 32 , (3, 0, None, None) , 0 , )),
	(( 'GetSafeArray' , 'pArray' , ), 1610678274, (1610678274, (), [ (16396, 2, None, None) , ], 1 , 1 , 4 , 0 , 40 , (3, 0, None, None) , 0 , )),
]

ICopyCircularDefinition_vtables_dispatch_ = 0
ICopyCircularDefinition_vtables_ = [
	(( 'GetOperationArray' , ), 1610678272, (1610678272, (), [ ], 1 , 1 , 4 , 0 , 24 , (13, 0, None, IID('{7AA0E540-0303-11D4-A30E-00C026EE094F}')) , 0 , )),
	(( 'GetAxis' , ), 1610678273, (1610678273, (), [ ], 1 , 1 , 4 , 0 , 32 , (13, 0, None, IID('{7AA0E540-0301-11D4-A30E-00C026EE094F}')) , 0 , )),
	(( 'SetAxis' , 'axis' , ), 1610678274, (1610678274, (), [ (13, 0, None, "IID('{7AA0E540-0301-11D4-A30E-00C026EE094F}')") , ], 1 , 1 , 4 , 0 , 40 , (3, 0, None, None) , 0 , )),
	(( 'GetCount1' , ), 1610678275, (1610678275, (), [ ], 1 , 1 , 4 , 0 , 48 , (3, 0, None, None) , 0 , )),
	(( 'SetCount1' , 'count' , ), 1610678276, (1610678276, (), [ (3, 0, None, None) , ], 1 , 1 , 4 , 0 , 56 , (3, 0, None, None) , 0 , )),
	(( 'GetStep1' , ), 1610678277, (1610678277, (), [ ], 1 , 1 , 4 , 0 , 64 , (5, 0, None, None) , 0 , )),
	(( 'SetStep1' , 'step' , ), 1610678278, (1610678278, (), [ (5, 0, None, None) , ], 1 , 1 , 4 , 0 , 72 , (3, 0, None, None) , 0 , )),
	(( 'GetFactor1' , ), 1610678279, (1610678279, (), [ ], 1 , 1 , 4 , 0 , 80 , (3, 0, None, None) , 0 , )),
	(( 'SetFactor1' , 'factor' , ), 1610678280, (1610678280, (), [ (3, 0, None, None) , ], 1 , 1 , 4 , 0 , 88 , (3, 0, None, None) , 0 , )),
	(( 'GetCount2' , ), 1610678281, (1610678281, (), [ ], 1 , 1 , 4 , 0 , 96 , (3, 0, None, None) , 0 , )),
	(( 'SetCount2' , 'count' , ), 1610678282, (1610678282, (), [ (3, 0, None, None) , ], 1 , 1 , 4 , 0 , 104 , (3, 0, None, None) , 0 , )),
	(( 'GetStep2' , ), 1610678283, (1610678283, (), [ ], 1 , 1 , 4 , 0 , 112 , (5, 0, None, None) , 0 , )),
	(( 'SetStep2' , 'step' , ), 1610678284, (1610678284, (), [ (5, 0, None, None) , ], 1 , 1 , 4 , 0 , 120 , (3, 0, None, None) , 0 , )),
	(( 'GetFactor2' , ), 1610678285, (1610678285, (), [ ], 1 , 1 , 4 , 0 , 128 , (3, 0, None, None) , 0 , )),
	(( 'SetFactor2' , 'factor' , ), 1610678286, (1610678286, (), [ (3, 0, None, None) , ], 1 , 1 , 4 , 0 , 136 , (3, 0, None, None) , 0 , )),
	(( 'GetInverce' , ), 1610678287, (1610678287, (), [ ], 1 , 1 , 4 , 0 , 144 , (3, 0, None, None) , 0 , )),
	(( 'SetInverce' , 'inverce' , ), 1610678288, (1610678288, (), [ (3, 0, None, None) , ], 1 , 1 , 4 , 0 , 152 , (3, 0, None, None) , 0 , )),
	(( 'GetCopyParamAlongDir' , 'count' , 'step' , 'factor' , 'dir' , 
			 ), 1610678289, (1610678289, (), [ (16387, 0, None, None) , (16389, 0, None, None) , (16387, 0, None, None) , (3, 0, None, None) , ], 1 , 1 , 4 , 0 , 160 , (3, 0, None, None) , 0 , )),
	(( 'SetCopyParamAlongDir' , 'count' , 'step' , 'factor' , 'dir' , 
			 ), 1610678290, (1610678290, (), [ (3, 0, None, None) , (5, 0, None, None) , (3, 0, None, None) , (3, 0, None, None) , ], 1 , 1 , 4 , 0 , 168 , (3, 0, None, None) , 0 , )),
	(( 'DeletedCollection' , ), 1610678291, (1610678291, (), [ ], 1 , 1 , 4 , 0 , 176 , (13, 0, None, IID('{BEC3920D-6238-401A-86A3-A600570F47A4}')) , 0 , )),
	(( 'GetGeomArray' , ), 1610678292, (1610678292, (), [ ], 1 , 1 , 4 , 0 , 184 , (3, 0, None, None) , 0 , )),
	(( 'SetGeomArray' , 'val' , ), 1610678293, (1610678293, (), [ (3, 0, None, None) , ], 1 , 1 , 4 , 0 , 192 , (3, 0, None, None) , 0 , )),
]

ICopyCurveDefinition_vtables_dispatch_ = 0
ICopyCurveDefinition_vtables_ = [
	(( 'OperationArray' , ), 1610678272, (1610678272, (), [ ], 1 , 1 , 4 , 0 , 24 , (13, 0, None, IID('{7AA0E540-0303-11D4-A30E-00C026EE094F}')) , 0 , )),
	(( 'CurveArray' , ), 1610678273, (1610678273, (), [ ], 1 , 1 , 4 , 0 , 32 , (13, 0, None, IID('{7AA0E540-0303-11D4-A30E-00C026EE094F}')) , 0 , )),
	(( 'GetStep' , ), 1610678274, (1610678274, (), [ ], 1 , 1 , 4 , 0 , 40 , (5, 0, None, None) , 0 , )),
	(( 'SetStep' , 'step' , ), 1610678275, (1610678275, (), [ (5, 0, None, None) , ], 1 , 1 , 4 , 0 , 48 , (3, 0, None, None) , 0 , )),
	(( 'GetCount' , ), 1610678276, (1610678276, (), [ ], 1 , 1 , 4 , 0 , 56 , (3, 0, None, None) , 0 , )),
	(( 'SetCount' , 'count' , ), 1610678277, (1610678277, (), [ (3, 0, None, None) , ], 1 , 1 , 4 , 0 , 64 , (3, 0, None, None) , 0 , )),
	(( 'GetFactor' , ), 1610678278, (1610678278, (), [ ], 1 , 1 , 4 , 0 , 72 , (3, 0, None, None) , 0 , )),
	(( 'SetFactor' , 'factor' , ), 1610678279, (1610678279, (), [ (3, 0, None, None) , ], 1 , 1 , 4 , 0 , 80 , (3, 0, None, None) , 0 , )),
	(( 'GetSence' , ), 1610678280, (1610678280, (), [ ], 1 , 1 , 4 , 0 , 88 , (3, 0, None, None) , 0 , )),
	(( 'SetSence' , 'sence' , ), 1610678281, (1610678281, (), [ (3, 0, None, None) , ], 1 , 1 , 4 , 0 , 96 , (3, 0, None, None) , 0 , )),
	(( 'GetKeepAngle' , ), 1610678282, (1610678282, (), [ ], 1 , 1 , 4 , 0 , 104 , (3, 0, None, None) , 0 , )),
	(( 'SetKeepAngle' , 'keepAngle' , ), 1610678283, (1610678283, (), [ (3, 0, None, None) , ], 1 , 1 , 4 , 0 , 112 , (3, 0, None, None) , 0 , )),
	(( 'GetFullCurve' , ), 1610678284, (1610678284, (), [ ], 1 , 1 , 4 , 0 , 120 , (3, 0, None, None) , 0 , )),
	(( 'SetFullCurve' , 'fullCurve' , ), 1610678285, (1610678285, (), [ (3, 0, None, None) , ], 1 , 1 , 4 , 0 , 128 , (3, 0, None, None) , 0 , )),
	(( 'DeletedCollection' , ), 1610678286, (1610678286, (), [ ], 1 , 1 , 4 , 0 , 136 , (13, 0, None, IID('{BEC3920D-6238-401A-86A3-A600570F47A4}')) , 0 , )),
	(( 'GetGeomArray' , ), 1610678287, (1610678287, (), [ ], 1 , 1 , 4 , 0 , 144 , (3, 0, None, None) , 0 , )),
	(( 'SetGeomArray' , 'val' , ), 1610678288, (1610678288, (), [ (3, 0, None, None) , ], 1 , 1 , 4 , 0 , 152 , (3, 0, None, None) , 0 , )),
]

ICopyMeshDefinition_vtables_dispatch_ = 0
ICopyMeshDefinition_vtables_ = [
	(( 'OperationArray' , ), 1610678272, (1610678272, (), [ ], 1 , 1 , 4 , 0 , 24 , (13, 0, None, IID('{7AA0E540-0303-11D4-A30E-00C026EE094F}')) , 0 , )),
	(( 'GetAngle1' , ), 1610678273, (1610678273, (), [ ], 1 , 1 , 4 , 0 , 32 , (5, 0, None, None) , 0 , )),
	(( 'SetAngle1' , 'angle' , ), 1610678274, (1610678274, (), [ (5, 0, None, None) , ], 1 , 1 , 4 , 0 , 40 , (3, 0, None, None) , 0 , )),
	(( 'GetCount1' , ), 1610678275, (1610678275, (), [ ], 1 , 1 , 4 , 0 , 48 , (3, 0, None, None) , 0 , )),
	(( 'SetCount1' , 'count' , ), 1610678276, (1610678276, (), [ (3, 0, None, None) , ], 1 , 1 , 4 , 0 , 56 , (3, 0, None, None) , 0 , )),
	(( 'GetStep1' , ), 1610678277, (1610678277, (), [ ], 1 , 1 , 4 , 0 , 64 , (5, 0, None, None) , 0 , )),
	(( 'SetStep1' , 'step' , ), 1610678278, (1610678278, (), [ (5, 0, None, None) , ], 1 , 1 , 4 , 0 , 72 , (3, 0, None, None) , 0 , )),
	(( 'GetFactor1' , ), 1610678279, (1610678279, (), [ ], 1 , 1 , 4 , 0 , 80 , (3, 0, None, None) , 0 , )),
	(( 'SetFactor1' , 'factor' , ), 1610678280, (1610678280, (), [ (3, 0, None, None) , ], 1 , 1 , 4 , 0 , 88 , (3, 0, None, None) , 0 , )),
	(( 'GetAngle2' , ), 1610678281, (1610678281, (), [ ], 1 , 1 , 4 , 0 , 96 , (5, 0, None, None) , 0 , )),
	(( 'SetAngle2' , 'angle' , ), 1610678282, (1610678282, (), [ (5, 0, None, None) , ], 1 , 1 , 4 , 0 , 104 , (3, 0, None, None) , 0 , )),
	(( 'GetCount2' , ), 1610678283, (1610678283, (), [ ], 1 , 1 , 4 , 0 , 112 , (3, 0, None, None) , 0 , )),
	(( 'SetCount2' , 'count' , ), 1610678284, (1610678284, (), [ (3, 0, None, None) , ], 1 , 1 , 4 , 0 , 120 , (3, 0, None, None) , 0 , )),
	(( 'GetStep2' , ), 1610678285, (1610678285, (), [ ], 1 , 1 , 4 , 0 , 128 , (5, 0, None, None) , 0 , )),
	(( 'SetStep2' , 'step' , ), 1610678286, (1610678286, (), [ (5, 0, None, None) , ], 1 , 1 , 4 , 0 , 136 , (3, 0, None, None) , 0 , )),
	(( 'GetFactor2' , ), 1610678287, (1610678287, (), [ ], 1 , 1 , 4 , 0 , 144 , (3, 0, None, None) , 0 , )),
	(( 'SetFactor2' , 'factor' , ), 1610678288, (1610678288, (), [ (3, 0, None, None) , ], 1 , 1 , 4 , 0 , 152 , (3, 0, None, None) , 0 , )),
	(( 'GetInsideFlag' , ), 1610678289, (1610678289, (), [ ], 1 , 1 , 4 , 0 , 160 , (3, 0, None, None) , 0 , )),
	(( 'SetInsideFlag' , 'flag' , ), 1610678290, (1610678290, (), [ (3, 0, None, None) , ], 1 , 1 , 4 , 0 , 168 , (3, 0, None, None) , 0 , )),
	(( 'GetCopyParamAlongAxis' , 'firstAxis' , 'angle' , 'count' , 'step' , 
			 'factor' , ), 1610678291, (1610678291, (), [ (3, 0, None, None) , (16389, 0, None, None) , (16387, 0, None, None) , 
			 (16389, 0, None, None) , (16387, 0, None, None) , ], 1 , 1 , 4 , 0 , 176 , (3, 0, None, None) , 0 , )),
	(( 'SetCopyParamAlongAxis' , 'firstAxis' , 'angle' , 'count' , 'step' , 
			 'factor' , ), 1610678292, (1610678292, (), [ (3, 0, None, None) , (5, 0, None, None) , (3, 0, None, None) , 
			 (5, 0, None, None) , (3, 0, None, None) , ], 1 , 1 , 4 , 0 , 184 , (3, 0, None, None) , 0 , )),
	(( 'DeletedCollection' , ), 1610678293, (1610678293, (), [ ], 1 , 1 , 4 , 0 , 192 , (13, 0, None, IID('{BEC3920D-6238-401A-86A3-A600570F47A4}')) , 0 , )),
	(( 'GetGeomArray' , ), 1610678294, (1610678294, (), [ ], 1 , 1 , 4 , 0 , 200 , (3, 0, None, None) , 0 , )),
	(( 'SetGeomArray' , 'val' , ), 1610678295, (1610678295, (), [ (3, 0, None, None) , ], 1 , 1 , 4 , 0 , 208 , (3, 0, None, None) , 0 , )),
	(( 'GetAxis1' , ), 1610678296, (1610678296, (), [ ], 1 , 1 , 4 , 0 , 216 , (13, 0, None, IID('{7AA0E540-0301-11D4-A30E-00C026EE094F}')) , 0 , )),
	(( 'SetAxis1' , 'axis' , ), 1610678297, (1610678297, (), [ (13, 0, None, "IID('{7AA0E540-0301-11D4-A30E-00C026EE094F}')") , ], 1 , 1 , 4 , 0 , 224 , (3, 0, None, None) , 0 , )),
	(( 'GetAxis2' , ), 1610678298, (1610678298, (), [ ], 1 , 1 , 4 , 0 , 232 , (13, 0, None, IID('{7AA0E540-0301-11D4-A30E-00C026EE094F}')) , 0 , )),
	(( 'SetAxis2' , 'axis' , ), 1610678299, (1610678299, (), [ (13, 0, None, "IID('{7AA0E540-0301-11D4-A30E-00C026EE094F}')") , ], 1 , 1 , 4 , 0 , 240 , (3, 0, None, None) , 0 , )),
]

ICurve3D_vtables_dispatch_ = 0
ICurve3D_vtables_ = [
	(( 'GetPoint' , 'paramT' , 'x' , 'y' , 'z' , 
			 ), 1610678272, (1610678272, (), [ (5, 1, None, None) , (16389, 2, None, None) , (16389, 2, None, None) , (16389, 2, None, None) , ], 1 , 1 , 4 , 0 , 24 , (3, 0, None, None) , 0 , )),
	(( 'GetTangentVector' , 'paramT' , 'x' , 'y' , 'z' , 
			 ), 1610678273, (1610678273, (), [ (5, 1, None, None) , (16389, 1, None, None) , (16389, 1, None, None) , (16389, 1, None, None) , ], 1 , 1 , 4 , 0 , 32 , (3, 0, None, None) , 0 , )),
	(( 'GetNormal' , 'paramT' , 'x' , 'y' , 'z' , 
			 ), 1610678274, (1610678274, (), [ (5, 1, None, None) , (16389, 2, None, None) , (16389, 2, None, None) , (16389, 2, None, None) , ], 1 , 1 , 4 , 0 , 40 , (3, 0, None, None) , 0 , )),
	(( 'GetDerivativeT' , 'paramT' , 'x' , 'y' , 'z' , 
			 ), 1610678275, (1610678275, (), [ (5, 1, None, None) , (16389, 2, None, None) , (16389, 2, None, None) , (16389, 2, None, None) , ], 1 , 1 , 4 , 0 , 48 , (3, 0, None, None) , 0 , )),
	(( 'GetDerivativeTT' , 'paramT' , 'x' , 'y' , 'z' , 
			 ), 1610678276, (1610678276, (), [ (5, 1, None, None) , (16389, 2, None, None) , (16389, 2, None, None) , (16389, 2, None, None) , ], 1 , 1 , 4 , 0 , 56 , (3, 0, None, None) , 0 , )),
	(( 'GetDerivativeTTT' , 'paramT' , 'x' , 'y' , 'z' , 
			 ), 1610678277, (1610678277, (), [ (5, 1, None, None) , (16389, 2, None, None) , (16389, 2, None, None) , (16389, 2, None, None) , ], 1 , 1 , 4 , 0 , 64 , (3, 0, None, None) , 0 , )),
	(( 'GetParamMin' , ), 1610678278, (1610678278, (), [ ], 1 , 1 , 4 , 0 , 72 , (5, 0, None, None) , 0 , )),
	(( 'GetParamMax' , ), 1610678279, (1610678279, (), [ ], 1 , 1 , 4 , 0 , 80 , (5, 0, None, None) , 0 , )),
	(( 'IsClosed' , ), 1610678280, (1610678280, (), [ ], 1 , 1 , 4 , 0 , 88 , (3, 0, None, None) , 0 , )),
	(( 'IsPeriodic' , ), 1610678281, (1610678281, (), [ ], 1 , 1 , 4 , 0 , 96 , (3, 0, None, None) , 0 , )),
	(( 'GetMetricLength' , 'startParam' , 'endParam' , ), 1610678282, (1610678282, (), [ (5, 0, None, None) , 
			 (5, 0, None, None) , ], 1 , 1 , 4 , 0 , 104 , (5, 0, None, None) , 0 , )),
	(( 'GetGabarit' , 'x1' , 'y1' , 'z1' , 'x2' , 
			 'y2' , 'z2' , ), 1610678283, (1610678283, (), [ (16389, 2, None, None) , (16389, 2, None, None) , 
			 (16389, 2, None, None) , (16389, 2, None, None) , (16389, 2, None, None) , (16389, 2, None, None) , ], 1 , 1 , 4 , 0 , 112 , (3, 0, None, None) , 0 , )),
	(( 'IsDegenerate' , ), 1610678284, (1610678284, (), [ ], 1 , 1 , 4 , 0 , 120 , (3, 0, None, None) , 0 , )),
	(( 'IsPlanar' , ), 1610678285, (1610678285, (), [ ], 1 , 1 , 4 , 0 , 128 , (3, 0, None, None) , 0 , )),
	(( 'IsLineSeg' , ), 1610678286, (1610678286, (), [ ], 1 , 1 , 4 , 0 , 136 , (3, 0, None, None) , 0 , )),
	(( 'IsArc' , ), 1610678287, (1610678287, (), [ ], 1 , 1 , 4 , 0 , 144 , (3, 0, None, None) , 0 , )),
	(( 'IsCircle' , ), 1610678288, (1610678288, (), [ ], 1 , 1 , 4 , 0 , 152 , (3, 0, None, None) , 0 , )),
	(( 'IsEllipse' , ), 1610678289, (1610678289, (), [ ], 1 , 1 , 4 , 0 , 160 , (3, 0, None, None) , 0 , )),
	(( 'IsNurbs' , ), 1610678290, (1610678290, (), [ ], 1 , 1 , 4 , 0 , 168 , (3, 0, None, None) , 0 , )),
	(( 'GetCurveParam' , ), 1610678291, (1610678291, (), [ ], 1 , 1 , 4 , 0 , 176 , (13, 0, None, None) , 0 , )),
	(( 'GetLength' , 'bitVector' , ), 1610678292, (1610678292, (), [ (19, 0, None, None) , ], 1 , 1 , 4 , 0 , 184 , (5, 0, None, None) , 0 , )),
	(( 'NearPointProjection' , 'x' , 'y' , 'z' , 't' , 
			 'ext' , ), 1610678293, (1610678293, (), [ (5, 1, None, None) , (5, 1, None, None) , (5, 1, None, None) , 
			 (16389, 2, None, None) , (3, 1, None, None) , ], 1 , 1 , 4 , 0 , 192 , (3, 0, None, None) , 0 , )),
	(( 'GetNurbs3dParam' , ), 1610678294, (1610678294, (), [ ], 1 , 1 , 4 , 0 , 200 , (13, 0, None, IID('{0363CD73-028A-485F-92BF-B4DB4B3E239A}')) , 0 , )),
	(( 'CalculatePolygon' , 'step' , 'points' , ), 1610678295, (1610678295, (), [ (5, 1, None, None) , 
			 (16396, 2, None, None) , ], 1 , 1 , 4 , 0 , 208 , (3, 0, None, None) , 0 , )),
]

ICurvePartArrayDefinition_vtables_dispatch_ = 0
ICurvePartArrayDefinition_vtables_ = [
	(( 'PartArray' , ), 1610678272, (1610678272, (), [ ], 1 , 1 , 4 , 0 , 24 , (13, 0, None, IID('{7AA0E540-0317-11D4-A30E-00C026EE094F}')) , 0 , )),
	(( 'CurveArray' , ), 1610678273, (1610678273, (), [ ], 1 , 1 , 4 , 0 , 32 , (13, 0, None, IID('{7AA0E540-0303-11D4-A30E-00C026EE094F}')) , 0 , )),
	(( 'GetStep' , ), 1610678274, (1610678274, (), [ ], 1 , 1 , 4 , 0 , 40 , (5, 0, None, None) , 0 , )),
	(( 'SetStep' , 'step' , ), 1610678275, (1610678275, (), [ (5, 0, None, None) , ], 1 , 1 , 4 , 0 , 48 , (3, 0, None, None) , 0 , )),
	(( 'GetCount' , ), 1610678276, (1610678276, (), [ ], 1 , 1 , 4 , 0 , 56 , (3, 0, None, None) , 0 , )),
	(( 'SetCount' , 'count' , ), 1610678277, (1610678277, (), [ (3, 0, None, None) , ], 1 , 1 , 4 , 0 , 64 , (3, 0, None, None) , 0 , )),
	(( 'GetFactor' , ), 1610678278, (1610678278, (), [ ], 1 , 1 , 4 , 0 , 72 , (3, 0, None, None) , 0 , )),
	(( 'SetFactor' , 'factor' , ), 1610678279, (1610678279, (), [ (3, 0, None, None) , ], 1 , 1 , 4 , 0 , 80 , (3, 0, None, None) , 0 , )),
	(( 'GetSence' , ), 1610678280, (1610678280, (), [ ], 1 , 1 , 4 , 0 , 88 , (3, 0, None, None) , 0 , )),
	(( 'SetSence' , 'sence' , ), 1610678281, (1610678281, (), [ (3, 0, None, None) , ], 1 , 1 , 4 , 0 , 96 , (3, 0, None, None) , 0 , )),
	(( 'GetKeepAngle' , ), 1610678282, (1610678282, (), [ ], 1 , 1 , 4 , 0 , 104 , (3, 0, None, None) , 0 , )),
	(( 'SetKeepAngle' , 'keepAngle' , ), 1610678283, (1610678283, (), [ (3, 0, None, None) , ], 1 , 1 , 4 , 0 , 112 , (3, 0, None, None) , 0 , )),
	(( 'GetFullCurve' , ), 1610678284, (1610678284, (), [ ], 1 , 1 , 4 , 0 , 120 , (3, 0, None, None) , 0 , )),
	(( 'SetFullCurve' , 'fullCurve' , ), 1610678285, (1610678285, (), [ (3, 0, None, None) , ], 1 , 1 , 4 , 0 , 128 , (3, 0, None, None) , 0 , )),
	(( 'DeletedCollection' , ), 1610678286, (1610678286, (), [ ], 1 , 1 , 4 , 0 , 136 , (13, 0, None, IID('{BEC3920D-6238-401A-86A3-A600570F47A4}')) , 0 , )),
]

ICutByPlaneDefinition_vtables_dispatch_ = 0
ICutByPlaneDefinition_vtables_ = [
	(( 'GetPlane' , ), 1610678272, (1610678272, (), [ ], 1 , 1 , 4 , 0 , 24 , (13, 0, None, IID('{7AA0E540-0301-11D4-A30E-00C026EE094F}')) , 0 , )),
	(( 'SetPlane' , 'plane' , ), 1610678273, (1610678273, (), [ (13, 0, None, "IID('{7AA0E540-0301-11D4-A30E-00C026EE094F}')") , ], 1 , 1 , 4 , 0 , 32 , (3, 0, None, None) , 0 , )),
	(( 'GetDirection' , ), 1610678274, (1610678274, (), [ ], 1 , 1 , 4 , 0 , 40 , (3, 0, None, None) , 0 , )),
	(( 'SetDirection' , 'direction' , ), 1610678275, (1610678275, (), [ (3, 0, None, None) , ], 1 , 1 , 4 , 0 , 48 , (3, 0, None, None) , 0 , )),
	(( 'ChooseBodies' , ), 1610678276, (1610678276, (), [ ], 1 , 1 , 4 , 0 , 56 , (13, 0, None, IID('{67B417BA-F248-4B56-AD03-C4057C7F2EEE}')) , 0 , )),
	(( 'ChooseParts' , ), 1610678277, (1610678277, (), [ ], 1 , 1 , 4 , 0 , 64 , (13, 0, None, IID('{2920B89D-636E-4DCC-8E62-34D2F4B4BB00}')) , 0 , )),
	(( 'SetChooseType' , 'val' , ), 1610678278, (1610678278, (), [ (3, 0, None, None) , ], 1 , 1 , 4 , 0 , 72 , (3, 0, None, None) , 0 , )),
	(( 'GetChooseType' , ), 1610678279, (1610678279, (), [ ], 1 , 1 , 4 , 0 , 80 , (3, 0, None, None) , 0 , )),
]

ICutBySketchDefinition_vtables_dispatch_ = 0
ICutBySketchDefinition_vtables_ = [
	(( 'GetSketch' , ), 1610678272, (1610678272, (), [ ], 1 , 1 , 4 , 0 , 24 , (13, 0, None, IID('{7AA0E540-0301-11D4-A30E-00C026EE094F}')) , 0 , )),
	(( 'SetSketch' , 'sketch' , ), 1610678273, (1610678273, (), [ (13, 0, None, "IID('{7AA0E540-0301-11D4-A30E-00C026EE094F}')") , ], 1 , 1 , 4 , 0 , 32 , (3, 0, None, None) , 0 , )),
	(( 'GetDirection' , ), 1610678274, (1610678274, (), [ ], 1 , 1 , 4 , 0 , 40 , (3, 0, None, None) , 0 , )),
	(( 'SetDirection' , 'direction' , ), 1610678275, (1610678275, (), [ (3, 0, None, None) , ], 1 , 1 , 4 , 0 , 48 , (3, 0, None, None) , 0 , )),
	(( 'ChooseBodies' , ), 1610678276, (1610678276, (), [ ], 1 , 1 , 4 , 0 , 56 , (13, 0, None, IID('{67B417BA-F248-4B56-AD03-C4057C7F2EEE}')) , 0 , )),
	(( 'ChooseParts' , ), 1610678277, (1610678277, (), [ ], 1 , 1 , 4 , 0 , 64 , (13, 0, None, IID('{2920B89D-636E-4DCC-8E62-34D2F4B4BB00}')) , 0 , )),
	(( 'SetChooseType' , 'val' , ), 1610678278, (1610678278, (), [ (3, 0, None, None) , ], 1 , 1 , 4 , 0 , 72 , (3, 0, None, None) , 0 , )),
	(( 'GetChooseType' , ), 1610678279, (1610678279, (), [ ], 1 , 1 , 4 , 0 , 80 , (3, 0, None, None) , 0 , )),
]

ICutEvolutionDefinition_vtables_dispatch_ = 0
ICutEvolutionDefinition_vtables_ = [
	(( 'SetSketch' , 'sketch' , ), 1610678272, (1610678272, (), [ (13, 0, None, "IID('{7AA0E540-0301-11D4-A30E-00C026EE094F}')") , ], 1 , 1 , 4 , 0 , 24 , (3, 0, None, None) , 0 , )),
	(( 'GetSketch' , ), 1610678273, (1610678273, (), [ ], 1 , 1 , 4 , 0 , 32 , (13, 0, None, IID('{7AA0E540-0301-11D4-A30E-00C026EE094F}')) , 0 , )),
	(( 'PathPartArray' , ), 1610678274, (1610678274, (), [ ], 1 , 1 , 4 , 0 , 40 , (13, 0, None, IID('{7AA0E540-0303-11D4-A30E-00C026EE094F}')) , 0 , )),
	(( 'GetSketchShiftType' , ), 1610678275, (1610678275, (), [ ], 1 , 1 , 4 , 0 , 48 , (2, 0, None, None) , 0 , )),
	(( 'SetSketchShiftType' , 'sketchShiftType' , ), 1610678276, (1610678276, (), [ (2, 0, None, None) , ], 1 , 1 , 4 , 0 , 56 , (3, 0, None, None) , 0 , )),
	(( 'GetCut' , ), 1610678277, (1610678277, (), [ ], 1 , 1 , 4 , 0 , 64 , (3, 0, None, None) , 0 , )),
	(( 'SetCut' , 'cut' , ), 1610678278, (1610678278, (), [ (3, 0, None, None) , ], 1 , 1 , 4 , 0 , 72 , (3, 0, None, None) , 0 , )),
	(( 'GetThinParam' , 'thin' , 'thinType' , 'normalThickness' , 'reverseThickness' , 
			 ), 1610678279, (1610678279, (), [ (16387, 0, None, None) , (16401, 0, None, None) , (16389, 0, None, None) , (16389, 0, None, None) , ], 1 , 1 , 4 , 0 , 80 , (3, 0, None, None) , 0 , )),
	(( 'SetThinParam' , 'thin' , 'thinType' , 'normalThickness' , 'reverseThickness' , 
			 ), 1610678280, (1610678280, (), [ (3, 0, None, None) , (17, 0, None, None) , (5, 0, None, None) , (5, 0, None, None) , ], 1 , 1 , 4 , 0 , 88 , (24, 0, None, None) , 0 , )),
	(( 'ThinParam' , ), 1610678281, (1610678281, (), [ ], 1 , 1 , 4 , 0 , 96 , (13, 0, None, IID('{7AA0E540-0306-11D4-A30E-00C026EE094F}')) , 0 , )),
	(( 'ChooseBodies' , ), 1610678282, (1610678282, (), [ ], 1 , 1 , 4 , 0 , 104 , (13, 0, None, IID('{67B417BA-F248-4B56-AD03-C4057C7F2EEE}')) , 0 , )),
	(( 'ChooseParts' , ), 1610678283, (1610678283, (), [ ], 1 , 1 , 4 , 0 , 112 , (13, 0, None, IID('{2920B89D-636E-4DCC-8E62-34D2F4B4BB00}')) , 0 , )),
	(( 'SetChooseType' , 'val' , ), 1610678284, (1610678284, (), [ (3, 0, None, None) , ], 1 , 1 , 4 , 0 , 120 , (3, 0, None, None) , 0 , )),
	(( 'GetChooseType' , ), 1610678285, (1610678285, (), [ ], 1 , 1 , 4 , 0 , 128 , (3, 0, None, None) , 0 , )),
	(( 'GetPathLength' , 'bitVector' , ), 1610678286, (1610678286, (), [ (19, 0, None, None) , ], 1 , 1 , 4 , 0 , 136 , (5, 0, None, None) , 0 , )),
]

ICutExtrusionDefinition_vtables_dispatch_ = 0
ICutExtrusionDefinition_vtables_ = [
	(( 'SetSketch' , 'name' , ), 1610678272, (1610678272, (), [ (13, 0, None, "IID('{7AA0E540-0301-11D4-A30E-00C026EE094F}')") , ], 1 , 1 , 4 , 0 , 24 , (3, 0, None, None) , 0 , )),
	(( 'GetSketch' , ), 1610678273, (1610678273, (), [ ], 1 , 1 , 4 , 0 , 32 , (13, 0, None, IID('{7AA0E540-0301-11D4-A30E-00C026EE094F}')) , 0 , )),
	(( 'GetSideParam' , 'forward' , 'type' , 'depth' , 'draftValue' , 
			 'draftOutward' , ), 1610678274, (1610678274, (), [ (3, 0, None, None) , (16401, 0, None, None) , (16389, 0, None, None) , 
			 (16389, 0, None, None) , (16387, 0, None, None) , ], 1 , 1 , 4 , 0 , 40 , (3, 0, None, None) , 0 , )),
	(( 'SetSideParam' , 'forward' , 'type' , 'depth' , 'depthToObj' , 
			 'draftOutward' , ), 1610678275, (1610678275, (), [ (3, 0, None, None) , (17, 0, None, None) , (5, 0, None, None) , 
			 (5, 0, None, None) , (3, 0, None, None) , ], 1 , 1 , 4 , 0 , 48 , (24, 0, None, None) , 0 , )),
	(( 'GetThinParam' , 'thin' , 'thinType' , 'normalThickness' , 'reverseThickness' , 
			 ), 1610678276, (1610678276, (), [ (16387, 0, None, None) , (16401, 0, None, None) , (16389, 0, None, None) , (16389, 0, None, None) , ], 1 , 1 , 4 , 0 , 56 , (3, 0, None, None) , 0 , )),
	(( 'SetThinParam' , 'thin' , 'thinType' , 'normalThickness' , 'reverseThickness' , 
			 ), 1610678277, (1610678277, (), [ (3, 0, None, None) , (17, 0, None, None) , (5, 0, None, None) , (5, 0, None, None) , ], 1 , 1 , 4 , 0 , 64 , (24, 0, None, None) , 0 , )),
	(( 'SetDirectionType' , 'dirType' , ), 1610678278, (1610678278, (), [ (3, 0, None, None) , ], 1 , 1 , 4 , 0 , 72 , (3, 0, None, None) , 0 , )),
	(( 'GetDirectionType' , ), 1610678279, (1610678279, (), [ ], 1 , 1 , 4 , 0 , 80 , (3, 0, None, None) , 0 , )),
	(( 'ThinParam' , ), 1610678280, (1610678280, (), [ ], 1 , 1 , 4 , 0 , 88 , (13, 0, None, IID('{7AA0E540-0306-11D4-A30E-00C026EE094F}')) , 0 , )),
	(( 'ExtrusionParam' , ), 1610678281, (1610678281, (), [ ], 1 , 1 , 4 , 0 , 96 , (13, 0, None, IID('{7AA0E540-0307-11D4-A30E-00C026EE094F}')) , 0 , )),
	(( 'GetCut' , ), 1610678282, (1610678282, (), [ ], 1 , 1 , 4 , 0 , 104 , (3, 0, None, None) , 0 , )),
	(( 'SetCut' , 'cut' , ), 1610678283, (1610678283, (), [ (3, 0, None, None) , ], 1 , 1 , 4 , 0 , 112 , (3, 0, None, None) , 0 , )),
	(( 'GetDepthObject' , 'normal' , ), 1610678284, (1610678284, (), [ (3, 0, None, None) , ], 1 , 1 , 4 , 0 , 120 , (13, 0, None, IID('{7AA0E540-0301-11D4-A30E-00C026EE094F}')) , 0 , )),
	(( 'SetDepthObject' , 'normal' , 'obj' , ), 1610678285, (1610678285, (), [ (3, 0, None, None) , 
			 (13, 0, None, "IID('{7AA0E540-0301-11D4-A30E-00C026EE094F}')") , ], 1 , 1 , 4 , 0 , 128 , (3, 0, None, None) , 0 , )),
	(( 'ResetDepthObject' , 'normal' , ), 1610678286, (1610678286, (), [ (3, 0, None, None) , ], 1 , 1 , 4 , 0 , 136 , (3, 0, None, None) , 0 , )),
	(( 'ChooseBodies' , ), 1610678287, (1610678287, (), [ ], 1 , 1 , 4 , 0 , 144 , (13, 0, None, IID('{67B417BA-F248-4B56-AD03-C4057C7F2EEE}')) , 0 , )),
	(( 'ChooseParts' , ), 1610678288, (1610678288, (), [ ], 1 , 1 , 4 , 0 , 152 , (13, 0, None, IID('{2920B89D-636E-4DCC-8E62-34D2F4B4BB00}')) , 0 , )),
	(( 'SetChooseType' , 'val' , ), 1610678289, (1610678289, (), [ (3, 0, None, None) , ], 1 , 1 , 4 , 0 , 160 , (3, 0, None, None) , 0 , )),
	(( 'GetChooseType' , ), 1610678290, (1610678290, (), [ ], 1 , 1 , 4 , 0 , 168 , (3, 0, None, None) , 0 , )),
]

ICutLoftDefinition_vtables_dispatch_ = 0
ICutLoftDefinition_vtables_ = [
	(( 'GetLoftParam' , 'closed' , 'flipVertex' , 'autoPath' , ), 1610678272, (1610678272, (), [ 
			 (16387, 0, None, None) , (16387, 0, None, None) , (16387, 0, None, None) , ], 1 , 1 , 4 , 0 , 24 , (3, 0, None, None) , 0 , )),
	(( 'SetLoftParam' , 'closed' , 'flipVertex' , 'autoPath' , ), 1610678273, (1610678273, (), [ 
			 (3, 0, None, None) , (3, 0, None, None) , (3, 0, None, None) , ], 1 , 1 , 4 , 0 , 32 , (24, 0, None, None) , 0 , )),
	(( 'GetThinParam' , 'thin' , 'thinType' , 'normalThickness' , 'reverseThickness' , 
			 ), 1610678274, (1610678274, (), [ (16387, 0, None, None) , (16401, 0, None, None) , (16389, 0, None, None) , (16389, 0, None, None) , ], 1 , 1 , 4 , 0 , 40 , (3, 0, None, None) , 0 , )),
	(( 'SetThinParam' , 'thin' , 'thinType' , 'normalThickness' , 'reverseThickness' , 
			 ), 1610678275, (1610678275, (), [ (3, 0, None, None) , (17, 0, None, None) , (5, 0, None, None) , (5, 0, None, None) , ], 1 , 1 , 4 , 0 , 48 , (24, 0, None, None) , 0 , )),
	(( 'ThinParam' , ), 1610678276, (1610678276, (), [ ], 1 , 1 , 4 , 0 , 56 , (13, 0, None, IID('{7AA0E540-0306-11D4-A30E-00C026EE094F}')) , 0 , )),
	(( 'Sketchs' , ), 1610678277, (1610678277, (), [ ], 1 , 1 , 4 , 0 , 64 , (13, 0, None, IID('{7AA0E540-0303-11D4-A30E-00C026EE094F}')) , 0 , )),
	(( 'GetCut' , ), 1610678278, (1610678278, (), [ ], 1 , 1 , 4 , 0 , 72 , (3, 0, None, None) , 0 , )),
	(( 'SetCut' , 'cut' , ), 1610678279, (1610678279, (), [ (3, 0, None, None) , ], 1 , 1 , 4 , 0 , 80 , (3, 0, None, None) , 0 , )),
	(( 'ChooseBodies' , ), 1610678280, (1610678280, (), [ ], 1 , 1 , 4 , 0 , 88 , (13, 0, None, IID('{67B417BA-F248-4B56-AD03-C4057C7F2EEE}')) , 0 , )),
	(( 'GetDirectionalLine' , ), 1610678281, (1610678281, (), [ ], 1 , 1 , 4 , 0 , 96 , (13, 0, None, IID('{7AA0E540-0301-11D4-A30E-00C026EE094F}')) , 0 , )),
	(( 'SetDirectionalLine' , 'sketch' , ), 1610678282, (1610678282, (), [ (13, 0, None, "IID('{7AA0E540-0301-11D4-A30E-00C026EE094F}')") , ], 1 , 1 , 4 , 0 , 104 , (3, 0, None, None) , 0 , )),
	(( 'ChooseParts' , ), 1610678283, (1610678283, (), [ ], 1 , 1 , 4 , 0 , 112 , (13, 0, None, IID('{2920B89D-636E-4DCC-8E62-34D2F4B4BB00}')) , 0 , )),
	(( 'SetChooseType' , 'val' , ), 1610678284, (1610678284, (), [ (3, 0, None, None) , ], 1 , 1 , 4 , 0 , 120 , (3, 0, None, None) , 0 , )),
	(( 'GetChooseType' , ), 1610678285, (1610678285, (), [ ], 1 , 1 , 4 , 0 , 128 , (3, 0, None, None) , 0 , )),
]

ICutRotatedDefinition_vtables_dispatch_ = 0
ICutRotatedDefinition_vtables_ = [
	(( 'SetSketch' , 'name' , ), 1610678272, (1610678272, (), [ (13, 0, None, "IID('{7AA0E540-0301-11D4-A30E-00C026EE094F}')") , ], 1 , 1 , 4 , 0 , 24 , (3, 0, None, None) , 0 , )),
	(( 'GetSketch' , ), 1610678273, (1610678273, (), [ ], 1 , 1 , 4 , 0 , 32 , (13, 0, None, IID('{7AA0E540-0301-11D4-A30E-00C026EE094F}')) , 0 , )),
	(( 'GetSideParam' , 'forward' , 'angle' , ), 1610678274, (1610678274, (), [ (3, 0, None, None) , 
			 (16389, 0, None, None) , ], 1 , 1 , 4 , 0 , 40 , (3, 0, None, None) , 0 , )),
	(( 'SetSideParam' , 'forward' , 'angle' , ), 1610678275, (1610678275, (), [ (3, 0, None, None) , 
			 (5, 0, None, None) , ], 1 , 1 , 4 , 0 , 48 , (24, 0, None, None) , 0 , )),
	(( 'GetThinParam' , 'thin' , 'thinType' , 'normalThickness' , 'reverseThickness' , 
			 ), 1610678276, (1610678276, (), [ (16387, 0, None, None) , (16401, 0, None, None) , (16389, 0, None, None) , (16389, 0, None, None) , ], 1 , 1 , 4 , 0 , 56 , (3, 0, None, None) , 0 , )),
	(( 'SetThinParam' , 'thin' , 'thinType' , 'normalThickness' , 'reverseThickness' , 
			 ), 1610678277, (1610678277, (), [ (3, 0, None, None) , (17, 0, None, None) , (5, 0, None, None) , (5, 0, None, None) , ], 1 , 1 , 4 , 0 , 64 , (24, 0, None, None) , 0 , )),
	(( 'SetDirectionType' , 'dirType' , ), 1610678278, (1610678278, (), [ (3, 0, None, None) , ], 1 , 1 , 4 , 0 , 72 , (3, 0, None, None) , 0 , )),
	(( 'GetDirectionType' , ), 1610678279, (1610678279, (), [ ], 1 , 1 , 4 , 0 , 80 , (3, 0, None, None) , 0 , )),
	(( 'SetToroidShapeType' , 'dirType' , ), 1610678280, (1610678280, (), [ (3, 0, None, None) , ], 1 , 1 , 4 , 0 , 88 , (3, 0, None, None) , 0 , )),
	(( 'GetToroidShapeType' , ), 1610678281, (1610678281, (), [ ], 1 , 1 , 4 , 0 , 96 , (3, 0, None, None) , 0 , )),
	(( 'ThinParam' , ), 1610678282, (1610678282, (), [ ], 1 , 1 , 4 , 0 , 104 , (13, 0, None, IID('{7AA0E540-0306-11D4-A30E-00C026EE094F}')) , 0 , )),
	(( 'RotatedParam' , ), 1610678283, (1610678283, (), [ ], 1 , 1 , 4 , 0 , 112 , (13, 0, None, IID('{7AA0E540-0308-11D4-A30E-00C026EE094F}')) , 0 , )),
	(( 'GetCut' , ), 1610678284, (1610678284, (), [ ], 1 , 1 , 4 , 0 , 120 , (3, 0, None, None) , 0 , )),
	(( 'SetCut' , 'cut' , ), 1610678285, (1610678285, (), [ (3, 0, None, None) , ], 1 , 1 , 4 , 0 , 128 , (3, 0, None, None) , 0 , )),
	(( 'ChooseBodies' , ), 1610678286, (1610678286, (), [ ], 1 , 1 , 4 , 0 , 136 , (13, 0, None, IID('{67B417BA-F248-4B56-AD03-C4057C7F2EEE}')) , 0 , )),
	(( 'ChooseParts' , ), 1610678287, (1610678287, (), [ ], 1 , 1 , 4 , 0 , 144 , (13, 0, None, IID('{2920B89D-636E-4DCC-8E62-34D2F4B4BB00}')) , 0 , )),
	(( 'SetChooseType' , 'val' , ), 1610678288, (1610678288, (), [ (3, 0, None, None) , ], 1 , 1 , 4 , 0 , 152 , (3, 0, None, None) , 0 , )),
	(( 'GetChooseType' , ), 1610678289, (1610678289, (), [ ], 1 , 1 , 4 , 0 , 160 , (3, 0, None, None) , 0 , )),
]

ICylinderParam_vtables_dispatch_ = 0
ICylinderParam_vtables_ = [
	(( 'GetRadius' , ), 1610678272, (1610678272, (), [ ], 1 , 1 , 4 , 0 , 24 , (5, 0, None, None) , 0 , )),
	(( 'GetHeight' , ), 1610678273, (1610678273, (), [ ], 1 , 1 , 4 , 0 , 32 , (5, 0, None, None) , 0 , )),
	(( 'GetPlacement' , ), 1610678274, (1610678274, (), [ ], 1 , 1 , 4 , 0 , 40 , (13, 0, None, IID('{7AA0E540-0310-11D4-A30E-00C026EE094F}')) , 0 , )),
]

ICylindricSpiralDefinition_vtables_dispatch_ = 0
ICylindricSpiralDefinition_vtables_ = [
	(( 'GetTurn' , ), 1610678272, (1610678272, (), [ ], 1 , 1 , 4 , 0 , 24 , (5, 0, None, None) , 0 , )),
	(( 'SetTurn' , 'turn' , ), 1610678273, (1610678273, (), [ (5, 0, None, None) , ], 1 , 1 , 4 , 0 , 32 , (3, 0, None, None) , 0 , )),
	(( 'GetStep' , ), 1610678274, (1610678274, (), [ ], 1 , 1 , 4 , 0 , 40 , (5, 0, None, None) , 0 , )),
	(( 'SetStep' , 'step' , ), 1610678275, (1610678275, (), [ (5, 0, None, None) , ], 1 , 1 , 4 , 0 , 48 , (3, 0, None, None) , 0 , )),
	(( 'GetTurnDir' , ), 1610678276, (1610678276, (), [ ], 1 , 1 , 4 , 0 , 56 , (3, 0, None, None) , 0 , )),
	(( 'SetTurnDir' , 'turnDir' , ), 1610678277, (1610678277, (), [ (3, 0, None, None) , ], 1 , 1 , 4 , 0 , 64 , (3, 0, None, None) , 0 , )),
	(( 'GetPlane' , ), 1610678278, (1610678278, (), [ ], 1 , 1 , 4 , 0 , 72 , (13, 0, None, IID('{7AA0E540-0301-11D4-A30E-00C026EE094F}')) , 0 , )),
	(( 'SetPlane' , 'plane' , ), 1610678279, (1610678279, (), [ (13, 0, None, "IID('{7AA0E540-0301-11D4-A30E-00C026EE094F}')") , ], 1 , 1 , 4 , 0 , 80 , (3, 0, None, None) , 0 , )),
	(( 'GetLocation' , 'x' , 'y' , ), 1610678280, (1610678280, (), [ (16389, 0, None, None) , 
			 (16389, 0, None, None) , ], 1 , 1 , 4 , 0 , 88 , (3, 0, None, None) , 0 , )),
	(( 'SetLocation' , 'x' , 'y' , ), 1610678281, (1610678281, (), [ (5, 0, None, None) , 
			 (5, 0, None, None) , ], 1 , 1 , 4 , 0 , 96 , (3, 0, None, None) , 0 , )),
	(( 'GetBuildMode' , ), 1610678282, (1610678282, (), [ ], 1 , 1 , 4 , 0 , 104 , (2, 0, None, None) , 0 , )),
	(( 'SetBuildMode' , 'buildMode' , ), 1610678283, (1610678283, (), [ (2, 0, None, None) , ], 1 , 1 , 4 , 0 , 112 , (3, 0, None, None) , 0 , )),
	(( 'GetBuildDir' , ), 1610678284, (1610678284, (), [ ], 1 , 1 , 4 , 0 , 120 , (3, 0, None, None) , 0 , )),
	(( 'SetBuildDir' , 'buildDir' , ), 1610678285, (1610678285, (), [ (3, 0, None, None) , ], 1 , 1 , 4 , 0 , 128 , (3, 0, None, None) , 0 , )),
	(( 'GetHeight' , ), 1610678286, (1610678286, (), [ ], 1 , 1 , 4 , 0 , 136 , (5, 0, None, None) , 0 , )),
	(( 'SetHeight' , 'height' , ), 1610678287, (1610678287, (), [ (5, 0, None, None) , ], 1 , 1 , 4 , 0 , 144 , (3, 0, None, None) , 0 , )),
	(( 'GetHeightType' , ), 1610678288, (1610678288, (), [ ], 1 , 1 , 4 , 0 , 152 , (2, 0, None, None) , 0 , )),
	(( 'SetHeightType' , 'heightType' , ), 1610678289, (1610678289, (), [ (2, 0, None, None) , ], 1 , 1 , 4 , 0 , 160 , (3, 0, None, None) , 0 , )),
	(( 'GetHeightAdd' , ), 1610678290, (1610678290, (), [ ], 1 , 1 , 4 , 0 , 168 , (5, 0, None, None) , 0 , )),
	(( 'SetHeightAdd' , 'heightAdd' , ), 1610678291, (1610678291, (), [ (5, 0, None, None) , ], 1 , 1 , 4 , 0 , 176 , (3, 0, None, None) , 0 , )),
	(( 'GetHeightAddHow' , ), 1610678292, (1610678292, (), [ ], 1 , 1 , 4 , 0 , 184 , (3, 0, None, None) , 0 , )),
	(( 'SetHeightAddHow' , 'heightAddHow' , ), 1610678293, (1610678293, (), [ (3, 0, None, None) , ], 1 , 1 , 4 , 0 , 192 , (3, 0, None, None) , 0 , )),
	(( 'SetHeightObject' , 'heightObject' , ), 1610678294, (1610678294, (), [ (13, 0, None, "IID('{7AA0E540-0301-11D4-A30E-00C026EE094F}')") , ], 1 , 1 , 4 , 0 , 200 , (3, 0, None, None) , 0 , )),
	(( 'GetHeightObject' , ), 1610678295, (1610678295, (), [ ], 1 , 1 , 4 , 0 , 208 , (13, 0, None, IID('{7AA0E540-0301-11D4-A30E-00C026EE094F}')) , 0 , )),
	(( 'GetDiam' , ), 1610678296, (1610678296, (), [ ], 1 , 1 , 4 , 0 , 216 , (5, 0, None, None) , 0 , )),
	(( 'SetDiam' , 'diamType' , ), 1610678297, (1610678297, (), [ (5, 0, None, None) , ], 1 , 1 , 4 , 0 , 224 , (3, 0, None, None) , 0 , )),
	(( 'GetDiamType' , ), 1610678298, (1610678298, (), [ ], 1 , 1 , 4 , 0 , 232 , (2, 0, None, None) , 0 , )),
	(( 'SetDiamType' , 'diamType' , ), 1610678299, (1610678299, (), [ (2, 0, None, None) , ], 1 , 1 , 4 , 0 , 240 , (3, 0, None, None) , 0 , )),
	(( 'GetDiamObject' , ), 1610678300, (1610678300, (), [ ], 1 , 1 , 4 , 0 , 248 , (13, 0, None, IID('{7AA0E540-0301-11D4-A30E-00C026EE094F}')) , 0 , )),
	(( 'SetDiamObject' , 'diamObject' , ), 1610678301, (1610678301, (), [ (13, 0, None, "IID('{7AA0E540-0301-11D4-A30E-00C026EE094F}')") , ], 1 , 1 , 4 , 0 , 256 , (3, 0, None, None) , 0 , )),
	(( 'GetFirstAngle' , ), 1610678302, (1610678302, (), [ ], 1 , 1 , 4 , 0 , 264 , (5, 0, None, None) , 0 , )),
	(( 'SetFirstAngle' , 'firstAngle' , ), 1610678303, (1610678303, (), [ (5, 0, None, None) , ], 1 , 1 , 4 , 0 , 272 , (3, 0, None, None) , 0 , )),
	(( 'GetSketch' , ), 1610678304, (1610678304, (), [ ], 1 , 1 , 4 , 0 , 280 , (13, 0, None, IID('{7AA0E540-0301-11D4-A30E-00C026EE094F}')) , 0 , )),
	(( 'GetCurve3D' , ), 1610678305, (1610678305, (), [ ], 1 , 1 , 4 , 0 , 288 , (13, 0, None, IID('{E5066490-773D-4289-A60B-2FC19865174A}')) , 0 , )),
]

IDefaultObject_vtables_dispatch_ = 0
IDefaultObject_vtables_ = [
	(( 'GetSurface' , ), 1610678272, (1610678272, (), [ ], 1 , 1 , 4 , 0 , 24 , (13, 0, None, IID('{081C7F2D-D5BC-40A6-92FE-C16B67D10B75}')) , 0 , )),
	(( 'GetCurve3D' , ), 1610678273, (1610678273, (), [ ], 1 , 1 , 4 , 0 , 32 , (13, 0, None, IID('{E5066490-773D-4289-A60B-2FC19865174A}')) , 0 , )),
]

IDeletedCopyCollection_vtables_dispatch_ = 0
IDeletedCopyCollection_vtables_ = [
	(( 'Refresh' , ), 1610678272, (1610678272, (), [ ], 1 , 1 , 4 , 0 , 24 , (3, 0, None, None) , 0 , )),
	(( 'GetCount' , ), 1610678273, (1610678273, (), [ ], 1 , 1 , 4 , 0 , 32 , (3, 0, None, None) , 0 , )),
	(( 'First' , 'index1' , 'index2' , ), 1610678274, (1610678274, (), [ (16387, 0, None, None) , 
			 (16387, 0, None, None) , ], 1 , 1 , 4 , 0 , 40 , (3, 0, None, None) , 0 , )),
	(( 'Last' , 'index1' , 'index2' , ), 1610678275, (1610678275, (), [ (16387, 0, None, None) , 
			 (16387, 0, None, None) , ], 1 , 1 , 4 , 0 , 48 , (3, 0, None, None) , 0 , )),
	(( 'Next' , 'index1' , 'index2' , ), 1610678276, (1610678276, (), [ (16387, 0, None, None) , 
			 (16387, 0, None, None) , ], 1 , 1 , 4 , 0 , 56 , (3, 0, None, None) , 0 , )),
	(( 'Prev' , 'index1' , 'index2' , ), 1610678277, (1610678277, (), [ (16387, 0, None, None) , 
			 (16387, 0, None, None) , ], 1 , 1 , 4 , 0 , 64 , (3, 0, None, None) , 0 , )),
	(( 'GetByIndex' , 'index' , 'index1' , 'index2' , ), 1610678278, (1610678278, (), [ 
			 (3, 0, None, None) , (16387, 0, None, None) , (16387, 0, None, None) , ], 1 , 1 , 4 , 0 , 72 , (3, 0, None, None) , 0 , )),
	(( 'Add' , 'index1' , 'index2' , ), 1610678279, (1610678279, (), [ (3, 0, None, None) , 
			 (3, 0, None, None) , ], 1 , 1 , 4 , 0 , 80 , (3, 0, None, None) , 0 , )),
	(( 'AddAt' , 'index1' , 'index2' , 'index' , ), 1610678280, (1610678280, (), [ 
			 (3, 0, None, None) , (3, 0, None, None) , (3, 0, None, None) , ], 1 , 1 , 4 , 0 , 88 , (3, 0, None, None) , 0 , )),
	(( 'DetachByIndex' , 'index' , ), 1610678281, (1610678281, (), [ (3, 0, None, None) , ], 1 , 1 , 4 , 0 , 96 , (3, 0, None, None) , 0 , )),
	(( 'DetachByBody' , 'index1' , 'index2' , ), 1610678282, (1610678282, (), [ (3, 0, None, None) , 
			 (3, 0, None, None) , ], 1 , 1 , 4 , 0 , 104 , (3, 0, None, None) , 0 , )),
	(( 'Clear' , ), 1610678283, (1610678283, (), [ ], 1 , 1 , 4 , 0 , 112 , (3, 0, None, None) , 0 , )),
	(( 'SetByIndex' , 'index1' , 'index2' , 'index' , ), 1610678284, (1610678284, (), [ 
			 (3, 0, None, None) , (3, 0, None, None) , (3, 0, None, None) , ], 1 , 1 , 4 , 0 , 120 , (3, 0, None, None) , 0 , )),
	(( 'FindIt' , 'index1' , 'index2' , ), 1610678285, (1610678285, (), [ (3, 0, None, None) , 
			 (3, 0, None, None) , ], 1 , 1 , 4 , 0 , 128 , (19, 0, None, None) , 0 , )),
]

IDerivativePartArrayDefinition_vtables_dispatch_ = 0
IDerivativePartArrayDefinition_vtables_ = [
	(( 'PartArray' , ), 1610678272, (1610678272, (), [ ], 1 , 1 , 4 , 0 , 24 , (13, 0, None, IID('{7AA0E540-0317-11D4-A30E-00C026EE094F}')) , 0 , )),
	(( 'SetDeriv' , 'deriv' , ), 1610678273, (1610678273, (), [ (13, 0, None, "IID('{7AA0E540-0301-11D4-A30E-00C026EE094F}')") , ], 1 , 1 , 4 , 0 , 32 , (3, 0, None, None) , 0 , )),
	(( 'GetDeriv' , ), 1610678274, (1610678274, (), [ ], 1 , 1 , 4 , 0 , 40 , (13, 0, None, IID('{7AA0E540-0301-11D4-A30E-00C026EE094F}')) , 0 , )),
	(( 'DeletedCollection' , ), 1610678275, (1610678275, (), [ ], 1 , 1 , 4 , 0 , 48 , (13, 0, None, IID('{BEC3920D-6238-401A-86A3-A600570F47A4}')) , 0 , )),
]

IDocument3D_vtables_dispatch_ = 0
IDocument3D_vtables_ = [
	(( 'UpdateDocumentParam' , ), 1610678272, (1610678272, (), [ ], 1 , 1 , 4 , 0 , 24 , (3, 0, None, None) , 0 , )),
	(( 'GetFileName' , ), 1610678273, (1610678273, (), [ ], 1 , 1 , 4 , 0 , 32 , (31, 0, None, None) , 0 , )),
	(( 'SetFileName' , 'name' , ), 1610678274, (1610678274, (), [ (31, 0, None, None) , ], 1 , 1 , 4 , 0 , 40 , (3, 0, None, None) , 0 , )),
	(( 'GetComment' , ), 1610678275, (1610678275, (), [ ], 1 , 1 , 4 , 0 , 48 , (31, 0, None, None) , 0 , )),
	(( 'SetComment' , 'comment' , ), 1610678276, (1610678276, (), [ (31, 0, None, None) , ], 1 , 1 , 4 , 0 , 56 , (3, 0, None, None) , 0 , )),
	(( 'GetAuthor' , ), 1610678277, (1610678277, (), [ ], 1 , 1 , 4 , 0 , 64 , (31, 0, None, None) , 0 , )),
	(( 'SetAuthor' , 'author' , ), 1610678278, (1610678278, (), [ (31, 0, None, None) , ], 1 , 1 , 4 , 0 , 72 , (3, 0, None, None) , 0 , )),
	(( 'IsActive' , ), 1610678279, (1610678279, (), [ ], 1 , 1 , 4 , 0 , 80 , (3, 0, None, None) , 0 , )),
	(( 'SetActive' , ), 1610678280, (1610678280, (), [ ], 1 , 1 , 4 , 0 , 88 , (3, 0, None, None) , 0 , )),
	(( 'GetInvisibleMode' , ), 1610678281, (1610678281, (), [ ], 1 , 1 , 4 , 0 , 96 , (3, 0, None, None) , 0 , )),
	(( 'GetPart' , 'type' , ), 1610678282, (1610678282, (), [ (3, 0, None, None) , ], 1 , 1 , 4 , 0 , 104 , (13, 0, None, IID('{7AA0E540-0300-11D4-A30E-00C026EE094F}')) , 0 , )),
	(( 'Create' , 'invisible' , '_typeDoc' , ), 1610678283, (1610678283, (), [ (3, 0, None, None) , 
			 (3, 0, None, None) , ], 1 , 1 , 4 , 0 , 112 , (3, 0, None, None) , 0 , )),
	(( 'Open' , 'fileName' , 'invisible' , ), 1610678284, (1610678284, (), [ (31, 0, None, None) , 
			 (3, 0, None, None) , ], 1 , 1 , 4 , 0 , 120 , (3, 0, None, None) , 0 , )),
	(( 'Save' , ), 1610678285, (1610678285, (), [ ], 1 , 1 , 4 , 0 , 128 , (3, 0, None, None) , 0 , )),
	(( 'SaveAs' , 'fileName' , ), 1610678286, (1610678286, (), [ (31, 0, None, None) , ], 1 , 1 , 4 , 0 , 136 , (3, 0, None, None) , 0 , )),
	(( 'Close' , ), 1610678287, (1610678287, (), [ ], 1 , 1 , 4 , 0 , 144 , (3, 0, None, None) , 0 , )),
	(( 'UserSelectEntity' , 'defSelectObject' , 'fnFilter' , 'prompt' , ), 1610678288, (1610678288, (), [ 
			 (13, 0, None, "IID('{7AA0E540-0301-11D4-A30E-00C026EE094F}')") , (16408, 0, None, None) , (31, 0, None, None) , ], 1 , 1 , 4 , 0 , 152 , (13, 0, None, IID('{7AA0E540-0301-11D4-A30E-00C026EE094F}')) , 0 , )),
	(( 'UserGetCursor' , 'prompt' , 'x' , 'y' , 'z' , 
			 ), 1610678289, (1610678289, (), [ (31, 0, None, None) , (16389, 0, None, None) , (16389, 0, None, None) , (16389, 0, None, None) , ], 1 , 1 , 4 , 0 , 160 , (3, 0, None, None) , 0 , )),
	(( 'IsEditMode' , ), 1610678290, (1610678290, (), [ ], 1 , 1 , 4 , 0 , 168 , (3, 0, None, None) , 0 , )),
	(( 'GetRequestInfo' , 'part' , ), 1610678291, (1610678291, (), [ (13, 0, None, "IID('{7AA0E540-0300-11D4-A30E-00C026EE094F}')") , ], 1 , 1 , 4 , 0 , 176 , (13, 0, None, IID('{7AA0E540-0313-11D4-A30E-00C026EE094F}')) , 0 , )),
	(( 'UserGetPlacementAndEntity' , 'entityCount' , ), 1610678292, (1610678292, (), [ (3, 0, None, None) , ], 1 , 1 , 4 , 0 , 184 , (3, 0, None, None) , 0 , )),
	(( 'EntityCollection' , 'objType' , 'checkEntity' , ), 1610678293, (1610678293, (), [ (2, 0, None, None) , 
			 (3, 0, None, None) , ], 1 , 1 , 4 , 0 , 192 , (13, 0, None, IID('{7AA0E540-0303-11D4-A30E-00C026EE094F}')) , 0 , )),
	(( 'SetPartFromFile' , 'fileName' , 'part' , 'externalFile' , ), 1610678294, (1610678294, (), [ 
			 (31, 0, None, None) , (13, 0, None, "IID('{7AA0E540-0300-11D4-A30E-00C026EE094F}')") , (3, 0, None, None) , ], 1 , 1 , 4 , 0 , 200 , (3, 0, None, None) , 0 , )),
	(( 'CreatePartFromFile' , 'fileName' , 'part' , 'plane' , ), 1610678295, (1610678295, (), [ 
			 (31, 0, None, None) , (13, 0, None, "IID('{7AA0E540-0300-11D4-A30E-00C026EE094F}')") , (13, 0, None, "IID('{7AA0E540-0301-11D4-A30E-00C026EE094F}')") , ], 1 , 1 , 4 , 0 , 208 , (3, 0, None, None) , 0 , )),
	(( 'IsDetail' , ), 1610678296, (1610678296, (), [ ], 1 , 1 , 4 , 0 , 216 , (3, 0, None, None) , 0 , )),
	(( 'ChangeObjectInLibRequest' , ), 1610678297, (1610678297, (), [ ], 1 , 1 , 4 , 0 , 224 , (3, 0, None, None) , 0 , )),
	(( 'StopLibRequest' , ), 1610678298, (1610678298, (), [ ], 1 , 1 , 4 , 0 , 232 , (3, 0, None, None) , 0 , )),
	(( 'MateConstraintCollection' , ), 1610678299, (1610678299, (), [ ], 1 , 1 , 4 , 0 , 240 , (13, 0, None, IID('{7AA0E540-0304-11D4-A30E-00C026EE094F}')) , 0 , )),
	(( 'AddMateConstraint' , 'constraintType' , 'obj1' , 'obj2' , 'direction' , 
			 'fixed' , 'val' , ), 1610678300, (1610678300, (), [ (3, 0, None, None) , (13, 0, None, "IID('{7AA0E540-0301-11D4-A30E-00C026EE094F}')") , 
			 (13, 0, None, "IID('{7AA0E540-0301-11D4-A30E-00C026EE094F}')") , (2, 0, None, None) , (2, 0, None, None) , (5, 0, None, None) , ], 1 , 1 , 4 , 0 , 248 , (3, 0, None, None) , 0 , )),
	(( 'RemoveMateConstraint' , 'constraintType' , 'obj1' , 'obj2' , ), 1610678301, (1610678301, (), [ 
			 (3, 0, None, None) , (13, 0, None, "IID('{7AA0E540-0301-11D4-A30E-00C026EE094F}')") , (13, 0, None, "IID('{7AA0E540-0301-11D4-A30E-00C026EE094F}')") , ], 1 , 1 , 4 , 0 , 256 , (3, 0, None, None) , 0 , )),
	(( 'GetSpecification' , ), 1610678302, (1610678302, (), [ ], 1 , 1 , 4 , 0 , 264 , (13, 0, None, IID('{7AA0E540-0315-11D4-A30E-00C026EE094F}')) , 0 , )),
	(( 'GetMateConstraint' , ), 1610678303, (1610678303, (), [ ], 1 , 1 , 4 , 0 , 272 , (13, 0, None, IID('{7AA0E540-0314-11D4-A30E-00C026EE094F}')) , 0 , )),
	(( 'PartCollection' , 'Refresh' , ), 1610678304, (1610678304, (), [ (3, 0, None, None) , ], 1 , 1 , 4 , 0 , 280 , (13, 0, None, IID('{7AA0E540-0317-11D4-A30E-00C026EE094F}')) , 0 , )),
	(( 'ZoomPrevNextOrAll' , 'type' , ), 1610678305, (1610678305, (), [ (2, 0, None, None) , ], 1 , 1 , 4 , 0 , 288 , (3, 0, None, None) , 0 , )),
	(( 'RefreshActiveWindow' , ), 1610678306, (1610678306, (), [ ], 1 , 1 , 4 , 0 , 296 , (3, 0, None, None) , 0 , )),
	(( 'CreatePartInAssembly' , 'fileName' , 'plane' , ), 1610678307, (1610678307, (), [ (31, 0, None, None) , 
			 (13, 0, None, "IID('{7AA0E540-0301-11D4-A30E-00C026EE094F}')") , ], 1 , 1 , 4 , 0 , 304 , (13, 0, None, IID('{7AA0E540-0300-11D4-A30E-00C026EE094F}')) , 0 , )),
	(( 'RebuildDocument' , ), 1610678308, (1610678308, (), [ ], 1 , 1 , 4 , 0 , 312 , (3, 0, None, None) , 0 , )),
	(( 'SaveAsToRasterFormat' , 'fileName' , 'par' , ), 1610678309, (1610678309, (), [ (31, 0, None, None) , 
			 (13, 0, None, "IID('{7AA0E540-0318-11D4-A30E-00C026EE094F}')") , ], 1 , 1 , 4 , 0 , 320 , (3, 0, None, None) , 0 , )),
	(( 'SaveAsToAdditionFormat' , 'fileName' , 'par' , ), 1610678310, (1610678310, (), [ (31, 0, None, None) , 
			 (13, 0, None, "IID('{7AA0E540-0319-11D4-A30E-00C026EE094F}')") , ], 1 , 1 , 4 , 0 , 328 , (3, 0, None, None) , 0 , )),
	(( 'RasterFormatParam' , ), 1610678311, (1610678311, (), [ ], 1 , 1 , 4 , 0 , 336 , (13, 0, None, IID('{7AA0E540-0318-11D4-A30E-00C026EE094F}')) , 0 , )),
	(( 'AdditionFormatParam' , ), 1610678312, (1610678312, (), [ ], 1 , 1 , 4 , 0 , 344 , (13, 0, None, IID('{7AA0E540-0319-11D4-A30E-00C026EE094F}')) , 0 , )),
	(( 'SetPerspective' , 'val' , ), 1610678313, (1610678313, (), [ (3, 0, None, None) , ], 1 , 1 , 4 , 0 , 352 , (3, 0, None, None) , 0 , )),
	(( 'GetPerspective' , ), 1610678314, (1610678314, (), [ ], 1 , 1 , 4 , 0 , 360 , (3, 0, None, None) , 0 , )),
	(( 'SetDrawMode' , 'mode' , ), 1610678315, (1610678315, (), [ (3, 0, None, None) , ], 1 , 1 , 4 , 0 , 368 , (3, 0, None, None) , 0 , )),
	(( 'GetDrawMode' , ), 1610678316, (1610678316, (), [ ], 1 , 1 , 4 , 0 , 376 , (3, 0, None, None) , 0 , )),
	(( 'GetViewProjectionCollection' , ), 1610678317, (1610678317, (), [ ], 1 , 1 , 4 , 0 , 384 , (13, 0, None, IID('{F6EDDAE7-AA95-4474-835E-BEB4BC25BAA8}')) , 0 , )),
	(( 'DeleteObject' , 'obj' , ), 1610678318, (1610678318, (), [ (13, 0, None, None) , ], 1 , 1 , 4 , 0 , 392 , (3, 0, None, None) , 0 , )),
	(( 'GetSelectionMng' , ), 1610678319, (1610678319, (), [ ], 1 , 1 , 4 , 0 , 400 , (13, 0, None, IID('{974E5E66-7948-401D-8DAE-C497A6BF1EBD}')) , 0 , )),
	(( 'GetChooseMng' , ), 1610678320, (1610678320, (), [ ], 1 , 1 , 4 , 0 , 408 , (13, 0, None, IID('{BB679D6E-1C5A-4B90-A559-CB37BA1E1FA7}')) , 0 , )),
	(( 'GetObjectType' , 'obj' , ), 1610678321, (1610678321, (), [ (13, 0, None, None) , ], 1 , 1 , 4 , 0 , 416 , (3, 0, None, None) , 0 , )),
	(( 'SaveAsToUncompressedRasterFormat' , 'fileName' , 'par' , ), 1610678322, (1610678322, (), [ (31, 0, None, None) , 
			 (13, 0, None, "IID('{7AA0E540-0318-11D4-A30E-00C026EE094F}')") , ], 1 , 1 , 4 , 0 , 424 , (3, 0, None, None) , 0 , )),
	(( 'AddImportedSurfaces' , 'fileName' , 'together' , ), 1610678323, (1610678323, (), [ (31, 0, None, None) , 
			 (3, 0, None, None) , ], 1 , 1 , 4 , 0 , 432 , (13, 0, None, IID('{7AA0E540-0303-11D4-A30E-00C026EE094F}')) , 0 , )),
	(( 'SetHideAllPlanes' , 'val' , ), 1610678324, (1610678324, (), [ (3, 0, None, None) , ], 1 , 1 , 4 , 0 , 440 , (3, 0, None, None) , 0 , )),
	(( 'GetHideAllPlanes' , ), 1610678325, (1610678325, (), [ ], 1 , 1 , 4 , 0 , 448 , (3, 0, None, None) , 0 , )),
	(( 'SetHideAllAxis' , 'val' , ), 1610678326, (1610678326, (), [ (3, 0, None, None) , ], 1 , 1 , 4 , 0 , 456 , (3, 0, None, None) , 0 , )),
	(( 'GetHideAllAxis' , ), 1610678327, (1610678327, (), [ ], 1 , 1 , 4 , 0 , 464 , (3, 0, None, None) , 0 , )),
	(( 'SetHideAllSketches' , 'val' , ), 1610678328, (1610678328, (), [ (3, 0, None, None) , ], 1 , 1 , 4 , 0 , 472 , (3, 0, None, None) , 0 , )),
	(( 'GetHideAllSketches' , ), 1610678329, (1610678329, (), [ ], 1 , 1 , 4 , 0 , 480 , (3, 0, None, None) , 0 , )),
	(( 'SetHideAllPlaces' , 'val' , ), 1610678330, (1610678330, (), [ (3, 0, None, None) , ], 1 , 1 , 4 , 0 , 488 , (3, 0, None, None) , 0 , )),
	(( 'GetHideAllPlaces' , ), 1610678331, (1610678331, (), [ ], 1 , 1 , 4 , 0 , 496 , (3, 0, None, None) , 0 , )),
	(( 'SetHideAllSurfaces' , 'val' , ), 1610678332, (1610678332, (), [ (3, 0, None, None) , ], 1 , 1 , 4 , 0 , 504 , (3, 0, None, None) , 0 , )),
	(( 'GetHideAllSurfaces' , ), 1610678333, (1610678333, (), [ ], 1 , 1 , 4 , 0 , 512 , (3, 0, None, None) , 0 , )),
	(( 'SetHideAllThreads' , 'val' , ), 1610678334, (1610678334, (), [ (3, 0, None, None) , ], 1 , 1 , 4 , 0 , 520 , (3, 0, None, None) , 0 , )),
	(( 'GetHideAllThreads' , ), 1610678335, (1610678335, (), [ ], 1 , 1 , 4 , 0 , 528 , (3, 0, None, None) , 0 , )),
	(( 'AttributeCollection' , 'key1' , 'key2' , 'key3' , 'key4' , 
			 'numb' , 'pObj' , ), 1610678336, (1610678336, (), [ (3, 0, None, None) , (3, 0, None, None) , 
			 (3, 0, None, None) , (3, 0, None, None) , (5, 0, None, None) , (13, 0, None, None) , ], 1 , 1 , 4 , 0 , 536 , (13, 0, None, IID('{E17C2BE7-9C11-4FB3-ADBD-04EC912784E8}')) , 0 , )),
	(( 'FeatureCollection' , 'key1' , 'key2' , 'key3' , 'key4' , 
			 'numb' , 'objType' , ), 1610678337, (1610678337, (), [ (3, 0, None, None) , (3, 0, None, None) , 
			 (3, 0, None, None) , (3, 0, None, None) , (5, 0, None, None) , (3, 0, None, None) , ], 1 , 1 , 4 , 0 , 544 , (13, 0, None, IID('{CE5D4888-9006-43AC-9ACC-6D9E58B408B4}')) , 0 , )),
	(( 'SetPartFromFileEx' , 'fileName' , 'part' , 'externalFile' , 'redraw' , 
			 ), 1610678338, (1610678338, (), [ (31, 0, None, None) , (13, 0, None, "IID('{7AA0E540-0300-11D4-A30E-00C026EE094F}')") , (3, 0, None, None) , (3, 0, None, None) , ], 1 , 1 , 4 , 0 , 552 , (3, 0, None, None) , 0 , )),
	(( 'ComponentPositioner' , ), 1610678339, (1610678339, (), [ ], 1 , 1 , 4 , 0 , 560 , (13, 0, None, IID('{6B9D0CE9-C3E6-436B-9EEE-02F439A45C02}')) , 0 , )),
	(( 'DefaultPlacement' , ), 1610678340, (1610678340, (), [ ], 1 , 1 , 4 , 0 , 568 , (13, 0, None, IID('{7AA0E540-0310-11D4-A30E-00C026EE094F}')) , 0 , )),
	(( 'SetShadedWireframe' , 'val' , ), 1610678341, (1610678341, (), [ (3, 0, None, None) , ], 1 , 1 , 4 , 0 , 576 , (3, 0, None, None) , 0 , )),
	(( 'GetShadedWireframe' , ), 1610678342, (1610678342, (), [ ], 1 , 1 , 4 , 0 , 584 , (3, 0, None, None) , 0 , )),
	(( 'GetEditMacroObject' , ), 1610678343, (1610678343, (), [ ], 1 , 1 , 4 , 0 , 592 , (13, 0, None, IID('{7AA0E540-0301-11D4-A30E-00C026EE094F}')) , 0 , )),
	(( 'SaveAsEx' , 'fileName' , 'saveMode' , ), 1610678344, (1610678344, (), [ (31, 0, None, None) , 
			 (3, 0, None, None) , ], 1 , 1 , 4 , 0 , 600 , (3, 0, None, None) , 0 , )),
	(( 'GetInterface' , 'o3dType' , ), 1610678345, (1610678345, (), [ (3, 0, None, None) , ], 1 , 1 , 4 , 0 , 608 , (13, 0, None, None) , 0 , )),
	(( 'GetDismantleMode' , ), 1610678346, (1610678346, (), [ ], 1 , 1 , 4 , 0 , 616 , (3, 0, None, None) , 0 , )),
	(( 'SetDismantleMode' , 'val' , ), 1610678347, (1610678347, (), [ (3, 0, None, None) , ], 1 , 1 , 4 , 0 , 624 , (3, 0, None, None) , 0 , )),
	(( 'SetHideAllCurves' , 'val' , ), 1610678348, (1610678348, (), [ (3, 0, None, None) , ], 1 , 1 , 4 , 0 , 632 , (3, 0, None, None) , 0 , )),
	(( 'GetHideAllCurves' , ), 1610678349, (1610678349, (), [ ], 1 , 1 , 4 , 0 , 640 , (3, 0, None, None) , 0 , )),
	(( 'SetHideAllControlPoints' , 'val' , ), 1610678350, (1610678350, (), [ (3, 0, None, None) , ], 1 , 1 , 4 , 0 , 648 , (3, 0, None, None) , 0 , )),
	(( 'GetHideAllControlPoints' , ), 1610678351, (1610678351, (), [ ], 1 , 1 , 4 , 0 , 656 , (3, 0, None, None) , 0 , )),
	(( 'CopyPart' , 'sourcePart' , 'newPlacement' , ), 1610678352, (1610678352, (), [ (13, 0, None, "IID('{7AA0E540-0300-11D4-A30E-00C026EE094F}')") , 
			 (13, 0, None, "IID('{7AA0E540-0310-11D4-A30E-00C026EE094F}')") , ], 1 , 1 , 4 , 0 , 664 , (13, 0, None, IID('{7AA0E540-0300-11D4-A30E-00C026EE094F}')) , 0 , )),
	(( 'GetTreeNeedRebuild' , ), 1610678353, (1610678353, (), [ ], 1 , 1 , 4 , 0 , 672 , (3, 0, None, None) , 0 , )),
	(( 'SetTreeNeedRebuild' , 'val' , ), 1610678354, (1610678354, (), [ (3, 0, None, None) , ], 1 , 1 , 4 , 0 , 680 , (3, 0, None, None) , 0 , )),
	(( 'UserSelectEntityEx' , 'defSelectObject' , 'fnFilter' , 'prompt' , 'processParam' , 
			 ), 1610678355, (1610678355, (), [ (13, 0, None, "IID('{7AA0E540-0301-11D4-A30E-00C026EE094F}')") , (16408, 0, None, None) , (31, 0, None, None) , (13, 0, None, None) , ], 1 , 1 , 4 , 0 , 688 , (13, 0, None, IID('{7AA0E540-0301-11D4-A30E-00C026EE094F}')) , 0 , )),
	(( 'PlaceFeatureAfter' , 'obj' , 'afterObj' , ), 1610678356, (1610678356, (), [ (13, 0, None, "IID('{1D15245B-695E-4F9F-AFCA-EACBC3A055BB}')") , 
			 (13, 0, None, "IID('{1D15245B-695E-4F9F-AFCA-EACBC3A055BB}')") , ], 1 , 1 , 4 , 0 , 696 , (3, 0, None, None) , 0 , )),
	(( 'SetRollBackFeature' , 'obj' , ), 1610678357, (1610678357, (), [ (13, 0, None, "IID('{1D15245B-695E-4F9F-AFCA-EACBC3A055BB}')") , ], 1 , 1 , 4 , 0 , 704 , (3, 0, None, None) , 0 , )),
	(( 'GetRollBackFeature' , ), 1610678358, (1610678358, (), [ ], 1 , 1 , 4 , 0 , 712 , (13, 0, None, IID('{1D15245B-695E-4F9F-AFCA-EACBC3A055BB}')) , 0 , )),
	(( 'SetEnableRollBackFeaturesInCollections' , 'val' , ), 1610678359, (1610678359, (), [ (3, 0, None, None) , ], 1 , 1 , 4 , 0 , 720 , (3, 0, None, None) , 0 , )),
	(( 'GetEnableRollBackFeaturesInCollections' , ), 1610678360, (1610678360, (), [ ], 1 , 1 , 4 , 0 , 728 , (3, 0, None, None) , 0 , )),
	(( 'ExcludeFeaturesAfter' , 'obj' , 'exclude' , ), 1610678361, (1610678361, (), [ (13, 0, None, "IID('{1D15245B-695E-4F9F-AFCA-EACBC3A055BB}')") , 
			 (3, 0, None, None) , ], 1 , 1 , 4 , 0 , 736 , (3, 0, None, None) , 0 , )),
	(( 'GetHideAllDimensions' , ), 1610678362, (1610678362, (), [ ], 1 , 1 , 4 , 0 , 744 , (3, 0, None, None) , 0 , )),
	(( 'SetHideAllDimensions' , 'val' , ), 1610678363, (1610678363, (), [ (3, 0, None, None) , ], 1 , 1 , 4 , 0 , 752 , (3, 0, None, None) , 0 , )),
	(( 'GetHideAllDesignations' , ), 1610678364, (1610678364, (), [ ], 1 , 1 , 4 , 0 , 760 , (3, 0, None, None) , 0 , )),
	(( 'SetHideAllDesignations' , 'val' , ), 1610678365, (1610678365, (), [ (3, 0, None, None) , ], 1 , 1 , 4 , 0 , 768 , (3, 0, None, None) , 0 , )),
	(( 'GetHideAllAuxiliaryGeom' , ), 1610678366, (1610678366, (), [ ], 1 , 1 , 4 , 0 , 776 , (3, 0, None, None) , 0 , )),
	(( 'SetHideAllAuxiliaryGeom' , 'val' , ), 1610678367, (1610678367, (), [ (3, 0, None, None) , ], 1 , 1 , 4 , 0 , 784 , (3, 0, None, None) , 0 , )),
	(( 'GetHideInComponentsMode' , ), 1610678368, (1610678368, (), [ ], 1 , 1 , 4 , 0 , 792 , (3, 0, None, None) , 0 , )),
	(( 'SetHideInComponentsMode' , 'val' , ), 1610678369, (1610678369, (), [ (3, 0, None, None) , ], 1 , 1 , 4 , 0 , 800 , (3, 0, None, None) , 0 , )),
	(( 'GetDocument3DNotifyResult' , ), 1610678370, (1610678370, (), [ ], 1 , 1 , 4 , 0 , 808 , (13, 0, None, IID('{06C34A3C-2634-4F82-BCE0-F3D73572958C}')) , 0 , )),
	(( 'GetReference' , ), 1610678371, (1610678371, (), [ ], 1 , 1 , 4 , 0 , 816 , (3, 0, None, None) , 0 , )),
	(( 'GetWindowNeedRebuild' , ), 1610678372, (1610678372, (), [ ], 1 , 1 , 4 , 0 , 824 , (3, 0, None, None) , 0 , )),
	(( 'SetWindowNeedRebuild' , 'val' , ), 1610678373, (1610678373, (), [ (3, 0, None, None) , ], 1 , 1 , 4 , 0 , 832 , (3, 0, None, None) , 0 , )),
	(( 'GetHideLayoutGeometry' , ), 1610678374, (1610678374, (), [ ], 1 , 1 , 4 , 0 , 840 , (3, 0, None, None) , 0 , )),
	(( 'SetHideLayoutGeometry' , 'val' , ), 1610678375, (1610678375, (), [ (3, 0, None, None) , ], 1 , 1 , 4 , 0 , 848 , (3, 0, None, None) , 0 , )),
	(( 'RunTakeCreateObjectProc' , 'processType' , 'takeObject' , 'needCreateTakeObj' , 'lostTakeObj' , 
			 ), 1610678376, (1610678376, (), [ (3, 0, None, None) , (13, 0, None, None) , (3, 0, None, None) , (3, 0, None, None) , ], 1 , 1 , 4 , 0 , 856 , (3, 0, None, None) , 0 , )),
	(( 'LoadFromAdditionFormat' , 'fileName' , 'par' , ), 1610678377, (1610678377, (), [ (31, 0, None, None) , 
			 (13, 0, None, "IID('{7AA0E540-0319-11D4-A30E-00C026EE094F}')") , ], 1 , 1 , 4 , 0 , 864 , (3, 0, None, None) , 0 , )),
	(( 'GetLastFeature' , ), 1610678378, (1610678378, (), [ ], 1 , 1 , 4 , 0 , 872 , (13, 0, None, IID('{1D15245B-695E-4F9F-AFCA-EACBC3A055BB}')) , 0 , )),
]

IDocument3DNotify_vtables_dispatch_ = 0
IDocument3DNotify_vtables_ = [
	(( 'BeginRebuild' , ), 1610743808, (1610743808, (), [ ], 1 , 1 , 4 , 0 , 32 , (11, 0, None, None) , 0 , )),
	(( 'Rebuild' , ), 1610743809, (1610743809, (), [ ], 1 , 1 , 4 , 0 , 40 , (11, 0, None, None) , 0 , )),
	(( 'BeginChoiceMaterial' , ), 1610743810, (1610743810, (), [ ], 1 , 1 , 4 , 0 , 48 , (11, 0, None, None) , 0 , )),
	(( 'ChoiceMaterial' , 'material' , 'density' , ), 1610743811, (1610743811, (), [ (30, 0, None, None) , 
			 (5, 0, None, None) , ], 1 , 1 , 4 , 0 , 56 , (11, 0, None, None) , 0 , )),
	(( 'BeginChoiceMarking' , ), 1610743812, (1610743812, (), [ ], 1 , 1 , 4 , 0 , 64 , (11, 0, None, None) , 0 , )),
	(( 'ChoiceMarking' , 'marking' , ), 1610743813, (1610743813, (), [ (30, 0, None, None) , ], 1 , 1 , 4 , 0 , 72 , (11, 0, None, None) , 0 , )),
	(( 'BeginSetPartFromFile' , ), 1610743814, (1610743814, (), [ ], 1 , 1 , 4 , 0 , 80 , (11, 0, None, None) , 0 , )),
	(( 'BeginCreatePartFromFile' , 'typeDoc' , 'plane' , ), 1610743815, (1610743815, (), [ (11, 0, None, None) , 
			 (13, 0, None, "IID('{7AA0E540-0301-11D4-A30E-00C026EE094F}')") , ], 1 , 1 , 4 , 0 , 88 , (11, 0, None, None) , 0 , )),
	(( 'CreateEmbodiment' , 'marking' , ), 1610743816, (1610743816, (), [ (30, 0, None, None) , ], 1 , 1 , 4 , 0 , 96 , (11, 0, None, None) , 0 , )),
	(( 'DeleteEmbodiment' , 'marking' , ), 1610743817, (1610743817, (), [ (30, 0, None, None) , ], 1 , 1 , 4 , 0 , 104 , (11, 0, None, None) , 0 , )),
	(( 'ChangeCurrentEmbodiment' , 'marking' , ), 1610743818, (1610743818, (), [ (30, 0, None, None) , ], 1 , 1 , 4 , 0 , 112 , (11, 0, None, None) , 0 , )),
	(( 'BeginChoiceProperty' , 'obj' , 'propID' , ), 1610743819, (1610743819, (), [ (13, 0, None, None) , 
			 (5, 0, None, None) , ], 1 , 1 , 4 , 0 , 120 , (11, 0, None, None) , 0 , )),
	(( 'ChoiceProperty' , 'obj' , 'propID' , ), 1610743820, (1610743820, (), [ (13, 0, None, None) , 
			 (5, 0, None, None) , ], 1 , 1 , 4 , 0 , 128 , (11, 0, None, None) , 0 , )),
	(( 'BeginRollbackFeatures' , ), 1610743821, (1610743821, (), [ ], 1 , 1 , 4 , 0 , 136 , (11, 0, None, None) , 0 , )),
	(( 'RollbackFeatures' , ), 1610743822, (1610743822, (), [ ], 1 , 1 , 4 , 0 , 144 , (11, 0, None, None) , 0 , )),
	(( 'BedinLoadCombinationChange' , 'index' , ), 1610743823, (1610743823, (), [ (3, 0, None, None) , ], 1 , 1 , 4 , 0 , 152 , (11, 0, None, None) , 0 , )),
	(( 'LoadCombinationChange' , 'index' , ), 1610743824, (1610743824, (), [ (3, 0, None, None) , ], 1 , 1 , 4 , 0 , 160 , (11, 0, None, None) , 0 , )),
]

IDocument3DNotifyResult_vtables_dispatch_ = 0
IDocument3DNotifyResult_vtables_ = [
	(( 'GetNotifyType' , ), 1610678272, (1610678272, (), [ ], 1 , 1 , 4 , 0 , 24 , (3, 0, None, None) , 0 , )),
	(( 'GetNotifyObjectType' , ), 1610678273, (1610678273, (), [ ], 1 , 1 , 4 , 0 , 32 , (3, 0, None, None) , 0 , )),
	(( 'GetNotifyObject' , ), 1610678274, (1610678274, (), [ ], 1 , 1 , 4 , 0 , 40 , (13, 0, None, None) , 0 , )),
	(( 'GetRequestFilesType' , ), 1610678275, (1610678275, (), [ ], 1 , 1 , 4 , 0 , 48 , (3, 0, None, None) , 0 , )),
]

IEdgeCollection_vtables_dispatch_ = 0
IEdgeCollection_vtables_ = [
	(( 'Refresh' , ), 1610678272, (1610678272, (), [ ], 1 , 1 , 4 , 0 , 24 , (3, 0, None, None) , 0 , )),
	(( 'GetCount' , ), 1610678273, (1610678273, (), [ ], 1 , 1 , 4 , 0 , 32 , (3, 0, None, None) , 0 , )),
	(( 'First' , ), 1610678274, (1610678274, (), [ ], 1 , 1 , 4 , 0 , 40 , (13, 0, None, IID('{7AA0E540-0321-11D4-A30E-00C026EE094F}')) , 0 , )),
	(( 'Last' , ), 1610678275, (1610678275, (), [ ], 1 , 1 , 4 , 0 , 48 , (13, 0, None, IID('{7AA0E540-0321-11D4-A30E-00C026EE094F}')) , 0 , )),
	(( 'Next' , ), 1610678276, (1610678276, (), [ ], 1 , 1 , 4 , 0 , 56 , (13, 0, None, IID('{7AA0E540-0321-11D4-A30E-00C026EE094F}')) , 0 , )),
	(( 'Prev' , ), 1610678277, (1610678277, (), [ ], 1 , 1 , 4 , 0 , 64 , (13, 0, None, IID('{7AA0E540-0321-11D4-A30E-00C026EE094F}')) , 0 , )),
	(( 'GetByIndex' , 'index' , ), 1610678278, (1610678278, (), [ (3, 0, None, None) , ], 1 , 1 , 4 , 0 , 72 , (13, 0, None, IID('{7AA0E540-0321-11D4-A30E-00C026EE094F}')) , 0 , )),
	(( 'FindIt' , 'entity' , ), 1610678279, (1610678279, (), [ (13, 0, None, "IID('{7AA0E540-0321-11D4-A30E-00C026EE094F}')") , ], 1 , 1 , 4 , 0 , 80 , (19, 0, None, None) , 0 , )),
]

IEdgeDefinition_vtables_dispatch_ = 0
IEdgeDefinition_vtables_ = [
	(( 'IsStraight' , ), 1610678272, (1610678272, (), [ ], 1 , 1 , 4 , 0 , 24 , (3, 0, None, None) , 0 , )),
	(( 'GetOwnerEntity' , ), 1610678273, (1610678273, (), [ ], 1 , 1 , 4 , 0 , 32 , (13, 0, None, IID('{7AA0E540-0301-11D4-A30E-00C026EE094F}')) , 0 , )),
	(( 'GetCurve3D' , ), 1610678274, (1610678274, (), [ ], 1 , 1 , 4 , 0 , 40 , (13, 0, None, IID('{E5066490-773D-4289-A60B-2FC19865174A}')) , 0 , )),
	(( 'GetAdjacentFace' , 'facePlus' , ), 1610678275, (1610678275, (), [ (3, 0, None, None) , ], 1 , 1 , 4 , 0 , 48 , (13, 0, None, IID('{7AA0E540-0322-11D4-A30E-00C026EE094F}')) , 0 , )),
	(( 'GetVertex' , 'start' , ), 1610678276, (1610678276, (), [ (3, 0, None, None) , ], 1 , 1 , 4 , 0 , 56 , (13, 0, None, IID('{7AA0E540-0320-11D4-A30E-00C026EE094F}')) , 0 , )),
	(( 'EdgeCollection' , 'begin' , ), 1610678277, (1610678277, (), [ (3, 0, None, None) , ], 1 , 1 , 4 , 0 , 64 , (13, 0, None, IID('{5E93D4B9-BAAB-4FC4-ACF8-8FF78E9D1B42}')) , 0 , )),
	(( 'OrientedEdgeCollection' , ), 1610678278, (1610678278, (), [ ], 1 , 1 , 4 , 0 , 72 , (13, 0, None, IID('{D19B0A07-4CA6-4E77-A8DB-8AC8C7123124}')) , 0 , )),
	(( 'IsArc' , ), 1610678279, (1610678279, (), [ ], 1 , 1 , 4 , 0 , 80 , (3, 0, None, None) , 0 , )),
	(( 'IsCircle' , ), 1610678280, (1610678280, (), [ ], 1 , 1 , 4 , 0 , 88 , (3, 0, None, None) , 0 , )),
	(( 'IsEllipse' , ), 1610678281, (1610678281, (), [ ], 1 , 1 , 4 , 0 , 96 , (3, 0, None, None) , 0 , )),
	(( 'IsNurbs' , ), 1610678282, (1610678282, (), [ ], 1 , 1 , 4 , 0 , 104 , (3, 0, None, None) , 0 , )),
	(( 'IsPeriodic' , ), 1610678283, (1610678283, (), [ ], 1 , 1 , 4 , 0 , 112 , (3, 0, None, None) , 0 , )),
	(( 'GetLength' , 'bitVector' , ), 1610678284, (1610678284, (), [ (19, 0, None, None) , ], 1 , 1 , 4 , 0 , 120 , (5, 0, None, None) , 0 , )),
	(( 'GetEntity' , ), 1610678285, (1610678285, (), [ ], 1 , 1 , 4 , 0 , 128 , (13, 0, None, IID('{7AA0E540-0301-11D4-A30E-00C026EE094F}')) , 0 , )),
	(( 'IsValid' , ), 1610678286, (1610678286, (), [ ], 1 , 1 , 4 , 0 , 136 , (3, 0, None, None) , 0 , )),
	(( 'GetSketchEdge' , ), 1610678287, (1610678287, (), [ ], 1 , 1 , 4 , 0 , 144 , (3, 0, None, None) , 0 , )),
]

IEllipse3dParam_vtables_dispatch_ = 0
IEllipse3dParam_vtables_ = [
	(( 'GetPlacement' , ), 1610678272, (1610678272, (), [ ], 1 , 1 , 4 , 0 , 24 , (13, 0, None, IID('{7AA0E540-0310-11D4-A30E-00C026EE094F}')) , 0 , )),
	(( 'GetMajorRadius' , ), 1610678273, (1610678273, (), [ ], 1 , 1 , 4 , 0 , 32 , (5, 0, None, None) , 0 , )),
	(( 'GetMinorRadius' , ), 1610678274, (1610678274, (), [ ], 1 , 1 , 4 , 0 , 40 , (5, 0, None, None) , 0 , )),
]

IEmbodiment3D_vtables_dispatch_ = 0
IEmbodiment3D_vtables_ = [
]

IEntity_vtables_dispatch_ = 0
IEntity_vtables_ = [
	(( 'GetHidden' , ), 1610678272, (1610678272, (), [ ], 1 , 1 , 4 , 0 , 24 , (3, 0, None, None) , 0 , )),
	(( 'SetHidden' , '_hidden' , ), 1610678273, (1610678273, (), [ (3, 0, None, None) , ], 1 , 1 , 4 , 0 , 32 , (3, 0, None, None) , 0 , )),
	(( 'GetName' , ), 1610678274, (1610678274, (), [ ], 1 , 1 , 4 , 0 , 40 , (31, 0, None, None) , 0 , )),
	(( 'SetName' , 'name' , ), 1610678275, (1610678275, (), [ (31, 0, None, None) , ], 1 , 1 , 4 , 0 , 48 , (3, 0, None, None) , 0 , )),
	(( 'ColorParam' , ), 1610678276, (1610678276, (), [ ], 1 , 1 , 4 , 0 , 56 , (13, 0, None, IID('{7AA0E540-0305-11D4-A30E-00C026EE094F}')) , 0 , )),
	(( 'GetAdvancedColor' , 'color' , 'ambient' , 'diffuse' , 'specularity' , 
			 'shininess' , 'transparency' , 'emission' , ), 1610678277, (1610678277, (), [ (16403, 0, None, None) , 
			 (16389, 0, None, None) , (16389, 0, None, None) , (16389, 0, None, None) , (16389, 0, None, None) , (16389, 0, None, None) , 
			 (16389, 0, None, None) , ], 1 , 1 , 4 , 0 , 64 , (3, 0, None, None) , 0 , )),
	(( 'SetAdvancedColor' , 'color' , 'ambient' , 'diffuse' , 'specularity' , 
			 'shininess' , 'transparency' , 'emission' , ), 1610678278, (1610678278, (), [ (19, 0, None, None) , 
			 (5, 0, None, None) , (5, 0, None, None) , (5, 0, None, None) , (5, 0, None, None) , (5, 0, None, None) , 
			 (5, 0, None, None) , ], 1 , 1 , 4 , 0 , 72 , (3, 0, None, None) , 0 , )),
	(( 'IsIt' , 'objType' , ), 1610678279, (1610678279, (), [ (2, 0, None, None) , ], 1 , 1 , 4 , 0 , 80 , (3, 0, None, None) , 0 , )),
	(( 'GetType' , ), 1610678280, (1610678280, (), [ ], 1 , 1 , 4 , 0 , 88 , (2, 0, None, None) , 0 , )),
	(( 'IsCreated' , ), 1610678281, (1610678281, (), [ ], 1 , 1 , 4 , 0 , 96 , (3, 0, None, None) , 0 , )),
	(( 'GetDefinition' , ), 1610678282, (1610678282, (), [ ], 1 , 1 , 4 , 0 , 104 , (13, 0, None, None) , 0 , )),
	(( 'Create' , ), 1610678283, (1610678283, (), [ ], 1 , 1 , 4 , 0 , 112 , (3, 0, None, None) , 0 , )),
	(( 'Update' , ), 1610678284, (1610678284, (), [ ], 1 , 1 , 4 , 0 , 120 , (3, 0, None, None) , 0 , )),
	(( 'GetParent' , ), 1610678285, (1610678285, (), [ ], 1 , 1 , 4 , 0 , 128 , (13, 0, None, IID('{7AA0E540-0300-11D4-A30E-00C026EE094F}')) , 0 , )),
	(( 'SetExcluded' , 'exclude' , ), 1610678286, (1610678286, (), [ (3, 0, None, None) , ], 1 , 1 , 4 , 0 , 136 , (3, 0, None, None) , 0 , )),
	(( 'GetExcluded' , ), 1610678287, (1610678287, (), [ ], 1 , 1 , 4 , 0 , 144 , (3, 0, None, None) , 0 , )),
	(( 'GetFeature' , ), 1610678288, (1610678288, (), [ ], 1 , 1 , 4 , 0 , 152 , (13, 0, None, IID('{1D15245B-695E-4F9F-AFCA-EACBC3A055BB}')) , 0 , )),
	(( 'BodyCollection' , ), 1610678289, (1610678289, (), [ ], 1 , 1 , 4 , 0 , 160 , (13, 0, None, IID('{64CBC7CB-005D-47DF-8B3E-53FD974C5A32}')) , 0 , )),
	(( 'GetMultiBodyParts' , ), 1610678290, (1610678290, (), [ ], 1 , 1 , 4 , 0 , 168 , (3, 0, None, None) , 0 , )),
	(( 'GetBodyParts' , ), 1610678291, (1610678291, (), [ ], 1 , 1 , 4 , 0 , 176 , (13, 0, None, IID('{DFC4E0F1-5270-40F3-8A4F-BEA75AB5383C}')) , 0 , )),
	(( 'GetUseColor' , ), 1610678292, (1610678292, (), [ ], 1 , 1 , 4 , 0 , 184 , (3, 0, None, None) , 0 , )),
	(( 'SetUseColor' , 'useColor' , ), 1610678293, (1610678293, (), [ (3, 0, None, None) , ], 1 , 1 , 4 , 0 , 192 , (3, 0, None, None) , 0 , )),
]

IEntityCollection_vtables_dispatch_ = 0
IEntityCollection_vtables_ = [
	(( 'Refresh' , ), 1610678272, (1610678272, (), [ ], 1 , 1 , 4 , 0 , 24 , (3, 0, None, None) , 0 , )),
	(( 'GetCount' , ), 1610678273, (1610678273, (), [ ], 1 , 1 , 4 , 0 , 32 , (3, 0, None, None) , 0 , )),
	(( 'First' , ), 1610678274, (1610678274, (), [ ], 1 , 1 , 4 , 0 , 40 , (13, 0, None, IID('{7AA0E540-0301-11D4-A30E-00C026EE094F}')) , 0 , )),
	(( 'Last' , ), 1610678275, (1610678275, (), [ ], 1 , 1 , 4 , 0 , 48 , (13, 0, None, IID('{7AA0E540-0301-11D4-A30E-00C026EE094F}')) , 0 , )),
	(( 'Next' , ), 1610678276, (1610678276, (), [ ], 1 , 1 , 4 , 0 , 56 , (13, 0, None, IID('{7AA0E540-0301-11D4-A30E-00C026EE094F}')) , 0 , )),
	(( 'Prev' , ), 1610678277, (1610678277, (), [ ], 1 , 1 , 4 , 0 , 64 , (13, 0, None, IID('{7AA0E540-0301-11D4-A30E-00C026EE094F}')) , 0 , )),
	(( 'GetByName' , 'name' , 'testFullName' , 'testIgnoreCase' , ), 1610678278, (1610678278, (), [ 
			 (31, 0, None, None) , (3, 0, None, None) , (3, 0, None, None) , ], 1 , 1 , 4 , 0 , 72 , (13, 0, None, IID('{7AA0E540-0301-11D4-A30E-00C026EE094F}')) , 0 , )),
	(( 'GetByIndex' , 'index' , ), 1610678279, (1610678279, (), [ (3, 0, None, None) , ], 1 , 1 , 4 , 0 , 80 , (13, 0, None, IID('{7AA0E540-0301-11D4-A30E-00C026EE094F}')) , 0 , )),
	(( 'SelectByPoint' , 'x' , 'y' , 'z' , ), 1610678280, (1610678280, (), [ 
			 (5, 0, None, None) , (5, 0, None, None) , (5, 0, None, None) , ], 1 , 1 , 4 , 0 , 88 , (3, 0, None, None) , 0 , )),
	(( 'Add' , 'entity' , ), 1610678281, (1610678281, (), [ (13, 0, None, "IID('{7AA0E540-0301-11D4-A30E-00C026EE094F}')") , ], 1 , 1 , 4 , 0 , 96 , (3, 0, None, None) , 0 , )),
	(( 'AddAt' , 'entity' , 'index' , ), 1610678282, (1610678282, (), [ (13, 0, None, "IID('{7AA0E540-0301-11D4-A30E-00C026EE094F}')") , 
			 (3, 0, None, None) , ], 1 , 1 , 4 , 0 , 104 , (3, 0, None, None) , 0 , )),
	(( 'AddBefore' , 'entity' , 'base' , ), 1610678283, (1610678283, (), [ (13, 0, None, "IID('{7AA0E540-0301-11D4-A30E-00C026EE094F}')") , 
			 (13, 0, None, "IID('{7AA0E540-0301-11D4-A30E-00C026EE094F}')") , ], 1 , 1 , 4 , 0 , 112 , (3, 0, None, None) , 0 , )),
	(( 'DetachByIndex' , 'index' , ), 1610678284, (1610678284, (), [ (3, 0, None, None) , ], 1 , 1 , 4 , 0 , 120 , (3, 0, None, None) , 0 , )),
	(( 'DetachByBody' , 'entity' , ), 1610678285, (1610678285, (), [ (13, 0, None, "IID('{7AA0E540-0301-11D4-A30E-00C026EE094F}')") , ], 1 , 1 , 4 , 0 , 128 , (3, 0, None, None) , 0 , )),
	(( 'Clear' , ), 1610678286, (1610678286, (), [ ], 1 , 1 , 4 , 0 , 136 , (3, 0, None, None) , 0 , )),
	(( 'SetByIndex' , 'entity' , 'index' , ), 1610678287, (1610678287, (), [ (13, 0, None, "IID('{7AA0E540-0301-11D4-A30E-00C026EE094F}')") , 
			 (3, 0, None, None) , ], 1 , 1 , 4 , 0 , 144 , (3, 0, None, None) , 0 , )),
	(( 'FindIt' , 'entity' , ), 1610678288, (1610678288, (), [ (13, 0, None, "IID('{7AA0E540-0301-11D4-A30E-00C026EE094F}')") , ], 1 , 1 , 4 , 0 , 152 , (19, 0, None, None) , 0 , )),
]

IEvolutionSurfaceDefinition_vtables_dispatch_ = 0
IEvolutionSurfaceDefinition_vtables_ = [
	(( 'SetSketch' , 'sketch' , ), 1610678272, (1610678272, (), [ (13, 0, None, "IID('{7AA0E540-0301-11D4-A30E-00C026EE094F}')") , ], 1 , 1 , 4 , 0 , 24 , (3, 0, None, None) , 0 , )),
	(( 'GetSketch' , ), 1610678273, (1610678273, (), [ ], 1 , 1 , 4 , 0 , 32 , (13, 0, None, IID('{7AA0E540-0301-11D4-A30E-00C026EE094F}')) , 0 , )),
	(( 'PathPartArray' , ), 1610678274, (1610678274, (), [ ], 1 , 1 , 4 , 0 , 40 , (13, 0, None, IID('{7AA0E540-0303-11D4-A30E-00C026EE094F}')) , 0 , )),
	(( 'GetSketchShiftType' , ), 1610678275, (1610678275, (), [ ], 1 , 1 , 4 , 0 , 48 , (2, 0, None, None) , 0 , )),
	(( 'SetSketchShiftType' , 's' , ), 1610678276, (1610678276, (), [ (2, 0, None, None) , ], 1 , 1 , 4 , 0 , 56 , (3, 0, None, None) , 0 , )),
	(( 'GetClosedShell' , ), 1610678277, (1610678277, (), [ ], 1 , 1 , 4 , 0 , 64 , (3, 0, None, None) , 0 , )),
	(( 'SetClosedShell' , 'closed' , ), 1610678278, (1610678278, (), [ (3, 0, None, None) , ], 1 , 1 , 4 , 0 , 72 , (3, 0, None, None) , 0 , )),
	(( 'GetPathLength' , 'bitVector' , ), 1610678279, (1610678279, (), [ (19, 0, None, None) , ], 1 , 1 , 4 , 0 , 80 , (5, 0, None, None) , 0 , )),
]

IExtrusionParam_vtables_dispatch_ = 0
IExtrusionParam_vtables_ = [
	(( 'GetTypeNormal' , ), 1610678272, (1610678272, (), [ ], 1 , 1 , 4 , 0 , 24 , (17, 0, None, None) , 0 , )),
	(( 'SetTypeNormal' , 'val' , ), 1610678273, (1610678273, (), [ (17, 0, None, None) , ], 1 , 1 , 4 , 0 , 32 , (3, 0, None, None) , 0 , )),
	(( 'GetDepthNormal' , ), 1610678274, (1610678274, (), [ ], 1 , 1 , 4 , 0 , 40 , (5, 0, None, None) , 0 , )),
	(( 'SetDepthNormal' , 'val' , ), 1610678275, (1610678275, (), [ (5, 0, None, None) , ], 1 , 1 , 4 , 0 , 48 , (3, 0, None, None) , 0 , )),
	(( 'GetDraftValueNormal' , ), 1610678276, (1610678276, (), [ ], 1 , 1 , 4 , 0 , 56 , (5, 0, None, None) , 0 , )),
	(( 'SetDraftValueNormal' , 'val' , ), 1610678277, (1610678277, (), [ (5, 0, None, None) , ], 1 , 1 , 4 , 0 , 64 , (3, 0, None, None) , 0 , )),
	(( 'GetDraftOutwardNormal' , ), 1610678278, (1610678278, (), [ ], 1 , 1 , 4 , 0 , 72 , (3, 0, None, None) , 0 , )),
	(( 'SetDraftOutwardNormal' , 'val' , ), 1610678279, (1610678279, (), [ (3, 0, None, None) , ], 1 , 1 , 4 , 0 , 80 , (3, 0, None, None) , 0 , )),
	(( 'GetTypeReverse' , ), 1610678280, (1610678280, (), [ ], 1 , 1 , 4 , 0 , 88 , (17, 0, None, None) , 0 , )),
	(( 'SetTypeReverse' , 'val' , ), 1610678281, (1610678281, (), [ (17, 0, None, None) , ], 1 , 1 , 4 , 0 , 96 , (3, 0, None, None) , 0 , )),
	(( 'GetDepthReverse' , ), 1610678282, (1610678282, (), [ ], 1 , 1 , 4 , 0 , 104 , (5, 0, None, None) , 0 , )),
	(( 'SetDepthReverse' , 'val' , ), 1610678283, (1610678283, (), [ (5, 0, None, None) , ], 1 , 1 , 4 , 0 , 112 , (3, 0, None, None) , 0 , )),
	(( 'GetDraftValueReverse' , ), 1610678284, (1610678284, (), [ ], 1 , 1 , 4 , 0 , 120 , (5, 0, None, None) , 0 , )),
	(( 'SetDraftValueReverse' , 'val' , ), 1610678285, (1610678285, (), [ (5, 0, None, None) , ], 1 , 1 , 4 , 0 , 128 , (3, 0, None, None) , 0 , )),
	(( 'GetDraftOutwardReverse' , ), 1610678286, (1610678286, (), [ ], 1 , 1 , 4 , 0 , 136 , (3, 0, None, None) , 0 , )),
	(( 'SetDraftOutwardReverse' , 'val' , ), 1610678287, (1610678287, (), [ (3, 0, None, None) , ], 1 , 1 , 4 , 0 , 144 , (3, 0, None, None) , 0 , )),
	(( 'GetDirection' , ), 1610678288, (1610678288, (), [ ], 1 , 1 , 4 , 0 , 152 , (3, 0, None, None) , 0 , )),
	(( 'SetDirection' , 'val' , ), 1610678289, (1610678289, (), [ (3, 0, None, None) , ], 1 , 1 , 4 , 0 , 160 , (3, 0, None, None) , 0 , )),
]

IExtrusionSurfaceDefinition_vtables_dispatch_ = 0
IExtrusionSurfaceDefinition_vtables_ = [
	(( 'SetSketch' , 'name' , ), 1610678272, (1610678272, (), [ (13, 0, None, "IID('{7AA0E540-0301-11D4-A30E-00C026EE094F}')") , ], 1 , 1 , 4 , 0 , 24 , (3, 0, None, None) , 0 , )),
	(( 'GetSketch' , ), 1610678273, (1610678273, (), [ ], 1 , 1 , 4 , 0 , 32 , (13, 0, None, IID('{7AA0E540-0301-11D4-A30E-00C026EE094F}')) , 0 , )),
	(( 'GetSideParam' , 'forward' , 'type' , 'depth' , 'draftValue' , 
			 'draftOutward' , ), 1610678274, (1610678274, (), [ (3, 0, None, None) , (16401, 0, None, None) , (16389, 0, None, None) , 
			 (16389, 0, None, None) , (16387, 0, None, None) , ], 1 , 1 , 4 , 0 , 40 , (3, 0, None, None) , 0 , )),
	(( 'SetSideParam' , 'forward' , 'type' , 'depth' , 'draftValue' , 
			 'draftOutward' , ), 1610678275, (1610678275, (), [ (3, 0, None, None) , (17, 0, None, None) , (5, 0, None, None) , 
			 (5, 0, None, None) , (3, 0, None, None) , ], 1 , 1 , 4 , 0 , 48 , (24, 0, None, None) , 0 , )),
	(( 'SetDirectionType' , 'dirType' , ), 1610678276, (1610678276, (), [ (3, 0, None, None) , ], 1 , 1 , 4 , 0 , 56 , (3, 0, None, None) , 0 , )),
	(( 'GetDirectionType' , ), 1610678277, (1610678277, (), [ ], 1 , 1 , 4 , 0 , 64 , (3, 0, None, None) , 0 , )),
	(( 'ExtrusionParam' , ), 1610678278, (1610678278, (), [ ], 1 , 1 , 4 , 0 , 72 , (13, 0, None, IID('{7AA0E540-0307-11D4-A30E-00C026EE094F}')) , 0 , )),
	(( 'GetDepthObject' , 'normal' , ), 1610678279, (1610678279, (), [ (3, 0, None, None) , ], 1 , 1 , 4 , 0 , 80 , (13, 0, None, IID('{7AA0E540-0301-11D4-A30E-00C026EE094F}')) , 0 , )),
	(( 'SetDepthObject' , 'normal' , 'obj' , ), 1610678280, (1610678280, (), [ (3, 0, None, None) , 
			 (13, 0, None, "IID('{7AA0E540-0301-11D4-A30E-00C026EE094F}')") , ], 1 , 1 , 4 , 0 , 88 , (3, 0, None, None) , 0 , )),
	(( 'ResetDepthObject' , 'normal' , ), 1610678281, (1610678281, (), [ (3, 0, None, None) , ], 1 , 1 , 4 , 0 , 96 , (3, 0, None, None) , 0 , )),
	(( 'GetClosedShell' , ), 1610678282, (1610678282, (), [ ], 1 , 1 , 4 , 0 , 104 , (3, 0, None, None) , 0 , )),
	(( 'SetClosedShell' , 'closed' , ), 1610678283, (1610678283, (), [ (3, 0, None, None) , ], 1 , 1 , 4 , 0 , 112 , (3, 0, None, None) , 0 , )),
]

IFaceCollection_vtables_dispatch_ = 0
IFaceCollection_vtables_ = [
	(( 'Refresh' , ), 1610678272, (1610678272, (), [ ], 1 , 1 , 4 , 0 , 24 , (3, 0, None, None) , 0 , )),
	(( 'GetCount' , ), 1610678273, (1610678273, (), [ ], 1 , 1 , 4 , 0 , 32 , (3, 0, None, None) , 0 , )),
	(( 'First' , ), 1610678274, (1610678274, (), [ ], 1 , 1 , 4 , 0 , 40 , (13, 0, None, IID('{7AA0E540-0322-11D4-A30E-00C026EE094F}')) , 0 , )),
	(( 'Last' , ), 1610678275, (1610678275, (), [ ], 1 , 1 , 4 , 0 , 48 , (13, 0, None, IID('{7AA0E540-0322-11D4-A30E-00C026EE094F}')) , 0 , )),
	(( 'Next' , ), 1610678276, (1610678276, (), [ ], 1 , 1 , 4 , 0 , 56 , (13, 0, None, IID('{7AA0E540-0322-11D4-A30E-00C026EE094F}')) , 0 , )),
	(( 'Prev' , ), 1610678277, (1610678277, (), [ ], 1 , 1 , 4 , 0 , 64 , (13, 0, None, IID('{7AA0E540-0322-11D4-A30E-00C026EE094F}')) , 0 , )),
	(( 'GetByIndex' , 'index' , ), 1610678278, (1610678278, (), [ (3, 0, None, None) , ], 1 , 1 , 4 , 0 , 72 , (13, 0, None, IID('{7AA0E540-0322-11D4-A30E-00C026EE094F}')) , 0 , )),
	(( 'GetByName' , 'name' , 'testFullName' , 'testIgnoreCase' , ), 1610678279, (1610678279, (), [ 
			 (31, 0, None, None) , (3, 0, None, None) , (3, 0, None, None) , ], 1 , 1 , 4 , 0 , 80 , (13, 0, None, IID('{7AA0E540-0322-11D4-A30E-00C026EE094F}')) , 0 , )),
	(( 'FindIt' , 'entity' , ), 1610678280, (1610678280, (), [ (13, 0, None, "IID('{7AA0E540-0322-11D4-A30E-00C026EE094F}')") , ], 1 , 1 , 4 , 0 , 88 , (19, 0, None, None) , 0 , )),
]

IFaceDefinition_vtables_dispatch_ = 0
IFaceDefinition_vtables_ = [
	(( 'IsPlanar' , ), 1610678272, (1610678272, (), [ ], 1 , 1 , 4 , 0 , 24 , (3, 0, None, None) , 0 , )),
	(( 'IsCone' , ), 1610678273, (1610678273, (), [ ], 1 , 1 , 4 , 0 , 32 , (3, 0, None, None) , 0 , )),
	(( 'IsCylinder' , ), 1610678274, (1610678274, (), [ ], 1 , 1 , 4 , 0 , 40 , (3, 0, None, None) , 0 , )),
	(( 'GetCylinderParam' , 'h' , 'r' , ), 1610678275, (1610678275, (), [ (16389, 0, None, None) , 
			 (16389, 0, None, None) , ], 1 , 1 , 4 , 0 , 48 , (3, 0, None, None) , 0 , )),
	(( 'GetOwnerEntity' , ), 1610678276, (1610678276, (), [ ], 1 , 1 , 4 , 0 , 56 , (13, 0, None, IID('{7AA0E540-0301-11D4-A30E-00C026EE094F}')) , 0 , )),
	(( 'GetSurface' , ), 1610678277, (1610678277, (), [ ], 1 , 1 , 4 , 0 , 64 , (13, 0, None, IID('{081C7F2D-D5BC-40A6-92FE-C16B67D10B75}')) , 0 , )),
	(( 'LoopCollection' , ), 1610678278, (1610678278, (), [ ], 1 , 1 , 4 , 0 , 72 , (13, 0, None, IID('{22866947-F414-484B-8CCC-F4440BFEF92F}')) , 0 , )),
	(( 'GetNormalOrientation' , ), 1610678279, (1610678279, (), [ ], 1 , 1 , 4 , 0 , 80 , (3, 0, None, None) , 0 , )),
	(( 'IsConnectedWith' , 'faceDefinition' , ), 1610678280, (1610678280, (), [ (13, 0, None, "IID('{7AA0E540-0322-11D4-A30E-00C026EE094F}')") , ], 1 , 1 , 4 , 0 , 88 , (3, 0, None, None) , 0 , )),
	(( 'ConnectedFaceCollection' , ), 1610678281, (1610678281, (), [ ], 1 , 1 , 4 , 0 , 96 , (13, 0, None, IID('{D269AD47-B2CC-4152-A7BA-127242371208}')) , 0 , )),
	(( 'EdgeCollection' , ), 1610678282, (1610678282, (), [ ], 1 , 1 , 4 , 0 , 104 , (13, 0, None, IID('{5E93D4B9-BAAB-4FC4-ACF8-8FF78E9D1B42}')) , 0 , )),
	(( 'GetNextFace' , ), 1610678283, (1610678283, (), [ ], 1 , 1 , 4 , 0 , 112 , (13, 0, None, IID('{7AA0E540-0322-11D4-A30E-00C026EE094F}')) , 0 , )),
	(( 'IsTorus' , ), 1610678284, (1610678284, (), [ ], 1 , 1 , 4 , 0 , 120 , (3, 0, None, None) , 0 , )),
	(( 'IsSphere' , ), 1610678285, (1610678285, (), [ ], 1 , 1 , 4 , 0 , 128 , (3, 0, None, None) , 0 , )),
	(( 'IsNurbsSurface' , ), 1610678286, (1610678286, (), [ ], 1 , 1 , 4 , 0 , 136 , (3, 0, None, None) , 0 , )),
	(( 'IsRevolved' , ), 1610678287, (1610678287, (), [ ], 1 , 1 , 4 , 0 , 144 , (3, 0, None, None) , 0 , )),
	(( 'IsSwept' , ), 1610678288, (1610678288, (), [ ], 1 , 1 , 4 , 0 , 152 , (3, 0, None, None) , 0 , )),
	(( 'GetTessellation' , ), 1610678289, (1610678289, (), [ ], 1 , 1 , 4 , 0 , 160 , (13, 0, None, IID('{5F12CD9D-4310-4A6B-B4B8-B1445ABB36D8}')) , 0 , )),
	(( 'GetArea' , 'bitVector' , ), 1610678290, (1610678290, (), [ (19, 0, None, None) , ], 1 , 1 , 4 , 0 , 168 , (5, 0, None, None) , 0 , )),
	(( 'GetEntity' , ), 1610678291, (1610678291, (), [ ], 1 , 1 , 4 , 0 , 176 , (13, 0, None, IID('{7AA0E540-0301-11D4-A30E-00C026EE094F}')) , 0 , )),
	(( 'IsValid' , ), 1610678292, (1610678292, (), [ ], 1 , 1 , 4 , 0 , 184 , (3, 0, None, None) , 0 , )),
]

IFacet_vtables_dispatch_ = 0
IFacet_vtables_ = [
	(( 'GetPointsCount' , ), 1610678272, (1610678272, (), [ ], 1 , 1 , 4 , 0 , 24 , (3, 0, None, None) , 0 , )),
	(( 'GetPoint' , 'index' , 'x' , 'y' , 'z' , 
			 ), 1610678273, (1610678273, (), [ (3, 1, None, None) , (16388, 2, None, None) , (16388, 2, None, None) , (16388, 2, None, None) , ], 1 , 1 , 4 , 0 , 32 , (3, 0, None, None) , 0 , )),
	(( 'GetNormal' , 'index' , 'x' , 'y' , 'z' , 
			 ), 1610678274, (1610678274, (), [ (3, 1, None, None) , (16388, 2, None, None) , (16388, 2, None, None) , (16388, 2, None, None) , ], 1 , 1 , 4 , 0 , 40 , (3, 0, None, None) , 0 , )),
	(( 'GetTessellationIndex' , 'index' , ), 1610678275, (1610678275, (), [ (3, 0, None, None) , ], 1 , 1 , 4 , 0 , 48 , (3, 0, None, None) , 0 , )),
]

IFeature_vtables_dispatch_ = 0
IFeature_vtables_ = [
	(( 'GetName' , ), 1610678272, (1610678272, (), [ ], 1 , 1 , 4 , 0 , 24 , (31, 0, None, None) , 0 , )),
	(( 'GetUpdateStamp' , ), 1610678273, (1610678273, (), [ ], 1 , 1 , 4 , 0 , 32 , (19, 0, None, None) , 0 , )),
	(( 'IsModified' , 'recursive' , ), 1610678274, (1610678274, (), [ (3, 0, None, None) , ], 1 , 1 , 4 , 0 , 40 , (3, 0, None, None) , 0 , )),
	(( 'SubFeatureCollection' , 'through' , 'libObject' , ), 1610678275, (1610678275, (), [ (3, 0, None, None) , 
			 (3, 0, None, None) , ], 1 , 1 , 4 , 0 , 48 , (13, 0, None, IID('{CE5D4888-9006-43AC-9ACC-6D9E58B408B4}')) , 0 , )),
	(( 'GetOwnerFeature' , ), 1610678276, (1610678276, (), [ ], 1 , 1 , 4 , 0 , 56 , (13, 0, None, IID('{1D15245B-695E-4F9F-AFCA-EACBC3A055BB}')) , 0 , )),
	(( 'IsValid' , ), 1610678277, (1610678277, (), [ ], 1 , 1 , 4 , 0 , 64 , (3, 0, None, None) , 0 , )),
	(( 'GetType' , ), 1610678278, (1610678278, (), [ ], 1 , 1 , 4 , 0 , 72 , (2, 0, None, None) , 0 , )),
	(( 'GetObject' , ), 1610678279, (1610678279, (), [ ], 1 , 1 , 4 , 0 , 80 , (13, 0, None, None) , 0 , )),
	(( 'SetExcluded' , 'exclude' , ), 1610678280, (1610678280, (), [ (3, 0, None, None) , ], 1 , 1 , 4 , 0 , 88 , (3, 0, None, None) , 0 , )),
	(( 'GetExcluded' , ), 1610678281, (1610678281, (), [ ], 1 , 1 , 4 , 0 , 96 , (3, 0, None, None) , 0 , )),
	(( 'AttributeCollection' , 'key1' , 'key2' , 'key3' , 'key4' , 
			 'numb' , ), 1610678282, (1610678282, (), [ (3, 0, None, None) , (3, 0, None, None) , (3, 0, None, None) , 
			 (3, 0, None, None) , (5, 0, None, None) , ], 1 , 1 , 4 , 0 , 104 , (13, 0, None, IID('{E17C2BE7-9C11-4FB3-ADBD-04EC912784E8}')) , 0 , )),
	(( 'EntityCollection' , 'objType' , ), 1610678283, (1610678283, (), [ (2, 0, None, None) , ], 1 , 1 , 4 , 0 , 112 , (13, 0, None, IID('{7AA0E540-0303-11D4-A30E-00C026EE094F}')) , 0 , )),
	(( 'VariableCollection' , ), 1610678284, (1610678284, (), [ ], 1 , 1 , 4 , 0 , 120 , (13, 0, None, IID('{7AA0E540-0311-11D4-A30E-00C026EE094F}')) , 0 , )),
	(( 'BodyCollection' , ), 1610678285, (1610678285, (), [ ], 1 , 1 , 4 , 0 , 128 , (13, 0, None, IID('{64CBC7CB-005D-47DF-8B3E-53FD974C5A32}')) , 0 , )),
	(( 'AttributeCollectionEx' , 'key1' , 'key2' , 'key3' , 'key4' , 
			 'numb' , 'sourcePart' , ), 1610678286, (1610678286, (), [ (3, 0, None, None) , (3, 0, None, None) , 
			 (3, 0, None, None) , (3, 0, None, None) , (5, 0, None, None) , (13, 0, None, "IID('{7AA0E540-0300-11D4-A30E-00C026EE094F}')") , ], 1 , 1 , 4 , 0 , 136 , (13, 0, None, IID('{E17C2BE7-9C11-4FB3-ADBD-04EC912784E8}')) , 0 , )),
	(( 'IsRollBacked' , ), 1610678287, (1610678287, (), [ ], 1 , 1 , 4 , 0 , 144 , (3, 0, None, None) , 0 , )),
	(( 'VariableCollectionEx' , 'sourse' , ), 1610678288, (1610678288, (), [ (3, 0, None, None) , ], 1 , 1 , 4 , 0 , 152 , (13, 0, None, IID('{7AA0E540-0311-11D4-A30E-00C026EE094F}')) , 0 , )),
	(( 'GetObjectError' , ), 1610678289, (1610678289, (), [ ], 1 , 1 , 4 , 0 , 160 , (3, 0, None, None) , 0 , )),
]

IFeatureCollection_vtables_dispatch_ = 0
IFeatureCollection_vtables_ = [
	(( 'Refresh' , ), 1610678272, (1610678272, (), [ ], 1 , 1 , 4 , 0 , 24 , (3, 0, None, None) , 0 , )),
	(( 'GetCount' , ), 1610678273, (1610678273, (), [ ], 1 , 1 , 4 , 0 , 32 , (3, 0, None, None) , 0 , )),
	(( 'First' , ), 1610678274, (1610678274, (), [ ], 1 , 1 , 4 , 0 , 40 , (13, 0, None, IID('{1D15245B-695E-4F9F-AFCA-EACBC3A055BB}')) , 0 , )),
	(( 'Last' , ), 1610678275, (1610678275, (), [ ], 1 , 1 , 4 , 0 , 48 , (13, 0, None, IID('{1D15245B-695E-4F9F-AFCA-EACBC3A055BB}')) , 0 , )),
	(( 'Next' , ), 1610678276, (1610678276, (), [ ], 1 , 1 , 4 , 0 , 56 , (13, 0, None, IID('{1D15245B-695E-4F9F-AFCA-EACBC3A055BB}')) , 0 , )),
	(( 'Prev' , ), 1610678277, (1610678277, (), [ ], 1 , 1 , 4 , 0 , 64 , (13, 0, None, IID('{1D15245B-695E-4F9F-AFCA-EACBC3A055BB}')) , 0 , )),
	(( 'GetByIndex' , 'index' , ), 1610678278, (1610678278, (), [ (3, 0, None, None) , ], 1 , 1 , 4 , 0 , 72 , (13, 0, None, IID('{1D15245B-695E-4F9F-AFCA-EACBC3A055BB}')) , 0 , )),
	(( 'GetByName' , 'name' , 'testFullName' , 'testIgnoreCase' , ), 1610678279, (1610678279, (), [ 
			 (31, 0, None, None) , (3, 0, None, None) , (3, 0, None, None) , ], 1 , 1 , 4 , 0 , 80 , (13, 0, None, IID('{1D15245B-695E-4F9F-AFCA-EACBC3A055BB}')) , 0 , )),
	(( 'FindIt' , 'mate' , ), 1610678280, (1610678280, (), [ (13, 0, None, "IID('{1D15245B-695E-4F9F-AFCA-EACBC3A055BB}')") , ], 1 , 1 , 4 , 0 , 88 , (19, 0, None, None) , 0 , )),
	(( 'Add' , 'obj' , ), 1610678281, (1610678281, (), [ (13, 0, None, "IID('{1D15245B-695E-4F9F-AFCA-EACBC3A055BB}')") , ], 1 , 1 , 4 , 0 , 96 , (3, 0, None, None) , 0 , )),
	(( 'AddAt' , 'obj' , 'index' , ), 1610678282, (1610678282, (), [ (13, 0, None, "IID('{1D15245B-695E-4F9F-AFCA-EACBC3A055BB}')") , 
			 (3, 0, None, None) , ], 1 , 1 , 4 , 0 , 104 , (3, 0, None, None) , 0 , )),
	(( 'AddBefore' , 'obj' , 'base' , ), 1610678283, (1610678283, (), [ (13, 0, None, "IID('{1D15245B-695E-4F9F-AFCA-EACBC3A055BB}')") , 
			 (13, 0, None, "IID('{1D15245B-695E-4F9F-AFCA-EACBC3A055BB}')") , ], 1 , 1 , 4 , 0 , 112 , (3, 0, None, None) , 0 , )),
	(( 'DetachByIndex' , 'index' , ), 1610678284, (1610678284, (), [ (3, 0, None, None) , ], 1 , 1 , 4 , 0 , 120 , (3, 0, None, None) , 0 , )),
	(( 'DetachByBody' , 'obj' , ), 1610678285, (1610678285, (), [ (13, 0, None, "IID('{1D15245B-695E-4F9F-AFCA-EACBC3A055BB}')") , ], 1 , 1 , 4 , 0 , 128 , (3, 0, None, None) , 0 , )),
	(( 'Clear' , ), 1610678286, (1610678286, (), [ ], 1 , 1 , 4 , 0 , 136 , (3, 0, None, None) , 0 , )),
	(( 'SetByIndex' , 'obj' , 'index' , ), 1610678287, (1610678287, (), [ (13, 0, None, "IID('{1D15245B-695E-4F9F-AFCA-EACBC3A055BB}')") , 
			 (3, 0, None, None) , ], 1 , 1 , 4 , 0 , 144 , (3, 0, None, None) , 0 , )),
	(( 'AttributeCollection' , 'key1' , 'key2' , 'key3' , 'key4' , 
			 'numb' , ), 1610678288, (1610678288, (), [ (3, 0, None, None) , (3, 0, None, None) , (3, 0, None, None) , 
			 (3, 0, None, None) , (5, 0, None, None) , ], 1 , 1 , 4 , 0 , 152 , (13, 0, None, IID('{E17C2BE7-9C11-4FB3-ADBD-04EC912784E8}')) , 0 , )),
]

IFilletDefinition_vtables_dispatch_ = 0
IFilletDefinition_vtables_ = [
	(( 'GetRadius' , ), 1610678272, (1610678272, (), [ ], 1 , 1 , 4 , 0 , 24 , (5, 0, None, None) , 0 , )),
	(( 'SetRadius' , 'radius' , ), 1610678273, (1610678273, (), [ (5, 0, None, None) , ], 1 , 1 , 4 , 0 , 32 , (24, 0, None, None) , 0 , )),
	(( 'GetTangent' , ), 1610678274, (1610678274, (), [ ], 1 , 1 , 4 , 0 , 40 , (3, 0, None, None) , 0 , )),
	(( 'SetTangent' , 'val' , ), 1610678275, (1610678275, (), [ (3, 0, None, None) , ], 1 , 1 , 4 , 0 , 48 , (24, 0, None, None) , 0 , )),
	(( 'Array' , ), 1610678276, (1610678276, (), [ ], 1 , 1 , 4 , 0 , 56 , (13, 0, None, IID('{7AA0E540-0303-11D4-A30E-00C026EE094F}')) , 0 , )),
]

IImportedSurfaceDefinition_vtables_dispatch_ = 0
IImportedSurfaceDefinition_vtables_ = [
	(( 'Clear' , ), 1610678272, (1610678272, (), [ ], 1 , 1 , 4 , 0 , 24 , (3, 0, None, None) , 0 , )),
	(( 'BeginCurve' , ), 1610678273, (1610678273, (), [ ], 1 , 1 , 4 , 0 , 32 , (3, 0, None, None) , 0 , )),
	(( 'AddPoint' , 'x' , 'y' , 'z' , ), 1610678274, (1610678274, (), [ 
			 (5, 0, None, None) , (5, 0, None, None) , (5, 0, None, None) , ], 1 , 1 , 4 , 0 , 40 , (3, 0, None, None) , 0 , )),
	(( 'EndCurve' , ), 1610678275, (1610678275, (), [ ], 1 , 1 , 4 , 0 , 48 , (3, 0, None, None) , 0 , )),
	(( 'AddCurve' , 'arr' , ), 1610678276, (1610678276, (), [ (12, 0, None, None) , ], 1 , 1 , 4 , 0 , 56 , (3, 0, None, None) , 0 , )),
]

IInclineDefinition_vtables_dispatch_ = 0
IInclineDefinition_vtables_ = [
	(( 'FaceArray' , ), 1610678272, (1610678272, (), [ ], 1 , 1 , 4 , 0 , 24 , (13, 0, None, IID('{7AA0E540-0303-11D4-A30E-00C026EE094F}')) , 0 , )),
	(( 'GetAngle' , ), 1610678273, (1610678273, (), [ ], 1 , 1 , 4 , 0 , 32 , (5, 0, None, None) , 0 , )),
	(( 'SetAngle' , 'angle' , ), 1610678274, (1610678274, (), [ (5, 0, None, None) , ], 1 , 1 , 4 , 0 , 40 , (3, 0, None, None) , 0 , )),
	(( 'GetDirection' , ), 1610678275, (1610678275, (), [ ], 1 , 1 , 4 , 0 , 48 , (3, 0, None, None) , 0 , )),
	(( 'SetDirection' , 'direction' , ), 1610678276, (1610678276, (), [ (3, 0, None, None) , ], 1 , 1 , 4 , 0 , 56 , (3, 0, None, None) , 0 , )),
	(( 'GetPlane' , ), 1610678277, (1610678277, (), [ ], 1 , 1 , 4 , 0 , 64 , (13, 0, None, IID('{7AA0E540-0301-11D4-A30E-00C026EE094F}')) , 0 , )),
	(( 'SetPlane' , 'plane' , ), 1610678278, (1610678278, (), [ (13, 0, None, "IID('{7AA0E540-0301-11D4-A30E-00C026EE094F}')") , ], 1 , 1 , 4 , 0 , 72 , (3, 0, None, None) , 0 , )),
]

IIntersectionResult_vtables_dispatch_ = 0
IIntersectionResult_vtables_ = [
	(( 'GetCount' , ), 1610678272, (1610678272, (), [ ], 1 , 1 , 4 , 0 , 24 , (3, 0, None, None) , 0 , )),
	(( 'GetIntersectionType' , 'index' , ), 1610678273, (1610678273, (), [ (3, 0, None, None) , ], 1 , 1 , 4 , 0 , 32 , (3, 0, None, None) , 0 , )),
]

ILineSeg3dParam_vtables_dispatch_ = 0
ILineSeg3dParam_vtables_ = [
	(( 'GetPointFirst' , 'x' , 'y' , 'z' , ), 1610678272, (1610678272, (), [ 
			 (16389, 0, None, None) , (16389, 0, None, None) , (16389, 0, None, None) , ], 1 , 1 , 4 , 0 , 24 , (3, 0, None, None) , 0 , )),
	(( 'GetPointLast' , 'x' , 'y' , 'z' , ), 1610678273, (1610678273, (), [ 
			 (16389, 0, None, None) , (16389, 0, None, None) , (16389, 0, None, None) , ], 1 , 1 , 4 , 0 , 32 , (3, 0, None, None) , 0 , )),
]

ILoftSurfaceDefinition_vtables_dispatch_ = 0
ILoftSurfaceDefinition_vtables_ = [
	(( 'GetLoftParam' , 'closed' , 'flipVertex' , 'autoPath' , ), 1610678272, (1610678272, (), [ 
			 (16387, 0, None, None) , (16387, 0, None, None) , (16387, 0, None, None) , ], 1 , 1 , 4 , 0 , 24 , (3, 0, None, None) , 0 , )),
	(( 'SetLoftParam' , 'closed' , 'flipVertex' , 'autoPath' , ), 1610678273, (1610678273, (), [ 
			 (3, 0, None, None) , (3, 0, None, None) , (3, 0, None, None) , ], 1 , 1 , 4 , 0 , 32 , (24, 0, None, None) , 0 , )),
	(( 'Sketchs' , ), 1610678274, (1610678274, (), [ ], 1 , 1 , 4 , 0 , 40 , (13, 0, None, IID('{7AA0E540-0303-11D4-A30E-00C026EE094F}')) , 0 , )),
	(( 'GetClosedShell' , ), 1610678275, (1610678275, (), [ ], 1 , 1 , 4 , 0 , 48 , (3, 0, None, None) , 0 , )),
	(( 'SetClosedShell' , 'closed' , ), 1610678276, (1610678276, (), [ (3, 0, None, None) , ], 1 , 1 , 4 , 0 , 56 , (3, 0, None, None) , 0 , )),
	(( 'GetDirectionalLine' , ), 1610678277, (1610678277, (), [ ], 1 , 1 , 4 , 0 , 64 , (13, 0, None, IID('{7AA0E540-0301-11D4-A30E-00C026EE094F}')) , 0 , )),
	(( 'SetDirectionalLine' , 'sketch' , ), 1610678278, (1610678278, (), [ (13, 0, None, "IID('{7AA0E540-0301-11D4-A30E-00C026EE094F}')") , ], 1 , 1 , 4 , 0 , 72 , (3, 0, None, None) , 0 , )),
]

ILoop_vtables_dispatch_ = 0
ILoop_vtables_ = [
	(( 'OrientedEdgeCollection' , 'val' , ), 1610678272, (1610678272, (), [ (13, 0, None, "IID('{7AA0E540-0321-11D4-A30E-00C026EE094F}')") , ], 1 , 1 , 4 , 0 , 24 , (13, 0, None, IID('{D19B0A07-4CA6-4E77-A8DB-8AC8C7123124}')) , 0 , )),
	(( 'EdgeCollection' , ), 1610678273, (1610678273, (), [ ], 1 , 1 , 4 , 0 , 32 , (13, 0, None, IID('{5E93D4B9-BAAB-4FC4-ACF8-8FF78E9D1B42}')) , 0 , )),
	(( 'IsOuter' , ), 1610678274, (1610678274, (), [ ], 1 , 1 , 4 , 0 , 40 , (3, 0, None, None) , 0 , )),
	(( 'GetLength' , 'bitVector' , ), 1610678275, (1610678275, (), [ (19, 0, None, None) , ], 1 , 1 , 4 , 0 , 48 , (5, 0, None, None) , 0 , )),
]

ILoopCollection_vtables_dispatch_ = 0
ILoopCollection_vtables_ = [
	(( 'Refresh' , ), 1610678272, (1610678272, (), [ ], 1 , 1 , 4 , 0 , 24 , (3, 0, None, None) , 0 , )),
	(( 'GetCount' , ), 1610678273, (1610678273, (), [ ], 1 , 1 , 4 , 0 , 32 , (3, 0, None, None) , 0 , )),
	(( 'First' , ), 1610678274, (1610678274, (), [ ], 1 , 1 , 4 , 0 , 40 , (13, 0, None, IID('{56965A12-03BB-4068-8AE9-BEFC23EEEB37}')) , 0 , )),
	(( 'Last' , ), 1610678275, (1610678275, (), [ ], 1 , 1 , 4 , 0 , 48 , (13, 0, None, IID('{56965A12-03BB-4068-8AE9-BEFC23EEEB37}')) , 0 , )),
	(( 'Next' , ), 1610678276, (1610678276, (), [ ], 1 , 1 , 4 , 0 , 56 , (13, 0, None, IID('{56965A12-03BB-4068-8AE9-BEFC23EEEB37}')) , 0 , )),
	(( 'Prev' , ), 1610678277, (1610678277, (), [ ], 1 , 1 , 4 , 0 , 64 , (13, 0, None, IID('{56965A12-03BB-4068-8AE9-BEFC23EEEB37}')) , 0 , )),
	(( 'GetByIndex' , 'index' , ), 1610678278, (1610678278, (), [ (3, 0, None, None) , ], 1 , 1 , 4 , 0 , 72 , (13, 0, None, IID('{56965A12-03BB-4068-8AE9-BEFC23EEEB37}')) , 0 , )),
	(( 'FindIt' , 'entity' , ), 1610678279, (1610678279, (), [ (13, 0, None, "IID('{56965A12-03BB-4068-8AE9-BEFC23EEEB37}')") , ], 1 , 1 , 4 , 0 , 80 , (19, 0, None, None) , 0 , )),
]

IMacro3DDefinition_vtables_dispatch_ = 0
IMacro3DDefinition_vtables_ = [
	(( 'FeatureCollection' , ), 1610678272, (1610678272, (), [ ], 1 , 1 , 4 , 0 , 24 , (13, 0, None, IID('{CE5D4888-9006-43AC-9ACC-6D9E58B408B4}')) , 0 , )),
	(( 'GetStaffVisible' , ), 1610678273, (1610678273, (), [ ], 1 , 1 , 4 , 0 , 32 , (3, 0, None, None) , 0 , )),
	(( 'SetStaffVisible' , 'val' , ), 1610678274, (1610678274, (), [ (3, 0, None, None) , ], 1 , 1 , 4 , 0 , 40 , (3, 0, None, None) , 0 , )),
	(( 'Destroy' , ), 1610678275, (1610678275, (), [ ], 1 , 1 , 4 , 0 , 48 , (3, 0, None, None) , 0 , )),
	(( 'Add' , 'obj' , ), 1610678276, (1610678276, (), [ (13, 0, None, None) , ], 1 , 1 , 4 , 0 , 56 , (3, 0, None, None) , 0 , )),
	(( 'SetUserParam' , 'userParam' , 'size' , 'nameFile' , 'nameLib' , 
			 'number' , ), 1610678277, (1610678277, (), [ (16408, 0, None, None) , (3, 0, None, None) , (31, 0, None, None) , 
			 (31, 0, None, None) , (3, 0, None, None) , ], 1 , 1 , 4 , 0 , 64 , (3, 0, None, None) , 0 , )),
	(( 'GetUserParamSize' , ), 1610678278, (1610678278, (), [ ], 1 , 1 , 4 , 0 , 72 , (3, 0, None, None) , 0 , )),
	(( 'GetUserParam' , 'userParam' , 'size' , ), 1610678279, (1610678279, (), [ (16408, 0, None, None) , 
			 (3, 0, None, None) , ], 1 , 1 , 4 , 0 , 80 , (3, 0, None, None) , 0 , )),
	(( 'GetUserLibraryFileName' , ), 1610678280, (1610678280, (), [ ], 1 , 1 , 4 , 0 , 88 , (31, 0, None, None) , 0 , )),
	(( 'GetUserLibraryName' , ), 1610678281, (1610678281, (), [ ], 1 , 1 , 4 , 0 , 96 , (31, 0, None, None) , 0 , )),
	(( 'GetUserLibraryCommand' , ), 1610678282, (1610678282, (), [ ], 1 , 1 , 4 , 0 , 104 , (3, 0, None, None) , 0 , )),
	(( 'SetObject' , 'index' , 'obj' , ), 1610678283, (1610678283, (), [ (3, 0, None, None) , 
			 (13, 0, None, None) , ], 1 , 1 , 4 , 0 , 112 , (3, 0, None, None) , 0 , )),
	(( 'GetObject' , 'index' , ), 1610678284, (1610678284, (), [ (3, 0, None, None) , ], 1 , 1 , 4 , 0 , 120 , (13, 0, None, None) , 0 , )),
	(( 'GetCountObj' , ), 1610678285, (1610678285, (), [ ], 1 , 1 , 4 , 0 , 128 , (3, 0, None, None) , 0 , )),
	(( 'ClearAllObj' , ), 1610678286, (1610678286, (), [ ], 1 , 1 , 4 , 0 , 136 , (3, 0, None, None) , 0 , )),
	(( 'GetDoubleClickEditOff' , ), 1610678287, (1610678287, (), [ ], 1 , 1 , 4 , 0 , 144 , (3, 0, None, None) , 0 , )),
	(( 'SetDoubleClickEditOff' , 'val' , ), 1610678288, (1610678288, (), [ (3, 0, None, None) , ], 1 , 1 , 4 , 0 , 152 , (3, 0, None, None) , 0 , )),
	(( 'GetPropertyObjectEditable' , ), 1610678289, (1610678289, (), [ ], 1 , 1 , 4 , 0 , 160 , (3, 0, None, None) , 0 , )),
	(( 'SetPropertyObjectEditable' , 'PVal' , ), 1610678290, (1610678290, (), [ (3, 0, None, None) , ], 1 , 1 , 4 , 0 , 168 , (3, 0, None, None) , 0 , )),
]

IMassInertiaParam_vtables_dispatch_ = 0
IMassInertiaParam_vtables_ = [
	(( 'GetXc' , ), 1610678272, (1610678272, (), [ ], 1 , 1 , 4 , 0 , 24 , (5, 0, None, None) , 0 , )),
	(( 'GetYc' , ), 1610678273, (1610678273, (), [ ], 1 , 1 , 4 , 0 , 32 , (5, 0, None, None) , 0 , )),
	(( 'GetZc' , ), 1610678274, (1610678274, (), [ ], 1 , 1 , 4 , 0 , 40 , (5, 0, None, None) , 0 , )),
	(( 'GetLx' , ), 1610678275, (1610678275, (), [ ], 1 , 1 , 4 , 0 , 48 , (5, 0, None, None) , 0 , )),
	(( 'GetLy' , ), 1610678276, (1610678276, (), [ ], 1 , 1 , 4 , 0 , 56 , (5, 0, None, None) , 0 , )),
	(( 'GetLz' , ), 1610678277, (1610678277, (), [ ], 1 , 1 , 4 , 0 , 64 , (5, 0, None, None) , 0 , )),
	(( 'GetLxy' , ), 1610678278, (1610678278, (), [ ], 1 , 1 , 4 , 0 , 72 , (5, 0, None, None) , 0 , )),
	(( 'GetLxz' , ), 1610678279, (1610678279, (), [ ], 1 , 1 , 4 , 0 , 80 , (5, 0, None, None) , 0 , )),
	(( 'GetLyz' , ), 1610678280, (1610678280, (), [ ], 1 , 1 , 4 , 0 , 88 , (5, 0, None, None) , 0 , )),
	(( 'GetJx' , ), 1610678281, (1610678281, (), [ ], 1 , 1 , 4 , 0 , 96 , (5, 0, None, None) , 0 , )),
	(( 'GetJy' , ), 1610678282, (1610678282, (), [ ], 1 , 1 , 4 , 0 , 104 , (5, 0, None, None) , 0 , )),
	(( 'GetJz' , ), 1610678283, (1610678283, (), [ ], 1 , 1 , 4 , 0 , 112 , (5, 0, None, None) , 0 , )),
	(( 'GetJxy' , ), 1610678284, (1610678284, (), [ ], 1 , 1 , 4 , 0 , 120 , (5, 0, None, None) , 0 , )),
	(( 'GetJxz' , ), 1610678285, (1610678285, (), [ ], 1 , 1 , 4 , 0 , 128 , (5, 0, None, None) , 0 , )),
	(( 'GetJyz' , ), 1610678286, (1610678286, (), [ ], 1 , 1 , 4 , 0 , 136 , (5, 0, None, None) , 0 , )),
	(( 'GetJx0' , ), 1610678287, (1610678287, (), [ ], 1 , 1 , 4 , 0 , 144 , (5, 0, None, None) , 0 , )),
	(( 'GetJy0' , ), 1610678288, (1610678288, (), [ ], 1 , 1 , 4 , 0 , 152 , (5, 0, None, None) , 0 , )),
	(( 'GetJz0' , ), 1610678289, (1610678289, (), [ ], 1 , 1 , 4 , 0 , 160 , (5, 0, None, None) , 0 , )),
	(( 'GetAxisX' , 'x' , 'y' , 'z' , ), 1610678290, (1610678290, (), [ 
			 (16389, 0, None, None) , (16389, 0, None, None) , (16389, 0, None, None) , ], 1 , 1 , 4 , 0 , 168 , (3, 0, None, None) , 0 , )),
	(( 'GetAxisY' , 'x' , 'y' , 'z' , ), 1610678291, (1610678291, (), [ 
			 (16389, 0, None, None) , (16389, 0, None, None) , (16389, 0, None, None) , ], 1 , 1 , 4 , 0 , 176 , (3, 0, None, None) , 0 , )),
	(( 'GetAxisZ' , 'x' , 'y' , 'z' , ), 1610678292, (1610678292, (), [ 
			 (16389, 0, None, None) , (16389, 0, None, None) , (16389, 0, None, None) , ], 1 , 1 , 4 , 0 , 184 , (3, 0, None, None) , 0 , )),
	(( 'GetR' , ), 1610678293, (1610678293, (), [ ], 1 , 1 , 4 , 0 , 192 , (5, 0, None, None) , 0 , )),
	(( 'GetM' , ), 1610678294, (1610678294, (), [ ], 1 , 1 , 4 , 0 , 200 , (5, 0, None, None) , 0 , )),
	(( 'GetV' , ), 1610678295, (1610678295, (), [ ], 1 , 1 , 4 , 0 , 208 , (5, 0, None, None) , 0 , )),
	(( 'GetF' , ), 1610678296, (1610678296, (), [ ], 1 , 1 , 4 , 0 , 216 , (5, 0, None, None) , 0 , )),
	(( 'SetBitVectorValue' , 'val' , 'setState' , ), 1610678297, (1610678297, (), [ (19, 0, None, None) , 
			 (3, 0, None, None) , ], 1 , 1 , 4 , 0 , 224 , (3, 0, None, None) , 0 , )),
]

IMateConstraint_vtables_dispatch_ = 0
IMateConstraint_vtables_ = [
	(( 'SetConstraintType' , 'type' , ), 1610678272, (1610678272, (), [ (2, 0, None, None) , ], 1 , 1 , 4 , 0 , 24 , (3, 0, None, None) , 0 , )),
	(( 'GetConstraintType' , ), 1610678273, (1610678273, (), [ ], 1 , 1 , 4 , 0 , 32 , (2, 0, None, None) , 0 , )),
	(( 'SetBaseObj' , 'number' , 'obj' , ), 1610678274, (1610678274, (), [ (2, 0, None, None) , 
			 (13, 0, None, "IID('{7AA0E540-0301-11D4-A30E-00C026EE094F}')") , ], 1 , 1 , 4 , 0 , 40 , (3, 0, None, None) , 0 , )),
	(( 'GetBaseObj' , 'number' , ), 1610678275, (1610678275, (), [ (2, 0, None, None) , ], 1 , 1 , 4 , 0 , 48 , (13, 0, None, IID('{7AA0E540-0301-11D4-A30E-00C026EE094F}')) , 0 , )),
	(( 'SetDirection' , 'direction' , ), 1610678276, (1610678276, (), [ (2, 0, None, None) , ], 1 , 1 , 4 , 0 , 56 , (3, 0, None, None) , 0 , )),
	(( 'GetDirection' , ), 1610678277, (1610678277, (), [ ], 1 , 1 , 4 , 0 , 64 , (2, 0, None, None) , 0 , )),
	(( 'SetFixed' , 'direction' , ), 1610678278, (1610678278, (), [ (2, 0, None, None) , ], 1 , 1 , 4 , 0 , 72 , (3, 0, None, None) , 0 , )),
	(( 'GetFixed' , ), 1610678279, (1610678279, (), [ ], 1 , 1 , 4 , 0 , 80 , (2, 0, None, None) , 0 , )),
	(( 'SetDistance' , 'distance' , ), 1610678280, (1610678280, (), [ (5, 0, None, None) , ], 1 , 1 , 4 , 0 , 88 , (3, 0, None, None) , 0 , )),
	(( 'GetDistance' , ), 1610678281, (1610678281, (), [ ], 1 , 1 , 4 , 0 , 96 , (5, 0, None, None) , 0 , )),
	(( 'Create' , ), 1610678282, (1610678282, (), [ ], 1 , 1 , 4 , 0 , 104 , (3, 0, None, None) , 0 , )),
	(( 'GetFeature' , ), 1610678283, (1610678283, (), [ ], 1 , 1 , 4 , 0 , 112 , (13, 0, None, IID('{1D15245B-695E-4F9F-AFCA-EACBC3A055BB}')) , 0 , )),
	(( 'GetEntityParams' , 'number' , 'params' , ), 1610678284, (1610678284, (), [ (2, 1, None, None) , 
			 (16396, 2, None, None) , ], 1 , 1 , 4 , 0 , 120 , (3, 0, None, None) , 0 , )),
]

IMateConstraintCollection_vtables_dispatch_ = 0
IMateConstraintCollection_vtables_ = [
	(( 'GetCount' , ), 1610678272, (1610678272, (), [ ], 1 , 1 , 4 , 0 , 24 , (3, 0, None, None) , 0 , )),
	(( 'First' , ), 1610678273, (1610678273, (), [ ], 1 , 1 , 4 , 0 , 32 , (13, 0, None, IID('{7AA0E540-0314-11D4-A30E-00C026EE094F}')) , 0 , )),
	(( 'Last' , ), 1610678274, (1610678274, (), [ ], 1 , 1 , 4 , 0 , 40 , (13, 0, None, IID('{7AA0E540-0314-11D4-A30E-00C026EE094F}')) , 0 , )),
	(( 'Next' , ), 1610678275, (1610678275, (), [ ], 1 , 1 , 4 , 0 , 48 , (13, 0, None, IID('{7AA0E540-0314-11D4-A30E-00C026EE094F}')) , 0 , )),
	(( 'Prev' , ), 1610678276, (1610678276, (), [ ], 1 , 1 , 4 , 0 , 56 , (13, 0, None, IID('{7AA0E540-0314-11D4-A30E-00C026EE094F}')) , 0 , )),
	(( 'GetByIndex' , 'index' , ), 1610678277, (1610678277, (), [ (3, 0, None, None) , ], 1 , 1 , 4 , 0 , 64 , (13, 0, None, IID('{7AA0E540-0314-11D4-A30E-00C026EE094F}')) , 0 , )),
	(( 'AddMateConstraint' , 'mate' , ), 1610678278, (1610678278, (), [ (13, 0, None, "IID('{7AA0E540-0314-11D4-A30E-00C026EE094F}')") , ], 1 , 1 , 4 , 0 , 72 , (3, 0, None, None) , 0 , )),
	(( 'RemoveMateConstraint' , 'mate' , ), 1610678279, (1610678279, (), [ (13, 0, None, "IID('{7AA0E540-0314-11D4-A30E-00C026EE094F}')") , ], 1 , 1 , 4 , 0 , 80 , (3, 0, None, None) , 0 , )),
	(( 'Clear' , ), 1610678280, (1610678280, (), [ ], 1 , 1 , 4 , 0 , 88 , (3, 0, None, None) , 0 , )),
	(( 'Refresh' , ), 1610678281, (1610678281, (), [ ], 1 , 1 , 4 , 0 , 96 , (3, 0, None, None) , 0 , )),
	(( 'FindIt' , 'mate' , ), 1610678282, (1610678282, (), [ (13, 0, None, "IID('{7AA0E540-0314-11D4-A30E-00C026EE094F}')") , ], 1 , 1 , 4 , 0 , 104 , (19, 0, None, None) , 0 , )),
	(( 'GetSafeArrayByObj' , 'obj' , 'pArray' , ), 1610678283, (1610678283, (), [ (13, 1, None, None) , 
			 (16396, 2, None, None) , ], 1 , 1 , 4 , 0 , 112 , (3, 0, None, None) , 0 , )),
]

IMeasurer_vtables_dispatch_ = 0
IMeasurer_vtables_ = [
	(( 'SetObject1' , 'obj' , ), 1610678272, (1610678272, (), [ (13, 0, None, "IID('{7AA0E540-0301-11D4-A30E-00C026EE094F}')") , ], 1 , 1 , 4 , 0 , 24 , (3, 0, None, None) , 0 , )),
	(( 'SetObject2' , 'obj' , ), 1610678273, (1610678273, (), [ (13, 0, None, "IID('{7AA0E540-0301-11D4-A30E-00C026EE094F}')") , ], 1 , 1 , 4 , 0 , 32 , (3, 0, None, None) , 0 , )),
	(( 'GetObject1' , ), 1610678274, (1610678274, (), [ ], 1 , 1 , 4 , 0 , 40 , (13, 0, None, IID('{7AA0E540-0301-11D4-A30E-00C026EE094F}')) , 0 , )),
	(( 'GetObject2' , ), 1610678275, (1610678275, (), [ ], 1 , 1 , 4 , 0 , 48 , (13, 0, None, IID('{7AA0E540-0301-11D4-A30E-00C026EE094F}')) , 0 , )),
	(( 'SetUnit' , 'bitVector' , ), 1610678276, (1610678276, (), [ (19, 0, None, None) , ], 1 , 1 , 4 , 0 , 56 , (3, 0, None, None) , 0 , )),
	(( 'GetUnit' , ), 1610678277, (1610678277, (), [ ], 1 , 1 , 4 , 0 , 64 , (3, 0, None, None) , 0 , )),
	(( 'SetExtendObject1' , 'ext' , ), 1610678278, (1610678278, (), [ (3, 0, None, None) , ], 1 , 1 , 4 , 0 , 72 , (3, 0, None, None) , 0 , )),
	(( 'SetExtendObject2' , 'ext' , ), 1610678279, (1610678279, (), [ (3, 0, None, None) , ], 1 , 1 , 4 , 0 , 80 , (3, 0, None, None) , 0 , )),
	(( 'GetExtendObject1' , ), 1610678280, (1610678280, (), [ ], 1 , 1 , 4 , 0 , 88 , (3, 0, None, None) , 0 , )),
	(( 'GetExtendObject2' , ), 1610678281, (1610678281, (), [ ], 1 , 1 , 4 , 0 , 96 , (3, 0, None, None) , 0 , )),
	(( 'Calc' , ), 1610678282, (1610678282, (), [ ], 1 , 1 , 4 , 0 , 104 , (3, 0, None, None) , 0 , )),
	(( 'IsAngleValid' , ), 1610678283, (1610678283, (), [ ], 1 , 1 , 4 , 0 , 112 , (3, 0, None, None) , 0 , )),
	(( 'GetAngle' , ), 1610678284, (1610678284, (), [ ], 1 , 1 , 4 , 0 , 120 , (5, 0, None, None) , 0 , )),
	(( 'GetDistance' , ), 1610678285, (1610678285, (), [ ], 1 , 1 , 4 , 0 , 128 , (5, 0, None, None) , 0 , )),
	(( 'GetPoint1' , 'x' , 'y' , 'z' , ), 1610678286, (1610678286, (), [ 
			 (16389, 0, None, None) , (16389, 0, None, None) , (16389, 0, None, None) , ], 1 , 1 , 4 , 0 , 136 , (3, 0, None, None) , 0 , )),
	(( 'GetPoint2' , 'x' , 'y' , 'z' , ), 1610678287, (1610678287, (), [ 
			 (16389, 0, None, None) , (16389, 0, None, None) , (16389, 0, None, None) , ], 1 , 1 , 4 , 0 , 144 , (3, 0, None, None) , 0 , )),
	(( 'GetMaxDistance' , ), 1610678288, (1610678288, (), [ ], 1 , 1 , 4 , 0 , 152 , (5, 0, None, None) , 0 , )),
	(( 'GetNormalDistance' , ), 1610678289, (1610678289, (), [ ], 1 , 1 , 4 , 0 , 160 , (5, 0, None, None) , 0 , )),
	(( 'GetMaxPoint1' , 'x' , 'y' , 'z' , ), 1610678290, (1610678290, (), [ 
			 (16389, 0, None, None) , (16389, 0, None, None) , (16389, 0, None, None) , ], 1 , 1 , 4 , 0 , 168 , (3, 0, None, None) , 0 , )),
	(( 'GetMaxPoint2' , 'x' , 'y' , 'z' , ), 1610678291, (1610678291, (), [ 
			 (16389, 0, None, None) , (16389, 0, None, None) , (16389, 0, None, None) , ], 1 , 1 , 4 , 0 , 176 , (3, 0, None, None) , 0 , )),
	(( 'GetNormalPoint1' , 'x' , 'y' , 'z' , ), 1610678292, (1610678292, (), [ 
			 (16389, 0, None, None) , (16389, 0, None, None) , (16389, 0, None, None) , ], 1 , 1 , 4 , 0 , 184 , (3, 0, None, None) , 0 , )),
	(( 'GetNormalPoint2' , 'x' , 'y' , 'z' , ), 1610678293, (1610678293, (), [ 
			 (16389, 0, None, None) , (16389, 0, None, None) , (16389, 0, None, None) , ], 1 , 1 , 4 , 0 , 192 , (3, 0, None, None) , 0 , )),
	(( 'GetMeasureResult' , ), 1610678294, (1610678294, (), [ ], 1 , 1 , 4 , 0 , 200 , (3, 0, None, None) , 0 , )),
	(( 'GetMinDistance' , ), 1610678295, (1610678295, (), [ ], 1 , 1 , 4 , 0 , 208 , (5, 0, None, None) , 0 , )),
	(( 'GetMinPoint1' , 'x' , 'y' , 'z' , ), 1610678296, (1610678296, (), [ 
			 (16389, 0, None, None) , (16389, 0, None, None) , (16389, 0, None, None) , ], 1 , 1 , 4 , 0 , 216 , (3, 0, None, None) , 0 , )),
	(( 'GetMinPoint2' , 'x' , 'y' , 'z' , ), 1610678297, (1610678297, (), [ 
			 (16389, 0, None, None) , (16389, 0, None, None) , (16389, 0, None, None) , ], 1 , 1 , 4 , 0 , 224 , (3, 0, None, None) , 0 , )),
]

IMeshPartArrayDefinition_vtables_dispatch_ = 0
IMeshPartArrayDefinition_vtables_ = [
	(( 'PartArray' , ), 1610678272, (1610678272, (), [ ], 1 , 1 , 4 , 0 , 24 , (13, 0, None, IID('{7AA0E540-0317-11D4-A30E-00C026EE094F}')) , 0 , )),
	(( 'GetAngle1' , ), 1610678273, (1610678273, (), [ ], 1 , 1 , 4 , 0 , 32 , (5, 0, None, None) , 0 , )),
	(( 'SetAngle1' , 'angle' , ), 1610678274, (1610678274, (), [ (5, 0, None, None) , ], 1 , 1 , 4 , 0 , 40 , (3, 0, None, None) , 0 , )),
	(( 'GetCount1' , ), 1610678275, (1610678275, (), [ ], 1 , 1 , 4 , 0 , 48 , (3, 0, None, None) , 0 , )),
	(( 'SetCount1' , 'count' , ), 1610678276, (1610678276, (), [ (3, 0, None, None) , ], 1 , 1 , 4 , 0 , 56 , (3, 0, None, None) , 0 , )),
	(( 'GetStep1' , ), 1610678277, (1610678277, (), [ ], 1 , 1 , 4 , 0 , 64 , (5, 0, None, None) , 0 , )),
	(( 'SetStep1' , 'step' , ), 1610678278, (1610678278, (), [ (5, 0, None, None) , ], 1 , 1 , 4 , 0 , 72 , (3, 0, None, None) , 0 , )),
	(( 'GetFactor1' , ), 1610678279, (1610678279, (), [ ], 1 , 1 , 4 , 0 , 80 , (3, 0, None, None) , 0 , )),
	(( 'SetFactor1' , 'factor' , ), 1610678280, (1610678280, (), [ (3, 0, None, None) , ], 1 , 1 , 4 , 0 , 88 , (3, 0, None, None) , 0 , )),
	(( 'GetAngle2' , ), 1610678281, (1610678281, (), [ ], 1 , 1 , 4 , 0 , 96 , (5, 0, None, None) , 0 , )),
	(( 'SetAngle2' , 'angle' , ), 1610678282, (1610678282, (), [ (5, 0, None, None) , ], 1 , 1 , 4 , 0 , 104 , (3, 0, None, None) , 0 , )),
	(( 'GetCount2' , ), 1610678283, (1610678283, (), [ ], 1 , 1 , 4 , 0 , 112 , (3, 0, None, None) , 0 , )),
	(( 'SetCount2' , 'count' , ), 1610678284, (1610678284, (), [ (3, 0, None, None) , ], 1 , 1 , 4 , 0 , 120 , (3, 0, None, None) , 0 , )),
	(( 'GetStep2' , ), 1610678285, (1610678285, (), [ ], 1 , 1 , 4 , 0 , 128 , (5, 0, None, None) , 0 , )),
	(( 'SetStep2' , 'step' , ), 1610678286, (1610678286, (), [ (5, 0, None, None) , ], 1 , 1 , 4 , 0 , 136 , (3, 0, None, None) , 0 , )),
	(( 'GetAxis1' , ), 1610678287, (1610678287, (), [ ], 1 , 1 , 4 , 0 , 144 , (13, 0, None, IID('{7AA0E540-0301-11D4-A30E-00C026EE094F}')) , 0 , )),
	(( 'SetAxis1' , 'axis' , ), 1610678288, (1610678288, (), [ (13, 0, None, "IID('{7AA0E540-0301-11D4-A30E-00C026EE094F}')") , ], 1 , 1 , 4 , 0 , 152 , (3, 0, None, None) , 0 , )),
	(( 'GetAxis2' , ), 1610678289, (1610678289, (), [ ], 1 , 1 , 4 , 0 , 160 , (13, 0, None, IID('{7AA0E540-0301-11D4-A30E-00C026EE094F}')) , 0 , )),
	(( 'SetAxis2' , 'axis' , ), 1610678290, (1610678290, (), [ (13, 0, None, "IID('{7AA0E540-0301-11D4-A30E-00C026EE094F}')") , ], 1 , 1 , 4 , 0 , 168 , (3, 0, None, None) , 0 , )),
	(( 'GetFactor2' , ), 1610678291, (1610678291, (), [ ], 1 , 1 , 4 , 0 , 176 , (3, 0, None, None) , 0 , )),
	(( 'SetFactor2' , 'factor' , ), 1610678292, (1610678292, (), [ (3, 0, None, None) , ], 1 , 1 , 4 , 0 , 184 , (3, 0, None, None) , 0 , )),
	(( 'GetInsideFlag' , ), 1610678293, (1610678293, (), [ ], 1 , 1 , 4 , 0 , 192 , (3, 0, None, None) , 0 , )),
	(( 'SetInsideFlag' , 'flag' , ), 1610678294, (1610678294, (), [ (3, 0, None, None) , ], 1 , 1 , 4 , 0 , 200 , (3, 0, None, None) , 0 , )),
	(( 'GetCopyParamAlongAxis' , 'firstAxis' , 'angle' , 'count' , 'step' , 
			 'factor' , ), 1610678295, (1610678295, (), [ (3, 0, None, None) , (16389, 0, None, None) , (16387, 0, None, None) , 
			 (16389, 0, None, None) , (16387, 0, None, None) , ], 1 , 1 , 4 , 0 , 208 , (3, 0, None, None) , 0 , )),
	(( 'SetCopyParamAlongAxis' , 'firstAxis' , 'angle' , 'count' , 'step' , 
			 'factor' , ), 1610678296, (1610678296, (), [ (3, 0, None, None) , (5, 0, None, None) , (3, 0, None, None) , 
			 (5, 0, None, None) , (3, 0, None, None) , ], 1 , 1 , 4 , 0 , 216 , (3, 0, None, None) , 0 , )),
	(( 'DeletedCollection' , ), 1610678297, (1610678297, (), [ ], 1 , 1 , 4 , 0 , 224 , (13, 0, None, IID('{BEC3920D-6238-401A-86A3-A600570F47A4}')) , 0 , )),
]

IMirrorAllDefinition_vtables_dispatch_ = 0
IMirrorAllDefinition_vtables_ = [
	(( 'GetPlane' , ), 1610678272, (1610678272, (), [ ], 1 , 1 , 4 , 0 , 24 , (13, 0, None, IID('{7AA0E540-0301-11D4-A30E-00C026EE094F}')) , 0 , )),
	(( 'SetPlane' , 'plane' , ), 1610678273, (1610678273, (), [ (13, 0, None, "IID('{7AA0E540-0301-11D4-A30E-00C026EE094F}')") , ], 1 , 1 , 4 , 0 , 32 , (3, 0, None, None) , 0 , )),
	(( 'ChooseBodies' , ), 1610678274, (1610678274, (), [ ], 1 , 1 , 4 , 0 , 40 , (13, 0, None, IID('{67B417BA-F248-4B56-AD03-C4057C7F2EEE}')) , 0 , )),
]

IMirrorDefinition_vtables_dispatch_ = 0
IMirrorDefinition_vtables_ = [
	(( 'GetOperationArray' , ), 1610678272, (1610678272, (), [ ], 1 , 1 , 4 , 0 , 24 , (13, 0, None, IID('{7AA0E540-0303-11D4-A30E-00C026EE094F}')) , 0 , )),
	(( 'GetPlane' , ), 1610678273, (1610678273, (), [ ], 1 , 1 , 4 , 0 , 32 , (13, 0, None, IID('{7AA0E540-0301-11D4-A30E-00C026EE094F}')) , 0 , )),
	(( 'SetPlane' , 'plane' , ), 1610678274, (1610678274, (), [ (13, 0, None, "IID('{7AA0E540-0301-11D4-A30E-00C026EE094F}')") , ], 1 , 1 , 4 , 0 , 40 , (3, 0, None, None) , 0 , )),
]

IModelLibrary_vtables_dispatch_ = 0
IModelLibrary_vtables_ = [
	(( 'ModelLibraryOperation' , 'libName' , 'type' , ), 1610678272, (1610678272, (), [ (31, 0, None, None) , 
			 (3, 0, None, None) , ], 1 , 1 , 4 , 0 , 24 , (3, 0, None, None) , 0 , )),
	(( 'ChoiceModelFromLib' , 'libFile' , 'type' , ), 1610678273, (1610678273, (), [ (31, 0, None, None) , 
			 (16387, 0, None, None) , ], 1 , 1 , 4 , 0 , 32 , (31, 0, None, None) , 0 , )),
	(( 'AddD3DocumentToLibrary' , 'libName' , 'fileName' , ), 1610678274, (1610678274, (), [ (31, 0, None, None) , 
			 (31, 0, None, None) , ], 1 , 1 , 4 , 0 , 40 , (3, 0, None, None) , 0 , )),
	(( 'CheckModelLibrary' , 'libName' , 'possibleMessage' , ), 1610678275, (1610678275, (), [ (31, 0, None, None) , 
			 (3, 0, None, None) , ], 1 , 1 , 4 , 0 , 48 , (3, 0, None, None) , 0 , )),
	(( 'ExistModelInLibrary' , 'name' , ), 1610678276, (1610678276, (), [ (31, 0, None, None) , ], 1 , 1 , 4 , 0 , 56 , (3, 0, None, None) , 0 , )),
]

IMoldCavityDefinition_vtables_dispatch_ = 0
IMoldCavityDefinition_vtables_ = [
	(( 'GetScale' , ), 1610678272, (1610678272, (), [ ], 1 , 1 , 4 , 0 , 24 , (5, 0, None, None) , 0 , )),
	(( 'SetScale' , 'val' , ), 1610678273, (1610678273, (), [ (5, 0, None, None) , ], 1 , 1 , 4 , 0 , 32 , (3, 0, None, None) , 0 , )),
	(( 'PartArray' , ), 1610678274, (1610678274, (), [ ], 1 , 1 , 4 , 0 , 40 , (13, 0, None, IID('{7AA0E540-0317-11D4-A30E-00C026EE094F}')) , 0 , )),
	(( 'GetScaleCentre' , ), 1610678275, (1610678275, (), [ ], 1 , 1 , 4 , 0 , 48 , (13, 0, None, IID('{7AA0E540-0301-11D4-A30E-00C026EE094F}')) , 0 , )),
	(( 'SetScaleCentre' , 'vert' , ), 1610678276, (1610678276, (), [ (13, 0, None, "IID('{7AA0E540-0301-11D4-A30E-00C026EE094F}')") , ], 1 , 1 , 4 , 0 , 56 , (3, 0, None, None) , 0 , )),
]

INurbs3dParam_vtables_dispatch_ = 0
INurbs3dParam_vtables_ = [
	(( 'GetDegree' , ), 1610678272, (1610678272, (), [ ], 1 , 1 , 4 , 0 , 24 , (2, 0, None, None) , 0 , )),
	(( 'GetClose' , ), 1610678273, (1610678273, (), [ ], 1 , 1 , 4 , 0 , 32 , (3, 0, None, None) , 0 , )),
	(( 'GetPeriodic' , ), 1610678274, (1610678274, (), [ ], 1 , 1 , 4 , 0 , 40 , (3, 0, None, None) , 0 , )),
	(( 'GetPointCollection' , ), 1610678275, (1610678275, (), [ ], 1 , 1 , 4 , 0 , 48 , (13, 0, None, IID('{AC0E0F4D-ACCE-40C4-9B7C-14DAAF224F48}')) , 0 , )),
	(( 'GetKnotCollection' , ), 1610678276, (1610678276, (), [ ], 1 , 1 , 4 , 0 , 56 , (13, 0, None, IID('{1F21432C-E5BA-404D-B18F-007A0D85CCD0}')) , 0 , )),
	(( 'GetNurbsPoints3DParams' , 'closed' , 'points' , 'weights' , 'knots' , 
			 ), 1610678277, (1610678277, (), [ (3, 1, None, None) , (16396, 1, None, None) , (16396, 1, None, None) , (16396, 1, None, None) , ], 1 , 1 , 4 , 0 , 64 , (3, 0, None, None) , 0 , )),
	(( 'GetMinMaxParameters' , 'closed' , 'tMin' , 'tMax' , ), 1610678278, (1610678278, (), [ 
			 (3, 1, None, None) , (16389, 2, None, None) , (16389, 2, None, None) , ], 1 , 1 , 4 , 0 , 72 , (3, 0, None, None) , 0 , )),
]

INurbsKnotCollection_vtables_dispatch_ = 0
INurbsKnotCollection_vtables_ = [
	(( 'Refresh' , ), 1610678272, (1610678272, (), [ ], 1 , 1 , 4 , 0 , 24 , (3, 0, None, None) , 0 , )),
	(( 'GetCount' , ), 1610678273, (1610678273, (), [ ], 1 , 1 , 4 , 0 , 32 , (3, 0, None, None) , 0 , )),
	(( 'First' , ), 1610678274, (1610678274, (), [ ], 1 , 1 , 4 , 0 , 40 , (5, 0, None, None) , 0 , )),
	(( 'Last' , ), 1610678275, (1610678275, (), [ ], 1 , 1 , 4 , 0 , 48 , (5, 0, None, None) , 0 , )),
	(( 'Next' , ), 1610678276, (1610678276, (), [ ], 1 , 1 , 4 , 0 , 56 , (5, 0, None, None) , 0 , )),
	(( 'Prev' , ), 1610678277, (1610678277, (), [ ], 1 , 1 , 4 , 0 , 64 , (5, 0, None, None) , 0 , )),
	(( 'GetByIndex' , 'index' , ), 1610678278, (1610678278, (), [ (3, 0, None, None) , ], 1 , 1 , 4 , 0 , 72 , (5, 0, None, None) , 0 , )),
	(( 'Clear' , ), 1610678279, (1610678279, (), [ ], 1 , 1 , 4 , 0 , 80 , (3, 0, None, None) , 0 , )),
	(( 'Add' , 'entity' , ), 1610678280, (1610678280, (), [ (5, 0, None, None) , ], 1 , 1 , 4 , 0 , 88 , (3, 0, None, None) , 0 , )),
	(( 'AddAt' , 'entity' , 'index' , ), 1610678281, (1610678281, (), [ (5, 0, None, None) , 
			 (3, 0, None, None) , ], 1 , 1 , 4 , 0 , 96 , (3, 0, None, None) , 0 , )),
	(( 'AddBefore' , 'entity' , 'base' , ), 1610678282, (1610678282, (), [ (5, 0, None, None) , 
			 (5, 0, None, None) , ], 1 , 1 , 4 , 0 , 104 , (3, 0, None, None) , 0 , )),
	(( 'DetachByIndex' , 'index' , ), 1610678283, (1610678283, (), [ (3, 0, None, None) , ], 1 , 1 , 4 , 0 , 112 , (3, 0, None, None) , 0 , )),
	(( 'DetachByBody' , 'entity' , ), 1610678284, (1610678284, (), [ (5, 0, None, None) , ], 1 , 1 , 4 , 0 , 120 , (3, 0, None, None) , 0 , )),
	(( 'SetByIndex' , 'entity' , 'index' , ), 1610678285, (1610678285, (), [ (5, 0, None, None) , 
			 (3, 0, None, None) , ], 1 , 1 , 4 , 0 , 128 , (3, 0, None, None) , 0 , )),
]

INurbsPoint3dCollCollection_vtables_dispatch_ = 0
INurbsPoint3dCollCollection_vtables_ = [
	(( 'Refresh' , ), 1610678272, (1610678272, (), [ ], 1 , 1 , 4 , 0 , 24 , (3, 0, None, None) , 0 , )),
	(( 'GetCount' , ), 1610678273, (1610678273, (), [ ], 1 , 1 , 4 , 0 , 32 , (3, 0, None, None) , 0 , )),
	(( 'First' , ), 1610678274, (1610678274, (), [ ], 1 , 1 , 4 , 0 , 40 , (13, 0, None, IID('{AC0E0F4D-ACCE-40C4-9B7C-14DAAF224F48}')) , 0 , )),
	(( 'Last' , ), 1610678275, (1610678275, (), [ ], 1 , 1 , 4 , 0 , 48 , (13, 0, None, IID('{AC0E0F4D-ACCE-40C4-9B7C-14DAAF224F48}')) , 0 , )),
	(( 'Next' , ), 1610678276, (1610678276, (), [ ], 1 , 1 , 4 , 0 , 56 , (13, 0, None, IID('{AC0E0F4D-ACCE-40C4-9B7C-14DAAF224F48}')) , 0 , )),
	(( 'Prev' , ), 1610678277, (1610678277, (), [ ], 1 , 1 , 4 , 0 , 64 , (13, 0, None, IID('{AC0E0F4D-ACCE-40C4-9B7C-14DAAF224F48}')) , 0 , )),
	(( 'GetByIndex' , 'index' , ), 1610678278, (1610678278, (), [ (3, 0, None, None) , ], 1 , 1 , 4 , 0 , 72 , (13, 0, None, IID('{AC0E0F4D-ACCE-40C4-9B7C-14DAAF224F48}')) , 0 , )),
	(( 'Clear' , ), 1610678279, (1610678279, (), [ ], 1 , 1 , 4 , 0 , 80 , (3, 0, None, None) , 0 , )),
	(( 'Add' , 'entity' , ), 1610678280, (1610678280, (), [ (13, 0, None, "IID('{AC0E0F4D-ACCE-40C4-9B7C-14DAAF224F48}')") , ], 1 , 1 , 4 , 0 , 88 , (3, 0, None, None) , 0 , )),
	(( 'AddAt' , 'entity' , 'index' , ), 1610678281, (1610678281, (), [ (13, 0, None, "IID('{AC0E0F4D-ACCE-40C4-9B7C-14DAAF224F48}')") , 
			 (3, 0, None, None) , ], 1 , 1 , 4 , 0 , 96 , (3, 0, None, None) , 0 , )),
	(( 'AddBefore' , 'entity' , 'base' , ), 1610678282, (1610678282, (), [ (13, 0, None, "IID('{AC0E0F4D-ACCE-40C4-9B7C-14DAAF224F48}')") , 
			 (13, 0, None, "IID('{AC0E0F4D-ACCE-40C4-9B7C-14DAAF224F48}')") , ], 1 , 1 , 4 , 0 , 104 , (3, 0, None, None) , 0 , )),
	(( 'DetachByIndex' , 'index' , ), 1610678283, (1610678283, (), [ (3, 0, None, None) , ], 1 , 1 , 4 , 0 , 112 , (3, 0, None, None) , 0 , )),
	(( 'DetachByBody' , 'entity' , ), 1610678284, (1610678284, (), [ (13, 0, None, "IID('{AC0E0F4D-ACCE-40C4-9B7C-14DAAF224F48}')") , ], 1 , 1 , 4 , 0 , 120 , (3, 0, None, None) , 0 , )),
	(( 'SetByIndex' , 'entity' , 'index' , ), 1610678285, (1610678285, (), [ (13, 0, None, "IID('{AC0E0F4D-ACCE-40C4-9B7C-14DAAF224F48}')") , 
			 (3, 0, None, None) , ], 1 , 1 , 4 , 0 , 128 , (3, 0, None, None) , 0 , )),
	(( 'FindIt' , 'entity' , ), 1610678286, (1610678286, (), [ (13, 0, None, "IID('{AC0E0F4D-ACCE-40C4-9B7C-14DAAF224F48}')") , ], 1 , 1 , 4 , 0 , 136 , (19, 0, None, None) , 0 , )),
]

INurbsPoint3dCollection_vtables_dispatch_ = 0
INurbsPoint3dCollection_vtables_ = [
	(( 'Refresh' , ), 1610678272, (1610678272, (), [ ], 1 , 1 , 4 , 0 , 24 , (3, 0, None, None) , 0 , )),
	(( 'GetCount' , ), 1610678273, (1610678273, (), [ ], 1 , 1 , 4 , 0 , 32 , (3, 0, None, None) , 0 , )),
	(( 'First' , ), 1610678274, (1610678274, (), [ ], 1 , 1 , 4 , 0 , 40 , (13, 0, None, IID('{47CDB649-C027-4E8D-8E25-1461CC6D7C12}')) , 0 , )),
	(( 'Last' , ), 1610678275, (1610678275, (), [ ], 1 , 1 , 4 , 0 , 48 , (13, 0, None, IID('{47CDB649-C027-4E8D-8E25-1461CC6D7C12}')) , 0 , )),
	(( 'Next' , ), 1610678276, (1610678276, (), [ ], 1 , 1 , 4 , 0 , 56 , (13, 0, None, IID('{47CDB649-C027-4E8D-8E25-1461CC6D7C12}')) , 0 , )),
	(( 'Prev' , ), 1610678277, (1610678277, (), [ ], 1 , 1 , 4 , 0 , 64 , (13, 0, None, IID('{47CDB649-C027-4E8D-8E25-1461CC6D7C12}')) , 0 , )),
	(( 'GetByIndex' , 'index' , ), 1610678278, (1610678278, (), [ (3, 0, None, None) , ], 1 , 1 , 4 , 0 , 72 , (13, 0, None, IID('{47CDB649-C027-4E8D-8E25-1461CC6D7C12}')) , 0 , )),
	(( 'Clear' , ), 1610678279, (1610678279, (), [ ], 1 , 1 , 4 , 0 , 80 , (3, 0, None, None) , 0 , )),
	(( 'Add' , 'entity' , ), 1610678280, (1610678280, (), [ (13, 0, None, "IID('{47CDB649-C027-4E8D-8E25-1461CC6D7C12}')") , ], 1 , 1 , 4 , 0 , 88 , (3, 0, None, None) , 0 , )),
	(( 'AddAt' , 'entity' , 'index' , ), 1610678281, (1610678281, (), [ (13, 0, None, "IID('{47CDB649-C027-4E8D-8E25-1461CC6D7C12}')") , 
			 (3, 0, None, None) , ], 1 , 1 , 4 , 0 , 96 , (3, 0, None, None) , 0 , )),
	(( 'AddBefore' , 'entity' , 'base' , ), 1610678282, (1610678282, (), [ (13, 0, None, "IID('{47CDB649-C027-4E8D-8E25-1461CC6D7C12}')") , 
			 (13, 0, None, "IID('{47CDB649-C027-4E8D-8E25-1461CC6D7C12}')") , ], 1 , 1 , 4 , 0 , 104 , (3, 0, None, None) , 0 , )),
	(( 'DetachByIndex' , 'index' , ), 1610678283, (1610678283, (), [ (3, 0, None, None) , ], 1 , 1 , 4 , 0 , 112 , (3, 0, None, None) , 0 , )),
	(( 'DetachByBody' , 'entity' , ), 1610678284, (1610678284, (), [ (13, 0, None, "IID('{47CDB649-C027-4E8D-8E25-1461CC6D7C12}')") , ], 1 , 1 , 4 , 0 , 120 , (3, 0, None, None) , 0 , )),
	(( 'SetByIndex' , 'entity' , 'index' , ), 1610678285, (1610678285, (), [ (13, 0, None, "IID('{47CDB649-C027-4E8D-8E25-1461CC6D7C12}')") , 
			 (3, 0, None, None) , ], 1 , 1 , 4 , 0 , 128 , (3, 0, None, None) , 0 , )),
	(( 'FindIt' , 'entity' , ), 1610678286, (1610678286, (), [ (13, 0, None, "IID('{47CDB649-C027-4E8D-8E25-1461CC6D7C12}')") , ], 1 , 1 , 4 , 0 , 136 , (19, 0, None, None) , 0 , )),
]

INurbsPoint3dParam_vtables_dispatch_ = 0
INurbsPoint3dParam_vtables_ = [
	(( 'GetPoint' , 'x' , 'y' , 'z' , ), 1610678272, (1610678272, (), [ 
			 (16389, 2, None, None) , (16389, 2, None, None) , (16389, 2, None, None) , ], 1 , 1 , 4 , 0 , 24 , (3, 0, None, None) , 0 , )),
	(( 'GetWeight' , ), 1610678273, (1610678273, (), [ ], 1 , 1 , 4 , 0 , 32 , (5, 0, None, None) , 0 , )),
]

INurbsSurfaceParam_vtables_dispatch_ = 0
INurbsSurfaceParam_vtables_ = [
	(( 'GetDegree' , 'paramU' , ), 1610678272, (1610678272, (), [ (3, 0, None, None) , ], 1 , 1 , 4 , 0 , 24 , (2, 0, None, None) , 0 , )),
	(( 'GetClose' , 'paramU' , ), 1610678273, (1610678273, (), [ (3, 0, None, None) , ], 1 , 1 , 4 , 0 , 32 , (3, 0, None, None) , 0 , )),
	(( 'GetPeriodic' , 'paramU' , ), 1610678274, (1610678274, (), [ (3, 0, None, None) , ], 1 , 1 , 4 , 0 , 40 , (3, 0, None, None) , 0 , )),
	(( 'GetPointCollection' , ), 1610678275, (1610678275, (), [ ], 1 , 1 , 4 , 0 , 48 , (13, 0, None, IID('{EFEECE8A-4BB9-4D51-B6A4-AC1BEDA73568}')) , 0 , )),
	(( 'GetKnotCollection' , 'paramU' , ), 1610678276, (1610678276, (), [ (3, 0, None, None) , ], 1 , 1 , 4 , 0 , 56 , (13, 0, None, IID('{1F21432C-E5BA-404D-B18F-007A0D85CCD0}')) , 0 , )),
	(( 'GetNurbsParams' , 'closedV' , 'closedU' , 'degreeV' , 'degreeU' , 
			 'nPV' , 'nPU' , 'points' , 'weights' , 'knotsV' , 
			 'knotsU' , ), 1610678277, (1610678277, (), [ (3, 1, None, None) , (3, 1, None, None) , (16387, 2, None, None) , 
			 (16387, 2, None, None) , (16387, 2, None, None) , (16387, 2, None, None) , (16396, 2, None, None) , (16396, 2, None, None) , 
			 (16396, 2, None, None) , (16396, 2, None, None) , ], 1 , 1 , 4 , 0 , 64 , (3, 0, None, None) , 0 , )),
	(( 'GetBoundaryUVNurbs' , 'uv' , 'closed' , 'loopIndex' , 'edgeIndex' , 
			 'degree' , 'points' , 'weights' , 'knots' , 'tMin' , 
			 'tMax' , ), 1610678278, (1610678278, (), [ (3, 1, None, None) , (3, 1, None, None) , (3, 1, None, None) , 
			 (3, 1, None, None) , (16387, 2, None, None) , (16396, 2, None, None) , (16396, 2, None, None) , (16396, 2, None, None) , 
			 (16389, 2, None, None) , (16389, 2, None, None) , ], 1 , 1 , 4 , 0 , 72 , (3, 0, None, None) , 0 , )),
	(( 'GetBoundaryCount' , ), 1610678279, (1610678279, (), [ ], 1 , 1 , 4 , 0 , 80 , (3, 0, None, None) , 0 , )),
	(( 'GetEdgesCount' , 'loopIndex' , ), 1610678280, (1610678280, (), [ (3, 0, None, None) , ], 1 , 1 , 4 , 0 , 88 , (3, 0, None, None) , 0 , )),
	(( 'GetMinMaxParameters' , 'closedV' , 'closedU' , 'uMin' , 'uMax' , 
			 'vMin' , 'vMax' , ), 1610678281, (1610678281, (), [ (3, 1, None, None) , (3, 1, None, None) , 
			 (16389, 2, None, None) , (16389, 2, None, None) , (16389, 2, None, None) , (16389, 2, None, None) , ], 1 , 1 , 4 , 0 , 96 , (3, 0, None, None) , 0 , )),
	(( 'GetUVPointFromBoundaryParameter' , 'uv' , 'closed' , 'loopIndex' , 'edgeIndex' , 
			 't' , 'u' , 'v' , ), 1610678282, (1610678282, (), [ (3, 1, None, None) , 
			 (3, 1, None, None) , (3, 1, None, None) , (3, 1, None, None) , (5, 1, None, None) , (16389, 2, None, None) , 
			 (16389, 2, None, None) , ], 1 , 1 , 4 , 0 , 104 , (3, 0, None, None) , 0 , )),
	(( 'GetBoundaryParameterFromUVPoint' , 'uv' , 'closed' , 'loopIndex' , 'edgeIndex' , 
			 'u' , 'v' , 't' , ), 1610678283, (1610678283, (), [ (3, 1, None, None) , 
			 (3, 1, None, None) , (3, 1, None, None) , (3, 1, None, None) , (5, 1, None, None) , (5, 1, None, None) , 
			 (16389, 2, None, None) , ], 1 , 1 , 4 , 0 , 112 , (3, 0, None, None) , 0 , )),
]

IObject3DNotify_vtables_dispatch_ = 0
IObject3DNotify_vtables_ = [
	(( 'BeginDelete' , 'obj' , ), 1610743808, (1610743808, (), [ (13, 0, None, None) , ], 1 , 1 , 4 , 0 , 32 , (11, 0, None, None) , 0 , )),
	(( 'Delete' , 'obj' , ), 1610743809, (1610743809, (), [ (13, 0, None, None) , ], 1 , 1 , 4 , 0 , 40 , (11, 0, None, None) , 0 , )),
	(( 'Excluded' , 'obj' , 'exclude' , ), 1610743810, (1610743810, (), [ (13, 0, None, None) , 
			 (11, 0, None, None) , ], 1 , 1 , 4 , 0 , 48 , (11, 0, None, None) , 0 , )),
	(( 'Hidden' , 'obj' , '_hidden' , ), 1610743811, (1610743811, (), [ (13, 0, None, None) , 
			 (11, 0, None, None) , ], 1 , 1 , 4 , 0 , 56 , (11, 0, None, None) , 0 , )),
	(( 'BeginPropertyChanged' , 'obj' , ), 1610743812, (1610743812, (), [ (13, 0, None, None) , ], 1 , 1 , 4 , 0 , 64 , (11, 0, None, None) , 0 , )),
	(( 'PropertyChanged' , 'obj' , ), 1610743813, (1610743813, (), [ (13, 0, None, None) , ], 1 , 1 , 4 , 0 , 72 , (11, 0, None, None) , 0 , )),
	(( 'BeginPlacementChanged' , 'obj' , ), 1610743814, (1610743814, (), [ (13, 0, None, None) , ], 1 , 1 , 4 , 0 , 80 , (11, 0, None, None) , 0 , )),
	(( 'PlacementChanged' , 'obj' , ), 1610743815, (1610743815, (), [ (13, 0, None, None) , ], 1 , 1 , 4 , 0 , 88 , (11, 0, None, None) , 0 , )),
	(( 'BeginProcess' , 'pType' , 'obj' , ), 1610743816, (1610743816, (), [ (3, 0, None, None) , 
			 (13, 0, None, None) , ], 1 , 1 , 4 , 0 , 96 , (11, 0, None, None) , 0 , )),
	(( 'EndProcess' , 'pType' , ), 1610743817, (1610743817, (), [ (3, 0, None, None) , ], 1 , 1 , 4 , 0 , 104 , (11, 0, None, None) , 0 , )),
	(( 'CreateObject' , 'obj' , ), 1610743818, (1610743818, (), [ (13, 0, None, None) , ], 1 , 1 , 4 , 0 , 112 , (11, 0, None, None) , 0 , )),
	(( 'UpdateObject' , 'obj' , ), 1610743819, (1610743819, (), [ (13, 0, None, None) , ], 1 , 1 , 4 , 0 , 120 , (11, 0, None, None) , 0 , )),
	(( 'BeginLoadStateChange' , 'obj' , 'loadState' , ), 1610743820, (1610743820, (), [ (13, 0, None, None) , 
			 (3, 0, None, None) , ], 1 , 1 , 4 , 0 , 128 , (11, 0, None, None) , 0 , )),
	(( 'LoadStateChange' , 'obj' , 'loadState' , ), 1610743821, (1610743821, (), [ (13, 0, None, None) , 
			 (3, 0, None, None) , ], 1 , 1 , 4 , 0 , 136 , (11, 0, None, None) , 0 , )),
]

IObject3DNotifyResult_vtables_dispatch_ = 0
IObject3DNotifyResult_vtables_ = [
	(( 'GetNotifyType' , ), 1610678272, (1610678272, (), [ ], 1 , 1 , 4 , 0 , 24 , (3, 0, None, None) , 0 , )),
	(( 'GetFeatureCollection' , ), 1610678273, (1610678273, (), [ ], 1 , 1 , 4 , 0 , 32 , (13, 0, None, None) , 0 , )),
	(( 'GetPlacement' , ), 1610678274, (1610678274, (), [ ], 1 , 1 , 4 , 0 , 40 , (13, 0, None, None) , 0 , )),
	(( 'GetProcessType' , ), 1610678275, (1610678275, (), [ ], 1 , 1 , 4 , 0 , 48 , (3, 0, None, None) , 0 , )),
	(( 'IsUndoMode' , ), 1610678276, (1610678276, (), [ ], 1 , 1 , 4 , 0 , 56 , (3, 0, None, None) , 0 , )),
	(( 'IsRedoMode' , ), 1610678277, (1610678277, (), [ ], 1 , 1 , 4 , 0 , 64 , (3, 0, None, None) , 0 , )),
]

IObjectsFilter3D_vtables_dispatch_ = 0
IObjectsFilter3D_vtables_ = [
	(( 'GetFilterAll' , ), 1610678272, (1610678272, (), [ ], 1 , 1 , 4 , 0 , 24 , (3, 0, None, None) , 0 , )),
	(( 'SetFilterAll' , 'all' , ), 1610678273, (1610678273, (), [ (3, 0, None, None) , ], 1 , 1 , 4 , 0 , 32 , (24, 0, None, None) , 0 , )),
	(( 'GetFilterFaces' , ), 1610678274, (1610678274, (), [ ], 1 , 1 , 4 , 0 , 40 , (3, 0, None, None) , 0 , )),
	(( 'SetFilterFaces' , 'value' , ), 1610678275, (1610678275, (), [ (3, 0, None, None) , ], 1 , 1 , 4 , 0 , 48 , (24, 0, None, None) , 0 , )),
	(( 'GetFilterEdges' , ), 1610678276, (1610678276, (), [ ], 1 , 1 , 4 , 0 , 56 , (3, 0, None, None) , 0 , )),
	(( 'SetFilterEdges' , 'value' , ), 1610678277, (1610678277, (), [ (3, 0, None, None) , ], 1 , 1 , 4 , 0 , 64 , (24, 0, None, None) , 0 , )),
	(( 'GetFilterVertexs' , ), 1610678278, (1610678278, (), [ ], 1 , 1 , 4 , 0 , 72 , (3, 0, None, None) , 0 , )),
	(( 'SetFilterVertexs' , 'value' , ), 1610678279, (1610678279, (), [ (3, 0, None, None) , ], 1 , 1 , 4 , 0 , 80 , (24, 0, None, None) , 0 , )),
	(( 'GetFilterCPlanes' , ), 1610678280, (1610678280, (), [ ], 1 , 1 , 4 , 0 , 88 , (3, 0, None, None) , 0 , )),
	(( 'SetFilterCPlanes' , 'value' , ), 1610678281, (1610678281, (), [ (3, 0, None, None) , ], 1 , 1 , 4 , 0 , 96 , (24, 0, None, None) , 0 , )),
	(( 'GetFilterCAxis' , ), 1610678282, (1610678282, (), [ ], 1 , 1 , 4 , 0 , 104 , (3, 0, None, None) , 0 , )),
	(( 'SetFilterCAxis' , 'value' , ), 1610678283, (1610678283, (), [ (3, 0, None, None) , ], 1 , 1 , 4 , 0 , 112 , (24, 0, None, None) , 0 , )),
]

IOrientedEdge_vtables_dispatch_ = 0
IOrientedEdge_vtables_ = [
	(( 'GetEdge' , ), 1610678272, (1610678272, (), [ ], 1 , 1 , 4 , 0 , 24 , (13, 0, None, IID('{7AA0E540-0321-11D4-A30E-00C026EE094F}')) , 0 , )),
	(( 'GetOrientation' , ), 1610678273, (1610678273, (), [ ], 1 , 1 , 4 , 0 , 32 , (3, 0, None, None) , 0 , )),
	(( 'GetOwnerEntity' , ), 1610678274, (1610678274, (), [ ], 1 , 1 , 4 , 0 , 40 , (13, 0, None, IID('{7AA0E540-0301-11D4-A30E-00C026EE094F}')) , 0 , )),
	(( 'GetNext' , ), 1610678275, (1610678275, (), [ ], 1 , 1 , 4 , 0 , 48 , (13, 0, None, IID('{42AA4E40-4415-4C79-8B8C-480E5AFDB79A}')) , 0 , )),
	(( 'GetSameSense' , ), 1610678276, (1610678276, (), [ ], 1 , 1 , 4 , 0 , 56 , (3, 0, None, None) , 0 , )),
	(( 'GetAdjacentFace' , 'facePlus' , ), 1610678277, (1610678277, (), [ (3, 0, None, None) , ], 1 , 1 , 4 , 0 , 64 , (13, 0, None, IID('{7AA0E540-0322-11D4-A30E-00C026EE094F}')) , 0 , )),
	(( 'IsStraight' , ), 1610678278, (1610678278, (), [ ], 1 , 1 , 4 , 0 , 72 , (3, 0, None, None) , 0 , )),
	(( 'IsSeam' , ), 1610678279, (1610678279, (), [ ], 1 , 1 , 4 , 0 , 80 , (3, 0, None, None) , 0 , )),
	(( 'IsPole' , ), 1610678280, (1610678280, (), [ ], 1 , 1 , 4 , 0 , 88 , (3, 0, None, None) , 0 , )),
]

IOrientedEdgeCollection_vtables_dispatch_ = 0
IOrientedEdgeCollection_vtables_ = [
	(( 'Refresh' , ), 1610678272, (1610678272, (), [ ], 1 , 1 , 4 , 0 , 24 , (3, 0, None, None) , 0 , )),
	(( 'GetCount' , ), 1610678273, (1610678273, (), [ ], 1 , 1 , 4 , 0 , 32 , (3, 0, None, None) , 0 , )),
	(( 'First' , ), 1610678274, (1610678274, (), [ ], 1 , 1 , 4 , 0 , 40 , (13, 0, None, IID('{42AA4E40-4415-4C79-8B8C-480E5AFDB79A}')) , 0 , )),
	(( 'Last' , ), 1610678275, (1610678275, (), [ ], 1 , 1 , 4 , 0 , 48 , (13, 0, None, IID('{42AA4E40-4415-4C79-8B8C-480E5AFDB79A}')) , 0 , )),
	(( 'Next' , ), 1610678276, (1610678276, (), [ ], 1 , 1 , 4 , 0 , 56 , (13, 0, None, IID('{42AA4E40-4415-4C79-8B8C-480E5AFDB79A}')) , 0 , )),
	(( 'Prev' , ), 1610678277, (1610678277, (), [ ], 1 , 1 , 4 , 0 , 64 , (13, 0, None, IID('{42AA4E40-4415-4C79-8B8C-480E5AFDB79A}')) , 0 , )),
	(( 'GetByIndex' , 'index' , ), 1610678278, (1610678278, (), [ (3, 0, None, None) , ], 1 , 1 , 4 , 0 , 72 , (13, 0, None, IID('{42AA4E40-4415-4C79-8B8C-480E5AFDB79A}')) , 0 , )),
	(( 'FindIt' , 'entity' , ), 1610678279, (1610678279, (), [ (13, 0, None, "IID('{42AA4E40-4415-4C79-8B8C-480E5AFDB79A}')") , ], 1 , 1 , 4 , 0 , 80 , (19, 0, None, None) , 0 , )),
]

IPart_vtables_dispatch_ = 0
IPart_vtables_ = [
	(( 'GetName' , ), 1610678272, (1610678272, (), [ ], 1 , 1 , 4 , 0 , 24 , (31, 0, None, None) , 0 , )),
	(( 'SetName' , 'name' , ), 1610678273, (1610678273, (), [ (31, 0, None, None) , ], 1 , 1 , 4 , 0 , 32 , (3, 0, None, None) , 0 , )),
	(( 'GetMarking' , ), 1610678274, (1610678274, (), [ ], 1 , 1 , 4 , 0 , 40 , (31, 0, None, None) , 0 , )),
	(( 'SetMarking' , 'marking' , ), 1610678275, (1610678275, (), [ (31, 0, None, None) , ], 1 , 1 , 4 , 0 , 48 , (3, 0, None, None) , 0 , )),
	(( 'ColorParam' , ), 1610678276, (1610678276, (), [ ], 1 , 1 , 4 , 0 , 56 , (13, 0, None, IID('{7AA0E540-0305-11D4-A30E-00C026EE094F}')) , 0 , )),
	(( 'GetAdvancedColor' , 'color' , 'ambient' , 'diffuse' , 'specularity' , 
			 'shininess' , 'transparency' , 'emission' , ), 1610678277, (1610678277, (), [ (16403, 0, None, None) , 
			 (16389, 0, None, None) , (16389, 0, None, None) , (16389, 0, None, None) , (16389, 0, None, None) , (16389, 0, None, None) , 
			 (16389, 0, None, None) , ], 1 , 1 , 4 , 0 , 64 , (3, 0, None, None) , 0 , )),
	(( 'SetAdvancedColor' , 'color' , 'ambient' , 'diffuse' , 'specularity' , 
			 'shininess' , 'transparency' , 'emission' , ), 1610678278, (1610678278, (), [ (19, 0, None, None) , 
			 (5, 0, None, None) , (5, 0, None, None) , (5, 0, None, None) , (5, 0, None, None) , (5, 0, None, None) , 
			 (5, 0, None, None) , ], 1 , 1 , 4 , 0 , 72 , (3, 0, None, None) , 0 , )),
	(( 'Update' , ), 1610678279, (1610678279, (), [ ], 1 , 1 , 4 , 0 , 80 , (3, 0, None, None) , 0 , )),
	(( 'SetUserParam' , 'value' , 'size' , 'fileName' , 'libName' , 
			 'command' , ), 1610678280, (1610678280, (), [ (16408, 0, None, None) , (3, 0, None, None) , (31, 0, None, None) , 
			 (31, 0, None, None) , (3, 0, None, None) , ], 1 , 1 , 4 , 0 , 88 , (3, 0, None, None) , 0 , )),
	(( 'GetUserParamSize' , ), 1610678281, (1610678281, (), [ ], 1 , 1 , 4 , 0 , 96 , (3, 0, None, None) , 0 , )),
	(( 'GetUserParam' , 'value' , 'size' , ), 1610678282, (1610678282, (), [ (16408, 0, None, None) , 
			 (3, 0, None, None) , ], 1 , 1 , 4 , 0 , 104 , (3, 0, None, None) , 0 , )),
	(( 'GetDefaultEntity' , 'objType' , ), 1610678283, (1610678283, (), [ (2, 0, None, None) , ], 1 , 1 , 4 , 0 , 112 , (13, 0, None, IID('{7AA0E540-0301-11D4-A30E-00C026EE094F}')) , 0 , )),
	(( 'EntityCollection' , 'objType' , ), 1610678284, (1610678284, (), [ (2, 0, None, None) , ], 1 , 1 , 4 , 0 , 120 , (13, 0, None, IID('{7AA0E540-0303-11D4-A30E-00C026EE094F}')) , 0 , )),
	(( 'NewEntity' , 'objType' , ), 1610678285, (1610678285, (), [ (2, 0, None, None) , ], 1 , 1 , 4 , 0 , 128 , (13, 0, None, IID('{7AA0E540-0301-11D4-A30E-00C026EE094F}')) , 0 , )),
	(( 'GetPlacement' , ), 1610678286, (1610678286, (), [ ], 1 , 1 , 4 , 0 , 136 , (13, 0, None, IID('{7AA0E540-0310-11D4-A30E-00C026EE094F}')) , 0 , )),
	(( 'SetPlacement' , 'p' , ), 1610678287, (1610678287, (), [ (13, 0, None, "IID('{7AA0E540-0310-11D4-A30E-00C026EE094F}')") , ], 1 , 1 , 4 , 0 , 144 , (3, 0, None, None) , 0 , )),
	(( 'UpdatePlacement' , ), 1610678288, (1610678288, (), [ ], 1 , 1 , 4 , 0 , 152 , (3, 0, None, None) , 0 , )),
	(( 'VariableCollection' , ), 1610678289, (1610678289, (), [ ], 1 , 1 , 4 , 0 , 160 , (13, 0, None, IID('{7AA0E540-0311-11D4-A30E-00C026EE094F}')) , 0 , )),
	(( 'RebuildModel' , ), 1610678290, (1610678290, (), [ ], 1 , 1 , 4 , 0 , 168 , (3, 0, None, None) , 0 , )),
	(( 'GetStandardComponent' , ), 1610678291, (1610678291, (), [ ], 1 , 1 , 4 , 0 , 176 , (3, 0, None, None) , 0 , )),
	(( 'SetStandardComponent' , 'f' , ), 1610678292, (1610678292, (), [ (3, 0, None, None) , ], 1 , 1 , 4 , 0 , 184 , (3, 0, None, None) , 0 , )),
	(( 'SetMateConstraintObjects' , 'collection' , ), 1610678293, (1610678293, (), [ (13, 0, None, "IID('{7AA0E540-0303-11D4-A30E-00C026EE094F}')") , ], 1 , 1 , 4 , 0 , 192 , (3, 0, None, None) , 0 , )),
	(( 'GetMateConstraintObjects' , ), 1610678294, (1610678294, (), [ ], 1 , 1 , 4 , 0 , 200 , (13, 0, None, IID('{7AA0E540-0303-11D4-A30E-00C026EE094F}')) , 0 , )),
	(( 'GetFixedComponent' , ), 1610678295, (1610678295, (), [ ], 1 , 1 , 4 , 0 , 208 , (3, 0, None, None) , 0 , )),
	(( 'SetFixedComponent' , 'f' , ), 1610678296, (1610678296, (), [ (3, 0, None, None) , ], 1 , 1 , 4 , 0 , 216 , (3, 0, None, None) , 0 , )),
	(( 'GetFileName' , ), 1610678297, (1610678297, (), [ ], 1 , 1 , 4 , 0 , 224 , (31, 0, None, None) , 0 , )),
	(( 'SetFileName' , 'name' , ), 1610678298, (1610678298, (), [ (31, 0, None, None) , ], 1 , 1 , 4 , 0 , 232 , (3, 0, None, None) , 0 , )),
	(( 'IsDetail' , ), 1610678299, (1610678299, (), [ ], 1 , 1 , 4 , 0 , 240 , (3, 0, None, None) , 0 , )),
	(( 'BeginEdit' , ), 1610678300, (1610678300, (), [ ], 1 , 1 , 4 , 0 , 248 , (13, 0, None, IID('{7AA0E540-0302-11D4-A30E-00C026EE094F}')) , 0 , )),
	(( 'EndEdit' , 'rebuild_' , ), 1610678301, (1610678301, (), [ (3, 0, None, None) , ], 1 , 1 , 4 , 0 , 256 , (3, 0, None, None) , 0 , )),
	(( 'GetPart' , 'type' , ), 1610678302, (1610678302, (), [ (3, 0, None, None) , ], 1 , 1 , 4 , 0 , 264 , (13, 0, None, IID('{7AA0E540-0300-11D4-A30E-00C026EE094F}')) , 0 , )),
	(( 'GetMass' , ), 1610678303, (1610678303, (), [ ], 1 , 1 , 4 , 0 , 272 , (5, 0, None, None) , 0 , )),
	(( 'PutStorage' , 'str' , 'type' , 'mirror' , ), 1610678304, (1610678304, (), [ 
			 (31, 0, None, None) , (3, 0, None, None) , (3, 0, None, None) , ], 1 , 1 , 4 , 0 , 280 , (3, 0, None, None) , 0 , )),
	(( 'SetExcluded' , 'exclude' , ), 1610678305, (1610678305, (), [ (3, 0, None, None) , ], 1 , 1 , 4 , 0 , 288 , (3, 0, None, None) , 0 , )),
	(( 'GetExcluded' , ), 1610678306, (1610678306, (), [ ], 1 , 1 , 4 , 0 , 296 , (3, 0, None, None) , 0 , )),
	(( 'GetMaterial' , ), 1610678307, (1610678307, (), [ ], 1 , 1 , 4 , 0 , 304 , (31, 0, None, None) , 0 , )),
	(( 'GetDensity' , ), 1610678308, (1610678308, (), [ ], 1 , 1 , 4 , 0 , 312 , (5, 0, None, None) , 0 , )),
	(( 'SetMaterial' , 'name' , 'density' , ), 1610678309, (1610678309, (), [ (31, 0, None, None) , 
			 (5, 0, None, None) , ], 1 , 1 , 4 , 0 , 320 , (3, 0, None, None) , 0 , )),
	(( 'GetUserLibraryFileName' , ), 1610678310, (1610678310, (), [ ], 1 , 1 , 4 , 0 , 328 , (31, 0, None, None) , 0 , )),
	(( 'GetUserLibraryName' , ), 1610678311, (1610678311, (), [ ], 1 , 1 , 4 , 0 , 336 , (31, 0, None, None) , 0 , )),
	(( 'GetUserLibraryCommand' , ), 1610678312, (1610678312, (), [ ], 1 , 1 , 4 , 0 , 344 , (3, 0, None, None) , 0 , )),
	(( 'BodyCollection' , ), 1610678313, (1610678313, (), [ ], 1 , 1 , 4 , 0 , 352 , (13, 0, None, IID('{64CBC7CB-005D-47DF-8B3E-53FD974C5A32}')) , 0 , )),
	(( 'GetFeature' , ), 1610678314, (1610678314, (), [ ], 1 , 1 , 4 , 0 , 360 , (13, 0, None, IID('{1D15245B-695E-4F9F-AFCA-EACBC3A055BB}')) , 0 , )),
	(( 'CalcMassInertiaProperties' , 'bitVector' , ), 1610678315, (1610678315, (), [ (19, 0, None, None) , ], 1 , 1 , 4 , 0 , 368 , (13, 0, None, IID('{74E97440-88A5-4D29-9543-59D775BC9A13}')) , 0 , )),
	(( 'GetMeasurer' , ), 1610678316, (1610678316, (), [ ], 1 , 1 , 4 , 0 , 376 , (13, 0, None, IID('{AC171655-ED3F-4F7A-A625-44083941AF85}')) , 0 , )),
	(( 'GetMainBody' , ), 1610678317, (1610678317, (), [ ], 1 , 1 , 4 , 0 , 384 , (13, 0, None, IID('{BE70EEE5-1767-483E-9D18-79BCEC5AB837}')) , 0 , )),
	(( 'GetUseColor' , ), 1610678318, (1610678318, (), [ ], 1 , 1 , 4 , 0 , 392 , (3, 0, None, None) , 0 , )),
	(( 'SetUseColor' , 'useColor' , ), 1610678319, (1610678319, (), [ (3, 0, None, None) , ], 1 , 1 , 4 , 0 , 400 , (3, 0, None, None) , 0 , )),
	(( 'GetObject3DNotifyResult' , ), 1610678320, (1610678320, (), [ ], 1 , 1 , 4 , 0 , 408 , (13, 0, None, IID('{6B04A0E4-837A-4151-8E5A-836517F39EAE}')) , 0 , )),
	(( 'UpdatePlacementEx' , 'redraw' , ), 1610678321, (1610678321, (), [ (3, 0, None, None) , ], 1 , 1 , 4 , 0 , 416 , (3, 0, None, None) , 0 , )),
	(( 'RebuildModelEx' , 'redraw' , ), 1610678322, (1610678322, (), [ (3, 0, None, None) , ], 1 , 1 , 4 , 0 , 424 , (3, 0, None, None) , 0 , )),
	(( 'GetNeedRebuild' , ), 1610678323, (1610678323, (), [ ], 1 , 1 , 4 , 0 , 432 , (3, 0, None, None) , 0 , )),
	(( 'SetNeedRebuild' , 'val' , ), 1610678324, (1610678324, (), [ (3, 0, None, None) , ], 1 , 1 , 4 , 0 , 440 , (3, 0, None, None) , 0 , )),
	(( 'CurveIntersection' , 'curve' , 'parts' , 'faces' , 'points' , 
			 ), 1610678325, (1610678325, (), [ (13, 0, None, "IID('{E5066490-773D-4289-A60B-2FC19865174A}')") , (13, 0, None, "IID('{7AA0E540-0317-11D4-A30E-00C026EE094F}')") , (13, 0, None, "IID('{D269AD47-B2CC-4152-A7BA-127242371208}')") , (13, 0, None, "IID('{A5E6E83E-1F33-4EAF-BAFC-A3F434F23BAA}')") , ], 1 , 1 , 4 , 0 , 448 , (3, 0, None, None) , 0 , )),
	(( 'TransformPoint' , 'x' , 'y' , 'z' , 'part1' , 
			 ), 1610678326, (1610678326, (), [ (16389, 3, None, None) , (16389, 3, None, None) , (16389, 3, None, None) , (13, 1, None, "IID('{7AA0E540-0300-11D4-A30E-00C026EE094F}')") , ], 1 , 1 , 4 , 0 , 456 , (3, 0, None, None) , 0 , )),
	(( 'GetHidden' , ), 1610678327, (1610678327, (), [ ], 1 , 1 , 4 , 0 , 464 , (3, 0, None, None) , 0 , )),
	(( 'SetHidden' , '_hidden' , ), 1610678328, (1610678328, (), [ (3, 0, None, None) , ], 1 , 1 , 4 , 0 , 472 , (3, 0, None, None) , 0 , )),
	(( 'SetObject' , 'index' , 'obj' , ), 1610678329, (1610678329, (), [ (3, 0, None, None) , 
			 (13, 0, None, None) , ], 1 , 1 , 4 , 0 , 480 , (3, 0, None, None) , 0 , )),
	(( 'GetObject' , 'index' , ), 1610678330, (1610678330, (), [ (3, 0, None, None) , ], 1 , 1 , 4 , 0 , 488 , (13, 0, None, None) , 0 , )),
	(( 'GetCountObj' , ), 1610678331, (1610678331, (), [ ], 1 , 1 , 4 , 0 , 496 , (3, 0, None, None) , 0 , )),
	(( 'ClearAllObj' , ), 1610678332, (1610678332, (), [ ], 1 , 1 , 4 , 0 , 504 , (3, 0, None, None) , 0 , )),
	(( 'CreateOrEditObject' , 'objType' , 'editObj' , ), 1610678333, (1610678333, (), [ (2, 0, None, None) , 
			 (13, 0, None, "IID('{7AA0E540-0301-11D4-A30E-00C026EE094F}')") , ], 1 , 1 , 4 , 0 , 512 , (13, 0, None, IID('{7AA0E540-0301-11D4-A30E-00C026EE094F}')) , 0 , )),
	(( 'GetDoubleClickEditOff' , ), 1610678334, (1610678334, (), [ ], 1 , 1 , 4 , 0 , 520 , (3, 0, None, None) , 0 , )),
	(( 'SetDoubleClickEditOff' , 'val' , ), 1610678335, (1610678335, (), [ (3, 0, None, None) , ], 1 , 1 , 4 , 0 , 528 , (3, 0, None, None) , 0 , )),
	(( 'TransformPoints' , 'poins' , 'part1' , ), 1610678336, (1610678336, (), [ (16396, 3, None, None) , 
			 (13, 0, None, "IID('{7AA0E540-0300-11D4-A30E-00C026EE094F}')") , ], 1 , 1 , 4 , 0 , 536 , (3, 0, None, None) , 0 , )),
	(( 'GetSummMatrix' , 'matrix' , 'part1' , ), 1610678337, (1610678337, (), [ (16396, 0, None, None) , 
			 (13, 0, None, "IID('{7AA0E540-0300-11D4-A30E-00C026EE094F}')") , ], 1 , 1 , 4 , 0 , 544 , (3, 0, None, None) , 0 , )),
	(( 'GetMultiBodyParts' , ), 1610678338, (1610678338, (), [ ], 1 , 1 , 4 , 0 , 552 , (3, 0, None, None) , 0 , )),
	(( 'SetSourceVariables' , 'rebuild_' , ), 1610678339, (1610678339, (), [ (3, 0, None, None) , ], 1 , 1 , 4 , 0 , 560 , (3, 0, None, None) , 0 , )),
	(( 'GetMathematic3D' , 'type' , ), 1610678340, (1610678340, (), [ (3, 0, None, None) , ], 1 , 1 , 4 , 0 , 568 , (13, 0, None, None) , 0 , )),
	(( 'GetGabarit' , 'full' , 'customizable' , 'x1' , 'y1' , 
			 'z1' , 'x2' , 'y2' , 'z2' , ), 1610678341, (1610678341, (), [ 
			 (3, 0, None, None) , (3, 0, None, None) , (16389, 0, None, None) , (16389, 0, None, None) , (16389, 0, None, None) , 
			 (16389, 0, None, None) , (16389, 0, None, None) , (16389, 0, None, None) , ], 1 , 1 , 4 , 0 , 576 , (3, 0, None, None) , 0 , )),
	(( 'GetObjectByName' , 'name' , 'objType' , 'testFullName' , 'testIgnoreCase' , 
			 ), 1610678342, (1610678342, (), [ (31, 0, None, None) , (2, 0, None, None) , (3, 0, None, None) , (3, 0, None, None) , ], 1 , 1 , 4 , 0 , 584 , (13, 0, None, IID('{7AA0E540-0301-11D4-A30E-00C026EE094F}')) , 0 , )),
	(( 'GetPropertyObjectEditable' , ), 1610678343, (1610678343, (), [ ], 1 , 1 , 4 , 0 , 592 , (3, 0, None, None) , 0 , )),
	(( 'SetPropertyObjectEditable' , 'PVal' , ), 1610678344, (1610678344, (), [ (3, 0, None, None) , ], 1 , 1 , 4 , 0 , 600 , (3, 0, None, None) , 0 , )),
]

IPartCollection_vtables_dispatch_ = 0
IPartCollection_vtables_ = [
	(( 'Refresh' , ), 1610678272, (1610678272, (), [ ], 1 , 1 , 4 , 0 , 24 , (3, 0, None, None) , 0 , )),
	(( 'GetCount' , ), 1610678273, (1610678273, (), [ ], 1 , 1 , 4 , 0 , 32 , (3, 0, None, None) , 0 , )),
	(( 'First' , ), 1610678274, (1610678274, (), [ ], 1 , 1 , 4 , 0 , 40 , (13, 0, None, IID('{7AA0E540-0300-11D4-A30E-00C026EE094F}')) , 0 , )),
	(( 'Last' , ), 1610678275, (1610678275, (), [ ], 1 , 1 , 4 , 0 , 48 , (13, 0, None, IID('{7AA0E540-0300-11D4-A30E-00C026EE094F}')) , 0 , )),
	(( 'Next' , ), 1610678276, (1610678276, (), [ ], 1 , 1 , 4 , 0 , 56 , (13, 0, None, IID('{7AA0E540-0300-11D4-A30E-00C026EE094F}')) , 0 , )),
	(( 'Prev' , ), 1610678277, (1610678277, (), [ ], 1 , 1 , 4 , 0 , 64 , (13, 0, None, IID('{7AA0E540-0300-11D4-A30E-00C026EE094F}')) , 0 , )),
	(( 'GetByName' , 'name' , 'testFullName' , 'testIgnoreCase' , ), 1610678278, (1610678278, (), [ 
			 (31, 0, None, None) , (3, 0, None, None) , (3, 0, None, None) , ], 1 , 1 , 4 , 0 , 72 , (13, 0, None, IID('{7AA0E540-0300-11D4-A30E-00C026EE094F}')) , 0 , )),
	(( 'GetByIndex' , 'index' , ), 1610678279, (1610678279, (), [ (3, 0, None, None) , ], 1 , 1 , 4 , 0 , 80 , (13, 0, None, IID('{7AA0E540-0300-11D4-A30E-00C026EE094F}')) , 0 , )),
	(( 'Add' , 'entity' , ), 1610678280, (1610678280, (), [ (13, 0, None, "IID('{7AA0E540-0300-11D4-A30E-00C026EE094F}')") , ], 1 , 1 , 4 , 0 , 88 , (3, 0, None, None) , 0 , )),
	(( 'AddAt' , 'entity' , 'index' , ), 1610678281, (1610678281, (), [ (13, 0, None, "IID('{7AA0E540-0300-11D4-A30E-00C026EE094F}')") , 
			 (3, 0, None, None) , ], 1 , 1 , 4 , 0 , 96 , (3, 0, None, None) , 0 , )),
	(( 'AddBefore' , 'entity' , 'base' , ), 1610678282, (1610678282, (), [ (13, 0, None, "IID('{7AA0E540-0300-11D4-A30E-00C026EE094F}')") , 
			 (13, 0, None, "IID('{7AA0E540-0300-11D4-A30E-00C026EE094F}')") , ], 1 , 1 , 4 , 0 , 104 , (3, 0, None, None) , 0 , )),
	(( 'DetachByIndex' , 'index' , ), 1610678283, (1610678283, (), [ (3, 0, None, None) , ], 1 , 1 , 4 , 0 , 112 , (3, 0, None, None) , 0 , )),
	(( 'DetachByBody' , 'entity' , ), 1610678284, (1610678284, (), [ (13, 0, None, "IID('{7AA0E540-0300-11D4-A30E-00C026EE094F}')") , ], 1 , 1 , 4 , 0 , 120 , (3, 0, None, None) , 0 , )),
	(( 'Clear' , ), 1610678285, (1610678285, (), [ ], 1 , 1 , 4 , 0 , 128 , (3, 0, None, None) , 0 , )),
	(( 'SetByIndex' , 'entity' , 'index' , ), 1610678286, (1610678286, (), [ (13, 0, None, "IID('{7AA0E540-0300-11D4-A30E-00C026EE094F}')") , 
			 (3, 0, None, None) , ], 1 , 1 , 4 , 0 , 136 , (3, 0, None, None) , 0 , )),
	(( 'FindIt' , 'entity' , ), 1610678287, (1610678287, (), [ (13, 0, None, "IID('{7AA0E540-0300-11D4-A30E-00C026EE094F}')") , ], 1 , 1 , 4 , 0 , 144 , (19, 0, None, None) , 0 , )),
]

IPlacement_vtables_dispatch_ = 0
IPlacement_vtables_ = [
	(( 'GetOrigin' , 'x' , 'y' , 'z' , ), 1610678272, (1610678272, (), [ 
			 (16389, 2, None, None) , (16389, 2, None, None) , (16389, 2, None, None) , ], 1 , 1 , 4 , 0 , 24 , (3, 0, None, None) , 0 , )),
	(( 'SetOrigin' , 'x' , 'y' , 'z' , ), 1610678273, (1610678273, (), [ 
			 (5, 0, None, None) , (5, 0, None, None) , (5, 0, None, None) , ], 1 , 1 , 4 , 0 , 32 , (3, 0, None, None) , 0 , )),
	(( 'GetAxis' , 'x' , 'y' , 'z' , 'type' , 
			 ), 1610678274, (1610678274, (), [ (16389, 2, None, None) , (16389, 2, None, None) , (16389, 2, None, None) , (3, 1, None, None) , ], 1 , 1 , 4 , 0 , 40 , (3, 0, None, None) , 0 , )),
	(( 'SetAxis' , 'x' , 'y' , 'z' , 'type' , 
			 ), 1610678275, (1610678275, (), [ (5, 0, None, None) , (5, 0, None, None) , (5, 0, None, None) , (3, 0, None, None) , ], 1 , 1 , 4 , 0 , 48 , (3, 0, None, None) , 0 , )),
	(( 'SetPlacement' , 'p' , ), 1610678276, (1610678276, (), [ (13, 0, None, "IID('{7AA0E540-0310-11D4-A30E-00C026EE094F}')") , ], 1 , 1 , 4 , 0 , 56 , (3, 0, None, None) , 0 , )),
	(( 'SetAxes' , 'Xx' , 'Xy' , 'Xz' , 'Yx' , 
			 'Yy' , 'Yz' , ), 1610678277, (1610678277, (), [ (5, 0, None, None) , (5, 0, None, None) , 
			 (5, 0, None, None) , (5, 0, None, None) , (5, 0, None, None) , (5, 0, None, None) , ], 1 , 1 , 4 , 0 , 64 , (3, 0, None, None) , 0 , )),
	(( 'PointProjection' , 'XIn' , 'YIn' , 'ZIn' , 'XOut' , 
			 'YOut' , ), 1610678278, (1610678278, (), [ (5, 1, None, None) , (5, 1, None, None) , (5, 1, None, None) , 
			 (16389, 2, None, None) , (16389, 2, None, None) , ], 1 , 1 , 4 , 0 , 72 , (3, 0, None, None) , 0 , )),
	(( 'PointOn' , 'XIn' , 'YIn' , 'XOut' , 'YOut' , 
			 'ZOut' , ), 1610678279, (1610678279, (), [ (5, 1, None, None) , (5, 1, None, None) , (16389, 2, None, None) , 
			 (16389, 2, None, None) , (16389, 2, None, None) , ], 1 , 1 , 4 , 0 , 80 , (3, 0, None, None) , 0 , )),
	(( 'GetVector' , 'type' , 'x' , 'y' , 'z' , 
			 ), 1610678280, (1610678280, (), [ (3, 1, None, None) , (16389, 2, None, None) , (16389, 2, None, None) , (16389, 2, None, None) , ], 1 , 1 , 4 , 0 , 88 , (3, 0, None, None) , 0 , )),
	(( 'SetVector' , 'type' , 'x' , 'y' , 'z' , 
			 ), 1610678281, (1610678281, (), [ (3, 0, None, None) , (5, 0, None, None) , (5, 0, None, None) , (5, 0, None, None) , ], 1 , 1 , 4 , 0 , 96 , (3, 0, None, None) , 0 , )),
	(( 'InitByMatrix3D' , 'mtr' , ), 1610678282, (1610678282, (), [ (12, 0, None, None) , ], 1 , 1 , 4 , 0 , 104 , (3, 0, None, None) , 0 , )),
	(( 'GetMatrix3D' , 'Result' , ), 1610678283, (1610678283, (), [ (16396, 2, None, None) , ], 1 , 1 , 4 , 0 , 112 , (3, 0, None, None) , 0 , )),
	(( 'Rotate' , 'X0' , 'Y0' , 'Z0' , 'AxisZX' , 
			 'AxisZXY' , 'AxisZZ' , 'angle' , ), 1610678284, (1610678284, (), [ (5, 1, None, None) , 
			 (5, 1, None, None) , (5, 1, None, None) , (5, 1, None, None) , (5, 1, None, None) , (5, 1, None, None) , 
			 (5, 1, None, None) , ], 1 , 1 , 4 , 0 , 120 , (3, 0, None, None) , 0 , )),
]

IPlane3PointsDefinition_vtables_dispatch_ = 0
IPlane3PointsDefinition_vtables_ = [
	(( 'GetPoint' , 'number' , ), 1610678272, (1610678272, (), [ (3, 0, None, None) , ], 1 , 1 , 4 , 0 , 24 , (13, 0, None, IID('{7AA0E540-0301-11D4-A30E-00C026EE094F}')) , 0 , )),
	(( 'SetPoint' , 'number' , 'val' , ), 1610678273, (1610678273, (), [ (3, 0, None, None) , 
			 (13, 0, None, "IID('{7AA0E540-0301-11D4-A30E-00C026EE094F}')") , ], 1 , 1 , 4 , 0 , 32 , (3, 0, None, None) , 0 , )),
	(( 'GetSurface' , ), 1610678274, (1610678274, (), [ ], 1 , 1 , 4 , 0 , 40 , (13, 0, None, IID('{081C7F2D-D5BC-40A6-92FE-C16B67D10B75}')) , 0 , )),
]

IPlaneAngleDefinition_vtables_dispatch_ = 0
IPlaneAngleDefinition_vtables_ = [
	(( 'GetPlane' , ), 1610678272, (1610678272, (), [ ], 1 , 1 , 4 , 0 , 24 , (13, 0, None, IID('{7AA0E540-0301-11D4-A30E-00C026EE094F}')) , 0 , )),
	(( 'SetPlane' , 'plane' , ), 1610678273, (1610678273, (), [ (13, 0, None, "IID('{7AA0E540-0301-11D4-A30E-00C026EE094F}')") , ], 1 , 1 , 4 , 0 , 32 , (3, 0, None, None) , 0 , )),
	(( 'GetAxis' , ), 1610678274, (1610678274, (), [ ], 1 , 1 , 4 , 0 , 40 , (13, 0, None, IID('{7AA0E540-0301-11D4-A30E-00C026EE094F}')) , 0 , )),
	(( 'SetAxis' , 'axis' , ), 1610678275, (1610678275, (), [ (13, 0, None, "IID('{7AA0E540-0301-11D4-A30E-00C026EE094F}')") , ], 1 , 1 , 4 , 0 , 48 , (3, 0, None, None) , 0 , )),
	(( 'GetAngle' , ), 1610678276, (1610678276, (), [ ], 1 , 1 , 4 , 0 , 56 , (5, 0, None, None) , 0 , )),
	(( 'SetAngle' , 'val' , ), 1610678277, (1610678277, (), [ (5, 0, None, None) , ], 1 , 1 , 4 , 0 , 64 , (3, 0, None, None) , 0 , )),
	(( 'GetSurface' , ), 1610678278, (1610678278, (), [ ], 1 , 1 , 4 , 0 , 72 , (13, 0, None, IID('{081C7F2D-D5BC-40A6-92FE-C16B67D10B75}')) , 0 , )),
]

IPlaneEdgePointDefinition_vtables_dispatch_ = 0
IPlaneEdgePointDefinition_vtables_ = [
	(( 'GetEdge' , ), 1610678272, (1610678272, (), [ ], 1 , 1 , 4 , 0 , 24 , (13, 0, None, IID('{7AA0E540-0301-11D4-A30E-00C026EE094F}')) , 0 , )),
	(( 'SetEdge' , 'val' , ), 1610678273, (1610678273, (), [ (13, 0, None, "IID('{7AA0E540-0301-11D4-A30E-00C026EE094F}')") , ], 1 , 1 , 4 , 0 , 32 , (3, 0, None, None) , 0 , )),
	(( 'GetPoint' , ), 1610678274, (1610678274, (), [ ], 1 , 1 , 4 , 0 , 40 , (13, 0, None, IID('{7AA0E540-0301-11D4-A30E-00C026EE094F}')) , 0 , )),
	(( 'SetPoint' , 'val' , ), 1610678275, (1610678275, (), [ (13, 0, None, "IID('{7AA0E540-0301-11D4-A30E-00C026EE094F}')") , ], 1 , 1 , 4 , 0 , 48 , (3, 0, None, None) , 0 , )),
	(( 'GetSurface' , ), 1610678276, (1610678276, (), [ ], 1 , 1 , 4 , 0 , 56 , (13, 0, None, IID('{081C7F2D-D5BC-40A6-92FE-C16B67D10B75}')) , 0 , )),
]

IPlaneLineToEdgeDefinition_vtables_dispatch_ = 0
IPlaneLineToEdgeDefinition_vtables_ = [
	(( 'GetEdgeFirst' , ), 1610678272, (1610678272, (), [ ], 1 , 1 , 4 , 0 , 24 , (13, 0, None, IID('{7AA0E540-0301-11D4-A30E-00C026EE094F}')) , 0 , )),
	(( 'SetEdgeFirst' , 'val' , ), 1610678273, (1610678273, (), [ (13, 0, None, "IID('{7AA0E540-0301-11D4-A30E-00C026EE094F}')") , ], 1 , 1 , 4 , 0 , 32 , (3, 0, None, None) , 0 , )),
	(( 'GetEdgeSecond' , ), 1610678274, (1610678274, (), [ ], 1 , 1 , 4 , 0 , 40 , (13, 0, None, IID('{7AA0E540-0301-11D4-A30E-00C026EE094F}')) , 0 , )),
	(( 'SetEdgeSecond' , 'val' , ), 1610678275, (1610678275, (), [ (13, 0, None, "IID('{7AA0E540-0301-11D4-A30E-00C026EE094F}')") , ], 1 , 1 , 4 , 0 , 48 , (3, 0, None, None) , 0 , )),
	(( 'GetParallel' , ), 1610678276, (1610678276, (), [ ], 1 , 1 , 4 , 0 , 56 , (3, 0, None, None) , 0 , )),
	(( 'SetParallel' , 'val' , ), 1610678277, (1610678277, (), [ (3, 0, None, None) , ], 1 , 1 , 4 , 0 , 64 , (3, 0, None, None) , 0 , )),
	(( 'GetSurface' , ), 1610678278, (1610678278, (), [ ], 1 , 1 , 4 , 0 , 72 , (13, 0, None, IID('{081C7F2D-D5BC-40A6-92FE-C16B67D10B75}')) , 0 , )),
]

IPlaneLineToPlaneDefinition_vtables_dispatch_ = 0
IPlaneLineToPlaneDefinition_vtables_ = [
	(( 'GetEdge' , ), 1610678272, (1610678272, (), [ ], 1 , 1 , 4 , 0 , 24 , (13, 0, None, IID('{7AA0E540-0301-11D4-A30E-00C026EE094F}')) , 0 , )),
	(( 'SetEdge' , 'val' , ), 1610678273, (1610678273, (), [ (13, 0, None, "IID('{7AA0E540-0301-11D4-A30E-00C026EE094F}')") , ], 1 , 1 , 4 , 0 , 32 , (3, 0, None, None) , 0 , )),
	(( 'GetPlane' , ), 1610678274, (1610678274, (), [ ], 1 , 1 , 4 , 0 , 40 , (13, 0, None, IID('{7AA0E540-0301-11D4-A30E-00C026EE094F}')) , 0 , )),
	(( 'SetPlane' , 'val' , ), 1610678275, (1610678275, (), [ (13, 0, None, "IID('{7AA0E540-0301-11D4-A30E-00C026EE094F}')") , ], 1 , 1 , 4 , 0 , 48 , (3, 0, None, None) , 0 , )),
	(( 'GetParallel' , ), 1610678276, (1610678276, (), [ ], 1 , 1 , 4 , 0 , 56 , (3, 0, None, None) , 0 , )),
	(( 'SetParallel' , 'val' , ), 1610678277, (1610678277, (), [ (3, 0, None, None) , ], 1 , 1 , 4 , 0 , 64 , (3, 0, None, None) , 0 , )),
	(( 'GetSurface' , ), 1610678278, (1610678278, (), [ ], 1 , 1 , 4 , 0 , 72 , (13, 0, None, IID('{081C7F2D-D5BC-40A6-92FE-C16B67D10B75}')) , 0 , )),
]

IPlaneMiddleDefinition_vtables_dispatch_ = 0
IPlaneMiddleDefinition_vtables_ = [
	(( 'GetObject' , 'number' , ), 1610678272, (1610678272, (), [ (3, 0, None, None) , ], 1 , 1 , 4 , 0 , 24 , (13, 0, None, IID('{7AA0E540-0301-11D4-A30E-00C026EE094F}')) , 0 , )),
	(( 'SetObject' , 'number' , 'val' , ), 1610678273, (1610678273, (), [ (3, 0, None, None) , 
			 (13, 0, None, "IID('{7AA0E540-0301-11D4-A30E-00C026EE094F}')") , ], 1 , 1 , 4 , 0 , 32 , (3, 0, None, None) , 0 , )),
	(( 'GetPosition' , ), 1610678274, (1610678274, (), [ ], 1 , 1 , 4 , 0 , 40 , (3, 0, None, None) , 0 , )),
	(( 'SetPosition' , 'val' , ), 1610678275, (1610678275, (), [ (3, 0, None, None) , ], 1 , 1 , 4 , 0 , 48 , (3, 0, None, None) , 0 , )),
	(( 'GetSurface' , ), 1610678276, (1610678276, (), [ ], 1 , 1 , 4 , 0 , 56 , (13, 0, None, IID('{081C7F2D-D5BC-40A6-92FE-C16B67D10B75}')) , 0 , )),
]

IPlaneNormalToSurfaceDefinition_vtables_dispatch_ = 0
IPlaneNormalToSurfaceDefinition_vtables_ = [
	(( 'GetFace' , ), 1610678272, (1610678272, (), [ ], 1 , 1 , 4 , 0 , 24 , (13, 0, None, IID('{7AA0E540-0301-11D4-A30E-00C026EE094F}')) , 0 , )),
	(( 'SetFace' , 'val' , ), 1610678273, (1610678273, (), [ (13, 0, None, "IID('{7AA0E540-0301-11D4-A30E-00C026EE094F}')") , ], 1 , 1 , 4 , 0 , 32 , (3, 0, None, None) , 0 , )),
	(( 'GetPlane' , ), 1610678274, (1610678274, (), [ ], 1 , 1 , 4 , 0 , 40 , (13, 0, None, IID('{7AA0E540-0301-11D4-A30E-00C026EE094F}')) , 0 , )),
	(( 'SetPlane' , 'val' , ), 1610678275, (1610678275, (), [ (13, 0, None, "IID('{7AA0E540-0301-11D4-A30E-00C026EE094F}')") , ], 1 , 1 , 4 , 0 , 48 , (3, 0, None, None) , 0 , )),
	(( 'GetAngle' , ), 1610678276, (1610678276, (), [ ], 1 , 1 , 4 , 0 , 56 , (5, 0, None, None) , 0 , )),
	(( 'SetAngle' , 'ang' , ), 1610678277, (1610678277, (), [ (5, 0, None, None) , ], 1 , 1 , 4 , 0 , 64 , (3, 0, None, None) , 0 , )),
	(( 'GetSurface' , ), 1610678278, (1610678278, (), [ ], 1 , 1 , 4 , 0 , 72 , (13, 0, None, IID('{081C7F2D-D5BC-40A6-92FE-C16B67D10B75}')) , 0 , )),
	(( 'GetAutoBuilding' , ), 1610678279, (1610678279, (), [ ], 1 , 1 , 4 , 0 , 80 , (3, 0, None, None) , 0 , )),
	(( 'SetAutoBuilding' , 'val' , ), 1610678280, (1610678280, (), [ (3, 0, None, None) , ], 1 , 1 , 4 , 0 , 88 , (3, 0, None, None) , 0 , )),
]

IPlaneOffsetDefinition_vtables_dispatch_ = 0
IPlaneOffsetDefinition_vtables_ = [
	(( 'GetDirection' , ), 1610678272, (1610678272, (), [ ], 1 , 1 , 4 , 0 , 24 , (3, 0, None, None) , 0 , )),
	(( 'SetDirection' , 'val' , ), 1610678273, (1610678273, (), [ (3, 0, None, None) , ], 1 , 1 , 4 , 0 , 32 , (3, 0, None, None) , 0 , )),
	(( 'GetPlane' , ), 1610678274, (1610678274, (), [ ], 1 , 1 , 4 , 0 , 40 , (13, 0, None, IID('{7AA0E540-0301-11D4-A30E-00C026EE094F}')) , 0 , )),
	(( 'SetPlane' , 'val' , ), 1610678275, (1610678275, (), [ (13, 0, None, "IID('{7AA0E540-0301-11D4-A30E-00C026EE094F}')") , ], 1 , 1 , 4 , 0 , 48 , (3, 0, None, None) , 0 , )),
	(( 'GetOffset' , ), 1610678276, (1610678276, (), [ ], 1 , 1 , 4 , 0 , 56 , (5, 0, None, None) , 0 , )),
	(( 'SetOffset' , 'val' , ), 1610678277, (1610678277, (), [ (5, 0, None, None) , ], 1 , 1 , 4 , 0 , 64 , (3, 0, None, None) , 0 , )),
	(( 'GetSurface' , ), 1610678278, (1610678278, (), [ ], 1 , 1 , 4 , 0 , 72 , (13, 0, None, IID('{081C7F2D-D5BC-40A6-92FE-C16B67D10B75}')) , 0 , )),
]

IPlaneParallelDefinition_vtables_dispatch_ = 0
IPlaneParallelDefinition_vtables_ = [
	(( 'GetPlane' , ), 1610678272, (1610678272, (), [ ], 1 , 1 , 4 , 0 , 24 , (13, 0, None, IID('{7AA0E540-0301-11D4-A30E-00C026EE094F}')) , 0 , )),
	(( 'SetPlane' , 'val' , ), 1610678273, (1610678273, (), [ (13, 0, None, "IID('{7AA0E540-0301-11D4-A30E-00C026EE094F}')") , ], 1 , 1 , 4 , 0 , 32 , (3, 0, None, None) , 0 , )),
	(( 'GetPoint' , ), 1610678274, (1610678274, (), [ ], 1 , 1 , 4 , 0 , 40 , (13, 0, None, IID('{7AA0E540-0301-11D4-A30E-00C026EE094F}')) , 0 , )),
	(( 'SetPoint' , 'val' , ), 1610678275, (1610678275, (), [ (13, 0, None, "IID('{7AA0E540-0301-11D4-A30E-00C026EE094F}')") , ], 1 , 1 , 4 , 0 , 48 , (3, 0, None, None) , 0 , )),
	(( 'GetSurface' , ), 1610678276, (1610678276, (), [ ], 1 , 1 , 4 , 0 , 56 , (13, 0, None, IID('{081C7F2D-D5BC-40A6-92FE-C16B67D10B75}')) , 0 , )),
]

IPlaneParam_vtables_dispatch_ = 0
IPlaneParam_vtables_ = [
	(( 'GetPlacement' , ), 1610678272, (1610678272, (), [ ], 1 , 1 , 4 , 0 , 24 , (13, 0, None, IID('{7AA0E540-0310-11D4-A30E-00C026EE094F}')) , 0 , )),
]

IPlanePerpendicularDefinition_vtables_dispatch_ = 0
IPlanePerpendicularDefinition_vtables_ = [
	(( 'GetEdge' , ), 1610678272, (1610678272, (), [ ], 1 , 1 , 4 , 0 , 24 , (13, 0, None, IID('{7AA0E540-0301-11D4-A30E-00C026EE094F}')) , 0 , )),
	(( 'SetEdge' , 'val' , ), 1610678273, (1610678273, (), [ (13, 0, None, "IID('{7AA0E540-0301-11D4-A30E-00C026EE094F}')") , ], 1 , 1 , 4 , 0 , 32 , (3, 0, None, None) , 0 , )),
	(( 'GetPoint' , ), 1610678274, (1610678274, (), [ ], 1 , 1 , 4 , 0 , 40 , (13, 0, None, IID('{7AA0E540-0301-11D4-A30E-00C026EE094F}')) , 0 , )),
	(( 'SetPoint' , 'val' , ), 1610678275, (1610678275, (), [ (13, 0, None, "IID('{7AA0E540-0301-11D4-A30E-00C026EE094F}')") , ], 1 , 1 , 4 , 0 , 48 , (3, 0, None, None) , 0 , )),
	(( 'GetSurface' , ), 1610678276, (1610678276, (), [ ], 1 , 1 , 4 , 0 , 56 , (13, 0, None, IID('{081C7F2D-D5BC-40A6-92FE-C16B67D10B75}')) , 0 , )),
]

IPlaneTangentToSurfaceDefinition_vtables_dispatch_ = 0
IPlaneTangentToSurfaceDefinition_vtables_ = [
	(( 'GetFace' , ), 1610678272, (1610678272, (), [ ], 1 , 1 , 4 , 0 , 24 , (13, 0, None, IID('{7AA0E540-0301-11D4-A30E-00C026EE094F}')) , 0 , )),
	(( 'SetFace' , 'val' , ), 1610678273, (1610678273, (), [ (13, 0, None, "IID('{7AA0E540-0301-11D4-A30E-00C026EE094F}')") , ], 1 , 1 , 4 , 0 , 32 , (3, 0, None, None) , 0 , )),
	(( 'GetPlane' , ), 1610678274, (1610678274, (), [ ], 1 , 1 , 4 , 0 , 40 , (13, 0, None, IID('{7AA0E540-0301-11D4-A30E-00C026EE094F}')) , 0 , )),
	(( 'SetPlane' , 'val' , ), 1610678275, (1610678275, (), [ (13, 0, None, "IID('{7AA0E540-0301-11D4-A30E-00C026EE094F}')") , ], 1 , 1 , 4 , 0 , 48 , (3, 0, None, None) , 0 , )),
	(( 'GetChoosePlane' , ), 1610678276, (1610678276, (), [ ], 1 , 1 , 4 , 0 , 56 , (2, 0, None, None) , 0 , )),
	(( 'SetChoosePlane' , 'Choose' , ), 1610678277, (1610678277, (), [ (2, 0, None, None) , ], 1 , 1 , 4 , 0 , 64 , (3, 0, None, None) , 0 , )),
	(( 'GetSurface' , ), 1610678278, (1610678278, (), [ ], 1 , 1 , 4 , 0 , 72 , (13, 0, None, IID('{081C7F2D-D5BC-40A6-92FE-C16B67D10B75}')) , 0 , )),
	(( 'GetAngle' , ), 1610678279, (1610678279, (), [ ], 1 , 1 , 4 , 0 , 80 , (5, 0, None, None) , 0 , )),
	(( 'SetAngle' , 'ang' , ), 1610678280, (1610678280, (), [ (5, 0, None, None) , ], 1 , 1 , 4 , 0 , 88 , (3, 0, None, None) , 0 , )),
]

IPolygonalLineDefinition_vtables_dispatch_ = 0
IPolygonalLineDefinition_vtables_ = [
	(( 'GetCountVertex' , ), 1610678272, (1610678272, (), [ ], 1 , 1 , 4 , 0 , 24 , (3, 0, None, None) , 0 , )),
	(( 'AddVertex' , 'x' , 'y' , 'z' , 'radius' , 
			 ), 1610678273, (1610678273, (), [ (5, 0, None, None) , (5, 0, None, None) , (5, 0, None, None) , (5, 0, None, None) , ], 1 , 1 , 4 , 0 , 32 , (3, 0, None, None) , 0 , )),
	(( 'InsertVertex' , 'index' , 'x' , 'y' , 'z' , 
			 'radius' , ), 1610678274, (1610678274, (), [ (3, 0, None, None) , (5, 0, None, None) , (5, 0, None, None) , 
			 (5, 0, None, None) , (5, 0, None, None) , ], 1 , 1 , 4 , 0 , 40 , (3, 0, None, None) , 0 , )),
	(( 'DeleteVertex' , 'index' , ), 1610678275, (1610678275, (), [ (3, 0, None, None) , ], 1 , 1 , 4 , 0 , 48 , (3, 0, None, None) , 0 , )),
	(( 'GetParamVertex' , 'index' , 'x' , 'y' , 'z' , 
			 'radius' , ), 1610678276, (1610678276, (), [ (3, 0, None, None) , (16389, 0, None, None) , (16389, 0, None, None) , 
			 (16389, 0, None, None) , (16389, 0, None, None) , ], 1 , 1 , 4 , 0 , 56 , (3, 0, None, None) , 0 , )),
	(( 'Flush' , ), 1610678277, (1610678277, (), [ ], 1 , 1 , 4 , 0 , 64 , (3, 0, None, None) , 0 , )),
	(( 'SetClosed' , 'cls' , ), 1610678278, (1610678278, (), [ (3, 0, None, None) , ], 1 , 1 , 4 , 0 , 72 , (3, 0, None, None) , 0 , )),
	(( 'GetClosed' , ), 1610678279, (1610678279, (), [ ], 1 , 1 , 4 , 0 , 80 , (3, 0, None, None) , 0 , )),
	(( 'ReadFromFile' , 'fileName' , ), 1610678280, (1610678280, (), [ (31, 0, None, None) , ], 1 , 1 , 4 , 0 , 88 , (3, 0, None, None) , 0 , )),
	(( 'WriteToFile' , 'fileName' , ), 1610678281, (1610678281, (), [ (31, 0, None, None) , ], 1 , 1 , 4 , 0 , 96 , (3, 0, None, None) , 0 , )),
	(( 'EdgeCollection' , ), 1610678282, (1610678282, (), [ ], 1 , 1 , 4 , 0 , 104 , (13, 0, None, IID('{5E93D4B9-BAAB-4FC4-ACF8-8FF78E9D1B42}')) , 0 , )),
	(( 'AddPointWithParams' , 'index' , ), 1610678283, (1610678283, (), [ (3, 0, None, None) , ], 1 , 1 , 4 , 0 , 112 , (13, 0, None, IID('{D2D61E71-151A-4359-A0BE-DEA5A76F2492}')) , 0 , )),
	(( 'GetPointParams' , 'index' , ), 1610678284, (1610678284, (), [ (3, 0, None, None) , ], 1 , 1 , 4 , 0 , 120 , (13, 0, None, IID('{D2D61E71-151A-4359-A0BE-DEA5A76F2492}')) , 0 , )),
	(( 'GetVertexVisible' , ), 1610678285, (1610678285, (), [ ], 1 , 1 , 4 , 0 , 128 , (3, 0, None, None) , 0 , )),
	(( 'SetVertexVisible' , 'visible' , ), 1610678286, (1610678286, (), [ (3, 0, None, None) , ], 1 , 1 , 4 , 0 , 136 , (3, 0, None, None) , 0 , )),
	(( 'GetCurve3D' , ), 1610678287, (1610678287, (), [ ], 1 , 1 , 4 , 0 , 144 , (13, 0, None, IID('{E5066490-773D-4289-A60B-2FC19865174A}')) , 0 , )),
]

IPolygonalLineVertexParam_vtables_dispatch_ = 0
IPolygonalLineVertexParam_vtables_ = [
	(( 'GetBuildingType' , ), 1610678272, (1610678272, (), [ ], 1 , 1 , 4 , 0 , 24 , (3, 0, None, None) , 0 , )),
	(( 'SetBuildingType' , 'type' , ), 1610678273, (1610678273, (), [ (3, 0, None, None) , ], 1 , 1 , 4 , 0 , 32 , (3, 0, None, None) , 0 , )),
	(( 'GetParamVertex' , 'x' , 'y' , 'z' , 'radius' , 
			 ), 1610678274, (1610678274, (), [ (16389, 0, None, None) , (16389, 0, None, None) , (16389, 0, None, None) , (16389, 0, None, None) , ], 1 , 1 , 4 , 0 , 40 , (3, 0, None, None) , 0 , )),
	(( 'SetParamVertex' , 'x' , 'y' , 'z' , 'radius' , 
			 ), 1610678275, (1610678275, (), [ (5, 0, None, None) , (5, 0, None, None) , (5, 0, None, None) , (5, 0, None, None) , ], 1 , 1 , 4 , 0 , 48 , (3, 0, None, None) , 0 , )),
	(( 'SetParamByVertex' , 'vertex' , 'radius' , ), 1610678276, (1610678276, (), [ (13, 0, None, "IID('{7AA0E540-0301-11D4-A30E-00C026EE094F}')") , 
			 (5, 0, None, None) , ], 1 , 1 , 4 , 0 , 56 , (3, 0, None, None) , 0 , )),
	(( 'GetParamByDistance' , 'distance' , 'radius' , ), 1610678277, (1610678277, (), [ (16389, 0, None, None) , 
			 (16389, 0, None, None) , ], 1 , 1 , 4 , 0 , 64 , (3, 0, None, None) , 0 , )),
	(( 'SetParamByDistance' , 'distance' , 'radius' , ), 1610678278, (1610678278, (), [ (5, 0, None, None) , 
			 (5, 0, None, None) , ], 1 , 1 , 4 , 0 , 72 , (3, 0, None, None) , 0 , )),
	(( 'GetBuildingObject' , ), 1610678279, (1610678279, (), [ ], 1 , 1 , 4 , 0 , 80 , (13, 0, None, IID('{7AA0E540-0301-11D4-A30E-00C026EE094F}')) , 0 , )),
	(( 'SetBuildingObject' , 'object' , ), 1610678280, (1610678280, (), [ (13, 0, None, "IID('{7AA0E540-0301-11D4-A30E-00C026EE094F}')") , ], 1 , 1 , 4 , 0 , 88 , (3, 0, None, None) , 0 , )),
	(( 'GetAssociation' , ), 1610678281, (1610678281, (), [ ], 1 , 1 , 4 , 0 , 96 , (13, 0, None, IID('{7AA0E540-0301-11D4-A30E-00C026EE094F}')) , 0 , )),
	(( 'SetAssociation' , 'vertex' , ), 1610678282, (1610678282, (), [ (13, 0, None, "IID('{7AA0E540-0301-11D4-A30E-00C026EE094F}')") , ], 1 , 1 , 4 , 0 , 104 , (3, 0, None, None) , 0 , )),
	(( 'GetVertex' , ), 1610678283, (1610678283, (), [ ], 1 , 1 , 4 , 0 , 112 , (13, 0, None, IID('{7AA0E540-0301-11D4-A30E-00C026EE094F}')) , 0 , )),
	(( 'GetIndex' , ), 1610678284, (1610678284, (), [ ], 1 , 1 , 4 , 0 , 120 , (3, 0, None, None) , 0 , )),
]

IProcess3DManipulatorsNotify_vtables_dispatch_ = 0
IProcess3DManipulatorsNotify_vtables_ = [
	(( 'RotateManipulator' , 'ManipulatorId' , 'X0' , 'Y0' , 'Z0' , 
			 'AxisZX' , 'AxisZXY' , 'AxisZZ' , 'angle' , 'FromEdit' , 
			 ), 1610743808, (1610743808, (), [ (3, 1, None, None) , (5, 1, None, None) , (5, 1, None, None) , (5, 1, None, None) , 
			 (5, 1, None, None) , (5, 1, None, None) , (5, 1, None, None) , (5, 1, None, None) , (11, 1, None, None) , ], 1 , 1 , 4 , 0 , 32 , (11, 0, None, None) , 0 , )),
	(( 'MoveManipulator' , 'ManipulatorId' , 'VX' , 'VY' , 'VZ' , 
			 'Delta' , 'FromEdit' , ), 1610743809, (1610743809, (), [ (3, 1, None, None) , (5, 1, None, None) , 
			 (5, 1, None, None) , (5, 1, None, None) , (5, 1, None, None) , (11, 1, None, None) , ], 1 , 1 , 4 , 0 , 40 , (11, 0, None, None) , 0 , )),
	(( 'ClickManipulatorPrimitive' , 'ManipulatorId' , 'PrimitiveType' , 'DoubleClick' , ), 1610743810, (1610743810, (), [ 
			 (3, 1, None, None) , (3, 1, None, None) , (11, 1, None, None) , ], 1 , 1 , 4 , 0 , 48 , (11, 0, None, None) , 0 , )),
	(( 'BeginDragManipulator' , 'ManipulatorId' , 'PrimitiveType' , ), 1610743811, (1610743811, (), [ (3, 1, None, None) , 
			 (3, 1, None, None) , ], 1 , 1 , 4 , 0 , 56 , (11, 0, None, None) , 0 , )),
	(( 'EndDragManipulator' , 'ManipulatorId' , 'PrimitiveType' , ), 1610743812, (1610743812, (), [ (3, 1, None, None) , 
			 (3, 1, None, None) , ], 1 , 1 , 4 , 0 , 64 , (11, 0, None, None) , 0 , )),
	(( 'CreateManipulatorEdit' , 'ManipulatorId' , 'PrimitiveType' , ), 1610743813, (1610743813, (), [ (3, 1, None, None) , 
			 (3, 1, None, None) , ], 1 , 1 , 4 , 0 , 72 , (11, 0, None, None) , 0 , )),
	(( 'DestroyManipulatorEdit' , 'ManipulatorId' , ), 1610743814, (1610743814, (), [ (3, 1, None, None) , ], 1 , 1 , 4 , 0 , 80 , (11, 0, None, None) , 0 , )),
	(( 'ChangeManipulatorValue' , 'ManipulatorId' , 'PrimitiveType' , 'newValue' , ), 1610743815, (1610743815, (), [ 
			 (3, 1, None, None) , (3, 1, None, None) , (5, 1, None, None) , ], 1 , 1 , 4 , 0 , 88 , (11, 0, None, None) , 0 , )),
]

IProcess3DNotify_vtables_dispatch_ = 0
IProcess3DNotify_vtables_ = [
	(( 'PlacementChange' , 'obj' , ), 1610743808, (1610743808, (), [ (13, 0, None, None) , ], 1 , 1 , 4 , 0 , 32 , (11, 0, None, None) , 0 , )),
	(( 'ExecuteCommand' , 'command' , ), 1610743809, (1610743809, (), [ (3, 0, None, None) , ], 1 , 1 , 4 , 0 , 40 , (11, 0, None, None) , 0 , )),
	(( 'Run' , ), 1610743810, (1610743810, (), [ ], 1 , 1 , 4 , 0 , 48 , (11, 0, None, None) , 0 , )),
	(( 'Stop' , ), 1610743811, (1610743811, (), [ ], 1 , 1 , 4 , 0 , 56 , (11, 0, None, None) , 0 , )),
	(( 'Activate' , ), 1610743812, (1610743812, (), [ ], 1 , 1 , 4 , 0 , 64 , (11, 0, None, None) , 0 , )),
	(( 'Deactivate' , ), 1610743813, (1610743813, (), [ ], 1 , 1 , 4 , 0 , 72 , (11, 0, None, None) , 0 , )),
	(( 'FilterObject' , 'obj' , ), 1610743814, (1610743814, (), [ (13, 0, None, None) , ], 1 , 1 , 4 , 0 , 80 , (11, 0, None, None) , 0 , )),
	(( 'CreateTakeObject' , 'obj' , ), 1610743815, (1610743815, (), [ (13, 0, None, None) , ], 1 , 1 , 4 , 0 , 88 , (11, 0, None, None) , 0 , )),
	(( 'EndProcess' , ), 1610743816, (1610743816, (), [ ], 1 , 1 , 4 , 0 , 96 , (11, 0, None, None) , 0 , )),
	(( 'ProcessingGroupObjects' , 'groupObjects' , 'selectionType' , ), 1610743817, (1610743817, (), [ (12, 0, None, None) , 
			 (3, 0, None, None) , ], 1 , 1 , 4 , 0 , 104 , (11, 0, None, None) , 0 , )),
]

IRasterFormatParam_vtables_dispatch_ = 0
IRasterFormatParam_vtables_ = [
	(( 'GetFormat' , ), 1610678272, (1610678272, (), [ ], 1 , 1 , 4 , 0 , 24 , (2, 0, None, None) , 0 , )),
	(( 'SetFormat' , 'f' , ), 1610678273, (1610678273, (), [ (2, 0, None, None) , ], 1 , 1 , 4 , 0 , 32 , (3, 0, None, None) , 0 , )),
	(( 'GetColorBPP' , ), 1610678274, (1610678274, (), [ ], 1 , 1 , 4 , 0 , 40 , (2, 0, None, None) , 0 , )),
	(( 'SetColorBPP' , 'f' , ), 1610678275, (1610678275, (), [ (2, 0, None, None) , ], 1 , 1 , 4 , 0 , 48 , (3, 0, None, None) , 0 , )),
	(( 'GetGreyScale' , ), 1610678276, (1610678276, (), [ ], 1 , 1 , 4 , 0 , 56 , (3, 0, None, None) , 0 , )),
	(( 'SetGreyScale' , 'f' , ), 1610678277, (1610678277, (), [ (3, 0, None, None) , ], 1 , 1 , 4 , 0 , 64 , (3, 0, None, None) , 0 , )),
	(( 'GetExtResolution' , ), 1610678278, (1610678278, (), [ ], 1 , 1 , 4 , 0 , 72 , (3, 0, None, None) , 0 , )),
	(( 'SetExtResolution' , 'f' , ), 1610678279, (1610678279, (), [ (3, 0, None, None) , ], 1 , 1 , 4 , 0 , 80 , (3, 0, None, None) , 0 , )),
	(( 'GetExtScale' , ), 1610678280, (1610678280, (), [ ], 1 , 1 , 4 , 0 , 88 , (5, 0, None, None) , 0 , )),
	(( 'SetExtScale' , 'f' , ), 1610678281, (1610678281, (), [ (5, 0, None, None) , ], 1 , 1 , 4 , 0 , 96 , (3, 0, None, None) , 0 , )),
	(( 'GetColorType' , ), 1610678282, (1610678282, (), [ ], 1 , 1 , 4 , 0 , 104 , (2, 0, None, None) , 0 , )),
	(( 'SetColorType' , 'f' , ), 1610678283, (1610678283, (), [ (2, 0, None, None) , ], 1 , 1 , 4 , 0 , 112 , (3, 0, None, None) , 0 , )),
	(( 'GetOnlyThinLine' , ), 1610678284, (1610678284, (), [ ], 1 , 1 , 4 , 0 , 120 , (3, 0, None, None) , 0 , )),
	(( 'SetOnlyThinLine' , 'f' , ), 1610678285, (1610678285, (), [ (3, 0, None, None) , ], 1 , 1 , 4 , 0 , 128 , (3, 0, None, None) , 0 , )),
	(( 'GetPages' , ), 1610678286, (1610678286, (), [ ], 1 , 1 , 4 , 0 , 136 , (31, 0, None, None) , 0 , )),
	(( 'SetPages' , 'p' , ), 1610678287, (1610678287, (), [ (31, 0, None, None) , ], 1 , 1 , 4 , 0 , 144 , (3, 0, None, None) , 0 , )),
	(( 'GetRangeIndex' , ), 1610678288, (1610678288, (), [ ], 1 , 1 , 4 , 0 , 152 , (2, 0, None, None) , 0 , )),
	(( 'SetRangeIndex' , 'f' , ), 1610678289, (1610678289, (), [ (2, 0, None, None) , ], 1 , 1 , 4 , 0 , 160 , (3, 0, None, None) , 0 , )),
	(( 'GetMultiPageOutput' , ), 1610678290, (1610678290, (), [ ], 1 , 1 , 4 , 0 , 168 , (3, 0, None, None) , 0 , )),
	(( 'SetMultiPageOutput' , 'f' , ), 1610678291, (1610678291, (), [ (3, 0, None, None) , ], 1 , 1 , 4 , 0 , 176 , (3, 0, None, None) , 0 , )),
	(( 'Init' , ), 1610678292, (1610678292, (), [ ], 1 , 1 , 4 , 0 , 184 , (3, 0, None, None) , 0 , )),
	(( 'GetSaveWorkArea' , ), 1610678293, (1610678293, (), [ ], 1 , 1 , 4 , 0 , 192 , (3, 0, None, None) , 0 , )),
	(( 'SetSaveWorkArea' , 'f' , ), 1610678294, (1610678294, (), [ (3, 0, None, None) , ], 1 , 1 , 4 , 0 , 200 , (3, 0, None, None) , 0 , )),
]

IRequestInfo_vtables_dispatch_ = 0
IRequestInfo_vtables_ = [
	(( 'GetPrompt' , ), 1610678272, (1610678272, (), [ ], 1 , 1 , 4 , 0 , 24 , (31, 0, None, None) , 0 , )),
	(( 'SetPrompt' , 'prompt' , ), 1610678273, (1610678273, (), [ (31, 0, None, None) , ], 1 , 1 , 4 , 0 , 32 , (3, 0, None, None) , 0 , )),
	(( 'GetPlacement' , ), 1610678274, (1610678274, (), [ ], 1 , 1 , 4 , 0 , 40 , (13, 0, None, IID('{7AA0E540-0310-11D4-A30E-00C026EE094F}')) , 0 , )),
	(( 'GetEntityCollection' , ), 1610678275, (1610678275, (), [ ], 1 , 1 , 4 , 0 , 48 , (13, 0, None, IID('{7AA0E540-0303-11D4-A30E-00C026EE094F}')) , 0 , )),
	(( 'GetFilterCallBack' , ), 1610678276, (1610678276, (), [ ], 1 , 1 , 4 , 0 , 56 , (16408, 0, None, None) , 0 , )),
	(( 'SetFilterCallBack' , 'callBack' , ), 1610678277, (1610678277, (), [ (16408, 0, None, None) , ], 1 , 1 , 4 , 0 , 64 , (3, 0, None, None) , 0 , )),
	(( 'GetCallBack' , ), 1610678278, (1610678278, (), [ ], 1 , 1 , 4 , 0 , 72 , (16408, 0, None, None) , 0 , )),
	(( 'SetCallBack' , 'callBack' , ), 1610678279, (1610678279, (), [ (16408, 0, None, None) , ], 1 , 1 , 4 , 0 , 80 , (3, 0, None, None) , 0 , )),
	(( 'GetCommandsString' , ), 1610678280, (1610678280, (), [ ], 1 , 1 , 4 , 0 , 88 , (31, 0, None, None) , 0 , )),
	(( 'SetCommandsString' , 'menu' , ), 1610678281, (1610678281, (), [ (31, 0, None, None) , ], 1 , 1 , 4 , 0 , 96 , (3, 0, None, None) , 0 , )),
	(( 'GetMenuId' , ), 1610678282, (1610678282, (), [ ], 1 , 1 , 4 , 0 , 104 , (3, 0, None, None) , 0 , )),
	(( 'SetMenuId' , 'menuId' , ), 1610678283, (1610678283, (), [ (3, 0, None, None) , ], 1 , 1 , 4 , 0 , 112 , (3, 0, None, None) , 0 , )),
	(( 'GetCurrentCommand' , ), 1610678284, (1610678284, (), [ ], 1 , 1 , 4 , 0 , 120 , (3, 0, None, None) , 0 , )),
	(( 'GetCursorName' , ), 1610678285, (1610678285, (), [ ], 1 , 1 , 4 , 0 , 128 , (31, 0, None, None) , 0 , )),
	(( 'SetCursorName' , 'cursor' , ), 1610678286, (1610678286, (), [ (31, 0, None, None) , ], 1 , 1 , 4 , 0 , 136 , (3, 0, None, None) , 0 , )),
	(( 'GetCursorId' , ), 1610678287, (1610678287, (), [ ], 1 , 1 , 4 , 0 , 144 , (3, 0, None, None) , 0 , )),
	(( 'SetCursorId' , 'cursorId' , ), 1610678288, (1610678288, (), [ (3, 0, None, None) , ], 1 , 1 , 4 , 0 , 152 , (3, 0, None, None) , 0 , )),
	(( 'GetTitle' , ), 1610678289, (1610678289, (), [ ], 1 , 1 , 4 , 0 , 160 , (31, 0, None, None) , 0 , )),
	(( 'SetTitle' , 'title' , ), 1610678290, (1610678290, (), [ (31, 0, None, None) , ], 1 , 1 , 4 , 0 , 168 , (3, 0, None, None) , 0 , )),
	(( 'GetMateConstraintCollection' , ), 1610678291, (1610678291, (), [ ], 1 , 1 , 4 , 0 , 176 , (13, 0, None, IID('{7AA0E540-0304-11D4-A30E-00C026EE094F}')) , 0 , )),
	(( 'GetIPhantom' , ), 1610678292, (1610678292, (), [ ], 1 , 1 , 4 , 0 , 184 , (13, 0, None, IID('{7AA0E540-0300-11D4-A30E-00C026EE094F}')) , 0 , )),
	(( 'CreatePhantom' , ), 1610678293, (1610678293, (), [ ], 1 , 1 , 4 , 0 , 192 , (3, 0, None, None) , 0 , )),
	(( 'GetProcessParam' , ), 1610678294, (1610678294, (), [ ], 1 , 1 , 4 , 0 , 200 , (13, 0, None, None) , 0 , )),
	(( 'SetProcessParam' , 'param' , ), 1610678295, (1610678295, (), [ (13, 0, None, None) , ], 1 , 1 , 4 , 0 , 208 , (3, 0, None, None) , 0 , )),
	(( 'GetCallBackFeature' , ), 1610678296, (1610678296, (), [ ], 1 , 1 , 4 , 0 , 216 , (13, 0, None, IID('{1D15245B-695E-4F9F-AFCA-EACBC3A055BB}')) , 0 , )),
	(( 'GetDynamicFiltering' , ), 1610678297, (1610678297, (), [ ], 1 , 1 , 4 , 0 , 224 , (3, 0, None, None) , 0 , )),
	(( 'SetDynamicFiltering' , 'f' , ), 1610678298, (1610678298, (), [ (3, 0, None, None) , ], 1 , 1 , 4 , 0 , 232 , (3, 0, None, None) , 0 , )),
	(( 'SetCursorText' , 'text' , ), 1610678299, (1610678299, (), [ (31, 0, None, None) , ], 1 , 1 , 4 , 0 , 240 , (3, 0, None, None) , 0 , )),
	(( 'GetShowCommandWindow' , ), 1610678300, (1610678300, (), [ ], 1 , 1 , 4 , 0 , 248 , (3, 0, None, None) , 0 , )),
	(( 'SetShowCommandWindow' , 'f' , ), 1610678301, (1610678301, (), [ (3, 0, None, None) , ], 1 , 1 , 4 , 0 , 256 , (3, 0, None, None) , 0 , )),
	(( 'GetTakeProcessObject' , ), 1610678302, (1610678302, (), [ ], 1 , 1 , 4 , 0 , 264 , (13, 0, None, None) , 0 , )),
	(( 'SetTakeProcessObject' , 'takeObject' , ), 1610678303, (1610678303, (), [ (13, 0, None, None) , ], 1 , 1 , 4 , 0 , 272 , (3, 0, None, None) , 0 , )),
	(( 'GetTakeObjectCallBack' , ), 1610678304, (1610678304, (), [ ], 1 , 1 , 4 , 0 , 280 , (16408, 0, None, None) , 0 , )),
	(( 'SetTakeObjectCallBack' , 'callBack' , ), 1610678305, (1610678305, (), [ (16408, 0, None, None) , ], 1 , 1 , 4 , 0 , 288 , (3, 0, None, None) , 0 , )),
	(( 'GetSelectionBandMode' , ), 1610678306, (1610678306, (), [ ], 1 , 1 , 4 , 0 , 296 , (3, 0, None, None) , 0 , )),
	(( 'SetSelectionBandMode' , 'f' , ), 1610678307, (1610678307, (), [ (3, 0, None, None) , ], 1 , 1 , 4 , 0 , 304 , (3, 0, None, None) , 0 , )),
	(( 'GetProcessingGroupObjectsCallBack' , ), 1610678308, (1610678308, (), [ ], 1 , 1 , 4 , 0 , 312 , (16408, 0, None, None) , 0 , )),
	(( 'SetProcessingGroupObjectsCallBack' , 'callBack' , ), 1610678309, (1610678309, (), [ (16408, 0, None, None) , ], 1 , 1 , 4 , 0 , 320 , (3, 0, None, None) , 0 , )),
	(( 'SetObjectsFilter3D' , 'filterType' , 'newVal' , ), 1610678310, (1610678310, (), [ (3, 0, None, None) , 
			 (3, 0, None, None) , ], 1 , 1 , 4 , 0 , 328 , (3, 0, None, None) , 0 , )),
	(( 'GetObjectsFilter3D' , 'filterType' , ), 1610678311, (1610678311, (), [ (3, 0, None, None) , ], 1 , 1 , 4 , 0 , 336 , (3, 0, None, None) , 0 , )),
]

IRibDefinition_vtables_dispatch_ = 0
IRibDefinition_vtables_ = [
	(( 'GetSketch' , ), 1610678272, (1610678272, (), [ ], 1 , 1 , 4 , 0 , 24 , (13, 0, None, IID('{7AA0E540-0301-11D4-A30E-00C026EE094F}')) , 0 , )),
	(( 'SetSketch' , 'sketch' , ), 1610678273, (1610678273, (), [ (13, 0, None, "IID('{7AA0E540-0301-11D4-A30E-00C026EE094F}')") , ], 1 , 1 , 4 , 0 , 32 , (3, 0, None, None) , 0 , )),
	(( 'GetIndexSegmentBySketch' , ), 1610678274, (1610678274, (), [ ], 1 , 1 , 4 , 0 , 40 , (3, 0, None, None) , 0 , )),
	(( 'SetIndexSegmentBySketch' , 'index' , ), 1610678275, (1610678275, (), [ (3, 0, None, None) , ], 1 , 1 , 4 , 0 , 48 , (3, 0, None, None) , 0 , )),
	(( 'GetAngle' , ), 1610678276, (1610678276, (), [ ], 1 , 1 , 4 , 0 , 56 , (5, 0, None, None) , 0 , )),
	(( 'SetAngle' , 'angle' , ), 1610678277, (1610678277, (), [ (5, 0, None, None) , ], 1 , 1 , 4 , 0 , 64 , (3, 0, None, None) , 0 , )),
	(( 'GetSide' , ), 1610678278, (1610678278, (), [ ], 1 , 1 , 4 , 0 , 72 , (3, 0, None, None) , 0 , )),
	(( 'SetSide' , 'side' , ), 1610678279, (1610678279, (), [ (3, 0, None, None) , ], 1 , 1 , 4 , 0 , 80 , (3, 0, None, None) , 0 , )),
	(( 'GetThinParam' , 'thinType' , 'normalThickness' , 'reverseThickness' , ), 1610678280, (1610678280, (), [ 
			 (16401, 0, None, None) , (16389, 0, None, None) , (16389, 0, None, None) , ], 1 , 1 , 4 , 0 , 88 , (3, 0, None, None) , 0 , )),
	(( 'SetThinParam' , 'thinType' , 'normalThickness' , 'reverseThickness' , ), 1610678281, (1610678281, (), [ 
			 (17, 0, None, None) , (5, 0, None, None) , (5, 0, None, None) , ], 1 , 1 , 4 , 0 , 96 , (24, 0, None, None) , 0 , )),
	(( 'ThinParam' , ), 1610678282, (1610678282, (), [ ], 1 , 1 , 4 , 0 , 104 , (13, 0, None, IID('{7AA0E540-0306-11D4-A30E-00C026EE094F}')) , 0 , )),
]

IRotatedParam_vtables_dispatch_ = 0
IRotatedParam_vtables_ = [
	(( 'GetAngleNormal' , ), 1610678272, (1610678272, (), [ ], 1 , 1 , 4 , 0 , 24 , (5, 0, None, None) , 0 , )),
	(( 'SetAngleNormal' , 'val' , ), 1610678273, (1610678273, (), [ (5, 0, None, None) , ], 1 , 1 , 4 , 0 , 32 , (3, 0, None, None) , 0 , )),
	(( 'GetAngleReverse' , ), 1610678274, (1610678274, (), [ ], 1 , 1 , 4 , 0 , 40 , (5, 0, None, None) , 0 , )),
	(( 'SetAngleReverse' , 'val' , ), 1610678275, (1610678275, (), [ (5, 0, None, None) , ], 1 , 1 , 4 , 0 , 48 , (3, 0, None, None) , 0 , )),
	(( 'GetToroidShape' , ), 1610678276, (1610678276, (), [ ], 1 , 1 , 4 , 0 , 56 , (3, 0, None, None) , 0 , )),
	(( 'SetToroidShape' , 'val' , ), 1610678277, (1610678277, (), [ (3, 0, None, None) , ], 1 , 1 , 4 , 0 , 64 , (3, 0, None, None) , 0 , )),
	(( 'GetDirection' , ), 1610678278, (1610678278, (), [ ], 1 , 1 , 4 , 0 , 72 , (3, 0, None, None) , 0 , )),
	(( 'SetDirection' , 'val' , ), 1610678279, (1610678279, (), [ (3, 0, None, None) , ], 1 , 1 , 4 , 0 , 80 , (3, 0, None, None) , 0 , )),
]

IRotatedSurfaceDefinition_vtables_dispatch_ = 0
IRotatedSurfaceDefinition_vtables_ = [
	(( 'SetSketch' , 'name' , ), 1610678272, (1610678272, (), [ (13, 0, None, "IID('{7AA0E540-0301-11D4-A30E-00C026EE094F}')") , ], 1 , 1 , 4 , 0 , 24 , (3, 0, None, None) , 0 , )),
	(( 'GetSketch' , ), 1610678273, (1610678273, (), [ ], 1 , 1 , 4 , 0 , 32 , (13, 0, None, IID('{7AA0E540-0301-11D4-A30E-00C026EE094F}')) , 0 , )),
	(( 'GetSideParam' , 'forward' , 'angle' , ), 1610678274, (1610678274, (), [ (3, 0, None, None) , 
			 (16389, 0, None, None) , ], 1 , 1 , 4 , 0 , 40 , (3, 0, None, None) , 0 , )),
	(( 'SetSideParam' , 'forward' , 'angle' , ), 1610678275, (1610678275, (), [ (3, 0, None, None) , 
			 (5, 0, None, None) , ], 1 , 1 , 4 , 0 , 48 , (24, 0, None, None) , 0 , )),
	(( 'SetToroidShapeType' , 'dirType' , ), 1610678276, (1610678276, (), [ (3, 0, None, None) , ], 1 , 1 , 4 , 0 , 56 , (3, 0, None, None) , 0 , )),
	(( 'GetToroidShapeType' , ), 1610678277, (1610678277, (), [ ], 1 , 1 , 4 , 0 , 64 , (3, 0, None, None) , 0 , )),
	(( 'SetDirectionType' , 'dirType' , ), 1610678278, (1610678278, (), [ (3, 0, None, None) , ], 1 , 1 , 4 , 0 , 72 , (3, 0, None, None) , 0 , )),
	(( 'GetDirectionType' , ), 1610678279, (1610678279, (), [ ], 1 , 1 , 4 , 0 , 80 , (3, 0, None, None) , 0 , )),
	(( 'RotatedParam' , ), 1610678280, (1610678280, (), [ ], 1 , 1 , 4 , 0 , 88 , (13, 0, None, IID('{7AA0E540-0308-11D4-A30E-00C026EE094F}')) , 0 , )),
	(( 'GetClosedShell' , ), 1610678281, (1610678281, (), [ ], 1 , 1 , 4 , 0 , 96 , (3, 0, None, None) , 0 , )),
	(( 'SetClosedShell' , 'closed' , ), 1610678282, (1610678282, (), [ (3, 0, None, None) , ], 1 , 1 , 4 , 0 , 104 , (3, 0, None, None) , 0 , )),
]

ISTrackingPointsMeasurer_vtables_dispatch_ = 0
ISTrackingPointsMeasurer_vtables_ = [
	(( 'SetPoint1' , 'x' , 'y' , 'z' , 'begin' , 
			 ), 1610678272, (1610678272, (), [ (5, 0, None, None) , (5, 0, None, None) , (5, 0, None, None) , (3, 0, None, None) , ], 1 , 1 , 4 , 0 , 24 , (24, 0, None, None) , 0 , )),
	(( 'SetPoint2' , 'x' , 'y' , 'z' , 'begin' , 
			 ), 1610678273, (1610678273, (), [ (5, 0, None, None) , (5, 0, None, None) , (5, 0, None, None) , (3, 0, None, None) , ], 1 , 1 , 4 , 0 , 32 , (24, 0, None, None) , 0 , )),
	(( 'SetRadius1' , 'val' , ), 1610678274, (1610678274, (), [ (5, 0, None, None) , ], 1 , 1 , 4 , 0 , 40 , (24, 0, None, None) , 0 , )),
	(( 'SetRadius2' , 'val' , ), 1610678275, (1610678275, (), [ (5, 0, None, None) , ], 1 , 1 , 4 , 0 , 48 , (24, 0, None, None) , 0 , )),
	(( 'Calculate' , ), 1610678276, (1610678276, (), [ ], 1 , 1 , 4 , 0 , 56 , (3, 0, None, None) , 0 , )),
	(( 'GetResultPoint1' , 'x' , 'y' , 'z' , ), 1610678277, (1610678277, (), [ 
			 (16389, 0, None, None) , (16389, 0, None, None) , (16389, 0, None, None) , ], 1 , 1 , 4 , 0 , 64 , (24, 0, None, None) , 0 , )),
	(( 'GetResultPoint2' , 'x' , 'y' , 'z' , ), 1610678278, (1610678278, (), [ 
			 (16389, 0, None, None) , (16389, 0, None, None) , (16389, 0, None, None) , ], 1 , 1 , 4 , 0 , 72 , (24, 0, None, None) , 0 , )),
]

ISelectionMng_vtables_dispatch_ = 0
ISelectionMng_vtables_ = [
	(( 'Select' , 'obj' , ), 1610678272, (1610678272, (), [ (13, 0, None, None) , ], 1 , 1 , 4 , 0 , 24 , (3, 0, None, None) , 0 , )),
	(( 'Unselect' , 'obj' , ), 1610678273, (1610678273, (), [ (13, 0, None, None) , ], 1 , 1 , 4 , 0 , 32 , (3, 0, None, None) , 0 , )),
	(( 'UnselectAll' , ), 1610678274, (1610678274, (), [ ], 1 , 1 , 4 , 0 , 40 , (3, 0, None, None) , 0 , )),
	(( 'IsSelected' , 'obj' , ), 1610678275, (1610678275, (), [ (13, 0, None, None) , ], 1 , 1 , 4 , 0 , 48 , (3, 0, None, None) , 0 , )),
	(( 'GetCount' , ), 1610678276, (1610678276, (), [ ], 1 , 1 , 4 , 0 , 56 , (3, 0, None, None) , 0 , )),
	(( 'First' , ), 1610678277, (1610678277, (), [ ], 1 , 1 , 4 , 0 , 64 , (13, 0, None, None) , 0 , )),
	(( 'Last' , ), 1610678278, (1610678278, (), [ ], 1 , 1 , 4 , 0 , 72 , (13, 0, None, None) , 0 , )),
	(( 'Next' , ), 1610678279, (1610678279, (), [ ], 1 , 1 , 4 , 0 , 80 , (13, 0, None, None) , 0 , )),
	(( 'Prev' , ), 1610678280, (1610678280, (), [ ], 1 , 1 , 4 , 0 , 88 , (13, 0, None, None) , 0 , )),
	(( 'GetObjectByIndex' , 'index' , ), 1610678281, (1610678281, (), [ (3, 0, None, None) , ], 1 , 1 , 4 , 0 , 96 , (13, 0, None, None) , 0 , )),
	(( 'GetObjectType' , 'index' , ), 1610678282, (1610678282, (), [ (3, 0, None, None) , ], 1 , 1 , 4 , 0 , 104 , (3, 0, None, None) , 0 , )),
]

IShellDefinition_vtables_dispatch_ = 0
IShellDefinition_vtables_ = [
	(( 'FaceArray' , ), 1610678272, (1610678272, (), [ ], 1 , 1 , 4 , 0 , 24 , (13, 0, None, IID('{7AA0E540-0303-11D4-A30E-00C026EE094F}')) , 0 , )),
	(( 'GetThinType' , ), 1610678273, (1610678273, (), [ ], 1 , 1 , 4 , 0 , 32 , (3, 0, None, None) , 0 , )),
	(( 'SetThinType' , 'thinType' , ), 1610678274, (1610678274, (), [ (3, 0, None, None) , ], 1 , 1 , 4 , 0 , 40 , (3, 0, None, None) , 0 , )),
	(( 'GetThickness' , ), 1610678275, (1610678275, (), [ ], 1 , 1 , 4 , 0 , 48 , (5, 0, None, None) , 0 , )),
	(( 'SetThickness' , 'thickness' , ), 1610678276, (1610678276, (), [ (5, 0, None, None) , ], 1 , 1 , 4 , 0 , 56 , (3, 0, None, None) , 0 , )),
]

ISketchDefinition_vtables_dispatch_ = 0
ISketchDefinition_vtables_ = [
	(( 'SetPlane' , 'name' , ), 1610678272, (1610678272, (), [ (13, 0, None, "IID('{7AA0E540-0301-11D4-A30E-00C026EE094F}')") , ], 1 , 1 , 4 , 0 , 24 , (3, 0, None, None) , 0 , )),
	(( 'GetPlane' , ), 1610678273, (1610678273, (), [ ], 1 , 1 , 4 , 0 , 32 , (13, 0, None, IID('{7AA0E540-0301-11D4-A30E-00C026EE094F}')) , 0 , )),
	(( 'GetLocation' , 'x' , 'y' , ), 1610678274, (1610678274, (), [ (16389, 0, None, None) , 
			 (16389, 0, None, None) , ], 1 , 1 , 4 , 0 , 40 , (3, 0, None, None) , 0 , )),
	(( 'SetLocation' , 'x' , 'y' , ), 1610678275, (1610678275, (), [ (5, 0, None, None) , 
			 (5, 0, None, None) , ], 1 , 1 , 4 , 0 , 48 , (3, 0, None, None) , 0 , )),
	(( 'GetAngle' , ), 1610678276, (1610678276, (), [ ], 1 , 1 , 4 , 0 , 56 , (5, 0, None, None) , 0 , )),
	(( 'SetAngle' , 'ang' , ), 1610678277, (1610678277, (), [ (5, 0, None, None) , ], 1 , 1 , 4 , 0 , 64 , (3, 0, None, None) , 0 , )),
	(( 'UserSetPlacement' , 'prompt' , ), 1610678278, (1610678278, (), [ (31, 0, None, None) , ], 1 , 1 , 4 , 0 , 72 , (3, 0, None, None) , 0 , )),
	(( 'BeginEdit' , ), 1610678279, (1610678279, (), [ ], 1 , 1 , 4 , 0 , 80 , (3, 0, None, None) , 0 , )),
	(( 'EndEdit' , ), 1610678280, (1610678280, (), [ ], 1 , 1 , 4 , 0 , 88 , (3, 0, None, None) , 0 , )),
	(( 'GetLoftPoint' , 'x' , 'y' , ), 1610678281, (1610678281, (), [ (16389, 0, None, None) , 
			 (16389, 0, None, None) , ], 1 , 1 , 4 , 0 , 96 , (3, 0, None, None) , 0 , )),
	(( 'SetLoftPoint' , 'x' , 'y' , ), 1610678282, (1610678282, (), [ (5, 0, None, None) , 
			 (5, 0, None, None) , ], 1 , 1 , 4 , 0 , 104 , (3, 0, None, None) , 0 , )),
	(( 'AddProjectionOf' , 'entity' , ), 1610678283, (1610678283, (), [ (13, 0, None, "IID('{7AA0E540-0301-11D4-A30E-00C026EE094F}')") , ], 1 , 1 , 4 , 0 , 112 , (3, 0, None, None) , 0 , )),
	(( 'GetSurface' , ), 1610678284, (1610678284, (), [ ], 1 , 1 , 4 , 0 , 120 , (13, 0, None, IID('{081C7F2D-D5BC-40A6-92FE-C16B67D10B75}')) , 0 , )),
	(( 'BeginEditEx' , 'readOnly' , ), 1610678285, (1610678285, (), [ (3, 0, None, None) , ], 1 , 1 , 4 , 0 , 128 , (3, 0, None, None) , 0 , )),
]

ISpecification3D_vtables_dispatch_ = 0
ISpecification3D_vtables_ = [
	(( 'SpcIncludePart' , 'part' , 'fillTexts' , ), 1610678272, (1610678272, (), [ (13, 0, None, "IID('{7AA0E540-0300-11D4-A30E-00C026EE094F}')") , 
			 (3, 0, None, None) , ], 1 , 1 , 4 , 0 , 24 , (3, 0, None, None) , 0 , )),
	(( 'GetSpcObjForGeomWithLimit' , 'nameLib' , 'numb' , 'part' , 'First' , 
			 'section' , 'attrTypeNumb' , ), 1610678273, (1610678273, (), [ (31, 0, None, None) , (3, 0, None, None) , 
			 (13, 0, None, "IID('{7AA0E540-0300-11D4-A30E-00C026EE094F}')") , (2, 0, None, None) , (2, 0, None, None) , (5, 0, None, None) , ], 1 , 1 , 4 , 0 , 32 , (3, 0, None, None) , 0 , )),
	(( 'D3GetSpcObjGeometry' , 'spcObj' , ), 1610678274, (1610678274, (), [ (3, 0, None, None) , ], 1 , 1 , 4 , 0 , 40 , (13, 0, None, IID('{7AA0E540-0300-11D4-A30E-00C026EE094F}')) , 0 , )),
]

ISphereParam_vtables_dispatch_ = 0
ISphereParam_vtables_ = [
	(( 'GetRadius' , ), 1610678272, (1610678272, (), [ ], 1 , 1 , 4 , 0 , 24 , (5, 0, None, None) , 0 , )),
	(( 'GetPlacement' , ), 1610678273, (1610678273, (), [ ], 1 , 1 , 4 , 0 , 32 , (13, 0, None, IID('{7AA0E540-0310-11D4-A30E-00C026EE094F}')) , 0 , )),
]

ISplineDefinition_vtables_dispatch_ = 0
ISplineDefinition_vtables_ = [
	(( 'GetCountVertex' , ), 1610678272, (1610678272, (), [ ], 1 , 1 , 4 , 0 , 24 , (3, 0, None, None) , 0 , )),
	(( 'AddVertex' , 'x' , 'y' , 'z' , 'radius' , 
			 ), 1610678273, (1610678273, (), [ (5, 0, None, None) , (5, 0, None, None) , (5, 0, None, None) , (5, 0, None, None) , ], 1 , 1 , 4 , 0 , 32 , (3, 0, None, None) , 0 , )),
	(( 'InsertVertex' , 'index' , 'x' , 'y' , 'z' , 
			 'radius' , ), 1610678274, (1610678274, (), [ (3, 0, None, None) , (5, 0, None, None) , (5, 0, None, None) , 
			 (5, 0, None, None) , (5, 0, None, None) , ], 1 , 1 , 4 , 0 , 40 , (3, 0, None, None) , 0 , )),
	(( 'DeleteVertex' , 'index' , ), 1610678275, (1610678275, (), [ (3, 0, None, None) , ], 1 , 1 , 4 , 0 , 48 , (3, 0, None, None) , 0 , )),
	(( 'GetParamVertex' , 'index' , 'x' , 'y' , 'z' , 
			 'weight' , ), 1610678276, (1610678276, (), [ (3, 0, None, None) , (16389, 0, None, None) , (16389, 0, None, None) , 
			 (16389, 0, None, None) , (16389, 0, None, None) , ], 1 , 1 , 4 , 0 , 56 , (3, 0, None, None) , 0 , )),
	(( 'Flush' , ), 1610678277, (1610678277, (), [ ], 1 , 1 , 4 , 0 , 64 , (3, 0, None, None) , 0 , )),
	(( 'SetClosed' , 'cls' , ), 1610678278, (1610678278, (), [ (3, 0, None, None) , ], 1 , 1 , 4 , 0 , 72 , (3, 0, None, None) , 0 , )),
	(( 'GetClosed' , ), 1610678279, (1610678279, (), [ ], 1 , 1 , 4 , 0 , 80 , (3, 0, None, None) , 0 , )),
	(( 'ReadFromFile' , 'fileName' , ), 1610678280, (1610678280, (), [ (31, 0, None, None) , ], 1 , 1 , 4 , 0 , 88 , (3, 0, None, None) , 0 , )),
	(( 'WriteToFile' , 'fileName' , ), 1610678281, (1610678281, (), [ (31, 0, None, None) , ], 1 , 1 , 4 , 0 , 96 , (3, 0, None, None) , 0 , )),
	(( 'SetSplineOnPoles' , 'splineOnPoles' , ), 1610678282, (1610678282, (), [ (3, 0, None, None) , ], 1 , 1 , 4 , 0 , 104 , (3, 0, None, None) , 0 , )),
	(( 'GetSplineOnPoles' , ), 1610678283, (1610678283, (), [ ], 1 , 1 , 4 , 0 , 112 , (3, 0, None, None) , 0 , )),
	(( 'SetDegree' , 'degree' , ), 1610678284, (1610678284, (), [ (3, 0, None, None) , ], 1 , 1 , 4 , 0 , 120 , (3, 0, None, None) , 0 , )),
	(( 'GetDegree' , ), 1610678285, (1610678285, (), [ ], 1 , 1 , 4 , 0 , 128 , (3, 0, None, None) , 0 , )),
	(( 'AddVertexAndAssociation' , 'index' , 'obj' , 'weight' , ), 1610678286, (1610678286, (), [ 
			 (3, 0, None, None) , (13, 0, None, "IID('{7AA0E540-0301-11D4-A30E-00C026EE094F}')") , (5, 0, None, None) , ], 1 , 1 , 4 , 0 , 136 , (3, 0, None, None) , 0 , )),
	(( 'SetAssociation' , 'index' , 'obj' , ), 1610678287, (1610678287, (), [ (3, 0, None, None) , 
			 (13, 0, None, "IID('{7AA0E540-0301-11D4-A30E-00C026EE094F}')") , ], 1 , 1 , 4 , 0 , 144 , (3, 0, None, None) , 0 , )),
	(( 'GetAssociation' , 'index' , ), 1610678288, (1610678288, (), [ (3, 0, None, None) , ], 1 , 1 , 4 , 0 , 152 , (13, 0, None, IID('{7AA0E540-0301-11D4-A30E-00C026EE094F}')) , 0 , )),
]

ISurface_vtables_dispatch_ = 0
ISurface_vtables_ = [
	(( 'GetGabarit' , 'x1' , 'y1' , 'z1' , 'x2' , 
			 'y2' , 'z2' , ), 1610678272, (1610678272, (), [ (16389, 0, None, None) , (16389, 0, None, None) , 
			 (16389, 0, None, None) , (16389, 0, None, None) , (16389, 0, None, None) , (16389, 0, None, None) , ], 1 , 1 , 4 , 0 , 24 , (3, 0, None, None) , 0 , )),
	(( 'GetPoint' , 'paramU' , 'paramV' , 'x' , 'y' , 
			 'z' , ), 1610678273, (1610678273, (), [ (5, 0, None, None) , (5, 0, None, None) , (16389, 0, None, None) , 
			 (16389, 0, None, None) , (16389, 0, None, None) , ], 1 , 1 , 4 , 0 , 32 , (3, 0, None, None) , 0 , )),
	(( 'GetNormal' , 'paramU' , 'paramV' , 'x' , 'y' , 
			 'z' , ), 1610678274, (1610678274, (), [ (5, 0, None, None) , (5, 0, None, None) , (16389, 0, None, None) , 
			 (16389, 0, None, None) , (16389, 0, None, None) , ], 1 , 1 , 4 , 0 , 40 , (3, 0, None, None) , 0 , )),
	(( 'GetTangentVectorU' , 'paramU' , 'paramV' , 'x' , 'y' , 
			 'z' , ), 1610678275, (1610678275, (), [ (5, 0, None, None) , (5, 0, None, None) , (16389, 0, None, None) , 
			 (16389, 0, None, None) , (16389, 0, None, None) , ], 1 , 1 , 4 , 0 , 48 , (3, 0, None, None) , 0 , )),
	(( 'GetTangentVectorV' , 'paramU' , 'paramV' , 'x' , 'y' , 
			 'z' , ), 1610678276, (1610678276, (), [ (5, 0, None, None) , (5, 0, None, None) , (16389, 0, None, None) , 
			 (16389, 0, None, None) , (16389, 0, None, None) , ], 1 , 1 , 4 , 0 , 56 , (3, 0, None, None) , 0 , )),
	(( 'GetDerivativeU' , 'paramU' , 'paramV' , 'x' , 'y' , 
			 'z' , ), 1610678277, (1610678277, (), [ (5, 0, None, None) , (5, 0, None, None) , (16389, 0, None, None) , 
			 (16389, 0, None, None) , (16389, 0, None, None) , ], 1 , 1 , 4 , 0 , 64 , (3, 0, None, None) , 0 , )),
	(( 'GetDerivativeV' , 'paramU' , 'paramV' , 'x' , 'y' , 
			 'z' , ), 1610678278, (1610678278, (), [ (5, 0, None, None) , (5, 0, None, None) , (16389, 0, None, None) , 
			 (16389, 0, None, None) , (16389, 0, None, None) , ], 1 , 1 , 4 , 0 , 72 , (3, 0, None, None) , 0 , )),
	(( 'GetDerivativeUU' , 'paramU' , 'paramV' , 'x' , 'y' , 
			 'z' , ), 1610678279, (1610678279, (), [ (5, 0, None, None) , (5, 0, None, None) , (16389, 0, None, None) , 
			 (16389, 0, None, None) , (16389, 0, None, None) , ], 1 , 1 , 4 , 0 , 80 , (3, 0, None, None) , 0 , )),
	(( 'GetDerivativeVV' , 'paramU' , 'paramV' , 'x' , 'y' , 
			 'z' , ), 1610678280, (1610678280, (), [ (5, 0, None, None) , (5, 0, None, None) , (16389, 0, None, None) , 
			 (16389, 0, None, None) , (16389, 0, None, None) , ], 1 , 1 , 4 , 0 , 88 , (3, 0, None, None) , 0 , )),
	(( 'GetDerivativeUV' , 'paramU' , 'paramV' , 'x' , 'y' , 
			 'z' , ), 1610678281, (1610678281, (), [ (5, 0, None, None) , (5, 0, None, None) , (16389, 0, None, None) , 
			 (16389, 0, None, None) , (16389, 0, None, None) , ], 1 , 1 , 4 , 0 , 96 , (3, 0, None, None) , 0 , )),
	(( 'GetDerivativeUUU' , 'paramU' , 'paramV' , 'x' , 'y' , 
			 'z' , ), 1610678282, (1610678282, (), [ (5, 0, None, None) , (5, 0, None, None) , (16389, 0, None, None) , 
			 (16389, 0, None, None) , (16389, 0, None, None) , ], 1 , 1 , 4 , 0 , 104 , (3, 0, None, None) , 0 , )),
	(( 'GetDerivativeVVV' , 'paramU' , 'paramV' , 'x' , 'y' , 
			 'z' , ), 1610678283, (1610678283, (), [ (5, 0, None, None) , (5, 0, None, None) , (16389, 0, None, None) , 
			 (16389, 0, None, None) , (16389, 0, None, None) , ], 1 , 1 , 4 , 0 , 112 , (3, 0, None, None) , 0 , )),
	(( 'GetDerivativeUVV' , 'paramU' , 'paramV' , 'x' , 'y' , 
			 'z' , ), 1610678284, (1610678284, (), [ (5, 0, None, None) , (5, 0, None, None) , (16389, 0, None, None) , 
			 (16389, 0, None, None) , (16389, 0, None, None) , ], 1 , 1 , 4 , 0 , 120 , (3, 0, None, None) , 0 , )),
	(( 'GetDerivativeUUV' , 'paramU' , 'paramV' , 'x' , 'y' , 
			 'z' , ), 1610678285, (1610678285, (), [ (5, 0, None, None) , (5, 0, None, None) , (16389, 0, None, None) , 
			 (16389, 0, None, None) , (16389, 0, None, None) , ], 1 , 1 , 4 , 0 , 128 , (3, 0, None, None) , 0 , )),
	(( 'GetParamUMin' , ), 1610678286, (1610678286, (), [ ], 1 , 1 , 4 , 0 , 136 , (5, 0, None, None) , 0 , )),
	(( 'GetParamUMax' , ), 1610678287, (1610678287, (), [ ], 1 , 1 , 4 , 0 , 144 , (5, 0, None, None) , 0 , )),
	(( 'GetParamVMin' , ), 1610678288, (1610678288, (), [ ], 1 , 1 , 4 , 0 , 152 , (5, 0, None, None) , 0 , )),
	(( 'GetParamVMax' , ), 1610678289, (1610678289, (), [ ], 1 , 1 , 4 , 0 , 160 , (5, 0, None, None) , 0 , )),
	(( 'IsClosedU' , ), 1610678290, (1610678290, (), [ ], 1 , 1 , 4 , 0 , 168 , (3, 0, None, None) , 0 , )),
	(( 'IsClosedV' , ), 1610678291, (1610678291, (), [ ], 1 , 1 , 4 , 0 , 176 , (3, 0, None, None) , 0 , )),
	(( 'IsPlane' , ), 1610678292, (1610678292, (), [ ], 1 , 1 , 4 , 0 , 184 , (3, 0, None, None) , 0 , )),
	(( 'IsCone' , ), 1610678293, (1610678293, (), [ ], 1 , 1 , 4 , 0 , 192 , (3, 0, None, None) , 0 , )),
	(( 'IsCylinder' , ), 1610678294, (1610678294, (), [ ], 1 , 1 , 4 , 0 , 200 , (3, 0, None, None) , 0 , )),
	(( 'IsTorus' , ), 1610678295, (1610678295, (), [ ], 1 , 1 , 4 , 0 , 208 , (3, 0, None, None) , 0 , )),
	(( 'IsSphere' , ), 1610678296, (1610678296, (), [ ], 1 , 1 , 4 , 0 , 216 , (3, 0, None, None) , 0 , )),
	(( 'IsNurbsSurface' , ), 1610678297, (1610678297, (), [ ], 1 , 1 , 4 , 0 , 224 , (3, 0, None, None) , 0 , )),
	(( 'IsRevolved' , ), 1610678298, (1610678298, (), [ ], 1 , 1 , 4 , 0 , 232 , (3, 0, None, None) , 0 , )),
	(( 'IsSwept' , ), 1610678299, (1610678299, (), [ ], 1 , 1 , 4 , 0 , 240 , (3, 0, None, None) , 0 , )),
	(( 'GetSurfaceParam' , ), 1610678300, (1610678300, (), [ ], 1 , 1 , 4 , 0 , 248 , (13, 0, None, None) , 0 , )),
	(( 'GetArea' , 'bitVector' , ), 1610678301, (1610678301, (), [ (19, 0, None, None) , ], 1 , 1 , 4 , 0 , 256 , (5, 0, None, None) , 0 , )),
	(( 'NearPointProjection' , 'x' , 'y' , 'z' , 'u' , 
			 'v' , 'ext' , ), 1610678302, (1610678302, (), [ (5, 1, None, None) , (5, 1, None, None) , 
			 (5, 1, None, None) , (16389, 2, None, None) , (16389, 2, None, None) , (3, 1, None, None) , ], 1 , 1 , 4 , 0 , 264 , (3, 0, None, None) , 0 , )),
	(( 'CurveIntersection' , 'curve' , 'pointsArr' , 'extSurf' , 'extCurve' , 
			 ), 1610678303, (1610678303, (), [ (13, 0, None, "IID('{E5066490-773D-4289-A60B-2FC19865174A}')") , (13, 0, None, "IID('{A5E6E83E-1F33-4EAF-BAFC-A3F434F23BAA}')") , (3, 0, None, None) , (3, 0, None, None) , ], 1 , 1 , 4 , 0 , 272 , (3, 0, None, None) , 0 , )),
	(( 'GetNurbsSurfaceParam' , ), 1610678304, (1610678304, (), [ ], 1 , 1 , 4 , 0 , 280 , (13, 0, None, IID('{A5A1CB44-5F2E-4059-86B3-4F5056EFF956}')) , 0 , )),
	(( 'GetBoundaryUVNurbs' , 'uv' , 'closed' , 'loopIndex' , 'edgeIndex' , 
			 'degree' , 'points' , 'weights' , 'knots' , 'tMin' , 
			 'tMax' , ), 1610678305, (1610678305, (), [ (3, 1, None, None) , (3, 1, None, None) , (3, 1, None, None) , 
			 (3, 1, None, None) , (16387, 2, None, None) , (16396, 2, None, None) , (16396, 2, None, None) , (16396, 2, None, None) , 
			 (16389, 2, None, None) , (16389, 2, None, None) , ], 1 , 1 , 4 , 0 , 288 , (3, 0, None, None) , 0 , )),
	(( 'GetBoundaryCount' , ), 1610678306, (1610678306, (), [ ], 1 , 1 , 4 , 0 , 296 , (3, 0, None, None) , 0 , )),
	(( 'GetEdgesCount' , 'loopIndex' , ), 1610678307, (1610678307, (), [ (3, 0, None, None) , ], 1 , 1 , 4 , 0 , 304 , (3, 0, None, None) , 0 , )),
]

ITessellation_vtables_dispatch_ = 0
ITessellation_vtables_ = [
	(( 'GetFacetsCount' , ), 1610678272, (1610678272, (), [ ], 1 , 1 , 4 , 0 , 24 , (3, 0, None, None) , 0 , )),
	(( 'GetFacetData' , 'index' , 'facet' , ), 1610678273, (1610678273, (), [ (3, 0, None, None) , 
			 (13, 0, None, "IID('{1EED6C22-25D4-49C6-B76A-90B768966A3B}')") , ], 1 , 1 , 4 , 0 , 32 , (3, 0, None, None) , 0 , )),
	(( 'GetPointsCount' , ), 1610678274, (1610678274, (), [ ], 1 , 1 , 4 , 0 , 40 , (3, 0, None, None) , 0 , )),
	(( 'GetPoint' , 'index' , 'x' , 'y' , 'z' , 
			 ), 1610678275, (1610678275, (), [ (3, 1, None, None) , (16388, 2, None, None) , (16388, 2, None, None) , (16388, 2, None, None) , ], 1 , 1 , 4 , 0 , 48 , (3, 0, None, None) , 0 , )),
	(( 'GetNormal' , 'index' , 'x' , 'y' , 'z' , 
			 ), 1610678276, (1610678276, (), [ (3, 1, None, None) , (16388, 2, None, None) , (16388, 2, None, None) , (16388, 2, None, None) , ], 1 , 1 , 4 , 0 , 56 , (3, 0, None, None) , 0 , )),
	(( 'SetFacetSize' , 'sag' , ), 1610678277, (1610678277, (), [ (5, 0, None, None) , ], 1 , 1 , 4 , 0 , 64 , (3, 0, None, None) , 0 , )),
	(( 'GetFacetSize' , ), 1610678278, (1610678278, (), [ ], 1 , 1 , 4 , 0 , 72 , (5, 0, None, None) , 0 , )),
	(( 'GetFacet' , ), 1610678279, (1610678279, (), [ ], 1 , 1 , 4 , 0 , 80 , (13, 0, None, IID('{1EED6C22-25D4-49C6-B76A-90B768966A3B}')) , 0 , )),
	(( 'Refresh' , ), 1610678280, (1610678280, (), [ ], 1 , 1 , 4 , 0 , 88 , (3, 0, None, None) , 0 , )),
	(( 'GetFacetPoints' , 'points' , 'indexes' , ), 1610678281, (1610678281, (), [ (16396, 2, None, None) , 
			 (16396, 2, None, None) , ], 1 , 1 , 4 , 0 , 96 , (3, 0, None, None) , 0 , )),
	(( 'GetFacetNormals' , 'normals' , ), 1610678282, (1610678282, (), [ (16396, 2, None, None) , ], 1 , 1 , 4 , 0 , 104 , (3, 0, None, None) , 0 , )),
	(( 'GetFacetParams' , 'params' , ), 1610678283, (1610678283, (), [ (16396, 2, None, None) , ], 1 , 1 , 4 , 0 , 112 , (3, 0, None, None) , 0 , )),
	(( 'SetFacetSag' , 'sag' , ), 1610678284, (1610678284, (), [ (5, 0, None, None) , ], 1 , 1 , 4 , 0 , 120 , (3, 0, None, None) , 0 , )),
	(( 'GetFacetSag' , ), 1610678285, (1610678285, (), [ ], 1 , 1 , 4 , 0 , 128 , (5, 0, None, None) , 0 , )),
	(( 'SetFacetAngle' , 'angle' , ), 1610678286, (1610678286, (), [ (5, 0, None, None) , ], 1 , 1 , 4 , 0 , 136 , (3, 0, None, None) , 0 , )),
	(( 'GetFacetAngle' , ), 1610678287, (1610678287, (), [ ], 1 , 1 , 4 , 0 , 144 , (5, 0, None, None) , 0 , )),
	(( 'SetNeedParams' , 'need' , ), 1610678288, (1610678288, (), [ (3, 0, None, None) , ], 1 , 1 , 4 , 0 , 152 , (3, 0, None, None) , 0 , )),
	(( 'GetNeedParams' , ), 1610678289, (1610678289, (), [ ], 1 , 1 , 4 , 0 , 160 , (3, 0, None, None) , 0 , )),
]

IThinParam_vtables_dispatch_ = 0
IThinParam_vtables_ = [
	(( 'GetThin' , ), 1610678272, (1610678272, (), [ ], 1 , 1 , 4 , 0 , 24 , (3, 0, None, None) , 0 , )),
	(( 'SetThin' , 'val' , ), 1610678273, (1610678273, (), [ (3, 0, None, None) , ], 1 , 1 , 4 , 0 , 32 , (3, 0, None, None) , 0 , )),
	(( 'GetThinType' , ), 1610678274, (1610678274, (), [ ], 1 , 1 , 4 , 0 , 40 , (17, 0, None, None) , 0 , )),
	(( 'SetThinType' , 'val' , ), 1610678275, (1610678275, (), [ (17, 0, None, None) , ], 1 , 1 , 4 , 0 , 48 , (3, 0, None, None) , 0 , )),
	(( 'GetNormalThickness' , ), 1610678276, (1610678276, (), [ ], 1 , 1 , 4 , 0 , 56 , (5, 0, None, None) , 0 , )),
	(( 'SetNormalThickness' , 'val' , ), 1610678277, (1610678277, (), [ (5, 0, None, None) , ], 1 , 1 , 4 , 0 , 64 , (3, 0, None, None) , 0 , )),
	(( 'GetReverseThickness' , ), 1610678278, (1610678278, (), [ ], 1 , 1 , 4 , 0 , 72 , (5, 0, None, None) , 0 , )),
	(( 'SetReverseThickness' , 'val' , ), 1610678279, (1610678279, (), [ (5, 0, None, None) , ], 1 , 1 , 4 , 0 , 80 , (3, 0, None, None) , 0 , )),
]

IThreadDefinition_vtables_dispatch_ = 0
IThreadDefinition_vtables_ = [
	(( 'GetDr' , ), 1610678272, (1610678272, (), [ ], 1 , 1 , 4 , 0 , 24 , (5, 0, None, None) , 0 , )),
	(( 'SetDr' , 'dr' , ), 1610678273, (1610678273, (), [ (5, 0, None, None) , ], 1 , 1 , 4 , 0 , 32 , (3, 0, None, None) , 0 , )),
	(( 'GetLength' , ), 1610678274, (1610678274, (), [ ], 1 , 1 , 4 , 0 , 40 , (5, 0, None, None) , 0 , )),
	(( 'SetLength' , 'length' , ), 1610678275, (1610678275, (), [ (5, 0, None, None) , ], 1 , 1 , 4 , 0 , 48 , (3, 0, None, None) , 0 , )),
	(( 'GetP' , ), 1610678276, (1610678276, (), [ ], 1 , 1 , 4 , 0 , 56 , (5, 0, None, None) , 0 , )),
	(( 'SetP' , 'p' , ), 1610678277, (1610678277, (), [ (5, 0, None, None) , ], 1 , 1 , 4 , 0 , 64 , (3, 0, None, None) , 0 , )),
	(( 'GetOutside' , ), 1610678278, (1610678278, (), [ ], 1 , 1 , 4 , 0 , 72 , (3, 0, None, None) , 0 , )),
	(( 'GetAutoDefinDr' , ), 1610678279, (1610678279, (), [ ], 1 , 1 , 4 , 0 , 80 , (3, 0, None, None) , 0 , )),
	(( 'SetAutoDefinDr' , 'autoDefinDr' , ), 1610678280, (1610678280, (), [ (3, 0, None, None) , ], 1 , 1 , 4 , 0 , 88 , (3, 0, None, None) , 0 , )),
	(( 'GetAllLength' , ), 1610678281, (1610678281, (), [ ], 1 , 1 , 4 , 0 , 96 , (3, 0, None, None) , 0 , )),
	(( 'SetAllLength' , 'allLength' , ), 1610678282, (1610678282, (), [ (3, 0, None, None) , ], 1 , 1 , 4 , 0 , 104 , (3, 0, None, None) , 0 , )),
	(( 'GetFaceValue' , ), 1610678283, (1610678283, (), [ ], 1 , 1 , 4 , 0 , 112 , (3, 0, None, None) , 0 , )),
	(( 'SetFaceValue' , 'faceValue' , ), 1610678284, (1610678284, (), [ (3, 0, None, None) , ], 1 , 1 , 4 , 0 , 120 , (3, 0, None, None) , 0 , )),
	(( 'GetBaseObject' , ), 1610678285, (1610678285, (), [ ], 1 , 1 , 4 , 0 , 128 , (13, 0, None, IID('{7AA0E540-0301-11D4-A30E-00C026EE094F}')) , 0 , )),
	(( 'SetBaseObject' , 'obj' , ), 1610678286, (1610678286, (), [ (13, 0, None, "IID('{7AA0E540-0301-11D4-A30E-00C026EE094F}')") , ], 1 , 1 , 4 , 0 , 136 , (3, 0, None, None) , 0 , )),
	(( 'GetFaceBegin' , ), 1610678287, (1610678287, (), [ ], 1 , 1 , 4 , 0 , 144 , (13, 0, None, IID('{7AA0E540-0301-11D4-A30E-00C026EE094F}')) , 0 , )),
	(( 'SetFaceBegin' , 'face' , ), 1610678288, (1610678288, (), [ (13, 0, None, "IID('{7AA0E540-0301-11D4-A30E-00C026EE094F}')") , ], 1 , 1 , 4 , 0 , 152 , (3, 0, None, None) , 0 , )),
	(( 'GetFaceEnd' , ), 1610678289, (1610678289, (), [ ], 1 , 1 , 4 , 0 , 160 , (13, 0, None, IID('{7AA0E540-0301-11D4-A30E-00C026EE094F}')) , 0 , )),
	(( 'SetFaceEnd' , 'face' , ), 1610678290, (1610678290, (), [ (13, 0, None, "IID('{7AA0E540-0301-11D4-A30E-00C026EE094F}')") , ], 1 , 1 , 4 , 0 , 168 , (3, 0, None, None) , 0 , )),
]

ITorusParam_vtables_dispatch_ = 0
ITorusParam_vtables_ = [
	(( 'GetRadius' , ), 1610678272, (1610678272, (), [ ], 1 , 1 , 4 , 0 , 24 , (5, 0, None, None) , 0 , )),
	(( 'GetGeneratrixRadius' , ), 1610678273, (1610678273, (), [ ], 1 , 1 , 4 , 0 , 32 , (5, 0, None, None) , 0 , )),
	(( 'GetPlacement' , ), 1610678274, (1610678274, (), [ ], 1 , 1 , 4 , 0 , 40 , (13, 0, None, IID('{7AA0E540-0310-11D4-A30E-00C026EE094F}')) , 0 , )),
]

IUnionComponentsDefinition_vtables_dispatch_ = 0
IUnionComponentsDefinition_vtables_ = [
	(( 'PartArray' , ), 1610678272, (1610678272, (), [ ], 1 , 1 , 4 , 0 , 24 , (13, 0, None, IID('{7AA0E540-0317-11D4-A30E-00C026EE094F}')) , 0 , )),
]

IVariable_vtables_dispatch_ = 0
IVariable_vtables_ = [
	(( 'GetName' , ), 1610678272, (1610678272, (), [ ], 1 , 1 , 4 , 0 , 24 , (31, 0, None, None) , 0 , )),
	(( 'GetNote' , ), 1610678273, (1610678273, (), [ ], 1 , 1 , 4 , 0 , 32 , (31, 0, None, None) , 0 , )),
	(( 'SetNote' , 'note' , ), 1610678274, (1610678274, (), [ (31, 0, None, None) , ], 1 , 1 , 4 , 0 , 40 , (3, 0, None, None) , 0 , )),
	(( 'GetValue' , ), 1610678275, (1610678275, (), [ ], 1 , 1 , 4 , 0 , 48 , (5, 0, None, None) , 0 , )),
	(( 'SetValue' , 'val' , ), 1610678276, (1610678276, (), [ (5, 0, None, None) , ], 1 , 1 , 4 , 0 , 56 , (3, 0, None, None) , 0 , )),
	(( 'GetParam' , ), 1610678277, (1610678277, (), [ ], 1 , 1 , 4 , 0 , 64 , (16408, 0, None, None) , 0 , )),
	(( 'GetPseudonym' , ), 1610678278, (1610678278, (), [ ], 1 , 1 , 4 , 0 , 72 , (31, 0, None, None) , 0 , )),
	(( 'SetPseudonym' , 'val' , ), 1610678279, (1610678279, (), [ (31, 0, None, None) , ], 1 , 1 , 4 , 0 , 80 , (3, 0, None, None) , 0 , )),
	(( 'GetExpression' , ), 1610678280, (1610678280, (), [ ], 1 , 1 , 4 , 0 , 88 , (31, 0, None, None) , 0 , )),
	(( 'SetExpression' , 'exp' , ), 1610678281, (1610678281, (), [ (31, 0, None, None) , ], 1 , 1 , 4 , 0 , 96 , (3, 0, None, None) , 0 , )),
	(( 'GetExternal' , ), 1610678282, (1610678282, (), [ ], 1 , 1 , 4 , 0 , 104 , (3, 0, None, None) , 0 , )),
	(( 'SetExternal' , 'fVal' , ), 1610678283, (1610678283, (), [ (3, 0, None, None) , ], 1 , 1 , 4 , 0 , 112 , (3, 0, None, None) , 0 , )),
	(( 'GetParameterNote' , ), 1610678284, (1610678284, (), [ ], 1 , 1 , 4 , 0 , 120 , (31, 0, None, None) , 0 , )),
	(( 'GetLinkVarName' , ), 1610678285, (1610678285, (), [ ], 1 , 1 , 4 , 0 , 128 , (31, 0, None, None) , 0 , )),
	(( 'GetLinkDocName' , ), 1610678286, (1610678286, (), [ ], 1 , 1 , 4 , 0 , 136 , (31, 0, None, None) , 0 , )),
	(( 'SetLink' , 'doc' , 'name' , ), 1610678287, (1610678287, (), [ (31, 0, None, None) , 
			 (31, 0, None, None) , ], 1 , 1 , 4 , 0 , 144 , (3, 0, None, None) , 0 , )),
	(( 'GetDisplayName' , ), 1610678288, (1610678288, (), [ ], 1 , 1 , 4 , 0 , 152 , (31, 0, None, None) , 0 , )),
	(( 'GetInformation' , ), 1610678289, (1610678289, (), [ ], 1 , 1 , 4 , 0 , 160 , (3, 0, None, None) , 0 , )),
	(( 'SetInformation' , 'fVal' , ), 1610678290, (1610678290, (), [ (3, 0, None, None) , ], 1 , 1 , 4 , 0 , 168 , (3, 0, None, None) , 0 , )),
]

IVariableCollection_vtables_dispatch_ = 0
IVariableCollection_vtables_ = [
	(( 'Refresh' , ), 1610678272, (1610678272, (), [ ], 1 , 1 , 4 , 0 , 24 , (3, 0, None, None) , 0 , )),
	(( 'GetCount' , ), 1610678273, (1610678273, (), [ ], 1 , 1 , 4 , 0 , 32 , (3, 0, None, None) , 0 , )),
	(( 'First' , ), 1610678274, (1610678274, (), [ ], 1 , 1 , 4 , 0 , 40 , (13, 0, None, IID('{7AA0E540-0312-11D4-A30E-00C026EE094F}')) , 0 , )),
	(( 'Last' , ), 1610678275, (1610678275, (), [ ], 1 , 1 , 4 , 0 , 48 , (13, 0, None, IID('{7AA0E540-0312-11D4-A30E-00C026EE094F}')) , 0 , )),
	(( 'Next' , ), 1610678276, (1610678276, (), [ ], 1 , 1 , 4 , 0 , 56 , (13, 0, None, IID('{7AA0E540-0312-11D4-A30E-00C026EE094F}')) , 0 , )),
	(( 'Prev' , ), 1610678277, (1610678277, (), [ ], 1 , 1 , 4 , 0 , 64 , (13, 0, None, IID('{7AA0E540-0312-11D4-A30E-00C026EE094F}')) , 0 , )),
	(( 'GetByIndex' , 'index' , ), 1610678278, (1610678278, (), [ (3, 0, None, None) , ], 1 , 1 , 4 , 0 , 72 , (13, 0, None, IID('{7AA0E540-0312-11D4-A30E-00C026EE094F}')) , 0 , )),
	(( 'GetByName' , 'name' , 'testFullName' , 'testIgnoreCase' , ), 1610678279, (1610678279, (), [ 
			 (31, 0, None, None) , (3, 0, None, None) , (3, 0, None, None) , ], 1 , 1 , 4 , 0 , 80 , (13, 0, None, IID('{7AA0E540-0312-11D4-A30E-00C026EE094F}')) , 0 , )),
	(( 'AddNewVariable' , 'name' , 'value' , 'note' , ), 1610678280, (1610678280, (), [ 
			 (31, 0, None, None) , (5, 0, None, None) , (31, 0, None, None) , ], 1 , 1 , 4 , 0 , 88 , (13, 0, None, IID('{7AA0E540-0312-11D4-A30E-00C026EE094F}')) , 0 , )),
	(( 'RemoveVariable' , 'name' , ), 1610678281, (1610678281, (), [ (31, 0, None, None) , ], 1 , 1 , 4 , 0 , 96 , (3, 0, None, None) , 0 , )),
]

IVertexDefinition_vtables_dispatch_ = 0
IVertexDefinition_vtables_ = [
	(( 'GetPoint' , 'x' , 'y' , 'z' , ), 1610678272, (1610678272, (), [ 
			 (16389, 0, None, None) , (16389, 0, None, None) , (16389, 0, None, None) , ], 1 , 1 , 4 , 0 , 24 , (3, 0, None, None) , 0 , )),
	(( 'GetOwnerEntity' , ), 1610678273, (1610678273, (), [ ], 1 , 1 , 4 , 0 , 32 , (13, 0, None, IID('{7AA0E540-0301-11D4-A30E-00C026EE094F}')) , 0 , )),
	(( 'GetTopologyVertex' , ), 1610678274, (1610678274, (), [ ], 1 , 1 , 4 , 0 , 40 , (3, 0, None, None) , 0 , )),
	(( 'GetFreeVertex' , ), 1610678275, (1610678275, (), [ ], 1 , 1 , 4 , 0 , 48 , (3, 0, None, None) , 0 , )),
	(( 'GetSketchVertex' , ), 1610678276, (1610678276, (), [ ], 1 , 1 , 4 , 0 , 56 , (3, 0, None, None) , 0 , )),
]

IViewProjection_vtables_dispatch_ = 0
IViewProjection_vtables_ = [
	(( 'IsCurrent' , ), 1610678272, (1610678272, (), [ ], 1 , 1 , 4 , 0 , 24 , (3, 0, None, None) , 0 , )),
	(( 'SetCurrent' , ), 1610678273, (1610678273, (), [ ], 1 , 1 , 4 , 0 , 32 , (3, 0, None, None) , 0 , )),
	(( 'GetName' , ), 1610678274, (1610678274, (), [ ], 1 , 1 , 4 , 0 , 40 , (31, 0, None, None) , 0 , )),
	(( 'SetName' , 'projName' , ), 1610678275, (1610678275, (), [ (31, 0, None, None) , ], 1 , 1 , 4 , 0 , 48 , (3, 0, None, None) , 0 , )),
	(( 'GetScale' , ), 1610678276, (1610678276, (), [ ], 1 , 1 , 4 , 0 , 56 , (5, 0, None, None) , 0 , )),
	(( 'SetScale' , 'scale' , ), 1610678277, (1610678277, (), [ (5, 0, None, None) , ], 1 , 1 , 4 , 0 , 64 , (3, 0, None, None) , 0 , )),
	(( 'GetPlacement' , ), 1610678278, (1610678278, (), [ ], 1 , 1 , 4 , 0 , 72 , (13, 0, None, IID('{7AA0E540-0310-11D4-A30E-00C026EE094F}')) , 0 , )),
	(( 'SetPlacement' , 'place' , ), 1610678279, (1610678279, (), [ (13, 0, None, "IID('{7AA0E540-0310-11D4-A30E-00C026EE094F}')") , ], 1 , 1 , 4 , 0 , 80 , (3, 0, None, None) , 0 , )),
	(( 'GetUserProjectionIndex' , ), 1610678280, (1610678280, (), [ ], 1 , 1 , 4 , 0 , 88 , (3, 0, None, None) , 0 , )),
	(( 'SetMatrix3D' , 'Matrix3D' , ), 1610678281, (1610678281, (), [ (12, 0, None, None) , ], 1 , 1 , 4 , 0 , 96 , (3, 0, None, None) , 0 , )),
	(( 'GetViewProjectonType' , ), 1610678282, (1610678282, (), [ ], 1 , 1 , 4 , 0 , 104 , (3, 0, None, None) , 0 , )),
]

IViewProjectionCollection_vtables_dispatch_ = 0
IViewProjectionCollection_vtables_ = [
	(( 'Refresh' , ), 1610678272, (1610678272, (), [ ], 1 , 1 , 4 , 0 , 24 , (3, 0, None, None) , 0 , )),
	(( 'GetCount' , ), 1610678273, (1610678273, (), [ ], 1 , 1 , 4 , 0 , 32 , (3, 0, None, None) , 0 , )),
	(( 'First' , ), 1610678274, (1610678274, (), [ ], 1 , 1 , 4 , 0 , 40 , (13, 0, None, IID('{737D35AF-C407-420D-9250-A2CBB416DCB9}')) , 0 , )),
	(( 'Last' , ), 1610678275, (1610678275, (), [ ], 1 , 1 , 4 , 0 , 48 , (13, 0, None, IID('{737D35AF-C407-420D-9250-A2CBB416DCB9}')) , 0 , )),
	(( 'Next' , ), 1610678276, (1610678276, (), [ ], 1 , 1 , 4 , 0 , 56 , (13, 0, None, IID('{737D35AF-C407-420D-9250-A2CBB416DCB9}')) , 0 , )),
	(( 'Prev' , ), 1610678277, (1610678277, (), [ ], 1 , 1 , 4 , 0 , 64 , (13, 0, None, IID('{737D35AF-C407-420D-9250-A2CBB416DCB9}')) , 0 , )),
	(( 'GetByIndex' , 'index' , ), 1610678278, (1610678278, (), [ (3, 0, None, None) , ], 1 , 1 , 4 , 0 , 72 , (13, 0, None, IID('{737D35AF-C407-420D-9250-A2CBB416DCB9}')) , 0 , )),
	(( 'GetByName' , 'projName' , 'testFullName' , 'testIgnoreCase' , ), 1610678279, (1610678279, (), [ 
			 (31, 0, None, None) , (3, 0, None, None) , (3, 0, None, None) , ], 1 , 1 , 4 , 0 , 80 , (13, 0, None, IID('{737D35AF-C407-420D-9250-A2CBB416DCB9}')) , 0 , )),
	(( 'FindIt' , 'projection' , ), 1610678280, (1610678280, (), [ (13, 0, None, "IID('{737D35AF-C407-420D-9250-A2CBB416DCB9}')") , ], 1 , 1 , 4 , 0 , 88 , (3, 0, None, None) , 0 , )),
	(( 'Add' , 'projection' , ), 1610678281, (1610678281, (), [ (13, 0, None, "IID('{737D35AF-C407-420D-9250-A2CBB416DCB9}')") , ], 1 , 1 , 4 , 0 , 96 , (3, 0, None, None) , 0 , )),
	(( 'DetachByIndex' , 'index' , ), 1610678282, (1610678282, (), [ (3, 0, None, None) , ], 1 , 1 , 4 , 0 , 104 , (3, 0, None, None) , 0 , )),
	(( 'DetachByBody' , 'projection' , ), 1610678283, (1610678283, (), [ (13, 0, None, "IID('{737D35AF-C407-420D-9250-A2CBB416DCB9}')") , ], 1 , 1 , 4 , 0 , 112 , (3, 0, None, None) , 0 , )),
	(( 'DetachByName' , 'projName' , ), 1610678284, (1610678284, (), [ (31, 0, None, None) , ], 1 , 1 , 4 , 0 , 120 , (3, 0, None, None) , 0 , )),
	(( 'NewViewProjection' , ), 1610678285, (1610678285, (), [ ], 1 , 1 , 4 , 0 , 128 , (13, 0, None, IID('{737D35AF-C407-420D-9250-A2CBB416DCB9}')) , 0 , )),
	(( 'GetViewProjectionScheme' , ), 1610678286, (1610678286, (), [ ], 1 , 1 , 4 , 0 , 136 , (3, 0, None, None) , 0 , )),
	(( 'SetViewProjectionScheme' , 'scheme' , ), 1610678287, (1610678287, (), [ (3, 0, None, None) , ], 1 , 1 , 4 , 0 , 144 , (3, 0, None, None) , 0 , )),
	(( 'SetBaseUserOrientation' , 'place' , ), 1610678288, (1610678288, (), [ (16396, 0, None, None) , ], 1 , 1 , 4 , 0 , 152 , (3, 0, None, None) , 0 , )),
	(( 'GetBaseUserOrientation' , 'place' , ), 1610678289, (1610678289, (), [ (16396, 0, None, None) , ], 1 , 1 , 4 , 0 , 160 , (3, 0, None, None) , 0 , )),
	(( 'AddUnfoldProjection' , 'place' , ), 1610678290, (1610678290, (), [ (16396, 0, None, None) , ], 1 , 1 , 4 , 0 , 168 , (13, 0, None, IID('{737D35AF-C407-420D-9250-A2CBB416DCB9}')) , 0 , )),
]

RecordMap = {
}

CLSIDToClassMap = {
}
CLSIDToPackageMap = {}
win32com.client.CLSIDToClass.RegisterCLSIDsFromDict( CLSIDToClassMap )
VTablesToPackageMap = {}
VTablesToClassMap = {
	'{7AA0E540-0302-11D4-A30E-00C026EE094F}' : 'IDocument3D',
	'{7AA0E540-0300-11D4-A30E-00C026EE094F}' : 'IPart',
	'{7AA0E540-0305-11D4-A30E-00C026EE094F}' : 'IColorParam',
	'{7AA0E540-0301-11D4-A30E-00C026EE094F}' : 'IEntity',
	'{1D15245B-695E-4F9F-AFCA-EACBC3A055BB}' : 'IFeature',
	'{CE5D4888-9006-43AC-9ACC-6D9E58B408B4}' : 'IFeatureCollection',
	'{E17C2BE7-9C11-4FB3-ADBD-04EC912784E8}' : 'IAttribute3DCollection',
	'{F5529801-EDF2-42AE-B0A4-8AB6F5650AE1}' : 'IAttribute3D',
	'{7AA0E540-0303-11D4-A30E-00C026EE094F}' : 'IEntityCollection',
	'{7AA0E540-0311-11D4-A30E-00C026EE094F}' : 'IVariableCollection',
	'{7AA0E540-0312-11D4-A30E-00C026EE094F}' : 'IVariable',
	'{64CBC7CB-005D-47DF-8B3E-53FD974C5A32}' : 'IBodyCollection',
	'{BE70EEE5-1767-483E-9D18-79BCEC5AB837}' : 'IBody',
	'{D269AD47-B2CC-4152-A7BA-127242371208}' : 'IFaceCollection',
	'{7AA0E540-0322-11D4-A30E-00C026EE094F}' : 'IFaceDefinition',
	'{081C7F2D-D5BC-40A6-92FE-C16B67D10B75}' : 'ISurface',
	'{E5066490-773D-4289-A60B-2FC19865174A}' : 'ICurve3D',
	'{0363CD73-028A-485F-92BF-B4DB4B3E239A}' : 'INurbs3dParam',
	'{AC0E0F4D-ACCE-40C4-9B7C-14DAAF224F48}' : 'INurbsPoint3dCollection',
	'{47CDB649-C027-4E8D-8E25-1461CC6D7C12}' : 'INurbsPoint3dParam',
	'{1F21432C-E5BA-404D-B18F-007A0D85CCD0}' : 'INurbsKnotCollection',
	'{A5E6E83E-1F33-4EAF-BAFC-A3F434F23BAA}' : 'ICoordinate3dCollection',
	'{A5A1CB44-5F2E-4059-86B3-4F5056EFF956}' : 'INurbsSurfaceParam',
	'{EFEECE8A-4BB9-4D51-B6A4-AC1BEDA73568}' : 'INurbsPoint3dCollCollection',
	'{22866947-F414-484B-8CCC-F4440BFEF92F}' : 'ILoopCollection',
	'{56965A12-03BB-4068-8AE9-BEFC23EEEB37}' : 'ILoop',
	'{D19B0A07-4CA6-4E77-A8DB-8AC8C7123124}' : 'IOrientedEdgeCollection',
	'{42AA4E40-4415-4C79-8B8C-480E5AFDB79A}' : 'IOrientedEdge',
	'{7AA0E540-0321-11D4-A30E-00C026EE094F}' : 'IEdgeDefinition',
	'{7AA0E540-0320-11D4-A30E-00C026EE094F}' : 'IVertexDefinition',
	'{5E93D4B9-BAAB-4FC4-ACF8-8FF78E9D1B42}' : 'IEdgeCollection',
	'{5F12CD9D-4310-4A6B-B4B8-B1445ABB36D8}' : 'ITessellation',
	'{1EED6C22-25D4-49C6-B76A-90B768966A3B}' : 'IFacet',
	'{74E97440-88A5-4D29-9543-59D775BC9A13}' : 'IMassInertiaParam',
	'{66CBDD80-332C-40B5-9968-DD902EBAB55D}' : 'IIntersectionResult',
	'{DFC4E0F1-5270-40F3-8A4F-BEA75AB5383C}' : 'IBodyParts',
	'{7AA0E540-0310-11D4-A30E-00C026EE094F}' : 'IPlacement',
	'{AC171655-ED3F-4F7A-A625-44083941AF85}' : 'IMeasurer',
	'{6B04A0E4-837A-4151-8E5A-836517F39EAE}' : 'IObject3DNotifyResult',
	'{7AA0E540-0317-11D4-A30E-00C026EE094F}' : 'IPartCollection',
	'{7AA0E540-0313-11D4-A30E-00C026EE094F}' : 'IRequestInfo',
	'{7AA0E540-0304-11D4-A30E-00C026EE094F}' : 'IMateConstraintCollection',
	'{7AA0E540-0314-11D4-A30E-00C026EE094F}' : 'IMateConstraint',
	'{7AA0E540-0315-11D4-A30E-00C026EE094F}' : 'ISpecification3D',
	'{7AA0E540-0318-11D4-A30E-00C026EE094F}' : 'IRasterFormatParam',
	'{7AA0E540-0319-11D4-A30E-00C026EE094F}' : 'IAdditionFormatParam',
	'{F6EDDAE7-AA95-4474-835E-BEB4BC25BAA8}' : 'IViewProjectionCollection',
	'{737D35AF-C407-420D-9250-A2CBB416DCB9}' : 'IViewProjection',
	'{974E5E66-7948-401D-8DAE-C497A6BF1EBD}' : 'ISelectionMng',
	'{BB679D6E-1C5A-4B90-A559-CB37BA1E1FA7}' : 'IChooseMng',
	'{6B9D0CE9-C3E6-436B-9EEE-02F439A45C02}' : 'IComponentPositioner',
	'{06C34A3C-2634-4F82-BCE0-F3D73572958C}' : 'IDocument3DNotifyResult',
	'{7AA0E540-0316-11D4-A30E-00C026EE094F}' : 'IModelLibrary',
	'{7AA0E540-0306-11D4-A30E-00C026EE094F}' : 'IThinParam',
	'{7AA0E540-0307-11D4-A30E-00C026EE094F}' : 'IExtrusionParam',
	'{7AA0E540-0308-11D4-A30E-00C026EE094F}' : 'IRotatedParam',
	'{16EAD9EF-671F-4557-9954-BB070864F638}' : 'IObjectsFilter3D',
	'{67B417BA-F248-4B56-AD03-C4057C7F2EEE}' : 'IChooseBodies',
	'{2920B89D-636E-4DCC-8E62-34D2F4B4BB00}' : 'IChooseParts',
	'{7AA0E540-0323-11D4-A30E-00C026EE094F}' : 'ISketchDefinition',
	'{44ABB63A-E6F2-47C5-945C-5C17D0477CE0}' : 'IThreadDefinition',
	'{7AA0E540-0335-11D4-A30E-00C026EE094F}' : 'IAxis2PointsDefinition',
	'{7AA0E540-0336-11D4-A30E-00C026EE094F}' : 'IAxis2PlanesDefinition',
	'{7AA0E540-0337-11D4-A30E-00C026EE094F}' : 'IAxisOperationsDefinition',
	'{7AA0E540-0339-11D4-A30E-00C026EE094F}' : 'IAxisEdgeDefinition',
	'{7AA0E540-0341-11D4-A30E-00C026EE094F}' : 'IPlaneOffsetDefinition',
	'{7AA0E540-0342-11D4-A30E-00C026EE094F}' : 'IPlane3PointsDefinition',
	'{7AA0E540-0343-11D4-A30E-00C026EE094F}' : 'IPlaneAngleDefinition',
	'{7AA0E540-0344-11D4-A30E-00C026EE094F}' : 'IPlaneEdgePointDefinition',
	'{7AA0E540-0345-11D4-A30E-00C026EE094F}' : 'IPlaneParallelDefinition',
	'{7AA0E540-0346-11D4-A30E-00C026EE094F}' : 'IPlanePerpendicularDefinition',
	'{7AA0E540-0347-11D4-A30E-00C026EE094F}' : 'IPlaneNormalToSurfaceDefinition',
	'{7AA0E540-0348-11D4-A30E-00C026EE094F}' : 'IPlaneTangentToSurfaceDefinition',
	'{7AA0E540-0349-11D4-A30E-00C026EE094F}' : 'IPlaneLineToEdgeDefinition',
	'{7AA0E540-0350-11D4-A30E-00C026EE094F}' : 'IPlaneLineToPlaneDefinition',
	'{7AA0E540-0355-11D4-A30E-00C026EE094F}' : 'IBaseExtrusionDefinition',
	'{7AA0E540-0356-11D4-A30E-00C026EE094F}' : 'IBossExtrusionDefinition',
	'{7AA0E540-0357-11D4-A30E-00C026EE094F}' : 'ICutExtrusionDefinition',
	'{7AA0E540-0358-11D4-A30E-00C026EE094F}' : 'IBaseRotatedDefinition',
	'{7AA0E540-0359-11D4-A30E-00C026EE094F}' : 'IBossRotatedDefinition',
	'{7AA0E540-0360-11D4-A30E-00C026EE094F}' : 'ICutRotatedDefinition',
	'{7AA0E540-0361-11D4-A30E-00C026EE094F}' : 'IBaseLoftDefinition',
	'{7AA0E540-0362-11D4-A30E-00C026EE094F}' : 'IBossLoftDefinition',
	'{7AA0E540-0363-11D4-A30E-00C026EE094F}' : 'ICutLoftDefinition',
	'{7AA0E540-0364-11D4-A30E-00C026EE094F}' : 'IBaseEvolutionDefinition',
	'{7AA0E540-0365-11D4-A30E-00C026EE094F}' : 'IBossEvolutionDefinition',
	'{7AA0E540-0366-11D4-A30E-00C026EE094F}' : 'ICutEvolutionDefinition',
	'{7AA0E540-0367-11D4-A30E-00C026EE094F}' : 'IFilletDefinition',
	'{7AA0E540-0368-11D4-A30E-00C026EE094F}' : 'IChamferDefinition',
	'{7AA0E540-0369-11D4-A30E-00C026EE094F}' : 'IShellDefinition',
	'{7AA0E540-0370-11D4-A30E-00C026EE094F}' : 'ICopyMeshDefinition',
	'{BEC3920D-6238-401A-86A3-A600570F47A4}' : 'IDeletedCopyCollection',
	'{7AA0E540-0371-11D4-A30E-00C026EE094F}' : 'ICopyCircularDefinition',
	'{7AA0E540-0372-11D4-A30E-00C026EE094F}' : 'ICopyCurveDefinition',
	'{7AA0E540-0373-11D4-A30E-00C026EE094F}' : 'IMirrorDefinition',
	'{7AA0E540-0374-11D4-A30E-00C026EE094F}' : 'IMirrorAllDefinition',
	'{7AA0E540-0375-11D4-A30E-00C026EE094F}' : 'ICutByPlaneDefinition',
	'{7AA0E540-0376-11D4-A30E-00C026EE094F}' : 'ICutBySketchDefinition',
	'{7AA0E540-0377-11D4-A30E-00C026EE094F}' : 'IMeshPartArrayDefinition',
	'{7AA0E540-0378-11D4-A30E-00C026EE094F}' : 'ICircularPartArrayDefinition',
	'{7AA0E540-0379-11D4-A30E-00C026EE094F}' : 'ICurvePartArrayDefinition',
	'{7AA0E540-0380-11D4-A30E-00C026EE094F}' : 'IDerivativePartArrayDefinition',
	'{7AA0E540-0381-11D4-A30E-00C026EE094F}' : 'IInclineDefinition',
	'{7AA0E540-0382-11D4-A30E-00C026EE094F}' : 'IRibDefinition',
	'{7AA0E540-0384-11D4-A30E-00C026EE094F}' : 'IImportedSurfaceDefinition',
	'{7AA0E540-0400-11D4-A30E-00C026EE094F}' : 'IPolygonalLineDefinition',
	'{D2D61E71-151A-4359-A0BE-DEA5A76F2492}' : 'IPolygonalLineVertexParam',
	'{7AA0E540-0401-11D4-A30E-00C026EE094F}' : 'IConicSpiralDefinition',
	'{7AA0E540-0402-11D4-A30E-00C026EE094F}' : 'ISplineDefinition',
	'{7AA0E540-0403-11D4-A30E-00C026EE094F}' : 'ICylindricSpiralDefinition',
	'{45702BE9-1505-40AB-BF0C-7FE86D5373E2}' : 'IEvolutionSurfaceDefinition',
	'{6D87BCE9-5D07-41AD-A137-42957DAF0A6F}' : 'IExtrusionSurfaceDefinition',
	'{FD27841D-1374-4F7F-AE8A-C2A44F89120D}' : 'IRotatedSurfaceDefinition',
	'{6E6A127B-233E-401F-8E29-BB298AE0FA45}' : 'ILoftSurfaceDefinition',
	'{B6F6D0AB-6339-4FC6-842B-CC96596BCE82}' : 'IMacro3DDefinition',
	'{7AA0E540-0338-11D4-A30E-00C026EE094F}' : 'IAxisConefaceDefinition',
	'{7C641671-F791-47AC-B8AE-382428D8A01D}' : 'IUnionComponentsDefinition',
	'{1DD4FF64-72EF-408A-A9C6-0009B01FFC94}' : 'IMoldCavityDefinition',
	'{CACF8C5A-9969-44A1-A36D-4CF516200920}' : 'IPlaneMiddleDefinition',
	'{BF0F6CEC-F517-4094-B913-6B0A28E7CA83}' : 'IControlPointDefinition',
	'{F53A02E1-C560-4DE3-9E19-0D634FBE49A5}' : 'IConjunctivePointDefinition',
	'{2CF40627-9D0A-4588-A399-45F0FF96165F}' : 'IAggregateDefinition',
	'{8E54CAEA-D1FC-4FF4-A0E5-4F5A9F5CDC6B}' : 'IDefaultObject',
	'{4C69F05F-981C-4183-8DC6-D2D375D29581}' : 'IEmbodiment3D',
	'{FE1515C7-7003-4EE2-9C65-0429039DD217}' : 'ILineSeg3dParam',
	'{9B2FED02-5FAC-4473-9E64-9BDF8B331E10}' : 'ICircle3dParam',
	'{1DD50F18-9C19-424C-B20E-77E1369976E3}' : 'IEllipse3dParam',
	'{9C412B77-BFDE-4D60-B8C7-BD849801975E}' : 'IPlaneParam',
	'{105943CF-5A3E-4AA6-4AA6-57B4179013FC}' : 'IConeParam',
	'{A2899CA0-C84E-4C16-BFB2-E8DA69FC117E}' : 'ICylinderParam',
	'{941163AA-0F8A-422A-BE1A-9F43C8001044}' : 'ISphereParam',
	'{C9C614A7-E8B6-4454-AC8B-E42330C11E15}' : 'ITorusParam',
	'{24A26824-E13C-453F-8874-A0DF62AB595A}' : 'IArc3dParam',
	'{4DEA35BC-F9E0-4A3E-B815-FB55896FC8EF}' : 'ISTrackingPointsMeasurer',
	'{EE5B4795-6E76-49A2-BFAD-9D953D82771F}' : 'IDocument3DNotify',
	'{7B4657BB-68D9-4CA8-BA81-52C1D5C96943}' : 'IObject3DNotify',
	'{0712DCCC-83E0-429E-AB8C-5B255DD3C4E4}' : 'IProcess3DNotify',
	'{45B82B5C-D0B7-4AC5-965C-26B09612CBF6}' : 'IProcess3DManipulatorsNotify',
}


NamesToIIDMap = {
	'IDocument3D' : '{7AA0E540-0302-11D4-A30E-00C026EE094F}',
	'IPart' : '{7AA0E540-0300-11D4-A30E-00C026EE094F}',
	'IColorParam' : '{7AA0E540-0305-11D4-A30E-00C026EE094F}',
	'IEntity' : '{7AA0E540-0301-11D4-A30E-00C026EE094F}',
	'IFeature' : '{1D15245B-695E-4F9F-AFCA-EACBC3A055BB}',
	'IFeatureCollection' : '{CE5D4888-9006-43AC-9ACC-6D9E58B408B4}',
	'IAttribute3DCollection' : '{E17C2BE7-9C11-4FB3-ADBD-04EC912784E8}',
	'IAttribute3D' : '{F5529801-EDF2-42AE-B0A4-8AB6F5650AE1}',
	'IEntityCollection' : '{7AA0E540-0303-11D4-A30E-00C026EE094F}',
	'IVariableCollection' : '{7AA0E540-0311-11D4-A30E-00C026EE094F}',
	'IVariable' : '{7AA0E540-0312-11D4-A30E-00C026EE094F}',
	'IBodyCollection' : '{64CBC7CB-005D-47DF-8B3E-53FD974C5A32}',
	'IBody' : '{BE70EEE5-1767-483E-9D18-79BCEC5AB837}',
	'IFaceCollection' : '{D269AD47-B2CC-4152-A7BA-127242371208}',
	'IFaceDefinition' : '{7AA0E540-0322-11D4-A30E-00C026EE094F}',
	'ISurface' : '{081C7F2D-D5BC-40A6-92FE-C16B67D10B75}',
	'ICurve3D' : '{E5066490-773D-4289-A60B-2FC19865174A}',
	'INurbs3dParam' : '{0363CD73-028A-485F-92BF-B4DB4B3E239A}',
	'INurbsPoint3dCollection' : '{AC0E0F4D-ACCE-40C4-9B7C-14DAAF224F48}',
	'INurbsPoint3dParam' : '{47CDB649-C027-4E8D-8E25-1461CC6D7C12}',
	'INurbsKnotCollection' : '{1F21432C-E5BA-404D-B18F-007A0D85CCD0}',
	'ICoordinate3dCollection' : '{A5E6E83E-1F33-4EAF-BAFC-A3F434F23BAA}',
	'INurbsSurfaceParam' : '{A5A1CB44-5F2E-4059-86B3-4F5056EFF956}',
	'INurbsPoint3dCollCollection' : '{EFEECE8A-4BB9-4D51-B6A4-AC1BEDA73568}',
	'ILoopCollection' : '{22866947-F414-484B-8CCC-F4440BFEF92F}',
	'ILoop' : '{56965A12-03BB-4068-8AE9-BEFC23EEEB37}',
	'IOrientedEdgeCollection' : '{D19B0A07-4CA6-4E77-A8DB-8AC8C7123124}',
	'IOrientedEdge' : '{42AA4E40-4415-4C79-8B8C-480E5AFDB79A}',
	'IEdgeDefinition' : '{7AA0E540-0321-11D4-A30E-00C026EE094F}',
	'IVertexDefinition' : '{7AA0E540-0320-11D4-A30E-00C026EE094F}',
	'IEdgeCollection' : '{5E93D4B9-BAAB-4FC4-ACF8-8FF78E9D1B42}',
	'ITessellation' : '{5F12CD9D-4310-4A6B-B4B8-B1445ABB36D8}',
	'IFacet' : '{1EED6C22-25D4-49C6-B76A-90B768966A3B}',
	'IMassInertiaParam' : '{74E97440-88A5-4D29-9543-59D775BC9A13}',
	'IIntersectionResult' : '{66CBDD80-332C-40B5-9968-DD902EBAB55D}',
	'IBodyParts' : '{DFC4E0F1-5270-40F3-8A4F-BEA75AB5383C}',
	'IPlacement' : '{7AA0E540-0310-11D4-A30E-00C026EE094F}',
	'IMeasurer' : '{AC171655-ED3F-4F7A-A625-44083941AF85}',
	'IObject3DNotifyResult' : '{6B04A0E4-837A-4151-8E5A-836517F39EAE}',
	'IPartCollection' : '{7AA0E540-0317-11D4-A30E-00C026EE094F}',
	'IRequestInfo' : '{7AA0E540-0313-11D4-A30E-00C026EE094F}',
	'IMateConstraintCollection' : '{7AA0E540-0304-11D4-A30E-00C026EE094F}',
	'IMateConstraint' : '{7AA0E540-0314-11D4-A30E-00C026EE094F}',
	'ISpecification3D' : '{7AA0E540-0315-11D4-A30E-00C026EE094F}',
	'IRasterFormatParam' : '{7AA0E540-0318-11D4-A30E-00C026EE094F}',
	'IAdditionFormatParam' : '{7AA0E540-0319-11D4-A30E-00C026EE094F}',
	'IViewProjectionCollection' : '{F6EDDAE7-AA95-4474-835E-BEB4BC25BAA8}',
	'IViewProjection' : '{737D35AF-C407-420D-9250-A2CBB416DCB9}',
	'ISelectionMng' : '{974E5E66-7948-401D-8DAE-C497A6BF1EBD}',
	'IChooseMng' : '{BB679D6E-1C5A-4B90-A559-CB37BA1E1FA7}',
	'IComponentPositioner' : '{6B9D0CE9-C3E6-436B-9EEE-02F439A45C02}',
	'IDocument3DNotifyResult' : '{06C34A3C-2634-4F82-BCE0-F3D73572958C}',
	'IModelLibrary' : '{7AA0E540-0316-11D4-A30E-00C026EE094F}',
	'IThinParam' : '{7AA0E540-0306-11D4-A30E-00C026EE094F}',
	'IExtrusionParam' : '{7AA0E540-0307-11D4-A30E-00C026EE094F}',
	'IRotatedParam' : '{7AA0E540-0308-11D4-A30E-00C026EE094F}',
	'IObjectsFilter3D' : '{16EAD9EF-671F-4557-9954-BB070864F638}',
	'IChooseBodies' : '{67B417BA-F248-4B56-AD03-C4057C7F2EEE}',
	'IChooseParts' : '{2920B89D-636E-4DCC-8E62-34D2F4B4BB00}',
	'ISketchDefinition' : '{7AA0E540-0323-11D4-A30E-00C026EE094F}',
	'IThreadDefinition' : '{44ABB63A-E6F2-47C5-945C-5C17D0477CE0}',
	'IAxis2PointsDefinition' : '{7AA0E540-0335-11D4-A30E-00C026EE094F}',
	'IAxis2PlanesDefinition' : '{7AA0E540-0336-11D4-A30E-00C026EE094F}',
	'IAxisOperationsDefinition' : '{7AA0E540-0337-11D4-A30E-00C026EE094F}',
	'IAxisEdgeDefinition' : '{7AA0E540-0339-11D4-A30E-00C026EE094F}',
	'IPlaneOffsetDefinition' : '{7AA0E540-0341-11D4-A30E-00C026EE094F}',
	'IPlane3PointsDefinition' : '{7AA0E540-0342-11D4-A30E-00C026EE094F}',
	'IPlaneAngleDefinition' : '{7AA0E540-0343-11D4-A30E-00C026EE094F}',
	'IPlaneEdgePointDefinition' : '{7AA0E540-0344-11D4-A30E-00C026EE094F}',
	'IPlaneParallelDefinition' : '{7AA0E540-0345-11D4-A30E-00C026EE094F}',
	'IPlanePerpendicularDefinition' : '{7AA0E540-0346-11D4-A30E-00C026EE094F}',
	'IPlaneNormalToSurfaceDefinition' : '{7AA0E540-0347-11D4-A30E-00C026EE094F}',
	'IPlaneTangentToSurfaceDefinition' : '{7AA0E540-0348-11D4-A30E-00C026EE094F}',
	'IPlaneLineToEdgeDefinition' : '{7AA0E540-0349-11D4-A30E-00C026EE094F}',
	'IPlaneLineToPlaneDefinition' : '{7AA0E540-0350-11D4-A30E-00C026EE094F}',
	'IBaseExtrusionDefinition' : '{7AA0E540-0355-11D4-A30E-00C026EE094F}',
	'IBossExtrusionDefinition' : '{7AA0E540-0356-11D4-A30E-00C026EE094F}',
	'ICutExtrusionDefinition' : '{7AA0E540-0357-11D4-A30E-00C026EE094F}',
	'IBaseRotatedDefinition' : '{7AA0E540-0358-11D4-A30E-00C026EE094F}',
	'IBossRotatedDefinition' : '{7AA0E540-0359-11D4-A30E-00C026EE094F}',
	'ICutRotatedDefinition' : '{7AA0E540-0360-11D4-A30E-00C026EE094F}',
	'IBaseLoftDefinition' : '{7AA0E540-0361-11D4-A30E-00C026EE094F}',
	'IBossLoftDefinition' : '{7AA0E540-0362-11D4-A30E-00C026EE094F}',
	'ICutLoftDefinition' : '{7AA0E540-0363-11D4-A30E-00C026EE094F}',
	'IBaseEvolutionDefinition' : '{7AA0E540-0364-11D4-A30E-00C026EE094F}',
	'IBossEvolutionDefinition' : '{7AA0E540-0365-11D4-A30E-00C026EE094F}',
	'ICutEvolutionDefinition' : '{7AA0E540-0366-11D4-A30E-00C026EE094F}',
	'IFilletDefinition' : '{7AA0E540-0367-11D4-A30E-00C026EE094F}',
	'IChamferDefinition' : '{7AA0E540-0368-11D4-A30E-00C026EE094F}',
	'IShellDefinition' : '{7AA0E540-0369-11D4-A30E-00C026EE094F}',
	'ICopyMeshDefinition' : '{7AA0E540-0370-11D4-A30E-00C026EE094F}',
	'IDeletedCopyCollection' : '{BEC3920D-6238-401A-86A3-A600570F47A4}',
	'ICopyCircularDefinition' : '{7AA0E540-0371-11D4-A30E-00C026EE094F}',
	'ICopyCurveDefinition' : '{7AA0E540-0372-11D4-A30E-00C026EE094F}',
	'IMirrorDefinition' : '{7AA0E540-0373-11D4-A30E-00C026EE094F}',
	'IMirrorAllDefinition' : '{7AA0E540-0374-11D4-A30E-00C026EE094F}',
	'ICutByPlaneDefinition' : '{7AA0E540-0375-11D4-A30E-00C026EE094F}',
	'ICutBySketchDefinition' : '{7AA0E540-0376-11D4-A30E-00C026EE094F}',
	'IMeshPartArrayDefinition' : '{7AA0E540-0377-11D4-A30E-00C026EE094F}',
	'ICircularPartArrayDefinition' : '{7AA0E540-0378-11D4-A30E-00C026EE094F}',
	'ICurvePartArrayDefinition' : '{7AA0E540-0379-11D4-A30E-00C026EE094F}',
	'IDerivativePartArrayDefinition' : '{7AA0E540-0380-11D4-A30E-00C026EE094F}',
	'IInclineDefinition' : '{7AA0E540-0381-11D4-A30E-00C026EE094F}',
	'IRibDefinition' : '{7AA0E540-0382-11D4-A30E-00C026EE094F}',
	'IImportedSurfaceDefinition' : '{7AA0E540-0384-11D4-A30E-00C026EE094F}',
	'IPolygonalLineDefinition' : '{7AA0E540-0400-11D4-A30E-00C026EE094F}',
	'IPolygonalLineVertexParam' : '{D2D61E71-151A-4359-A0BE-DEA5A76F2492}',
	'IConicSpiralDefinition' : '{7AA0E540-0401-11D4-A30E-00C026EE094F}',
	'ISplineDefinition' : '{7AA0E540-0402-11D4-A30E-00C026EE094F}',
	'ICylindricSpiralDefinition' : '{7AA0E540-0403-11D4-A30E-00C026EE094F}',
	'IEvolutionSurfaceDefinition' : '{45702BE9-1505-40AB-BF0C-7FE86D5373E2}',
	'IExtrusionSurfaceDefinition' : '{6D87BCE9-5D07-41AD-A137-42957DAF0A6F}',
	'IRotatedSurfaceDefinition' : '{FD27841D-1374-4F7F-AE8A-C2A44F89120D}',
	'ILoftSurfaceDefinition' : '{6E6A127B-233E-401F-8E29-BB298AE0FA45}',
	'IMacro3DDefinition' : '{B6F6D0AB-6339-4FC6-842B-CC96596BCE82}',
	'IAxisConefaceDefinition' : '{7AA0E540-0338-11D4-A30E-00C026EE094F}',
	'IUnionComponentsDefinition' : '{7C641671-F791-47AC-B8AE-382428D8A01D}',
	'IMoldCavityDefinition' : '{1DD4FF64-72EF-408A-A9C6-0009B01FFC94}',
	'IPlaneMiddleDefinition' : '{CACF8C5A-9969-44A1-A36D-4CF516200920}',
	'IControlPointDefinition' : '{BF0F6CEC-F517-4094-B913-6B0A28E7CA83}',
	'IConjunctivePointDefinition' : '{F53A02E1-C560-4DE3-9E19-0D634FBE49A5}',
	'IAggregateDefinition' : '{2CF40627-9D0A-4588-A399-45F0FF96165F}',
	'IDefaultObject' : '{8E54CAEA-D1FC-4FF4-A0E5-4F5A9F5CDC6B}',
	'IEmbodiment3D' : '{4C69F05F-981C-4183-8DC6-D2D375D29581}',
	'ILineSeg3dParam' : '{FE1515C7-7003-4EE2-9C65-0429039DD217}',
	'ICircle3dParam' : '{9B2FED02-5FAC-4473-9E64-9BDF8B331E10}',
	'IEllipse3dParam' : '{1DD50F18-9C19-424C-B20E-77E1369976E3}',
	'IPlaneParam' : '{9C412B77-BFDE-4D60-B8C7-BD849801975E}',
	'IConeParam' : '{105943CF-5A3E-4AA6-4AA6-57B4179013FC}',
	'ICylinderParam' : '{A2899CA0-C84E-4C16-BFB2-E8DA69FC117E}',
	'ISphereParam' : '{941163AA-0F8A-422A-BE1A-9F43C8001044}',
	'ITorusParam' : '{C9C614A7-E8B6-4454-AC8B-E42330C11E15}',
	'IArc3dParam' : '{24A26824-E13C-453F-8874-A0DF62AB595A}',
	'ISTrackingPointsMeasurer' : '{4DEA35BC-F9E0-4A3E-B815-FB55896FC8EF}',
	'IDocument3DNotify' : '{EE5B4795-6E76-49A2-BFAD-9D953D82771F}',
	'IObject3DNotify' : '{7B4657BB-68D9-4CA8-BA81-52C1D5C96943}',
	'IProcess3DNotify' : '{0712DCCC-83E0-429E-AB8C-5B255DD3C4E4}',
	'IProcess3DManipulatorsNotify' : '{45B82B5C-D0B7-4AC5-965C-26B09612CBF6}',
}


