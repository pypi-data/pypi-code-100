from typing import List
from manga_scrap.modelos import MangaPreview, Imagen, Genero, CapituloPreview, CapituloDetalle, MangaDetalle
from manga_scrap.proveedores.proveedor import Proveedor
import requests
from bs4 import BeautifulSoup as BS, Tag
import logging

log = logging.getLogger("manga_scrap")


class MangaList(Proveedor):

    @property
    def url_catalogo(self) -> str:
        return "https://leermanga.net/biblioteca"

    @property
    def nombre(self) -> str:
        return "mangaList.com"

    def generar_catalogo(self, pagina: int = None) -> List[MangaPreview]:
        log.debug("Generando catalogo")
        numero_paginas = pagina if pagina else self._contar_paginas()
        previews_lista = []
        for i in range(numero_paginas):
            i += 1
            log.debug(f'Número de pagina actual: {i}')
            previews = self._obtener_preview_mangas(i)
            previews_lista += previews

        return previews_lista

    def obtener_manga_detalle(self, preview: MangaPreview) -> MangaDetalle:
        capitulos = self._obtener_capitulos(preview.enlace_manga)
        return MangaDetalle(
            nombre=preview.nombre,
            imagen=preview.enlace_imagen,
            enlace=preview.enlace_manga,
            contenido_adulto=preview.contenido_adulto,
            generos=preview.generos,
            capitulos=capitulos
        )

    def obtener_capitulo_detalle(self, enlace_capitulo: str) -> CapituloDetalle:
        log.debug(f"Obteniendo todo el contenido de capítulo {enlace_capitulo}...")
        r = requests.get(enlace_capitulo)
        soup = BS(r.text, features="html.parser")

        nombre = soup.find('h1', attrs={'id': 'chapter-heading'}).contents[0].strip()

        images = soup.find_all("div", {"id": "images_chapter"})
        lista_images = []
        img = images[0].contents
        for enlace_img in img:
            if type(enlace_img) is Tag:
                imagen = Imagen(enlace_img.attrs.get("data-src"))
                lista_images.append(imagen)

        return CapituloDetalle(nombre, enlace_capitulo, lista_images)

    def _obtener_preview_mangas(self, page: int):
        log.debug("Generando previews")
        r = requests.get(f"{self.url_catalogo}?page={page}")
        soup = BS(r.text, features='html.parser')
        cosa = soup.find_all("div", {"class": "manga_biblioteca"})
        mangas_previews = []
        for resultado in cosa:
            enlace = resultado.contents[3].attrs.get("href")
            imagen = resultado.contents[3].contents[1].attrs.get("src")
            nombre = resultado.contents[3].attrs.get("title")
            manga = MangaPreview(nombre, imagen, enlace, self._obtener_generos(enlace))
            log.debug(f'Nombre manga: {nombre}')
            mangas_previews.append(manga)
        return mangas_previews

    def _obtener_capitulos(self, enlace: str):
        log.debug(f"Obteniendo capítulos desde enlace {enlace}...")
        r = requests.get(enlace)
        soup = BS(r.text, features='html.parser')
        table = soup.findAll('li', attrs={'class': 'wp-manga-chapter'})
        capitulos = []
        for row in table:
            enlace_capitulo = (row.contents[1].attrs.get("href"))
            nombre = row.contents[1].next.strip()
            capitulo = CapituloPreview(nombre, enlace_capitulo)
            capitulos.append(capitulo)
        return capitulos

    def _contar_paginas(self):
        log.debug("Contando paginas")
        r = requests.get(self.url_catalogo)
        soup = BS(r.text, features='html.parser')
        paginas = soup.find('ul', attrs={'class': 'pagination'})
        numero_paginas = paginas.contents[-4].contents[0].contents[0]
        log.debug(f'Número de paginas {numero_paginas}')
        return int(numero_paginas)

    def _obtener_generos(self, enlace: str):
        log.info(f"Obteniendo géneros para manga con enlace {enlace}")
        r = requests.get(enlace)
        soup = BS(r.text, features='html.parser')
        datos_interesantes = soup.findAll("i", {"class": "fas fa-tag"})
        categorias = []
        for i in datos_interesantes:
            genero = Genero(i.next.strip())
            categorias.append(genero)
        return categorias
