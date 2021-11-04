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
icmInfo['moduleName'] = "palsBases"
####+END:

####+BEGIN: bx:icm:py:version-timestamp :style "date"
icmInfo['version'] = "202110161301"
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
*  This file:/bisos/git/auth/bxRepos/bisos-pip/pals/py3/bisos/pals/palsBases.py :: [[elisp:(org-cycle)][| ]]
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
# import pwd
# import grp
# import collections
# import enum
#

#import traceback

import pathlib

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

# from bisos.basics import pattern

from bisos.bpo import bpo
from bisos.pals import palsBpo
from bisos.pals import palsSis
from bisos.icm import fpath

####+BEGIN: bx:dblock:python:section :title "Start Your Sections Here"
"""
*  [[elisp:(beginning-of-buffer)][Top]] ############## [[elisp:(blee:ppmm:org-mode-toggle)][Nat]] [[elisp:(delete-other-windows)][(1)]]    *Start Your Sections Here*  [[elisp:(org-cycle)][| ]]  [[elisp:(org-show-subtree)][|=]]
"""
####+END:


####+BEGIN: bx:dblock:python:class :className "PalsBases" :superClass "object" :comment "Bases of a palsBpo" :classType "basic"
"""
*  _[[elisp:(blee:menu-sel:outline:popupMenu)][±]]_ _[[elisp:(blee:menu-sel:navigation:popupMenu)][Ξ]]_ [[elisp:(bx:orgm:indirectBufOther)][|>]] *[[elisp:(blee:ppmm:org-mode-toggle)][|N]]*  Class-basic :: /PalsBases/ object =Bases of a palsBpo=  [[elisp:(org-cycle)][| ]]
"""
class PalsBases(object):
####+END:
    """
** Abstraction of the base ByStar Portable Object
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
            palsBpo,
    ):
        self.bpoId = bpoId
        self.palsBpo = palsBpo

####+BEGIN: bx:icm:py3:method :methodName "basesUpdate" :deco "default"
    """
**  _[[elisp:(blee:menu-sel:outline:popupMenu)][±]]_ _[[elisp:(blee:menu-sel:navigation:popupMenu)][Ξ]]_ [[elisp:(bx:orgm:indirectBufOther)][|>]] *[[elisp:(blee:ppmm:org-mode-toggle)][|N]]*  Method-    :: /basesUpdate/ deco=default  [[elisp:(org-cycle)][| ]]
"""
    @icm.subjectToTracking(fnLoc=True, fnEntry=True, fnExit=True)
    def basesUpdate(
####+END:
            self,
    ):
        self.varBasePath_update()
        self.controlBasePath_update()
        self.logBasePath_update()
        self.curBasePath_update()
        self.tmpBasePath_update()
        return


####+BEGIN: bx:icm:py3:method :methodName "varBasePath_update" :deco "default"
    """
**  _[[elisp:(blee:menu-sel:outline:popupMenu)][±]]_ _[[elisp:(blee:menu-sel:navigation:popupMenu)][Ξ]]_ [[elisp:(bx:orgm:indirectBufOther)][|>]] *[[elisp:(blee:ppmm:org-mode-toggle)][|N]]*  Method-    :: /varBasePath_update/ deco=default  [[elisp:(org-cycle)][| ]]
"""
    @icm.subjectToTracking(fnLoc=True, fnEntry=True, fnExit=True)
    def varBasePath_update(
####+END:
            self,
    ) -> pathlib.Path:

        actualBasePath = pathlib.Path(
            os.path.join(
                "/var/bisos/bpo/var",
                self.bpoId,
                "bpo",
            )
        )
        actualBasePath.mkdir(parents=True, exist_ok=True)
        bpoBasePath  = self.varBasePath_obtain()

        return fpath.symlinkUpdate(actualBasePath, bpoBasePath)


####+BEGIN: bx:icm:py3:method :methodName "varBasePath_obtain" :deco "default"
    """
**  _[[elisp:(blee:menu-sel:outline:popupMenu)][±]]_ _[[elisp:(blee:menu-sel:navigation:popupMenu)][Ξ]]_ [[elisp:(bx:orgm:indirectBufOther)][|>]] *[[elisp:(blee:ppmm:org-mode-toggle)][|N]]*  Method-    :: /varBasePath_obtain/ deco=default  [[elisp:(org-cycle)][| ]]
"""
    @icm.subjectToTracking(fnLoc=True, fnEntry=True, fnExit=True)
    def varBasePath_obtain(
####+END:
            self,
    ) -> pathlib.Path:
        return (
            pathlib.Path(
                os.path.join(
                    self.palsBpo.bpoBaseDir, "var"
                )
            )
        )


####+BEGIN: bx:icm:py3:method :methodName "controlBasePath_update" :deco "default"
    """
**  _[[elisp:(blee:menu-sel:outline:popupMenu)][±]]_ _[[elisp:(blee:menu-sel:navigation:popupMenu)][Ξ]]_ [[elisp:(bx:orgm:indirectBufOther)][|>]] *[[elisp:(blee:ppmm:org-mode-toggle)][|N]]*  Method-    :: /controlBasePath_update/ deco=default  [[elisp:(org-cycle)][| ]]
"""
    @icm.subjectToTracking(fnLoc=True, fnEntry=True, fnExit=True)
    def controlBasePath_update(
####+END:
            self,
    ) -> pathlib.Path:

        actualBasePath = pathlib.Path(
            os.path.join(
                "/var/bisos/bpo/control",
                self.bpoId,
                "bpo",
            )
        )
        actualBasePath.mkdir(parents=True, exist_ok=True)
        bpoBasePath  = self.controlBasePath_obtain()

        return fpath.symlinkUpdate(actualBasePath, bpoBasePath)


####+BEGIN: bx:icm:py3:method :methodName "controlBasePath_obtain" :deco "default"
    """
