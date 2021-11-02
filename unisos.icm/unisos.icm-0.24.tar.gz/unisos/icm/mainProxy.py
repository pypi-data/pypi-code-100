# -*- coding: utf-8 -*-
"""\
*    *[Summary]* ::  A /library/ with ICM Cmnds to support Service Object processing facilities
"""

moduleDescription="""
*       [[elisp:(org-cycle)][| *Description:* | ]]
**  [[elisp:(org-cycle)][| ]]  [Xref]          :: *[Related/Xrefs:]*  <<Xref-Here->>  -- External Documents  [[elisp:(org-cycle)][| ]]

**  [[elisp:(org-cycle)][| ]]   Model and Terminology                                      :Overview:
*** bxpRootXxFile   -- /etc/bystarRoot, ~/.bystarRoot, /bystar
*** bxpRoot         -- Base For This Module
*** bpb             -- ByStar Platform Base, Location Of Relevant Parts (Bisos, blee, bsip
*** bpd             -- ByStar Platform Directory (Object), An instance of Class BxpBaseDir
**      [End-Of-Description]
"""

moduleUsage="""
*       [[elisp:(org-cycle)][| *Usage:* | ]]

**      How-Tos:
**      [End-Of-Usage]
"""

moduleStatus="""
*       [[elisp:(org-cycle)][| *Status:* | ]]
**  [[elisp:(org-cycle)][| ]]  [Info]          :: *[Current-Info:]* Status/Maintenance -- General TODO List [[elisp:(org-cycle)][| ]]
** TODO [[elisp:(org-cycle)][| ]]  Current         :: Just getting started [[elisp:(org-cycle)][| ]]
**      [End-Of-Status]
"""

####+BEGIN: bx:icm:python:top-of-file :partof "bystar" :copyleft "halaal+minimal"
"""
*  This file:/de/bx/nne/dev-py/pypi/pkgs/bisos/common/dev/bisos/common/serviceObject.py :: [[elisp:(org-cycle)][| ]]
 is part of The Libre-Halaal ByStar Digital Ecosystem. http://www.by-star.net
 *CopyLeft*  This Software is a Libre-Halaal Poly-Existential. See http://www.freeprotocols.org
 A Python Interactively Command Module (PyICM). Part Of ByStar.
 Best Developed With COMEEGA-Emacs And Best Used With Blee-ICM-Players.
 Warning: All edits wityhin Dynamic Blocks may be lost.
"""
####+END:


"""
*  [[elisp:(org-cycle)][| *Lib-Module-INFO:* |]] :: Author, Copyleft and Version Information
"""

####+BEGIN: bx:global:lib:name-py :style "fileName"
__libName__ = "serviceObject"
####+END:

####+BEGIN: bx:global:timestamp:version-py :style "date"
__version__ = "201805282859"
####+END:

####+BEGIN: bx:global:icm:status-py :status "Production"
__status__ = "Production"
####+END:

__credits__ = [""]

####+BEGIN: bx:dblock:global:file-insert-cond :cond "./blee.el" :file "/libre/ByStar/InitialTemplates/update/sw/icm/py/icmInfo-mbNedaGpl.py"
icmInfo = {
    'authors':         ["[[http://mohsen.1.banan.byname.net][Mohsen Banan]]"],
    'copyright':       "Copyright 2017, [[http://www.neda.com][Neda Communications, Inc.]]",
    'licenses':        ["[[https://www.gnu.org/licenses/agpl-3.0.en.html][Affero GPL]]", "Libre-Halaal Services License", "Neda Commercial License"],
    'maintainers':     ["[[http://mohsen.1.banan.byname.net][Mohsen Banan]]",],
    'contacts':        ["[[http://mohsen.1.banan.byname.net/contact]]",],
    'partOf':          ["[[http://www.by-star.net][Libre-Halaal ByStar Digital Ecosystem]]",]
}
####+END:

####+BEGIN: bx:icm:python:topControls 
"""
*  [[elisp:(org-cycle)][|/Controls/| ]] :: [[elisp:(org-show-subtree)][|=]]  [[elisp:(show-all)][Show-All]]  [[elisp:(org-shifttab)][Overview]]  [[elisp:(progn (org-shifttab) (org-content))][Content]] | [[file:Panel.org][Panel]] | [[elisp:(blee:ppmm:org-mode-toggle)][Nat]] | [[elisp:(bx:org:run-me)][Run]] | [[elisp:(bx:org:run-me-eml)][RunEml]] | [[elisp:(delete-other-windows)][(1)]] | [[elisp:(progn (save-buffer) (kill-buffer))][S&Q]]  [[elisp:(save-buffer)][Save]]  [[elisp:(kill-buffer)][Quit]] [[elisp:(org-cycle)][| ]]
** /Version Control/ ::  [[elisp:(call-interactively (quote cvs-update))][cvs-update]]  [[elisp:(vc-update)][vc-update]] | [[elisp:(bx:org:agenda:this-file-otherWin)][Agenda-List]]  [[elisp:(bx:org:todo:this-file-otherWin)][ToDo-List]]
"""
####+END:

"""
* 
####+BEGIN: bx:dblock:global:file-insert-cond :cond "./blee.el" :file "/bisos/apps/defaults/software/plusOrg/dblock/inserts/pythonWb.org"
*  /Python Workbench/ ::  [[elisp:(org-cycle)][| ]]  [[elisp:(python-check (format "/bisos/venv/py3/bisos3/bin/python -m pyclbr %s" (bx:buf-fname))))][pyclbr]] || [[elisp:(python-check (format "/bisos/venv/py3/bisos3/bin/python -m pydoc ./%s" (bx:buf-fname))))][pydoc]] || [[elisp:(python-check (format "/bisos/pipx/bin/pyflakes %s" (bx:buf-fname)))][pyflakes]] | [[elisp:(python-check (format "/bisos/pipx/bin/pychecker %s" (bx:buf-fname))))][pychecker (executes)]] | [[elisp:(python-check (format "/bisos/pipx/bin/pycodestyle %s" (bx:buf-fname))))][pycodestyle]] | [[elisp:(python-check (format "/bisos/pipx/bin/flake8 %s" (bx:buf-fname))))][flake8]] | [[elisp:(python-check (format "/bisos/pipx/bin/pylint %s" (bx:buf-fname))))][pylint]]  [[elisp:(org-cycle)][| ]]
####+END:
"""


####+BEGIN: bx:icm:python:section :title "ContentsList"
"""
*  [[elisp:(beginning-of-buffer)][Top]] ################ [[elisp:(blee:ppmm:org-mode-toggle)][Nat]] [[elisp:(delete-other-windows)][(1)]]    *ContentsList*  [[elisp:(org-cycle)][| ]]  [[elisp:(org-show-subtree)][|=]] 
"""
####+END:


####+BEGIN: bx:dblock:python:icmItem :itemType "=Imports=" :itemTitle "*IMPORTS*"
"""
*  [[elisp:(org-cycle)][| ]]  [[elisp:(org-show-subtree)][|=]] [[elisp:(show-children 10)][|V]] [[elisp:(org-tree-to-indirect-buffer)][|>]] [[elisp:(blee:ppmm:org-mode-toggle)][Nat]] [[elisp:(beginning-of-buffer)][Top]] [[elisp:(delete-other-windows)][(1)]] || =Imports=      :: *IMPORTS*  [[elisp:(org-cycle)][| ]]
"""
####+END:

#import os
#import collections
#import enum

import sys
import types

####+BEGIN: bx:dblock:global:file-insert :file "/libre/ByStar/InitialTemplates/update/sw/icm/py/importUcfIcmG.py"
from unisos import ucf
from unisos import icm

icm.unusedSuppressForEval(ucf.__file__)  # in case icm and ucf are not used

G = icm.IcmGlobalContext()
#G.icmLibsAppend = __file__
#G.qicmCmndsLibsAppend = __file__

####+END:

import __main__

