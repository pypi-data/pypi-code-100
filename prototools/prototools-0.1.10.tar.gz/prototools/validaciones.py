from os import error
from typing import Any, Optional, Sequence, Union
import collections.abc

SEQUENCE_ABC = collections.abc.Sequence

class _ValidacionExcepcion(Exception):
    """Clase base para excepciones 
    
    Son lanzadas cuando las funciones son usadas de forma incorrecta. 
    No representa un falla de validación.
    """
    pass


def _excepcion(standard: str, custom: Optional[str] = None) -> None:
    """Se eleva una excepción con un mensaje estándar si no se provee 
    un mensaje personalizado.

    Args:
        standard: Mensaje de excepción.
        custom: Mensaje personalizado.
    
    Raises:
        ValidacionExcepcion: Si no se llega a validar.
    """
    if custom is None:
        raise _ValidacionExcepcion(str(standard))
    else:
        raise _ValidacionExcepcion(str(custom))

def _valor_strip(valor: str, strip: Union[None, str, bool]) -> str:
    """Retorna el valor aplicando el metodo strip()

    Args:
        valor (str): valor.
        strip (None, str, bool, optional): si es None, los espacios en
            blancos son removidos; si es una cadena de texto, los
            caracteres de la cadena son removidos; si es Falso, no se
            remueve nada. 
    """
    if strip is None:
        valor = valor.strip()
    elif isinstance(strip, str):
        valor = valor.strip(strip)
    elif strip is False:
        pass
    return valor


def _pre_validacion(
    valor: str, 
    vacio: bool, 
    strip: Union[None, str, bool],
) -> tuple:
    """Pre validación que se ejecuta en otras funciones.

    Args:
        valor (str): Valor a pre-validar.
        vacio (bool): Si es verdadero, permite el ingreso de valores 
            vacíos.
        strip (None, str, bool): metodo strip().

    Returns:
        Tuple (vacio, valor).

    Raises:
        _excepcion: Si existen valores vacíos y vacío es False.
    """
    valor = str(valor)
    valor = _valor_strip(valor, strip)

    if not vacio and valor == "":
        _excepcion("No se permiten valores en blanco.")
    elif vacio and valor == "":
        return True, valor
    return False, valor

def _validar_parametros_genericos(
    vacio: bool, 
    strip: Union[None, str, bool],
) -> None:
    """Se validan los parámetros genéricos presentes en otras 
    funciones.

    Args:
        vacio (bool): Si es verdadero, permite el ingreso de valores vacíos.
        strip (None, str, bool): metodo strip().

    Raises:
        _ValidacionExcepcion: Si alguno de sus argumentos son 
            inválidos.

    Todo:
        Incluir más parámetros genéricos.
    """
    if not isinstance(vacio, bool):
        raise _ValidacionExcepcion("El argumento debe ser de tipo bool.")
    if not isinstance(strip, (type(None), bool, str)):
        raise _ValidacionExcepcion("El argumento strip debe ser bool, str o None.")

