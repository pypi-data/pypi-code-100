import pygame, codecs
import sys, time, random, math
from pygame.locals import *
def text_print(text, font=None, size=50, color=(0,0,0), xy=(0,0), TF=True):
    """size=字体大小, font=字体名称, xy=位置"""
    a = pygame.font.SysFont(font, size)
    text_font = a.render(text, TF, color)
    screen = pygame.display.get_surface()
    screen.blit(text_font, xy)
def font_print(screen,text, font=None, size=50, color=(0,0,0), xy=(0,0), TF=True):
    """size=字体大小, font=字体名称, xy=位置"""
    a = pygame.font.SysFont(font, size)
    text_font = a.render(text, TF, color)
    screen.blit(text_font, xy)
# 对文件的操作
# 写入文本:
# 传入参数为content，strim，path；content为需要写入的内容，数据类型为字符串。
# path为写入的位置，数据类型为字符串。strim写入方式
# 传入的path需如下定义：path= r’ D:\text.txt’
# f = codecs.open(path, strim, 'utf8')中，codecs为包，需要用impor引入。
# strim=’a’表示追加写入txt，可以换成’w’，表示覆盖写入。
# 'utf8'表述写入的编码，可以换成'utf16'等。

def write_txt(content, strim, path):
    f = codecs.open(path, strim, encoding='utf8')
    f.write(str(content))
    f.close()
# 读取txt：
# 表示按行读取txt文件,utf8表示读取编码为utf8的文件，可以根据需求改成utf16，或者GBK等。
# 返回的为数组，每一个数组的元素代表一行，
# 若想返回字符串格式，可以将改写成return ‘\n’.join(lines)
def read_txt(path):
    with open(path, 'r', encoding='utf8') as f:
        lines = f.readlines()
    return lines

def print_text(font, x, y, text, color=(255, 255, 255)):
    imgText = font.render(text, True, color)
    screen = pygame.display.get_surface()
    screen.blit(imgText, (x,y))
def angular_velocity(angle):
    vel = Point(0, 0)
    vel.x = math.cos( math.radians(angle) )
    vel.y = math.sin( math.radians(angle) )
    return vel
def wrap_angle(angle):
    return abs(angle % 360)
def target_angle(x1, y1, x2, y2):
    delta_x = x2 - x1
    delta_y = y2 - y1
    angle_radians = math.atan2(delta_y, delta_x)
    angle_degrees = math.degrees(angle_radians)
    return angle_degrees
def distance(point1, point2):
    delta_x = point1.x - point2.x
    delta_y = point1.y - point2.y
    dist = math.sqrt(delta_x*delta_x + delta_y*delta_y)
    return dist
class MySprite(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.master_image = None
        self.frame = 0
        self.old_frame = -1
        self.frame_width = 1
        self.frame_height = 1
        self.first_frame = 0
        self.last_frame = 0
        self.columns = 1
        self.last_time = 0
        self.direction = 0
        self.velocty = Point(0, 0)
    def _getx(self): return self.rect.x
    def _setx(self, value): self.rect.x = value
    x = property(_getx, _setx)

    def _gety(self): return self.rect.y
    def _sety(self, value): self.rect.y = value
    y = property(_gety, _sety)

    def _getpos(self): return self.rect.topleft
    def _setpos(self, pos): self.rect.topleft = pos
    position = property(_getpos, _setpos)
    def load(self, filename, width=0, height=0, columns=1):
        self.master_image = pygame.image.load(filename).convert_alpha()
        self.set_image(self.master_image, width, height, columns)
    def set_image(self, image, width=0, height=0, columns=1):
        self.master_image = image
        if width==0 and height==0:
            self.frame_width = image.get_width()
            self.frame_height = image.get_height()
        else:
            self.frame_width = width
            self.frame_height = height
            rect = self.master_image.get_rect()
            self.last_frame = (rect.width // width) * (rect.height // height)-1
        self.rect = Rect(0, 0, self.frame_width, self.frame_height)
        self.columns = columns

    def update(self, current_time, rate=30):
        if current_time > self.last_time + rate:
            self.frame += 1
            if self.frame > self.last_frame:
                self.frame = self.first_frame
            self.last_time = current_time
        if self.frame != self.old_frame:
            frame_x = (self.frame % self.columns) * self.frame_width
            frame_y = (self.frame // self.columns) * self.frame_height
            rect = Rect(frame_x, frame_y, self.frame_width, self.frame_height)
            self.image = self.master_image.subsurface(rect)
            self.old_frame = self.frame
        else:
            self.frame = self.first_frame
    def __str__(self):
        return str(self.frame) + "," + str(self.first_frame) + \
               "," + str(self.last_frame) + "," + str(self.frame_width) + \
               "," + str(self.frame_height) + "," + str(self.columns) + \
               "," + str(self.rect)
class Point(object):
    def __init__(self, x, y):
        self.__x = x
        self.__y = y
    def getx(self):
        return self.__x
    def setx(self, x):
        self.__x = x
    x = property(getx, setx)

    def gety(self):
        return self.__y
    def sety(self, y):
        self.__y = y
    y = property(gety, sety)
    def __str__(self):
        return "{X:" + "{:.0f}".format(self.__x) + \
                ", Y:" + "{:.0f}".format(self.__y) + "}"
class Tank(MySprite):
    def __init__(self):
        MySprite.__init__(self)
    def float_pos(self):
        self.velocity = angular_velocity(angle)
        self.float_pos.x += self.velocity.x
        self.float_pos.y += self.velocity.y
class SnakeSegment(MySprite):
    def __init__(self, color=(20,200,20)):
        MySprite.__init__(self)
        image = pygame.Surface((32,32)).convert_alpha()
        image.fill((255, 255, 255, 0))
        pygame.draw.circle(image, color, (16, 16), 16, 0)
        self.set_image(image)
        MySprite.update(self, 0, 30)
class Food(MySprite):
    def __init__(self):
        MySprite.__init__(self)
        image = pygame.Surface((32,32)).convert_alpha()
        image.fill((255, 255, 255, 0))
        pygame.draw.circle(image, (250, 250, 50), (16, 16), 16, 0)
        self.set_image(image)
        MySprite.update(self, 0, 30)
        self.X = random.randint(0, 23) * 32
        self.Y = random.randint(0, 17) * 32

import PyQt5, tkinter

class Qtclass(PyQt5, tkinter):
    pass

