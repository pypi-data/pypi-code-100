# -*- coding: utf-8 -*-
"""\
* *[Summary]* :: A /library/ Beginning point for development of new ICM oriented libraries.
"""

import typing

icmInfo: typing.Dict[str, typing.Any] = { 'moduleDescription': ["""
*       [[elisp:(org-show-subtree)][|=]]  [[elisp:(org-cycle)][| *Description:* | ]]
**  [[elisp:(org-cycle)][| ]]  [Xref]          :: *[Related/Xrefs:]*  <<Xref-Here->>  -- External Documents  [[elisp:(org-cycle)][| ]]

**  [[elisp:(org-cycle)][| ]]   Model and Terminology                                      :Overview:
*** concept             -- Desctiption of concept
**      [End-Of-Description]
"""], }

icmInfo['moduleUsage'] = """
*       [[elisp:(org-show-subtree)][|=]]  [[elisp:(org-cycle)][| *Usage:* | ]]

**      How-Tos:
**      [End-Of-Usage]
"""

icmInfo['moduleStatus'] = """
*       [[elisp:(org-show-subtree)][|=]]  [[elisp:(org-cycle)][| *Status:* | ]]
**  [[elisp:(org-cycle)][| ]]  [Info]          :: *[Current-Info:]* Status/Maintenance -- General TODO List [[elisp:(org-cycle)][| ]]
** TODO [[elisp:(org-cycle)][| ]]  Current     :: For now it is an ICM. Turn it into ICM-Lib. [[elisp:(org-cycle)][| ]]
**      [End-Of-Status]
"""

"""
*  [[elisp:(org-cycle)][| *ICM-INFO:* |]] :: Author, Copyleft and Version Information
"""
####+BEGIN: bx:icm:py:name :style "fileName"
icmInfo['moduleName'] = "bpoFpBases"
####+END:

####+BEGIN: bx:icm:py:version-timestamp :style "date"
icmInfo['version'] = "202110070455"
####+END:

####+BEGIN: bx:icm:py:status :status "Production"
icmInfo['status']  = "Production"
####+END:

icmInfo['credits'] = ""

####+BEGIN: bx:dblock:global:file-insert-cond :cond "./blee.el" :file "/bisos/apps/defaults/update/sw/icm/py/icmInfo-mbNedaGplByStar.py"
icmInfo['authors'] = "[[http://mohsen.1.banan.byname.net][Mohsen Banan]]"
icmInfo['copyright'] = "Copyright 2017, [[http://www.neda.com][Neda Communications, Inc.]]"
icmInfo['licenses'] = "[[https://www.gnu.org/licenses/agpl-3.0.en.html][Affero GPL]]", "Libre-Halaal Services License", "Neda Commercial License"
icmInfo['maintainers'] = "[[http://mohsen.1.banan.byname.net][Mohsen Banan]]"
icmInfo['contacts'] = "[[http://mohsen.1.banan.byname.net/contact]]"
icmInfo['partOf'] = "[[http://www.by-star.net][Libre-Halaal ByStar Digital Ecosystem]]"
####+END:

icmInfo['panel'] = "{}-Panel.org".format(icmInfo['moduleName'])
icmInfo['groupingType'] = "IcmGroupingType-pkged"
icmInfo['cmndParts'] = "IcmCmndParts[common] IcmCmndParts[param]"


####+BEGIN: bx:icm:python:top-of-file :partof "bystar" :copyleft "halaal+minimal"
"""
*  This file:/bisos/git/auth/bxRepos/bisos-pip/bpo/py3/bisos/bpo/bpoFpBases.py :: [[elisp:(org-cycle)][| ]]
 is part of The Libre-Halaal ByStar Digital Ecosystem. http://www.by-star.net
 *CopyLeft*  This Software is a Libre-Halaal Poly-Existential. See http://www.freeprotocols.org
 A Python Interactively Command Module (PyICM).
 Best Developed With COMEEGA-Emacs And Best Used With Blee-ICM-Players.
 *WARNING*: All edits wityhin Dynamic Blocks may be lost.
"""
####+END:

####+BEGIN: bx:icm:python:topControls :partof "bystar" :copyleft "halaal+minimal"
"""
*  [[elisp:(org-cycle)][|/Controls/| ]] :: [[elisp:(org-show-subtree)][|=]]  [[elisp:(show-all)][Show-All]]  [[elisp:(org-shifttab)][Overview]]  [[elisp:(progn (org-shifttab) (org-content))][Content]] | [[file:Panel.org][Panel]] | [[elisp:(blee:ppmm:org-mode-toggle)][Nat]] | [[elisp:(bx:org:run-me)][Run]] | [[elisp:(bx:org:run-me-eml)][RunEml]] | [[elisp:(delete-other-windows)][(1)]] | [[elisp:(progn (save-buffer) (kill-buffer))][S&Q]]  [[elisp:(save-buffer)][Save]]  [[elisp:(kill-buffer)][Quit]] [[elisp:(org-cycle)][| ]]
** /Version Control/ ::  [[elisp:(call-interactively (quote cvs-update))][cvs-update]]  [[elisp:(vc-update)][vc-update]] | [[elisp:(bx:org:agenda:this-file-otherWin)][Agenda-List]]  [[elisp:(bx:org:todo:this-file-otherWin)][ToDo-List]]
"""
####+END:
####+BEGIN: bx:dblock:global:file-insert-cond :cond "./blee.el" :file "/bisos/apps/defaults/software/plusOrg/dblock/inserts/pyWorkBench.org"
"""
*  /Python Workbench/ ::  [[elisp:(org-cycle)][| ]]  [[elisp:(python-check (format "/bisos/venv/py3/bisos3/bin/python -m pyclbr %s" (bx:buf-fname))))][pyclbr]] || [[elisp:(python-check (format "/bisos/venv/py3/bisos3/bin/python -m pydoc ./%s" (bx:buf-fname))))][pydoc]] || [[elisp:(python-check (format "/bisos/pipx/bin/pyflakes %s" (bx:buf-fname)))][pyflakes]] | [[elisp:(python-check (format "/bisos/pipx/bin/pychecker %s" (bx:buf-fname))))][pychecker (executes)]] | [[elisp:(python-check (format "/bisos/pipx/bin/pycodestyle %s" (bx:buf-fname))))][pycodestyle]] | [[elisp:(python-check (format "/bisos/pipx/bin/flake8 %s" (bx:buf-fname))))][flake8]] | [[elisp:(python-check (format "/bisos/pipx/bin/pylint %s" (bx:buf-fname))))][pylint]]  [[elisp:(org-cycle)][| ]]
"""
####+END:

####+BEGIN: bx:icm:python:icmItem :itemType "=Imports=" :itemTitle "*IMPORTS*"
"""
*  _[[elisp:(blee:menu-sel:outline:popupMenu)][±]]_ _[[elisp:(blee:menu-sel:navigation:popupMenu)][Ξ]]_ [[elisp:(bx:orgm:indirectBufOther)][|>]] *[[elisp:(blee:ppmm:org-mode-toggle)][|N]]*  =Imports=  :: *IMPORTS*  [[elisp:(org-cycle)][| ]]
"""
####+END:

import collections

import __main__


####+BEGIN: bx:dblock:global:file-insert-cond :cond "./blee.el" :file "/bisos/apps/defaults/update/sw/icm/py/importUcfIcmG.py"
from unisos import ucf
from unisos import icm

icm.unusedSuppressForEval(ucf.__file__)  # in case icm and ucf are not used

G = icm.IcmGlobalContext()
# G.icmLibsAppend = __file__
# G.icmCmndsLibsAppend = __file__
####+END:

from bisos.basics import pattern

#from bisos.icm import clsMethod
from bisos.icm import fp

#from bisos.bpo import bpo
from bisos.pals import palsBpo

####+BEGIN: bx:dblock:python:section :title "Common Parameters Specification"
"""
*  [[elisp:(beginning-of-buffer)][Top]] ############## [[elisp:(blee:ppmm:org-mode-toggle)][Nat]] [[elisp:(delete-other-windows)][(1)]]    *Common Parameters Specification*  [[elisp:(org-cycle)][| ]]  [[elisp:(org-show-subtree)][|=]]
"""
####+END:


####+BEGIN: bx:dblock:python:class :className "BpoFpBase" :superClass "object" :comment "" :classType "basic"
"""
*  _[[elisp:(blee:menu-sel:outline:popupMenu)][±]]_ _[[elisp:(blee:menu-sel:navigation:popupMenu)][Ξ]]_ [[elisp:(bx:orgm:indirectBufOther)][|>]] *[[elisp:(blee:ppmm:org-mode-toggle)][|N]]*  Class-basic :: /BpoFpBase/ object  [[elisp:(org-cycle)][| ]]
"""
class BpoFpBase(object):
####+END:
    """
** Links a base within a BPO to a ICM-FPs class
"""
####+BEGIN: bx:icm:py3:method :methodName "__init__" :deco "default"
    """
**  _[[elisp:(blee:menu-sel:outline:popupMenu)][±]]_ _[[elisp:(blee:menu-sel:navigation:popupMenu)][Ξ]]_ [[elisp:(bx:orgm:indirectBufOther)][|>]] *[[elisp:(blee:ppmm:org-mode-toggle)][|N]]*  Method-    :: /__init__/ deco=default  [[elisp:(org-cycle)][| ]]
"""
    @icm.subjectToTracking(fnLoc=True, fnEntry=True, fnExit=True)
    def __init__(
####+END:
            self,
            bpoId,
            fileSysPath,
    ):
        self.bpoId = bpoId
        self.fpsBaseDir = None
        self.fpsBaseInst = None


####+BEGIN: bx:icm:py3:method :methodName "fps_absBasePath" :deco "default"
    """
**  _[[elisp:(blee:menu-sel:outline:popupMenu)][±]]_ _[[elisp:(blee:menu-sel:navigation:popupMenu)][Ξ]]_ [[elisp:(bx:orgm:indirectBufOther)][|>]] *[[elisp:(blee:ppmm:org-mode-toggle)][|N]]*  Method-    :: /fps_absBasePath/ deco=default  [[elisp:(org-cycle)][| ]]
"""
    @icm.subjectToTracking(fnLoc=True, fnEntry=True, fnExit=True)
    def fps_absBasePath(
####+END:
           self,
    ):
        return typing.cast(str, self.fpsBaseDir)


####+BEGIN: bx:icm:py3:method :methodName "fps_absBasePathSet" :deco "default"
    """
**  _[[elisp:(blee:menu-sel:outline:popupMenu)][±]]_ _[[elisp:(blee:menu-sel:navigation:popupMenu)][Ξ]]_ [[elisp:(bx:orgm:indirectBufOther)][|>]] *[[elisp:(blee:ppmm:org-mode-toggle)][|N]]*  Method-    :: /fps_absBasePathSet/ deco=default  [[elisp:(org-cycle)][| ]]
"""
    @icm.subjectToTracking(fnLoc=True, fnEntry=True, fnExit=True)
    def fps_absBasePathSet(
####+END:
            self,
            fpsBaseDir,
    ):
        self.fpsBaseDir = fpsBaseDir

