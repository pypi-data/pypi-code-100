import logging
from src.services import srequest
from src.api import oking
import sys

global is_connected_oracle_client, client_data

logging.basicConfig(level=logging.DEBUG,
                    format='[%(levelname)s][%(asctime)s] %(message)s',
                    datefmt='%Y-%m-%d %I:%M:%S')
logger = logging.getLogger()
logger.info('Iniciando oking __init__')


def get_token_from_params(args: list) -> str:
    if len(args) >= 2:
        return args[1]
    else:
        logger.error('Informe o token da integracao como parametro')
        exit(1)


token_oking = get_token_from_params(sys.argv)

# Consultar dados da integracao do cliente (modulos, tempo de execucao, dados api okvendas)
client_data = oking.get(f'https://appbuilder.openk.com.br/api/consulta/integracao_oking/filtros?token={token_oking}', None)

if client_data is not None:
    assert client_data['integracao_id'] is not None, 'Id da integracao nao informado (Api Oking)'
    assert client_data['db_type'] is not None, 'Tipo do banco de dados nao informado (Api Oking)'
    assert client_data['host'] is not None, 'Host do banco de dados nao informado (Api Oking)'
    assert client_data['database'] is not None, 'Nome do banco de dados nao informado (Api Oking)'
    assert client_data['user'] is not None, 'Usuario do banco de dados nao informado (Api Oking)'
    assert client_data['password'] is not None, 'Senha do banco de dados nao informado (Api Oking)'
    assert client_data['url_api'] is not None, 'Url da api okvendas nao informado (Api Oking)'
    assert client_data['token_api'] is not None, 'Token da api okvendas nao informado (Api Oking)'
    is_connected_oracle_client = False
else:
    logger.warning(f'Cliente nao configurado no painel oking para o token: {token_oking}')
