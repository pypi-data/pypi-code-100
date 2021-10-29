#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
2020 - Rafael Guerreiro Osorio - Ipea.

pynad - class Person

"""


class Person():
    """
    representa um registro de pessoa.

    As instâncias desta classe representam registros de pessoas e
    seus atributos correspondem às variáveis empregadas na identificação,
    especificadas em __load_panel_metadata__(), função que retorna
    **attribs** e **categs** usados para criar uma instância;
    **values** é o registro como lista de valores e os
    códigos dos atributos da pessoa
    """

    def __init__(self, attribs, categs, values):
        for idx, attrib in enumerate(attribs):
            self.__dict__[attrib] = values[idx]
        self.sexcat = categs['sexcat'][str(self.sex)]
        self.stdcat = categs['stdcat'][str(self.std)] + 18 * ' '
        self.pid = 0
        self.cla = 0
        self.grp = 0
        self.ind = 0
        self.igi = 0
        self.igd = ''
        self.igm = ''
        self.iga = ''
        self.grpent = 0
        self.indent = 0

    def __repr__(self):
        """
        Retorna uma string que representa a pessoa.

        Contém os atributos usados na identificação,
        bem como os resultantes
        """
        repres = (f'e{self.ent} {self.sexcat[:3]} '
                  + f'{self.dta}-{self.dtm:02.0f}-{self.dtd:02.0f} '
                  + f'{self.ord:02.0f} {self.stdcat[:18]} '
                  + f'cla {self.cla} grpd {self.grp} ind {self.ind:02.0f}')
        if self.igd:
            repres += f' ({self.age} anos - {self.ano - self.age}-99-99)'
        return repres

    def classificada(self, csvdel=','):
        """
        Retorna o registro csv correspondente a pessoa.

        Para escrita no no arquivo de identificação de um painel
        """
        return csvdel.join([str(atrib) for atrib in (self.ano, self.tri,
                                                     self.upa, self.dom,
                                                     self.paibge, self.ent,
                                                     self.ord, self.pid,
                                                     self.cla, self.grp,
                                                     self.grpent,
                                                     self.ind, self.indent,
                                                     self.igd, self.igm,
                                                     self.iga)])

    def ident(self, estrita):
        """Retorna os atributos para a agregação em indivíduos."""
        idnt = f'{self.sexcat[:3]} '
        idnt += f'{self.dta}-{self.dtm:02.0f}-{self.dtd:02.0f}'
        if estrita:
            idnt += f' {self.ord:02.0f} {self.stdcat[:18]}'
        return idnt
