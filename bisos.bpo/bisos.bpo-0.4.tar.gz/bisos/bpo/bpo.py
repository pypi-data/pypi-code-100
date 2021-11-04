# -*- coding: utf-8 -*-
"""\
* *[Summary]* :: A /library/ Beginning point for development of new ICM oriented libraries.
"""

import typing

from unisos.icm.icm import EH_problem_usageError, ReturnCode

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
** TODO [[elisp:(org-cycle)][| ]]  Current         :: Just getting started [[elisp:(org-cycle)][| ]]
**      [End-Of-Status]
"""

"""
*  [[elisp:(org-cycle)][| *ICM-INFO:* |]] :: Author, Copyleft and Version Information
"""
####+BEGIN: bx:icm:py:name :style "fileName"
icmInfo['moduleName'] = "bpo"
####+END:

####+BEGIN: bx:icm:py:version-timestamp :style "date"
icmInfo['version'] = "202109272532"
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
*  This file:/bisos/git/auth/bxRepos/bisos-pip/bpo/py3/bisos/bpo/bpo.py :: [[elisp:(org-cycle)][| ]]
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
#import pwd
#import grp
import collections
import enum

####+BEGIN: bx:dblock:global:file-insert-cond :cond "./blee.el" :file "/bisos/apps/defaults/update/sw/icm/py/importUcfIcmG.py"
from unisos import ucf
from unisos import icm

icm.unusedSuppressForEval(ucf.__file__)  # in case icm and ucf are not used

G = icm.IcmGlobalContext()
# G.icmLibsAppend = __file__
# G.icmCmndsLibsAppend = __file__
####+END:

# from bisos.platform import bxPlatformConfig
# from bisos.platform import bxPlatformThis

from bisos.basics import pattern

####+BEGIN: bx:dblock:python:section :title "Start Your Sections Here"
"""
*  [[elisp:(beginning-of-buffer)][Top]] ############## [[elisp:(blee:ppmm:org-mode-toggle)][Nat]] [[elisp:(delete-other-windows)][(1)]]    *Start Your Sections Here*  [[elisp:(org-cycle)][| ]]  [[elisp:(org-show-subtree)][|=]]
"""
####+END:

####+BEGIN: bx:dblock:python:enum :enumName "bpoId_Type" :comment ""
"""
*  _[[elisp:(blee:menu-sel:outline:popupMenu)][±]]_ _[[elisp:(blee:menu-sel:navigation:popupMenu)][Ξ]]_ [[elisp:(bx:orgm:indirectBufOther)][|>]] *[[elisp:(blee:ppmm:org-mode-toggle)][|N]]*  Enum       :: /bpoId_Type/  [[elisp:(org-cycle)][| ]]
"""
@enum.unique
class bpoId_Type(enum.Enum):
####+END:
    path = 'path'   # FoeignBpo
    homeDir = 'homeDir'
    acctId = 'acctId'
    genericName = 'genericName'  # ByN
    objId = 'objId'
    relObjId = 'relObjId'

####+BEGIN: bx:dblock:python:enum :enumName "bpo_Type" :comment ""
"""
*  _[[elisp:(blee:menu-sel:outline:popupMenu)][±]]_ _[[elisp:(blee:menu-sel:navigation:popupMenu)][Ξ]]_ [[elisp:(bx:orgm:indirectBufOther)][|>]] *[[elisp:(blee:ppmm:org-mode-toggle)][|N]]*  Enum       :: /bpo_Type/  [[elisp:(org-cycle)][| ]]
"""
@enum.unique
class bpo_Type(enum.Enum):
####+END:
    project = 'project'
    pals = 'pals'

####+BEGIN: bx:dblock:python:enum :enumName "bpo_Purpose" :comment ""
"""
*  _[[elisp:(blee:menu-sel:outline:popupMenu)][±]]_ _[[elisp:(blee:menu-sel:navigation:popupMenu)][Ξ]]_ [[elisp:(bx:orgm:indirectBufOther)][|>]] *[[elisp:(blee:ppmm:org-mode-toggle)][|N]]*  Enum       :: /bpo_Purpose/  [[elisp:(org-cycle)][| ]]
"""
@enum.unique
class bpo_Purpose(enum.Enum):
####+END:
    info = 'info'
    materialize = 'materialize'



####+BEGIN: bx:dblock:python:func :funcName "bpoIdType_obtain" :funcType "Obtain" :retType "str" :deco "" :argsList "bpoId"
"""
*  _[[elisp:(blee:menu-sel:outline:popupMenu)][±]]_ _[[elisp:(blee:menu-sel:navigation:popupMenu)][Ξ]]_ [[elisp:(bx:orgm:indirectBufOther)][|>]] *[[elisp:(blee:ppmm:org-mode-toggle)][|N]]*  Func-Obtain :: /bpoIdType_obtain/ retType=str argsList=(bpoId)  [[elisp:(org-cycle)][| ]]
"""
def bpoId_Type_obtain(
    bpoId,
):
####+END:
    """
