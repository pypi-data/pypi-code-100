import os.path
from playsound import playsound
import pygame
from PIL import Image
from hwpfc import root_dir
import time

def show_image():
    img = Image.open(os.path.join(root_dir, "media/hello.jpg"))
    img.show()


def play_music():
    music_path = os.path.join(root_dir, "media/hello.wav")
    pygame.mixer.init()
    pygame.mixer.music.load(music_path)
    pygame.mixer.music.play()
    time.sleep(5)


def run():
    show_image()
    play_music()

run()