####+BEGIN: bx:icm:py3:method :methodName "fps_baseInstanceMake" :deco "default"
    """
**  _[[elisp:(blee:menu-sel:outline:popupMenu)][±]]_ _[[elisp:(blee:menu-sel:navigation:popupMenu)][Ξ]]_ [[elisp:(bx:orgm:indirectBufOther)][|>]] *[[elisp:(blee:ppmm:org-mode-toggle)][|N]]*  Method-    :: /fps_baseInstanceMake/ deco=default  [[elisp:(org-cycle)][| ]]
"""
    @icm.subjectToTracking(fnLoc=True, fnEntry=True, fnExit=True)
    def fps_baseInstanceMake(
####+END:
            self,
            BaseClassName,
    ):
        fpsPath = self.fps_absBasePath()
        self.fpsBaseInst = pattern.sameInstance(
            BaseClassName,
            fpsPath,
        )
        return self.fpsBaseInst

####+BEGIN: bx:icm:py3:method :methodName "fps_baseInstanceGet" :deco "default"
    """
**  _[[elisp:(blee:menu-sel:outline:popupMenu)][±]]_ _[[elisp:(blee:menu-sel:navigation:popupMenu)][Ξ]]_ [[elisp:(bx:orgm:indirectBufOther)][|>]] *[[elisp:(blee:ppmm:org-mode-toggle)][|N]]*  Method-    :: /fps_baseInstanceGet/ deco=default  [[elisp:(org-cycle)][| ]]
"""
    @icm.subjectToTracking(fnLoc=True, fnEntry=True, fnExit=True)
    def fps_baseInstanceGet(
####+END:
            self,
    ):
        return self.fpsBaseInst


####+BEGIN: bx:icm:py3:method :methodName "fps_baseMake" :deco "default"
    """
**  _[[elisp:(blee:menu-sel:outline:popupMenu)][±]]_ _[[elisp:(blee:menu-sel:navigation:popupMenu)][Ξ]]_ [[elisp:(bx:orgm:indirectBufOther)][|>]] *[[elisp:(blee:ppmm:org-mode-toggle)][|N]]*  Method-    :: /fps_baseMake/ deco=default  [[elisp:(org-cycle)][| ]]
"""
    @icm.subjectToTracking(fnLoc=True, fnEntry=True, fnExit=True)
    def fps_baseMake(
####+END:
            self,
    ):
        icm.EH_problem_usageError("This should have been specified in the subClass")
        return None


####+BEGIN: bx:dblock:python:section :title "Common Examples Sections"
"""
*  [[elisp:(beginning-of-buffer)][Top]] ############## [[elisp:(blee:ppmm:org-mode-toggle)][Nat]] [[elisp:(delete-other-windows)][(1)]]    *Common Examples Sections*  [[elisp:(org-cycle)][| ]]  [[elisp:(org-show-subtree)][|=]]
"""
####+END:


####+BEGIN: bx:dblock:python:func :funcName "examples_bpo_fpBases" :comment "Show/Verify/Update For relevant PBDs" :funcType "examples" :retType "none" :deco "" :argsList "bpoId cls menuLevel='chapter'"
"""
*  _[[elisp:(blee:menu-sel:outline:popupMenu)][±]]_ _[[elisp:(blee:menu-sel:navigation:popupMenu)][Ξ]]_ [[elisp:(bx:orgm:indirectBufOther)][|>]] *[[elisp:(blee:ppmm:org-mode-toggle)][|N]]*  Func-examples :: /examples_bpo_fpBases/ =Show/Verify/Update For relevant PBDs= retType=none argsList=(bpoId cls menuLevel='chapter')  [[elisp:(org-cycle)][| ]]
"""
def examples_bpo_fpBases(
    bpoId,
    cls,
    menuLevel='chapter',
):
####+END:
    """
** Common examples.
"""
    def cpsInit(): return collections.OrderedDict()
    def menuItem(verbosity): icm.ex_gCmndMenuItem(cmndName, cps, cmndArgs, verbosity=verbosity) # 'little' or 'none'
    # def execLineEx(cmndStr): icm.ex_gExecMenuItem(execLine=cmndStr)

    # oneBpo = "pmi_ByD-100001"
    # thisClass = "PalsRepo_LiveParams"
    oneBpo = bpoId
    thisClass = cls

    if menuLevel == 'chapter':
        icm.cmndExampleMenuChapter('*BPO FILE_Params Access And Management*')
    else:
        icm.cmndExampleMenuChapter('*BPO FILE_Params Access And Management*')

    cmndName = "bpoFpParamsList" ; cmndArgs = "" ;
    cps=cpsInit() ; cps['bpoId'] = oneBpo ; cps['cls'] = thisClass
    menuItem(verbosity='little')

    # cmndArgs = "basic" ; menuItem(verbosity='little')
    cmndArgs = "basic setExamples getExamples" ; menuItem(verbosity='little')

    cmndName = "bpoFpParamsSetDefaults" ; cmndArgs = "" ;
    cps=cpsInit() ; cps['bpoId'] = oneBpo ; cps['cls'] = thisClass
    menuItem(verbosity='little')

    cmndName = "bpoFpParamsRead" ; cmndArgs = "" ;
    cps=cpsInit() ; cps['bpoId'] = oneBpo ; cps['cls'] = thisClass
    menuItem(verbosity='little')

    # cmndArgs = "basic" ; menuItem(verbosity='little')
    cmndArgs = "basic setExamples getExamples" ; menuItem(verbosity='little')


