
# Queries nao podem terminar com ponto e virgula

def get_product_protocol_command(connection_type: str):
	if connection_type.lower() == 'mysql':
		return 'update openk_semaforo.produto set data_sincronizacao = now() where codigo_erp = %s and codigo_erp_sku = %s'
	elif connection_type.lower() == 'oracle':
		return 'update openk_semaforo.produto set data_sincronizacao = SYSDATE where codigo_erp = :codigo_erp and codigo_erp_sku = :codigo_erp_sku'
	elif connection_type.lower() == 'sqlserver':
		return 'update openk_semaforo.produto set data_sincronizacao = now() where codigo_erp = %s and codigo_erp_sku = %s'


def get_stock_protocol_command(connection_type: str):
	if connection_type.lower() == 'mysql':
		return 'update openk_semaforo.estoque_produto set data_sincronizacao = now() where codigo_erp = %s'
	elif connection_type.lower() == 'oracle':
		return 'update openk_semaforo.estoque_produto set data_sincronizacao = SYSDATE where codigo_erp = :codigo_erp'
	elif connection_type.lower() == 'sqlserver':
		return 'update openk_semaforo.estoque_produto set data_sincronizacao = now() where codigo_erp = %s'


def get_price_protocol_command(connection_type: str):
	if connection_type.lower() == 'mysql':
		return 'update openk_semaforo.preco_produto set data_sincronizacao = now() where codigo_erp = %s'
	elif connection_type.lower() == 'oracle':
		return 'update openk_semaforo.preco_produto set data_sincronizacao = SYSDATE where codigo_erp = :codigo_erp'
	elif connection_type.lower() == 'sqlserver':
		return 'update openk_semaforo.preco_produto set data_sincronizacao = now() where codigo_erp = %s'


def get_insert_client_command(connection_type: str):
	if connection_type.lower() == 'mysql':
		return '''insert into openk_semaforo.cliente (nome, razao_social, cpf, cnpj, email, telefone_residencial, telefone_celular, cep, 
														tipo_logradouro, logradouro, numero, complemento, bairro, cidade, estado, referencia)
					values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) '''
	elif connection_type.lower() == 'oracle':
		return '''INSERT INTO OPENK_SEMAFORO.CLIENTE (NOME, RAZAO_SOCIAL, CPF, CNPJ, EMAIL, TELEFONE_RESIDENCIAL, TELEFONE_CELULAR, CEP, 
														TIPO_LOGRADOURO, LOGRADOURO,NUMERO, COMPLEMENTO, BAIRRO, CIDADE, ESTADO, REFERENCIA) 
				VALUES (:1, :2, :3, :4, :5, :6, :7, :8, :9, :10, :11, :12, :13, :14, :15, :16) '''
	elif connection_type.lower() == 'sqlserver':
		return ''


def get_insert_order_command(connection_type: str):
	if connection_type.lower() == 'mysql':
		return '''insert into openk_semaforo.pedido (pedido_id, pedido_venda_id, data_pedido, status, cliente_id, valor, valor_desconto, valor_frete, 
					valor_adicional_forma_pagamento, data_pagamento, tipo_pagamento, bandeira, parcelas, condicao_pagamento_erp, codigo_rastreio, data_previsao_entrega, 
					transportadora, modo_envio)
					values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) '''
	elif connection_type.lower() == 'oracle':
		return '''INSERT INTO OPENK_SEMAFORO.PEDIDO (PEDIDO_ID, PEDIDO_VENDA_ID, DATA_PEDIDO, STATUS, CLIENTE_ID, VALOR, VALOR_DESCONTO, VALOR_FRETE, 
					VALOR_ADICIONAL_FORMA_PAGAMENTO, DATA_PAGAMENTO, TIPO_PAGAMENTO, BANDEIRA, PARCELAS, CONDICAO_PAGAMENTO_ERP, CODIGO_RASTREIO, DATA_PREVISAO_ENTREGA, 
					TRANSPORTADORA, MODO_ENVIO)
					VALUES (:1, :2, TO_DATE(:3, 'YYYY-MM-DD HH24:MI:SS'), :4, :5, :6, :7, :8, :9, TO_DATE(:10, 'YYYY-MM-DD HH24:MI:SS'), :11, :12, :13, :14, :15, TO_DATE(:16, 'YYYY-MM-DD HH24:MI:SS'), :17, :18) '''
	elif connection_type.lower() == 'sqlserver':
		return ''


def get_insert_order_items_command(connection_type: str):
	if connection_type.lower() == 'mysql':
		return '''insert into openk_semaforo.itens_pedido (pedido_id, sku, codigo_erp, quantidade, ean, valor, valor_desconto, valor_frete) 
					values (%s, %s, %s, %s, %s, %s, %s, %s) '''
	elif connection_type.lower() == 'oracle':
		return '''INSERT INTO OPENK_SEMAFORO.ITENS_PEDIDO (PEDIDO_ID, SKU, CODIGO_ERP, QUANTIDADE, EAN, VALOR, VALOR_DESCONTO, VALOR_FRETE)
					VALUES (:1, :2, :3, :4, :5, :6, :7, :8)'''
	elif connection_type.lower() == 'sqlserver':
		return ''


def get_query_client(connection_type: str):
	if connection_type.lower() == 'mysql':
		return 'select id from openk_semaforo.cliente where email = %s'
	elif connection_type.lower() == 'oracle':
		return 'SELECT ID FROM OPENK_SEMAFORO.CLIENTE WHERE EMAIL = :email'
	elif connection_type.lower() == 'sqlserver':
		return ''


def get_query_order(connection_type: str):
	if connection_type.lower() == 'mysql':
		return 'select id from openk_semaforo.pedido where pedido_id = %s'
	elif connection_type.lower() == 'oracle':
		return 'SELECT ID FROM OPENK_SEMAFORO.PEDIDO WHERE PEDIDO_ID = :order_id'
	elif connection_type.lower() == 'sqlserver':
		return ''


def get_command_parameter(connection_type: str, parameters: list):
	if connection_type.lower() == 'mysql':
		return tuple(parameters)
	elif connection_type.lower() == 'oracle':
		return parameters
	elif connection_type.lower() == 'sqlserver':
		return parameters


def get_order_protocol_command(connection_type: str):
	if connection_type.lower() == 'mysql':
		return 'update openk_semaforo.pedido set data_sincronizacao = now(), codigo_referencia = %s where pedido_id = %s'
	elif connection_type.lower() == 'oracle':
		return 'UPDATE OPENK_SEMAFORO.PEDIDO SET DATA_SINCRONIZACAO = SYSDATE, CODIGO_REFERENCIA = :order_erp_id WHERE PEDIDO_ID = :order_id'
	elif connection_type.lower() == 'sqlserver':
		return ''
