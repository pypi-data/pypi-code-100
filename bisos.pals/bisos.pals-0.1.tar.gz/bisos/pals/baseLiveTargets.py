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
icmInfo['moduleName'] = "baseLiveTargets"
####+END:

####+BEGIN: bx:icm:py:version-timestamp :style "date"
icmInfo['version'] = "202110151523"
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
*  This file:/bisos/git/auth/bxRepos/bisos-pip/pals/py3/bisos/pals/baseLiveTargets.py :: [[elisp:(org-cycle)][| ]]
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


import os
import collections
import pathlib
import invoke

####+BEGIN: bx:dblock:global:file-insert-cond :cond "./blee.el" :file "/bisos/apps/defaults/update/sw/icm/py/importUcfIcmG.py"
from unisos import ucf
from unisos import icm

icm.unusedSuppressForEval(ucf.__file__)  # in case icm and ucf are not used

G = icm.IcmGlobalContext()
# G.icmLibsAppend = __file__
# G.icmCmndsLibsAppend = __file__
####+END:

from bisos.basics import pattern
from bisos.icm import fp
# from bisos.bpo import bpo
from bisos.bpo import bpoFpBases
from bisos.pals import palsBpo
# from bisos.pals import palsRepo
from bisos.pals import repoLiveParams
from bisos.cntnr import curFps
from bisos.icm import fpath

####+BEGIN: bx:dblock:python:section :title "Class Definitions"
"""
*  [[elisp:(beginning-of-buffer)][Top]] ############## [[elisp:(blee:ppmm:org-mode-toggle)][Nat]] [[elisp:(delete-other-windows)][(1)]]    *Class Definitions*  [[elisp:(org-cycle)][| ]]  [[elisp:(org-show-subtree)][|=]]
"""
####+END:

####+BEGIN: bx:dblock:python:class :className "PalsBase_LiveTargets" :superClass "bpoFpBases.BpoFpBase" :comment "" :classType "basic"
"""
*  _[[elisp:(blee:menu-sel:outline:popupMenu)][±]]_ _[[elisp:(blee:menu-sel:navigation:popupMenu)][Ξ]]_ [[elisp:(bx:orgm:indirectBufOther)][|>]] *[[elisp:(blee:ppmm:org-mode-toggle)][|N]]*  Class-basic :: /PalsBase_LiveTargets/ bpoFpBases.BpoFpBase  [[elisp:(org-cycle)][| ]]
"""
class PalsBase_LiveTargets(bpoFpBases.BpoFpBase):
####+END:
    """
** Abstraction of the PalsBase for LiveTargets
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
    ):
        self.bpoId = bpoId
        self.thisPalsBpo = palsBpo.obtainBpo(bpoId)


####+BEGIN: bx:icm:py3:method :methodName "fps_absBasePath" :deco "default"
    """
**  _[[elisp:(blee:menu-sel:outline:popupMenu)][±]]_ _[[elisp:(blee:menu-sel:navigation:popupMenu)][Ξ]]_ [[elisp:(bx:orgm:indirectBufOther)][|>]] *[[elisp:(blee:ppmm:org-mode-toggle)][|N]]*  Method-    :: /fps_absBasePath/ deco=default  [[elisp:(org-cycle)][| ]]
"""
    @icm.subjectToTracking(fnLoc=True, fnEntry=True, fnExit=True)
    def fps_absBasePath(
####+END:
           self,
    ):
        return typing.cast(str, self.basePath_obtain())


####+BEGIN: bx:icm:py3:method :methodName "basePath_obtain" :deco "default"
    """
**  _[[elisp:(blee:menu-sel:outline:popupMenu)][±]]_ _[[elisp:(blee:menu-sel:navigation:popupMenu)][Ξ]]_ [[elisp:(bx:orgm:indirectBufOther)][|>]] *[[elisp:(blee:ppmm:org-mode-toggle)][|N]]*  Method-    :: /basePath_obtain/ deco=default  [[elisp:(org-cycle)][| ]]
"""
    @icm.subjectToTracking(fnLoc=True, fnEntry=True, fnExit=True)
    def basePath_obtain(
####+END:
           self,
    ) -> pathlib.Path:
        palsControlPath = self.thisPalsBpo.bases.controlBasePath_obtain()
        return (
            pathlib.Path(
                os.path.join(
                    palsControlPath,
                    "liveTargets",
                )
            )
        )

####+BEGIN: bx:icm:py3:method :methodName "basePath_update" :deco "default"
    """
**  _[[elisp:(blee:menu-sel:outline:popupMenu)][±]]_ _[[elisp:(blee:menu-sel:navigation:popupMenu)][Ξ]]_ [[elisp:(bx:orgm:indirectBufOther)][|>]] *[[elisp:(blee:ppmm:org-mode-toggle)][|N]]*  Method-    :: /basePath_update/ deco=default  [[elisp:(org-cycle)][| ]]
"""
    @icm.subjectToTracking(fnLoc=True, fnEntry=True, fnExit=True)
    def basePath_update(
####+END:
           self,
    ) -> pathlib.Path:
        liveTargetsPalsPath = self.basePath_obtain()
        liveTargetsPalsPath.mkdir(parents=True, exist_ok=True)
        return liveTargetsPalsPath

####+BEGIN: bx:icm:py3:method :methodName "targetParamsPath_obtain" :deco "default"
    """
**  _[[elisp:(blee:menu-sel:outline:popupMenu)][±]]_ _[[elisp:(blee:menu-sel:navigation:popupMenu)][Ξ]]_ [[elisp:(bx:orgm:indirectBufOther)][|>]] *[[elisp:(blee:ppmm:org-mode-toggle)][|N]]*  Method-    :: /targetParamsPath_obtain/ deco=default  [[elisp:(org-cycle)][| ]]
"""
    @icm.subjectToTracking(fnLoc=True, fnEntry=True, fnExit=True)
    def targetParamsPath_obtain(
####+END:
           self,
    ) -> pathlib.Path:
        liveTargetsPalsPath = self.basePath_obtain()
        return (
            pathlib.Path(
                os.path.join(
                    liveTargetsPalsPath,
                    "targetParams",
                )
            )
        )

####+BEGIN: bx:icm:py3:method :methodName "fps_baseMake" :deco "default"
    """
**  _[[elisp:(blee:menu-sel:outline:popupMenu)][±]]_ _[[elisp:(blee:menu-sel:navigation:popupMenu)][Ξ]]_ [[elisp:(bx:orgm:indirectBufOther)][|>]] *[[elisp:(blee:ppmm:org-mode-toggle)][|N]]*  Method-    :: /fps_baseMake/ deco=default  [[elisp:(org-cycle)][| ]]
"""
    @icm.subjectToTracking(fnLoc=True, fnEntry=True, fnExit=True)
    def fps_baseMake(
####+END:
            self,
    ):
        #palsControlPath = self.basePath_obtain()
        fpsPath = self.basePath_obtain()
        self.fpsBaseInst = PalsBase_LiveTargets_FPs(
            fpsPath,
        )
        return self.fpsBaseInst

####+BEGIN: bx:dblock:python:class :className "PalsBase_LiveTargets_FPs" :superClass "fp.FP_Base" :comment "Expected to be subclassed" :classType "basic"
"""
*  _[[elisp:(blee:menu-sel:outline:popupMenu)][±]]_ _[[elisp:(blee:menu-sel:navigation:popupMenu)][Ξ]]_ [[elisp:(bx:orgm:indirectBufOther)][|>]] *[[elisp:(blee:ppmm:org-mode-toggle)][|N]]*  Class-basic :: /PalsBase_LiveTargets_FPs/ fp.FP_Base =Expected to be subclassed=  [[elisp:(org-cycle)][| ]]
"""
class PalsBase_LiveTargets_FPs(fp.FP_Base):
####+END:
    """ Representation of a FILE_TreeObject when _objectType_ is FILE_ParamBase (a node).
    """

####+BEGIN: bx:icm:py3:method :methodName "__init__" :deco "default"
    """
**  _[[elisp:(blee:menu-sel:outline:popupMenu)][±]]_ _[[elisp:(blee:menu-sel:navigation:popupMenu)][Ξ]]_ [[elisp:(bx:orgm:indirectBufOther)][|>]] *[[elisp:(blee:ppmm:org-mode-toggle)][|N]]*  Method-    :: /__init__/ deco=default  [[elisp:(org-cycle)][| ]]
"""
    @icm.subjectToTracking(fnLoc=True, fnEntry=True, fnExit=True)
    def __init__(
####+END:
            self,
            fileSysPath,
    ):
        """Representation of a FILE_TreeObject when _objectType_ is FILE_ParamBase (a node)."""
        super().__init__(fileSysPath,)

####+BEGIN: bx:icm:py3:method :methodName "fps_asIcmParamsAdd" :deco "staticmethod"
    """
**  _[[elisp:(blee:menu-sel:outline:popupMenu)][±]]_ _[[elisp:(blee:menu-sel:navigation:popupMenu)][Ξ]]_ [[elisp:(bx:orgm:indirectBufOther)][|>]] *[[elisp:(blee:ppmm:org-mode-toggle)][|N]]*  Method-    :: /fps_asIcmParamsAdd/ deco=staticmethod  [[elisp:(org-cycle)][| ]]
"""
    @staticmethod
    def fps_asIcmParamsAdd(
####+END:
            icmParams,
    ):
        """staticmethod: takes in icmParms and augments it with fileParams. returns icmParams."""
        icmParams.parDictAdd(
            parName='palsLiveTargetMode',
            parDescription="",
            parDataType=None,
            parDefault=None,
            parChoices=list(),
            parScope=icm.ICM_ParamScope.TargetParam,  # type: ignore
            argparseShortOpt=None,
            argparseLongOpt='--palsLiveTargetMode',
        )

        return icmParams


####+BEGIN: bx:icm:py3:method :methodName "fps_namesWithRelPath" :deco "classmethod"
    """
**  _[[elisp:(blee:menu-sel:outline:popupMenu)][±]]_ _[[elisp:(blee:menu-sel:navigation:popupMenu)][Ξ]]_ [[elisp:(bx:orgm:indirectBufOther)][|>]] *[[elisp:(blee:ppmm:org-mode-toggle)][|N]]*  Method-    :: /fps_namesWithRelPath/ deco=classmethod  [[elisp:(org-cycle)][| ]]
"""
    @classmethod
    def fps_namesWithRelPath(
####+END:
            cls,
    ):
        """classmethod: returns a dict with fp names as key and relBasePath as value.
        The names refer to icmParams.parDictAdd(parName) of fps_asIcmParamsAdd
        """
        relBasePath = "."
        return (
            {
                'palsLiveTargetMode': relBasePath,
            }
        )


####+BEGIN: bx:dblock:python:class :className "PalsBase_LiveParams" :superClass "object" :comment "" :classType "basic"
"""
*  _[[elisp:(blee:menu-sel:outline:popupMenu)][±]]_ _[[elisp:(blee:menu-sel:navigation:popupMenu)][Ξ]]_ [[elisp:(bx:orgm:indirectBufOther)][|>]] *[[elisp:(blee:ppmm:org-mode-toggle)][|N]]*  Class-basic :: /PalsBase_LiveParams/ object  [[elisp:(org-cycle)][| ]]
"""
class PalsBase_LiveParams(object):
####+END:
    """
** Abstraction of the PalsBase for LiveTargets
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
    ):
        self.bpoId = bpoId
        self.thisPalsBpo = palsBpo.obtainBpo(bpoId)


####+BEGIN: bx:icm:py3:method :methodName "fps_absBasePath" :deco "default"
    """
**  _[[elisp:(blee:menu-sel:outline:popupMenu)][±]]_ _[[elisp:(blee:menu-sel:navigation:popupMenu)][Ξ]]_ [[elisp:(bx:orgm:indirectBufOther)][|>]] *[[elisp:(blee:ppmm:org-mode-toggle)][|N]]*  Method-    :: /fps_absBasePath/ deco=default  [[elisp:(org-cycle)][| ]]
"""
    @icm.subjectToTracking(fnLoc=True, fnEntry=True, fnExit=True)
    def fps_absBasePath(
####+END:
           self,
    ):
        return typing.cast(str, self.basePath_obtain())