####+BEGIN: bx:dblock:python:section :title "ICM Commands"
"""
*  [[elisp:(beginning-of-buffer)][Top]] ############## [[elisp:(blee:ppmm:org-mode-toggle)][Nat]] [[elisp:(delete-other-windows)][(1)]]    *ICM Commands*  [[elisp:(org-cycle)][| ]]  [[elisp:(org-show-subtree)][|=]]
"""
####+END:


"""
*  [[elisp:(beginning-of-buffer)][Top]] ################ [[elisp:(delete-other-windows)][(1)]]      *File Parameters Get/Set -- Commands*
"""

####+BEGIN: bx:icm:python:cmnd:classHead :cmndName "bpoFpParamsList" :parsMand "bpoId cls" :parsOpt "" :argsMin "0" :argsMax "3" :asFunc "" :interactiveP ""
"""
*  _[[elisp:(blee:menu-sel:outline:popupMenu)][±]]_ _[[elisp:(blee:menu-sel:navigation:popupMenu)][Ξ]]_ [[elisp:(bx:orgm:indirectBufOther)][|>]] *[[elisp:(blee:ppmm:org-mode-toggle)][|N]]*  ICM-Cmnd   :: /bpoFpParamsList/ parsMand=bpoId cls parsOpt= argsMin=0 argsMax=3 asFunc= interactive=  [[elisp:(org-cycle)][| ]]
"""
class bpoFpParamsList(icm.Cmnd):
    cmndParamsMandatory = [ 'bpoId', 'cls', ]
    cmndParamsOptional = [ ]
    cmndArgsLen = {'Min': 0, 'Max': 3,}

    @icm.subjectToTracking(fnLoc=True, fnEntry=True, fnExit=True)
    def cmnd(self,
        interactive=False,        # Can also be called non-interactively
        bpoId=None,         # or Cmnd-Input
        cls=None,         # or Cmnd-Input
        argsList=[],         # or Args-Input
    ):
        cmndOutcome = self.getOpOutcome()
        if interactive:
            if not self.cmndLineValidate(outcome=cmndOutcome):
                return cmndOutcome
            effectiveArgsList = G.icmRunArgsGet().cmndArgs  # type: ignore
        else:
            effectiveArgsList = argsList

        callParamsDict = {'bpoId': bpoId, 'cls': cls, }
        if not icm.cmndCallParamsValidate(callParamsDict, interactive, outcome=cmndOutcome):
            return cmndOutcome
        bpoId = callParamsDict['bpoId']
        cls = callParamsDict['cls']

        cmndArgsSpecDict = self.cmndArgsSpec()
        if not self.cmndArgsValidate(effectiveArgsList, cmndArgsSpecDict, outcome=cmndOutcome):
            return cmndOutcome
####+END:
        thisBpo = palsBpo.obtainBpo(bpoId,) ; icm.unusedSuppress(thisBpo)

        # exec(
        #     "palsRepo_liveParams = __main__.{cls}('{bpoId}',)".format(cls=cls, bpoId=bpoId,),
        #     globals(),
        # )

        bpoFpBaseInst = getattr(__main__, cls)(bpoId)

        fps_base = bpoFpBaseInst.fps_baseMake()
        fps_namesWithAbsPath = fps_base.fps_namesWithAbsPath()

        if interactive:
            formatTypes = self.cmndArgsGet("0&2", cmndArgsSpecDict, effectiveArgsList)
        else:
            formatTypes = effectiveArgsList

        if formatTypes:
            if formatTypes[0] == "all":
                    cmndArgsSpec = cmndArgsSpecDict.argPositionFind("0&2")
                    argChoices = cmndArgsSpec.argChoicesGet()
                    argChoices.pop(0)
                    formatTypes = argChoices

        for each in formatTypes:    # type: ignore
            if each == 'basic':
                fp.FP_listIcmParams(fps_namesWithAbsPath,)
            elif each == 'getExamples':
                print("Get Examples Come Here")
            elif each == 'setExamples':
                print("Set Examples Come Here")
            else:
                icm.EH_problem_usageError(f"Unknown {each}")

        return cmndOutcome

####+BEGIN: bx:icm:python:method :methodName "cmndArgsSpec" :methodType "anyOrNone" :retType "bool" :deco "default" :argsList ""
    """
**  _[[elisp:(blee:menu-sel:outline:popupMenu)][±]]_ _[[elisp:(blee:menu-sel:navigation:popupMenu)][Ξ]]_ [[elisp:(bx:orgm:indirectBufOther)][|>]] *[[elisp:(blee:ppmm:org-mode-toggle)][|N]]*  Method-anyOrNone :: /cmndArgsSpec/ retType=bool argsList=nil deco=default  [[elisp:(org-cycle)][| ]]
"""
    @icm.subjectToTracking(fnLoc=True, fnEntry=True, fnExit=True)
    def cmndArgsSpec(self):
