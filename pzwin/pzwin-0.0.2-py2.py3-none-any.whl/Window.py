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
from pzwin.WinFrame import WinFrame
from pzwin.Dialog import Dialog
from pzwin.Button import Button
from pzwin.Label import Label

class Window(WinFrame):
    #DEFAULT_FORM_BG_COLOR = (255, 255, 255)  # White background

    def __init__(self, parent:WinBase|None, rect:Rect):
        super().__init__(parent, rect)
        

    #向窗体添加控件
    def addFrame(self, rect: Rect)->WinFrame:
        return WinFrame(self, rect)
    def addDialog(self, rect: Rect)->Dialog:
        return Dialog(self, rect)