####+BEGIN: bx:icm:py3:method :methodName "basePath_obtain" :deco "default"
    """
**  _[[elisp:(blee:menu-sel:outline:popupMenu)][±]]_ _[[elisp:(blee:menu-sel:navigation:popupMenu)][Ξ]]_ [[elisp:(bx:orgm:indirectBufOther)][|>]] *[[elisp:(blee:ppmm:org-mode-toggle)][|N]]*  Method-    :: /basePath_obtain/ deco=default  [[elisp:(org-cycle)][| ]]
"""
    @icm.subjectToTracking(fnLoc=True, fnEntry=True, fnExit=True)
    def basePath_obtain(
####+END:
           self,
    ) -> pathlib.Path:
        palsControlPath = self.thisPalsBpo.bases.controlBasePath_obtain()
        return (
            pathlib.Path(
                os.path.join(
                    palsControlPath,
                    "liveTargets",
                    "targetParams"
                )
            )
        )


####+BEGIN: bx:icm:py3:method :methodName "basePath_update" :deco "default"
    """
**  _[[elisp:(blee:menu-sel:outline:popupMenu)][±]]_ _[[elisp:(blee:menu-sel:navigation:popupMenu)][Ξ]]_ [[elisp:(bx:orgm:indirectBufOther)][|>]] *[[elisp:(blee:ppmm:org-mode-toggle)][|N]]*  Method-    :: /basePath_update/ deco=default  [[elisp:(org-cycle)][| ]]
"""
    @icm.subjectToTracking(fnLoc=True, fnEntry=True, fnExit=True)
    def basePath_update(
####+END:
           self,
    ) -> pathlib.Path:
        liveTargetsPalsPath = self.basePath_obtain()
        liveTargetsPalsPath.mkdir(parents=True, exist_ok=True)
        return liveTargetsPalsPath


####+BEGIN: bx:icm:py3:method :methodName "fps_baseMake" :deco "default"
    """
**  _[[elisp:(blee:menu-sel:outline:popupMenu)][±]]_ _[[elisp:(blee:menu-sel:navigation:popupMenu)][Ξ]]_ [[elisp:(bx:orgm:indirectBufOther)][|>]] *[[elisp:(blee:ppmm:org-mode-toggle)][|N]]*  Method-    :: /fps_baseMake/ deco=default  [[elisp:(org-cycle)][| ]]
"""
    @icm.subjectToTracking(fnLoc=True, fnEntry=True, fnExit=True)
    def fps_baseMake(
####+END:
            self,
    ):
        #palsControlPath = self.basePath_obtain()
        fpsPath = self.basePath_obtain()
        self.fpsBaseInst = repoLiveParams.PalsRepo_LiveParams_FPs(
            fpsPath,
        )
        return self.fpsBaseInst



####+BEGIN: bx:dblock:python:section :title "ICM Commands"
"""
*  [[elisp:(beginning-of-buffer)][Top]] ############## [[elisp:(blee:ppmm:org-mode-toggle)][Nat]] [[elisp:(delete-other-windows)][(1)]]    *ICM Commands*  [[elisp:(org-cycle)][| ]]  [[elisp:(org-show-subtree)][|=]]
"""
####+END:


####+BEGIN: bx:icm:python:cmnd:classHead :cmndName "examples_baseLiveTargets" :cmndType "ICM-Cmnd-FWrk"  :comment "FrameWrk: ICM Examples" :parsMand "bpoId" :parsOpt "" :argsMin "0" :argsMax "0" :asFunc "" :interactiveP ""
"""
*  _[[elisp:(blee:menu-sel:outline:popupMenu)][±]]_ _[[elisp:(blee:menu-sel:navigation:popupMenu)][Ξ]]_ [[elisp:(bx:orgm:indirectBufOther)][|>]] *[[elisp:(blee:ppmm:org-mode-toggle)][|N]]*  ICM-Cmnd-FWrk :: /examples_baseLiveTargets/ =FrameWrk: ICM Examples= parsMand=bpoId parsOpt= argsMin=0 argsMax=0 asFunc= interactive=  [[elisp:(org-cycle)][| ]]
"""
class examples_baseLiveTargets(icm.Cmnd):
    cmndParamsMandatory = [ 'bpoId', ]
    cmndParamsOptional = [ ]
    cmndArgsLen = {'Min': 0, 'Max': 0,}

    @icm.subjectToTracking(fnLoc=True, fnEntry=True, fnExit=True)
    def cmnd(self,
        interactive=False,        # Can also be called non-interactively
        bpoId=None,         # or Cmnd-Input
    ):
        cmndOutcome = self.getOpOutcome()
        if interactive:
            if not self.cmndLineValidate(outcome=cmndOutcome):
                return cmndOutcome

        callParamsDict = {'bpoId': bpoId, }
        if not icm.cmndCallParamsValidate(callParamsDict, interactive, outcome=cmndOutcome):
            return cmndOutcome
        bpoId = callParamsDict['bpoId']