from bisos.platform import bxPlatformConfig
#from bisos.platform import bxPlatformThis

#import shutil
#import copy

####+BEGIN: bx:dblock:python:section :title "Library Description (Overview)"
"""
*  [[elisp:(beginning-of-buffer)][Top]] ################ [[elisp:(blee:ppmm:org-mode-toggle)][Nat]] [[elisp:(delete-other-windows)][(1)]]    *Library Description (Overview)*  [[elisp:(org-cycle)][| ]]  [[elisp:(org-show-subtree)][|=]] 
"""
####+END:

####+BEGIN: bx:dblock:python:section :title "Directory Base Locations"
"""
*  [[elisp:(beginning-of-buffer)][Top]] ################ [[elisp:(blee:ppmm:org-mode-toggle)][Nat]] [[elisp:(delete-other-windows)][(1)]]    *Directory Base Locations*  [[elisp:(org-cycle)][| ]]  [[elisp:(org-show-subtree)][|=]] 
"""
####+END:


####+BEGIN: bx:dblock:python:subSection :title "Bxo Roots And InfoBases"
"""
*  [[elisp:(beginning-of-buffer)][Top]] ================ [[elisp:(blee:ppmm:org-mode-toggle)][Nat]] [[elisp:(delete-other-windows)][(1)]]          *Bxo Roots And InfoBases*  [[elisp:(org-cycle)][| ]]  [[elisp:(org-show-subtree)][|=]] 
"""
####+END:



####+BEGIN: bx:icm:python:func :funcName "G_main" :funcType "FrameWrk" :retType "Void" :deco "" :argsList ""
"""
*  [[elisp:(org-cycle)][| ]]  [[elisp:(org-show-subtree)][|=]] [[elisp:(show-children 10)][|V]] [[elisp:(org-tree-to-indirect-buffer)][|>]] [[elisp:(blee:ppmm:org-mode-toggle)][Nat]] [[elisp:(beginning-of-buffer)][Top]] [[elisp:(delete-other-windows)][(1)]] || Func-FrameWrk  :: /G_main/ retType=Void argsList=nil  [[elisp:(org-cycle)][| ]]
"""
def G_main():
####+END:
    """
** Replaces ICM dispatcher for other command line args parsings.
"""
    pass

####+BEGIN: bx:icm:python:icmItem :itemType "Configuration" :itemTitle "= =Framework::= g_ Settings -- ICMs Imports ="
"""
*  [[elisp:(org-cycle)][| ]]  [[elisp:(org-show-subtree)][|=]] [[elisp:(show-children 10)][|V]] [[elisp:(org-tree-to-indirect-buffer)][|>]] [[elisp:(blee:ppmm:org-mode-toggle)][Nat]] [[elisp:(beginning-of-buffer)][Top]] [[elisp:(delete-other-windows)][(1)]] || Configuration  :: = =Framework::= g_ Settings -- ICMs Imports =  [[elisp:(org-cycle)][| ]]
"""
####+END:

# g_examples = __main__.examples  # or None
# g_mainEntry = None  # or G_main

####+BEGIN: bx:dblock:global:file-insert :file "/libre/ByStar/InitialTemplates/update/sw/icm/py/icm2.G_main.py"
"""
*  [[elisp:(beginning-of-buffer)][Top]] # /Dblk-Begin/ # [[elisp:(blee:ppmm:org-mode-toggle)][Nat]] [[elisp:(delete-other-windows)][(1)]]    *= =Framework::= ICM main() =*
"""

