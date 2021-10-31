import os
from pathlib import Path
from datetime import datetime
from typing import Dict, Union, List, Optional, Any

import shortuuid
from slugify import slugify

from pydantic import BaseModel, EmailStr, ValidationError, validator

from .util import GeoLocation

NoneType = type(None)

class SaberesConfig(BaseModel):
    """
    Modelo de configuração do Saber. 
    Essa classe é usada para armazenar algumas configurações de base do Baobáxia.

    Configuração disponível no arquivo: /home/mocambola/.baobaxia.conf
    """

    data_path: Path
    saber_file_ext: str = '.baobaxia'
    
    default_balaio: str

    smid_len: int = 13
    slug_smid_len: int = 7
    slug_name_len: int = 7
    slug_sep: str = '_'

class Saber(BaseModel):
    """Modelo da classe Saber

    Os Saberes são informações memorizadas nas mucuas em formato
    textual e anexo arquivos binarios como imagens, documentos,
    audios, videos.
    
    :param smid: Id do Saber (SmallID)
    :type smid: str
    :param name: Nome do saber
    :type name: str
    :param slug: Identificativo do Saber, gerado pelo nome e id (Name + Smid)
    :type slug: str
    :param path: Caminho do Saber (Path)
    :type path: str
    :param balaio: Balaio de base do Saber (SLUG)
    :type balaio: str, Optional
    :param mucua: Mucua de base do Saber (SLUG)
    :type mucua: str, Optional
    :param application: Aplicação padrão para este tipo de Saber
    :type application: str
    :param created: Data de gravação
    :type created: datetime
    :param creator: Mocambola gravador
    :type creator: str
    :param last_update: Data do ultimo manejo
    :type last_update: datetime
    :param data: Modelo de dados especifico do Saber (BaseModel). 
    :type data: BaseModel, optional

    """
    name: str
    path: Path = Path('.')
    smid: Optional[str] = None
    slug: Optional[str] = None

    balaio: Optional[str] = None
    mucua: Optional[str] = None

    content: List[Path] = []

    application: str = "root"

    created: Optional[datetime] = None
    creator: Optional[str] = None 
    last_update: Optional[datetime] = None

class Mocambola(Saber):
    """
    Modelo da classe Mocambola.

    Mocambolas somos nois \\o//
    
    :param email: Email do mocambola
    :type email: emailStr, optional
    :param mocambo: Mocambo de base (SMID) 
    :type mocambo: str, optional
    :param username: Username do mocambola
    :type username: str
    :param name: Nome do mocambola
    :type name: str, optional
    :param is_native: Nativo por padrã não (False)
    :type is_native: str, false
    :param family: Familia do mocambola
    :type family: str, optional
    
    :param password_hash: Hash da senha
    :type password_hash: str
    :param validation_code: Codigo de validação
    :type validation_code: str
    
    """
    
    email: Optional[EmailStr] = None
    mocambo: Optional[str] = None
    username: str
    name: Optional[str] = None    

    is_native: bool = False
    roles: List[str] = []
    family: Optional[str] = None

    password_hash: Optional[str] = None

    recovery_question: Optional[str] = None
    recovery_answer_hash: Optional[str] = None

class Balaio(Saber):
    """
    Modelo da classe Balaio. 

    Balaio é o lugar onde guarda as coisas, e também uma pasta gerenciada
    com git-annex.
    
    :param mucua_padrao: Mucua padrão para o Balaio (SLUG)
    :type mucua_padrao: str
    """
    default_mucua: Optional[str] = None

class Mucua(Saber):
    """
    Modelo da classe Mucua. 
    
    Mucua è um nó da rede Baobáxia, e também é o fruto do Baobá.
    """
    pass

class SaberesDataStore():
    """
    Classe para armazenar os Saberes em memória e criar objetos de acesso (SaberesDataset).

    :param config: Objeto de configuração SaberConfig
    :type config: SaberConfig
    
    """

    def __init__(self, config: SaberesConfig):
        """Metodo construtor
        """
        super().__init__()
        self.config = config
        self.clear_cache()

    def clear_cache(self):
        """Limpa a cache
        """
        self._saberes = {}

    def cache(self, saber: Saber):
        """Coloca o Saber na cache
        
        :param saber: Objeto Saber a ser memorizado na cache
        :type saber: Saber

        """
        if saber.balaio not in self._saberes:
            self._saberes[saber.balaio] = {}
        if saber.mucua not in self._saberes[saber.balaio]:
            self._saberes[saber.balaio][saber.mucua] = {}
        self._saberes[saber.balaio][saber.mucua][saber.path] = saber

    def uncache(self, balaio: Optional[str], mucua: Optional[str], path: Path):
        """Remove o objeto do cache

        :param saber: Objeto Saber a ser removido da cache
        :type saber: Saber

        """
        del self._saberes[balaio][mucua][path]

    def get_cache(self, balaio: Optional[str], mucua: Optional[str], path: Path):
        return self._saberes[balaio][mucua][path]

    def is_cached(self, balaio: Optional[str], mucua: Optional[str], path: Path):
        return balaio in self._saberes and \
               mucua in self._saberes[balaio] and \
               path in self._saberes[balaio][mucua]

    def create_dataset(self, model: type, balaio: str, mucua: str, mocambola: Optional[str] = None):
        return SaberesDataset(self, model, balaio, mucua, mocambola)

    def create_balaio_dataset(self, mocambola: Optional[str] = None):
        return SaberesDataset(self, Balaio, None, None, mocambola)

    def create_mucua_dataset(self, balaio: str, mocambola: Optional[str] = None):
        return SaberesDataset(self, Mucua, balaio, None, mocambola)

