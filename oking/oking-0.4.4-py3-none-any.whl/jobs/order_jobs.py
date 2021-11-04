import logging
from datetime import datetime
from time import sleep
from src.entities.order import Order
from src.entities.pedido import Pedido
import src
import src.database.connection as database
from src.database import queries
from src.database.utils import DatabaseConfig
import src.database.utils as utils
import src.api.okvendas as api_okvendas

logger = logging.getLogger()

default_limit = 50
queue_status = {
    'pending': 'PEDIDO',
    'paid': 'PEDIDO_PAGO',
    'shipped': 'ENCAMINHADO_ENTREGA',
    'delivered': 'ENTREGUE',
    'canceled': 'CANCELADO',
    'no_invoice': 'SEM_NOTA_FISCAL',
    'invoiced': 'FATURADO'
}


def define_job_start(job_config: dict) -> None:
    global current_job
    current_job = job_config.get('job_name')
    if current_job == 'internaliza_pedidos_job':  # Inicia o job a partir dos pedidos AgPagamento
        job_orders(job_config, True)
    else:  # Inicia o job a partir dos pedidos Confirmados
        job_orders(job_config)


def job_orders(job_config: dict, start_at_pending: bool = False) -> None:
    db_config = utils.get_database_config(job_config)
    if start_at_pending:
        process_order_queue(queue_status.get('pending'), db_config)

    process_order_queue(queue_status.get('paid'), db_config)

    process_order_queue(queue_status.get('canceled'), db_config)

    process_order_queue(queue_status.get('invoiced'), db_config)

    process_order_queue(queue_status.get('shipped'), db_config)

    process_order_queue(queue_status.get('delivered'), db_config)


def process_order_queue(status: str, db_config: DatabaseConfig) -> None:
    queue = api_okvendas.get_order_queue(
        url=src.client_data.get('url_api') + '/pedido/fila/{0}',
        token=src.client_data.get('token_api'),
        status=status,
        limit=default_limit)

    for q_order in queue:
        sleep(0.5)
        logger.info(current_job + f' | Iniciando processamento do pedido {q_order.order_id}')
        order = api_okvendas.get_order(
            url=src.client_data.get('url_api') + '/pedido/{0}',
            token=src.client_data.get('token_api'),
            order_id=q_order.order_id)

        if order.erp_code is not None and order.erp_code != '':
            if check_order_existence(db_config, order.order_id):
                logger.info(current_job + ' | Pedido ja integrado com o ERP, chamando procedure de atualizacao...')
                if call_update_order_procedure(db_config, order):
                    logger.info(current_job + ' | Pedido atualizado com sucesso')
                    protocol_order(db_config, order)
            else:
                logger.warning(current_job + f' | Pedido {order.order_id} nao existe no banco semaforo porem ja foi integrado previamente. Protocolando pedido...')
                protocol_non_existent_order(order)

        else:
            logger.info(current_job + ' | Inserindo pedido no banco semaforo')
            inserted = insert_temp_order(order, db_config)
            if inserted:
                logger.info(current_job + ' | Pedido inserido com sucesso, chamando procedures...')
                sp_success, client_erp_id, order_erp_id = call_order_procedures(db_config, q_order.order_id)
                if sp_success:
                    logger.info(current_job + ' | Chamadas das procedures executadas com sucesso, protocolando pedido...')
                    protocol_order(db_config, order, order_erp_id, client_erp_id)


def protocol_order(db_config: DatabaseConfig, order: Order, order_erp_id: str = '', client_erp_id: str = '') -> None:
    db = database.Connection(db_config)
    try:
        if order_erp_id != '':
            updated_order_code = api_okvendas.put_order_erp_code(src.client_data.get('url_api') + '/pedido/integradoERP',
                                                                 src.client_data.get('token_api'),
                                                                 order.order_id,
                                                                 order_erp_id)
            if updated_order_code:
                logger.info(current_job + ' | Codigo Erp do pedido atualizado via api OkVendas')
            else:
                logger.warning(current_job + ' | Falha ao atualizar o Codigo Erp do pedido via api OkVendas')

        if client_erp_id != '':
            updated_client_code = api_okvendas.put_client_erp_code(src.client_data.get('url_api') + '/cliente/codigo',
                                                                   src.client_data.get('token_api'),
                                                                   {
                                                                       'cpf_cnpj': order.user.cpf if order.user.cpf is not None or order.user.cpf != '' else order.user.cnpj,
                                                                       'codigo_cliente': client_erp_id
                                                                   })
            if updated_client_code:
                logger.info(current_job + ' | Codigo Erp do cliente atualizado via api OkVendas')
            else:
                logger.warning(current_job + ' | Falha ao atualizar o Codigo Erp do cliente via api OkVendas')

        protocoled_order = api_okvendas.put_protocol_orders(order.order_id)
        if protocoled_order:
            logger.info(current_job + ' | Pedido protocolado via api OkVendas')
        else:
            logger.warning(current_job + ' | Falha ao protocolar pedido via api OkVendas')

        logger.info(current_job + ' | Protocolando pedido no banco semaforo')
        conn = db.get_conect()
        cursor = conn.cursor()
        cursor.execute(queries.get_order_protocol_command(db_config.db_type), queries.get_command_parameter(db_config.db_type, [order_erp_id, order.order_id]))
        cursor.close()
        conn.commit()
        conn.close()
    except Exception as e:
        logger.error(f'Erro ao protocolar pedidos: {e}')


def protocol_non_existent_order(order: Order) -> None:
    try:
        protocoled_order = api_okvendas.put_protocol_orders(order.order_id)
        if protocoled_order:
            logger.info(current_job + f' | Pedido {order.order_id} protocolado via api OkVendas')
        else:
            logger.warning(current_job + f' | Falha ao protocolar pedido {order.order_id} via api OkVendas')
    except Exception as ex:
        logger.error(f'Erro ao protocolar pedido {order.order_id}: {str(ex)}')


def insert_temp_order(order: Order, db_config: DatabaseConfig) -> bool:
    step = ''
    db = database.Connection(db_config)
    conn = db.get_conect()
    try:
        step = 'conexao'
        cursor = conn.cursor()

        # insere cliente
        step = 'insere cliente'
        logger.info(f'\tPedido {order.order_id}: Inserindo cliente')
        cursor.execute(queries.get_insert_client_command(db_config.db_type), queries.get_command_parameter(db_config.db_type, [
            order.user.name,
            order.user.company_name,
            order.user.cpf,
            order.user.cnpj,
            order.user.email,
            order.user.residential_phone,
            order.user.mobile_phone,
            order.user.address.zipcode,
            order.user.address.address_type,
            order.user.address.address_line,
            order.user.address.number,
            order.user.address.complement,
            order.user.address.neighbourhood,
            order.user.address.city,
            order.user.address.state,
            order.user.address.reference]))

        if cursor.rowcount > 0:
            logger.info(current_job + f' | Cliente inserido para o pedido {order.order_id}')
            cursor.execute(queries.get_query_client(db_config.db_type), queries.get_command_parameter(db_config.db_type, [order.user.email]))
            client_id = cursor.fetchone()
            if client_id is None:
                cursor.close()
                raise Exception('Nao foi possivel obter o cliente inserido do banco de dados')
        else:
            cursor.close()
            raise Exception('O cliente nao foi inserido')

        # insere pedido
        step = 'insere pedido'
        logger.info(f'\tPedido {order.order_id}: Inserindo cabecalho pedido')
        cursor.execute(queries.get_insert_order_command(db_config.db_type), queries.get_command_parameter(db_config.db_type, [
            order.order_id,
            order.order_code,
            str(datetime.strptime(order.date.replace('T', ' '), '%Y-%m-%d %H:%M:%S')),
            order.status,
            client_id[0],
            order.total_amount,
            order.total_discount,
            order.freight_amount,
            order.additional_payment_amount,
            str(datetime.strptime(order.paid_date.replace('T', ' '), '%Y-%m-%d %H:%M:%S')),
            order.payment_type,
            order.flag,
            order.parcels,
            order.erp_payment_condition,
            order.tracking_code,
            str(datetime.strptime(order.delivery_forecast.replace('T', ' '), '%Y-%m-%d %H:%M:%S')),
            order.carrier,
            order.shipping_mode]))

        if cursor.rowcount > 0:
            logger.info(current_job + f' | Pedido {order.order_id} inserido')
            cursor.execute(queries.get_query_order(db_config.db_type), queries.get_command_parameter(db_config.db_type, [order.order_id]))
            order_id = cursor.fetchone()
            if order_id is None:
                cursor.close()
                raise Exception('Nao foi possivel obter o pedido inserido no banco de dados')
        else:
            cursor.close()
            raise Exception('O cliente nao foi inserido')

        # insere itens
        step = 'insere itens'
        logger.info(f'\tPedido {order.order_id}: Inserindo itens do pedido')
        for item in order.items:
            cursor.execute(queries.get_insert_order_items_command(db_config.db_type), queries.get_command_parameter(db_config.db_type, [
                order.order_id,
                item.sku,
                item.erp_code,
                item.quantity,
                item.ean,
                item.value,
                item.discount,
                item.freight_value]))

        cursor.close()
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        logger.error(current_job + f' | Passo {step} - Erro durante a inserção dos dados do pedido {order.order_id}: {str(e)}')
        conn.rollback()
        conn.close()
        return False


def call_order_procedures(db_config: DatabaseConfig, order_id: int) -> (bool, str, str):
    client_erp_id = ''
    order_erp_id = ''
    success = True
    db = database.Connection(db_config)
    conn = db.get_conect()
    try:
        cursor = conn.cursor()

        client_out_value = cursor.var(str)
        cursor.callproc('OPENK_SEMAFORO.SP_PROCESSA_CLIENTE', [order_id, client_out_value])
        client_erp_id = client_out_value.getvalue()
        if client_erp_id is not None:
            logger.info(current_job + f' | Cliente ERP criado com sucesso {client_erp_id}')
            order_out_value = cursor.var(str)
            cursor.callproc('OPENK_SEMAFORO.SP_PROCESSA_PEDIDO', [order_id, order_out_value])
            order_erp_id = order_out_value.getvalue()
            if order_erp_id is not None:
                logger.info(current_job + f' | Pedido ERP criado com sucesso {order_erp_id}')
            else:
                success = False
                logger.warning(current_job + f' | Nao foi possivel obter o id do pedido do ERP (retorno da procedure)')
        else:
            success = False
            logger.warning(current_job + f' | Nao foi possivel obter o id do cliente do ERP (retorno da procedure)')

        cursor.close()
        if success:
            conn.commit()
        else:
            conn.rollback()
        conn.close()
        return success, client_erp_id, order_erp_id
    except Exception as e:
        logger.error(current_job + f' | Erro: {e}')
        conn.rollback()
        conn.close()


def call_update_order_procedure(db_config: DatabaseConfig, order: Order) -> bool:
    success = True
    db = database.Connection(db_config)
    conn = db.get_conect()
    try:
        cursor = conn.cursor()
        order_updated = cursor.var(int)
        cursor.callproc('OPENK_SEMAFORO.SP_ATUALIZA_PEDIDO', [order.order_id, order.status, order_updated])
        updated = order_updated.getvalue()
        if updated is None or updated <= 0:
            success = False
            logger.warning(current_job + f' | Nao foi possivel atualizar o pedido informado')

        cursor.close()
        if success:
            conn.commit()
        else:
            conn.rollback()
        conn.close()
        return success
    except Exception as e:
        logger.error(current_job + f' | Erro: {e}')
        conn.rollback()
        conn.close()


def check_order_existence(db_config: DatabaseConfig, order_id: int) -> bool:
    db = database.Connection(db_config)
    conn = db.get_conect()
    try:
        cursor = conn.cursor()
        cursor.execute(queries.get_query_order(db_config.db_type), queries.get_command_parameter(db_config.db_type, [order_id]))
        existent_order = cursor.fetchone()[0]
        cursor.close()
        conn.close()
        return existent_order is not None and existent_order > 0
    except Exception as e:
        conn.close()
        return False