def classedCmndsDict(importedCmndsModules):
    """
** Should be done here, can not be done in icm library because of the evals.
"""
    import importlib
    importedCmndsFilesList=[]
    importedTagsList=[]
    for moduleName in importedCmndsModules:
        #print(f"moduleName={moduleName}")
        moduleNameList = moduleName.split(".")
        importTag = moduleNameList.pop()
        importModule = ".".join(moduleNameList)
        #print(f"importTag= {importTag} -- moduleNameList={moduleNameList} -- importModule={importModule}")
        _tmp = importlib.import_module(importModule)
        exec(f"{importTag} = _tmp.{importTag}") # assignment is a statement
        #eval(f"print({importTag}.__file__)") # DEBUG
        eval(f"importedCmndsFilesList.append({importTag}.__file__)") # expression
        importedTagsList.append(importTag)

    #print(importedCmndsFilesList)
    #print(importedTagsList)

    callDict = dict()
    for eachCmnd in icm.cmndList_mainsMethods().cmnd(
            interactive=False,
            importedCmnds={}, # __main__.g_importedCmnds -- Being obsoleted
            mainFileName=__main__.__file__,
            importedCmndsFilesList=importedCmndsFilesList,
    ):
        #print(f"eachCmnd={eachCmnd}")
        try:
            callDict[eachCmnd] = eval("__main__.{}".format(eachCmnd))
        except AttributeError:
            #print(f"AttributeError -- __main__.{eachCmnd} -- ignored")
            pass
        except NameError:
            #print(f"NameError -- __main__.{eachCmnd} -- ignored")
            pass
        else:
            #print(f"Added __main__.{eachCmnd}")
            continue

        for importTag in importedTagsList:
            #print(f"trying {importTag}")
            try:
                #print(f"Evaling -- {importTag}.{eachCmnd}")
                eval(f"{importTag}.{eachCmnd}")
            except AttributeError:
                #print(f"AttributeError -- {importTag}.{eachCmnd}")
                continue
            try:
                callDict[eachCmnd] = eval(f"{importTag}.{eachCmnd}")
                #print("callDict -- {importTag}.{eachCmnd}")
                break
            except NameError:
                pass


    return callDict


G = icm.IcmGlobalContext()

# icmInfo = G.icmInfo()

# try:
#    __main__.icmInfo
# except AttributeError:
#     pass
# else:
#     icmInfo.update(__main__.icmInfo)

#     icmInfo['icmName'] = __main__.__icmName__
#     icmInfo['version'] = __main__.__version__
#     icmInfo['status'] = __main__.__status__
#     icmInfo['credits'] = __main__.__credits__

#     G.icmInfoSet(icmInfo)

def g_icmMain(
        noCmndEntry=None,   # To Be Obsoleted
        extraParamsHook=None,
        importedCmndsModules=[],
        icmPreCmndsHook=None,
        icmPostCmndsHook=None,
        icmInfo=None,
):
    """This ICM's specific information is passed to G_mainWithClass"""

    G.icmInfoSet(icmInfo)

    examples = None
    mainEntry = None

    if noCmndEntry:
        if type(noCmndEntry) is types.FunctionType:
            mainEntry = noCmndEntry
            # examples is None
        else:  # We then assume it is a Cmnd
            examples = noCmndEntry
            mainEntry = noCmndEntry

    sys.exit(
        icm.G_mainWithClass(
            inArgv=sys.argv[1:],                 # Mandatory
            #extraArgs=__main__.g_argsExtraSpecify,        # Mandatory
            extraArgs=extraParamsHook,
            G_examples=examples,               # Mandatory
            classedCmndsDict=classedCmndsDict(importedCmndsModules),   # Mandatory
            mainEntry=mainEntry,
            g_icmPreCmnds=icmPreCmndsHook,
            g_icmPostCmnds=icmPostCmndsHook,
        )
    )


####+BEGIN: bx:icm:python:section :title "End Of Editable Text"
"""
*  [[elisp:(beginning-of-buffer)][Top]] ################ [[elisp:(blee:ppmm:org-mode-toggle)][Nat]] [[elisp:(delete-other-windows)][(1)]]    *End Of Editable Text*  [[elisp:(org-cycle)][| ]]  [[elisp:(org-show-subtree)][|=]] 
"""
####+END:

####+BEGIN: bx:dblock:global:file-insert-cond :cond "./blee.el" :file "/libre/ByStar/InitialTemplates/software/plusOrg/dblock/inserts/endOfFileControls.org"
#+STARTUP: showall
####+END:
