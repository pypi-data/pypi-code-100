from __future__ import annotations
from abc import abstractmethod, ABCMeta
from collections.abc import Callable

from enum import IntEnum
import os
import sys
import weakref
from queue import Queue

import pygame
import pygame.freetype
from pygame.color import Color
from pygame.rect import Rect

import pgzero.game
from pgzero.actor import Actor
from pgzero.constants import mouse
from pgzero.constants import keys
from pgzero.keyboard import keyboard

from pzwin.Constants import *
from pzwin.WinEvent import WinEvent

g_pzwinDeskTop: WinBase|None = None

class WinBase(metaclass=ABCMeta):
    # 防抖动的计数参数，该值适合于60帧速率的pgzero事件循环函数update()，如果不是60帧的速率，可以适当调整该值
    ANTI_KEY_SHARKING_COUNT: int = 10
    keyCounter:int = 0
    lastKey:keys = keys.POWER  # 这里使用POWER键作为未按键的判断
    
    eventQueue:Queue = Queue()

    _pos:tuple[int, int] #(left, top)
    _size:tuple[int, int] #(width, height)
    _absolutePosition:tuple[int, int] #(left, top)
    _isDesktop:bool = False    
    _rect:Rect
    _absoluteRect:Rect
    _formBGColor:Color
    _surface:pygame.Surface|None
    _fontEntity: dict[str, pygame.freetype.Font] = {}
    _zBuffer:list[WinBase]=[]
    _parent:WinBase|None
    _mousePointer: pygame.Surface|None
    _mousePos:tuple[int, int]
    _mousePointerAnchor:tuple[int, int]
    _isShow:bool

    def __init__(self,  parent:WinBase|None, rect:Rect):
        global g_pzwinDeskTop
        
        self._pos = (rect.left, rect.top)
        self._size = (rect.width, rect.height)
        self._rect = rect
        self._formBGColor = DefaultColor.FORM_BACKGROUND.value
        self._surface:pygame.Surface|None = pygame.Surface(self._size)#None
        self._fontEntity: dict[str, pygame.freetype.Font] = {}
        self._zBuffer:list[WinBase]=[]
        
        self._borderColor:Color = DefaultColor.BORDER.value
        self._borderThickness:int = 1
        self._textColor:Color = DefaultColor.TEXT.value
        self._fontName:str = DefaultFont.NAME
        self._fontSize:int = DefaultFont.SIZE
        self._caption:str = ''
        self._id:str = ''
        self._borderVisible:bool = False
        self._isHorizontalCenter:bool = False
        self._isVerticalCenter:bool = True
        
        if parent != None:#首个窗口（桌面）为None
            self._parent:WinBase|None = weakref.proxy(parent)
            self._parent.lastZBuffer = self
            parentAbsolutionPos:tuple[int, int] = self.getParentAbsolutePosition()
            self._absolutePosition:tuple[int, int] = (parentAbsolutionPos[0] + rect.left, parentAbsolutionPos[1] + rect.top)
            self._absoluteRect:Rect = self.convertToAbsoluteRect()
            self._isDesktop:bool = False
        else:
            self._parent:WinBase|None = None
            g_pzwinDeskTop = self #此处导致桌面顶层窗体的引用计数+1，但对子窗体应该没有影响
            self._isDesktop:bool = True
            self._rect = Rect(0, 0, self._rect.width, self._rect.height)
            self._absolutePosition: tuple[int, int] = (0,0)
            self._absoluteRect:Rect = Rect(0, 0, self._rect.width, self._rect.height)
            self._isShow = True

            self.keyCounter = 0
            self.lastKey = keys.POWER  # 这里使用POWER键作为未按键的判断

            #pgzero.game.screen = pygame.display.set_mode(self._rect.size, pygame.NOFRAME|pygame.FULLSCREEN|pygame.SCALED)
            #pygame.mouse.set_visible(False)
            #self._surface = pgzero.game.screen

        self._onKeyPress:Callable[[WinBase, keys], bool]|None = None
        self._onMouseMove:Callable[[WinBase, tuple, tuple, mouse], bool]|None = None
        self._onMouseDown:Callable[[WinBase, tuple, mouse], bool]|None = None
        self._onMouseUp:Callable[[WinBase, tuple, mouse], bool]|None = None
        self._onShow:Callable[[WinBase], bool]|None = None
        self._onHide:Callable[[WinBase], bool]|None = None


        self.loadMousePointer('mousepointer2.png')
        self._mousePointerAnchor:tuple[int, int] = (0, 0) #鼠标缺省焦点在左上角


        #设置鼠标居中
        self._mousePos = (self._rect.width//2, self._rect.height//2)

    #每个自定义回调函数的派生类都要实现该方法，并确保调用父类的该方法，以减少内存引用数量
    def clearCallBack(self):
        self._onKeyPress:Callable[[WinBase, keys], bool]|None = None
        self._onMouseMove:Callable[[WinBase, tuple, tuple, mouse], bool]|None = None
        self._onMouseDown:Callable[[WinBase, tuple, mouse], bool]|None = None
        self._onMouseUp:Callable[[WinBase, tuple, mouse], bool]|None = None
        self._onShow:Callable[[WinBase], bool]|None = None
        self._onHide:Callable[[WinBase], bool]|None = None        

    #派生出来的组件、窗体，在其实例被del之前，应调用destory来释放内存引用计数
    def destroy(self):
        print('1------X',self._caption, self.__class__, sys.getrefcount(self))#保留打印，以确保能清除干净内存
        for childWin in reversed(self._zBuffer):
            childWin.clearCallBack()
            childWin.destroy()
            del childWin
        self.clearCallBack()
        if self._isDesktop != True:
            try:
                self._parent._zBuffer.remove(self)
                print('2------X', self.__class__, sys.getrefcount(self))#保留打印，以确保能清除干净内存
            except ReferenceError:
                print('none')
        print('3------X', self.__class__, sys.getrefcount(self))#保留打印，以确保能清除干净内存

    def __del__(self):
        print('1------>', self._caption, self.__class__, sys.getrefcount(self))#保留打印，以确保能清除干净内存

    #定义zBuffer的只写属性    
    def _zBufferAppend(self, child: WinBase):
        self._zBuffer.append(child)
    lastZBuffer=property(None, _zBufferAppend)

    @property
    def caption(self):
        return self._caption
    @caption.setter
    def caption(self, captionString:str):
        self._caption = captionString

    def show(self)->WinBase:
        self._isShow = True
        if self._onShow != None:
            self._isShow = self._onShow()
        return self
    @property
    def onShow(self)->Callable[[WinBase], bool]|None:
        return self._onShow
    @onShow.setter
    def onShow(self, fn:Callable[[WinBase], bool]|None):
        self._onShow = fn

    def hide(self)->WinBase:
        self._isShow = False
        if self._onHide != None:
            self._isShow = self._onHide()
        return self
    @property
    def onHide(self)->Callable[[WinBase], bool]|None:
        return self._onHide
    @onHide.setter
    def onHide(self, fn:Callable[[WinBase], bool]|None):
        self._onHide = fn

    def getSurface(self)->pygame.Surface:
        return self._surface
    def getParentSurface(self)->pygame.Surface:
        if self._isDesktop == False:
            return self._parent.getSurface()
        else:
            return pgzero.game.screen

    def getAbsolutePosition(self)->tuple[int, int]:
        return self._absolutePosition
    def getParentAbsolutePosition(self)->tuple[int, int]:
        if self._isDesktop == False:
            return self._parent.getAbsolutePosition()
        else:
            return (0, 0)
    def convertToAbsoluteRect(self)->Rect:
        absolutePos = self.getAbsolutePosition()
        absoluteRect:Rect = Rect(absolutePos[0], absolutePos[1], self._rect.width, self._rect.height)
        return absoluteRect

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
        if self._isDesktop:
            parentSurface = self.getParentSurface()
            parentSurface.blit(self._surface, self._pos)
        #最后画处于最上层的鼠标
        self.drawMousePointer()

    def wipeOff(self):
        self._surface.fill(self._formBGColor)

    def drawForm(self):
        self._surface.fill(self._formBGColor)
                
    def drawText(self, s: str, pos, color, fontName: str, fontSize: int):
        if fontName not in self._fontEntity:
            currentPath = os.path.split(os.path.realpath(__file__))[0]
            self._fontEntity[fontName] = pygame.freetype.Font(
                os.path.join(currentPath, 'fonts',fontName), 20)
        fontRect:Rect = self._fontEntity[fontName].get_rect(s, size=fontSize)
        (targetX, targetY) = pos
        if self._isHorizontalCenter:
            targetX = self._rect.width // 2 - fontRect.width // 2
        if self._isVerticalCenter:
            targetY = self._rect.height // 2 - fontRect.height // 2
        self._fontEntity[fontName].render_to(
            self._surface, (targetX, targetY), s, color, size=fontSize)

    def drawBorder(self):
        if self._borderVisible:
            pygame.draw.rect(self._surface, self._borderColor, Rect(0, 0, self._rect.width, self._rect.height), self._borderThickness)

    @abstractmethod
    def drawMousePointer(self):
        #To do: 由于鼠标pos记录的是在桌面窗体内的位置，所以要计算鼠标在当前窗体中的位置。理论上只应在桌面窗体的重绘时来绘制鼠标，否则会有截断的情况
        #To do: 还要计算anchorPoint
        #self._mousePointer.pos = self._mousePos
        #mouseBlitPos:Rect =
        if self._isDesktop == False:
            return 
        parentSurface = self.getParentSurface()
        parentSurface.blit(self._mousePointer, self._mousePos)

    @abstractmethod
    def drawCursor(self):
        pass

    #返回True说明事件已被处理，不应该再向父窗体传递
    def eventLoop(self, recvWin:WinBase|None, winEvent:WinEvent)->bool:
        if recvWin != None:
            if  self == recvWin:
                return self.eventProcessor(winEvent)
            else:
                for chrldWin in reversed(self._zBuffer):
                    if chrldWin.eventLoop(recvWin, winEvent):
                        return True
            return False
        else:
            for childWin in reversed(self._zBuffer):
                if childWin.eventLoop(recvWin, winEvent):
                    return True
            return self.eventProcessor(winEvent)

    def eventProcessor(self, winEvent:WinEvent)->bool:
        match winEvent.type:
            case WinEventType.WET_KEY:
                if self._onKeyPress != None:
                    return self._onKeyPress(winEvent.params['key'])
            case WinEventType.WET_MOUSE:
                match winEvent.subType:
                    case MouseSubEvent.MOUSE_MOVE:
                        if self._onMouseMove != None:
                            return self._onMouseMove(winEvent.params['pos'], winEvent.params['rel'], winEvent.params['buttons'])
                    case MouseSubEvent.MOUSE_DOWN:
                        if self._onMouseDown != None:
                            return self._onMouseDown(winEvent.params['pos'], winEvent.params['button'])
                    case MouseSubEvent.MOUSE_UP:
                        if self._onMouseUp != None:
                            return self._onMouseUp(winEvent.params['pos'], winEvent.params['button'])
        return False
    def on_mouse_move(self, pos, rel, buttons:mouse):
        winEvent = WinEvent(WinEventType.WET_MOUSE, MouseSubEvent.MOUSE_MOVE, {'pos':pos,'rel':rel, 'buttons':buttons})
        #self.msgLoop(winEvent)
        WinBase.pumpEvent(None, winEvent)
    def on_mouse_down(self, pos, button):
        winEvent = WinEvent(WinEventType.WET_MOUSE, MouseSubEvent.MOUSE_DOWN, {'pos':pos, 'button':button})
        #self.msgLoop(winEvent)
        WinBase.pumpEvent(None, winEvent)
    def on_mouse_up(self, pos, button):
        winEvent = WinEvent(WinEventType.WET_MOUSE, MouseSubEvent.MOUSE_UP, {'pos':pos, 'button':button})
        #self.msgLoop(winEvent)
        WinBase.pumpEvent(None, winEvent)
    @classmethod
    def on_key_press(cls, key:keys):
        winEvent = WinEvent(WinEventType.WET_KEY, KeySubEvent.KEY_PRESS, {'key':key})
        WinBase.pumpEvent(None, winEvent)
    # keyDown()需要在pgzero的on_key_down()事件触发函数中被调用
    @classmethod
    def keyDown(cls, key: keys):
        cls.lastKey = key
        cls.on_key_press(cls.lastKey)
    # keyUp()需要在pgzero的on_key_up()事件触发函数中被调用
    @classmethod
    def keyUp(cls):
        cls.lastKey = keys.POWER
        cls.keyCounter = 0
    # keyPressCheck()需要在pgzero的事件循环函数update()中被调用        
    @classmethod
    def keyPressCheck(cls):
        if keyboard[cls.lastKey]:
            cls.keyCounter += 1
        if cls.keyCounter > cls.ANTI_KEY_SHARKING_COUNT:
            cls.on_key_press(cls.lastKey)
    @abstractmethod
    def onMouseMove(self, pos)->bool:
        pass
    @abstractmethod            
    def onMouseDown(self, pos, button:mouse)->bool:
        pass
    @abstractmethod
    def onMouseUp(self, pos, button:mouse)->bool:
        pass
    @abstractmethod
    def onKeyPress(self, key:keys)->bool:
        pass

    @staticmethod
    def pumpEvent(recvWin:WinBase|None, winEvent: WinEvent):
        if not WinBase.eventQueue.full():
            WinBase.eventQueue.put({'winObj': recvWin, 'event': winEvent})
    
    @classmethod
    def dispatch(cls):
        global g_pzwinDeskTop
        
        cls.keyPressCheck()
        
        while not cls.eventQueue.empty():
            queueElement = cls.eventQueue.get()
            if g_pzwinDeskTop != None:
                g_pzwinDeskTop.eventLoop(queueElement['winObj'], queueElement['event'])
    @abstractmethod
    def update(self):
        pass

    #builder mode start here...
    def setBgColor(self, color:Color)->WinBase:
        self._formBGColor = color
        return self
    def setBorderColor(self, color:Color)->WinBase:
        self._borderColor = color
        return self
    def setBorderThickness(self, thickness:int)->WinBase:
        if thickness >= 0:
            self._borderThickness = thickness
        return self
    def setTextColor(self, color:Color)->WinBase:
        self._textColor = color
        return self
    def setCaption(self, text:str)->WinBase:
        self.caption = text
        return self
    def setMouseMoveCallBack(self, fn:Callable[[WinBase, tuple, tuple, mouse], bool]|None)->WinBase:
        self._onMouseMove = fn
        return self
    def setMouseDownCallBack(self, fn:Callable[[WinBase, tuple, mouse], bool]|None)->WinBase:
        self._onMouseDown = fn
        return self
    def setMouseUpCallBack(self, fn:Callable[[WinBase, tuple, mouse], bool]|None)->WinBase:
        self._onMouseUp = fn
        return self
    def setKeyPressCallBack(self, fn:Callable[[WinBase, keys], bool]|None)->WinBase:
        self._onKeyPress = fn
        return self
    def setShowCallBack(self, fn:Callable[[WinBase], bool]|None)->WinBase:
        self._onShow = fn
        return self
    def setHideCallBack(self, fn:Callable[[WinBase], bool]|None)->WinBase:
        self._onHide = fn
        return self
    def setBorderVisible(self, isVisible:bool)->WinBase:
        self._borderVisible = isVisible
        return self
    def setTextFont(self, fontName:str)->WinBase:
        self._fontName = fontName
        return self
    def setTextSize(self, fontSize:int)->WinBase:
        self._fontSize = fontSize
        return self        
    def setTextHorizontalCenter(self, isHorizontalCenter:bool)->WinBase:
        self._isHorizontalCenter = isHorizontalCenter
        return self
    def setTextVerticalCenter(self, isVerticalCenter:bool)->WinBase:
        self._isVerticalCenter = isVerticalCenter
        return self
    def loadMousePointer(self, fileName:str)->WinBase:
        currentPath = os.path.split(os.path.realpath(__file__))[0]
        currentPath = os.path.join(currentPath, 'images', fileName)
        if os.path.splitext(fileName)[1].lower() == '.png':
            self._mousePointer = pygame.image.load(currentPath).convert_alpha()
        else:
            self._mousePointer = pygame.image.load(currentPath).convert()
        return self
    def setMousePointerAnchor(self, anchorPoint: tuple[int, int] = (0, 0))->WinBase:
        self._mousePointerAnchor:tuple[int, int] = anchorPoint
        return self
    def switchDesktopFullscreenState(self)->WinBase:
        pygame.display.toggle_fullscreen()
        return self
    def setSystemMouseVisibility(self, isVisible:bool)->WinBase:
        pygame.mouse.set_visible(isVisible)
        return self