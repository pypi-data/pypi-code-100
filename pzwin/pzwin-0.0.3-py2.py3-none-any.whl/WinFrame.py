from __future__ import annotations
from enum import IntEnum
from collections.abc import Callable

import os
import sys
import pygame
import pgzrun
import pgzero.game
from pygame.rect import Rect

from pgzero.actor import Actor
from pgzero.constants import mouse
from pgzero.constants import keys

from pzwin.Constants import *
from pzwin.WinEvent import *
from pzwin.WinBase import WinBase
from pzwin.Button import Button
from pzwin.Label import Label
class WinFrame(WinBase):
    def __init__(self, parent:WinBase|None, rect:Rect):
        super().__init__(parent, rect)
        self._onMouseMove = self.onMouseMove
        self._onMouseDown = self.onMouseDown
        self._onMouseUp = self.onMouseUp
        self._onKeyPress = self.onKeyPress
        self._onClose:Callable[[WinBase], bool]|None = None

        #_captionLabel宽度减28是为了扣除左边的图标，再减32是为了扣除右边的关闭按钮
        self._captionLabel: Label = self.addLabel(Rect(28, 0, self._rect.width-28 - 32, 32))\
            .setText(self._caption)\
            .setTextUpColor(DefaultColor.TEXT.value)\
            .setTextOverColor(DefaultColor.TEXT.value)\
            .setTextDownColor(DefaultColor.TEXT.value)\
            .setTextSize(12)
        #参考Windows窗口的按钮，大小似乎只有32点阵宽高
        self.__closeBtn: Button = self.addButton(Rect(rect.width - 32, 0, 32, 32))
        self.__closeBtn.setOffPicture('cross_up.png')\
            .setOverPicture('cross_over.png')\
            .setDownPicture('cross_down.png')\
            .setClickCallBack(self._onClose)

        if parent == None:
            self._isDesktop:bool = True
        else:
            self._isDesktop:bool = False
        self.onCreated()

    #每个自定义回调函数的派生类都要实现该方法，并确保调用父类的该方法，以减少内存引用数量
    def clearCallBack(self):
        super().clearCallBack()
        self._onClose:Callable[[WinBase], bool]|None = None
        self.__closeBtn.setClickCallBack(None)

    def draw(self):
        if self._isShow == False:
            return
        #第一步应该先擦除屏幕，一般来说只需要最底层的deskTop窗体实例调用该函数即可
        self.wipeOff()

        #接着依次绘制窗体和窗体上的组件、边框等，先绘制自己的，再调用子窗体的方法来绘制处于上层的子窗体
        self.drawForm()

        #再根据输入焦点画键盘输入的光标
        self.drawCursor()

        #所有都画完后，将surface贴到父窗体的surface上，如果是deskTop窗体，它的父窗体surface就是pgzero.game.screen
        #if self._isDesktop:
        parentSurface = self.getParentSurface()
        parentSurface.blit(self._surface, self._pos)
        
        #最后画处于最上层的鼠标
        self.drawMousePointer()

    def drawForm(self):
        #对于桌面来说，建议使用全屏模式，这里注释掉是为了方便调式
        if self._isDesktop:
            #os.environ['SDL_VIDEO_CENTERED'] = '1' #居中显示
            #os.environ['SDL_VIDEO_WINDOW_POS'] = "0, 0"
            #pgzero.game.screen = pygame.display.set_mode(self._rect.size)
            #pgzero.game.screen = pygame.display.set_mode(self._rect.size, pygame.NOFRAME|pygame.FULLSCREEN|pygame.SCALED)
            #pygame.mouse.set_visible(False)
            pass

        for childWin in self._zBuffer:
            if childWin == self:
                continue
            childWin.drawForm()

        self.drawBorder()

        #所有都画完后，将surface贴到父窗体的surface上
        if self._isDesktop == False:
            parentSurface = self.getParentSurface()
            parentSurface.blit(self._surface, self._pos)
            #self.getParentSurface().blit(self._surface, self._pos)
    def drawBorder(self):
        if self._borderVisible:
            pygame.draw.rect(self._surface, self._borderColor, Rect(0, 0, self._rect.width, self._rect.height), self._borderThickness)
            pygame.draw.line(self._surface, self._borderColor, (0, 32), (self._rect.width, 32))
    def drawMousePointer(self):
        if self._absoluteRect.collidepoint(self._mousePos):
            parentSurface = self.getParentSurface()
            parentSurface.blit(self._mousePointer, self._mousePos)

    def drawCursor(self):
        pass

    def update(self):
        for childWin in self._zBuffer:
            if childWin == self:
                continue
            childWin.update()
        #这里可以进行update计算
        

    #onMouseMove要返回False，因为需要桌面窗体来绘制定制鼠标
    def onMouseMove(self, pos, rel, buttons)->bool:
        self._mousePos = pos
        return False
    def onMouseDown(self, pos, buttons)->bool:
        return False
    def onMouseUp(self, pos, button)->bool:
        return False
    def onKeyPress(self, key:keys)->bool:
        return False
    def onShonw(self):
        pass
    def onCreated(self):
        pass
    def onClose(self):
        pass
    
    @property
    def onClose(self):
        return self._onClose
    @onClose.setter
    def onClose(self, fn):
        self._onClose = fn
        self.__closeBtn.onClick = fn

    def setCloseCallBack(self, fn:Callable[[WinBase], bool]|None)->WinBase:
        self.onClose = fn
        return self
    def setCaption(self, text:str)->WinBase:
        self.caption = text
        self._captionLabel.setText(text)
        return self

    def addButton(self, rect: Rect)->Button:
        return Button(self, rect)
    def addLabel(self, rect: Rect)->Label:
        return Label(self, rect)