**  _[[elisp:(blee:menu-sel:outline:popupMenu)][±]]_ _[[elisp:(blee:menu-sel:navigation:popupMenu)][Ξ]]_ [[elisp:(bx:orgm:indirectBufOther)][|>]] *[[elisp:(blee:ppmm:org-mode-toggle)][|N]]*  Method-    :: /controlBasePath_obtain/ deco=default  [[elisp:(org-cycle)][| ]]
"""
    @icm.subjectToTracking(fnLoc=True, fnEntry=True, fnExit=True)
    def controlBasePath_obtain(
####+END:
            self,
    ) -> pathlib.Path:
        return (
            pathlib.Path(
                os.path.join(
                    self.palsBpo.bpoBaseDir, "control"
                )
            )
        )


####+BEGIN: bx:icm:py3:method :methodName "logBasePath_update" :deco "default"
    """
**  _[[elisp:(blee:menu-sel:outline:popupMenu)][±]]_ _[[elisp:(blee:menu-sel:navigation:popupMenu)][Ξ]]_ [[elisp:(bx:orgm:indirectBufOther)][|>]] *[[elisp:(blee:ppmm:org-mode-toggle)][|N]]*  Method-    :: /logBasePath_update/ deco=default  [[elisp:(org-cycle)][| ]]
"""
    @icm.subjectToTracking(fnLoc=True, fnEntry=True, fnExit=True)
    def logBasePath_update(
####+END:
           self,
    ) -> pathlib.Path:

        actualBasePath = pathlib.Path(
            os.path.join(
                "/var/bisos/bpo/log",
                self.bpoId,
                "bpo",
            )
        )
        actualBasePath.mkdir(parents=True, exist_ok=True)
        bpoBasePath  = self.logBasePath_obtain()

        return fpath.symlinkUpdate(actualBasePath, bpoBasePath)


####+BEGIN: bx:icm:py3:method :methodName "logBasePath_obtain" :deco "default"
    """
**  _[[elisp:(blee:menu-sel:outline:popupMenu)][±]]_ _[[elisp:(blee:menu-sel:navigation:popupMenu)][Ξ]]_ [[elisp:(bx:orgm:indirectBufOther)][|>]] *[[elisp:(blee:ppmm:org-mode-toggle)][|N]]*  Method-    :: /logBasePath_obtain/ deco=default  [[elisp:(org-cycle)][| ]]
"""
    @icm.subjectToTracking(fnLoc=True, fnEntry=True, fnExit=True)
    def logBasePath_obtain(
####+END:
            self,
    ) -> pathlib.Path:
        return (
            pathlib.Path(
                os.path.join(
                    self.palsBpo.bpoBaseDir, "log"
                )
            )
        )


####+BEGIN: bx:icm:py3:method :methodName "tmpBasePath_update" :deco "default"
    """
**  _[[elisp:(blee:menu-sel:outline:popupMenu)][±]]_ _[[elisp:(blee:menu-sel:navigation:popupMenu)][Ξ]]_ [[elisp:(bx:orgm:indirectBufOther)][|>]] *[[elisp:(blee:ppmm:org-mode-toggle)][|N]]*  Method-    :: /tmpBasePath_update/ deco=default  [[elisp:(org-cycle)][| ]]
"""
    @icm.subjectToTracking(fnLoc=True, fnEntry=True, fnExit=True)
    def tmpBasePath_update(
####+END:
          self,
    ) -> pathlib.Path:

        actualBasePath = pathlib.Path(
            os.path.join(
                "/tmp/bisos",
            )
        )
        actualBasePath.mkdir(parents=True, exist_ok=True)
        bpoBasePath  = self.tmpBasePath_obtain()

        return fpath.symlinkUpdate(actualBasePath, bpoBasePath)

####+BEGIN: bx:icm:py3:method :methodName "tmpBasePath_obtain" :deco "default"
    """
**  _[[elisp:(blee:menu-sel:outline:popupMenu)][±]]_ _[[elisp:(blee:menu-sel:navigation:popupMenu)][Ξ]]_ [[elisp:(bx:orgm:indirectBufOther)][|>]] *[[elisp:(blee:ppmm:org-mode-toggle)][|N]]*  Method-    :: /tmpBasePath_obtain/ deco=default  [[elisp:(org-cycle)][| ]]
"""
    @icm.subjectToTracking(fnLoc=True, fnEntry=True, fnExit=True)
    def tmpBasePath_obtain(
####+END:
            self,
    ) -> pathlib.Path:
        return (
            pathlib.Path(
                os.path.join(
                    self.palsBpo.bpoBaseDir, "tmp"
                )
            )
        )


####+BEGIN: bx:icm:py3:method :methodName "curBasePath_update" :deco "default"
    """
**  _[[elisp:(blee:menu-sel:outline:popupMenu)][±]]_ _[[elisp:(blee:menu-sel:navigation:popupMenu)][Ξ]]_ [[elisp:(bx:orgm:indirectBufOther)][|>]] *[[elisp:(blee:ppmm:org-mode-toggle)][|N]]*  Method-    :: /curBasePath_update/ deco=default  [[elisp:(org-cycle)][| ]]
"""
    @icm.subjectToTracking(fnLoc=True, fnEntry=True, fnExit=True)
    def curBasePath_update(
####+END:
          self,
    ) -> pathlib.Path:

        actualBasePath = pathlib.Path(
            os.path.join(
                "/var/bisos/bpo/cur",
                self.bpoId,
                "bpo",
            )
        )
        actualBasePath.mkdir(parents=True, exist_ok=True)
        bpoBasePath  = self.curBasePath_obtain()

        return fpath.symlinkUpdate(actualBasePath, bpoBasePath)

####+BEGIN: bx:icm:py3:method :methodName "curBasePath_obtain" :deco "default"
    """
**  _[[elisp:(blee:menu-sel:outline:popupMenu)][±]]_ _[[elisp:(blee:menu-sel:navigation:popupMenu)][Ξ]]_ [[elisp:(bx:orgm:indirectBufOther)][|>]] *[[elisp:(blee:ppmm:org-mode-toggle)][|N]]*  Method-    :: /curBasePath_obtain/ deco=default  [[elisp:(org-cycle)][| ]]
"""
    @icm.subjectToTracking(fnLoc=True, fnEntry=True, fnExit=True)
    def curBasePath_obtain(
####+END:
            self,
    ) -> pathlib.Path:
        return (
            pathlib.Path(
                os.path.join(
                    self.palsBpo.bpoBaseDir, "cur"
                )
            )
        )


####+BEGIN: bx:dblock:python:class :className "PalsSivdBases" :superClass "object" :comment "Bases of a palsBpo" :classType "basic"
"""
*  _[[elisp:(blee:menu-sel:outline:popupMenu)][±]]_ _[[elisp:(blee:menu-sel:navigation:popupMenu)][Ξ]]_ [[elisp:(bx:orgm:indirectBufOther)][|>]] *[[elisp:(blee:ppmm:org-mode-toggle)][|N]]*  Class-basic :: /PalsSivdBases/ object =Bases of a palsBpo=  [[elisp:(org-cycle)][| ]]
"""
class PalsSivdBases(object):
####+END:
    """
** Abstraction of the base ByStar Portable Object
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
            palsBpo,
            sivdId,
    ):
        self.bpoId = bpoId
        self.palsBpo = palsBpo
        self.sivdId = sivdId
        self.palsBases = PalsBases(bpoId, palsBpo)

####+BEGIN: bx:icm:py3:method :methodName "basesUpdate" :deco "default"
    """
**  _[[elisp:(blee:menu-sel:outline:popupMenu)][±]]_ _[[elisp:(blee:menu-sel:navigation:popupMenu)][Ξ]]_ [[elisp:(bx:orgm:indirectBufOther)][|>]] *[[elisp:(blee:ppmm:org-mode-toggle)][|N]]*  Method-    :: /basesUpdate/ deco=default  [[elisp:(org-cycle)][| ]]
"""
    @icm.subjectToTracking(fnLoc=True, fnEntry=True, fnExit=True)
    def basesUpdate(
####+END:
            self,
    ):
        self.varBasePath_update()
        self.controlBasePath_update()
        self.logBasePath_update()
        self.curBasePath_update()
        self.tmpBasePath_update()
        return


####+BEGIN: bx:icm:py3:method :methodName "varBasePath_update" :deco "default"
    """
**  _[[elisp:(blee:menu-sel:outline:popupMenu)][±]]_ _[[elisp:(blee:menu-sel:navigation:popupMenu)][Ξ]]_ [[elisp:(bx:orgm:indirectBufOther)][|>]] *[[elisp:(blee:ppmm:org-mode-toggle)][|N]]*  Method-    :: /varBasePath_update/ deco=default  [[elisp:(org-cycle)][| ]]
"""
    @icm.subjectToTracking(fnLoc=True, fnEntry=True, fnExit=True)
    def varBasePath_update(
####+END:
            self,
    ) -> pathlib.Path:

        actualBasePath = pathlib.Path(
            os.path.join(
                "/var/bisos/bpo/var",
                self.bpoId,
                "bpo",
                self.sivdId,
            )
        )
        actualBasePath.mkdir(parents=True, exist_ok=True)
        bpoBasePath  = self.varBasePath_obtain()

        return fpath.symlinkUpdate(actualBasePath, bpoBasePath)


####+BEGIN: bx:icm:py3:method :methodName "varBasePath_obtain" :deco "default"
    """
**  _[[elisp:(blee:menu-sel:outline:popupMenu)][±]]_ _[[elisp:(blee:menu-sel:navigation:popupMenu)][Ξ]]_ [[elisp:(bx:orgm:indirectBufOther)][|>]] *[[elisp:(blee:ppmm:org-mode-toggle)][|N]]*  Method-    :: /varBasePath_obtain/ deco=default  [[elisp:(org-cycle)][| ]]
"""
    @icm.subjectToTracking(fnLoc=True, fnEntry=True, fnExit=True)
    def varBasePath_obtain(
####+END:
            self,
    ) -> pathlib.Path:
        return (
            pathlib.Path(
                os.path.join(
                    palsSis.sivd_instanceBaseDir(
                        self.bpoId,
                        self.sivdId,
                    ),
                    "var",
                )
            )
        )


####+BEGIN: bx:icm:py3:method :methodName "controlBasePath_update" :deco "default"
    """
**  _[[elisp:(blee:menu-sel:outline:popupMenu)][±]]_ _[[elisp:(blee:menu-sel:navigation:popupMenu)][Ξ]]_ [[elisp:(bx:orgm:indirectBufOther)][|>]] *[[elisp:(blee:ppmm:org-mode-toggle)][|N]]*  Method-    :: /controlBasePath_update/ deco=default  [[elisp:(org-cycle)][| ]]
"""
    @icm.subjectToTracking(fnLoc=True, fnEntry=True, fnExit=True)
    def controlBasePath_update(
####+END:
            self,
    ) -> pathlib.Path:

        actualBasePath = pathlib.Path(
            os.path.join(
                "/var/bisos/bpo/control",
                self.bpoId,
                "bpo",
                self.sivdId,
            )
        )
        actualBasePath.mkdir(parents=True, exist_ok=True)
        bpoBasePath  = self.controlBasePath_obtain()

        return fpath.symlinkUpdate(actualBasePath, bpoBasePath)