####+END:
        def cpsInit(): return collections.OrderedDict()
        def menuItem(verbosity): icm.ex_gCmndMenuItem(cmndName, cps, cmndArgs, verbosity=verbosity) # 'little' or 'none'
        # def execLineEx(cmndStr): icm.ex_gExecMenuItem(execLine=cmndStr)

        # oneBpo = "pmi_ByD-100001"
        # oneRepo= "par_live"

        oneBpo = bpoId

        icm.cmndExampleMenuChapter('=Misc=  *Facilities*')

        cmndName = "liveTargetsSetup" ; cmndArgs = "" ;
        cps=cpsInit() ; cps['bpoId'] = oneBpo
        menuItem(verbosity='little')

        thisClass = "PalsBase_LiveTargets"

        bpoFpBases.examples_bpo_fpBases(bpoId, thisClass)

        icm.cmndExampleMenuChapter('=PalsBase_LiveTargets=  *Access And Management*')

        cmndName = "bpoFpParamsSet" ; cmndArgs = "" ;
        cps=cpsInit() ; cps['bpoId'] = oneBpo ; cps['cls'] = thisClass

        cps['palsLiveTargetMode'] = "live"
        menuItem(verbosity='little')

        cps['palsLiveTargetMode'] = "here"
        menuItem(verbosity='little')

        icm.cmndExampleMenuChapter('=LiveParams=  *Facilities*')

        bpoFpBases.examples_bpo_fpBases(bpoId, "PalsBase_LiveParams")

        repoLiveParams.examples_repoLiveParams_basic(bpoId=bpoId, className='PalsBase_LiveParams')

        icm.cmndExampleMenuChapter('=Set Target Mode=  *Facilities*')

        cmndName = "targetModeSet"
        cps=cpsInit() ; cps['bpoId'] = oneBpo

        cmndArgs = "live" ; menuItem(verbosity='little')
        cmndArgs = "here" ; menuItem(verbosity='little')

        cmndName = "bpoFpParamSetWithNameValue"
        cps=cpsInit() ; cps['bpoId'] = oneBpo ; cps['cls'] = "PalsBase_LiveTargets"
        cmndArgs = "palsLiveTargetMode here" ; menuItem(verbosity='little')
        cmndArgs = "palsLiveTargetMode live" ; menuItem(verbosity='little')


        cmndName = "bpoFpParamGetWithName"
        cps=cpsInit() ; cps['bpoId'] = oneBpo ; cps['cls'] = "PalsBase_LiveTargets"
        cmndArgs = "palsLiveTargetMode" ; menuItem(verbosity='little')

        return(cmndOutcome)


####+BEGIN: bx:icm:python:cmnd:classHead :cmndName "liveTargetsSetup" :parsMand "bpoId" :parsOpt "" :argsMin "0" :argsMax "0" :asFunc "" :interactiveP ""
"""
*  _[[elisp:(blee:menu-sel:outline:popupMenu)][±]]_ _[[elisp:(blee:menu-sel:navigation:popupMenu)][Ξ]]_ [[elisp:(bx:orgm:indirectBufOther)][|>]] *[[elisp:(blee:ppmm:org-mode-toggle)][|N]]*  ICM-Cmnd   :: /liveTargetsSetup/ parsMand=bpoId parsOpt= argsMin=0 argsMax=0 asFunc= interactive=  [[elisp:(org-cycle)][| ]]
"""
class liveTargetsSetup(icm.Cmnd):
    cmndParamsMandatory = [ 'bpoId', ]
    cmndParamsOptional = [ ]
    cmndArgsLen = {'Min': 0, 'Max': 0,}

    @icm.subjectToTracking(fnLoc=True, fnEntry=True, fnExit=True)
    def cmnd(self,
        interactive=False,        # Can also be called non-interactively
        bpoId=None,         # or Cmnd-Input
    ):
        cmndOutcome = self.getOpOutcome()
        if interactive:
            if not self.cmndLineValidate(outcome=cmndOutcome):
                return cmndOutcome

        callParamsDict = {'bpoId': bpoId, }
        if not icm.cmndCallParamsValidate(callParamsDict, interactive, outcome=cmndOutcome):
            return cmndOutcome
        bpoId = callParamsDict['bpoId']

