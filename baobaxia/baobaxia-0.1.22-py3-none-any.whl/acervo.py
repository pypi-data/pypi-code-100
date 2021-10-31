from pathlib import Path
from enum import Enum
from typing import Optional, List, Tuple, Any
import re
import traceback

from fastapi import Header, File, UploadFile, HTTPException, Query, Form
from fastapi.responses import FileResponse
from pydantic import BaseModel

from .saberes import Saber, SaberesConfig
from .sankofa import Sankofa
from .rest import BaobaxiaAPI
from .root import (
    BaobaxiaError,
    SessionNotFound,
    SessionExpired
)

from configparser import ConfigParser

ROLE_ACERVO_EDITOR = 'acervo.editor'
ROLE_ACERVO_PUBLISHER = 'acervo.publisher'

class MidiaTipo(str, Enum):
    video = 'video'
    audio = 'audio'
    imagem = 'imagem'
    arquivo = 'arquivo'

class MidiaStatus(str, Enum):
    draft = 'draft'
    published = 'published'

class Midia(Saber):
    titulo: str
    descricao: Optional[str] = None
    autor: Optional[str] = None
    mocambo: Optional[str] = None
    tipo: Optional[MidiaTipo] = None
    status: MidiaStatus = MidiaStatus.draft
    tags: List[str] = []

pastas_por_tipo = {
    MidiaTipo.video: 'videos',
    MidiaTipo.audio: 'audios',
    MidiaTipo.imagem: 'imagens',
    MidiaTipo.arquivo: 'arquivos',
}

tipos_por_content_type = {
    'application/ogg': MidiaTipo.audio,
    'audio/ogg': MidiaTipo.audio,
    'audio/mpeg': MidiaTipo.audio,
    'image/jpeg': MidiaTipo.imagem,
    'image/png': MidiaTipo.imagem,
    'image/gif': MidiaTipo.imagem,
    'video/ogg': MidiaTipo.video,
    'video/ogv': MidiaTipo.video,
    'video/avi': MidiaTipo.video,
    'video/mp4': MidiaTipo.video,
    'video/webm': MidiaTipo.video,
    'application/pdf': MidiaTipo.arquivo,
    'application/odt': MidiaTipo.arquivo,
    'application/ods': MidiaTipo.arquivo,
    'application/odp': MidiaTipo.arquivo,
}

api = BaobaxiaAPI()

origins = ["*"]

base_path = api.baobaxia.config.data_path / \
    api.baobaxia.config.default_balaio / \
    api.baobaxia.default_mucua.path

acervo_path = base_path / 'acervo'
if not acervo_path.exists():
    acervo_path.mkdir()
for tipo, pasta in pastas_por_tipo.items():
    pasta_path = acervo_path / pasta
    if not pasta_path.exists():
        pasta_path.mkdir()

saberes_patterns = []
for pattern in pastas_por_tipo.values():
    saberes_patterns.append('acervo/'+pattern+'/*/')
api.baobaxia.discover_saberes(
#    balaio_slug=api.baobaxia.default_balaio,
#    mucua_slug=api.baobaxia.default_mucua,
    model=Midia,
    patterns=saberes_patterns,
    indexes_names=['tags'])

api.add_saberes_api(
    Midia,
    url_path='acervo/midia',
    skip_put_method=True,
    get_summary='Retornar informações da mídia')

async def post_midia(*,
                    balaio: str,
                    mucua: str,
                    titulo: str = Form(...),
                    descricao: Optional[str] = Form(None),
                    autor: Optional[str] = Form(None),
                    mocambo: Optional[str] = Form(None),
                    tipo: MidiaTipo = Form(...),
                    tags: Optional[str] = Form(None),
                    token: str = Header(...)) -> Midia:
    try:
        mocambola = api.baobaxia.get_session_mocambola(token)
        if not ROLE_ACERVO_EDITOR in mocambola.roles:
            raise HTTPException(status_code=401, detail='Mocambola não é um editor')
        midia = Midia(
            balaio=balaio,
            mucua=mucua,
            name=titulo,
            path=Path('acervo') / pastas_por_tipo[tipo],
            titulo=titulo,
            descricao=descricao,
            autor=autor,
            mocambo=mocambo,
            tipo=tipo,
            tags=re.split('; |, ', tags) if tags is not None else [])
        return api.baobaxia.put_midia(
            balaio, mucua, midia, token)
    except (SessionNotFound, SessionExpired):
        traceback.print_exc()
        raise HTTPException(status_code=401, detail="Token inválido")
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