** NOT yet -- ea-NUM means old ByStarUid, A pure number means nativeSO. nonNumber means foreignBxO
"""
    icm.unusedSuppress(bpoId)
    return bpoId_Type.acctId


####+BEGINNOT: bx:dblock:python:func :funcName "bpoBaseDir_obtain" :funcType "Obtain" :retType "str" :deco "" :argsList "bpoId"
"""
*  _[[elisp:(blee:menu-sel:outline:popupMenu)][±]]_ _[[elisp:(blee:menu-sel:navigation:popupMenu)][Ξ]]_ [[elisp:(bx:orgm:indirectBufOther)][|>]] *[[elisp:(blee:ppmm:org-mode-toggle)][|N]]*  Func-Obtain :: /bpoBaseDir_obtain/ retType=str argsList=(bpoId)  [[elisp:(org-cycle)][| ]]
"""
def bpoBaseDir_obtain(
    bpoId: str,
) -> str:
####+END:
    """
**
"""
    bpoBaseDir = ""
    idType = bpoId_Type_obtain(bpoId)

    if idType == bpoId_Type.path:
        bpoBaseDir = bpoId
    elif idType == bpoId_Type.homeDir:
        bpoBaseDir = bpoId
    elif idType == bpoId_Type.acctId:
        bpoBaseDir = os.path.expanduser(f"~{bpoId}")
        if bpoBaseDir == format(f"~{bpoId}"):
            icm.EH_problem_usageError(f"bpoId={bpoId} is not a valid account")
            bpoBaseDir = ""
    else:
        icm.EH_problem_usageError("")

    return bpoBaseDir


####+BEGIN: bx:dblock:python:subSection :title "Class Definitions"

####+END:

####+BEGIN: bx:dblock:python:class :className "EffectiveBpos" :superClass "object" :comment "" :classType "basic"
"""
*  _[[elisp:(blee:menu-sel:outline:popupMenu)][±]]_ _[[elisp:(blee:menu-sel:navigation:popupMenu)][Ξ]]_ [[elisp:(bx:orgm:indirectBufOther)][|>]] *[[elisp:(blee:ppmm:org-mode-toggle)][|N]]*  Class-basic :: /EffectiveBpos/ object  [[elisp:(org-cycle)][| ]]
"""
class EffectiveBpos(object):
####+END:
    """y
