import random

#random password generator
def get_random_password(min_length :'Longitud minima' = 8, max_length :'Longitud maxima' = 8, numbers :'Incluye Numeros?' = True, letters :'Incluye Letras?' = True, special_characters :'Incluye caracteres especiales?' = True, caps :'Usar Mayusculas?' = True) -> str:
    if min_length > max_length:
        max_length = min_length

    if numbers == False and letters == False and special_characters == False:
        return "RG0 : Necesitas al menos un parametro activo - 'numbers', 'letters', 'symbols' "
    elif  min_length <= 0 or max_length <= 0:
        return "RG1 : La longitud debe ser mayor a cero"


    _numbers = []
    _letters = []
    _symbols = []
    _caps = []
    
    if numbers == True:
        _numbers = list("1234567890")
    elif numbers == False:
        _numbers == list("")

    if letters == True:
        _letters = list("abcdefghijklmnñopqrstuvwyz")
    elif letters == False:
        _letters == list("")

    if special_characters == True:
        symbols = list("~!@#$%^&*()_+-=[]{}|;:<>,./")
    elif special_characters == False:
        symbols == list("")

    if caps == True:
        _caps = list("ABCDEFGHIJKLMNÑOPQRSTUVWXYZ")
    elif caps == False or _letters == False:
        _caps = list("")

    all_chars = _numbers + _letters + symbols + _caps

    #generate random password
    password = []
    for i in range(random.randint(min_length, max_length)):
        password.append(all_chars[random.randint(0, len(all_chars)-1)])
    
    password = ''.join(password)
    return password

def get_random_number_list(min_length :'Longitud minima' = 8, max_length: 'Longitud maxima' = 8, floats :'Usar flotantes?' = False, negatives :'Usar numeros negativos?' = False, binary :'Usar solo numeros del 1 al 0?' = False, round : 'Redondeamiento de los flotantes' = 2) -> list:
    if min_length > max_length:
        max_length = min_length
        
    #error check
    if min_length <= 0 or max_length <= 0:
        return "RG1 : La longitud debe ser mayor a cero"

    #generate random list
    if binary == True:
        if floats == True:
            if negatives == True:
                # list with only -1 to 1 floats
                lista  = [random.random()*random.randint(-1, 1) for i in range(random.randint(min_length, max_length))]
                lista = [round(elem, 2) for elem in lista]
                return lista
            else:
                # list with only 0 to 1 floats
                lista = [random.random()*random.randint(0, 1) for i in range(random.randint(min_length, max_length))]
                lista = [round(elem, 2) for elem in lista]
                return lista
            
        else:
            if negatives == True:
                # list with only -1 to 1 integers
                return [random.randint(-1, 1) for i in range(random.randint(min_length, max_length))]
            else:
                # list with only 0 to 1 integers
                return [random.randint(0, 1) for i in range(random.randint(min_length, max_length))]
        
    else:
        if floats == True:
            if negatives == True:
                # list with only -9.0 to 9.o floats
                lista = [random.uniform(-9.0, 9.0) for i in range(random.randint(min_length, max_length))]
                lista = [round(elem, 2) for elem in lista]
                return lista
            
            else:
                # list with only 0 to 9 floats
                lista = [random.uniform(0, 9) for i in range(random.randint(min_length, max_length))]
                lista = [round(elem, 2) for elem in lista]
                return lista
            
        else:
            if negatives == True:
                # list with only -9 to 9 integers
                return [random.randint(-9, 9) for i in range(random.randint(min_length, max_length))]

            else:
                # list with only 0 to 9 integers
                return [random.randint(0, 9) for i in range(random.randint(min_length, max_length))]
        