####+BEGIN: bx:icm:py3:method :methodName "controlBasePath_obtain" :deco "default"
    """
**  _[[elisp:(blee:menu-sel:outline:popupMenu)][±]]_ _[[elisp:(blee:menu-sel:navigation:popupMenu)][Ξ]]_ [[elisp:(bx:orgm:indirectBufOther)][|>]] *[[elisp:(blee:ppmm:org-mode-toggle)][|N]]*  Method-    :: /controlBasePath_obtain/ deco=default  [[elisp:(org-cycle)][| ]]
"""
    @icm.subjectToTracking(fnLoc=True, fnEntry=True, fnExit=True)
    def controlBasePath_obtain(
####+END:
            self,
    ) -> pathlib.Path:
        return (
            pathlib.Path(
                os.path.join(
                    palsSis.sivd_instanceBaseDir(
                        self.bpoId,
                        self.sivdId,
                    ),
                    "control",
                )
            )
        )


####+BEGIN: bx:icm:py3:method :methodName "logBasePath_update" :deco "default"
    """
**  _[[elisp:(blee:menu-sel:outline:popupMenu)][±]]_ _[[elisp:(blee:menu-sel:navigation:popupMenu)][Ξ]]_ [[elisp:(bx:orgm:indirectBufOther)][|>]] *[[elisp:(blee:ppmm:org-mode-toggle)][|N]]*  Method-    :: /logBasePath_update/ deco=default  [[elisp:(org-cycle)][| ]]
"""
    @icm.subjectToTracking(fnLoc=True, fnEntry=True, fnExit=True)
    def logBasePath_update(
####+END:
           self,
    ) -> pathlib.Path:

        actualBasePath = pathlib.Path(
            os.path.join(
                "/var/bisos/bpo/log",
                self.bpoId,
                "bpo",
                self.sivdId,
            )
        )
        actualBasePath.mkdir(parents=True, exist_ok=True)
        bpoBasePath  = self.logBasePath_obtain()

        return fpath.symlinkUpdate(actualBasePath, bpoBasePath)


####+BEGIN: bx:icm:py3:method :methodName "logBasePath_obtain" :deco "default"
    """
**  _[[elisp:(blee:menu-sel:outline:popupMenu)][±]]_ _[[elisp:(blee:menu-sel:navigation:popupMenu)][Ξ]]_ [[elisp:(bx:orgm:indirectBufOther)][|>]] *[[elisp:(blee:ppmm:org-mode-toggle)][|N]]*  Method-    :: /logBasePath_obtain/ deco=default  [[elisp:(org-cycle)][| ]]
"""
    @icm.subjectToTracking(fnLoc=True, fnEntry=True, fnExit=True)
    def logBasePath_obtain(
####+END:
            self,
    ) -> pathlib.Path:
        return (
            pathlib.Path(
                os.path.join(
                    palsSis.sivd_instanceBaseDir(
                        self.bpoId,
                        self.sivdId,
                    ),
                    "log"
                )
            )
        )


####+BEGIN: bx:icm:py3:method :methodName "tmpBasePath_update" :deco "default"
    """
**  _[[elisp:(blee:menu-sel:outline:popupMenu)][±]]_ _[[elisp:(blee:menu-sel:navigation:popupMenu)][Ξ]]_ [[elisp:(bx:orgm:indirectBufOther)][|>]] *[[elisp:(blee:ppmm:org-mode-toggle)][|N]]*  Method-    :: /tmpBasePath_update/ deco=default  [[elisp:(org-cycle)][| ]]
"""
    @icm.subjectToTracking(fnLoc=True, fnEntry=True, fnExit=True)
    def tmpBasePath_update(
####+END:
          self,
    ) -> pathlib.Path:

        actualBasePath = pathlib.Path(
            os.path.join(
                "/tmp/bisos",
            )
        )
        actualBasePath.mkdir(parents=True, exist_ok=True)
        bpoBasePath  = self.tmpBasePath_obtain()

        return fpath.symlinkUpdate(actualBasePath, bpoBasePath)

####+BEGIN: bx:icm:py3:method :methodName "tmpBasePath_obtain" :deco "default"
    """
**  _[[elisp:(blee:menu-sel:outline:popupMenu)][±]]_ _[[elisp:(blee:menu-sel:navigation:popupMenu)][Ξ]]_ [[elisp:(bx:orgm:indirectBufOther)][|>]] *[[elisp:(blee:ppmm:org-mode-toggle)][|N]]*  Method-    :: /tmpBasePath_obtain/ deco=default  [[elisp:(org-cycle)][| ]]
"""
    @icm.subjectToTracking(fnLoc=True, fnEntry=True, fnExit=True)
    def tmpBasePath_obtain(
####+END:
            self,
    ) -> pathlib.Path:
        return (
            pathlib.Path(
                os.path.join(
                    palsSis.sivd_instanceBaseDir(
                        self.bpoId,
                        self.sivdId,
                    ),
                    "tmp",
                )
            )
        )