** Only one instance is created for a given BpoId.
"""
    effectiveBposList = {}

    @staticmethod
    def addBpo(
            bpoId,
            bpo,
    ):
        # print(f"ccc Adding bpoId={bpoId} bpo={bpo}")
        __class__.effectiveBposList.update({bpoId: bpo})
        return None

    @staticmethod
    def givenBpoIdObtainBpo(
            bpoId,
            BpoClass,
    ):
        if bpoId in __class__.effectiveBposList:
            return __class__.effectiveBposList[bpoId]
        else:
            # return BpoClass(bpoId)
            return pattern.sameInstance(BpoClass, bpoId)  # In the __init__ of BpoClass there should be a addBpo

    @staticmethod
    def givenBpoIdGetBpo(
            bpoId,
    ):
        """Should be renamed to givenBpoIdFindBpo"""
        # print(f"aaa bpoId={bpoId}")
        if bpoId in __class__.effectiveBposList:
            return __class__.effectiveBposList[bpoId]
        else:
            # icm.EH_problem_usageError("")
            return None

    @staticmethod
    def givenBpoIdGetBpoOrNone(
            bpoId,
    ):
        # print(f"bbb bpoId={bpoId}")
        if bpoId in __class__.effectiveBposList:
            return __class__.effectiveBposList[bpoId]
        else:
            return None


####+BEGIN: bx:icm:python:func :funcName "obtainBpo" :funcType "anyOrNone" :retType "bool" :deco "" :argsList "bpoId"
"""
*  _[[elisp:(blee:menu-sel:outline:popupMenu)][±]]_ _[[elisp:(blee:menu-sel:navigation:popupMenu)][Ξ]]_ [[elisp:(bx:orgm:indirectBufOther)][|>]] *[[elisp:(blee:ppmm:org-mode-toggle)][|N]]*  Func-anyOrNone :: /obtainBpo/ retType=bool argsList=(bpoId)  [[elisp:(org-cycle)][| ]]
"""
def obtainBpo(
    bpoId,
):
####+END:
    return EffectiveBpos.givenBpoIdObtainBpo(bpoId, Bpo)


####+BEGIN: bx:dblock:python:class :className "Bpo" :superClass "object" :comment "ByStar Portable Object -- to be subclassed" :classType "basic"
"""
*  _[[elisp:(blee:menu-sel:outline:popupMenu)][±]]_ _[[elisp:(blee:menu-sel:navigation:popupMenu)][Ξ]]_ [[elisp:(bx:orgm:indirectBufOther)][|>]] *[[elisp:(blee:ppmm:org-mode-toggle)][|N]]*  Class-basic :: /Bpo/ object =ByStar Portable Object -- to be subclassed=  [[elisp:(org-cycle)][| ]]
"""
class Bpo(object):
####+END:
    """
** Abstraction of the base ByStar Portable Object
"""
    def __init__(
            self,
            bpoId,
    ):
        '''Constructor'''

        self.baseDir = bpoBaseDir_obtain(bpoId)
        if not self.baseDir:
            icm.EH_problem_usageError(f"Missing baseDir for bpoId={bpoId}")
            return

        EffectiveBpos.addBpo(bpoId, self)

        self.bpoId = bpoId
        self.bpoName = bpoId
        self.bpoBaseDir = bpoBaseDir_obtain(bpoId)

        self.repo_rbxe = BpoRepo_Rbxe(bpoId)
        self.repo_bxeTree = BpoRepo_BxeTree(bpoId)



####+BEGIN: bx:dblock:python:class :className "BpoBases" :superClass "object" :comment "A BPO Repository -- to be subclassed" :classType "basic"
"""
*  _[[elisp:(blee:menu-sel:outline:popupMenu)][±]]_ _[[elisp:(blee:menu-sel:navigation:popupMenu)][Ξ]]_ [[elisp:(bx:orgm:indirectBufOther)][|>]] *[[elisp:(blee:ppmm:org-mode-toggle)][|N]]*  Class-basic :: /BpoBases/ object =A BPO Repository -- to be subclassed=  [[elisp:(org-cycle)][| ]]
"""
class BpoBases(object):
####+END:
    """
** Abstraction of the base ByStar Portable Object
"""

    def __init__(
            self,
            bpoId,
    ):
        self.bpo = EffectiveBpos.givenBpoIdGetBpo(bpoId)
        if not self.bpo:
            icm.EH_critical_usageError(f"Missing BPO for {bpoId}")
            return

        self.bpoId = self.bpo.bpoId
        self.bpoName = self.bpo.bpoName
        self.bpoBaseDir = self.bpo.baseDir

        # print(self.bpo)
        # print(self.bpo.__dict__)

    def bases_update(self,):
        self.varBase_update()
        self.tmpBase_update()
        return

    def varBase_update(self,):
        return "NOTYET"

    def varBase_obtain(self,):
        return os.path.join(self.bpo.baseDir, "var") # type: ignore

    def tmpBase_update(self,):
        return "NOTYET"

    def tmpBase_obtain(self,):
        return os.path.join(self.bpo.baseDir, "tmp") # type: ignore


####+BEGIN: bx:dblock:python:class :className "BpoRepo" :superClass "object" :comment "A BPO Repository -- to be subclassed" :classType "basic"
"""
*  _[[elisp:(blee:menu-sel:outline:popupMenu)][±]]_ _[[elisp:(blee:menu-sel:navigation:popupMenu)][Ξ]]_ [[elisp:(bx:orgm:indirectBufOther)][|>]] *[[elisp:(blee:ppmm:org-mode-toggle)][|N]]*  Class-basic :: /BpoRepo/ object =A BPO Repository -- to be subclassed=  [[elisp:(org-cycle)][| ]]
"""
class BpoRepo(object):
####+END:
    """
