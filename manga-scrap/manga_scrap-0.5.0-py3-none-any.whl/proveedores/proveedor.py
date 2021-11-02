import logging
from abc import ABC, abstractmethod
from ..modelos import MangaPreview, MangaDetalle, CapituloDetalle, CapituloPreview
from typing import List
from requests import get
from ..excepciones import ServidorRespondeContenidoProhibido

log = logging.getLogger("manga_scrap")


class Proveedor(ABC):
    """
    Clase base que define la interfaz para todas las implementaciones que representan a un proveedor de contenido,
    con sus detalles de implementación.
    """
    _catalogo: List[MangaPreview] = []

    def check_respuesta(self):
        log.debug(f"Haciendo check de disponibilidad para proveedor {self.nombre}...")
        respuesta = get(self.url_catalogo)
        if respuesta.status_code == 403:
            log.error(f"El proveedor {self.nombre} con url {self.url_catalogo} ha prohibido el acceso a su contenido.")
            raise ServidorRespondeContenidoProhibido(self.url_catalogo)
        if respuesta.status_code != 200:
            log.warning(
                f"El proveedor {self.nombre} con url {self.url_catalogo} ha respondido con código diferente a 200: {respuesta.status_code}")

    @property
    @abstractmethod
    def url_catalogo(self) -> str:
        """
        :return: URL correspondiente al catálogo del proveedor.
        """

    @property
    @abstractmethod
    def nombre(self) -> str:
        """
        :return: Nombre del proveedor
        """

    @abstractmethod
    def generar_catalogo (self, pagina : int = None)  -> List[MangaPreview]:
        """
        Scrapea la lista de mangas para generar un catálogo

        :return: un catálogo de tipo List[MangaPreview]
        """

    @property
    def catalogo(self) -> List[MangaPreview]:
        if not self._catalogo:
            self._catalogo = self.generar_catalogo()

        return self._catalogo

    @abstractmethod
    def obtener_manga_detalle(self, preview: MangaPreview) -> MangaDetalle:
        """
        Scrapea y construye un manga detalle a partide una preview.
        :param preview: MangaPreview que se usará para scrappear y llenar el resto de datos de un MangaDetalle.
        :return:
        """

    @abstractmethod
    def obtener_capitulo_detalle(self, enlace_capitulo: str) -> CapituloDetalle:
        """
        Scrapea un preview de capitulo y devuelve todo el contenido de un capítulo
        :param enlace:
        :return: Capitulo construído
        """
