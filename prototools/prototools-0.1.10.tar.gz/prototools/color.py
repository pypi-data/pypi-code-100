import os
from prototools.config import ANSICOLOR, CSI

os.system("")

class Ansi:
    """Clase para los colores Ansi.

    Args:
        codigo (dict): Diccionario de códigos.
    """
    def __init__(self, codigo: dict) -> None:
        for atributo, valor in codigo.items():
            setattr(self, atributo, self.caracter(valor))

    def caracter(self, codigo: dict) -> str:
        """Devuelve un caracter Ansi

        Args:
            codigo (dict): Diccionario de códigos.
        """
        return u"{}{}m".format(CSI,codigo)

fore = Ansi(ANSICOLOR["fore"])
back = Ansi(ANSICOLOR["back"])

colores = (
    "negro", 
    "rojo", 
    "verde", 
    "amarillo", 
    "azul", 
    "magenta", 
    "cyan", 
    "blanco"
)

fg ={colores[x]: f'3{x}' for x in range(8)}
bg ={colores[x]: f'4{x}' for x in range(8)}

RESET = '0'
opt_dict = {
    'bold': '1', 
    'underscore': '4', 
    'blink': '5', 
    'reverse': '7', 
    'conceal': '8'
}

def _colorizar(txt="", opts=(), **kwargs):
    codigos = []
    if txt == "" and len(opts) == 1 and opts[0] == "reset":
        return '\x1b[%sm' % RESET
    for k, v in kwargs.items():
        if k == "fg":
            codigos.append(fg[v])
        elif k == "bg":
            codigos.append(bg[v])
    for o in opts:
        if o in opt_dict:
            codigos.append(opt_dict[o])
    if "norest" not in opts:
        txt = '%s\x1b[%sm' % (txt or '', RESET)
    return '%s%s' % (('\x1b[%sm' % ';'.join(codigos)), txt or '')

def colorizar(texto, fore, back="negro"):
    return f"\x1b[{fg[fore]}m\x1b[{bg[back]}m{texto}\x1b[0m"

def crear_estilo(opts=(), **kwargs):
    """Crea funciones para colorear cadenas de texto.

    todo:
        Añadir ejemplos.

    Example:

        >>> rojo = crear_estilo(fg='rojo')
    """
    return lambda texto: _colorizar(texto, opts, **kwargs)

negro = crear_estilo(fg="negro")
rojo = crear_estilo(fg="rojo")
verde = crear_estilo(fg="verde")
amarillo = crear_estilo(fg="amarillo")
azul = crear_estilo(fg="azul")
magenta = crear_estilo(fg="magenta")
cyan = crear_estilo(fg="cyan")
blanco = crear_estilo(fg="blanco")