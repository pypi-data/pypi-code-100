from django.conf import settings

name = "suap_ead"

skins = [
    ("ava_ead_default", 'AVA padrão'),
    ("ava_ead_alternative", 'AVA alternativo'),
    ("suap_ead_default", 'SUAP-EaD padrão'),
    ("suap_ead_alternative", 'SUAP-EaD alternativo'),
    ("highcontrast", 'Alto contraste'),
    ("dark", 'Dark'),
    ("contrast", 'Contraste'),
    ("golden", 'Dourado'),
    ("purple", 'Púrpura'),
    ("navy", 'Marinha'),
    ("coral", 'Coral'),
]


def get_setting(key, default):
    return getattr(settings, key, default)