####+BEGIN: bx:icm:py3:method :methodName "curBasePath_update" :deco "default"
    """
**  _[[elisp:(blee:menu-sel:outline:popupMenu)][±]]_ _[[elisp:(blee:menu-sel:navigation:popupMenu)][Ξ]]_ [[elisp:(bx:orgm:indirectBufOther)][|>]] *[[elisp:(blee:ppmm:org-mode-toggle)][|N]]*  Method-    :: /curBasePath_update/ deco=default  [[elisp:(org-cycle)][| ]]
"""
    @icm.subjectToTracking(fnLoc=True, fnEntry=True, fnExit=True)
    def curBasePath_update(
####+END:
          self,
    ) -> pathlib.Path:

        actualBasePath = pathlib.Path(
            os.path.join(
                "/var/bisos/bpo/cur",
                self.bpoId,
                "bpo",
                self.sivdId,
            )
        )
        actualBasePath.mkdir(parents=True, exist_ok=True)
        bpoBasePath  = self.curBasePath_obtain()

        return fpath.symlinkUpdate(actualBasePath, bpoBasePath)

####+BEGIN: bx:icm:py3:method :methodName "curBasePath_obtain" :deco "default"
    """
**  _[[elisp:(blee:menu-sel:outline:popupMenu)][±]]_ _[[elisp:(blee:menu-sel:navigation:popupMenu)][Ξ]]_ [[elisp:(bx:orgm:indirectBufOther)][|>]] *[[elisp:(blee:ppmm:org-mode-toggle)][|N]]*  Method-    :: /curBasePath_obtain/ deco=default  [[elisp:(org-cycle)][| ]]
"""
    @icm.subjectToTracking(fnLoc=True, fnEntry=True, fnExit=True)
    def curBasePath_obtain(
####+END:
            self,
    ) -> pathlib.Path:
        return (
            pathlib.Path(
                os.path.join(
                    palsSis.sivd_instanceBaseDir(
                        self.bpoId,
                        self.sivdId,
                    ),
                    "cur",
                )
            )
        )



####+BEGIN: bx:dblock:python:class :className "PalsSiBases" :superClass "object" :comment "Bases of a palsBpo" :classType "basic"
"""
*  _[[elisp:(blee:menu-sel:outline:popupMenu)][±]]_ _[[elisp:(blee:menu-sel:navigation:popupMenu)][Ξ]]_ [[elisp:(bx:orgm:indirectBufOther)][|>]] *[[elisp:(blee:ppmm:org-mode-toggle)][|N]]*  Class-basic :: /PalsSiBases/ object =Bases of a palsBpo=  [[elisp:(org-cycle)][| ]]
"""
class PalsSiBases(object):
####+END:
    """
** Abstraction of the base ByStar Portable Object
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
            palsBpo,
            siId,
    ):
        self.bpoId = bpoId
        self.palsBpo = palsBpo
        self.siId = siId
        self.palsBases = PalsBases(bpoId, palsBpo)

####+BEGIN: bx:icm:py3:method :methodName "basesUpdate" :deco "default"
    """
**  _[[elisp:(blee:menu-sel:outline:popupMenu)][±]]_ _[[elisp:(blee:menu-sel:navigation:popupMenu)][Ξ]]_ [[elisp:(bx:orgm:indirectBufOther)][|>]] *[[elisp:(blee:ppmm:org-mode-toggle)][|N]]*  Method-    :: /basesUpdate/ deco=default  [[elisp:(org-cycle)][| ]]
"""
    @icm.subjectToTracking(fnLoc=True, fnEntry=True, fnExit=True)
    def basesUpdate(
####+END:
            self,
    ):
        self.varBasePath_update()
        self.controlBasePath_update()
        self.logBasePath_update()
        self.curBasePath_update()
        self.tmpBasePath_update()
        return


####+BEGIN: bx:icm:py3:method :methodName "varBasePath_update" :deco "default"
    """
**  _[[elisp:(blee:menu-sel:outline:popupMenu)][±]]_ _[[elisp:(blee:menu-sel:navigation:popupMenu)][Ξ]]_ [[elisp:(bx:orgm:indirectBufOther)][|>]] *[[elisp:(blee:ppmm:org-mode-toggle)][|N]]*  Method-    :: /varBasePath_update/ deco=default  [[elisp:(org-cycle)][| ]]
"""
    @icm.subjectToTracking(fnLoc=True, fnEntry=True, fnExit=True)
    def varBasePath_update(
####+END:
            self,
    ) -> pathlib.Path:

        actualBasePath = pathlib.Path(
            os.path.join(
                "/var/bisos/bpo/var",
                self.bpoId,
                "bpo",
                self.siId,
            )
        )
        actualBasePath.mkdir(parents=True, exist_ok=True)
        bpoBasePath  = self.varBasePath_obtain()

        return fpath.symlinkUpdate(actualBasePath, bpoBasePath)


####+BEGIN: bx:icm:py3:method :methodName "varBasePath_obtain" :deco "default"
    """
**  _[[elisp:(blee:menu-sel:outline:popupMenu)][±]]_ _[[elisp:(blee:menu-sel:navigation:popupMenu)][Ξ]]_ [[elisp:(bx:orgm:indirectBufOther)][|>]] *[[elisp:(blee:ppmm:org-mode-toggle)][|N]]*  Method-    :: /varBasePath_obtain/ deco=default  [[elisp:(org-cycle)][| ]]
"""
    @icm.subjectToTracking(fnLoc=True, fnEntry=True, fnExit=True)
    def varBasePath_obtain(
####+END:
            self,
    ) -> pathlib.Path:
        return (
            pathlib.Path(
                os.path.join(
                    palsSis.si_instanceBaseDir(
                        self.bpoId,
                        self.siId,
                    ),
                    "var",
                )
            )
        )


####+BEGIN: bx:icm:py3:method :methodName "controlBasePath_update" :deco "default"
    """
**  _[[elisp:(blee:menu-sel:outline:popupMenu)][±]]_ _[[elisp:(blee:menu-sel:navigation:popupMenu)][Ξ]]_ [[elisp:(bx:orgm:indirectBufOther)][|>]] *[[elisp:(blee:ppmm:org-mode-toggle)][|N]]*  Method-    :: /controlBasePath_update/ deco=default  [[elisp:(org-cycle)][| ]]
"""
    @icm.subjectToTracking(fnLoc=True, fnEntry=True, fnExit=True)
    def controlBasePath_update(
####+END:
            self,
    ) -> pathlib.Path:

        actualBasePath = pathlib.Path(
            os.path.join(
                "/var/bisos/bpo/control",
                self.bpoId,
                "bpo",
                self.siId,
            )
        )
        actualBasePath.mkdir(parents=True, exist_ok=True)
        bpoBasePath  = self.controlBasePath_obtain()

        return fpath.symlinkUpdate(actualBasePath, bpoBasePath)


####+BEGIN: bx:icm:py3:method :methodName "controlBasePath_obtain" :deco "default"
    """
**  _[[elisp:(blee:menu-sel:outline:popupMenu)][±]]_ _[[elisp:(blee:menu-sel:navigation:popupMenu)][Ξ]]_ [[elisp:(bx:orgm:indirectBufOther)][|>]] *[[elisp:(blee:ppmm:org-mode-toggle)][|N]]*  Method-    :: /controlBasePath_obtain/ deco=default  [[elisp:(org-cycle)][| ]]
"""
    @icm.subjectToTracking(fnLoc=True, fnEntry=True, fnExit=True)
    def controlBasePath_obtain(
####+END:
            self,
    ) -> pathlib.Path:
        return (
            pathlib.Path(
                os.path.join(
                    palsSis.si_instanceBaseDir(
                        self.bpoId,
                        self.siId,
                    ),
                    "control",
                )
            )
        )


####+BEGIN: bx:icm:py3:method :methodName "logBasePath_update" :deco "default"
    """
**  _[[elisp:(blee:menu-sel:outline:popupMenu)][±]]_ _[[elisp:(blee:menu-sel:navigation:popupMenu)][Ξ]]_ [[elisp:(bx:orgm:indirectBufOther)][|>]] *[[elisp:(blee:ppmm:org-mode-toggle)][|N]]*  Method-    :: /logBasePath_update/ deco=default  [[elisp:(org-cycle)][| ]]
"""
    @icm.subjectToTracking(fnLoc=True, fnEntry=True, fnExit=True)
    def logBasePath_update(
####+END:
           self,
    ) -> pathlib.Path:

        actualBasePath = pathlib.Path(
            os.path.join(
                "/var/bisos/bpo/log",
                self.bpoId,
                "bpo",
                self.siId,
            )
        )
        actualBasePath.mkdir(parents=True, exist_ok=True)
        bpoBasePath  = self.logBasePath_obtain()

        return fpath.symlinkUpdate(actualBasePath, bpoBasePath)


####+BEGIN: bx:icm:py3:method :methodName "logBasePath_obtain" :deco "default"
    """
**  _[[elisp:(blee:menu-sel:outline:popupMenu)][±]]_ _[[elisp:(blee:menu-sel:navigation:popupMenu)][Ξ]]_ [[elisp:(bx:orgm:indirectBufOther)][|>]] *[[elisp:(blee:ppmm:org-mode-toggle)][|N]]*  Method-    :: /logBasePath_obtain/ deco=default  [[elisp:(org-cycle)][| ]]
"""
    @icm.subjectToTracking(fnLoc=True, fnEntry=True, fnExit=True)
    def logBasePath_obtain(
####+END:
            self,
    ) -> pathlib.Path:
        return (
            pathlib.Path(
                os.path.join(
                    palsSis.si_instanceBaseDir(
                        self.bpoId,
                        self.siId,
                    ),
                    "log"
                )
            )
        )


####+BEGIN: bx:icm:py3:method :methodName "tmpBasePath_update" :deco "default"
    """
**  _[[elisp:(blee:menu-sel:outline:popupMenu)][±]]_ _[[elisp:(blee:menu-sel:navigation:popupMenu)][Ξ]]_ [[elisp:(bx:orgm:indirectBufOther)][|>]] *[[elisp:(blee:ppmm:org-mode-toggle)][|N]]*  Method-    :: /tmpBasePath_update/ deco=default  [[elisp:(org-cycle)][| ]]
"""
    @icm.subjectToTracking(fnLoc=True, fnEntry=True, fnExit=True)
    def tmpBasePath_update(
####+END:
          self,
    ) -> pathlib.Path:

        actualBasePath = pathlib.Path(
            os.path.join(
                "/tmp/bisos",
            )
        )
        actualBasePath.mkdir(parents=True, exist_ok=True)
        bpoBasePath  = self.tmpBasePath_obtain()

        return fpath.symlinkUpdate(actualBasePath, bpoBasePath)

####+BEGIN: bx:icm:py3:method :methodName "tmpBasePath_obtain" :deco "default"
    """
