def ezs_print(content :'contenido' , color:'Color del mensaje' =None, end :'Final del contenido' ='\n', flush :'Limpiar buffer interno' =False, times :'Veces que se printea' =1, add :'Sumar al contenido (para contenido numerico)' =False, enumerate :'Enumerar Las veces que se printea' =False):
    """
    Prints content in a specified color.
    """
    ezs_colors = {
        'red': '\033[91m',
        'green': '\033[92m',
        'yellow': '\033[93m',
        'blue': '\033[94m',
        'magenta': '\033[95m',
        'cyan': '\033[96m',
        'white': '\033[97m',
        'end': '\033[0m'
    }

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
            # check if is a valid color
            if color in ezs_colors.values():
                color = color
            else:
                # set color to white
                color = ezs_colors['white']

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


ezs_print(content=1, end=', ', times=1000, add=1)