####+END:
        """
***** Cmnd Args Specification
"""
        cmndArgsSpecDict = icm.CmndArgsSpecDict()
        cmndArgsSpecDict.argsDictAdd(
            argPosition="0&2",
            argName="formatTypes",
            argDefault="all",
            argChoices=['all', 'basic', 'setExamples', 'getExamples'],
            argDescription="Action to be specified by rest"
        )

        return cmndArgsSpecDict

####+BEGIN: bx:icm:python:method :methodName "cmndDocStr" :methodType "anyOrNone" :retType "bool" :deco "default" :argsList ""
    """
**  _[[elisp:(blee:menu-sel:outline:popupMenu)][±]]_ _[[elisp:(blee:menu-sel:navigation:popupMenu)][Ξ]]_ [[elisp:(bx:orgm:indirectBufOther)][|>]] *[[elisp:(blee:ppmm:org-mode-toggle)][|N]]*  Method-anyOrNone :: /cmndDocStr/ retType=bool argsList=nil deco=default  [[elisp:(org-cycle)][| ]]
"""
    @icm.subjectToTracking(fnLoc=True, fnEntry=True, fnExit=True)
    def cmndDocStr(self):
####+END:
        return """
***** [[elisp:(org-cycle)][| *CmndDesc:* | ]]  Returns the full path of the Sr baseDir.
"""


####+BEGIN: bx:icm:python:cmnd:classHead :cmndName "bpoFpParamsSet" :parsMand "bpoId cls" :parsOpt "" :argsMin "0" :argsMax "0" :asFunc "" :interactiveP ""
"""
*  _[[elisp:(blee:menu-sel:outline:popupMenu)][±]]_ _[[elisp:(blee:menu-sel:navigation:popupMenu)][Ξ]]_ [[elisp:(bx:orgm:indirectBufOther)][|>]] *[[elisp:(blee:ppmm:org-mode-toggle)][|N]]*  ICM-Cmnd   :: /bpoFpParamsSet/ parsMand=bpoId cls parsOpt= argsMin=0 argsMax=0 asFunc= interactive=  [[elisp:(org-cycle)][| ]]
"""
class bpoFpParamsSet(icm.Cmnd):
    cmndParamsMandatory = [ 'bpoId', 'cls', ]
    cmndParamsOptional = [ ]
    cmndArgsLen = {'Min': 0, 'Max': 0,}

    @icm.subjectToTracking(fnLoc=True, fnEntry=True, fnExit=True)
    def cmnd(self,
        interactive=False,        # Can also be called non-interactively
        bpoId=None,         # or Cmnd-Input
        cls=None,         # or Cmnd-Input
    ):
        cmndOutcome = self.getOpOutcome()
        if interactive:
            if not self.cmndLineValidate(outcome=cmndOutcome):
                return cmndOutcome

        callParamsDict = {'bpoId': bpoId, 'cls': cls, }
        if not icm.cmndCallParamsValidate(callParamsDict, interactive, outcome=cmndOutcome):
            return cmndOutcome
        bpoId = callParamsDict['bpoId']
        cls = callParamsDict['cls']

####+END:
        thisBpo = palsBpo.obtainBpo(bpoId,) ; icm.unusedSuppress(thisBpo)

        bpoFpBaseInst = getattr(__main__, cls)(bpoId)
        fps_base = bpoFpBaseInst.fps_baseMake()
        fps_namesWithAbsPath = fps_base.fps_namesWithAbsPath()

        fp.FP_writeWithIcmParams(fps_namesWithAbsPath,)

        return cmndOutcome

####+BEGIN: bx:icm:python:method :methodName "cmndDocStr" :methodType "anyOrNone" :retType "bool" :deco "default" :argsList ""
    """
**  _[[elisp:(blee:menu-sel:outline:popupMenu)][±]]_ _[[elisp:(blee:menu-sel:navigation:popupMenu)][Ξ]]_ [[elisp:(bx:orgm:indirectBufOther)][|>]] *[[elisp:(blee:ppmm:org-mode-toggle)][|N]]*  Method-anyOrNone :: /cmndDocStr/ retType=bool argsList=nil deco=default  [[elisp:(org-cycle)][| ]]
"""
    @icm.subjectToTracking(fnLoc=True, fnEntry=True, fnExit=True)
    def cmndDocStr(self):
####+END:
        return """
***** [[elisp:(org-cycle)][| *CmndDesc:* | ]]  Returns the full path of the Sr baseDir.
"""


####+BEGIN: bx:icm:python:cmnd:classHead :cmndName "bpoFpParamsSetDefaults" :parsMand "bpoId cls" :parsOpt "" :argsMin "0" :argsMax "0" :asFunc "" :interactiveP ""
"""
*  _[[elisp:(blee:menu-sel:outline:popupMenu)][±]]_ _[[elisp:(blee:menu-sel:navigation:popupMenu)][Ξ]]_ [[elisp:(bx:orgm:indirectBufOther)][|>]] *[[elisp:(blee:ppmm:org-mode-toggle)][|N]]*  ICM-Cmnd   :: /bpoFpParamsSetDefaults/ parsMand=bpoId cls parsOpt= argsMin=0 argsMax=0 asFunc= interactive=  [[elisp:(org-cycle)][| ]]
"""
class bpoFpParamsSetDefaults(icm.Cmnd):
    cmndParamsMandatory = [ 'bpoId', 'cls', ]
    cmndParamsOptional = [ ]
    cmndArgsLen = {'Min': 0, 'Max': 0,}

    @icm.subjectToTracking(fnLoc=True, fnEntry=True, fnExit=True)
    def cmnd(self,
        interactive=False,        # Can also be called non-interactively
        bpoId=None,         # or Cmnd-Input
        cls=None,         # or Cmnd-Input
    ):
        cmndOutcome = self.getOpOutcome()
        if interactive:
            if not self.cmndLineValidate(outcome=cmndOutcome):
                return cmndOutcome

        callParamsDict = {'bpoId': bpoId, 'cls': cls, }
        if not icm.cmndCallParamsValidate(callParamsDict, interactive, outcome=cmndOutcome):
            return cmndOutcome
        bpoId = callParamsDict['bpoId']
        cls = callParamsDict['cls']

####+END:
        thisBpo = palsBpo.obtainBpo(bpoId,) ; icm.unusedSuppress(thisBpo)

        bpoFpBaseInst = getattr(__main__, cls)(bpoId)
        fps_base = bpoFpBaseInst.fps_baseMake()
        fps_namesWithAbsPath = fps_base.fps_namesWithAbsPath()

        fp.FP_writeDefaultsWithIcmParams(fps_namesWithAbsPath,)

        return cmndOutcome

####+BEGIN: bx:icm:python:method :methodName "cmndDocStr" :methodType "anyOrNone" :retType "bool" :deco "default" :argsList ""
    """
**  _[[elisp:(blee:menu-sel:outline:popupMenu)][±]]_ _[[elisp:(blee:menu-sel:navigation:popupMenu)][Ξ]]_ [[elisp:(bx:orgm:indirectBufOther)][|>]] *[[elisp:(blee:ppmm:org-mode-toggle)][|N]]*  Method-anyOrNone :: /cmndDocStr/ retType=bool argsList=nil deco=default  [[elisp:(org-cycle)][| ]]
"""
    @icm.subjectToTracking(fnLoc=True, fnEntry=True, fnExit=True)
    def cmndDocStr(self):
####+END:
        return """
***** [[elisp:(org-cycle)][| *CmndDesc:* | ]]  Returns the full path of the Sr baseDir.
"""


####+BEGIN: bx:icm:python:cmnd:classHead :cmndName "bpoFpParamSetWithNameValue" :parsMand "bpoId cls" :parsOpt "" :argsMin "2" :argsMax "2" :asFunc "" :interactiveP ""
"""
*  _[[elisp:(blee:menu-sel:outline:popupMenu)][±]]_ _[[elisp:(blee:menu-sel:navigation:popupMenu)][Ξ]]_ [[elisp:(bx:orgm:indirectBufOther)][|>]] *[[elisp:(blee:ppmm:org-mode-toggle)][|N]]*  ICM-Cmnd   :: /bpoFpParamSetWithNameValue/ parsMand=bpoId cls parsOpt= argsMin=2 argsMax=2 asFunc= interactive=  [[elisp:(org-cycle)][| ]]
"""
class bpoFpParamSetWithNameValue(icm.Cmnd):
    cmndParamsMandatory = [ 'bpoId', 'cls', ]
    cmndParamsOptional = [ ]
    cmndArgsLen = {'Min': 2, 'Max': 2,}

    @icm.subjectToTracking(fnLoc=True, fnEntry=True, fnExit=True)
    def cmnd(self,
        interactive=False,        # Can also be called non-interactively
        bpoId=None,         # or Cmnd-Input
        cls=None,         # or Cmnd-Input
        argsList=[],         # or Args-Input
    ):
        cmndOutcome = self.getOpOutcome()
        if interactive:
            if not self.cmndLineValidate(outcome=cmndOutcome):
                return cmndOutcome
            effectiveArgsList = G.icmRunArgsGet().cmndArgs  # type: ignore
        else:
            effectiveArgsList = argsList

        callParamsDict = {'bpoId': bpoId, 'cls': cls, }
        if not icm.cmndCallParamsValidate(callParamsDict, interactive, outcome=cmndOutcome):
            return cmndOutcome
        bpoId = callParamsDict['bpoId']
        cls = callParamsDict['cls']

        cmndArgsSpecDict = self.cmndArgsSpec()
        if not self.cmndArgsValidate(effectiveArgsList, cmndArgsSpecDict, outcome=cmndOutcome):
            return cmndOutcome
####+END:
        paramName = self.cmndArgsGet("0", cmndArgsSpecDict, effectiveArgsList)
        paramValue = self.cmndArgsGet("1", cmndArgsSpecDict, effectiveArgsList)

        print(f"{paramName} {paramValue}")

        thisBpo = palsBpo.obtainBpo(bpoId,) ; icm.unusedSuppress(thisBpo)

        bpoFpBaseInst = getattr(__main__, cls)(bpoId)

        fpsBaseInst = bpoFpBaseInst.fps_baseMake()

        fpsBaseInst.fps_setParam(paramName, paramValue)

        return cmndOutcome


####+BEGIN: bx:icm:python:method :methodName "cmndArgsSpec" :methodType "anyOrNone" :retType "bool" :deco "default" :argsList ""
    """
**  _[[elisp:(blee:menu-sel:outline:popupMenu)][±]]_ _[[elisp:(blee:menu-sel:navigation:popupMenu)][Ξ]]_ [[elisp:(bx:orgm:indirectBufOther)][|>]] *[[elisp:(blee:ppmm:org-mode-toggle)][|N]]*  Method-anyOrNone :: /cmndArgsSpec/ retType=bool argsList=nil deco=default  [[elisp:(org-cycle)][| ]]
"""
    @icm.subjectToTracking(fnLoc=True, fnEntry=True, fnExit=True)
    def cmndArgsSpec(self):
####+END:
        """
***** Cmnd Args Specification
"""
        cmndArgsSpecDict = icm.CmndArgsSpecDict()
        cmndArgsSpecDict.argsDictAdd(
            argPosition="0",
            argName="paramName",
            argDefault="OopsName",
            argChoices=[],
            argDescription="Action to be specified by rest"
        )
        cmndArgsSpecDict.argsDictAdd(
            argPosition="1",
            argName="paramValue",
            argDefault="OopsValue",
            argChoices=[],
            argDescription="Action to be specified by rest"
        )

        return cmndArgsSpecDict



####+BEGIN: bx:icm:python:cmnd:classHead :cmndName "bpoFpParamGetWithName" :parsMand "bpoId cls" :parsOpt "" :argsMin "1" :argsMax "1" :asFunc "" :interactiveP ""
"""
*  _[[elisp:(blee:menu-sel:outline:popupMenu)][±]]_ _[[elisp:(blee:menu-sel:navigation:popupMenu)][Ξ]]_ [[elisp:(bx:orgm:indirectBufOther)][|>]] *[[elisp:(blee:ppmm:org-mode-toggle)][|N]]*  ICM-Cmnd   :: /bpoFpParamGetWithName/ parsMand=bpoId cls parsOpt= argsMin=1 argsMax=1 asFunc= interactive=  [[elisp:(org-cycle)][| ]]
"""
class bpoFpParamGetWithName(icm.Cmnd):
    cmndParamsMandatory = [ 'bpoId', 'cls', ]
    cmndParamsOptional = [ ]
    cmndArgsLen = {'Min': 1, 'Max': 1,}

    @icm.subjectToTracking(fnLoc=True, fnEntry=True, fnExit=True)
    def cmnd(self,
        interactive=False,        # Can also be called non-interactively
        bpoId=None,         # or Cmnd-Input
        cls=None,         # or Cmnd-Input
        argsList=[],         # or Args-Input
    ):
        cmndOutcome = self.getOpOutcome()
        if interactive:
            if not self.cmndLineValidate(outcome=cmndOutcome):
                return cmndOutcome
            effectiveArgsList = G.icmRunArgsGet().cmndArgs  # type: ignore
        else:
            effectiveArgsList = argsList

        callParamsDict = {'bpoId': bpoId, 'cls': cls, }
        if not icm.cmndCallParamsValidate(callParamsDict, interactive, outcome=cmndOutcome):
            return cmndOutcome
        bpoId = callParamsDict['bpoId']
        cls = callParamsDict['cls']

        cmndArgsSpecDict = self.cmndArgsSpec()
        if not self.cmndArgsValidate(effectiveArgsList, cmndArgsSpecDict, outcome=cmndOutcome):
            return cmndOutcome
####+END:
        paramName = self.cmndArgsGet("0", cmndArgsSpecDict, effectiveArgsList)

        thisBpo = palsBpo.obtainBpo(bpoId,) ; icm.unusedSuppress(thisBpo)

        bpoFpBaseInst = getattr(__main__, cls)(bpoId)

        fpsBaseInst = bpoFpBaseInst.fps_baseMake()

        paramValue = fpsBaseInst.fps_getParam(paramName,)

        print(f"{paramValue.parValueGet()}")

        return cmndOutcome


####+BEGIN: bx:icm:python:method :methodName "cmndArgsSpec" :methodType "anyOrNone" :retType "bool" :deco "default" :argsList ""
    """
**  _[[elisp:(blee:menu-sel:outline:popupMenu)][±]]_ _[[elisp:(blee:menu-sel:navigation:popupMenu)][Ξ]]_ [[elisp:(bx:orgm:indirectBufOther)][|>]] *[[elisp:(blee:ppmm:org-mode-toggle)][|N]]*  Method-anyOrNone :: /cmndArgsSpec/ retType=bool argsList=nil deco=default  [[elisp:(org-cycle)][| ]]
"""
    @icm.subjectToTracking(fnLoc=True, fnEntry=True, fnExit=True)
    def cmndArgsSpec(self):
####+END:
        """
***** Cmnd Args Specification
"""
        cmndArgsSpecDict = icm.CmndArgsSpecDict()
        cmndArgsSpecDict.argsDictAdd(
            argPosition="0",
            argName="paramName",
            argDefault="OopsName",
            argChoices=[],
            argDescription="Action to be specified by rest"
        )

        return cmndArgsSpecDict



