from itertools import tee
import os
import sys
import time
import warnings

from functools import wraps, update_wrapper
from typing import Any, Callable, Optional, TypeVar, Union

from prototools.componentes import Borde
from prototools.color import colorizar, crear_estilo
from prototools.experimental import strip_ansi

PLUGINS = dict()

FuncType = Callable[..., Any]
F = TypeVar('F', bound=FuncType)


class Contador:
    """Cuenta el número de llamadas que realiza la funcion decorada.

    Examples:
        Scripts::

            @Contador
            def actualizar():
                print("Actualizando!")

            actualizar()
            actualizar()
            actualizar()
        
        Output::

            Llamada N°1 de 'actualizar'
            Actualizando!
            Llamada N°2 de 'actualizar'
            Actualizando!
            Llamada N°3 de 'actualizar'
            Actualizando!
    """
    def __init__(self, funcion) -> None:
        update_wrapper(self, funcion)
        self.funcion = funcion
        self.llamadas = 0

    def __call__(self, *args: Any, **kwargs: Any) -> Any:
        self.llamadas += 1
        print(f"Llamada N°{self.llamadas} de {self.funcion.__name__!r}")
        return self.funcion(*args, **kwargs)


def debug(funcion):
    """Muestra el signature de la función a decorar y retorna su valor.

    Example:
        Script::
        
            @debug
            def saludar(nombre):
                return f"Hola {nombre}"

            saludar("ProtoTools")

        Output::

            Llamando: saludar('ProtoTools')
            'saludar' retornó 'Hola ProtoTools'
    """
    @wraps(funcion)
    def wrapper(*args, **kwargs):
        args_repr = [repr(a) for a in args]
        kwargs_repr = [f"{k}={v!r}" for k, v in kwargs.items()]
        signature = ", ".join(args_repr + kwargs_repr)
        print(f"Llamando: {funcion.__name__}({signature})")
        valor = funcion(*args, **kwargs)
        print(f"{funcion.__name__!r} retornó {valor!r}")
        return valor
    return wrapper

def obsoleto(mensaje):
    """Decora una funcion obsoleta y manda un mensaje de aviso.

    Example:
        Script::

            @obsoleto("se recomendia usar 'obtener_version()'")
            def obtener():
                return "version 1.0"

            print(obtener())

        Output::

            DeprecationWarning: 
            Función 'obtener' esta obsoleta!, se recomendia usar 
            'obtener_version()'
    
    """
    def inner(funcion):
        @wraps(funcion)
        def wrapper(*args, **kwargs):
            warnings.warn(
                f"\nFunción '{funcion.__name__}' esta obsoleta!, {mensaje}",
                category=DeprecationWarning, 
                stacklevel=2,
                )
            return funcion(*args, **kwargs)
        return wrapper
    return inner

def registrar(funcion):
    """Registra una funcion como un plug-in.
    
    Example:
        Script::

            from prototools.decoradores import PLUGINS, registrar

            @registrar
            def f():
                pass

            print(PLUGINS)

        OUTPUT::

            {'f': <function f at 0x00000258176C64C8>}
    """
    PLUGINS[funcion.__name__] = funcion
    return funcion

def ralentizar(_funcion=None, *, radio: int = 1):
    """Ralentiza unos segundos antes de llamar a la función decorada.

    Example:
        Script::

            @ralentizar(radio=2)
            def temporizador(n):
                if n < 1:
                    print("Fin!")
                else:
                    print(n)
                    temporizador(n - 1)

            temporizador(3)

        Output::

            3
            2
            1
            Fin!
    """
    def inner(funcion):
        @wraps(funcion)
        def wrapper(*args, **kwargs):
            time.sleep(radio)
            return funcion(*args, **kwargs)
        return wrapper
    
    if _funcion is None:
        return inner
    else:
        return inner(_funcion)