** Abstraction of the base ByStar Portable Object
"""

    def __init__(
            self,
            bpoId,
    ):
        self.bpo = EffectiveBpos.givenBpoIdGetBpo(bpoId)
        if not self.bpo:
            # icm.EH_critical_usageError(f"Missing BPO for {bpoId}")
            return



####+BEGIN: bx:dblock:python:class :className "BpoRepo_Rbxe" :superClass "object" :comment "A BPO Repository -- to be subclassed" :classType "basic"
"""
*  _[[elisp:(blee:menu-sel:outline:popupMenu)][±]]_ _[[elisp:(blee:menu-sel:navigation:popupMenu)][Ξ]]_ [[elisp:(bx:orgm:indirectBufOther)][|>]] *[[elisp:(blee:ppmm:org-mode-toggle)][|N]]*  Class-basic :: /BpoRepo_Rbxe/ object =A BPO Repository -- to be subclassed=  [[elisp:(org-cycle)][| ]]
"""
class BpoRepo_Rbxe(BpoRepo):
####+END:
    """
** Abstraction of the base ByStar Portable Object
"""
    def __init__(
            self,
            bpoId,
    ):
        super().__init__(bpoId)
        if not EffectiveBpos.givenBpoIdGetBpo(bpoId):
            icm.EH_critical_usageError(f"Missing BPO for {bpoId}")
            return

    def info(self,):
        print(f"rbxeInfo bpoId={self.bpo.bpoId}") # type: ignore


####+BEGIN: bx:dblock:python:class :className "BpoRepo_BxeTree" :superClass "object" :comment "A BPO Repository -- to be subclassed" :classType "basic"
"""
*  _[[elisp:(blee:menu-sel:outline:popupMenu)][±]]_ _[[elisp:(blee:menu-sel:navigation:popupMenu)][Ξ]]_ [[elisp:(bx:orgm:indirectBufOther)][|>]] *[[elisp:(blee:ppmm:org-mode-toggle)][|N]]*  Class-basic :: /BpoRepo_BxeTree/ object =A BPO Repository -- to be subclassed=  [[elisp:(org-cycle)][| ]]
"""
class BpoRepo_BxeTree(BpoRepo):
####+END:
    """
** Abstraction of the base ByStar Portable Object
"""
    def __init__(
            self,
            bpoId,
    ):
        super().__init__(bpoId)
        if not EffectiveBpos.givenBpoIdGetBpo(bpoId):
            icm.EH_critical_usageError(f"Missing BPO for {bpoId}")
            return

    def info(self,):
        print("bxeTreeInfo")


####+BEGIN: bx:dblock:python:section :title "Common Parameters Specification"
"""
*  [[elisp:(beginning-of-buffer)][Top]] ############## [[elisp:(blee:ppmm:org-mode-toggle)][Nat]] [[elisp:(delete-other-windows)][(1)]]    *Common Parameters Specification*  [[elisp:(org-cycle)][| ]]  [[elisp:(org-show-subtree)][|=]]
"""
####+END:


####+BEGIN: bx:dblock:python:func :funcName "commonParamsSpecify" :funcType "ParSpec" :retType "" :deco "" :argsList "icmParams"
"""
*  _[[elisp:(blee:menu-sel:outline:popupMenu)][±]]_ _[[elisp:(blee:menu-sel:navigation:popupMenu)][Ξ]]_ [[elisp:(bx:orgm:indirectBufOther)][|>]] *[[elisp:(blee:ppmm:org-mode-toggle)][|N]]*  Func-ParSpec :: /commonParamsSpecify/ retType= argsList=(icmParams)  [[elisp:(org-cycle)][| ]]
"""
def commonParamsSpecify(
    icmParams,
):
####+END:
    icmParams.parDictAdd(
        parName='bpoId',
        parDescription="Bx Portable ObjectId",
        parDataType=None,
        parDefault=None,
        parChoices=["any"],
        # parScope=icm.ICM_ParamScope.TargetParam,
        argparseShortOpt=None,
        argparseLongOpt='--bpoId',
    )


####+BEGIN: bx:dblock:python:section :title "Common Examples Sections"
"""
*  [[elisp:(beginning-of-buffer)][Top]] ############## [[elisp:(blee:ppmm:org-mode-toggle)][Nat]] [[elisp:(delete-other-windows)][(1)]]    *Common Examples Sections*  [[elisp:(org-cycle)][| ]]  [[elisp:(org-show-subtree)][|=]]
"""
####+END:


####+BEGIN: bx:dblock:python:func :funcName "examples_bpo_basicAccess" :comment "Show/Verify/Update For relevant PBDs" :funcType "examples" :retType "none" :deco "" :argsList "oneBpo"
"""
*  _[[elisp:(blee:menu-sel:outline:popupMenu)][±]]_ _[[elisp:(blee:menu-sel:navigation:popupMenu)][Ξ]]_ [[elisp:(bx:orgm:indirectBufOther)][|>]] *[[elisp:(blee:ppmm:org-mode-toggle)][|N]]*  Func-examples :: /examples_bpo_basicAccess/ =Show/Verify/Update For relevant PBDs= retType=none argsList=(oneBpo)  [[elisp:(org-cycle)][| ]]
"""
def examples_bpo_basicAccess(
    oneBpo,
):
####+END:
    """
