class BaseError(Exception):
    pass

class CapituloInicialInvalido(BaseError):
    def __init__(self, manga):

        super(CapituloInicialInvalido, self).__init__(
            f"Manga: {manga.nombre} no parte por capítulo 0 ni 1"
        )

class NoExisteCapitulo(BaseError):
    def __init__(self, manga, index: int):
        super().__init__(
            f"Manga: {manga.nombre} no tiene un capítulo de índice {index}"
        )

class ServidorRespondeContenidoProhibido(BaseError):
    def __init__(self, enlace: str):
        super().__init__(
            f"Enlace: {enlace} ha prohibido el acceso a su contenido (error 403)"
        )