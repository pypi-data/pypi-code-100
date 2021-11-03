import re

CONSOLA_UI_ANCHO = 47
CONSOLA_ANCHO = 80
CONSOLA_ALTO = 40

CORREO_REGEX = re.compile(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)")

URL_REGEX = re.compile(
    r"""(http(s)?:\/\/.)?(www\.)?[-a-zA-Z0-9@:%._\+~#=]{2,256}\.[a-z]{2,6}\b([-a-zA-Z0-9@:%_\+.~#?&//=]*)"""
)

DIAS_DE_SEMANA = {
    "LUN": "Lunes",
    "MAR": "Martes",
    "MIE": "Miercoles",
    "JUE": "Jueves",
    "VIE": "Viernes",
    "SAB": "Sabado",
    "DOM": "Domingo",
}

_MESES = (
    ('enero',31),
    ('febrero',28),
    ('marzo',31),
    ('abril',30),
    ('mayo',31),
    ('junio',30),
    ('julio',31),
    ('agosto',31),
    ('setiembre',30),
    ('octubre',31),
    ('noviembre',30),
    ('diciembre',31))

MESES = (
    'enero', 
    'febrero',
    'marzo',
    'abril',
    'mayo',
    'junio', 
    'julio',
    'agosto',
    'setiembre',
    'octubre',
    'noviembre',
    'diciembre'
)

MES = {
    'enero':31,
    'febrero':28,
    'marzo':31,
	'abril':30,
    'mayo':31,
    'junio':30,
    'julio':31,
	'agosto':31,
    'setiembre':30,
    'octubre':31,
	'noviembre':30,
    'diciembre':31,
}

MES_ = {
    'enero':31,
    'febrero':29,
    'marzo':31,
	'abril':30,
    'mayo':31,
    'junio':30,
    'julio':31,
	'agosto':31,
    'setiembre':30,
    'octubre':31,
	'noviembre':30,
    'diciembre':31
}

dias = (
    'Lun',
    'Mar',
    'Mie',
    'Jue',
    'Vie',
    'Sab',
    'Dom',
)

dia = {
    'lunes':0,
    'martes':1,
    'miercoles':2,
    'jueves':3,
    'viernes':4,
    'sabado':5,
    'domingo':6,
}