####+END:
        liveTargets = pattern.sameInstance(PalsBase_LiveTargets, bpoId)
        liveTargetsPalsPath = liveTargets.basePath_update()

        print(liveTargetsPalsPath)

        return cmndOutcome



####+BEGIN: bx:icm:python:cmnd:classHead :cmndName "targetModeSet" :parsMand "bpoId" :parsOpt "" :argsMin "1" :argsMax "1" :asFunc "" :interactiveP ""
"""
*  _[[elisp:(blee:menu-sel:outline:popupMenu)][±]]_ _[[elisp:(blee:menu-sel:navigation:popupMenu)][Ξ]]_ [[elisp:(bx:orgm:indirectBufOther)][|>]] *[[elisp:(blee:ppmm:org-mode-toggle)][|N]]*  ICM-Cmnd   :: /targetModeSet/ parsMand=bpoId parsOpt= argsMin=1 argsMax=1 asFunc= interactive=  [[elisp:(org-cycle)][| ]]
"""
class targetModeSet(icm.Cmnd):
    cmndParamsMandatory = [ 'bpoId', ]
    cmndParamsOptional = [ ]
    cmndArgsLen = {'Min': 1, 'Max': 1,}

    @icm.subjectToTracking(fnLoc=True, fnEntry=True, fnExit=True)
    def cmnd(self,
        interactive=False,        # Can also be called non-interactively
        bpoId=None,         # or Cmnd-Input
        argsList=[],         # or Args-Input
    ):
        cmndOutcome = self.getOpOutcome()
        if interactive:
            if not self.cmndLineValidate(outcome=cmndOutcome):
                return cmndOutcome
            effectiveArgsList = G.icmRunArgsGet().cmndArgs  # type: ignore
        else:
            effectiveArgsList = argsList

        callParamsDict = {'bpoId': bpoId, }
        if not icm.cmndCallParamsValidate(callParamsDict, interactive, outcome=cmndOutcome):
            return cmndOutcome
        bpoId = callParamsDict['bpoId']

        cmndArgsSpecDict = self.cmndArgsSpec()
        if not self.cmndArgsValidate(effectiveArgsList, cmndArgsSpecDict, outcome=cmndOutcome):
            return cmndOutcome
####+END:
        cmndArgs = list(self.cmndArgsGet("0&1", cmndArgsSpecDict, effectiveArgsList)) # type: ignore

        liveTargetsInst = pattern.sameInstance(PalsBase_LiveTargets, bpoId)
        targetParamsBasePath = liveTargetsInst.targetParamsPath_obtain()

        liveTargetFpsInst = liveTargetsInst.fps_baseMake()

        if cmndArgs[0] == "here":
            liveTargetFpsInst.fps_setParam('palsLiveTargetMode', "here")

            hereParamsBasePath = pathlib.Path(curFps.baseDirObtain())

            fpath.symlinkUpdate(hereParamsBasePath, targetParamsBasePath)

        elif cmndArgs[0] == "live":
            liveTargetFpsInst.fps_setParam('palsLiveTargetMode', "live")

            liveParamsInst = pattern.sameInstance(repoLiveParams.PalsRepo_LiveParams, bpoId)
            liveParamsBasePath = pathlib.Path(
                liveParamsInst.fps_absBasePath()
            )

            fpath.symlinkUpdate(liveParamsBasePath, targetParamsBasePath)

        else:
            icm.EH_critical_oops(f"should never happen: cmndArgs[0]={cmndArgs[0]}")

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
            argPosition="0&1",
            argName="cmndArgs",
            argDefault='live',
            argChoices=['live', 'here',],
            argDescription="One Argument , live or here"
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
