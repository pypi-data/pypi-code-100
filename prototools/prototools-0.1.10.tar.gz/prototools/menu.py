import os
from prototools.config import ANSICOLOR
import sys
from builtins import input, print
from time import sleep
from typing import Any, Callable, Generator, Optional, Type, Union

from prototools.experimental import strip_ansi
from prototools.componentes import (
    Borde, 
    Dimension, 
    Elementos, 
    Encabezado, 
    Estilo, 
    Texto, 
    Pie, 
    Elemento, 
    Salir, 
    Entrada
)

try:
    import msvcrt
except ImportError:
    pass


class EzMenu:
    """Representacion de un Menu de opciones (EZ version).

    Args:
        opcion (list, optional): Lista o tupla de etiquetas de cada 
            opcion del menu.
        plugins (dict, optional): Diccionario con funciones como 
            valores.
        titulo (str, optional): Titulo por defecto 'Menu'.
        indicacion (str, optional): Mensaje por defecto 'Opcion:'.
        ancho (int, optional): Ancho del Menu.
        registrar (bool, optional): Si es verdadero, acepta el 
            registro de plugins.
        color Optional[bool]: Si es verdadero, acepta cadenas de texto
            en color (sin deformar el menu).

    Example:
        Script::

            from prototools.menu import EzMenu
            
            def _entradas():
                x = input("Ingresar el primer numero: ")
                y = input("Ingresar el segundo numero: ")
                return float(x), float(y)

            def suma():
                x, y = _entradas(mensajes)
                print(x + y)

            def resta():
                x, y = _entradas(mensajes)
                print(x - y)

            def multiplicacion():
                x, y = _entradas(mensajes)
                print(x * y)

            def division():
                x, y = _entradas(mensajes)
                try:
                    print(x/y)
                except ZeroDivisionError:
                    print("No es divisible")

            menu = EzMenu()
            menu.agregar_opciones(
                "sumar", "restar", "multiplicar", "dividir", "salir"
                )
            menu.agregar_funciones(
                suma, resta, multiplicacion, division
                )
            menu.run()

        Output::

            ┌──────────────────────────────────────┐
            │            Menu Principal            │
            │ 1. Sumar                             │
            │ 2. Restar                            │
            │ 3. Multiplicar                       │
            │ 4. Dividir                           │
            │ 5. Salir                             │
            └──────────────────────────────────────┘
            Opcion:
    """
    def __init__(
        self, 
        opcion: Optional[list] = None,
        plugins: Optional[dict] = None,
        titulo: Optional[str] = "Menu Principal",
        indicacion: Optional[str]= "Opcion: ",
        ancho: Optional[int] = None,
        registrar: Optional[bool] = False,
        color: Optional[bool] = False,
    ) -> None :
        self.opcion = opcion
        self.opciones = []
        self.plugins = plugins
        self.__funciones = {}
        self._titulo = titulo
        self._indicacion = indicacion
        self.mensajes = {}
        self.borde = Borde()
        if ancho is None:
            self.ancho = self._obtener_ancho()
        else:
            self.ancho = ancho
        if registrar:
            for i, v in enumerate(plugins.values(), 1):
                self.__funciones[i] = v
        if color:
            self.color = 1
        else:
            self.color = 0


    def titulo(self, titulo: str):
        """Modifica el titulo del menu principal de opciones.
        
        Args:
            titulo (str): Titulo principal a mostrar en el menu de 
                opciones.

        Examples:

            >>> from prototools.menu import EzMenu
            >>> menu = EzMenu()
            >>> menu.titulo("Bienvenido")
        """
        self._titulo = titulo

    def indicacion(self, mensaje: str):
        """Modifica el mensaje de la indicacion de la entrada.
        
        Args:
            mensaje (str): Mensaje a mostrar en la entrada de 
                opciones.

        Example:

            >>> from prototools.menu import EzMenu
            >>> menu = EzMenu()
            >>> menu.indicacion("Ingresa una opcion: ")
        """
        self._indicacion = mensaje

    def agregar_opciones(self, *args):
        """Agrega las opciones del menú.
        
        Args:
            *args (str): Serie de opciones.

        Example:

            >>> from prototools.menu import EzMenu
            >>> menu = EzMenu()
            >>> menu.agregar_opciones("Registrar", "Ver", "Salir")
        """
        for arg in args:
            self.opciones.append(arg)

    def agregar_funcion(self, nombre: Callable, key: int, args: Any = None):
        """Agrega una funcion al menú.
        
        Args:
            nombre (func): Nombre de la función.
            key (int): Número del menú de opciones.
            args (Any, optional): Argumentos de la funcion.
        
        Example:
            ::

                from prototools.menu import EzMenu

                def f():
                    pass

                menu = EzMenu()
                menu.agregar_funcion(f)
        """
        if args is None:
            self.__funciones[key] = nombre
        else:
            self.__funciones[key] = lambda: nombre(args)

    def agregar_funciones(self, *args):
        """Agrega una serie de funciones al menú.
        
        Args:
            *args (Callable): Nombre de funciones ordenadas al igual 
                que el menú de opciones.

        Example:
            ::

                from prototools.menu import EzMenu

                def a():
                    pass

                def b():
                    pass

                def c():
                    pass

                menu = EzMenu()
                menu.agregar_funciones(a, b, c)
        """
        for i, arg in enumerate(args, 1):
            self.__funciones[i] = arg

    def _pantalla_menu(self):
        """Imprime en pantalla las opciones del menu."""
        if self.color:
            _titulo = strip_ansi(self._titulo)
            _t = len(self._titulo) - len(_titulo)
        else:
            _t = 0
        print(
            self.borde.superior_izquierdo 
            + self.borde.horizontal * (self.ancho-2) 
            + self.borde.superior_derecho
        )
        print(
            f"{self.borde.vertical}"
            f"{self._titulo:^{self.ancho-2+_t}}"  
            f"{self.borde.vertical}"
        )
        for numero, opcion in enumerate(self.opciones):
            _tmp = len(strip_ansi(opcion))+5 # todo
            tmp = f"{self.borde.vertical} {numero + 1}. {opcion.capitalize()}"
            print(f"{tmp}{self.borde.vertical:>{self.ancho-_tmp}}") 
        print(
            self.borde.inferior_izquierdo 
            + self.borde.horizontal * (self.ancho-2) 
            + self.borde.inferior_derecho
        )

    def _clear(self) -> None:
        """Limpia la pantalla."""
        os.system('cls' if os.name == 'nt' else 'clear')

    def _esperar(self) -> Callable:
        """Espera por alguna respuesta del usuario.
        """
        print("\nPresionar cualquier tecla para continuar...")
        return msvcrt.getch() if os.name == "nt" else input()

    def _obtener_ancho(self) -> int:
        """Obtiene el ancho de la consola.
        """
        if sys.platform in ("win32", "linux", "darwin"):
            return os.get_terminal_size()[0]
        else:
            return 47

    def run(self):
        """Ejecuta el menu de opciones.

        Example:

            >>> from prototools import EzMenu
            >>> menu = EzMenu()
            >>> menu.run()
        """
        ultima_opcion = len(self.opciones)
        while True:
            self._clear()
            self._pantalla_menu()
            opcion = input(self._indicacion)
            self._clear()
            try:
                if int(opcion) == ultima_opcion:
                    print("Fin del programa")
                    sleep(1)
                    break
                if int(opcion) not in self.__funciones:
                    print("Opcion no disponible")
                else:
                    self.__funciones[int(opcion)]()
                self._esperar()
            except ValueError:
                print("Solo se aceptan numeros")
                self._esperar()
        sys.exit(0)


class ConstruirMenu:
    """
    Constructor para generar el formato del menu.

    Args:
        dimension_max (Dimension, optional): Dimension maxima del menu.

    Example:
        Script::

            from prototools.componentes import (
                Dimension, Elemento, Salir
                )
            from prototools.menu import ConstruirMenu

            e1 = Elemento("Consultar")
            e2 = Elemento("Registrar")
            e3 = Elemento("Opciones Avanzadas")
            e4 = Salir()

            c = ConstruirMenu(dimension_max=Dimension(ancho=40))
            print(c.formatear(
                titulo="Menu Principal",
                elementos=(e1, e2, e3, e4)
                )
            )

        Output::

                ┌─────────────────────────────────┐
                │                                 │
                │         Menu Principal          │
                │                                 │
                │                                 │
                │  1 - Consultar                  │
                │  2 - Registrar                  │
                │  3 - Opciones Avanzadas         │
                │  4 - Salir                      │
                │                                 │
                │                                 │
                └─────────────────────────────────┘

                >>>
                
    """
    def __init__(self, dimension_max: Optional[Dimension] = None) -> None:
        if dimension_max is None:
            dimension_max = Dimension(ancho=80, alto=40)
        self._dimensio_max = dimension_max
        self._encabezado = Encabezado(Estilo(), dimension_max=dimension_max)
        self._prologo = Texto(Estilo(),dimension_max=dimension_max)
        self._elementos = Elementos(Estilo(), dimension_max=dimension_max)
        self._epilogo = Texto(Estilo(), dimension_max=dimension_max)
        self._pie = Pie(Estilo(), dimension_max=dimension_max)
        self._entrada = Entrada(Estilo(), dimension_max=dimension_max)

    def limpiar_datos(self):
        """Limpia los datos desde una generacion previa del menu."""
        self._encabezado.titulo = None
        self._encabezado.subtitulo = None
        self._prologo.texto = None
        self._epilogo.texto = None
        self._elementos.elementos = None

    def formatear(
        self, 
        titulo=None, 
        subtitulo=None, 
        prologo_texto=None, 
        epilogo_texto=None, 
        elementos=None
    ) -> str:
        self.limpiar_datos()
        contenido = ""
        if titulo is not None:
            self._encabezado.titulo = titulo
        if subtitulo is not None:
            self._encabezado.subtitulo = subtitulo
        secciones = [self._encabezado]
        if prologo_texto is not None:
            self._prologo.texto = prologo_texto
            secciones.append(self._prologo)
        if elementos is not None:
            self._elementos.elementos = elementos
            secciones.append(self._elementos)
        if epilogo_texto is not None:
            self._epilogo.texto = epilogo_texto
            secciones.append(self._epilogo)
        secciones.append(self._pie)
        secciones.append(self._entrada)
        for seccion in secciones:
            contenido += "\n".join(seccion._generar())
            if not isinstance(seccion, Entrada):
                contenido += "\n"
        return contenido