api.add_api_route('/{balaio}/{mucua}/acervo/midia',
                  post_midia,
                  response_model=Midia,
                  methods=['POST'],
                  summary='Enviar as informações de uma mídia')

async def put_midia(*,
                    balaio: str,
                    mucua: str,
                    path: Path,
                    titulo: str = Form(...),
                    descricao: Optional[str] = Form(None),
                    autor: Optional[str] = Form(None),
                    mocambo: Optional[str] = Form(None),
                    tags: Optional[str] = Form(None),
                    token: str = Header(...)) -> Midia:
    try:
        mocambola = api.baobaxia.get_session_mocambola(token)
        if not ROLE_ACERVO_EDITOR in mocambola.roles:
            raise HTTPException(status_code=401, detail='Mocambola não é um editor')
        midia = api.baobaxia.get_midia(balaio, mucua, path, token)
        if midia.status == MidiaStatus.published and not ROLE_ACERVO_PUBLISHER in mocambola.roles:
            raise HTTPException(status_code=401, detail='Mocambola não é um publisher')
        midia.titulo = titulo
        midia.descricao = descricao
        midia.autor = autor
        midia.mocambo = mocambo
        midia.tags = re.split('; |, ', tags) if tags is not None else []
        return api.baobaxia.put_midia(
            balaio, mucua, midia, token)
    except (SessionNotFound, SessionExpired):
        traceback.print_exc()
        raise HTTPException(status_code=401, detail="Token inválido")
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

api.add_api_route('/{balaio}/{mucua}/acervo/midia/{path:path}',
                  put_midia,
                  response_model=Midia,
                  methods=['PUT'],
                  summary='Atualizar as informações de uma mídia')

async def upload_midia(*,
                       balaio: str,
                       mucua: str,
                       path: Path,
                       arquivo: UploadFile = File(...),
                       token: str = Header(...)):
    try:
        mocambola = api.baobaxia.get_session_mocambola(token)
        if not ROLE_ACERVO_EDITOR in mocambola.roles:
            raise HTTPException(status_code=401, detail='Mocambola não é um editor')
        saber = api.baobaxia.get_midia(balaio, mucua, path, token=token)
        if saber.status == MidiaStatus.published and not ROLE_ACERVO_PUBLISHER in mocambolas.roles:
            raise HTTPException(status_code=401, detail='Mocambola não é um publisher')
        if len(saber.content) == 0:
            saber.content.append(arquivo.filename)
        else:
            saber.content[0] = arquivo.filename
        with (base_path / saber.path / saber.content[0]).open(
                'wb') as arquivo_saber:
            arquivo_saber.write(arquivo.file.read())
            arquivo_saber.close()
            api.baobaxia.put_midia(balaio, mucua, saber, token)
        return {'detail': 'success'}
    except (SessionNotFound, SessionExpired):
        traceback.print_exc()
        raise HTTPException(status_code=401, detail="Token inválido")
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

api.add_api_route('/{balaio}/{mucua}/acervo/upload/{path:path}', upload_midia,
                  response_model=dict, methods=['POST'],
                  summary='Enviar o arquivo uma mídia já existente')

async def download_midia(balaio: str,
                         mucua: str,
                         path: Path,
                         token: Optional[str] = Header(None)):
    try:
        saber = api.baobaxia.get_midia(balaio, mucua, path, token=token)
        if len(saber.content) == 0:
            raise HTTPException(status_code=404, detail='Acervo não encontrado')
        return FileResponse(path=str(base_path / saber.path / saber.content[0]))
    except (SessionNotFound, SessionExpired):
        traceback.print_exc()
        raise HTTPException(status_code=401, detail="Token inválido")
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

api.add_api_route('/{balaio}/{mucua}/acervo/download/{path:path}',  
                  download_midia,
                  methods=['GET'],
                  summary='Retornar o arquivo de uma mídia')

