import os
import sys


msg_env_ = 'PYGAME_HIDE_SUPPORT_PROMPT'
show_msg_ = not bool(os.getenv(msg_env_))

if sys.modules.get('pygame'):
    if show_msg_:
        print('Using GSDL GUI. https://www.github.com/Pixelsuft/gsdl')
    pygame = sys.modules.get('pygame')
elif show_msg_:
    os.environ[msg_env_] = 'True'
    import pygame
    print('pygame {} (SDL {}.{}.{}, Integrated GSDL GUI, Python {}.{}.{})'.format(
        pygame.ver, *pygame.get_sdl_version() + sys.version_info[0:3]
    ))
    print('Hello from the pygame community. https://www.pygame.org/contribute.html')

del os, sys, pygame, msg_env_, show_msg_