def timer(_funcion=None, *, color: Optional[str] = None, fondo: Optional[str] = None):
    """Imprime el tiempo de ejecución de la función a decorar.

    Args:
        color (str, optional): Colorea el tiempo de ejecucion.

    Example:
        Script::

            @timer
            def f(n):
                for _ in range(n):
                    sum([x**2 for x in range(10_000)])

            f(10)

        Output::

            f terminó en 0.0289 segundos
    """
    def inner(funcion):
        if color is None:
            colorizar = crear_estilo(fg="blanco")
        else:
            colorizar = crear_estilo(fg=color)
        if fondo:
            colorizar = crear_estilo(fg=color, bg=fondo)
        @wraps(funcion)
        def wrapper(*args, **kwargs):
            inicio = time.time()
            resultado = funcion(*args, **kwargs)
            fin = time.time()
            print(colorizar(f"'{funcion.__name__}' terminó en {fin - inicio:.4f} segundos"))
            return resultado
        return wrapper
    if _funcion is None:
        return inner
    else:
        return inner(_funcion)

def repetir(_funcion=None, *, n: int = 2):
    """Repite un número determinado de veces la función a decorar.

    Args:
        n (int): Cantidad de veces a repetir.

    Example:
        Script::

            @repetir(4)
            def saludar(nombre):
                print(f"Hola {nombre}!")

            saludar("ProtoTools")

        Output::
            
            Hola ProtoTools!
            Hola ProtoTools!
            Hola ProtoTools!
            Hola ProtoTools!
    """
    def inner(funcion):
        @wraps(funcion)
        def wrapper(*args, **kwargs):
            for _ in range(n):
                resultado = funcion(*args, **kwargs)
            return resultado
        return wrapper
    if _funcion is None:
        return inner
    else:
        return inner(_funcion)

def singleton(cls):
    """Convierte una clase en Singleton Class (una sola instancia).

    Example:
        Script::

            @singleton
            class T:
                pass

        >>> a = T()
        >>> b = T()
        >>> id(a)
        2031647265608
        >>> id(b)
        2031647265608
        >>> a is b
        True
    """
    @wraps(cls)
    def wrapper(*args, **kwargs):
        if not wrapper.instance:
            wrapper.instance = cls(*args, **kwargs)
        return wrapper.instance
    wrapper.instance = None
    return wrapper

def caja(_funcion=None, *, estilo="delgado"):
    """Caja que rodea al retorno de la función decorada.

    Args:
        estilo (str, optional): Estilo del borde.

    Example:
        Script::

            @caja(estilo="doble")
            def mensaje(msj):
                return msj

            mensaje("ProtoTools")

        Output::

            ╔════════════╗
            ║ ProtoTools ║
            ╚════════════╝ 
    """
    def inner(funcion):
        borde = Borde(estilo)
        @wraps(funcion)
        def wrapper(*args, **kwargs):
            resultado = funcion(*args, **kwargs)
            print(u"{izquierda}{centro}{derecha}".format(
                izquierda=borde.superior_izquierdo,
                centro=borde.horizontal * (len(resultado) + 2),
                derecha=borde.superior_derecho,
            ))
            print(u"{lado_izquierdo}{contenido}{lado_derecho}".format(
                lado_izquierdo=borde.vertical,
                contenido=" "+resultado+" ",
                lado_derecho=borde.vertical,
            ))
            print(u"{izquierda}{centro}{derecha}".format(
                izquierda=borde.inferior_izquierdo,
                centro=borde.horizontal * (len(resultado) + 2),
                derecha=borde.inferior_derecho,
            ))
            return resultado
        return wrapper
    if _funcion is None:
        return inner
    else:
        return inner(_funcion)

def banner(contenido: str, ancho: int, estilo: str = None):
    """Coloca el retorno(str) de una funcion decorada dentro de un 
    banner.

    Args:
        contenido (str): Contenido a ser mostrado en el banner.
        ancho (int): Ancho del banner.
        estido (str, optional): Estilo del borde.

    Example:
        Script::

            @banner("ProtoTools", 12)
            def mensaje():
                return None

            mensaje()

        Output::

            ════════════
             ProtoTools   
            ════════════
    """
    if estilo is not None:
        borde = Borde(estilo)
    borde = Borde("doble")
    def inner(funcion):
        @wraps(funcion)
        def wrapper(*args, **kwargs):
            print(borde.horizontal*ancho)
            resultado = funcion(*args, **kwargs)
            print(contenido.center(ancho))
            print(borde.horizontal*ancho)
            return resultado
        return wrapper
    return inner

def continuar(indicacion: str = "Desea continuar? (s/n)") -> bool:
    """Realiza una pregunta (Desea continuar? (s/n))

    Args:
        indicacion (str): Indicacion a mostrar.

    Returns:
        bool: La respuesta (Verdadero o Falso).

    Example:

        >>> respuesta = continuar()
        Desea continuar? (s/n)
        s
        >>> respuesta
        True

    """
    print(indicacion)
    return input().lower().startswith("s")

def calcular_ancho() -> int:
    """Obtiene el ancho de la consola.

    Returns:
        int: El ancho de la consola.

    Example:

        >>> from prototools.utils import calcular_ancho
        >>> print(calcular_ancho())
        80
    """
    if sys.platform in ("win32", "linux", "darwin"):
        return os.get_terminal_size()[0]
    else:
        return 47


def boxln(
    mensaje: str, 
    ancho: Optional[str] = None, 
    color: Optional[str] = None, 
    estilo: Optional[str] = None, 
    alineacion: Optional[str] = "izquierda"
) -> str:
    """Caja con texto colorizado, por defecto blanco.

    Args:
        mensaje (str, optional): Mensaje a mostrar en la caja.
        ancho (int, optional): Ancho de la consola.
        color (str, optional): Color del texto.
        estilo (str, optional): Estilo del borde de la caja.
        alineacion (str, optional): Alineacion de la caja, por defecto
            la alineacion es izquierda.

    Example:

        >>> from prototools.utils import boxln
        >>> boxln('test', ancho=20)
        ┌──────────────────┐
        │Test              │
        └──────────────────┘
        >>> boxln("Test", alineacion="centro", ancho=15, color="verde")
        ┌─────────────┐
        │    Test     │
        └─────────────┘
        >>> boxln("Test", estilo="doble", alineacion="derecha", ancho=9)
        ╔═══════╗
        ║   Test║
        ╚═══════╝
    """
    _alineacion = {"centro": "^", "izquierda": "<", "derecha": ">"}
    if color is None:
        colorizar = crear_estilo(fg="blanco")
    else:
        colorizar = crear_estilo(fg=color)
    if ancho is None:
        ancho = calcular_ancho()
    if estilo is not None:
        borde = Borde(estilo)
    else:
        borde = Borde("delgado")

    real_size = len(strip_ansi(colorizar(mensaje)))
    size = len(colorizar(mensaje))

    print(u"{izquierda}{centro}{derecha}".format(
        izquierda=borde.superior_izquierdo,
        centro=borde.horizontal * (ancho - 2),
        derecha=borde.superior_derecho,
    ))
    print(u"{mi}{contenido:{ali}{ancho}}{md}".format(
        mi=borde.vertical,
        contenido=colorizar(mensaje),
        ali=_alineacion[alineacion],
        ancho=(ancho-2) - real_size + size,
        md=borde.vertical
    ))
    print(u"{izquierda}{centro}{derecha}".format(
        izquierda=borde.inferior_izquierdo,
        centro=borde.horizontal * (ancho - 2),
        derecha=borde.inferior_derecho,
    ))

def bannerln(
    mensaje: str, 
    estilo: Optional[Borde] = None, 
    ancho: Optional[int] = None,
    alineacion: Optional[str] = "derecha",
) -> str:
    """Texto adornado con lineas horizontales.

    Args:
        mensaje (str): Mensaje a mostrar.
        estilo (Borde, optional): Estilo del borde.
        ancho (int, optional): Ancho del banner.
        alineacion (str, optional): Alineacion del banner.
    
    Example:

        >>> bannerln("Test")
        ======= Test =======
    """
    if estilo is None:
        borde = Borde("doble")
    else:
        borde = Borde(estilo=estilo)
    if ancho is None:
        ancho = calcular_ancho()

    if alineacion == "centro":
        print(u"{izquierda} {contenido} {derecha}".format(
            izquierda=borde.horizontal * (
                (ancho - int(round(len(mensaje))))//2 - 1
                ),
            contenido=mensaje,
            derecha=borde.horizontal * (
                (ancho - int(round(len(mensaje))))//2 - 1
                ),
        ))
    elif alineacion == "izquierda":
        print(u"{contenido} {derecha}".format(
            contenido=mensaje,
            derecha=borde.horizontal * (ancho - len(mensaje) -1),
        ))
    elif alineacion == "derecha":
        print(u"{izquierda} {contenido}".format(
            contenido=mensaje,
            izquierda=borde.horizontal * (ancho - len(mensaje) -1),
        ))

def test_funciones(
    objs: dict, 
    mensaje: Optional[str] = "Iteración", 
    retorno: Optional[bool] = False, 
    args: Optional[Union[list, tuple]] = None,
) -> Union[Any, None]:
    """Evaluar funciones.

    Args:
        objs (dict): Diccionario de funciones (key=nombre, value=funcion).
        mensaje (str, optional): Indicacion, por defecto 'Iteración'.
        retorno (bool, optional): Por defecto falso, las funciones 
            evaluadas no retornan nada.
        args (list, tuple, optional): Lista o tupla de argumentos de las
            funciones evaluadas.

    Example:
        Script::
            
            from prototools.utils import test_funciones, registrar, PLUGINS

            F = PLUGINS

            @registrar
            @timer
            def f(x, y):
                return x**y

            test_funciones(F, args=(10, 200))

        Output::

            ════════════════════════════════════════ Iteración N°1 | (10, 200)
            'f' terminó en 0.0002 segundos
    
    todo: 
        Mejorar el ejemplo. Posible cambio a un modulo separado a futuro.
    """
    if isinstance(args, tuple):
        ns = len(args)
    else:
        ns = 1
    maximo = len(str(max(args)))
    
    for n in range(ns):
        bannerln(f"{mensaje} N°{n+1} | {str(args[n]):>{maximo}}")
        for obj in objs.values():
            if args is not None:
                if isinstance(args, tuple):
                    resultado = obj(*args[n])
                else:
                    resultado = obj(args)
            else:
                resultado = obj()
    if retorno:
        return resultado
    else:
        return None

def chunker(secuencia, tamaño):
    """Chunker simple.

    todo:
        Documentacion (incluir ejemplos) y pruebas unitarias.
    """
    return (
        secuencia[posicion:posicion + tamaño] 
        for posicion in range(0, len(secuencia), tamaño)
        )

def mostrar_matriz(m: list, ancho: int = 4, color=None, sep=1) -> None:
    """Muestra una matriz con bordes.

    Args:
        m (list): Matriz.
        ancho (int, optional): Ancho del borde.

    Example:

        >>> from prototools.utils import mostrar_matriz
        >>> m = [[0, 1, 2], [3, 4, 5]] 
        >>> mostrar_matriz(m)
        +----+----+----+
        | 0  | 1  | 2  |
        +----+----+----+
        | 3  | 4  | 5  |
        +----+----+----+
    """
    if color is None:
        for i in range(len(m)):
            r='|'
            for j in range(len(m[i])):
                r += f'{m[i][j]:^{ancho}}|'
            tmp = "+"+"-"*ancho+""
            print(tmp*len(m[0])+"+")
            print(r)
        print(tmp*len(m[0])+"+")
    else:
        for i in range(len(m)):
            r=''
            for j in range(len(m[i])):
                r += f'{m[i][j]:^{ancho}}{" "*sep}'
            print(r)
        print('')

class RangeDict(dict):
    """Custom range.

    Example:

        >>> from prototools.utils import RangeDict
        >>> scale = ({
            (17, 20): 'AD',
            (13, 16): 'A,
            (11, 12): 'B',
            (0, 10): 'C'
        })
    """
    def __missing__(self, key):
        for (start, end), value in ((key, value) for key, value in self.items() if isinstance(key, tuple)):
            if start <= key <= end:
                return value
        raise KeyError(f'{key} not found.')

def pares(iterable):
    """s -> (s0, s1), (s1, s2), (s2, s3), ..."""
    a, b = tee(iterable)
    next(b, None)
    return zip(a, b)


def terminal_size() -> int:
        """Returns the width of the terminal.
        """
        if sys.platform in ("win32", "linux", "darwin"):
            return os.get_terminal_size()[0]
        else:
            return 47