class SaberesDataset():
    """Classe usada para criar e manejar os saberes.
    """

    def __init__(self,
                 datastore: SaberesDataStore,
                 model: type,
                 balaio: Optional[str] = None,
                 mucua: Optional[str] = None,
                 mocambola: Optional[str] = None):
        super().__init__()
        self.datastore = datastore
        self.model = model
        self.balaio = balaio
        self.mucua = mucua
        self.mocambola = mocambola

    def get_base_path(self):
        """Retorna o caminho básico usado pelo Dataset.
        """
        path = self.datastore.config.data_path
        if self.balaio is not None:
            path = path / self.balaio
            if self.mucua is not None:
                path = path / self.mucua
        return path

    def get_file_path(self, path):
        """Retorna o caminho de um saber (existente ou não) dentro do contexto do Dataset.
        """
        return self.get_base_path() / path / self.datastore.config.saber_file_ext

    def read_file(self, path: Path):
        """Retorna um saber armazenado em um arquivo.
        """
        return self.model.parse_file(path)

    def create_smid(self):
        """Cria um identificador aleatório pequeno (small id).
        """
        return shortuuid.ShortUUID().random(
            length=self.datastore.config.smid_len)

    def create_slug(self, smid: str, name: str):
        """Cria uma chave para o saber, usando o identificador e o nome atribuído.
        """
        result = slugify(name)
        if len(result) > self.datastore.config.slug_name_len:
            result = result[:self.datastore.config.slug_name_len]
        result += self.datastore.config.slug_sep
        if len(smid) > self.datastore.config.slug_smid_len:
            result += smid[:self.datastore.config.slug_smid_len]
        else:
            result += smid
        return result

    def find_and_collect(self, pattern: str):
        """Busca e coleta saberes a partir de um padrão para caminhos de arquivos.
        """
        result = []
        baobaxia_files = self.get_base_path().glob(
            pattern+self.datastore.config.saber_file_ext)
        for bf in baobaxia_files:
            result_item = self.read_file(path=bf)
            result.append(result_item)
            self.datastore.cache(result_item)
        return result

    def collect(self, path: Path):
        """Coleta um saber.
        """
        if self.datastore.is_cached(self.balaio, self.mucua, path):
            return self.datastore.get_cache(self.balaio, self.mucua, path).copy()
        result = self.read_file(self.get_file_path(path))
        self.datastore.cache(result)
        return result.copy()

    def settle(self, saber: Saber):
        """Assenta um saber em seu arquivo correspondente.
        """
        if self.mocambola is None:
            raise RuntimeError('Dataset is readonly (no mocambola defined)')
        if saber.balaio is None:
            saber.balaio = self.balaio
        elif saber.balaio != self.balaio:
            raise RuntimeError('Wrong balaio')
        if saber.mucua is None:
            saber.mucua = self.mucua
        elif saber.mucua != self.mucua:
            raise RuntimeError('Wrong mucua')
        if saber.slug is not None and self.datastore.is_cached(
            self.balaio, self.mucua, saber.path):
            saber_old = self.datastore.get_cache(self.balaio, self.mucua, saber.path)
            saber.created = saber_old.created
            saber.creator = saber_old.creator
        else:
            if saber.slug is None:
                if saber.smid is None:
                    saber.smid = self.create_smid()
                saber.slug = self.create_slug(saber.smid, saber.name)
                saber.path = saber.path / saber.slug
            saber.created = datetime.now()
            if isinstance(self.mocambola, Mocambola):
                saber.creator = self.mocambola.username
            else:
                saber.creator = self.mocambola
        saber.last_update = datetime.now()
        dirpath = self.get_base_path() / saber.path
        if not dirpath.exists():
            dirpath.mkdir(parents=True)
        filepath = self.get_file_path(saber.path)
        if not filepath.exists():
            filepath.touch()
        filepath.open('w').write(saber.json())

        self.datastore.cache(saber)
        return saber.copy()

    def drop(self, path: Path):
        """Abandona um saber assentado no caminho fornecido.
        """
        if self.mocambola is None:
            raise RuntimeError('Dataset is readonly (no mocambola defined)')
        self.datastore.uncache(self.balaio, self.mucua, path)

