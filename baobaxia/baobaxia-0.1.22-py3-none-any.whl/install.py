from .saberes import SaberesConfig, Saber, SaberesDataset, \
    SaberesDataStore, Balaio, Mucua, Mocambola
from .sankofa import Sankofa

from pathlib import Path
from configparser import ConfigParser

import argparse, os

from getpass import getpass

parser = argparse.ArgumentParser("criar_mucua")
parser.add_argument("--path", help="Caminho absoluto da pasta para os dados do Baobáxia", type=str)
parser.add_argument("--balaio", help="Nome do Balaio", type=str)
parser.add_argument("--mucua", help="Nome da Mucua local onde instalar o Baobáxia", type=str)
parser.add_argument("--mocambola", help="Username para criar um Mocambola", type=str)
parser.add_argument("--email", help="Email do Mocambola", type=str)
parser.add_argument("--password", help="Password para o Mocambola", type=str)
parser.add_argument("--smid_len", help="Numero de carateres para os IDs", type=int)
parser.add_argument("--slug_name_len", help="Numero de carateres para os nomes abreviados", type=int)
parser.add_argument("--slug_smid_len", help="Numero de carateres para os IDs abreviados", type=int)
parser.add_argument("--slug_sep", help="Caracter separador para o identificativo", type=str)


args = parser.parse_args()

def install_interactive():
    print('Instalador do Baobáxia')
    print('Entre com os dados do ambiente')
    path = input('Caminho do diretório de dados: ')
    balaio = input('Nome do balaio: ')
    mucua = input('Nome da mucua: ')
    print('Entre com os dados do mocambola')
    mocambola = input('Nome de usuário: ')
    email = input('E-mail: ')
    password = getpass('Senha: ')
    print('Entre com as configurações de chave primária')
    smid_len = input('Tamanho da chave aleatória (smid) ')
    slug_name_len = int(input('Tamanho do nome na chave primária: '))
    slug_smid_len = int(input('Tamanho da chave aleatória na chave primária: '))
    slug_sep = input('Separador da chave primária: ')
    install(path = path,
            balaio = balaio,
            mucua = mucua,
            mocambola = mocambola,
            email = email,
            password = password,
            smid_len = smid_len,
            slug_name_len = slug_name_len,
            slug_smid_len = slug_smid_len,
            slug_sep = slug_sep)

def install(*, path: str, balaio: str, mucua: str, mocambola: str,
            email: str, password: str, smid_len: int, slug_name_len: int,
            slug_smid_len: int, slug_sep: str):
    """Instalador do Baobáxia

    :param path: Caminho absoluto da pasta para os dados do Baobáxia
    :type path: str
    :param balaio: Nome do Balaio
    :type balaio: str
    :param mucua: Nome da Mucua local onde instalar o Baobáxia
    :type mucua: str
    :param mocambola: Username para criar um Mocambola
    :type mocambola: str
    :param email: Email do Mocambola
    :type email: str
    :param password: Password para o Mocambola
    :type password: str
    :param smid_len: Numero de carateres para os IDs
    :type smid_len: int
    :param slug_name_len: Numero de carateres para os nomes abreviados
    :type slug_name_len: int
    :param slug_smid_len: Numero de carateres para os IDs abreviados
    :type slug_smid_len: int
    :param slug_sep: Caracter separador para o identificativo
    :type slug_sep: str

    """

    data_path = Path(path)

    if data_path.is_absolute:
        config = SaberesConfig(
            data_path = data_path,
            default_balaio = balaio,
            smid_len = smid_len, 
            slug_name_len = slug_name_len,
            slug_smid_len = slug_smid_len,
            slug_sep = slug_sep
        )
        datastore = SaberesDataStore(config)
        balaio_dataset = datastore.create_balaio_dataset(
            mocambola=mocambola)
        balaio_saber = balaio_dataset.settle(
            Balaio(name=balaio, default_mucua=mucua))
        mucua_dataset = datastore.create_mucua_dataset(
            balaio=balaio_saber.slug, mocambola=mocambola)
        mucua_saber = mucua_dataset.settle(
            Mucua(name=mucua))
        
        balaio_saber.default_mucua = mucua_saber.slug
        balaio_dataset.settle(balaio_saber)

        mocambolas_path = config.data_path / balaio_saber.slug \
            / mucua_saber.slug / 'mocambolas'
        mocambolas_path.mkdir()
        mocambola_dataset = datastore.create_dataset(
            Mocambola, balaio_saber.slug, mucua_saber.slug, mocambola)
        from .util import str_to_hash
        mocambola_saber = mocambola_dataset.settle(
            Mocambola(
                path=Path('mocambolas'),
                name=mocambola,
                username=mocambola,
                email=email,
                password_hash=str_to_hash(password)
                ))

        Sankofa.create_balaio(balaio=balaio_saber.slug,
                              description=balaio_saber.slug,
                              config=config)
        
        Sankofa.add(saberes=[mucua_saber,
                             mocambola_saber],
                    mocambola=mocambola_saber,
                    config=config)

    config_file = ConfigParser()
    
    config_file['default'] = {
        "data_path": path,
        "saber_file_ext": ".baobaxia",
        "default_balaio": balaio_saber.slug,
        "default_mucua": mucua_saber.slug,
        "smid_len": smid_len,
        "slug_smid_len": slug_smid_len,
        "slug_name_len": slug_name_len,
        "slug_sep": slug_sep
    }

    try:     
        with open(os.path.join(os.path.expanduser("~"), '.baobaxia.conf'), 'w') as writefile:
            config_file.write(writefile)
    except IOError:
        pass

def criar_mucua():
    install(**args.__dict__)