def _validar_parametros_numeros(
    min: Optional[Union[int, float, None]] = None, 
    max: Optional[Union[int, float, None]] = None, 
    menor: Optional[Union[int, float, None]] = None, 
    mayor: Optional[Union[int, float, None]] = None,
) -> None:
    """Validación de los parámetros cuando estos son numéricos.

    Se usa en las funciones validar_numero(), validar_int(), 
    validar_float() para validar sus argumentos.

    Args:
        min (int, float, None, optional): Valor mínimo.
        max (int, float, None, optional): Valor máximo.
        menor (int, float, None, optional): Límite mínimo para el 
            valor.
        mayor (int, float, None, optional): Límite máximo para el 
            valor.

    Raises:
        _ValidacionExcepcion: Si uno de los argumentos no pasa la 
            validación.
    """
    if (min is not None) and (mayor is not None):
        raise _ValidacionExcepcion(
            "Solo un argumento para mínimo o mayor",
            "puede ser pasado, no ambos.",
            )
    if (max is not None) and (menor is not None):
        raise _ValidacionExcepcion(
            "Solo un argumento para máximo o menor", 
            "puede ser pasadao, no ambos.",
            )
    if (min is not None) and (max is not None) and (min > max):
        raise _ValidacionExcepcion(
            "El argumento mínimo debe ser menor o igual", 
            "que el argumento para el máximo.",
            )
    if (min is not None) and (menor is not None) and (min >= menor):
        raise _ValidacionExcepcion(
            "El argumento mínimo debe ser menor", 
            "que el argumento para el máximo.",
            )
    if (max is not None) and (mayor is not None) and (max <= mayor):
        raise _ValidacionExcepcion(
            "El argumento máximo debe ser mayor", 
            "que el argumento para el mínimo.",
            )

    for nombre, valor in (
        ("min", min), 
        ("max", max), 
        ("menor", menor),
        ("mayor", mayor),
        ):
        if not isinstance(valor, (int, float, type(None))):
            raise _ValidacionExcepcion(
                f"El parametro {nombre} debe ser de tipo int, float o None."
                )

def validar_str(
    valor: str, 
    vacio: Optional[bool] = False, 
    strip : Union[bool, str, None] = None,
) -> str:
    """Validación de cadenas de texto.

    Args:
        valor (str): Cadena de texto a validar.
        vacio (bool, optional): Si es verdadero, permite el ingreso de 
            valores vacíos, por defecto es falso.
        strip (bool, str, None, optional): metodo strip a aplicar.

    Returns:
        str: Cadena de texto.

    Raises:
        _ValidacionExcepcion: Si el valor no es una cadena de texto.

    Examples:

        >>> from prototools.validaciones import validar_str
        >>> validar_str('python')
        python
        >>> validar_str('  rust')
        rust
        >>> validar_str('')
        Traceback (most recent call last):
            ...
        prototools._ValidacionException: No se permiten valores en 
        blanco.
    """
    _validar_parametros_genericos(vacio=vacio, strip=strip)
    _, valor = _pre_validacion(valor, vacio, strip)
    return valor

def _validar_numero(
    valor, 
    vacio: Optional[bool] = False,
    strip: Union[None, str, bool] = None,
    tipo: Optional[str] = "num", 
    min: Optional[Union[int, float , None]] = None, 
    max: Optional[Union[int, float , None]] = None, 
    menor: Optional[Union[int, float , None]] = None, 
    mayor: Optional[Union[int, float , None]] = None, 
    custom: Optional[str] = None,
) -> Union[int, str, float]:
    """Validación de numéros.

    Args:
        valor: Valor a ser validado.
        vacio: Si es verdadero, permite el ingreso de valores vacíos,
            por defecto es falso.
        strip: Si es None, los espacios en blanco son removidos.
        tipo: Tipo de número (num, int o float).
        min: Valor mínimo (inclusivo) para pasar la validación.
        max: Valor máximo (inclusivo) para pasar la validación.
        menor: Valor mínimo (excluyente) para pasar la validación.
        mayor: Valor máximo (excluyente) para pasar la validación.
        custom: Mensaje de error personalizado.
    
    Returns:
        Valor numérico.

    Raises:
        _excepcion: Si el valor no es int o float.

    Examples:

        >>> from prototools.validaciones import validar_numero
        >>> validar_numero('3')
        3
        >>> validar_numero('3.0')
        3.0
        
    """
    assert tipo in ("num", "int", "float")

    _validar_parametros_genericos(vacio=vacio, strip=strip)
    _validar_parametros_numeros(min=min, max=max, menor=menor, mayor=mayor)
    
    retorno, valor = _pre_validacion(valor, vacio, strip)

    if retorno:
        if (tipo == "num" and "." in valor) or (tipo == "float"):
            try:
                return float(valor)
            except ValueError:
                return valor
        elif (tipo == "num" and "." not in valor) or (tipo == "int"):
            try:
                return int(valor)
            except ValueError:
                return valor
        else:
            assert False
    
    if tipo == "num" and "." in valor:
        try:
            valor_numerico = float(valor)
        except:
            _excepcion(f"{valor} no es un número.", custom)
    elif tipo == "num" and "." not in valor:
        try:
            valor_numerico = int(valor)
        except:
            _excepcion(f"{valor} no es un número.", custom)
    elif tipo == "float":
        try:
            valor_numerico = float(valor)
        except:
            _excepcion(f"{valor} no es un flotante.", custom)
    elif tipo == "int":
        try:
            if float(valor) % 1 != 0:
                _excepcion(f"{valor} no es un entero.", custom)
            valor_numerico = int(float(valor))
        except:
            _excepcion(f"{valor} no es un entero", custom)
    else:
        assert False
    
    if min is not None and valor_numerico < min:
        _excepcion(f"El número mínimo debe ser {min}", custom)

    if max is not None and valor_numerico > max:
        _excepcion(f"El número máximo debe ser {max}", custom)

    if menor is not None and valor_numerico >= menor:
        _excepcion(f"El número debe ser menor que {menor}", custom)
        
    if mayor is not None and valor_numerico <= mayor:
        _excepcion(f"El número debe ser mayor que {mayor}", custom)

    return valor_numerico

def validar_int(
    valor: str, 
    vacio: Optional[bool] = False, 
    min: Optional[Union[int, float , None]] = None,  
    max: Optional[Union[int, float , None]] = None, 
    menor: Optional[Union[int, float , None]] = None,  
    mayor: Optional[Union[int, float , None]] = None,  
    custom: Optional[str] = None,
) -> int:
    """Validación de números enteros.
    
    Args:
        valor: Valor entero a ser validado.
        vacio: Si es verdadero, permite el ingreso de valores vacíos,
            por defecto es falso.
        min: Valor mínimo (inclusivo) para pasar la validación.
        max: Valor máximo (inclusivo) para pasar la validación.
        menor: Valor mínimo (excluyente) para pasar la validación.
        mayor: Valor máximo (excluyente) para pasar la validación.
        custom: Mensaje de error personalizado.
    
    Returns:
        int: Valor numérico entero.

    Raises:
        _ValidacionExcepcion: Si el valor no es un entero.

    Examples:

        >>> from prototools.validaciones import validar_int
        >>> validar_int(2)
        2
        >>> validar_int('8')
        8
        >>> validar_int('A4')
        Traceback (most recent call last):
            ...
        prototools._ValidacionException: A4 no es un entero.
    """
    return _validar_numero(
        valor=valor, 
        vacio=vacio, 
        tipo="int", 
        min=min, 
        max=max, 
        menor=menor, 
        mayor=mayor, 
        custom=custom,
    )

def validar_float(
    valor: str, 
    vacio: Optional[bool] = False, 
    min: Optional[Union[int, float , None]] = None,  
    max: Optional[Union[int, float , None]] = None, 
    menor: Optional[Union[int, float , None]] = None,  
    mayor: Optional[Union[int, float , None]] = None,  
    custom: str = None,
) -> float:
    """Validación de números flotantes.
    
    Args:
        valor: Valor flotante a ser validado.
        vacio: Si es verdadero, permite el ingreso de valores vacíos,
            por defecto es falso.
        min: Valor mínimo (inclusivo) para pasar la validación.
        max: Valor máximo (inclusivo) para pasar la validación.
        menor: Valor mínimo (excluyente) para pasar la validación.
        mayor: Valor máximo (excluyente) para pasar la validación.
        custom: Mensaje de error personalizado.
    
    Returns:
        float: Valor numérico flotante.

    Raises:
        _ValidacionExcepcion: Si el valor no es un flotante.

    Examples:

        >>> from prototools.validaciones import validar_float
        >>> validar_float(1)
        1.0
        >>> validar_float(1.4)
        1.4
        >>> validar_float(-13)
        -13.0
        >>> validar_float('pi')
        Traceback (most recent call last):
            ...
        prototools._ValidacionException: pi no es un flotante.
    """
    return _validar_numero(
        valor=valor, 
        vacio=vacio, 
        tipo="float", 
        min=min, 
        max=max, 
        menor=menor, 
        mayor=mayor, 
        custom=custom,
    )

def validar_si_no(
    valor: str,
    vacio: Optional[bool] = False,
    si: Optional[str] = "si",
    no: Optional[str] = "no",
    sensible: Optional[bool] = False,
    custom: Optional[str] = None,
):
    """Validación para entradas si y no.

    Args:
        valor: Valor a ser validado.
        vacio: Si es verdadero, permite el ingreso de valores vacios,
            por defecto es falso.
        si: Valor de la respuesta afirmativa, por defecto 'si'.
        no: Valor de la respuesta negativa, por defecto 'no'.
        sensible: Si es verdadero, distingue entre mayúsculas y 
            minúsculas.
        custom: Mensaje de error personalizado.
    
    Returns:
        El argumento del parámetro 'si' o 'no', no el valor.

    Raises:
        ValidacionExcepcion: Si el valor no es una respuesta si o no.

    Examples:

        >>> from prototools.validaciones import validar_si_no
        >>> validar_si_no('s')
        'si'
        >>> validar_si_no('si')
        'si'
        >>> validar_si_no('no')
        'no'
        >>> validar_si_no('Ok', si='ok', no='nope')
        'ok'
    """
    _validar_parametros_genericos(vacio=vacio)
    retorno, valor = _pre_validacion(valor, vacio)

    if retorno:
        return valor
    
    si = str(si)
    no = str(no)

    if len(si) == 0:
        raise _ValidacionExcepcion(
            "El argumento de 'si' no debe estar vacío."
            )
    if len(no) == 0:
        raise _ValidacionExcepcion(
            "El argumento de 'no' no debe esta vacío."
            )
    if (si == no) or (not sensible and si.upper() == no.upper()):
        raise _ValidacionExcepcion(
            "Los argumentos 'si' y 'no' deben ser diferentes."
            )
    if (si[0] == no[0]) or (not sensible and si[0].upper() == no[0].upper()):
        raise _ValidacionExcepcion(
            "Los primeros caracteres de 'si' y 'no' deben ser diferentes."
            )

    retorno, valor = _pre_validacion(valor, vacio)

    if retorno:
        return valor
    
    if sensible:
        if valor in (si, si[0]):
            return si
        elif valor in (no, no[0]):
            return no
    else:
        if valor.upper() in (si.upper(), si[0].upper()):
            return si
        elif valor.upper() in (no.upper(), no[0].upper()):
            return no

    _excepcion(f"{valor} no es una opción válida", custom)

    mensaje = (
        "La ejecución alcanzo este punto,",
        "a pesar que la línea previa elevó una excepción"
    )
    assert False, mensaje

def _validar_parametros_choice(
    choices: Sequence[Any],
    vacio: bool = False,
    strip: Union[None, str, bool] = None,
    numerado: bool = False,
    letrado: bool = False,
    sensitive: bool = False,
) -> None:

    if not isinstance(sensitive, bool):
        raise _ValidacionExcepcion("El argumento 'sensitive' debe ser de tipo bool.")
    if not isinstance(choices, SEQUENCE_ABC):
        raise _ValidacionExcepcion("El argumento 'choices' deber ser una secuencia.")
    
    try:
        len(choices)
    except:
        raise _ValidacionExcepcion("El argumento 'choices' debe ser una secuencia.")
    if vacio == False and len(choices) < 2:
        raise _ValidacionExcepcion("'choices' debe tener al menos dos elementos si 'vacio' es falso.")
    elif vacio == True and len(choices) < 1:
        raise _ValidacionExcepcion("'choices' debe por lo menos tener un elemnto.")

    _validar_parametros_genericos(vacio=vacio, strip=strip)

    if letrado and len(choices) > 26:
        raise _ValidacionExcepcion("El argumento 'letrado' no puede ser 'True' si hay mas de 26 opciones.")
    if letrado and numerado:
        raise _ValidacionExcepcion("Los argumentos 'letrado' y 'numerado' no pueden ser al mismo tiempo 'True'.")
    if len(choices) != len(set(choices)):
        raise _ValidacionExcepcion("Entradas duplicadas en el argumento 'choices'")
    if not sensitive and len(choices) != len(set([choice.upper() for choice in choices])):
        raise _ValidacionExcepcion("Entradas sensibles duplicadas en el argumento 'choices'")

def validar_choice(
    valor: str,
    choices: Sequence[Any],
    vacio: bool = False,
    strip: Union[None, str, bool] = None,
    numerado: bool = False,
    letrado: bool = False,
    sensitive: bool = False,
) -> str:
    """Valida una serie de opciones.

    Args:
        valor (str): El valor a ser validado.
        choices (Sequence[Any]): Opciones.
        vacio (bool): Si es verdadero, permite el ingreso de valores 
            vacíos.
        strip (None, str, bool): metodo strip().
        numerado (bool): Si es 'True', tambien se aceptan numeros, 
            ej: '1' o '2'.
        letrado (bool): Si es 'True', tambien se aceptan letras, 
            ej: 'A' o 'B' o 'a' o 'b'.
        sensitive (bool): Si es 'True', distingue entre mayúsculas y 
            minúsculas.
    """
    _validar_parametros_choice(
        choices=choices,
        vacio=vacio,
        strip=strip,
        numerado=numerado,
        letrado=letrado,
        sensitive=sensitive,
    )

    choices_ = [str(choice) for choice in choices]
    
    if "" in choices_:
        vacio = True

    retorno, valor = _pre_validacion(valor, vacio, strip)
    
    if retorno:
        return valor
    if valor in choices_:
        return valor
    if numerado and valor.isdigit() and 0 < int(valor) <= len(choices_):
        return choices_[int(valor) - 1]
    if letrado and len(valor) == 1 and valor.isalpha() and 0 < ord(valor.upper()) - 64 <= len(choices_):
        return choices_[ord(valor.upper()) - 65]
    if not sensitive and valor.upper() in [choice.upper() for choice in choices_]:
        return choices_[[choice.upper() for choice in choices_].index(valor.upper())]

    _excepcion("{} no es una opcion valida".format(valor))
    assert False, "..."

def _validar_bool():
    """Validacion de booleanos.
    """
    pass

def _validar_email():
    """Validacion de correo electronico.
    """
    pass

def _validar_url():
    """Validacion de dirrecciones web.
    """
    pass

def _validar_mes():
    """Validacion de mes.
    """
    pass

def _validar_dia():
    """Validacion de dia.
    """
    pass

def validar(indicacion: str, secuencia: SEQUENCE_ABC, error: str = "Opción no válida!"):
    """Validacion simple sin excepciones.

    Args:
        indicacion (str): Texto a mostrar.
        secuencia (Union[list, tuple, dict]): Secuencia de 
            la cual validar.

    Returns:
        str: Valor validado.

    Example:

        >>> from prototools.validaciones import validar
        >>> t = validar('Tamaño: ', ('pequeña', 'mediana', 'familiar'))
        Tamaño: p
        Tamaño: pequeña
        >>> t
        'pequeña'
    """
    while True:
        valor = input(indicacion)
        if valor in secuencia:
            return valor
        else:
            print(error)