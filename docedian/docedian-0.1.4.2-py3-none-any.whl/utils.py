# -*- coding: utf-8 -*-


def compute_vat_vd(rut):
    """
    :param rut(str): rut to check
    
    Obtiene el digito de verificacion de un rut

    :return result(str): vat vd
    """
    result = None
    factores = [3, 7, 13, 17, 19, 23, 29, 37, 41, 43, 47, 53, 59, 67, 71]
    rut_ajustado=str(rut).rjust( 15, '0')
    s = sum(int(rut_ajustado[14-i]) * factores[i] for i in range(14)) % 11
    if s > 1:
        result =  11 - s
    else:
        result = s

    return str(result)