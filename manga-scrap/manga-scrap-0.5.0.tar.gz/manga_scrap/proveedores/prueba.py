import logging
from typing import List

from .proveedor import Proveedor
from ..modelos import MangaPreview, Imagen, Genero, CapituloDetalle, MangaDetalle, CapituloPreview

log = logging.getLogger("manga_scrap")


class PruebaProveedor(Proveedor):
    """
    Proveedor de prueba que devuelve un catálogo de 3 mangas, cada uno con 3 capítulo y cada capítulo con 3 fotos.
    """

    @property
    def url_catalogo(self) -> str:
        return "prueba.net"

    @property
    def nombre(self) -> str:
        return "Proveedor Dummy"

    def generar_catalogo(self, pagina: int = None) -> List[MangaPreview]:
        preview: List[MangaPreview] = []
        for i in range(1, 4):
            p = MangaPreview(f"Manga Nº{i}", f"https://dummy.cl/portada/{i}", f"https://dummy.cl/manga/{i}",
                             [Genero("Hentai")], True)
            preview.append(p)
        return preview

    def obtener_manga_detalle(self, preview: MangaPreview) -> MangaDetalle:
        detalle = MangaDetalle(
            preview.nombre,
            preview.enlace_imagen,
            preview.enlace_manga,
            preview.contenido_adulto,
            preview.generos,
            [CapituloPreview("capítulo 1", "https://dummy-c.com/1"), CapituloPreview("capítulo 2", "https://dummy-c.com/2"), CapituloPreview("capítulo 3", "https://dummy-c.com/3")]
        )

        return detalle

    def obtener_capitulo_detalle(self, enlace_capitulo: str) -> CapituloDetalle:
        imagenes: List[Imagen] = []
        for i in range(1, 4):
            img = Imagen("https://dummy-img/i")
            imagenes.append(img)

        return CapituloDetalle("Capítulo 1", "https://dummy-c/1", imagenes)
