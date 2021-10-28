import os.path
from playsound import playsound
from PIL import Image
from hwpfc import root_dir

def show_image():
    img = Image.open(os.path.join(root_dir, "media/hello.jpg"))
    img.show()


def play_music():
    playsound(os.path.join(root_dir, "media/hello.wav"))

def run():
    show_image()
    play_music()

run()