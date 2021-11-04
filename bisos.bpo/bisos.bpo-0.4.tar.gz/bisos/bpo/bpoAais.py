# -*- coding: utf-8 -*-
"""\
* *[Summary]* :: A /library/ Beginning point for development of new ICM oriented libraries.
"""

icmInfo = { 'moduleDescription': ["""
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
icmInfo['moduleName'] = "bpoPals"
####+END:

####+BEGIN: bx:icm:py:version-timestamp :style "date"
icmInfo['version'] = "202109171849"
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
*  This file:/tmp/bpoPals.py :: [[elisp:(org-cycle)][| ]]
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
*  [[elisp:(org-cycle)][| ]] [[elisp:(org-show-subtree)][|=]] [[elisp:(show-children 10)][|V]] [[elisp:(bx:orgm:indirectBufOther)][|>]] [[elisp:(bx:orgm:indirectBufMain)][|I]] [[elisp:(blee:ppmm:org-mode-toggle)][|N]] [[elisp:(org-top-overview)][|O]] [[elisp:(progn (org-shifttab) (org-content))][|C]] [[elisp:(delete-other-windows)][|1]]  =Imports=      :: *IMPORTS*  [[elisp:(org-cycle)][| ]]
"""
####+END:


import os
import pwd
import grp
import collections
import enum

####+BEGIN: bx:dblock:global:file-insert-cond :cond "./blee.el" :file "/bisos/apps/defaults/update/sw/icm/py/importUcfIcmBleepG.py"
from unisos import ucf
from unisos import icm

icm.unusedSuppressForEval(ucf.__file__)  # in case icm and ucf are not used

G = icm.IcmGlobalContext()
# G.icmLibsAppend = __file__
# G.icmCmndsLibsAppend = __file__

from blee.icmPlayer import bleep
####+END:

from bisos.platform import bxPlatformConfig
from bisos.platform import bxPlatformThis

from bisos.bpo import bpo

####+BEGIN: bx:dblock:python:section :title "Start Your Sections Here"
"""
*  [[elisp:(beginning-of-buffer)][Top]] ############## [[elisp:(blee:ppmm:org-mode-toggle)][Nat]] [[elisp:(delete-other-windows)][(1)]]    *Start Your Sections Here*  [[elisp:(org-cycle)][| ]]  [[elisp:(org-show-subtree)][|=]]
"""
####+END:


####+BEGIN: bx:dblock:python:func :funcName "srRootDir_obtain" :funcType "Obtain" :retType "str" :deco "" :argsList "bpoBaseDir"
"""
*  [[elisp:(org-cycle)][| ]] [[elisp:(org-show-subtree)][|=]] [[elisp:(show-children 10)][|V]] [[elisp:(bx:orgm:indirectBufOther)][|>]] [[elisp:(bx:orgm:indirectBufMain)][|I]] [[elisp:(blee:ppmm:org-mode-toggle)][|N]] [[elisp:(org-top-overview)][|O]] [[elisp:(progn (org-shifttab) (org-content))][|C]] [[elisp:(delete-other-windows)][|1]]  Func-Obtain    :: /srRootDir_obtain/ retType=str argsList=(bpoBaseDir)  [[elisp:(org-cycle)][| ]]
"""
def srRootDir_obtain(
    bpoBaseDir,
):
####+END:
    """
**
"""
    return (
        os.path.join(
            bpoBaseDir,
            "so/r3/sr",
        )
    )


####+BEGIN: bx:dblock:python:func :funcName "srFullPathBaseDir_obtain" :funcType "Obtain" :retType "str" :deco "" :argsList "bpoId srRelPath"
"""
*  [[elisp:(org-cycle)][| ]] [[elisp:(org-show-subtree)][|=]] [[elisp:(show-children 10)][|V]] [[elisp:(bx:orgm:indirectBufOther)][|>]] [[elisp:(bx:orgm:indirectBufMain)][|I]] [[elisp:(blee:ppmm:org-mode-toggle)][|N]] [[elisp:(org-top-overview)][|O]] [[elisp:(progn (org-shifttab) (org-content))][|C]] [[elisp:(delete-other-windows)][|1]]  Func-Obtain    :: /srFullPathBaseDir_obtain/ retType=str argsList=(bpoId srRelPath)  [[elisp:(org-cycle)][| ]]
"""
def srFullPathBaseDir_obtain(
    bpoId,
    srRelPath,
):
####+END:
    """
** Join dirs as expected.
"""
    return (
        os.path.join(
            srRootDir_obtain(
                bpo.bpoBaseDir_obtain(
                    bpoId
                )
            ),
            srRelPath,
        )
    )


####+BEGIN: bx:dblock:python:subSection :title "Bpo+Sr Roots and InfoBases (Control/Input)"

####+END:



####+BEGIN: bx:dblock:python:func :funcName "bpbBisos_baseObtain_control" :comment "BISOS DATA" :funcType "obtain" :retType "bool" :deco "" :argsList "baseDir"
"""
*  [[elisp:(org-cycle)][| ]] [[elisp:(org-show-subtree)][|=]] [[elisp:(show-children 10)][|V]] [[elisp:(bx:orgm:indirectBufOther)][|>]] [[elisp:(bx:orgm:indirectBufMain)][|I]] [[elisp:(blee:ppmm:org-mode-toggle)][|N]] [[elisp:(org-top-overview)][|O]] [[elisp:(progn (org-shifttab) (org-content))][|C]] [[elisp:(delete-other-windows)][|1]]  Func-obtain    :: /bpbBisos_baseObtain_control/ =BISOS DATA= retType=bool argsList=(baseDir)  [[elisp:(org-cycle)][| ]]
"""
def bpbBisos_baseObtain_control(
    baseDir,
):
####+END:
    bxpRoot = "bxpRoot_baseObtain()"

    return( os.path.join(
        bxpRoot, "bisos", "input"
    ))


####+BEGIN: bx:dblock:python:subSection :title "Bpo+Sr RunTime  Bases"

####+END:

####+BEGIN: bx:dblock:python:func :funcName "bpoSr_runBaseObtain_root" :funcType "obtain" :retType "bool" :deco "" :argsList "bpoId sr"
"""
*  [[elisp:(org-cycle)][| ]] [[elisp:(org-show-subtree)][|=]] [[elisp:(show-children 10)][|V]] [[elisp:(bx:orgm:indirectBufOther)][|>]] [[elisp:(bx:orgm:indirectBufMain)][|I]] [[elisp:(blee:ppmm:org-mode-toggle)][|N]] [[elisp:(org-top-overview)][|O]] [[elisp:(progn (org-shifttab) (org-content))][|C]] [[elisp:(delete-other-windows)][|1]]  Func-obtain    :: /bpoSr_runBaseObtain_root/ retType=bool argsList=(bpoId sr)  [[elisp:(org-cycle)][| ]]
"""
def bpoSr_runBaseObtain_root(
    bpoId,
    sr,
):
####+END:
    return(
        os.path.join(
            bxPlatformConfig.rootDir_deRun_fpObtain(configBaseDir=None,),
            "bisos/r3/bpo",
            bpoId,
        )
    )



####+BEGIN: bx:dblock:python:func :funcName "bpoSr_runBaseObtain_var" :funcType "obtain" :retType "bool" :deco "" :argsList "bpoId sr"
"""
*  [[elisp:(org-cycle)][| ]] [[elisp:(org-show-subtree)][|=]] [[elisp:(show-children 10)][|V]] [[elisp:(bx:orgm:indirectBufOther)][|>]] [[elisp:(bx:orgm:indirectBufMain)][|I]] [[elisp:(blee:ppmm:org-mode-toggle)][|N]] [[elisp:(org-top-overview)][|O]] [[elisp:(progn (org-shifttab) (org-content))][|C]] [[elisp:(delete-other-windows)][|1]]  Func-obtain    :: /bpoSr_runBaseObtain_var/ retType=bool argsList=(bpoId sr)  [[elisp:(org-cycle)][| ]]
"""
def bpoSr_runBaseObtain_var(
    bpoId,
    sr,
):
####+END:
    return(
        os.path.join(
            bpoSr_runBaseObtain_root(
                bpoId,
                sr,
            ),
            "var"
        )
    )

####+BEGIN: bx:dblock:python:func :funcName "bpoSr_runBaseObtain_tmp" :funcType "obtain" :retType "bool" :deco "" :argsList "bpoId sr"
"""
*  [[elisp:(org-cycle)][| ]] [[elisp:(org-show-subtree)][|=]] [[elisp:(show-children 10)][|V]] [[elisp:(bx:orgm:indirectBufOther)][|>]] [[elisp:(bx:orgm:indirectBufMain)][|I]] [[elisp:(blee:ppmm:org-mode-toggle)][|N]] [[elisp:(org-top-overview)][|O]] [[elisp:(progn (org-shifttab) (org-content))][|C]] [[elisp:(delete-other-windows)][|1]]  Func-obtain    :: /bpoSr_runBaseObtain_tmp/ retType=bool argsList=(bpoId sr)  [[elisp:(org-cycle)][| ]]
"""
def bpoSr_runBaseObtain_tmp(
    bpoId,
    sr,
):
####+END:
    return(
        os.path.join(
            bpoSr_runBaseObtain_root(
                bpoId,
                sr,
            ),
            "tmp"
        )
    )

####+BEGIN: bx:dblock:python:func :funcName "bpoSr_runBaseObtain_log" :funcType "obtain" :retType "bool" :deco "" :argsList "bpoId sr"
"""
*  [[elisp:(org-cycle)][| ]] [[elisp:(org-show-subtree)][|=]] [[elisp:(show-children 10)][|V]] [[elisp:(bx:orgm:indirectBufOther)][|>]] [[elisp:(bx:orgm:indirectBufMain)][|I]] [[elisp:(blee:ppmm:org-mode-toggle)][|N]] [[elisp:(org-top-overview)][|O]] [[elisp:(progn (org-shifttab) (org-content))][|C]] [[elisp:(delete-other-windows)][|1]]  Func-obtain    :: /bpoSr_runBaseObtain_log/ retType=bool argsList=(bpoId sr)  [[elisp:(org-cycle)][| ]]
"""
def bpoSr_runBaseObtain_log(
    bpoId,
    sr,
):
####+END:
    return(
        os.path.join(
            bpoSr_runBaseObtain_root(
                bpoId,
                sr,
            ),
            "log"
        )
    )

####+BEGIN: bx:dblock:python:section :title "Common Arguments Specification"
"""
*  [[elisp:(beginning-of-buffer)][Top]] ############## [[elisp:(blee:ppmm:org-mode-toggle)][Nat]] [[elisp:(delete-other-windows)][(1)]]    *Common Arguments Specification*  [[elisp:(org-cycle)][| ]]  [[elisp:(org-show-subtree)][|=]]
"""
####+END:


####+BEGIN: bx:dblock:python:subSection :title "Class Definitions"

####+END:


####+BEGIN: bx:dblock:python:class :className "Bpo" :superClass "object" :comment "Expected to be subclassed" :classType "basic"
"""
*  [[elisp:(org-cycle)][| ]] [[elisp:(org-show-subtree)][|=]] [[elisp:(show-children 10)][|V]] [[elisp:(bx:orgm:indirectBufOther)][|>]] [[elisp:(bx:orgm:indirectBufMain)][|I]] [[elisp:(blee:ppmm:org-mode-toggle)][|N]] [[elisp:(org-top-overview)][|O]] [[elisp:(progn (org-shifttab) (org-content))][|C]] [[elisp:(delete-other-windows)][|1]]  Class-basic    :: /Bpo/ object =Expected to be subclassed=  [[elisp:(org-cycle)][| ]]
"""
class Bpo(object):
####+END:
    """
** Abstraction of the base ByStar Portable Object
"""


    def __init__(
        self,
        baseDirType=None,
        destPathRoot=None,
        destPathRel=None,
    ):
        self.baseDirType=baseDirType
        self.destPathRoot=destPathRoot
        self.destPathRel=destPathRel

    def destPathFullGet(self,):
        return None
        # return (
        #     os.path.abspath(
        #         os.path.join(self.destPathRoot, self.destPathRel)
        #     )
        # )


####+BEGIN: bx:dblock:python:section :title "Common Parameters Specification"
"""
*  [[elisp:(beginning-of-buffer)][Top]] ############## [[elisp:(blee:ppmm:org-mode-toggle)][Nat]] [[elisp:(delete-other-windows)][(1)]]    *Common Parameters Specification*  [[elisp:(org-cycle)][| ]]  [[elisp:(org-show-subtree)][|=]]
"""
####+END:


####+BEGIN: bx:dblock:python:func :funcName "commonParamsSpecify" :funcType "ParSpec" :retType "" :deco "" :argsList "icmParams"
"""
*  [[elisp:(org-cycle)][| ]] [[elisp:(org-show-subtree)][|=]] [[elisp:(show-children 10)][|V]] [[elisp:(bx:orgm:indirectBufOther)][|>]] [[elisp:(bx:orgm:indirectBufMain)][|I]] [[elisp:(blee:ppmm:org-mode-toggle)][|N]] [[elisp:(org-top-overview)][|O]] [[elisp:(progn (org-shifttab) (org-content))][|C]] [[elisp:(delete-other-windows)][|1]]  Func-ParSpec   :: /commonParamsSpecify/ retType= argsList=(icmParams)  [[elisp:(org-cycle)][| ]]
"""
def commonParamsSpecify(
    icmParams,
):
####+END:
    icmParams.parDictAdd(
        parName='sr',
        parDescription="Service Realization Path (sr/marme/dsnProc)",
        parDataType=None,
        parDefault=None,
        parChoices=["any"],
        parScope=icm.ICM_ParamScope.TargetParam,
        argparseShortOpt=None,
        argparseLongOpt='--sr',
    )


####+BEGIN: bx:dblock:python:section :title "Common Examples Sections"
"""
*  [[elisp:(beginning-of-buffer)][Top]] ############## [[elisp:(blee:ppmm:org-mode-toggle)][Nat]] [[elisp:(delete-other-windows)][(1)]]    *Common Examples Sections*  [[elisp:(org-cycle)][| ]]  [[elisp:(org-show-subtree)][|=]]
"""
####+END:


####+BEGIN: bx:dblock:python:func :funcName "examples_bpo_srBaseDir" :comment "Show/Verify/Update For relevant PBDs" :funcType "examples" :retType "none" :deco "" :argsList ""
"""
*  [[elisp:(org-cycle)][| ]] [[elisp:(org-show-subtree)][|=]] [[elisp:(show-children 10)][|V]] [[elisp:(bx:orgm:indirectBufOther)][|>]] [[elisp:(bx:orgm:indirectBufMain)][|I]] [[elisp:(blee:ppmm:org-mode-toggle)][|N]] [[elisp:(org-top-overview)][|O]] [[elisp:(progn (org-shifttab) (org-content))][|C]] [[elisp:(delete-other-windows)][|1]]  Func-examples  :: /examples_bpo_srBaseDir/ =Show/Verify/Update For relevant PBDs= retType=none argsList=nil  [[elisp:(org-cycle)][| ]]
"""
def examples_bpo_srBaseDir():
####+END:
    """
** Common examples.
"""
    def cpsInit(): return collections.OrderedDict()
    def menuItem(verbosity): icm.ex_gCmndMenuItem(cmndName, cps, cmndArgs, verbosity=verbosity) # 'little' or 'none'
    def execLineEx(cmndStr): icm.ex_gExecMenuItem(execLine=cmndStr)

    # oneForeignBxo = "mcmFbxo"

    oneBpo = "pmi_ByD-100001"

    oneSrRelPath = "marme/dsnProc"

    def moduleOverviewMenuItem(overviewCmndName):
        icm.cmndExampleMenuChapter('* =Module=  Overview (desc, usage, status)')
        cmndName = "overview_bxpBaseDir" ; cmndArgs = "moduleDescription moduleUsage moduleStatus" ;
        cps = collections.OrderedDict()
        icm.ex_gCmndMenuItem(cmndName, cps, cmndArgs, verbosity='none') # 'little' or 'none'

    # moduleOverviewMenuItem(bpo_libOverview)

    icm.cmndExampleMenuChapter(' =Bpo+Sr ZZZ Info Base Roots=  *bpoSr Control Roots*')

    cmndName = "bpoSrFullPathBaseDir" ; cmndArgs = "" ;
    cps=cpsInit() ; cps['bpoId'] = oneBpo ; cps['sr'] = oneSrRelPath
    menuItem(verbosity='little')


    icm.cmndExampleMenuChapter(' =Bpo+Sr Info Base Roots=  *bpoSr Control Roots*')

    cmndName = "bpoSrRunRootBaseDir" ; cmndArgs = "" ;
    cps=cpsInit() ; cps['bpoId'] = oneBpo ; cps['sr'] = oneSrRelPath
    menuItem(verbosity='little')

    cmndName = "bpoSrRunRootBaseDir" ; cmndArgs = "all" ;
    cps=cpsInit() ; cps['bpoId'] = oneBpo ; cps['sr'] = oneSrRelPath
    menuItem(verbosity='little')

    cmndName = "bpoSrRunRootBaseDir" ; cmndArgs = "var" ;
    cps=cpsInit() ; cps['bpoId'] = oneBpo ; cps['sr'] = oneSrRelPath
    menuItem(verbosity='little')


####+BEGIN: bx:dblock:python:section :title "ICM Commands"
"""
*  [[elisp:(beginning-of-buffer)][Top]] ############## [[elisp:(blee:ppmm:org-mode-toggle)][Nat]] [[elisp:(delete-other-windows)][(1)]]    *ICM Commands*  [[elisp:(org-cycle)][| ]]  [[elisp:(org-show-subtree)][|=]]
"""
####+END:


####+BEGIN: bx:icm:python:cmnd:classHead :cmndName "bpoSrFullPathBaseDir" :parsMand "bpoId sr" :parsOpt "" :argsMin "0" :argsMax "0" :asFunc "" :interactiveP ""
"""
*  [[elisp:(org-cycle)][| ]] [[elisp:(org-show-subtree)][|=]] [[elisp:(show-children 10)][|V]] [[elisp:(bx:orgm:indirectBufOther)][|>]] [[elisp:(bx:orgm:indirectBufMain)][|I]] [[elisp:(blee:ppmm:org-mode-toggle)][|N]] [[elisp:(org-top-overview)][|O]] [[elisp:(progn (org-shifttab) (org-content))][|C]] [[elisp:(delete-other-windows)][|1]]  ICM-Cmnd       :: /bpoSrFullPathBaseDir/ parsMand=bpoId sr parsOpt= argsMin=0 argsMax=0 asFunc= interactive=  [[elisp:(org-cycle)][| ]]
"""
class bpoSrFullPathBaseDir(icm.Cmnd):
    cmndParamsMandatory = [ 'bpoId', 'sr', ]
    cmndParamsOptional = [ ]
    cmndArgsLen = {'Min': 0, 'Max': 0,}

    @icm.subjectToTracking(fnLoc=True, fnEntry=True, fnExit=True)
    def cmnd(self,
        interactive=False,        # Can also be called non-interactively
        bpoId=None,         # or Cmnd-Input
        sr=None,         # or Cmnd-Input
    ):
        cmndOutcome = self.getOpOutcome()
        if interactive:
            if not self.cmndLineValidate(outcome=cmndOutcome):
                return cmndOutcome

        callParamsDict = {'bpoId': bpoId, 'sr': sr, }
        if not icm.cmndCallParamsValidate(callParamsDict, interactive, outcome=cmndOutcome):
            return cmndOutcome
        bpoId = callParamsDict['bpoId']
        sr = callParamsDict['sr']

####+END:
        retVal = srFullPathBaseDir_obtain(
            bpoId=bpoId,
            srRelPath=sr,
        )

        if interactive:
            icm.ANN_write("{}".format(retVal))

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
***** [[elisp:(org-cycle)][| *CmndDesc:* | ]]  Returns the full path of the Sr baseDir.
"""


####+BEGIN: bx:icm:python:cmnd:classHead :cmndName "bpoSrRunRootBaseDir" :parsMand "bpoId sr" :parsOpt "" :argsMin "0" :argsMax "3" :asFunc "" :interactiveP ""
"""
*  [[elisp:(org-cycle)][| ]] [[elisp:(org-show-subtree)][|=]] [[elisp:(show-children 10)][|V]] [[elisp:(bx:orgm:indirectBufOther)][|>]] [[elisp:(bx:orgm:indirectBufMain)][|I]] [[elisp:(blee:ppmm:org-mode-toggle)][|N]] [[elisp:(org-top-overview)][|O]] [[elisp:(progn (org-shifttab) (org-content))][|C]] [[elisp:(delete-other-windows)][|1]]  ICM-Cmnd       :: /bpoSrRunRootBaseDir/ parsMand=bpoId sr parsOpt= argsMin=0 argsMax=3 asFunc= interactive=  [[elisp:(org-cycle)][| ]]
"""
class bpoSrRunRootBaseDir(icm.Cmnd):
    cmndParamsMandatory = [ 'bpoId', 'sr', ]
    cmndParamsOptional = [ ]
    cmndArgsLen = {'Min': 0, 'Max': 3,}

    @icm.subjectToTracking(fnLoc=True, fnEntry=True, fnExit=True)
    def cmnd(self,
        interactive=False,        # Can also be called non-interactively
        bpoId=None,         # or Cmnd-Input
        sr=None,         # or Cmnd-Input
        argsList=[],         # or Args-Input
    ):
        cmndOutcome = self.getOpOutcome()
        if interactive:
            if not self.cmndLineValidate(outcome=cmndOutcome):
                return cmndOutcome
            effectiveArgsList = G.icmRunArgsGet().cmndArgs
        else:
            effectiveArgsList = argsList

        callParamsDict = {'bpoId': bpoId, 'sr': sr, }
        if not icm.cmndCallParamsValidate(callParamsDict, interactive, outcome=cmndOutcome):
            return cmndOutcome
        bpoId = callParamsDict['bpoId']
        sr = callParamsDict['sr']

        cmndArgsSpecDict = self.cmndArgsSpec()
        if not self.cmndArgsValidate(effectiveArgsList, cmndArgsSpecDict, outcome=cmndOutcome):
            return cmndOutcome
####+END:

        cmndArgs = self.cmndArgsGet("0&2", cmndArgsSpecDict, effectiveArgsList)

        if len(cmndArgs):
            if cmndArgs[0] == "all":
                cmndArgsSpec = cmndArgsSpecDict.argPositionFind("0&2")
                argChoices = cmndArgsSpec.argChoicesGet()
                argChoices.pop(0)
                cmndArgs= argChoices

        retVal = bpoSr_runBaseObtain_root(
            bpoId=bpoId,
            sr=sr,
        )

        if interactive:
            icm.ANN_write("{}".format(retVal))
            for each in cmndArgs:
                if each == "var":
                    icm.ANN_write("{each}".format(each=bpoSr_runBaseObtain_var(bpoId, sr)))
                elif each == "tmp":
                    icm.ANN_write("{each}".format(each=bpoSr_runBaseObtain_tmp(bpoId, sr)))
                elif each == "log":
                    icm.ANN_write("{each}".format(each=bpoSr_runBaseObtain_log(bpoId, sr)))
                else:
                    icm.EH_problem_usageError("")

        return cmndOutcome.set(
            opError=icm.notAsFailure(retVal),
            opResults=retVal,
        )

####+BEGIN: bx:icm:python:method :methodName "cmndArgsSpec" :methodType "anyOrNone" :retType "bool" :deco "default" :argsList ""
    """
**  [[elisp:(org-cycle)][| ]] [[elisp:(org-show-subtree)][|=]] [[elisp:(show-children 10)][|V]] [[elisp:(bx:orgm:indirectBufOther)][|>]] [[elisp:(bx:orgm:indirectBufMain)][|I]] [[elisp:(blee:ppmm:org-mode-toggle)][|N]] [[elisp:(org-top-overview)][|O]] [[elisp:(progn (org-shifttab) (org-content))][|C]] [[elisp:(delete-other-windows)][|1]]  Method-anyOrNone :: /cmndArgsSpec/ retType=bool argsList=nil deco=default  [[elisp:(org-cycle)][| ]]
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
            argName="cmndArgs",
            argDefault=None,
            argChoices=['all', 'var', 'tmp', 'log',],
            argDescription="Rest of args for use by action"
        )

        return cmndArgsSpecDict

    
####+BEGIN: bx:icm:python:method :methodName "cmndDocStr" :methodType "anyOrNone" :retType "bool" :deco "default" :argsList ""
    """
**  [[elisp:(org-cycle)][| ]] [[elisp:(org-show-subtree)][|=]] [[elisp:(show-children 10)][|V]] [[elisp:(bx:orgm:indirectBufOther)][|>]] [[elisp:(bx:orgm:indirectBufMain)][|I]] [[elisp:(blee:ppmm:org-mode-toggle)][|N]] [[elisp:(org-top-overview)][|O]] [[elisp:(progn (org-shifttab) (org-content))][|C]] [[elisp:(delete-other-windows)][|1]]  Method-anyOrNone :: /cmndDocStr/ retType=bool argsList=nil deco=default  [[elisp:(org-cycle)][| ]]
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
