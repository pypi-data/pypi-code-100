import itertools
from typing import *


def ezs_print(content :Any , color:Union[int, str, hex]='white', end : Any ='\n', flush :bool =False, times :int =1, add :Union[int, float] =False, enumerate :bool =False) -> Any :
    # docstring for ezs_print
    """
    Printea un mensaje manipulando algunos parametros.
    color : Color del contenido (int : hexadecimal en int, str : "blue", hex : 0xFF0000)
    end : Caracter de fin de linea
    end : Final del contenido
    flush : Limpiar buffer interno
    times : Veces que se printea
    add : Suma al contenido (para contenido numerico)
    enumerate : Enumerar Las veces que se printea 
    """
    ezs_colors = {
        'red': '\033[91m',
        'green': '\033[92m',
        'yellow': '\033[93m',
        'blue': '\033[94m',
        'magenta': '\033[95m',
        'cyan': '\033[96m',
        'white': '\033[97m',
        'end': '\033[0m',
        'pink' : '\033[95m',
        'orange' : '\033[93m',
        'light_blue' : '\033[94m',
        'brown' : '\033[33m',
        'black' : '\033[30m',
        'gray' : '\033[37m',
        'light_green' : '\033[92m',
        'light_yellow' : '\033[93m',
        'light_magenta' : '\033[95m',
        'light_red': '\033[91m'
    }

    # check if color is hex

    # convert color from string to integer
    if color is not None:
        # check if is a string    
        if isinstance(color, str):
            # check if is a valid color
            if color in ezs_colors:
                color = ezs_colors[color]
                            
            else:
                color = ezs_colors['white']
                            
        # if is not a string, check if is an integer
        elif isinstance(color, int):       
            # convert from integer to hex (0x)
            color = hex(color)
            # remove 0x from hex
            color = color[2:]            
            # convert to rgb
            color = tuple(int(color[i:i+2], 16) for i in (0, 2, 4))
            color = f'\033[38;2;{color[0]};{color[1]};{color[2]}m'
            
    else:
        # set color to white
        color = ezs_colors['white']

    for i in range(times):
        if enumerate:
            print(f'{i+1} - ', end='')
        print(f'{color}{content}{ezs_colors["end"]}', end=end, flush=flush)
        if add != False:
            # if content is numeric, add
            if isinstance(content, int) or isinstance(content, float):
                content += add
                
    return content

# convert all elememnts in a list to a type
def convert_list(lista :list , type : str, exclude :bool =True) -> list:
    # docstring for ezs_convert_list
    """
    Convierte todos los elementos de una lista a un tipo de dato.
    lista : Lista a convertir
    type : Tipo de dato a convertir
    exclude : Eliminar valores que no se pueden convertir?  (True = Eliminar)
    """
    
    valid_types = [int, float, str]
    if type not in valid_types:
        raise TypeError(f'{type} No es un tipo de dato valido para convertir ')
    
    # check if is a list
    if isinstance(lista, list):
        # convert all elements in a list to a specified type
        for i in range(len(lista)):
            try:
                lista[i] = type(lista[i])
            except ValueError:
                if exclude:
                    lista.pop(i)
    else:
        # if is not a list, return error
        raise "F0 : Necesitas Usar una lista"
        
    return lista

# get all possible combinations of a list
def get_all_combinations(lista : list) -> list:
    # docstring for ezs_get_all_combinations
    """
    Obtiene todas las combinaciones posibles de una lista.
    lista : Lista a ser usada
    """
    # check if is a list
    if isinstance(lista, list):
        return list(itertools.product(lista, repeat=len(lista)))
    else:
        # if is not a list, return error
        raise "F0 : Necesitas Usar una lista"


