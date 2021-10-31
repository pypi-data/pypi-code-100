import re

def check_error(ErrorCode):
    pattern = r"^[A-Z][A-Z]([0-9])+$"

    if re.match(pattern, ErrorCode):
        return True
    else:
        return False

def help(ErrorCode):
    if not check_error(ErrorCode):
        return "EH0 : Codigo de error invalido"
    
    code_name = ErrorCode[0:2]
    code_num = int(ErrorCode[2:])
    error_help = ""

    try:
        if code_name == "EH":
            error_help = EH.get(code_num)

        elif code_name == "SP":
            error_help = SP.get(code_num)
        
        elif code_name == "RG":
            error_help = RG.get(code_num)

    except:
        return "EH0 : Codigo de error invalido"
    
    else:
        print(error_help)
        return 0


EH = {
    0 : "Codigo de error invalido. Ocurre cuando usas un codigo de error inexistente o mal-escritos en la funcion help."
}

RG = {
    0 : "Necesitas al menos un parametro activo - 'numbers', 'letters', 'symbols'. Ocurre cuando todos los parametros al generar una contraseña aleatoria son 'False'",
    1 : "La longitud debe ser mayor a cero . Ocurre cuando la longitud al crear una contraseña es 0"
}

SP = {
    0 : "Necesitas el link de la playlist. Ocurre cuando el link que estas usando no es de una playlist de Spotify"
}
