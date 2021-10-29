#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Aplicativo para Gerenciar a PNADC.

Rafael Guerreiro Osorio - Ipea
2020-21
"""


import json
import os
import sys
import time
from ftplib import FTP, error_perm
from io import BytesIO, StringIO, TextIOWrapper
from pathlib import Path, PurePosixPath as pPath
from subprocess import run
from zipfile import ZipFile, ZIP_DEFLATED, BadZipFile
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QGuiApplication, QIcon
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, \
                            QMessageBox, QTreeWidgetItem
from tablib import Dataset
from .main_form import Ui_main_window
from .aux_functions import csv_nome, elapsed, sizestr
from .metadata import _metadata_pnadc_anual, _metadata_pnadc_trimestral
from .person import Person
from .ident import __id_birthdate_unknown__, __id_split_grpds__, \
                   __id_cls1__, __id_cls2__, __id_cls3__

APP_PATH = os.path.dirname(os.path.abspath(__file__))

# constantes para os microdados da PNADC
PNADCA = 'anual'
PNADCT = 'trimestral'
FTP_FOLDERS = {PNADCA: ('Trabalho_e_Rendimento',
                        'Pesquisa_Nacional_por_Amostra_de_Domicilios_continua',
                        'Anual', 'Microdados'),
               PNADCT: ('Trabalho_e_Rendimento',
                        'Pesquisa_Nacional_por_Amostra_de_Domicilios_continua',
                        'Trimestral', 'Microdados')}

# pastas especificas no IBGE
TRIDOCS = 'Documentacao'
CA_DOCS = 'Documentacao'
CA_DATA = 'Dados'
CA_VIS = 'Visita'
CA_TRI = 'Trimestre'

# nome para pastas das cópias locais e paineis
ORI = 'originais'
META = 'metadados'
MICRO = 'microdados'
REGPES = 'pessoas'
REGIND = 'individuos'
REGPID = 'chaves'

# chaves dos dicionários de variáveis json
_VPART = 'parte'  # parte do registro: identificação e controle etc.
_VDESC = 'nome'  # nome da variável
_VPER = 'periodo'  # periodo
_VPOS = 'colunas'  # posição no arquivo original
_VSIZE = 'bytes'  # bytes necessários para o tipo de dado
_VCAT = 'valores'  # categorias ou valores
_VQUES = 'quesito'  # número da questão para variáveis do questionário
_MISS = 'vazio'  # chave para "não aplicável" em _VCAT

# constantes para status de arquivos
ATUALIZADO = 'sincronizado'
REMOVER = 'REMOVER'
DOWNLOAD = 'BAIXAR'
UNKNOWN = 'verificar atualizações'
UNLOCAL = 'ignorar arquivo local'
UNREMOTE = 'ignorar arquivo remoto'
UNCHECK = {ATUALIZADO: REMOVER,
           REMOVER: UNLOCAL,
           DOWNLOAD: UNREMOTE,
           UNKNOWN: REMOVER}

# delimitador de arquivos CSV
DELIMITER = ','

# constantes para os nomes de blocos - sections
BASE = 'basico'
EDUC = 'educa'
TRAB = 'trabalho'
OREN = 'rendas'
MORA = 'moradia'
TICS = 'tics'
TURI = 'turismo'
DERI = 'derivadas'
TRIN = 'trabinfa'

# indicador de progresso
PROGRESSO = {'◐': '◓', '◓': '◑', '◑': '◒', '◒': '◐'}


class MainWindow(QMainWindow):
    """A janela principal do app."""

    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_main_window()
        self.ui.setupUi(self)

        # menu
        self.ui.menu_file_new.triggered.connect(self._menu_new)
        self.ui.menu_file_open.triggered.connect(self._menu_open)
        self.ui.menu_file_close.triggered.connect(self._ui_reset)
        self.ui.menu_file_quit.triggered.connect(QGuiApplication.quit)
        self.ui.menu_sync_verify.triggered.connect(self._menu_verify)
        self.ui.menu_sync_update.triggered.connect(self._menu_update)
        self.ui.menu_tools_csv.triggered.connect(self._menu_csv)
        self.ui.menu_tools_panels_new.triggered.connect(self._menu_panel_new)
        self.ui.menu_tools_panels_open.triggered.connect(
            self._menu_panel_update)
        self.ui.menu_help_show.triggered.connect(self._menu_help)

        # treeCopiaLocal
        self.ui.tree.clicked.connect(self._tree_change)
        self.ui.tree.itemDoubleClicked.connect(self._tree_item_exp_children)
        self.ui.tree.itemExpanded.connect(self._tree_item_exp)
        self.ui.tree.itemCollapsed.connect(self._tree_item_exp)

        # atributos
        self.ultatu = None
        self.ultver = None
        self.copialocal = None
        self.remote = []
        self.elementos = []
        self.msgbox = QMessageBox()
        self._ui_reset()

    def _ui_enabled(self, enabled):
        """Suspende ui durante processamento."""
        self.ui.centralwidget.setEnabled(enabled)
        self.ui.menubar.setEnabled(enabled)

    def _ui_reset(self):
        """Retorna app ao estado inicial."""
        self.ultatu = None
        self.ui.menu_file_close.setEnabled(False)
        self.ui.menu_sync.setEnabled(False)
        self.ui.menu_sync_update.setEnabled(False)
        self.ui.menu_tools.setEnabled(False)
        self.ui.menu_tools_csv.setChecked(False)
        self.ui.menu_tools_panels.setEnabled(False)
        self.ui.copia_local_nome.setText('Nenhum arquivo aberto')
        self.ui.copia_local_ultatu.setText('')
        self.ui.tree.clear()
        self.elementos = []
        if self.ultver is None:
            self.ui.tree.setHeaderLabels(['Arquivos originais da Pnadc',
                                          'Status na cópia local'])

    def _ui_show_prgs(self, message):
        """Mostrar progresso no processamento de paineis."""
        message = PROGRESSO[message[0]] + message[1:]
        self.ui.statusbar.showMessage(message)
        QGuiApplication.processEvents()
        return message

    def _tree_build(self):
        """Constrói a árvore a partir da lista de elementos."""

        def add_child(parent, child):
            item = QTreeWidgetItem(parent, [child['text'],
                                            child['status']])
            item.setFlags(item.flags() | Qt.ItemIsUserCheckable
                          | Qt.ItemIsTristate)
            item.setCheckState(0, child['check'])
            item.setData(0, Qt.UserRole, elemento)
            if child['folder']:
                item.setIcon(0, icofld)
                # item.setExpanded(elemento['expanded'])
            else:
                item.setIcon(0, icodoc)
                if child['check'] == 0:
                    item.setText(1, UNCHECK[child['status']])
            return item

        icofld = QIcon(str(Path(APP_PATH, 'folder.svg')))
        icodoc = QIcon(str(Path(APP_PATH, 'file.svg')))
        elementos = self.elementos[:]
        self.ui.tree.clear()
        self.ui.tree.sortItems(0, Qt.AscendingOrder)
        parent = None
        added = {}
        while elementos:
            elemento = elementos.pop(0)
            if elemento['pid'] == -1:
                parent = self.ui.tree
            elif elemento['pid'] not in added:
                elementos.append(elemento)
                continue
            else:
                parent = added[elemento['pid']]
            item = add_child(parent, elemento)
            added[elemento['uid']] = item
            self.elementos[elemento['uid']]['widget'] = item
            item.setData(0, Qt.UserRole, elemento)

    def _tree_change(self, index):
        """Evento mudança."""
        treeitem = self.ui.tree.itemFromIndex(index)
        self._tree_change_handler(treeitem)

    def _tree_change_handler(self, item):
        """Processa mudanças na árvore."""
        def update_children(parentdata, check):
            children = [ele['widget'] for ele in self.elementos
                        if ele['pid'] == parentdata['uid']]
            while children:
                child = children.pop()
                if child.childCount():
                    update_children(child.data(0, Qt.UserRole), check)
                childdata = child.data(0, Qt.UserRole)
                childcheck = check
                if not childdata['folder']:
                    if check == 1:
                        childcheck = child.checkState(0)
                    if childcheck == Qt.Unchecked:
                        child.setText(1, UNCHECK[childdata['status']])
                    else:
                        child.setText(1, childdata['status'])
                self.elementos[childdata['uid']]['check'] = childcheck
                self.elementos[childdata['uid']]['expanded'] = \
                    child.isExpanded()
                child.setData(0, Qt.UserRole,
                              self.elementos[childdata['uid']])

        itemdata = item.data(0, Qt.UserRole)
        if itemdata['folder']:
            update_children(itemdata, item.checkState(0))
        else:
            if item.checkState(0) == Qt.Checked:
                item.setText(1, itemdata['status'])
            else:
                item.setText(1, UNCHECK[itemdata['status']])
            self.elementos[itemdata['uid']]['check'] = item.checkState(0)
            self.elementos[itemdata['uid']]['expanded'] = \
                item.isExpanded()
            item.setData(0, Qt.UserRole, self.elementos[itemdata['uid']])

        # Qt bug: se não alterar algo, não desseleciona 2ndo nivel
        # das checkboxes de parents em tristate
        item.treeWidget().setCurrentItem(None)

    def _tree_data(self, files):
        """Gera lista de elementos para tree a partir de file list."""
        parentid = {'.': -1}
        elementos = []
        uniqueid = 0
        for filerec in files:
            file = filerec[0]
            options = filerec[1]
            parentes = [str(par) for par
                        in pPath(file['parent'], file['name']).parents
                        if str(par) != '.']
            parentes.sort()
            for parente in parentes:
                if parente not in parentid:
                    parentid[parente] = uniqueid
                    parent = str(pPath(parente).parent)
                    elementos.append({'uid': uniqueid,
                                      'pid': parentid[parent],
                                      'folder': True,
                                      'file': file,
                                      'text': Path(parente).parts[-1],
                                      'status': '',
                                      'check': options['check'],
                                      'expanded': options['expanded'],
                                      'widget': None})
                    uniqueid += 1
            elementos.append({'uid': uniqueid,
                              'pid': parentid[str(file['parent'])],
                              'folder': False,
                              'file': file,
                              'text': file['name'],
                              'status': options['status'],
                              'check': options['check'],
                              'expanded': options['expanded'],
                              'widget': None})
            uniqueid += 1
        self.elementos = elementos

    def _tree_item_exp(self, item):
        """Evento expansão de item."""
        idx = self.elementos.index(item.data(0, Qt.UserRole))
        self.elementos[idx]['expanded'] = item.isExpanded()
        item.setData(0, Qt.UserRole, self.elementos[idx])

    def _tree_item_exp_children(self, item):
        """Exibe os subitems de um item."""
        def expand_children(item, expand):
            children = [[ele['widget'], idx] for idx, ele
                        in enumerate(self.elementos)
                        if ele['pid'] == item.data(0, Qt.UserRole)['uid']]
            while children:
                child = children.pop()
                if child[0].childCount():
                    expand_children(child[0], expand)
                    child[0].setExpanded(expand)
                self.elementos[child[1]]['expanded'] = child[0].isExpanded()

        # dblclck ocorre antes da mudança de expanded
        # a definição abaixo gera um comportamento interessante
        # com duplos cliques sucessivos
        expand = not item.isExpanded()
        expand_children(item, expand)

    def _tree_sel_export(self):
        """Gera lista de arquivos com seleção a partir de elementos."""
        arquivos = []
        for elemento in self.elementos[:]:
            if not elemento['folder']:
                arquivos.append(
                    [{'parent': elemento['file']['parent'],
                      'name': elemento['file']['name'],
                      'size': elemento['file']['size']},
                     {'status': elemento['status'],
                      'check': elemento['check'],
                      'expanded': elemento['expanded']}])
        return arquivos

    def _menu_csv(self):
        """Gerar ou excluir arquivos csv."""
        if not self.ui.menu_tools_csv.isChecked():
            with ZipFile(self.copialocal, 'a', ZIP_DEFLATED) as archive:
                drop = [file for file in archive.namelist()
                        if Path(file).parts[0] == MICRO]
            mensagem = ('Excluir os arquivos de microdados'
                        + ' em formato CSV gerados por pynad'
                        + '<br><br>Continuar?')
            if drop:
                resposta = self.msgbox.question(self, 'Confirmar',
                                                mensagem,
                                                QMessageBox.Yes |
                                                QMessageBox.No,
                                                QMessageBox.No)
                if resposta == self.msgbox.No:
                    self.ui.menu_tools_csv.setChecked(
                        not self.ui.menu_tools_csv.isChecked())
                    return
                self._ui_enabled(False)
                self._proc_drop(self.copialocal, drop)
                self.ui.menu_tools_panels.setEnabled(False)
                self._ui_enabled(True)
        else:
            self._ui_enabled(False)
            self._proc_csv()
            self.ui.menu_tools_panels.setEnabled(True)
            self._ui_enabled(True)

    def _menu_help(self):
        """Exibir a ajuda."""
        import webbrowser
        webbrowser.open(str(Path(APP_PATH, 'help.html')))

    def _menu_new(self):
        """Criar um arquivo ZIP para armazenar uma cópia local da Pnadc."""
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        output = QFileDialog.getSaveFileName(self,
                                             'Criar uma cópia local', '',
                                             'Zip Files (*.zip)',
                                             options=options)
        file = output[0]
        if file:
            if not file.endswith('.zip'):
                file += '.zip'
            self.copialocal = file
            with ZipFile(file, 'w', ZIP_DEFLATED) as target:
                target.writestr('pynad.json',
                                json.dumps([None, None, []]))
            self.ui.copia_local_nome.setText(Path(self.copialocal).name)
            ultima = ('Última atualização: <b>nenhuma</b>')
            self.ui.copia_local_ultatu.setText(ultima)
            self.ui.menu_file_close.setEnabled(True)
            self.ui.menu_sync.setEnabled(True)
            self.ui.menu_sync_verify.setEnabled(True)
            if self.remote:
                self._tree_data(self.remote)
                self._tree_build()
                self.ui.menu_sync_update.setEnabled(True)
            else:
                self._menu_verify()

    def _menu_open(self):
        """Escolher um arquivo ZIP criado por pynad."""
        def valid():
            # Verifica se arquivo zip é uma cópia local válida
            try:
                with ZipFile(self.copialocal) as source:
                    pynadjson = json.loads(source.read('pynad.json'))
                    if isinstance(pynadjson, list) and len(pynadjson) == 3:
                        result = True
                    else:
                        result = False
            except (KeyError, IndexError, BadZipFile):
                result = None
            return result

        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        output = QFileDialog.getOpenFileName(self,
                                             'Abrir uma cópia local', '',
                                             'Zip Files (*.zip)',
                                             options=options)
        if output[0]:
            self.copialocal = output[0]
            if not valid():
                mensagem = f'{output[0]}<br><br>Não é uma cópia local válida'
                self.msgbox.warning(self, 'Arquivo inválido', mensagem)
                self.copialocal = None
                return
            self.ui.menu_sync.setEnabled(True)
            self.ui.menu_sync_verify.setEnabled(True)
            self._proc_copialocal()

    def _menu_panel_new(self):
        """Criar um novo arquivo e gerar painéis."""
        paineis = self._panels_available()
        if paineis:
            options = QFileDialog.Options()
            options |= QFileDialog.DontUseNativeDialog
            output = QFileDialog.getSaveFileName(self,
                                                 'Criar um arquivo para'
                                                 + ' armazenar paineis', '',
                                                 'Zip Files (*.zip)',
                                                 options=options)
            file = output[0]
            if file:
                if file == self.copialocal:
                    return
                panlist = [str(painel) for painel in paineis]
                mensagem = ('A cópia local da Pnadc contém os paineis:<br>'
                            + f'<b>{", ".join(panlist)}</b>'
                            + '<br><br>O processamento dos painéis'
                            + ' é lento e exige 16GB de memória RAM.'
                            + '<br><br>Continuar?')
                resposta = self.msgbox.question(self, 'Confirmar',
                                                mensagem,
                                                QMessageBox.Yes |
                                                QMessageBox.No,
                                                QMessageBox.No)
                if resposta == self.msgbox.No:
                    return
                if not file.endswith('.zip'):
                    file += '.zip'
                with ZipFile(file, 'w', ZIP_DEFLATED) as target:
                    target.writestr('pynad.json',
                                    json.dumps(
                                        'Paineis da Pnadc criados por pynad'))
                self._proc_panels(paineis, file)

    def _menu_panel_update(self):
        paineis = self._panels_available()
        if paineis:
            options = QFileDialog.Options()
            options |= QFileDialog.DontUseNativeDialog
            output = QFileDialog.getOpenFileName(self,
                                                 'Abrir um arquivo ZIP com'
                                                 + ' painéis da Pnadc', '',
                                                 'Zip Files (*.zip)',
                                                 options=options)
            file = output[0]
            if not file:
                return
            valid = True
            with ZipFile(file) as src:
                files = src.namelist()
                try:
                    content = json.loads(src.read('pynad.json'))
                    if content != 'Paineis da Pnadc criados por pynad':
                        valid = False
                except KeyError:
                    valid = False
            if not valid:
                self.msgbox.warning(
                    self, 'Arquivo inválido',
                    f'{file}<br><br>Não é um arquivo de painéis')
                return
        else:
            return
        paineis = json.loads(json.dumps(paineis))
        with ZipFile(file) as src:
            atuais = json.loads(
                src.read(f'{REGPES}/microdados.pnadc.paineis.json'))

        # paineis que não estão disponíveis na copia local
        # serão removidos
        remover = [painel for painel in atuais if painel not in paineis]
        atualizar = []
        for painel in paineis:
            if painel in atuais:

                # painel existe, mas precisa de atualização
                # por mudança no conjunto de arquivos fonte
                if atuais[painel] != paineis[painel]:
                    remover.append(painel)
                    atualizar.append(painel)

            # o painel não existe e precisa ser criado
            else:
                atualizar.append(painel)
        if not remover and not atualizar:
            self.ui.statusbar.showMessage('Arquivo de painéis atualizado')
            return
        atualizados = [painel for painel in atuais
                       if painel not in remover and painel not in atualizar]
        # confirmar atualização
        rem, atu, ign = '', '', ''
        if remover:
            rem = ('<br><br>Painéis para remover:<br><b>'
                   + f'{", ".join(remover)}</b>')
        if atualizar:
            atu = ('<br><br>Painéis para gerar:<br>'
                   + f'<b>{", ".join(atualizar)}</b>')
        if atualizados:
            ign = ('<br><br>Painéis atualizados:<br>'
                   + f'<b>{", ".join(atualizados)}</b>')
        mensagem = ('<b>O arquivo com painéis da Pnadc está desatualizado.</b>'
                    + rem + atu + ign
                    + '<br><br>O processamento dos painéis'
                    + ' é lento e exige 16GB de memória RAM.'
                    + '<br><br>Continuar?')
        resposta = self.msgbox.question(self, 'Confirmar',
                                        mensagem,
                                        QMessageBox.Yes |
                                        QMessageBox.No,
                                        QMessageBox.No)
        if resposta == self.msgbox.No:
            return

        drop = []
        if remover:
            drop = [file for file in files for key in remover
                    if key in file]
        if atualizar:
            drop.extend([file for file in files
                         if 'microdados.pnadc.paineis.json' in file])

        # remove e atualiza
        self._proc_drop(file, drop)
        if atualizar:
            self._proc_panels({int(painel): paineis[painel]
                               for painel in atualizar},
                              file, paineis)

    def _menu_update(self):
        """Sincroniza a cópia local."""
        # primeiro, verificar se há updates - de acordo com as seleções
        curfiles = [ele for ele in self.elementos
                    if not ele['folder']]
        actions = {}
        for file in curfiles:
            status = file['status']
            if not file['check']:
                status = UNCHECK[status]
            if status not in actions:
                actions[status] = [0, 0, []]
            actions[status][0] += 1
            actions[status][1] += file['file']['size']
            actions[status][2].append(str(pPath('originais',
                                                file['file']['parent'],
                                                file['file']['name'])))
        atualtxt = ''
        ignortxt = ''
        removtxt = ''
        downltxt = ''
        if ATUALIZADO in actions:
            atualtxt += f'{actions[ATUALIZADO][0]:4.0f} arquivos atualizados'
            atualtxt += f' - {sizestr(actions[ATUALIZADO][1])}<br>'
        if UNLOCAL in actions:
            ignortxt += f'{actions[UNLOCAL][0]:4.0f} arquivos locais ignorados'
            ignortxt += f' - {sizestr(actions[UNLOCAL][1])}<br>'
        if UNREMOTE in actions:
            ignortxt += f'{actions[UNREMOTE][0]:4.0f} arquivos'
            ignortxt += ' remotos ignorados'
            ignortxt += f' - {sizestr(actions[UNREMOTE][1])}<br>'
        if REMOVER in actions:
            removtxt += f'<b>{REMOVER:>7}</b> {actions[REMOVER][0]:4.0f}'
            removtxt += f' arquivos - {sizestr(actions[REMOVER][1])}<br>'
        if DOWNLOAD in actions:
            downltxt += f'<b>{DOWNLOAD:>7}</b> {actions[DOWNLOAD][0]:4.0f}'
            downltxt += f' arquivos - {sizestr(actions[DOWNLOAD][1])}<br>'
        if not any(status in actions for status in (REMOVER, DOWNLOAD)):
            mensagem = f'{atualtxt}{ignortxt}<br>'
            mensagem += 'Sem arquivos para baixar ou remover'
            self.msgbox.warning(self, 'Nada a atualizar', mensagem)
        else:
            mensagem = f'{atualtxt}{ignortxt}<br>'
            mensagem += '<u><b>Atualizações:</b></u><br><br>'
            mensagem += removtxt + downltxt
            resposta = self.msgbox.question(self, 'Confirmar atualizações',
                                            mensagem,
                                            QMessageBox.Yes |
                                            QMessageBox.No,
                                            QMessageBox.No)
            if resposta == self.msgbox.No:
                self._ui_enabled(True)
                return

            # UPDATES
            self._ui_enabled(False)

            # remover arquivos e apagar pynad.json e metadados
            with ZipFile(self.copialocal) as archive:
                files = archive.namelist()
            metafiles = [file for file in files if META in Path(file).parts[0]]
            metafiles.append('pynad.json')
            if not removtxt:
                actions[REMOVER] = [0, 0, metafiles]
            else:
                actions[REMOVER][2].extend(metafiles)
            self._proc_drop(self.copialocal, actions[REMOVER][2])

            # baixar arquivos
            if downltxt:
                self._proc_downloads(actions[DOWNLOAD])

            # atualizar o status dos arquivos
            locais = self._list_local_files()
            arvore = self._tree_sel_export()
            finais = []
            for item in arvore:
                for file in locais:
                    if file[0] == item[0]:

                        # existe em remote e em locais - atualizado
                        if any(file[0] == rem[0] for rem in self.remote):
                            item[1]['status'] = ATUALIZADO
                        else:

                            # existe em locais mas não em remote - remover
                            item[1]['status'] = REMOVER

                # existe em locais ou em remote - entra
                if (any(item[0] == file[0] for file in locais)
                        or any(item[0] == rem[0] for rem in self.remote)):
                    item[0]['parent'] = str(item[0]['parent'])
                    finais.append(item)

            # escrever novo pynad.json
            with ZipFile(self.copialocal, 'a', ZIP_DEFLATED) as target:
                target.writestr('pynad.json',
                                json.dumps([time.time(), self.ultver,
                                            finais]))
            self._proc_copialocal()
            self._proc_metadata()
            if self.ui.menu_tools_csv.isChecked():
                self._proc_csv()
            self._ui_enabled(True)

    def _menu_verify(self):
        """Verifica os arquivos remotos no servidor do IBGE."""
        if self.ultver:
            mensagem = ('Mapear os arquivos da Pnadc em '
                        + '<b>ftp.ibge.gov.br</b> pode demorar alguns minutos'
                        '<br><br>Evite verificações desnecessárias'
                        + f'<br><br><b>{elapsed(self.ultver)}</b> desde a'
                        + ' última verificação<br><br>Verificar agora?')
        else:
            mensagem = ('Mapear os arquivos da Pnadc em '
                        + '<b>ftp.ibge.gov.br</b> pode demorar alguns minutos'
                        + '<br><br>Verificar agora?')

        resposta = self.msgbox.question(self, 'Confirmar',
                                        mensagem,
                                        QMessageBox.Yes |
                                        QMessageBox.No,
                                        QMessageBox.No)
        if resposta == self.msgbox.No:
            return
        self._ui_enabled(False)
        self._list_remote_files()
        self._ui_enabled(True)
        if self.remote:
            self.ultver = time.time()
            dtu = time.localtime(self.ultver)
            self.ui.tree.setHeaderLabels(['Arquivos originais da Pnadc em '
                                          + f'{dtu.tm_mday:02.0f}/'
                                          + f'{dtu.tm_mon:02.0f}/'
                                          + f'{dtu.tm_year}',
                                          'Status na cópia local'])
        else:
            self.msgbox.warning(self, 'Erro de conexão',
                                'Não foi possível mapear '
                                + '<b>ftp.ibge.gov.br</b><br><br>'
                                + 'Verifique se há conexão à internet e se o'
                                + ' servidor do IBGE está respondendo')
            return
        self._proc_copialocal()
        self._menu_update()

    def _proc_copialocal(self):
        """Exibe o conteúdo da copia local e ajusta ui."""
        source = ZipFile(self.copialocal)
        self._ui_reset()
        self.ui.menu_sync.setEnabled(True)
        self.ui.menu_file_close.setEnabled(True)
        self.ui.menu_tools.setEnabled(True)
        if any(MICRO in Path(file).parts[0] for file in source.namelist()):
            self.ui.menu_tools_csv.setChecked(True)
            self.ui.menu_tools_panels.setEnabled(True)
        self.ui.copia_local_nome.setText(Path(self.copialocal).name)

        # carrega pynad.json
        pynadfile = BytesIO()
        pynadfile.write(source.read('pynad.json'))
        pynadinfo = TextIOWrapper(pynadfile, encoding='utf-8')
        pynadinfo.seek(0)
        info = json.loads(pynadinfo.read())

        # json é incompatível com Path, caminho foi guardado como string
        for item in info[2]:
            item[0]['parent'] = pPath(item[0]['parent'])

        # 1o elemento de info é a data da atualização do arquivo
        self.ultatu = info[0]
        if self.ultatu:
            dtu = time.localtime(self.ultatu)
            ultima = ('Última atualização:'
                      + f' <b>{dtu.tm_mday:02.0f}/'
                      + f'{dtu.tm_mon:02.0f}/'
                      + f'{dtu.tm_year}</b>')
        else:
            ultima = ('Última atualização: <b>nenhuma</b>')
        self.ui.copia_local_ultatu.setText(ultima)

        # 2o elemento é a data da última verificação que corresponde
        # à atualização, mas só carrega se não houver verificação atual
        # a verificação realizada na seção prepondera sobre a da última
        # atualização - mas podem ter arquivos abertos diferentes, aí
        # fica o mapa mais novo
        if self.ultver is None or (info[1] is not None
                                   and self.ultver < info[1]):
            self.ultver = info[1]

        # ainda pode ser None - arquivos novos sem verificação/atualização
        if self.ultver:
            dtu = time.localtime(self.ultver)
            self.ui.tree.setHeaderLabels(['Arquivos originais da Pnadc em '
                                          + f'{dtu.tm_mday:02.0f}/'
                                          + f'{dtu.tm_mon:02.0f}/'
                                          + f'{dtu.tm_year}',
                                          'Status na cópia local'])
            self.ui.menu_sync_update.setEnabled(True)

        # construir a lista de arquivos
        info[2].extend([remote for remote in self.remote
                        if all(remote[0] != file[0] for file in info[2])])

        # marcar arquivos obsoletos
        for file in info[2]:
            if self.remote and all(file[0] != rem[0] for rem in self.remote):
                file[1]['status'] = REMOVER

        # construir a árvore de arquivos
        self._tree_data(info[2])
        self._tree_build()

    def _proc_csv(self):
        """
        Gera os arquivos de microdados em formato CSV.

        para funcionar, precisa ter o microdado e o respectivo dicionário
        na cópia local

        _csv_nome depende das características da distribuição de dados
        do IBGE - nomenclatura de arquivos de microdados
        """
        statusbar = self.ui.statusbar
        archive = ZipFile(self.copialocal, 'a', ZIP_DEFLATED)

        # carrega metadados dos arquivos de microdados.json
        metafiles = ('microdados.pnadc.trimestral.json',
                     'microdados.pnadc.anual.json')
        metas = {}
        dados = {}
        for metafile in metafiles:
            if str(pPath(META, metafile)) in archive.namelist():
                metas[metafile] = json.loads(
                    archive.read(str(pPath(META, metafile))))
            if str(pPath(MICRO, metafile)) in archive.namelist():
                dados[metafile] = json.loads(
                    archive.read(str(pPath(MICRO, metafile))))

        if not metas and not dados:
            return

        if metas == dados:
            self._ui_enabled(True)
            statusbar.showMessage('Microdados em csv atualizados')
            return

        # arquivos de microdados que não correspondem aos metadados
        # são removidos (mudança de nome do arquivo ou dicionario)
        drop = []
        if dados:
            for metafile in dados:
                if metafile not in metas:
                    drop.extend([str(pPath(MICRO, csv_nome(Path(item[0]).name,
                                                           item[3])))
                                for item in dados[metafile]])
                else:
                    drop.extend([str(pPath(MICRO, csv_nome(Path(item[0]).name,
                                                           item[3])))
                                 for item in dados[metafile]
                                 if item not in metas[metafile]])

        # arquivos de registro são sempre atualizados
        drop.extend([str(pPath(MICRO, dado)) for dado in dados
                     if str(pPath(MICRO, dado)) in archive.namelist()])
        archive.close()

        # atualizações dos microdados - remoções e novos
        self._proc_drop(self.copialocal, drop)
        archive = ZipFile(self.copialocal, 'a', ZIP_DEFLATED)

        for metafile in metas:
            archive.writestr(str(pPath(MICRO, metafile)),
                             archive.read(str(pPath(META, metafile))))
            for microdado in metas[metafile]:
                nome = csv_nome(Path(microdado[0]).name, microdado[3])
                if str(pPath(MICRO, nome)) not in archive.namelist():
                    QGuiApplication.processEvents()
                    self._proc_csv_conv(nome, microdado, archive)
        archive.close()
        statusbar.showMessage('Microdados em csv atualizados')

    def _proc_csv_conv(self, nome, microdado, archive):
        """
        Faz a conversão do arquivo.

        dicvars = ((*var*, *start*, *stop*), ...), onde:
         - **var** variable code - nome das variáveis na primeira linha
         - **start** coluna inicial - começando em 0
         - **stop** coluna depois da final

        O conteúdo dos campos é integralmente preservado,
        exceto os campos em branco ou com . que são transformados
        em strings vazias ''
        """
        # primeiro lê o arquivo json com os metadados
        # para um arquivo na memoria e cria o dicionario
        # para conversão
        original = BytesIO()
        original.write(archive.read(microdado[2]))
        metadata = TextIOWrapper(original, encoding='utf-8')
        metadata.seek(0)
        meta = json.loads(metadata.read())
        dicvars = [(var,
                    meta[var][_VPOS][0] - 1,
                    meta[var][_VPOS][1]) for var in meta]

        # extrair o arquivo zip com os microdados para um
        # arquivo na memória
        message = self._ui_show_prgs('◒ Descompactando '
                                     + f'{Path(microdado[0]).name}'
                                     + ' - aguarde...')
        with ZipFile(BytesIO(archive.read(microdado[0]))) as src:
            original = BytesIO()
            original.write(src.read(src.namelist()[0]))

        # arquivo csv na memória
        tgt = StringIO()
        tgt.write(DELIMITER.join([var[0] for var in dicvars]) + '\n')
        fixwidth = TextIOWrapper(original, encoding='utf-8')
        size = fixwidth.tell()
        fixwidth.seek(0)
        message = self._ui_show_prgs(f'{message[0]} Gerando {nome} (0%)')
        report = 1
        read = 0
        for reg in fixwidth:
            csvreg = DELIMITER.join([reg[var[1]:var[2]].strip(' .')
                                     for var in dicvars])
            tgt.write(csvreg + '\n')
            read += len(reg)
            if (read / size) * 100 >= report:
                message = self._ui_show_prgs(f'{message[0]}'
                                             + f' Gerando {nome} ({report}%)')
                QGuiApplication.processEvents()
                report += 1

        # acrescentar arquivo csv à cópia local (archive)
        message = self._ui_show_prgs(f'{message[0]} Compactando {nome}'
                                     + ' - aguarde...')
        tgt.seek(0)
        archive.writestr(str(pPath(MICRO, nome)), tgt.read())

    def _proc_downloads(self, downloads):
        """Baixa arquivos de ftp.ibge.gov.br."""
        server = altFTP('ftp.ibge.gov.br', timeout=120)
        server.connect()
        server.login()
        with ZipFile(self.copialocal, 'a', ZIP_DEFLATED) as archive:
            file = 0
            size = 0
            message = '◐'
            for download in downloads[2]:
                pnad = Path(download).parts[1]
                remotefile = pPath(*FTP_FOLDERS[pnad],
                                   *Path(download).parts[2:])

                file += 1
                message = (f'{message[0]} Baixando {sizestr(downloads[1])} '
                           + f'({size / downloads[1] * 100:.0f}%) - '
                           + f' arquivo {file} de {downloads[0]} -'
                           + f' {Path(download).name}')
                message = self._ui_show_prgs(message)
                with archive.open(download, 'w') as target:
                    server.retrbinary(f'RETR {remotefile}', target.write)
                size += [file.file_size for file in archive.infolist()
                         if file.filename == download][0]

    def _proc_drop(self, archive, delete):
        """Deleta arquivos de um container zip."""
        def with_zipfile():
            os.rename(archive, archive + '.old')
            with ZipFile(archive + '.old') as src:
                with ZipFile(archive, 'w', ZIP_DEFLATED) as tgt:
                    filelist = [file for file in src.namelist()
                                if file not in delete]
                    msg = '◒'
                    for idx, file in enumerate(filelist):
                        tgt.writestr(file, src.read(file))
                        msg = self._ui_show_prgs(
                            f'{msg[0]} Removendo arquivos da cópia local ('
                            + f'{idx / len(filelist) * 100:3.0f}%)'
                            + f'  {elapsed(start)}')
            os.remove(archive + '.old')

        if not delete:
            return
        start = time.time()
        self._ui_show_prgs('◒ Removendo arquivos da cópia local'
                           + ' - aguarde...')

        # tenta usar 7zip command line (mais rápido)
        if os.name == 'posix':
            u7z = '7za'
        else:
            u7z = '7z'
        try:
            run((u7z, 'd', archive, *delete),
                capture_output=True, check=True)
        except FileNotFoundError:
            try:

                # tenta usar zip command line
                run(('zip', '-d', archive, *delete),
                    capture_output=True, check=True)
            except FileNotFoundError:

                # método lento com python standard library
                with_zipfile()
        self.ui.statusbar.showMessage('Arquivos removidos')

    def _proc_metadata(self):
        """
        Extrai e organiza os metadados.

        Os metadados são gerados com as atualizações

        O conteúdo é restrito ao necessário para ler os arquivos de microdados
        e rotular as variáveis
        e suas categorias - não inclui
        deflatores, códigos de ocupação, documentos de metodologia etc.

        só gera metadados para arquivos de microdados existentes, se
        houver um dicionário que não corresponda a um arquivo de microdados
        não será considerado
        """
        self.ui.statusbar.showMessage('Atualizando metadados...')

        # verificar os dados originais no mirrorfile
        # pode ter qualquer combo de PNADCT e PNADCA
        metadados = {}
        metadados[PNADCA] = _metadata_pnadc_anual(self.copialocal)
        metadados[PNADCT] = _metadata_pnadc_trimestral(self.copialocal)
        archive = ZipFile(self.copialocal, 'a', ZIP_DEFLATED)
        for pnad in metadados:
            if pnad == PNADCA and metadados[PNADCA]:
                processados = []
                for item in metadados[pnad]:
                    target = str(pPath(META, Path(item[1]).name))
                    if item[1] not in processados:
                        processados.append(item[1])
                        archive.writestr(target, archive.read(item[1]))
                    item[1] = target
                    if item[2][0] not in processados:
                        processados.append(item[2][0])
                        archive.writestr(item[2][0], json.dumps(item[2][1]))
                    item[2] = item[2][0]
                target = str(pPath(META, 'microdados.pnadc.anual.json'))
                archive.writestr(target, json.dumps(metadados[pnad]))
            if pnad == PNADCT and metadados[PNADCT]:
                item = metadados[pnad][0]
                archive.writestr(str(pPath(META, item[1])), item[2][2].read())
                archive.writestr(item[2][0], json.dumps(item[2][1]))
                for item in metadados[pnad]:
                    item[2] = item[2][0]
                target = str(pPath(META, 'microdados.pnadc.trimestral.json'))
                archive.writestr(target, json.dumps(metadados[pnad]))
        archive.close()
        self.ui.statusbar.showMessage('')

    def _proc_panels(self, paineis, file, microdados=None):
        """Processa os painéis de acordo com a seleção."""
        self._ui_enabled(False)

        # monta paineis de domicilios e pessoas
        self._panels_dwelling(paineis, file, microdados)

        # identifica os indivíduos
        self._panels_id(paineis, file)

        # monta bases de individuos
        self._panels_individuals(paineis, file)
        self.ui.statusbar.showMessage(f'{len(paineis.keys())} '
                                      + 'painéis processados')
        self._ui_enabled(True)

    def _list_local_files(self, root='originais'):
        """
        Lista arquivos na copia local.

        Para cada arquivo há um dicionário com 3 entradas:
            - 'parent', 'name' e 'size'
        """
        with ZipFile(self.copialocal) as source:
            filelist = source.infolist()
        arquivos = []
        for fileinfo in filelist:
            partes = Path(fileinfo.filename).parts
            if root == partes[0]:
                arquivos.append(
                    [{'parent': pPath(*partes[1:-1]),
                      'name': partes[-1],
                      'size': fileinfo.file_size}])
        return arquivos

    def _list_remote_files(self):
        """
        Lista arquivos de microdados da Pnadc no servidor FTP do IBGE.

        Para cada arquivo há um dicionário com 3 entradas:
            - 'parent', 'name' e 'size'
        """

        def isfolder(path):
            try:
                server.cwd(path)
                server.cwd('..')
                return True
            except error_perm:
                return False

        def mapftp(pnad, ftproot, ftpcur, msg):
            server.cwd(str(pPath(ftproot, ftpcur)))
            itens = server.nlst()
            for item in itens:
                sourcename = pPath(ftproot, ftpcur, item)
                if isfolder(str(sourcename)):
                    mapftp(pnad, ftproot, pPath(ftpcur, item), msg)
                else:
                    msg = self._ui_show_prgs(
                        msg[0] + stub
                        + f'{len(remotefiles)} arq'
                        + f'uivos em {elapsed(start)}')
                    QGuiApplication.processEvents()
                    remotefiles.append([{'parent': pPath(pnad, ftpcur),
                                         'name': item,
                                         'size': server.size(str(sourcename))},
                                        {'status': DOWNLOAD,
                                         'check': Qt.Checked,
                                         'expanded': False}])
        try:
            start = time.time()
            stub = '  Verificando arquivos da Pnadc em ftp.ibge.gov.br: '
            message = self._ui_show_prgs('◒' + stub)
            remotefiles = []

            # até 2 minutos sem responder
            server = altFTP('ftp.ibge.gov.br', timeout=120)
            server.connect()
            server.login()
            mapftp(PNADCA, pPath('/', *FTP_FOLDERS[PNADCA]), pPath(''),
                   message)
            mapftp(PNADCT, pPath('/', *FTP_FOLDERS[PNADCT]), pPath(''),
                   message)
            server.close()
        except Exception:
            remotefiles = []
        self.remote = remotefiles
        self.ui.statusbar.showMessage('')

    def _panels_available(self):
        """
        Analisa os painéis contidos na cópia local.

        Um painel exige ao menos os microdados de 5 trimestres
        Para os últimos 4 trimestres não há paineis completos
        """
        # 1) quais são os painéis contidos na cópia local
        microdados = {}
        with ZipFile(self.copialocal) as archive:
            try:
                microdados[PNADCT] = json.loads(archive.read(
                    f'{MICRO}/microdados.pnadc.trimestral.json'))
            except KeyError:
                pass
            try:
                microdados[PNADCA] = json.loads(archive.read(
                    f'{MICRO}/microdados.pnadc.anual.json'))
            except KeyError:
                pass

        # para criar paineis precisa ter a pnadc trimestral
        if PNADCT not in microdados:
            self.ui.statusbar.showMessage('Não há painéis na cópia local')
            return False

        # 2) quais são os arquivos anuais e trimestrais de cada painel
        panels = {}

        # Os microdados trimestrais estão ordenados, então é
        # impossível os 4 últimos serem início de painel
        for idx, microdado in enumerate(microdados[PNADCT][:-4]):
            ano = int(Path(microdado[0]).name.split('_')[1][2:6])
            tri = int(Path(microdado[0]).name.split('_')[1][:2])
            pid = ano * 10 + tri

            # verificar continuidade dos microdados trimestrais
            continuidade = True
            for seq in range(1, 5):
                proximo = microdados[PNADCT][idx + seq]
                anoprox = int(Path(proximo[0]).name.split('_')[1][2:6])
                triprox = int(Path(proximo[0]).name.split('_')[1][:2])
                if tri + seq <= 4:
                    if triprox != tri + seq or ano != anoprox:
                        continuidade = False
                        break
                else:
                    if triprox != (tri + seq - 4) or anoprox != (ano + 1):
                        continuidade = False
                        break

            if continuidade:
                panels[pid] = [[item[0] for item
                                in microdados[PNADCT][idx:idx + 5]]]
                if PNADCA in microdados:
                    anuais = []
                    for seq in range(5):
                        if tri > 4:
                            tri = 1
                            ano += 1
                        anuais.append((str(ano), f'trimestre{tri}'))
                        anuais.append((str(ano), f'visita{seq + 1}'))
                        tri += 1
                    panels[pid].append([microdado[0] for microdado
                                        in microdados[PNADCA]
                                        if any(f'_{anual[0]}_'
                                               in microdado[0] and
                                               anual[1] in microdado[0]
                                               for anual in anuais)])
                else:
                    panels[pid].append([])
        return panels

    def _panels_dwelling(self, panels, archive, microdados=None):
        """Monta os painéis de domicílios."""
        def organise(joinfiles):
            alphaheader = ['ano', 'trimestre', 'uf', 'capital', 'rm_ride',
                           'estrato', 'posest', 'upa']
            headers = {}
            for visita in joinfiles:
                for file in visita:
                    with ZipFile(self.copialocal) as src:
                        file[1].write(src.read(f'{MICRO}/{file[0]}'))
                    file[1] = TextIOWrapper(file[1], encoding='utf-8')
                    file[1].seek(0)
                    headers[file[0]] = \
                        file[1].readline().strip('\n').split(DELIMITER)
            ordenar = [[], []]
            for header in headers:
                for var in headers[header]:
                    if (var not in alphaheader
                        and var not in ordenar[0]
                            and var[0] == 'v'):
                        ordenar[0].append(var)
                    if (var not in alphaheader
                        and var not in ordenar[1]
                            and var[0] == 's'):
                        ordenar[1].append(var)
            ordenar[0].sort()
            ordenar[1].sort()
            newheader = alphaheader + ordenar[0] + ordenar[1]
            return newheader

        def append(joinfiles, newheader, msg):
            data = {}
            keys = ['upa', 'v1008', 'v2003']
            for visita, bases in enumerate(joinfiles):
                msg = self._ui_show_prgs(msg)
                bases[0][1].seek(0)
                header = bases[0][1].readline()
                header = header.replace('\n', '').split(DELIMITER)
                poskeys = [header.index(var) for var in keys]
                posvars = [header.index(var) if var in header else -1
                           for var in newheader]
                count = 0
                for reg in bases[0][1]:
                    reg = reg.replace('\n', '').split(DELIMITER)
                    key = tuple([int(reg[pos]) for pos in poskeys] + [visita])
                    if reg[header.index('v1016')] == str(visita + 1):
                        data[key] = [reg[pos] if pos > -1 else ''
                                     for pos in posvars]
                    count += 1
                    if count == 10000:
                        count = 0
                        msg = self._ui_show_prgs(msg)
                if len(bases) == 2:
                    bases[1][1].seek(0)
                    header = bases[1][1].readline()
                    header = header.replace('\n', '').split(DELIMITER)
                    poskeys = [header.index(var) for var in keys]
                    posvars = [header.index(var) if var in header else -1
                               for var in newheader]
                    count = 0
                    for reg in bases[1][1]:
                        reg = reg.replace('\n', '').split(DELIMITER)
                        key = tuple([int(reg[pos]) for pos in poskeys]
                                    + [visita])
                        xtr = [reg[pos] if pos > -1 else '' for pos in posvars]
                        if key in data:
                            fin = []
                            for idx, _unu in enumerate(xtr):
                                if data[key][idx] == '' and xtr[idx] == '':
                                    fin.append('')
                                elif data[key][idx] != '':
                                    fin.append(data[key][idx])
                                elif xtr[idx] != '':
                                    fin.append(xtr[idx])
                            data[key] = fin
                        count += 1
                        if count == 10000:
                            count = 0
                            msg = self._ui_show_prgs(msg)
            return data

        message = '◑'
        for idx, panel in enumerate(panels):
            message = (message[0] + ' Montando painel de domicilios'
                       + f' {panel} ({idx + 1} de {len(panels)})')
            message = self._ui_show_prgs(message)
            tri = int(str(panel)[-1]) - 1
            ano = panel // 10
            joinfiles = []
            for vis in range(0, 5):
                tri += 1
                if tri > 4:
                    tri = 1
                    ano = ano + 1
                trimestre = [file for file in panels[panel][1]
                             if f'trimestre{tri}' in file
                             and str(ano) == Path(file).name.split('_')[1]]
                if trimestre:
                    joinfiles.append([[csv_nome(Path(trimestre[0]).name,
                                                PNADCA), BytesIO()]])
                else:
                    joinfiles.append([[csv_nome(
                        Path(panels[panel][0][vis]).name,
                        PNADCT), BytesIO()]])
                visita = [file for file in panels[panel][1]
                          if f'visita{vis + 1}' in file]
                if visita:
                    joinfiles[-1].append([csv_nome(Path(visita[0]).name,
                                                   PNADCA), BytesIO()])
            newheader = organise(joinfiles)
            message = self._ui_show_prgs(message)
            joined = append(joinfiles, newheader, message)
            tgt = StringIO()
            tgt.write(DELIMITER.join(newheader) + '\n')
            message = self._ui_show_prgs(self.ui.statusbar.currentMessage())
            cnt = 0
            for reg in joined.values():
                tgt.write(DELIMITER.join(reg) + '\n')
                cnt += 1
                if cnt == 10000:
                    cnt = 0
                    message = self._ui_show_prgs(message)
            tgt.seek(0)
            with ZipFile(archive, 'a', ZIP_DEFLATED) as arc:
                arc.writestr(f'{REGPES}/microdados.pnadc.paineis.{panel}.csv',
                             tgt.read())
            del joinfiles

        if microdados is None:
            microdados = panels
        with ZipFile(archive, 'a', ZIP_DEFLATED) as arc:
            arc.writestr(f'{REGPES}/microdados.pnadc.paineis.json',
                         json.dumps(microdados))

    def _panels_id(self, panels, archive):
        """Identifica os painéis."""

        def load_panel(panelfile, msg):

            def csv2person(record):
                pessoa = []
                for attrib in attribs.values():
                    pessoa.append(int(record[attrib[1]]))
                return tuple(pessoa)

            def load_panel_metadata(header):
                # atributos e variáveis correspondentes
                attribs = {'ano': ['ano'],
                           'tri': ['trimestre'],
                           'upa': ['upa'],
                           'dom': ['v1008'],
                           'paibge': ['v1014'],
                           'ent': ['v1016'],
                           'tam': ['v2001'],
                           'ord': ['v2003'],
                           'std': ['v2005'],
                           'sex': ['v2007'],
                           'dtd': ['v2008'],
                           'dtm': ['v20081'],
                           'dta': ['v20082'],
                           'age': ['v2009']}

                # acha a posição de cada atributo e obtém as descrições
                # dos códigos de sexo e situação no domicílio
                # tem que ler o header, a ordem das variáveis
                # é diferente
                for attrib in attribs.values():
                    attrib.append(header.index(attrib[0]))
                categs = {'stdcat': dicionario['v2005']['valores'],
                          'sexcat': dicionario['v2007']['valores']}
                return attribs, categs

            painel = {}
            pdef = True
            file = TextIOWrapper(BytesIO(target.read(panelfile)),
                                 encoding='utf-8')
            file.seek(0)
            header = file.readline()
            header = header.replace('\n', '').split(DELIMITER)

            # variáveis usadas na identificação e categorias de sexo e sitdom
            attribs, categs = load_panel_metadata(header)
            count = 0
            for line in file:

                # cada registro de pessoa em texto csv é pŕocessado
                # para gerar uma instância da classe Person, cujos atributos
                # são as variáveis empregadas na identificação
                person = Person(attribs, categs,
                                csv2person(line.split(',')))

                # a identificação do painel é feita a partir do
                # primeiro registro de pessoa
                if pdef:
                    pid = person.ano * 10 + person.tri
                    pdef = False

                # todas as pessoas recebem o código de identificação do painel
                person.pid = pid

                # se for data ignorada, imputa ano de nascimento
                # igual ao ano de inicio do painel
                if person.dtd == 99:
                    person.dta = int(person.pid / 10) - person.age

                # a pessoa do registro é inserida na lista de seu domicílio
                # criando as entradas da upa e do domicílio se necessário
                if person.upa not in painel:
                    painel[person.upa] = {}
                if person.dom not in painel[person.upa]:
                    painel[person.upa][person.dom] = []
                painel[person.upa][person.dom].append(person)
                count += 1
                if count == 10000:
                    count = 0
                    msg = self._ui_show_prgs(msg)
            return pid, painel, msg

        classificadores = (__id_cls1__, __id_cls2__, __id_cls3__)
        with ZipFile(self.copialocal) as src:
            dicionario = json.loads(src.read(str(pPath(META,
                                                       'variaveis.pnadc.'
                                                       + 'trimestral.json'))))
        target = ZipFile(archive, 'a', ZIP_DEFLATED)
        message = '◑'
        for idx, panel in enumerate(panels):
            message = (message[0] + ' Identificando indivíduos'
                       + f' {panel} ({idx + 1} de {len(panels)})')
            message = self._ui_show_prgs(message)

            # carrega o painel na memória
            pid, pan, message = load_panel(
                f'{REGPES}/microdados.pnadc.paineis.{panel}.csv', message)

            # passa a lista de pessoas de cada domicílio do painel
            # para os classificadores
            count = 0
            for upa in tuple(pan.keys()):
                count += 1
                if count == 75:
                    count = 0
                    message = self._ui_show_prgs(message)
                for dom in tuple(pan[upa].keys()):

                    # alguma pessoa tem data de nascimento ignorada
                    if any(pessoa.dtd == 99 for pessoa in pan[upa][dom]):
                        __id_birthdate_unknown__(pan[upa][dom])

                    # identificar e separar os grupos domésticos do domicílio
                    grpsdom = __id_split_grpds__(pan[upa][dom])

                    # identificar os indivíduos de cada grupo doméstico
                    for grpdom in grpsdom:
                        for classificador in classificadores:
                            classificadas = classificador(grpsdom[grpdom],
                                                          grpdom)
                            if classificadas:
                                break

            # escreve o arquivo csv de identificação
            targetfile = StringIO()
            targetfile.write(DELIMITER.join(('ano', 'trimestre', 'upa',
                                             'v1008', 'v1014', 'v1016',
                                             'v2003', 'pid', 'pidcla',
                                             'pidgrp', 'pidgrpent',
                                             'pidind', 'pidindent', 'piddnd',
                                             'piddnm', 'piddna')) + '\n')
            count = 0
            for upa in tuple(pan.keys()):
                count += 1
                if count == 75:
                    count = 0
                    message = self._ui_show_prgs(message)
                for dom in tuple(pan[upa].keys()):
                    for pessoa in pan[upa][dom]:
                        targetfile.write(pessoa.classificada() + '\n')
            targetfile.seek(0)
            target.writestr(f'{REGPID}/pid{pid}.csv', targetfile.read())

        # copia a lista de microdados
        target.writestr(f'{REGPID}/microdados.pnadc.paineis.json',
                        target.read(f'{REGPES}/'
                                    + 'microdados.pnadc.paineis.json'))
        target.close()

    def _panels_individuals(self, panels, file):

        def weights(header, individuos, msg):
            posv1016 = header.index('v1016')
            posv1027 = header.index('v1027')
            posv1029 = header.index('v1029')
            posposest = header.index('posest')
            popposest = {}
            for vis in range(1, 6):
                popposest[str(vis)] = {}
            for individuo in individuos:
                for pessoa in individuos[individuo]:
                    visita = pessoa[posv1016]
                    posest = pessoa[posposest]
                    if posest not in popposest[visita]:
                        msg = self._ui_show_prgs(msg)
                        popposest[visita][posest] = [int(pessoa[posv1029]),
                                                     float(pessoa[posv1027])]
                    else:
                        popposest[visita][posest][1] += float(pessoa[posv1027])
            count = 0
            for individuo in individuos:
                for idx, pessoa in enumerate(individuos[individuo]):
                    visita = pessoa[posv1016]
                    posest = pessoa[posposest]
                    peso = (popposest[visita][posest][0] /
                            popposest[visita][posest][1] *
                            float(pessoa[posv1027]))
                    individuos[individuo][idx] += (str(peso), )
                count += 1
                if count == 20000:
                    msg = self._ui_show_prgs(msg)
                    count = 0
            header.append('pidpeso')
            return header, msg

        def unstack(stacked, pidfile, msg):
            individuos = {}
            src = TextIOWrapper(pidfile, encoding='utf-8')
            pidheader = src.readline()
            pidheader = pidheader.replace('\n', '').split(DELIMITER)
            indpos = tuple(pidheader.index(var) for var in
                           ('upa', 'v1008', 'pidgrp', 'pidind'))
            pespos = tuple(pidheader.index(var) for var in
                           ('upa', 'v1008', 'v1016', 'v2003'))
            pidpos = tuple(pidheader.index(var) for var in pidheader
                           if var[:3] == 'pid')
            count = 0
            for reg in src:
                reg = reg.replace('\n', '').split(DELIMITER)
                indkey = tuple(int(reg[pos]) for pos in indpos)
                try:
                    peskey = tuple(int(reg[pos]) for pos in pespos)
                except IndexError:
                    print(pespos, reg)
                    raise
                pid_dt = tuple(reg[pos] for pos in pidpos)
                if indkey not in individuos:
                    individuos[indkey] = [pid_dt, [peskey]]
                else:
                    individuos[indkey][1].append(peskey)
                count += 1
                if count == 10000:
                    msg = self._ui_show_prgs(msg)
                    count = 0

            pidheader = [var for var in pidheader if var[:3] == 'pid']
            pessoas = {}
            src = TextIOWrapper(stacked, encoding='utf-8')
            panheader = src.readline()
            panheader = panheader.replace('\n', '').split(DELIMITER)
            pespos = tuple(panheader.index(var) for var in
                           ('upa', 'v1008', 'v1016', 'v2003'))
            count = 0
            for reg in src:
                reg = reg.replace('\n', '').split(DELIMITER)
                peskey = tuple(int(reg[pos]) for pos in pespos)
                pessoas[peskey] = tuple(reg)
                count += 1
                if count == 10000:
                    msg = self._ui_show_prgs(msg)
                    count = 0

            count = 0
            for ind in individuos:
                pesind = []
                for peskey in individuos[ind][1][:]:
                    pesind.append(individuos[ind][0] + pessoas[peskey])
                individuos[ind] = pesind
                count += 1
                if count == 10000:
                    msg = self._ui_show_prgs(msg)
            pesheader, msg = weights((pidheader + panheader), individuos, msg)
            return pesheader, individuos, msg

        def write_base(panel, pesheader, individuos, msg):
            # BASE - caso especial
            # inclui todas as variáveis constantes nas visitas
            constantes = ('uf', 'capital', 'rm_ride', 'v1022', 'v1023',
                          'estrato', 'posest', 'v1014', 'pid', 'upa', 'v1008',
                          'pidgrp', 'pidgrpent', 'pidind', 'pidcla',
                          'pidindent', 'piddnd', 'piddnm', 'piddna')
            variaveis = [var for var in pesheader
                         if var[:2] in ('v1', 'v2') or var[:3] == 'vd2'
                         and var not in constantes]
            variaveis.sort()
            variaveis = ['ano', 'trimestre', 'pidpeso'] + variaveis
            header = constantes + tuple(f'{var}_{vis}' for vis in range(1, 6)
                                        for var in variaveis)
            tgt = StringIO()
            tgt.write(DELIMITER.join(header) + '\n')
            count = 0
            for indkey in individuos:
                reg = [individuos[indkey][0][pesheader.index(var)]
                       for var in constantes]
                track = 1
                for pessoa in individuos[indkey]:
                    visita = int(pessoa[pesheader.index('v1016')])
                    while visita > track:
                        reg.extend([''] * len(variaveis))
                        track += 1
                    reg.extend([pessoa[pesheader.index(var)]
                                for var in variaveis])
                    track += 1
                while track < 6:
                    reg.extend([''] * len(variaveis))
                    track += 1
                tgt.write(DELIMITER.join(reg) + '\n')
                count += 1
                if count == 10000:
                    msg = self._ui_show_prgs(msg)
                    count = 0
            tgt.seek(0)
            tgtname = f'{REGIND}/microdados.pnadc.paineis.{panel}.{BASE}.csv'
            msg = self._ui_show_prgs(msg)
            with ZipFile(file, 'a', ZIP_DEFLATED) as archive:
                archive.writestr(tgtname, tgt.read())
            del tgt
            msg = self._ui_show_prgs(msg)
            return msg

        def write_sections(panel, pesheader, individuos, msg):
            constantes = ('pid', 'upa', 'v1008', 'pidgrp', 'pidind')
            sections = ((EDUC, ('v3',)),
                        (TRAB, ('v4',)),
                        (OREN, ('v5', 'vi5')),
                        (DERI, ('vd', 'vdi')),
                        (MORA, ('s01',)),
                        (TICS, ('s07',)),
                        (TURI, ('s08',)),
                        (TRIN, ('s06', 'sd')))
            for section in sections:
                variaveis = [var for var in pesheader
                             if any(prefix in var[:len(prefix)]
                                    for prefix in section[1])]
                if not variaveis:
                    continue
                variaveis.sort()
                header = constantes + tuple(f'{var}_{vis}'
                                            for vis in range(1, 6)
                                            for var in variaveis)
                datafile = StringIO()
                datafile.write(DELIMITER.join(header) + '\n')
                count = 0
                for indkey in individuos:
                    reg = [individuos[indkey][0][pesheader.index(var)]
                           for var in constantes]
                    track = 1
                    for pessoa in individuos[indkey]:
                        visita = int(pessoa[pesheader.index('v1016')])
                        while visita > track:
                            reg.extend([''] * len(variaveis))
                            track += 1
                        reg.extend([pessoa[pesheader.index(var)]
                                    for var in variaveis])
                        track += 1
                    while track < 6:
                        reg.extend([''] * len(variaveis))
                        track += 1
                    datafile.write(DELIMITER.join(reg) + '\n')
                    count += 1
                    if count == 1000:
                        msg = self._ui_show_prgs(msg)
                        count = 0

                # usar tablib para eliminar colunas vazias
                # das visitas sem info suplementar
                data = Dataset()
                datafile.seek(0)
                data.load(datafile, format='csv')
                for var in data.headers[:]:
                    if not any(obs != '' for obs in data[var]):
                        del data[var]
                        msg = self._ui_show_prgs(msg)
                datafile = StringIO(data.export('csv'))
                datafile.seek(0)
                tgtname = (f'{REGIND}/microdados.pnadc.paineis.'
                           + f'{panel}.{section[0]}.csv')
                msg = self._ui_show_prgs(msg)
                with ZipFile(file, 'a', ZIP_DEFLATED) as archive:
                    archive.writestr(tgtname, datafile.read())
                del datafile
                msg = self._ui_show_prgs(msg)
            return msg

        message = '◑'
        for idx, panel in enumerate(panels):
            message = (message[0] + ' Montando painel de indivíduos'
                       + f' {panel} ({idx + 1} de {len(panels)})')
            message = self._ui_show_prgs(message)

            with ZipFile(file) as src:
                stacked = BytesIO(src.read(
                          f'{REGPES}/microdados.pnadc.paineis.{panel}.csv'))
                message = self._ui_show_prgs(message)
                pidfile = BytesIO(src.read(f'{REGPID}/pid{panel}.csv'))
            message = self._ui_show_prgs(message)
            header, individuos, message = unstack(stacked, pidfile, message)
            message = write_base(panel, header, individuos, message)
            message = write_sections(panel, header, individuos, message)
        message = self._ui_show_prgs(message)
        with ZipFile(file, 'a', ZIP_DEFLATED) as tgt:
            tgt.writestr(f'{REGIND}/microdados.pnadc.paineis.json',
                         tgt.read(f'{REGPID}/microdados.pnadc.paineis.json'))


class altFTP(FTP):
    """Corrige problema do servidor de FTP do IBGE."""

    def makepasv(self):
        """
        O servidor do IBGE tem um problema de configuração.

        Retorna um endereço diferente do externo, e em Windows
        isso causa um erro em socket.py, que é chamada por ftplib
        WinError 10060
        """
        invhost, port = super(altFTP, self).makepasv()
        return self.host, port


def pynad_app():
    """Inicia o app."""
    app = QApplication([])
    gui = MainWindow()
    gui.show()
    sys.exit(app.exec())