async def publish_midia(*,
                        balaio: str,
                        mucua: str,
                        path: Path,
                        token: str = Header(...)):
    try:
        mocambola = api.baobaxia.get_session_mocambola(token)
        if not ROLE_ACERVO_PUBLISHER in mocambola.roles:
            raise HTTPException(status_code=401, detail='Mocambola não é um publisher')
        midia = api.baobaxia.get_midia(balaio, mucua, path, token)
        if len(midia.content) == 0:
            raise HTTPException(status_code=412, detail='Nâo foi realizado upload do arquivo de mídia')
        midia.status = MidiaStatus.published
        api.baobaxia.put_midia(balaio, mucua, midia, token)
        return {'detail': 'success'}
    except (SessionNotFound, SessionExpired):
        traceback.print_exc()
        raise HTTPException(status_code=401, detail="Token inválido")
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

api.add_api_route('/{balaio}/{mucua}/acervo/publish/{path:path}',
    publish_midia,
    methods=['PUT'],
    summary='Publica uma mídia')

async def find_midias(*,
                      balaio: str,
                      mucua: str,
                      keywords: Optional[str] = None,
                      hashtags: Optional[str] = Query(None),
                      tipos: Optional[str] = Query(None),
                      status: Optional[str] = Query(None),
                      creator: Optional[str] = Query(None),
                      ordem_campo: Optional[str] = None,
                      ordem_decrescente: bool = False,
                      pag_tamanho: int = 12,
                      pag_atual: int = 1,
                      token: Optional[str] = Header(None)):
    try:
        tp_list = []
        if tipos is not None and len(tipos) > 0:
            tp_list = tipos.split(' ')
        kw_list = []
        if keywords is not None and len(keywords) > 0:
            kw_list = keywords.split(' ')
        ht_list = []
        if hashtags is not None and len(hashtags) > 0:
            ht_list = hashtags.split(' ')
        def filter_function(midia):
            if status is not None and midia.status != status:
                return False
            if creator is not None and midia.creator != creator:
                return False
            if len(tp_list) > 0 and midia.tipo.value not in tipos:
                return False
            match = True
            for kw in kw_list:
                if kw not in midia.titulo and kw not in midia.descricao:
                    match = False
                    break
            for ht in ht_list:
                if ht not in midia.tags:
                    match = False
                    break
            return match
    
        def sorted_function(midia):
            if ordem_campo is None:
                return 0
            elif hasattr(midia, ordem_campo):
                return getattr(midia, ordem_campo)
            else:
                return 0
    
        return api.baobaxia.find_midias(
            balaio, mucua, token,
            filter_function=filter_function,
            sorted_function=sorted_function,
            sorted_reverse=ordem_decrescente,
            page_size=pag_tamanho,
            page_index=pag_atual)

    except (SessionNotFound, SessionExpired):
        traceback.print_exc()
        raise HTTPException(status_code=401, detail="Token inválido")
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

api.add_api_route('/{balaio}/{mucua}/acervo/find', find_midias,
                  response_model=List[Midia], methods=['GET'],
                  summary='Busca mídias de acordo com os parâmetros fornecidos')

async def get_tipos_por_content_type():
    return tipos_por_content_type
api.add_api_route('/{balaio}/{mucua}/acervo/tipos_por_content_type',
                  get_tipos_por_content_type, response_model=dict,
                  methods=['GET'],
                  summary='Retornar os content types aceitos e ' + \
                  'os tipos de mídia correspondentes para o json')

class TagCounter(BaseModel):
    tag: str
    count: int

async def get_top_tags(*,
                       balaio: str,
                       mucua: str,
                       size: int = 10):
    try:
        api.baobaxia._check_cache(Midia, 'midia', saberes_patterns, balaio, mucua)
        tags = api.baobaxia.indexes[balaio][mucua]['midia']['tags']
        counters = []
        for tag in tags:
            counters.append(TagCounter(
                tag=tag,
                count=len(tags[tag])
                ))
        
        return sorted(counters, key=lambda counter: counter.count, reverse=True)[:size] 
    except (SessionNotFound, SessionExpired):
        traceback.print_exc()
        raise HTTPException(status_code=401, detail="Token inválido")
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

api.add_api_route('/{balaio}/{mucua}/acervo/top_tags',
                  get_top_tags,
                  response_model=List[TagCounter],
                  methods=['GET'],
                  summary='Retorna as tags mais usadas')
    
        
from fastapi.middleware.cors import CORSMiddleware
api.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"])