**  _[[elisp:(blee:menu-sel:outline:popupMenu)][±]]_ _[[elisp:(blee:menu-sel:navigation:popupMenu)][Ξ]]_ [[elisp:(bx:orgm:indirectBufOther)][|>]] *[[elisp:(blee:ppmm:org-mode-toggle)][|N]]*  Method-    :: /tmpBasePath_obtain/ deco=default  [[elisp:(org-cycle)][| ]]
"""
    @icm.subjectToTracking(fnLoc=True, fnEntry=True, fnExit=True)
    def tmpBasePath_obtain(
####+END:
            self,
    ) -> pathlib.Path:
        return (
            pathlib.Path(
                os.path.join(
                    palsSis.si_instanceBaseDir(
                        self.bpoId,
                        self.siId,
                    ),
                    "tmp",
                )
            )
        )


####+BEGIN: bx:icm:py3:method :methodName "curBasePath_update" :deco "default"
    """
**  _[[elisp:(blee:menu-sel:outline:popupMenu)][±]]_ _[[elisp:(blee:menu-sel:navigation:popupMenu)][Ξ]]_ [[elisp:(bx:orgm:indirectBufOther)][|>]] *[[elisp:(blee:ppmm:org-mode-toggle)][|N]]*  Method-    :: /curBasePath_update/ deco=default  [[elisp:(org-cycle)][| ]]
"""
    @icm.subjectToTracking(fnLoc=True, fnEntry=True, fnExit=True)
    def curBasePath_update(
####+END:
          self,
    ) -> pathlib.Path:

        actualBasePath = pathlib.Path(
            os.path.join(
                "/var/bisos/bpo/cur",
                self.bpoId,
                "bpo",
                self.siId,
            )
        )
        actualBasePath.mkdir(parents=True, exist_ok=True)
        bpoBasePath  = self.curBasePath_obtain()

        return fpath.symlinkUpdate(actualBasePath, bpoBasePath)

####+BEGIN: bx:icm:py3:method :methodName "curBasePath_obtain" :deco "default"
    """
**  _[[elisp:(blee:menu-sel:outline:popupMenu)][±]]_ _[[elisp:(blee:menu-sel:navigation:popupMenu)][Ξ]]_ [[elisp:(bx:orgm:indirectBufOther)][|>]] *[[elisp:(blee:ppmm:org-mode-toggle)][|N]]*  Method-    :: /curBasePath_obtain/ deco=default  [[elisp:(org-cycle)][| ]]
"""
    @icm.subjectToTracking(fnLoc=True, fnEntry=True, fnExit=True)
    def curBasePath_obtain(
####+END:
            self,
    ) -> pathlib.Path:
        return (
            pathlib.Path(
                os.path.join(
                    palsSis.si_instanceBaseDir(
                        self.bpoId,
                        self.siId,
                    ),
                    "cur",
                )
            )
        )


####+BEGIN: bx:dblock:python:section :title "ICM Commands"
"""
*  [[elisp:(beginning-of-buffer)][Top]] ############## [[elisp:(blee:ppmm:org-mode-toggle)][Nat]] [[elisp:(delete-other-windows)][(1)]]    *ICM Commands*  [[elisp:(org-cycle)][| ]]  [[elisp:(org-show-subtree)][|=]]
"""
####+END:

####+BEGIN: bx:icm:python:cmnd:classHead :cmndName "basesUpdate" :parsMand "bpoId" :parsOpt "" :argsMin "0" :argsMax "5" :asFunc "" :interactiveP ""
"""
*  _[[elisp:(blee:menu-sel:outline:popupMenu)][±]]_ _[[elisp:(blee:menu-sel:navigation:popupMenu)][Ξ]]_ [[elisp:(bx:orgm:indirectBufOther)][|>]] *[[elisp:(blee:ppmm:org-mode-toggle)][|N]]*  ICM-Cmnd   :: /basesUpdate/ parsMand=bpoId parsOpt= argsMin=0 argsMax=5 asFunc= interactive=  [[elisp:(org-cycle)][| ]]
"""
class basesUpdate(icm.Cmnd):
    cmndParamsMandatory = [ 'bpoId', ]
    cmndParamsOptional = [ ]
    cmndArgsLen = {'Min': 0, 'Max': 5,}

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

        cmndArgs = list(self.cmndArgsGet("0&5", cmndArgsSpecDict, effectiveArgsList)) # type: ignore

        if len(cmndArgs):
            if  cmndArgs[0] == "all":
                cmndArgsSpec = cmndArgsSpecDict.argPositionFind("0&5")
                argChoices = cmndArgsSpec.argChoicesGet()
                argChoices.pop(0)
                cmndArgs= argChoices

        thisBpo = palsBpo.obtainBpo(bpoId,)

        for each in cmndArgs:
            try:
                baseUpdateMethod = getattr(thisBpo.bases, "{each}BasePath_update".format(each=each))
                palsBpoBase = baseUpdateMethod()
                print(palsBpoBase)
            except AttributeError:
                icm.EH_critical_exception("")
                continue

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
            argPosition="0&5",
            argName="cmndArgs",
            argDefault='all',
            argChoices=['all', 'var', 'tmp', 'log', 'control', 'cur'],
            argDescription="Rest of args for use by action"
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


####+BEGIN: bx:icm:python:cmnd:classHead :cmndName "basesUpdateSivd" :parsMand "bpoId sivd" :parsOpt "" :argsMin "0" :argsMax "5" :asFunc "" :interactiveP ""
"""
*  _[[elisp:(blee:menu-sel:outline:popupMenu)][±]]_ _[[elisp:(blee:menu-sel:navigation:popupMenu)][Ξ]]_ [[elisp:(bx:orgm:indirectBufOther)][|>]] *[[elisp:(blee:ppmm:org-mode-toggle)][|N]]*  ICM-Cmnd   :: /basesUpdateSivd/ parsMand=bpoId sivd parsOpt= argsMin=0 argsMax=5 asFunc= interactive=  [[elisp:(org-cycle)][| ]]
"""
class basesUpdateSivd(icm.Cmnd):
    cmndParamsMandatory = [ 'bpoId', 'sivd', ]
    cmndParamsOptional = [ ]
    cmndArgsLen = {'Min': 0, 'Max': 5,}

    @icm.subjectToTracking(fnLoc=True, fnEntry=True, fnExit=True)
    def cmnd(self,
        interactive=False,        # Can also be called non-interactively
        bpoId=None,         # or Cmnd-Input
        sivd=None,         # or Cmnd-Input
        argsList=[],         # or Args-Input
    ):
        cmndOutcome = self.getOpOutcome()
        if interactive:
            if not self.cmndLineValidate(outcome=cmndOutcome):
                return cmndOutcome
            effectiveArgsList = G.icmRunArgsGet().cmndArgs  # type: ignore
        else:
            effectiveArgsList = argsList

        callParamsDict = {'bpoId': bpoId, 'sivd': sivd, }
        if not icm.cmndCallParamsValidate(callParamsDict, interactive, outcome=cmndOutcome):
            return cmndOutcome
        bpoId = callParamsDict['bpoId']
        sivd = callParamsDict['sivd']

        cmndArgsSpecDict = self.cmndArgsSpec()
        if not self.cmndArgsValidate(effectiveArgsList, cmndArgsSpecDict, outcome=cmndOutcome):
            return cmndOutcome
####+END:

        cmndArgs = list(self.cmndArgsGet("0&5", cmndArgsSpecDict, effectiveArgsList)) # type: ignore

        if len(cmndArgs):
            if  cmndArgs[0] == "all":
                cmndArgsSpec = cmndArgsSpecDict.argPositionFind("0&5")
                argChoices = cmndArgsSpec.argChoicesGet()
                argChoices.pop(0)
                cmndArgs= argChoices

        thisBpo = palsBpo.obtainBpo(bpoId,)

        thisPalsSivdBases = PalsSivdBases(bpoId, thisBpo, sivd)

        for each in cmndArgs:
            try:
                baseUpdateMethod = getattr(thisPalsSivdBases, "{each}BasePath_update".format(each=each))
                palsBpoBase = baseUpdateMethod()
                print(palsBpoBase)
            except AttributeError:
                icm.EH_critical_exception("")
                continue

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
            argPosition="0&5",
            argName="cmndArgs",
            argDefault='all',
            argChoices=['all', 'var', 'tmp', 'log', 'control', 'cur'],
            argDescription="Rest of args for use by action"
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


####+BEGIN: bx:icm:python:cmnd:classHead :cmndName "basesUpdateSi" :parsMand "bpoId si" :parsOpt "" :argsMin "0" :argsMax "5" :asFunc "" :interactiveP ""
"""
*  _[[elisp:(blee:menu-sel:outline:popupMenu)][±]]_ _[[elisp:(blee:menu-sel:navigation:popupMenu)][Ξ]]_ [[elisp:(bx:orgm:indirectBufOther)][|>]] *[[elisp:(blee:ppmm:org-mode-toggle)][|N]]*  ICM-Cmnd   :: /basesUpdateSi/ parsMand=bpoId si parsOpt= argsMin=0 argsMax=5 asFunc= interactive=  [[elisp:(org-cycle)][| ]]
"""
class basesUpdateSi(icm.Cmnd):
    cmndParamsMandatory = [ 'bpoId', 'si', ]
    cmndParamsOptional = [ ]
    cmndArgsLen = {'Min': 0, 'Max': 5,}

    @icm.subjectToTracking(fnLoc=True, fnEntry=True, fnExit=True)
    def cmnd(self,
        interactive=False,        # Can also be called non-interactively
        bpoId=None,         # or Cmnd-Input
        si=None,         # or Cmnd-Input
        argsList=[],         # or Args-Input
    ):
        cmndOutcome = self.getOpOutcome()
        if interactive:
            if not self.cmndLineValidate(outcome=cmndOutcome):
                return cmndOutcome
            effectiveArgsList = G.icmRunArgsGet().cmndArgs  # type: ignore
        else:
            effectiveArgsList = argsList

        callParamsDict = {'bpoId': bpoId, 'si': si, }
        if not icm.cmndCallParamsValidate(callParamsDict, interactive, outcome=cmndOutcome):
            return cmndOutcome
        bpoId = callParamsDict['bpoId']
        si = callParamsDict['si']

        cmndArgsSpecDict = self.cmndArgsSpec()
        if not self.cmndArgsValidate(effectiveArgsList, cmndArgsSpecDict, outcome=cmndOutcome):
            return cmndOutcome
####+END:

        cmndArgs = list(self.cmndArgsGet("0&5", cmndArgsSpecDict, effectiveArgsList)) # type: ignore

        if len(cmndArgs):
            if  cmndArgs[0] == "all":
                cmndArgsSpec = cmndArgsSpecDict.argPositionFind("0&5")
                argChoices = cmndArgsSpec.argChoicesGet()
                argChoices.pop(0)
                cmndArgs= argChoices

        thisBpo = palsBpo.obtainBpo(bpoId,)

        thisPalsSiBases = PalsSiBases(bpoId, thisBpo, si)

        for each in cmndArgs:
            try:
                baseUpdateMethod = getattr(thisPalsSiBases, "{each}BasePath_update".format(each=each))
                palsBpoBase = baseUpdateMethod()
                print(palsBpoBase)
            except AttributeError:
                icm.EH_critical_exception("")
                continue

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
            argPosition="0&5",
            argName="cmndArgs",
            argDefault='all',
            argChoices=['all', 'var', 'tmp', 'log', 'control', 'cur'],
            argDescription="Rest of args for use by action"
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