####+BEGINNOT: bx:icm:python:cmnd:classHead :cmndName "bpoFpParamsRead" :parsMand "bpoId cls" :parsOpt "" :argsMin "0" :argsMax "999" :asFunc "" :interactiveP ""
"""
*  _[[elisp:(blee:menu-sel:outline:popupMenu)][±]]_ _[[elisp:(blee:menu-sel:navigation:popupMenu)][Ξ]]_ [[elisp:(bx:orgm:indirectBufOther)][|>]] *[[elisp:(blee:ppmm:org-mode-toggle)][|N]]*  ICM-Cmnd   :: /bpoFpParamsRead/ parsMand=bpoId cls parsOpt= argsMin=0 argsMax=999 asFunc= interactive=  [[elisp:(org-cycle)][| ]]
"""
class bpoFpParamsRead(icm.Cmnd):
    cmndParamsMandatory = [ 'bpoId', 'cls', ]
    cmndParamsOptional = [ ]
    cmndArgsLen = {'Min': 0, 'Max': 999,}

    @icm.subjectToTracking(fnLoc=True, fnEntry=True, fnExit=True)
    def cmnd(self,
        interactive=False,        # Can also be called non-interactively
        bpoId=None,         # or Cmnd-Input
        cls=None,         # or Cmnd-Input
        argsList=[],         # or Args-Input
    ):
        cmndOutcome = self.getOpOutcome()
        if interactive:
            if not self.cmndLineValidate(outcome=cmndOutcome):
                return cmndOutcome
            effectiveArgsList = G.icmRunArgsGet().cmndArgs  # type: ignore
        else:
            effectiveArgsList = argsList

        callParamsDict = {'bpoId': bpoId, 'cls': cls, }
        if not icm.cmndCallParamsValidate(callParamsDict, interactive, outcome=cmndOutcome):
            return cmndOutcome
        bpoId = callParamsDict['bpoId']
        cls = callParamsDict['cls']

        cmndArgsSpecDict = self.cmndArgsSpec(bpoId, cls)
        if not self.cmndArgsValidate(effectiveArgsList, cmndArgsSpecDict, outcome=cmndOutcome):
            return cmndOutcome
####+END:
        thisBpo = palsBpo.obtainBpo(bpoId,) ; icm.unusedSuppress(thisBpo)

        bpoFpBaseInst = getattr(__main__, cls)(bpoId)
        fpBaseDir = bpoFpBaseInst.fps_absBasePath()

        if interactive:
            formatTypes = self.cmndArgsGet("0&999", cmndArgsSpecDict, effectiveArgsList)
        else:
            formatTypes = effectiveArgsList

        for each in formatTypes:  # type: ignore
            if each == 'all':
                icm.LOG_here(f"""format={each} -- fpBaseDir={fpBaseDir}""")
                fp.FP_readTreeAtBaseDir_CmndOutput(
                    interactive=interactive,
                    fpBaseDir=fpBaseDir,
                    cmndOutcome=cmndOutcome,
                )
            else:
                icm.LOG_here(f"""format={each} -- fpBaseDir={fpBaseDir}""")

                filePar = icm.FILE_ParamReadFrom(
                    parRoot=fpBaseDir,
                    parName=each,
                )
                print(filePar.parValueGet())   # type: ignore

        return cmndOutcome

####+BEGIN: bx:icm:python:method :methodName "cmndArgsSpec" :methodType "anyOrNone" :retType "bool" :deco "default" :argsList "bpoId cls"
    """
**  _[[elisp:(blee:menu-sel:outline:popupMenu)][±]]_ _[[elisp:(blee:menu-sel:navigation:popupMenu)][Ξ]]_ [[elisp:(bx:orgm:indirectBufOther)][|>]] *[[elisp:(blee:ppmm:org-mode-toggle)][|N]]*  Method-anyOrNone :: /cmndArgsSpec/ retType=bool argsList=(bpoId cls) deco=default  [[elisp:(org-cycle)][| ]]
"""
    @icm.subjectToTracking(fnLoc=True, fnEntry=True, fnExit=True)
    def cmndArgsSpec(
        self,
        bpoId,
        cls,
    ):
####+END:
        """
***** Cmnd Args Specification
"""
        cmndArgsSpecDict = icm.CmndArgsSpecDict()
        argChoices = ['all', 'obj']

        thisBpo = palsBpo.obtainBpo(bpoId,) ; icm.unusedSuppress(thisBpo)

        bpoFpBaseInst = getattr(__main__, cls)(bpoId)
        fps_base = bpoFpBaseInst.fps_baseMake() # type: ignore
        for each in fps_base.fps_namesWithRelPath():
            argChoices.append(each)

        cmndArgsSpecDict.argsDictAdd(
            argPosition="0&999",
            argName="formatTypes",
            argDefault="all",
            argChoices=argChoices,
            argDescription="One, many or all"
        )

        return cmndArgsSpecDict

####+BEGIN: bx:icm:python:method :methodName "cmndDocStr" :methodType "anyOrNone" :retType "bool" :deco "default" :argsList ""
    """
**  _[[elisp:(blee:menu-sel:outline:popupMenu)][±]]_ _[[elisp:(blee:menu-sel:navigation:popupMenu)][Ξ]]_ [[elisp:(bx:orgm:indirectBufOther)][|>]] *[[elisp:(blee:ppmm:org-mode-toggle)][|N]]*  Method-anyOrNone :: /cmndDocStr/ retType=bool argsList=nil deco=default  [[elisp:(org-cycle)][| ]]
"""
    @icm.subjectToTracking(fnLoc=True, fnEntry=True, fnExit=True)
    def cmndDocStr(self):
####+END:
        return """
***** [[elisp:(org-cycle)][| *CmndDesc:* | ]]  Returns the full path of the Sr baseDir.
"""



####+BEGIN: bx:icm:python:section :title "End Of Editable Text"
"""
*  [[elisp:(beginning-of-buffer)][Top]] ############## [[elisp:(blee:ppmm:org-mode-toggle)][Nat]] [[elisp:(delete-other-windows)][(1)]]    *End Of Editable Text*  [[elisp:(org-cycle)][| ]]  [[elisp:(org-show-subtree)][|=]]
"""
####+END:

####+BEGIN: bx:dblock:global:file-insert-cond :cond "./blee.el" :file "/bisos/apps/defaults/software/plusOrg/dblock/inserts/endOfFileControls.org"
#+STARTUP: showall
####+END:
