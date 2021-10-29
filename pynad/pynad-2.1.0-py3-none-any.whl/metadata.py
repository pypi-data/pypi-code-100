#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
2020 - Rafael Guerreiro Osorio - Ipea.

pynad - métodos de extração de metadados

ROTINAS QUE DEPENDEM DE COMO O IBGE DIVULGA METADADOS
"""

import re
from io import BytesIO
from pathlib import Path, PurePosixPath as pPath
from zipfile import ZipFile, ZIP_DEFLATED
from tablib import Dataset

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


def _metadata_pnadc_anual(mirrorfile):
    """
    Extrai e organiza metadados da pnadc anual.

    Esta rotina depende de como o IBGE organiza os
    arquivos para divulgação

    Em dezembro de 2019 a estrutura de disseminação da pnadc
    anual mudou radicalmente

    Há pastas para:
     - 5 visitas (dicionario por visita e por ano)
     - 4 trimestres (dicionário por trimestre vale para todos os anos)
    """
    archive = ZipFile(mirrorfile, 'a', ZIP_DEFLATED)
    microdados = _metadata_pnadc_anual_arquivos(archive.namelist())
    for microdado in microdados:
        # lê o dicionário correspondente
        temp = BytesIO(archive.read(microdado[1]))
        doc = Dataset()
        doc.load(temp.getvalue(), format='xls')
        dicionario = _metadata_pnadc_vars(doc.export('tsv'))

        # acrescenta à lista
        nome = Path(microdado[0]).name
        if 'trimestre' in nome:
            dicid = nome[:-4].split('_')[2]
        else:
            dicid = '.'.join(nome[:-4].split('_')[1:3])
        target = f'variaveis.pnadc.anual.{dicid}.json'
        microdado[2] = [str(pPath(META, target)), dicionario]
    archive.close()
    return microdados


def _metadata_pnadc_anual_arquivos(zipitems):
    microdados = []
    for vis in range(1, 6):
        datafolder = pPath(ORI, PNADCA, CA_VIS, f'{CA_VIS}_{vis}', CA_DATA)
        docsfolder = pPath(ORI, PNADCA, CA_VIS, f'{CA_VIS}_{vis}', CA_DOCS)
        docfiles = [item for item in zipitems
                    if str(docsfolder) in item
                    and 'dicionario' in item
                    and item.endswith('xls')]
        datafiles = [item for item in zipitems
                     if str(datafolder) in item
                     and item.endswith('zip')]
        for doc in docfiles:
            anodoc = Path(doc).name.split('_')[3]
            microdados.extend([[item, doc, '', PNADCA]
                               for item in datafiles
                               if (Path(item).name.split('_')[1]
                                   == anodoc and f'{CA_VIS.lower()}{vis}'
                                   in item) or
                               (Path(item).name.split('_')[1]
                                in ('2013', '2014') and
                                f'{CA_VIS.lower()}{vis}'
                                in item and anodoc == '2012')])
    for tri in range(1, 5):
        datafolder = pPath(ORI, PNADCA, CA_TRI, f'{CA_TRI}_{tri}', CA_DATA)
        docsfolder = pPath(ORI, PNADCA, CA_TRI, f'{CA_TRI}_{tri}', CA_DOCS)
        docfiles = [item for item in zipitems
                    if str(docsfolder) in item
                    and 'dicionario' in item
                    and item.endswith('xls')]
        datafiles = [item for item in zipitems
                     if str(datafolder) in item
                     and item.endswith('zip')]
        if docfiles:
            doc = docfiles[0]
            microdados.extend([[item, doc, '', PNADCA]
                               for item in datafiles])
    return microdados


def _metadata_pnadc_trimestral(mirrorfile):
    """
    Extrai e organiza metadados da pnadc trimestral.

    Esta rotina depende de como o IBGE organiza os
    arquivos para divulgação
    """
    archive = ZipFile(mirrorfile, 'a', ZIP_DEFLATED)

    # apenas um dicionário para a pnadc trimestral
    file = [file for file in archive.namelist() if
            all(stub in file for stub
                in (ORI, PNADCT, TRIDOCS, 'Dicionario_e_input'))]

    if not file:
        archive.close()
        return None

    file = file[0]

    # ler o arquivo zip do dicionário e obter metadados
    buffer = BytesIO(archive.read(file))
    file = ZipFile(buffer)
    diciori = [item for item in file.namelist()
               if 'dicionario' in item][0]
    original = BytesIO(file.read(diciori))

    # le o dicionario com tablib e converte para tsv
    doc = Dataset()
    doc.load(original.getvalue(), format='xls')
    dicionario = _metadata_pnadc_vars(doc.export('tsv'))
    target = str(pPath(META, 'variaveis.pnadc.trimestral.json'))

    # lista com os arquivos de microdados trimestrais
    arquivos = archive.namelist()
    arquivos.remove('pynad.json')
    microdados = [[item, diciori, [target, dicionario, original], PNADCT]
                  for item in arquivos
                  if ORI in item and PNADCT in item and
                  item.split('/')[2].isnumeric()]
    archive.close()
    return microdados


def _metadata_pnadc_vars(contents):
    """Depende da estrutura dos dicionários de variáveis."""
    def __clean_label(label):
        label = label.replace('"', '').strip()
        label = label.replace('\n', ' ')
        label = re.sub(' +', ' ', label)
        try:
            label = int(float(label))
        except ValueError:
            pass
        return label

    def __set_bytes(size):
        # dtype bytes para armazenar 9 * colunas da var
        # C signed numeric types
        # 99 - 1 byte
        # 9999 - 2 bytes
        # 999999999 - 4 bytes - float ou int
        # >999999999 - 8 bytes - double ou long
        # pnadc pesos são floats - code 15
        bts = 'ERROR'
        if size <= 2:
            bts = 1
        elif size <= 4:
            bts = 2
        elif size <= 9:
            bts = 4
        elif size <= 14:
            bts = 8
        elif size == 15:
            bts = 15
        return bts

    # meta é o dicionário de variáveis
    meta = {}
    curvar = None

    # seção do questionário
    parte = ''

    # pula linhas de cabeçalho e processa
    rows = contents.split('\r\n')[3:-1]
    for row in rows:

        # line breaks, double spaces e outras coisas
        # limpar campos para processar linhas
        fields = [__clean_label(field) for field in row.split('\t')]

        # linha com informação de "parte" do questionário
        if fields[0] and not fields[1]:
            parte = fields[0].lower()

        # linha principal de variável
        elif all(isinstance(field, int)
                 for field in (fields[0], fields[1])):

            # código (uf, v1008 etc) é a chave em meta
            curvar = fields[2].lower()
            meta[curvar] = {}

            # parte atual
            meta[curvar][_VPART] = parte

            # tuple com:
            # coluna inicial - index em 1
            # coluna final
            # número de colunas
            meta[curvar][_VPOS] = (fields[0],
                                   fields[0] + fields[1] - 1,
                                   fields[1])

            meta[curvar][_VSIZE] = __set_bytes(meta[curvar][_VPOS][2])

            # número do quesito (se tiver)
            meta[curvar][_VQUES] = fields[3]

            # descrição da variável
            meta[curvar][_VDESC] = fields[4].lower()
            if not meta[curvar][_VDESC]:
                meta[curvar][_VDESC] = curvar

            # período
            meta[curvar][_VPER] = fields[7].lower()

            # tem campo 5 - categórica ou info adicional
            meta[curvar][_VCAT] = {}
            especial = (' a ', 'código', 'valor', '130', '01-')
            if (isinstance(fields[5], int)
                    or any(item in fields[5].lower() for item in especial)):
                meta[curvar][_VCAT][fields[5]] = str(fields[6]).lower()
            elif fields[5] or fields[6]:
                meta[curvar][_VCAT] = ', '.join([item.lower()
                                                 for item in fields[5:7]
                                                 if item])

        # linha de categoria
        elif not fields[0] and not fields[1]:
            if not fields[5]:
                fields[5] = _MISS
            try:
                meta[curvar][_VCAT][fields[5]] = fields[6].strip().lower()
            except TypeError:
                print(curvar, fields)
    return meta
