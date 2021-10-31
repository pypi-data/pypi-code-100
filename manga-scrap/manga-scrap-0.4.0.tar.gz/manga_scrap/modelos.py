import json
import logging
from dataclasses import dataclass
from typing import List

log = logging.getLogger("manga_scrap")


class JsonSerializable:
    def to_json_string(self) -> str:
        return json.dumps(self, default=lambda o: o.__dict__, ensure_ascii=False).encode("utf-8").decode()


@dataclass()
class Genero(JsonSerializable):
    """
    Representacion de un único genero para un manga
    """
    genero: str

    def __repr__(self):
        return self.genero

    def __str__(self):
        return self.genero


@dataclass()
class MangaPreview(JsonSerializable):
    """
    Representación de un manga sin contenido, visto desde el catálogo.

    :param: nombre: str
    :param: enlace_imagen: str
    :param: enlace_manga: str
    """
    nombre: str
    enlace_imagen: str
    enlace_manga: str
    generos: List[Genero]
    contenido_adulto: bool = False


@dataclass()
class Imagen(JsonSerializable):
    """
    Representación de una única imagen/hoja de un manga
    """
    enlace: str

@dataclass()
class CapituloPreview(JsonSerializable):
    """
    Representación de un capítulo antes de abrirse, útil para la vista de detalle.
    """
    nombre: str
    enlace: str

@dataclass()
class CapituloDetalle(JsonSerializable):
    """
    Representación de un capítulo cuando se está viendo, incluye su información y todas las imágenes del susodicho capítulo.
    """
    nombre: str
    enlace: str
    imagenes: List[Imagen]


@dataclass()
class MangaDetalle(JsonSerializable):
    """
    Representación de un manga con información detallada, útil para vistas de detalle.
    """

    nombre: str
    imagen: str
    enlace: str
    contenido_adulto: bool
    generos: List[Genero]
    capitulos: List[CapituloPreview]
