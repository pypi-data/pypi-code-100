# -*- coding: utf-8 -*-


# PaymentMeansCode
# 13.2.11. Medios de Pago: cbc:PaymentMeansCode 
# Código Medio
PaymentMeansCode = {
    '10': '01 - Efectivo',
    '48': '48 - Tarjeta Crédito',
    '49': '49 - Tarjeta Débito',
    '47': '47 - Transferencia Débito Bancaria',
    '42': '42 - Consiganción bancaria',
    '44': '44 - Nota cambiaria',
    '3': '3 - Débito ACH',
    '20': '20 - Cheque',
    '25': '25 - Cheque certificado',
    '23': '23 - Cheque bancario de gerencia',
    '26': '26 - Cheque Local',
    '71': '71 - Bonos',
    '24': '24 - Vales',
    '64': '64 - Nota promisoria firmada pro el banco',
    '61': '61 - Nota promisoria firmada por el acreedor',
    '65': '65 - Nota promisoria firmada por un banco avalada porotro banco',
    '62': '62 - Nota promisoria firmada por el acreedor, avalada por el banco',
    '66': '66 - Nota promisoria firmada ',
    '63': '63 - Nota promisoria firmada por el acreedor, avalada por un tercero',
    '67': '67 - Nota promisoria firmada por un tercero avalada por un banco',
    '60': '60 - Nota promisoria',
    '2': '2 - Crédito ACH',
    '96': '96 - Método de pago solicitado no usuado',
    'ZZZ': 'ZZZ - Otro* ',
    '91': '91 - Nota bancaria transferible',
    '95': '95 - Giro formato abierto',
    '92': '92 - Cheque local transferible',
    '13': '13 - Crédito Ahorro',
    '93': '93 - Giro referenciado',
    '14': '14 - Débito Ahorro',
    '94': '94 - Giro urgente',
    '39': '39 - Crédito Intercambio Corporativo (CTX) ',
    '40': '40 - Débito Intercambio Corporativo (CTX)',
    '4': '4 - Reversión débito de demanda ACH ',
    '41': '41 - Desembolso Crédito plus (CCD+)',
    '5': '5 - Reversión crédito de demanda ACH ',
    '43': '43 - Desembolso Débito plus (CCD+) ',
    '6': '6 - Crédito de demanda ACH ',
    '45': '45 - Transferencia Crédito Bancario ',
    '7': '7 - Débito de demanda ACH ',
    '46': '46 - Transferencia Débito Bancario ',
    '9': '9 - Clearing Nacional o Regional ',
    '50': '50 - Postgiro ',
    '11': '11 - Reversión Crédito Ahorro ',
    '51': '51 - Telex estándar bancario ',
    '12': '12 - Reversión Débito Ahorro ',
    '52': '52 - Pago comercial urgente ',
    '18': '18 - Desembolso (CCD) débito ',
    '53': '53 - Pago Tesorería Urgente',
    '19': '19 - Crédito Pago negocio corporativo (CTP) ',
    '15': '15 - Bookentry Crédito',
    '21': '21 - Poyecto bancario 16 Bookentry Débito',
    '22': '22 - Proyecto bancario certificado ',
    '17': '17 - Desembolso Crédito (CCD)',
    '27': '27 - Débito Pago Neogcio Corporativo (CTP) ',
    '70': '70 - Retiro de nota por el por el acreedor',
    '28': '28 - Crédito Negocio Intercambio Corporativo (CTX) ',
    '74': '74 - Retiro de nota por el por el acreedor sobre un banco',
    '29': '29 - Débito Negocio Intercambio Corporativo (CTX) ',
    '75': '75 - Retiro de nota por el acreedor, avalada por otro banco',
    '30': '30 - Transferencia Crédito ',
    '76': '76 - Retiro de nota por el acreedor, sobre un banco avalada por un tercero',
    '31': '31 - Transferencia Débito ',
    '77': '77 - Retiro de una nota por el acreedor sobre un tercero',
    '32': '32 - Desembolso Crédito plus (CCD+) ',
    '78': '78 - Retiro de una nota por el acreedor sobre un tercero avalada por un banco',
    '33': '33 - Desembolso Débito plus (CCD+) ',
    '1 ': '1  - Instrumento no definido',
    '34': '34 - Pago y depósito pre acordado (PPD) ',
    '37': '37 - Pago Negocio Corporativo Ahorros Crédito (CTP)',
    '35': '35 - Desembolso Crédito (CCD) ',
    '38': '38 - Pago Negocio Corporativo Ahorros Débito (CTP)',
    '36': '36 - Desembolso Débito (CCD) ',
    '97': '97 - Clearing entre partners',
        
}


# 13.2.12. Ambiente de Destino del Documento: cbc:ProfileExecutionID y cbc:UUID/@schemeID 
# Código de Ambiente


# 13.2.13. Documento de identificación (Tipo de Identificador Fiscal): @schemeName
# Código de Identificador Fiscal



# 13.2.14. Tipo de organización jurídica (Personas): cbc:AdditionalAccountID 
# Código de Organización Jurídica
OrganizationType = {
    '1': '1 - Persona Jurídica y asimiladas',
    '2': '2 - Persona Natural y asimiladas',
}

# 13.2.15. Para el grupo TaxScheme
# Código de Tipo de Impuesto
TaxTypeCode = {
'01': '01 - IVA',
'04': '04 - INC',
'ZA': 'ZA - IVA e INC',
'ZZ (*)': 'ZZ (*) - No aplica',
}