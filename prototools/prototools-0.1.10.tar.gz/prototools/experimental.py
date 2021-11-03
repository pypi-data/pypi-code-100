"""
Modulo Experimental
"""
import re
from inspect import getmembers, isfunction
import sys
from textwrap import dedent
from typing import Any, Callable, Tuple, List
from prototools.config import RELLENOS, MARGENES, BORDES, TIPOS_BORDES

tipo = TIPOS_BORDES[1]

_Relleno = type("Relleno", (), RELLENOS)
_Margenes = type("Margenes", (), MARGENES)
_Borde = type(
    "Borde", (), {atributo:valor[tipo] for atributo, valor in BORDES.items()}
    )

class Margen:
    def __init__(self) -> None:
        for atributo, valor in MARGENES.items():
            setattr(self, atributo, valor)


def partir(predicado, valores) -> Tuple[list, list]:
    """
    Separa los valores en dos conjuntos, basado en el retorno de la 
    función (True/False):

        >>> t = partir(lambda x: x < 4, range(9))
        ([4, 5, 6, 7, 8], [0, 1, 2, 3])
    """
    resultado = ([], [])
    for item in valores:
        resultado[predicado(item)].append(item)
    return resultado

def strip_ansi(s):
    t = re.compile(r"""
    \x1b     # caracter ESC
    \[       # caracter [
    [;\d]*   # 0 or mas digitios or punto y comas
    [A-Za-z] # una letra
    """, re.VERBOSE).sub
    return t("",s)


def run_loop(funcion, indicacion, error, args):
    operador_relacional, valor = args
    while True:
        n =int(input(indicacion))
        condicion = {
            '>': n > valor,
            '>=': n >= valor,
            '<': n < valor,
            '<=': n <= valor,
            '==': n == valor,
            '!=': n != valor,
        }
        if condicion[operador_relacional]:
            print(funcion(n)); break
        else:
            print(error)


def main_loop(funcion: Callable, validacion: Callable) -> None:
    """Ejecuta una funcion hasta que la validacion sea falsa.

    Args:
        funcion (Callable): Funcion a iterar.
        valicacion (Callable): Funcion validadora.
    """
    while True:
        funcion()
        if not validacion():
            break


def create_func(name, args, unique):
    """Crea una funcion (experimental).
    """
    template = dedent(f'''
    def {name}({", ".join(args.split())}):
        print('algo')
        {unique}
        print('algo')
    ''').strip()
    ns = {}
    exec(template, ns)
    return ns[name]

def __f():
    return [n for n in globals() if not n.startswith("__")]

def obtener_funciones(modulo):
    return [
        funcion for nombre, funcion in getmembers(modulo, isfunction) 
        if nombre not in ('getmembers', 'getmodule', 'isfunction') 
        and not nombre.startswith("_")
        ]

def modulo():
    return __import__(__name__)

class Modulo:
    def get(self):
        return __import__(__name__)

def crear_enlace(lista):
    return {k:v for k,v in enumerate(lista, 1)}

def return_names():
    return [n for n in sys.modules[__name__].__dir__() if not n.startswith("__")]

def tabulado(m: List[str], alineacion: str = "centro", ancho: int = 20) -> None:
    """Muestra una secuencia de forma tabulada.

    Args:
        m (List[str]): Secuencia a mostrar.
        alineacion (str): Alineacion de los elementos de la secuencia.
        ancho (int): Ancho de columna.

    Returns:
        none: Muestra la secuencia en un formato tabulado.
    """
    alineaciones = {
        "derecha": ">",
        "izquierda": "<",
        "centro": "^",
    }
    for fila in m:
        r=''
        for col in fila:
            r += f'{col:{alineaciones[alineacion]}{ancho}}'
        print(r)


class Tabulado:
    """Clase para representar una pantalla tabulada.

    Args:
        dimension (Tuple): Dimension (fila, columna).

    Example:

        Script::

            t =Tabulado(dimension=(3, 3))
            t.add("Zen",        (0,0))
            t.add("of",         (0,1))
            t.add("Python",     (0,2))
            t.add("Tim Peters", (2,2))
            t.show()

        Output::

            Zen         of          Python       

                                    Tim Peters
    """
    def __init__(self, dimension: Tuple = (3, 6)) -> None:
        self.dimension = dimension
        self._matrix()

    def _matrix(self):
        self.m = [
            ['' for i in range(self.dimension[0])] 
            for j in range(self.dimension[1])
        ]
    
    def add(self, valor: Any, posicion: Tuple) -> None:
        """Metodo para añidar elementos a mostrar posteriormente.

        Args:
            valor (Any): valor del elemento.
            posicion (Tuple): posicion del elemento (fila, columna).
        
        Example::

                # t es una instancia de Tabulado
                t.add("Hola Mundo", (0, 0))
        """
        try:
            self.m[posicion[0]][posicion[1]] = valor
        except IndexError:
            print("Solo puede colocar elementos dentro de la dimension asignada.")

    def show(self, alineacion="centro", ancho=20):
        """Muestra la secuencia usando la funcion 'tabulado'

        Example::
        
                # t es una instancia de Tabulado
                t.show()
        """
        tabulado(self.m, alineacion=alineacion, ancho=ancho)