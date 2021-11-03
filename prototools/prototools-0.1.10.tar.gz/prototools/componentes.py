import os
import platform
import subprocess
import sys
import textwrap
from builtins import input, print
from typing import Any
from typing import Generator, Optional, Type

from prototools.config import BORDES, MARGENES, RELLENOS, TIPOS_BORDES


class Pantalla:
    """Componente de Pantalla para consola.

    Args:
        alto (int): Alto de la pantalla en columnas.
        ancho (int): Ancho de la pantalla en filas.

    Example:

        >>> from prototools.componentes import Pantalla
        >>> pantalla = Pantalla()
    """

    def __init__(self) -> None:
        self._tw = textwrap.TextWrapper()
        if sys.platform in ("win32", "linux", "darwin"):
            ancho = os.get_terminal_size()[0]
        else:
            ancho = 47
        self._alto = 40
        self._ancho = ancho

    @property
    def alto(self) -> int:
        """int: Alto de la pantalla en columnas.
        """
        return self._alto

    @property
    def ancho(self) -> int:
        """int: Ancho de la pantalla en filas.
        """
        return self._ancho

    @staticmethod
    def clear() -> None:
        """Llamado a la funcion 'clear' específica de cada plataforma.
        """
        if platform.system() == "Windows":
            subprocess.check_call("cls", shell=True)
        else:
            print(subprocess.check_output("clear").decode())
    
    @staticmethod
    def flush() -> None:
        """Volcado del buffer.
        """
        sys.stdout.flush()
    
    @staticmethod
    def input(indicacion: str) -> str:
        """Indicación a mostrar al momento de ingresar una entrada.

        Args:
            indicacion (str): mensaje a mostrar.

        Returns:
            La entrada del usuario. 
        """
        return input(indicacion)

    @staticmethod
    def printf(*args: Any) -> None:
        """Muestra los argumentos en la pantalla.

        Args:
            *args: Parámetros de tamaño variable.
        """
        print(*args, end='')
    
    @staticmethod
    def println(*args: Any) -> None:
        """Muestra los argumentos en la pantalla, incluyendo una
        nueva línea.

        Args:
            *args: Parámetros de tamaño variable.
        """
        print(*args)


class Borde:
    """Borde del menu.

    Args:
        tipo (str): Tipo de borde.
        superior_izquierdo (str): Borde superior izquierdo.
        superior_derecho (str): Borde superior derecho.
        inferior_izquierdo (str): Borde inferior izquierdo.
        inferior_derecho (str): Borde inferior derecho.
        vertical (str): Borde vertical.
        vertical_izquierdo (str): Borde vertical izquierdo.
        vertical_derecho (str): Borde vertical derecho.
        horizontal (str): Borde horizontal.
        horizontal_izquierdo (str): Borde horizontal izquierdo.
        horizontal_derecho (str): Borde horizontal derecho.
        interseccion (str): Borde de interseccion.

    Examples:

        >>> borde = Borde()
        >>> borde.superior_izquierdo
        '┌'
        >>> borde = Borde("ascii")
        >>> borde.superior_izquierdo
        '+'
        >>> borde = Borde("doble")
        >>> borde.establecer_borde("grueso")
        >>> borde.tipo
        'grueso'
    """
    def __init__(self, tipo: str = "delgado") -> None:
        self.tipo = tipo
        self.establecer_borde(self.tipo)

    def establecer_borde(self, tipo: str):
        """Establece el tipo del borde.
        
        Args:
            tipo (str): Tipo de borde (ascii, delgado, grueso, doble).
        
        Example:

            >>> borde = Borde()
            >>> borde.establecer_borde('ascii')
            >>> borde.tipo
            'ascii'
        """
        if tipo in TIPOS_BORDES.values():
            self.tipo = tipo
            for atributo, valor in BORDES.items():
                setattr(self, atributo, valor[tipo])
        else:
            raise TypeError(
                f"'tipo' debe ser 'str' y estar en las siguientes opciones: "
                f"{', '.join(list(TIPOS_BORDES.values()))}"
                )


class Margen:
    """Margenes del menu.
    
    El margen es el area entre las dimensiones maximas especificadas
    (el ancho y el alto de la pantalla) y el borde el menu.

    Args:
        izquierdo (int): Margen izquierdo.
        derecho (int): Margen derecho.
        superior (int): Margen superior.
        inferior (int): Margen inferior.
    
    Examples:

        >>> from prototools.componentes import Margen
        >>> margen = Margen()
        >>> margen.derecho
        2
        >>> margen.superior
        1
    """
    def __init__(self) -> None:
        for atributo, valor in MARGENES.items():
            setattr(self, atributo, valor)


class Relleno:
    """Relleno del menu.

    El relleno es el area entre el borde del menu y el contenido
    del menu.

    Args:
        izquierdo (int): Relleno izquierdo.
        derecho (int): Relleno derecho.
        superior (int): Relleno superior.
        inferior (int): Relleno inferior.

    Examples:

        >>> from prototools.componentes import Relleno
        >>> relleno = Relleno()
        >>> relleno.izquierdo
        2
        >>> relleno.inferior
        1
    """
    def __init__(self) -> None:
        for atributo, valor in RELLENOS.items():
            setattr(self, atributo, valor)


class Estilo:
    """Clase para especificar todo el estilo del menu (margenes, 
    relleno y borde).

    Args:
        margen (Margen): Margen del menu.
        relleno (Relleno): Relleno del menu.
        borde (Borde): Borde del menu.

    Examples:

        >>> estilo = Estilo()
        >>> estilo.margen.izquierdo
        2
        >>> estilo.borde.tipo
        'delgado'
        >>> estilo.rellono.inferior
        1
    """
    def __init__(
        self, 
        margen: Margen = None, 
        relleno: Relleno = None, 
        tipo_borde: str = None,
    ) -> None:
        if margen is None:
            margen = Margen()
        self.margen = margen
        if relleno is None:
            relleno = Relleno()
        self.relleno = relleno
        if tipo_borde is not None:
            borde = Borde(tipo_borde)
        else:
            borde = Borde()
        self.borde = borde


class Dimension:
    """Ancho y alto de un componente.

    Args:
        ancho (int): Ancho del componente en columnas.
        alto (int): Alto del componente en filas.
        dimension (Dimension, optional): Dimension existente para 
            duplicar el ancho y el alto.

    Examples:

        >>> dimension = Dimension(40,20)
        >>> dimension.alto
        40
        >>> dimension.ancho
        20
        >>> otra_dimension = Dimension()
        >>> otra_dimension
        '0x0'
        >>> nueva_dimension = Dimension(dimension=dimension)
        >>> nueva_dimension
        '40x20'
    """
    def __init__(
        self, 
        ancho: int = 0, 
        alto: int = 0, 
        dimension: Optional[Type["Dimension"]] = None
    ) -> None:
        self.ancho = ancho
        self.alto = alto
        if dimension is not None:
            self.ancho = dimension.ancho
            self.alto = dimension.alto

    def __str__(self):
        return f"{self.ancho}x{self.alto}"


class Componente:
    """Clase base para los componentes del Menu.

    Args:
        estilo: Estilo para el componente.
        dimension_max: Dimension maxima del menu (ancho x alto). Si
            no se especifica, los valores por defecto seran ancho=80
            y alto=40.

    Raises:
        TypeError: Si estilo no es del tipo Estilo.

    Examples:

        >>> componente = Componente(Estilo())
    """
    def __init__(self, estilo, dimension_max=None) -> None:
        if not isinstance(estilo, Estilo):
            raise TypeError("estilo debe ser de tipo Estilo")
        if dimension_max is None:
            dimension_max = Dimension(ancho=80, alto=40)
        self._estilo = estilo
        self._dimension_max = dimension_max

    @property
    def dimension_max(self):
        """La dimension máxima del componente."""
        return self._dimension_max

    @property
    def margen(self):
        """Los margenes de este componente."""
        return self._estilo.margen

    @property
    def relleno(self):
        """Los rellenos de este componente."""
        return self._estilo.relleno

    @property
    def borde(self):
        """Los bordes de este componente."""
        return self._estilo.borde

    def calcular_ancho_borde(self) -> int:
        """Calcula el ancho del borde del menu.
        
        Si el ancho máximo es de 80 caracteres y los margenes 
        izquierdo y derecho son 1, el ancho seria 77 
        (80 - 1 - 1 - 1 = 77).

        Returns:
            int: Ancho del borde en columnas.

        Example:

        >>> margen = Margen()
        >>> margen.izquierdo = 1
        >>> margen.derecho = 1
        >>> componente = Componente(Estilo(margen=margen))
        >>> componente.calcular_ancho_borde()
        77
        """
        return (self.dimension_max.ancho 
                - self.margen.izquierdo 
                - self.margen.derecho - 1)
    
    def calcular_ancho_contenido(self) -> int:
        """Calcula el ancho del contenido.

        Si el ancho del borde es de 77 y los rellenos izquierdo y 
        derecho son 2, el ancho del contenido seria 71 
        (77 - 2 - 2 - 2 = 71).

        Returns:
            int: El tamaño del contenido interno en columnas.

        Examples:

            >>> margen = Margen()
            >>> margen.izquierdo = 1
            >>> margen.derecho = 1
            >>> componente = Componente(Estilo(margen=margen))
            >>> componente.relleno.izquierdo
            2
            >>> componente.relleno.derecho
            2
            >>> componente.calcular_ancho_borde()
            77
            >>> componente.calcular_ancho_contenido()
            71
        """
        return (self.calcular_ancho_borde() 
                - self.relleno.izquierdo 
                - self.relleno.derecho - 2)

    def _generar(self) -> Generator[str, str, None]:
        """Genera el componente (Se implementa en otras clases).

        Yields:
            str: El siguiente caracter de la cadena de texto a 
                mostrar en el componente.

        Example:
            Cada subclase implementa ``_generar()``::

                SubclaseA._generar()
                SubclaseB._generar()
                SubclaseC._generar()
        """
        raise NotImplemented()

    def _horizontal_interno(self) -> str:
        """Bordes horizontales internos.
        
        Returns:
            str: Caracteres horizontales internos.
        """
        return u"{}".format(
            self.borde.horizontal * (self.calcular_ancho_borde() - 2)
            )

    def _horizontal_externo(self) -> str:
        """Bordes horizontales externos.
        
        Returns:
            str: Caracteres horizontales externas.
        """
        return u"{}".format(
            self.borde.horizontal * (self.calcular_ancho_borde() - 2)
            )

    def _horizontal_interno_borde(self) -> str:
        """Seccion completa de lineas horizontales internas.

        Incluye ambos bordes verticales.

        Returns:
            str: El borde horizontal completo.
        """
        return u"{margen}{v_izquierdo}{horizontal}{v_derecho}".format(
            margen=" " * self.margen.izquierdo,
            v_izquierdo=self.borde.vertical_izquierdo,
            horizontal=self._horizontal_interno(),
            v_derecho=self.borde.vertical_derecho,
        )

    def _horizontal_externo_borde_inferior(self) -> str:
        """Seccion completa de bordes exteriores inferiores.
        
        Incluye ambos bordes verticales.

        Returns:
            str: El borde inferior completo del menu.
        """
        return u"{margen}{v_izquierdo}{horizontal}{v_derecho}".format(
            margen=" " * self.margen.izquierdo,
            v_izquierdo=self.borde.inferior_izquierdo,
            horizontal=self._horizontal_interno(),
            v_derecho=self.borde.inferior_derecho,
        )
    
    def _horizontal_externo_borde_superior(self) -> str:
        """Seccion completa de bordes exteriores superiores.
        
        Incluye ambos bordes verticales.

        Returns:
            str: El borde superior completo del menu.
        """
        return u"{margen}{v_izquierdo}{horizontal}{v_derecho}".format(
            margen=" " * self.margen.izquierdo,
            v_izquierdo=self.borde.superior_izquierdo,
            horizontal=self._horizontal_interno(),
            v_derecho=self.borde.superior_derecho,
        )

    def _fila(
        self, 
        contenido: str = "", 
        alineacion: str = "izquierda",
    ) -> str:
        """Una fila del menu.

        Returns:
            str: Una fila del componente incluyendo su contenido.
        """
        return u"{margen}{vertical}{contenido}{vertical}".format(
            margen=" " * self.margen.izquierdo,
            vertical=self.borde.vertical,
            contenido=self._contenido(contenido, alineacion),
        )
    
    @staticmethod
    def _alineacion(alineacion: str) -> str:
        if str(alineacion).strip() == "centrada":
            return "^"
        elif str(alineacion).strip() == "derecha":
            return ">"
        else:
            return "<"

    def _contenido(
        self, 
        contenido: Optional[str] = "", 
        alineacion: Optional[str] = "izquierda"
    ) -> str:
        return u"{relleno_izq}{text:{alineacion}{ancho}}{relleno_der}".format(
            relleno_izq=" " * self.relleno.izquierdo,
            relleno_der=" " * self.relleno.derecho,
            text=contenido,
            alineacion=self._alineacion(alineacion),
            ancho=(
                self.calcular_ancho_borde() 
                - self.relleno.izquierdo
                - self.relleno.derecho - 2
                ),
        )


class Encabezado(Componente):
    """Encabezado del menu.

    Las alineaciones disponibles son: 'centrada', 'izquierda' y 
    'derecha'.

    Args:
        estilo (Estilo): Estilo del componente.
        dimension_max (Dimension, optional): Dimension maxima del 
            componente.
        titulo (str, optional): Titulo del encabezado.
        titulo_alineacion (str, optional): Alineacion del titulo.
        subtitulo (str, optional): Subtitulo del encabezado.
        subtitulo_alineacion (str, optional): Alineacion del subtitulo.
        inferior (bool): Si es verdadero, muestra el borde inferior, 
            por defecto es falso.

    Raises:
        TypeError: Si alguna de las alineaciones no es la correcta.

    Example:

        >>> e = Estilo()
        >>> d = Dimension(40, 20)
        >>> encabezado = Encabezado(e, d, titulo="ProtoTools")
        >>> for s in _generar(encabezado): print(s)
        ┌─────────────────────────────────┐
        │                                 │
        │  ProtoTools                     │
        │                                 │
    """
    def __init__(
        self, 
        estilo: Estilo, 
        dimension_max: Optional[Dimension] = None,
        titulo: Optional[str] = None,
        titulo_alineacion: Optional[str] = None,
        subtitulo: Optional[str] = None,
        subtitulo_alineacion: Optional[str] = None,
        inferior: bool = False,
    ) -> None:
        super().__init__(estilo, dimension_max=dimension_max)
        self.titulo = titulo
        self.subtitulo = subtitulo
        self.subtitulo_alineacion = subtitulo_alineacion
        self.inferior = inferior
        if titulo_alineacion is None:
            self.titulo_alineacion = "centrada"
        elif titulo_alineacion not in ("centrada", "izquierda", "derecha"):
            raise TypeError(
                f"La alineacion debe de ser una de las siguientes opciones: "
                f"centrada, izquierda o derecha"
                )
        else:
            self.titulo_alineacion = titulo_alineacion


    def _generar(self):
        for x in range(self.margen.superior):
            yield ""
        yield self._horizontal_externo_borde_superior()
        for x in range(self.relleno.superior):
            yield self._fila()
        if self.titulo is not None and self.titulo != "":
            yield self._fila(
                contenido=self.titulo, 
                alineacion=self.titulo_alineacion,
                )
        if self.subtitulo is not None and self.subtitulo != "":
            yield self._fila()
            yield self._fila(
                contenido=self.subtitulo, 
                alineacion=self.subtitulo_alineacion,
                )
        for x in range(self.relleno.inferior):
            yield self._fila()
        if self.inferior:
            yield self._horizontal_interno_borde()


class Pie(Componente):
    """Seccion de pie del menu.

    La seccion de pie del menu contiene el borde inferior del menu,
    bordes verticales, rellenos inferiores y el margen inferior.

    Example:

        >>> d = Dimension(40, 20)
        >>> e = Estilo()
        >>> pie = Pie(e, d)
        >>> for s in _generar(pie): print(s)
        │                                 │
        └─────────────────────────────────┘
    """
    def _generar(self) -> Generator[str, str, None]:
        for _ in range(self.relleno.superior):
            yield self._fila()
        yield self._horizontal_externo_borde_inferior()
        for _ in range(self.margen.inferior):
            yield ""


class Texto(Componente):
    """Seccion para mostrar el texto del menu.

    Bloque que puede ser usado para mostrar texto al usuario en la 
    parte superior o inferior de la seccion de elementos.

    Args:
        estilo (Estilo): Estilo para el componente.
        dimension_max (Dimension, optional): Dimension maxima del 
            componente.
        texto (str, optional): Texto a mostrar en el bloque de la 
            seccion.
        alineacion (str): Por defecto la alineacion es 'izquierda'.
        superior (bool, optional): Si es verdadero, muestra el borde 
            superior, por defecto es falso.
        inferior (bool, optional): Si es verdadero, muestra el borde
            inferior, por defecto es falso.

    Example:

        >>> e = Estilo()
        >>> texto = 'Esta es la seccion de texto...'
        >>> t = Texto(e, texto=texto)
        >>> for s in t._generar(): print(s)
        │                                                            │
        │  Esta es la seccion de texto...                            │
        │                                                            │
    """
    def __init__(
        self, 
        estilo: Estilo, 
        dimension_max: Optional[Dimension] = None,
        texto: Optional[str] = None,
        alineacion: str = "izquierda",
        superior: Optional[bool] = False,
        inferior: Optional[bool] = False,
    ) -> None:
        super().__init__(estilo, dimension_max=dimension_max)
        self.texto = texto
        self.alineacion = alineacion
        self.superior = superior
        self.inferior = inferior

    def _generar(self) -> Generator[str, str, None]:
        if self.superior:
            yield self._horizontal_interno_borde()
        for _ in range(self.relleno.superior):
            yield self._fila()
        if self.texto is not None and self.texto != "":
            for linea in textwrap.wrap(
                self.texto, width=self.calcular_ancho_contenido()
                ):
                yield self._fila(contenido=linea, alineacion=self.alineacion)
        for _ in range(self.relleno.inferior):
            yield self._fila()
        if self.inferior:
            yield self._horizontal_interno_borde()


class Elementos(Componente):
    """Seccion del menu para mostrar las opciones del menu (elementos).

    Args:
        estilo (Estilo): Estilo para el componente.
        dimension_max (Dimension, optional): Dimension maxima del 
            componente.
        elementos (str, optional): Elementos de la seccion.
        alineacion (str): Por defecto la alineacion es 'izquierda'.

    Example:
        Script::

            e1 = Elemento("Estado de Cuenta")
            e2 = Elemento("Transacciones")

            elementos = Elementos(Estilo(), elementos=(e1, e2))
            for s in elementos._generar():
                print(s)

        Output::

            │                                                         │
            │  1 - Transacciones                                      │
            │  2 - Estado                                             │
            │                                                         │
    """
    def __init__(
        self,
        estilo: Estilo,
        dimension_max: Optional[Dimension] = None,
        elementos = None,
        alineacion: str = "izquierda",
    ) -> None:
        super().__init__(estilo, dimension_max=dimension_max)
        if elementos is not None:
            self._elementos = elementos
        else:
            self._elementos = list()
        self.alineacion = alineacion
        self._borde_superior = dict()
        self._borde_inferior = dict()

    @property
    def elementos(self):
        """Elementos del componente."""
        return self._elementos

    @elementos.setter
    def elementos(self, elementos):
        self._elementos = elementos

    @property
    def elementos_borde_inferior(self):
        """
        Retorna una lista de nombres de todos los elementos que 
        deberian mostrar un borde inferior.

        Returns:
            Lista de nombres que deberian mostrar un borde inferior.
        """
        return self._borde_inferior.keys()

    @property
    def elementos_borde_superior(self):
        """
        Retorna una lista de nombres de todos los elementos que 
        deberian mostrar un borde superior.

        Returns:
            Lista de nombres que deberian mostrar un borde superior.
        """
        return self._borde_superior.keys()

    def mostrar_elemento_borde_inferior(self, texto: str, flag: bool):
        """Coloca un flag que mostrara el borde inferior por un 
        elemento con el texto especifico.

        Args:
            texto (str): Texto del elemento.
            flag (bool): Booleano especificando si el borde se 
                mostrara.
        """
        if flag:
            self._borde_inferior[texto] = True
        else:
            self._borde_inferior.pop(texto, None)

    def mostrar_elemento_borde_superior(self, texto: str, flag: bool):
        """Coloca un flag que mostrara el borde superior por un 
        elemento con el texto especifico.

        Args:
            texto (str): Texto del elemento.
            flag (bool): Booleano especificando si el borde se mostrara.
        """
        if flag:
            self._borde_superior[texto] = True
        else:
            self._borde_superior.pop(texto, None)

    def _generar(self) -> Generator[str, str, None]:
        for _ in range(self.relleno.superior):
            yield self._fila()
        for indice, elemento in enumerate(self.elementos):
            if elemento.texto in self.elementos_borde_superior:
                yield self._horizontal_interno_borde()
            yield self._fila(
                contenido=elemento.mostrar(indice), 
                alineacion=self.alineacion,
                )
            if elemento.texto in self.elementos_borde_inferior:
                yield self._horizontal_interno_borde()
        for _ in range(self.relleno.superior):
            yield self._fila()


class Elemento:
    """Elemento generico del menu.

    Args: 
        texto (str): Texto del elemento.
        menu (object, optional): Menu al que pertenece el elemento.
        salir (bool, optional): Ya sea si el menu debería salir una 
            vez que la accion del elemento haya concluido.

    Example:

        >>> e1 = Elemento("Enviar archivos")
        >>> e2 = Elemento("Archivos enviados")
        >>> e3 = Elemento("Archivos recibidos") 
    """
    def __init__(
        self, 
        texto: str, 
        menu: Optional[object] = None, 
        salir: Optional[bool] = False,
    ) -> None:
        self.texto = texto
        self.menu = menu
        self.salir = salir

    def __str__(self) -> str:
        return f"{self.menu.obtener_titulo()} {self.obtener_texto()}"

    def __eq__(self, o: object) -> bool:
        return (
            self.texto == o.texto and self.menu == o.menu and
            self.salir == o.salir)

    def configurar(self):
        """Acciones de configuracion necesarias para el elemento.
        
        Necesita ser sobreescrito.
        """
        pass

    def accion(self):
        """Accion principal del elemento.
        
        Necesita ser sobreescrito.
        """
        pass

    def limpiar(self):
        """Limpieza de acciones necesarias para el elemento.
        
        Necesita ser sobreescrito.
        """
        pass

    def obtener_retorno(self):
        """Retorno del valor del elemento.
        """
        pass

    def obtener_texto(self):
        """Obtener el texto del elemento"""
        return self.texto() if callable(self.texto) else self.texto

    def mostrar(self, indice: int) -> str:
        """Como se mostrara el elemento en el menu.
        
        Por defecto::

            1 - Elemento
            2 - Otro elemento

        Args:
            indice (int): Indice del elemento en la lista de elementos.
        """
        return f"{indice + 1} - {self.obtener_texto()}"


class Salir(Elemento):
    """Representacion de la opcion 'salir'.

    Args:
        text (str): Texto a mostrar, por defecto 'Salir'.
    """
    def __init__(self, texto: str = "Salir", menu: str = None) -> None:
        super().__init__(texto, menu=menu, salir=True)

    def mostrar(self, indice):
        """
        """
        if self.menu and self.menu.parent and self.obtener_texto() == "Salir":
            self.texto = f"Regresar al {self.menu.parent.obtener_titulo()}"
        return super().mostrar(indice)
    

class Entrada(Componente):
    """Representacion de la entrada del menu para el usuario.

    Args:
        estilo (Estilo): Estilo para el componente.
        dimension_max (Dimension, optional): Dimension maxima del 
            componente.
        indicacion (str, optional): Indicacion a mostrar en el 
            componente.

    Note:

        La indicación `Opcion:` (del ejemplo) se genera en una línea más 
        abajo como se puede apreciar en la salida del script de ejemplo.

    Example:
        Script::

            d = Dimension(40, 20)
            e = Estilo()
            entrada = Entrada(e, d, indicacion="Opcion: ")
            for s in _generar(entrada): print(s)

        Output::
        
            >>> 

            Opcion:
    """
    def __init__(
        self, 
        estilo: Estilo, 
        dimension_max: Optional[Dimension] = None, 
        indicacion: Optional[str] = ">>> ", 
    ) -> None:
        super().__init__(estilo, dimension_max=dimension_max)
        self._indicacion = indicacion

    @property
    def indicacion(self):
        """Indicacion de la entrada"""
        return self._indicacion

    @indicacion.setter
    def indicacion(self, indicacion):
        self._indicacion = indicacion

    def _generar(self) -> Generator[str, str, None]:
        for _ in range(self.relleno.superior):
            yield ""
        for linea in self.indicacion.split():
            yield u"{margen}{linea}".format(
                margen=" " * self.margen.izquierdo,
                linea=linea,
            )