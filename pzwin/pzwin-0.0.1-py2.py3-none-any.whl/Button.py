from enum import IntEnum
from collections.abc import Callable

import os
import sys
import pygame
import pgzero.game
from pygame.rect import Rect

from pgzero.actor import Actor
from pgzero.constants import mouse
from pgzero.constants import keys

from pzwin.Constants import *
from pzwin.WinEvent import *
from pzwin.WinBase import WinBase
from pzwin.Label import Label

class Button(Label):
    def __init__(self, parent:WinBase, rect:Rect):
        super().__init__(parent, rect)
        
        self.__moUpPicPath:str = ''
        self.__winUpBtnPic: pygame.Surface|None = None

        self.__moOverPicPath:str = ''
        self.__winOverBtnPic: pygame.Surface|None = None

        self.__moDownPicPath:str = ''
        self.__winDownBtnPic: pygame.Surface|None = None
        
        self._text:str = 'Button text'

    @property
    def btnUpPic(self)->pygame.Surface:
        return self.__winUpBtnPic
    @btnUpPic.setter
    def btnUpPic(self, picPath:str):
        currentPath = os.path.split(os.path.realpath(__file__))[0]
        self.__moUpPicPath = os.path.join(currentPath, 'images', picPath)
        if os.path.splitext(picPath)[1].lower() == '.png':
            self.__winUpBtnPic: pygame.Surface = pygame.image.load(self.__moUpPicPath).convert_alpha()
        else:
            self.__winUpBtnPic: pygame.Surface = pygame.image.load(self.__moUpPicPath).convert()
    
    @property
    def btnOverPic(self)->pygame.Surface:
        return self.__winOverBtnPic
    @btnOverPic.setter
    def btnOverPic(self, picPath:str):
        currentPath = os.path.split(os.path.realpath(__file__))[0]
        self.__moOverPicPath = os.path.join(currentPath, 'images', picPath)
        if os.path.splitext(picPath)[1].lower() == '.png':
            self.__winOverBtnPic: pygame.Surface = pygame.image.load(self.__moOverPicPath).convert_alpha()
        else:
            self.__winOverBtnPic: pygame.Surface = pygame.image.load(self.__moOverPicPath).convert()
        
    @property
    def btnDownPic(self)->pygame.Surface:
        return self.__winDownBtnPic
    @btnDownPic.setter
    def btnDownPic(self, picPath:str):
        currentPath = os.path.split(os.path.realpath(__file__))[0]
        self.__moDownPicPath = os.path.join(currentPath, 'images', picPath)
        if os.path.splitext(picPath)[1].lower() == '.png':
            self.__winDownBtnPic: pygame.Surface = pygame.image.load(self.__moDownPicPath).convert_alpha()
        else:
            self.__winOverBtnPic: pygame.Surface = pygame.image.load(self.__moOverPicPath).convert()
    
    def drawForm(self):
        self._surface.fill(self._formBGColor)
        match self._moState:
            case MouseOverState.MOS_NONE:
                if self.__winUpBtnPic != None:
                    self._surface.blit(self.__winUpBtnPic, (0,0))
                else:
                    self._surface.fill(DefaultColor.BTN_UP.value)
                    if self._text != '':
                        self.drawText(self._text, (5,5), self._winUpTextColor, self._fontName, self._fontSize)
                    self.drawBorder()
            case MouseOverState.MOS_OVER:
                if self.__winOverBtnPic != None:
                    self._surface.blit(self.__winOverBtnPic, (0,0))
                else:
                    self._surface.fill(DefaultColor.BTN_OVER.value)
                    if self._text != '':
                        self.drawText(self._text, (5,5), self._winOverTextColor, self._fontName, self._fontSize)
                    self.drawBorder()
            case MouseOverState.MOS_DOWN:
                if self.__winDownBtnPic != None:
                    self._surface.blit(self.__winDownBtnPic, (0,0))
                else:
                    self._surface.fill(DefaultColor.BTN_DOWN.value)
                    if self._text != '':
                        self.drawText(self._text, (5,5), self._winDownTextColor, self._fontName, self._fontSize)
                    self.drawBorder()

        #所有都画完后，将surface贴到父窗体的surface上
        parentSurface = self.getParentSurface()
        parentSurface.blit(self._surface, dest=self._pos)

    #builder mode start here...
    def setOffPicture(self, filename:str)->WinBase:
        self.btnUpPic = filename
        return self
    def setOverPicture(self, filename:str)->WinBase:
        self.btnOverPic = filename
        return self
    def setDownPicture(self, filename:str)->WinBase:
        self.btnDownPic = filename
        return self