** Common examples.
"""
    def cpsInit(): return collections.OrderedDict()
    def menuItem(verbosity): icm.ex_gCmndMenuItem(cmndName, cps, cmndArgs, verbosity=verbosity) # 'little' or 'none'
    # def execLineEx(cmndStr): icm.ex_gExecMenuItem(execLine=cmndStr)

    #oneBpo = "pmi_ByD-100001"

    # def moduleOverviewMenuItem(overviewCmndName):
    #     icm.cmndExampleMenuChapter('* =Module=  Overview (desc, usage, status)')
    #     cmndName = "overview_bxpBaseDir" ; cmndArgs = "moduleDescription moduleUsage moduleStatus" ;
    #     cps = collections.OrderedDict()
    #     icm.ex_gCmndMenuItem(cmndName, cps, cmndArgs, verbosity='none') # 'little' or 'none'

    # moduleOverviewMenuItem(bpo_libOverview)

    icm.cmndExampleMenuChapter('*General BPO Access And Management Commands*')

    cmndName = "bpoIdTypeObtain"
    cmndArgs = ""
    cps = cpsInit() ; cps['bpoId'] = oneBpo
    menuItem(verbosity='none')
    # menuItem(verbosity='full')

    cmndName = "bpoBaseDirObtain"
    cmndArgs = ""
    cps = cpsInit() ; cps['bpoId'] = oneBpo
    menuItem(verbosity='none')
    # menuItem(verbosity='full')


####+BEGIN: bx:dblock:python:section :title "ICM Commands"
"""
*  [[elisp:(beginning-of-buffer)][Top]] ############## [[elisp:(blee:ppmm:org-mode-toggle)][Nat]] [[elisp:(delete-other-windows)][(1)]]    *ICM Commands*  [[elisp:(org-cycle)][| ]]  [[elisp:(org-show-subtree)][|=]]
"""
####+END:


####+BEGIN: bx:icm:python:cmnd:classHead :cmndName "bpoIdTypeObtain" :parsMand "bpoId" :parsOpt "" :argsMin "0" :argsMax "0" :asFunc "" :interactiveP ""
"""
*  _[[elisp:(blee:menu-sel:outline:popupMenu)][±]]_ _[[elisp:(blee:menu-sel:navigation:popupMenu)][Ξ]]_ [[elisp:(bx:orgm:indirectBufOther)][|>]] *[[elisp:(blee:ppmm:org-mode-toggle)][|N]]*  ICM-Cmnd   :: /bpoIdTypeObtain/ parsMand=bpoId parsOpt= argsMin=0 argsMax=0 asFunc= interactive=  [[elisp:(org-cycle)][| ]]
"""
class bpoIdTypeObtain(icm.Cmnd):
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
        retVal = bpoId_Type_obtain(bpoId)

        if interactive:
            icm.ANN_write(f"{retVal}")

        return cmndOutcome.set(
            opError=icm.notAsFailure(retVal),
            opResults=retVal,
        )

####+BEGIN: bx:icm:python:method :methodName "cmndDocStr" :methodType "anyOrNone" :retType "bool" :deco "default" :argsList ""
    """
**  [[elisp:(org-cycle)][| ]] [[elisp:(org-show-subtree)][|=]] [[elisp:(show-children 10)][|V]] [[elisp:(bx:orgm:indirectBufOther)][|>]] [[elisp:(bx:orgm:indirectBufMain)][|I]] [[elisp:(blee:ppmm:org-mode-toggle)][|N]] [[elisp:(org-top-overview)][|O]] [[elisp:(progn (org-shifttab) (org-content))][|C]] [[elisp:(delete-other-windows)][|1]]  Method-anyOrNone :: /cmndDocStr/ retType=bool argsList=nil deco=default  [[elisp:(org-cycle)][| ]]
"""
    @icm.subjectToTracking(fnLoc=True, fnEntry=True, fnExit=True)
    def cmndDocStr(self):
####+END:
        return """
***** [[elisp:(org-cycle)][| *CmndDesc:* | ]]  Returns the type of bpoId
"""


####+BEGIN: bx:icm:python:cmnd:classHead :cmndName "bpoBaseDirObtain" :parsMand "bpoId" :parsOpt "" :argsMin "0" :argsMax "0" :asFunc "" :interactiveP ""
"""
*  _[[elisp:(blee:menu-sel:outline:popupMenu)][±]]_ _[[elisp:(blee:menu-sel:navigation:popupMenu)][Ξ]]_ [[elisp:(bx:orgm:indirectBufOther)][|>]] *[[elisp:(blee:ppmm:org-mode-toggle)][|N]]*  ICM-Cmnd   :: /bpoBaseDirObtain/ parsMand=bpoId parsOpt= argsMin=0 argsMax=0 asFunc= interactive=  [[elisp:(org-cycle)][| ]]
"""
class bpoBaseDirObtain(icm.Cmnd):
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
        retVal = bpoBaseDir_obtain(bpoId)

        if interactive:
            icm.ANN_write(f"{retVal}")

        return cmndOutcome.set(
            opError=icm.notAsFailure(retVal),
            opResults=retVal,
        )

####+BEGIN: bx:icm:python:method :methodName "cmndDocStr" :methodType "anyOrNone" :retType "bool" :deco "default" :argsList ""
    """
**  [[elisp:(org-cycle)][| ]] [[elisp:(org-show-subtree)][|=]] [[elisp:(show-children 10)][|V]] [[elisp:(bx:orgm:indirectBufOther)][|>]] [[elisp:(bx:orgm:indirectBufMain)][|I]] [[elisp:(blee:ppmm:org-mode-toggle)][|N]] [[elisp:(org-top-overview)][|O]] [[elisp:(progn (org-shifttab) (org-content))][|C]] [[elisp:(delete-other-windows)][|1]]  Method-anyOrNone :: /cmndDocStr/ retType=bool argsList=nil deco=default  [[elisp:(org-cycle)][| ]]
"""
    @icm.subjectToTracking(fnLoc=True, fnEntry=True, fnExit=True)
    def cmndDocStr(self):
####+END:
        return """
***** [[elisp:(org-cycle)][| *CmndDesc:* | ]]  Returns the type of bpoId
"""


####+BEGIN: bx:icm:python:section :title "End Of Editable Text"
"""
*  [[elisp:(beginning-of-buffer)][Top]] ############## [[elisp:(blee:ppmm:org-mode-toggle)][Nat]] [[elisp:(delete-other-windows)][(1)]]    *End Of Editable Text*  [[elisp:(org-cycle)][| ]]  [[elisp:(org-show-subtree)][|=]]
"""
####+END:

####+BEGIN: bx:dblock:global:file-insert-cond :cond "./blee.el" :file "/bisos/apps/defaults/software/plusOrg/dblock/inserts/endOfFileControls.org"
#+STARTUP: showall
####+END:
