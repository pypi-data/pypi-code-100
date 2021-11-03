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

class Label(WinBase):
    def __init__(self, parent:WinBase, rect:Rect):
        super().__init__(parent, rect)
        
        self._text:str = 'Label text'
        self._winUpTextColor: Color = DefaultColor.TEXT_UP.value
        self._winOverTextColor: Color = DefaultColor.TEXT_OVER.value
        self._winDownTextColor: Color = DefaultColor.TEXT_DOWN.value

        self._moState:MouseOverState = MouseOverState.MOS_NONE
        
        self._onMouseMove = self.onMouseMove
        self._onMouseDown = self.onMouseDown
        self._onMouseUp = self.onMouseUp
        
        self._onClick:Callable[[WinBase], bool]|None = None
        
        self.show()

    #每个自定义回调函数的派生类都要实现该方法，并确保调用父类的该方法，以减少内存引用数量
    def clearCallBack(self):
        print('Label clearCallBack before', sys.getrefcount(self))
        super().clearCallBack()
        self._onClick:Callable[[WinBase], bool]|None = None
        print('Label clearCallBack after', sys.getrefcount(self))

    @property
    def text(self)->str:
        return self._text
    @text.setter
    def text(self, textString:str):
        self._text = textString
        
    def draw(self):
        pass
    def drawForm(self):
        self._surface.fill(self._formBGColor)
        match self._moState:
            case MouseOverState.MOS_NONE:
                #self._surface.fill(DefaultColor.BTN_UP.value)
                if self._text != '':
                    self.drawText(self._text, (5,5), self._winUpTextColor, self._fontName, self._fontSize)
            case MouseOverState.MOS_OVER:
                #self._surface.fill(DefaultColor.BTN_OVER.value)
                if self._text != '':
                    self.drawText(self._text, (5,5), self._winOverTextColor, self._fontName, self._fontSize)
            case MouseOverState.MOS_DOWN:
                #self._surface.fill(DefaultColor.BTN_DOWN.value)
                if self._text != '':
                    self.drawText(self._text, (5,5), self._winDownTextColor, self._fontName, self._fontSize)

        #所有都画完后，将surface贴到父窗体的surface上
        parentSurface = self.getParentSurface()
        parentSurface.blit(self._surface, dest=self._pos)

    def drawMousePointer(self):
        pass

    def drawCursor(self):
        pass

    def update(self):
        for childWin in self._zBuffer:
            if childWin == self:
                continue
            childWin.update()
        #这里可以进行update计算

    def eventProcessor(self, winEvent:WinEvent)->bool:
        if super().eventProcessor(winEvent) == False:
            match winEvent.type:
                case WinEventType.WET_BTN:
                    if self._onClick != None:
                        return self._onClick()
            return False
        return True
    
    #onMouseMove要返回False，因为需要桌面窗体来绘制定制鼠标
    def onMouseMove(self, pos, rel, buttons)->bool:
        self._mousePos = pos
        if self._absoluteRect.collidepoint(pos):
            if self._moState != MouseOverState.MOS_DOWN:
                self._moState = MouseOverState.MOS_OVER
            return False
        else:
            self._moState = MouseOverState.MOS_NONE
            if self._absoluteRect.collidepoint(pos):
                return False
            else:
                return False
                
    def onMouseDown(self, pos, button)->bool:
        if button == mouse.LEFT and self._absoluteRect.collidepoint(pos):
            self._moState = MouseOverState.MOS_DOWN
            return True
        return False
    def onMouseUp(self, pos, button)->bool:
        if button == mouse.LEFT and self._absoluteRect.collidepoint(pos):
            self._moState = MouseOverState.MOS_OVER
            winEvent = WinEvent(WinEventType.WET_BTN, ButtonSubEvent.BTN_CLICK, {})
            WinBase.pumpEvent(self, winEvent)
        return False
    def onKeyPress(self, key:keys)->bool:
        return False

    @property
    def onClick(self):
        return self._onClick
    @onClick.setter
    def onClick(self, fn:Callable[[WinBase], bool]|None):
        self._onClick = fn

    #builder mode start here...
    def setTextUpColor(self, color:Color)->WinBase:
        self._winUpTextColor = color
        return self
    def setTextOverColor(self, color:Color)->WinBase:
        self._winOverTextColor = color
        return self
    def setTextDownColor(self, color:Color)->WinBase:
        self._winDownTextColor = color
        return self
    def setClickCallBack(self, fn:Callable[[WinBase], bool]|None)->WinBase:
        self._onClick = fn
        return self
    def setText(self, text:str)->WinBase:
        self._text = text
        return self

