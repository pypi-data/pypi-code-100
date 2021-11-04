import os
if os.name != 'posix':
    from pynput import keyboard

KEY_TABLE = [
'nul','soh','stx','etx','eot','enq','ack','bel','bs','tab','lf','vt','ff','cr','so','si','dle','dc1','dc2','dc3',
'dc4','nak','syn','etb','can','em','sub','esc','fs','gs','rs','us','space','!','"','#','$','%','&','\'',
'(',')','*','+',',','-','.','/','0','1','2','3','4','5','6','7','8','9',':',';',
'<','=','>','?','@','A','B','C','D','E','F','G','H','I','J','K','L','M','N','O',
'P','Q','R','S','T','U','V','W','X','Y','Z','[','\\',']','^','_','`','a','b','c',
'd','e','f','g','h','i','j','k','l','m','l','o','p','q','r','s','t','u','v','w',
'x','y','z','{','|','}','~','del'
]

if os.name != 'posix':
    def key_str(key):
        key_str = None
        if key == keyboard.Key.delete:
            key_str = 'delete'
        elif key == keyboard.Key.down:
            key_str = 'down'
        elif key == keyboard.Key.esc:
            key_str = 'esc'
        elif key == keyboard.Key.f1:
            key_str = 'f1'
        elif key == keyboard.Key.f2:
            key_str = 'f2'
        elif key == keyboard.Key.f3:
            key_str = 'f3'
        elif key == keyboard.Key.f4:
            key_str = 'f4'
        elif key == keyboard.Key.f5:
            key_str = 'f5'
        elif key == keyboard.Key.f6:
            key_str = 'f6'
        elif key == keyboard.Key.f7:
            key_str = 'f7'
        elif key == keyboard.Key.f8:
            key_str = 'f8'
        elif key == keyboard.Key.f9:
            key_str = 'f9'
        elif key == keyboard.Key.f10:
            key_str = 'f10'
        elif key == keyboard.Key.f11:
            key_str = 'f11'
        elif key == keyboard.Key.f12:
            key_str = 'f12'
        elif key == keyboard.Key.home:
            key_str = 'home'
        elif key == keyboard.Key.left:
            key_str = 'left'
        elif key == keyboard.Key.right:
            key_str = 'right'
        elif key == keyboard.Key.space:
            key_str = 'space'
        elif key == keyboard.Key.up:
            key_str = 'up'
        else:
            key_str = None

        return key_str
else:
    def key_str(key):
        pass