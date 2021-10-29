"""
---------------------------------------------------
---------------- MÓDULO: exchange -----------------
---------------------------------------------------
Dentro da proposta do pacote jaiminho, este módulo
tem por objetivo consolidar os principais elementos
para o gerenciamento de e-mails a partir do servidor
Exchange da Microsoft utilizando, como principal
ferramenta, a biblioteca exchangelib do Python.
Aqui, o usuário poderá encontrar diversas
funcionalidades responsáveis por encapsular boa 
parte do trabalho de construção de e-mails, envio
de anexo, preparação de HTML, entre outras features
comumente utilizadas no gerenciamento de e-mails.

Table of Contents
---------------------------------------------------
1. Configurações iniciais
    1.1 Importando bibliotecas
    1.2 Configurando logs
2. Encapsulando envio de e-mails
    2.1 Funções auxiliares
---------------------------------------------------
"""

# Author: Thiago Panini
# Date: 29/08/2021


"""
---------------------------------------------------
------------ 1. CONFIGURAÇÕES INICIAIS ------------
            1.1 Importando bibliotecas
---------------------------------------------------
"""

# Classes da biblioteca exchangelib
from exchangelib import Credentials, Account, Configuration, Message, \
                        FileAttachment, HTMLBody

# Bibliotecas gerais
from pandas import DataFrame
from io import BytesIO

# Formatação html customizada
from pretty_html_table import build_table


"""
---------------------------------------------------
-------- 2. ENCAPSULANDO O ENVIO DE EMAILS --------
               2.1 Funções auxiliares
---------------------------------------------------
"""

# Conectando ao servidor Exchange
def connect_to_exchange(username, password, server, mail_box):
    """
    Providencia o retorno de uma conta configurada da Exchange
    a partir da utilização de credenciais válidas fornecidas
    pelo usuário. Na prática, esta função realiza a criação
    sequencial dos objetos Credentials, Configuration e 
    Account da biblioteca exchangelib, permitindo assim uma
    maior facilidade no manuseio dos elementos básicos de
    criação e configuração de conta no processo de gerenciamento
    de e-mails.

    Parâmetros
    ----------
    :param username:
        Usuário de e-mail com permissões válidas de envio de
        e-mails a partir da caixa genérica (mail_box) fornecida.
        Eventualmente, este parâmetro pode ser preenchido com
        o usuário de domínio Windows utilizado na autenticação
        do sistema de envio de e-mails pela Microsoft.
        [type: string]

    :param password:
        Senha referente ao usuário "username" fornecido para
        a devida autenticação no envio de e-mails.
        [type: string]

    :param server:
        Servidor de gerenciamento de e-mails utilizado nas
        operações a serem realizadas pelo objeto de conta
        criado. Um exemplo prático do servidor associado ao
        outlook do office 365 é: "outlook.office365.com"
        [type: string]

    :param mail_box:
        Caixa de e-mail a ser utilizada nas operações a serem
        designadas, sejam estas de leitura ou envio de e-mails.
        Basicamente, este parâmetro é equivalente ao parâmetro
        "primary_smtp_address" da classe Account e é a partir
        dele que as ações de e-mail são vinculadas.
        [type: string]

    Retorno
    -------
    :return account:
        Objeto do tipo Account considerando as credenciais
        fornecidas e uma configuração previamente estabelecida
        com o servidor e o endereço de SMTP primário também
        fornecidos.
        [type: Account]
    """

    # Configurando credenciais do usuário
    creds = Credentials(
        username=username, 
        password=password
    )

    # Configurando servidor com as credenciais fornecidas
    config = Configuration(
        server=server, 
        credentials=creds
    )

    # Criando objeto de conta com todo o ambiente já configurado
    account = Account(
        primary_smtp_address=mail_box, 
        credentials=creds, 
        config=config
    )
    
    return account

# Criando objeto de mensagem
def create_message(account, subject, body, to_recipients):
    """
    Consolida os elementos mais básicos para a criação de
    um objeto de mensagem a ser gerenciado externamente
    pelo usuário ou por demais funções neste módulo.
    Em linhas gerais, o código neste bloco instancia a 
    classe Message() da biblioteca exchangelib com os
    argumentos fundamentais para a construção de uma
    simples mensagem.

    Parâmetros
    ----------
    :param account:
        Objeto do tipo Account considerando as credenciais
        fornecidas e uma configuração previamente estabelecida
        com o servidor e o endereço de SMTP primário também
        fornecidos.
        [type: Account]

    :param subject:
        Título da mensagem ser enviada por e-mail.
        [type: string]

    :param body:
        Corpo da mensagem a ser enviada por e-mail. Este 
        argumento é automaticamente transformado em uma 
        string HTML a partir da aplicação da classe HTMLBody()
        antes da consolidação na classe Message().
        [type: string]

    Retorno
    -------
    :return m:
        Mensagem construída a partir da inicialização da classe
        Message() da biblioteca exchangelib. Tal mensagem 
        representa as configurações mais básicas de um e-mail 
        contendo uma conta configurada, um titulo, um corpo html 
        e uma lista válida de destinatários.
        [type: Message]
    """

    m = Message(
        account=account,
        subject=subject,
        body=HTMLBody(body),
        to_recipients=to_recipients
    )

    return m

# Anexando arquivos à mensagem
def attach_file(message, file, attachment_name, is_inline=False):
    """
    Anexa arquivos a uma mensagem já criada. De forma
    interna e dinâmica, o código desenvolvido verifica
    o tipo primitivo do arquivo passado no parâmetro
    "file" para que, dessa forma, seja possível gerenciar
    diferentes tipos de anexos fornecidos pelos usuários,
    desde caminhos de referência no sistema operacional
    até conteúdos em bytes já lidos em memória ou objetos
    do tipo DataFrame do pandas. Para cada caso, uma regra
    diferente é aplicada, seja esta associada à leitura
    do arquivo local referenciado ou até a utilização de
    um buffer de memória para transformação do arquivo em
    um formato de bytes a ser anexado posteriormente.

    Parâmetros
    ----------
    :param message:
        Mensagem criada previamente a partir de configurações
        de conta fornecidas pelo usuário. Dentro das 
        funcionalidades deste módulo, a função create_message()
        retorna uma mensagem básica e pode ser utilizada como
        parâmetro para esta lógica de anexo.
        [type: Message]

    :param file:
        Arquivo a ser anexado à mensagem alvo. Este parâmetro
        pode conter diferentes tipos primitivos, sendo eles:
            * Referência de caminho do arquivo local no SO
            * Conteúdo em bytes já lido previamente
            * Objeto DataFrame do pandas a ser anexado como csv
        Caso nenhuma das três opções seja respeitada dentro
        da solicitação de anexo proposta por esta função, a
        mensagem é retornada sem anexo e uma mensagem de alerta
        é fornecida ao usuário.
        [type: str, bytes ou DataFrame]

    :param attachment_name:
        Nome do anexo a ser enviado (com extensão).
        [type: str]

    :param is_inline:
    """

    # Leitura de arquivo local em bytes
    if type(file) is str:
        with open(file, 'rb') as f:
            content = f.read()

    # Salva objeto DataFrame em buffer para posterior leitura
    elif type(file) is DataFrame:
        buffer = BytesIO()
        file.to_csv(buffer)
        content = buffer.getvalue()

    # Arquivo passado já encontra-se em bytes
    elif type(file) is bytes:
        content = file
    
    # Formato do anexo inválido
    else:
        print(f'Formato do parâmetro "file" ({type(file)}) inválido. Retornando mensagem sem anexo')
        return message

    # Criando objeto de anexo e incluindo na mensagem
    file = FileAttachment(
        name=attachment_name,
        content=content,
        is_inline=is_inline,
        content_id=attachment_name
    )
    message.attach(file)
    
    return message

# Formatando DataFrames como HTML
def df_to_html(df, color='blue_light', font_size='medium', 
               font_family='Century Gothic', text_align='left'):
    """
    Transformação o conteúdo de um objeto DataFrame em
    uma tabela pré formatada em HTML. Em linhas gerais,
    esta função executa a função build_table() do pacote
    pretty-html-table criado justamente com a finalidade
    de transcrever DataFrames em tabelas HTML. A função
    build_table() recebe alguns argumentos essenciais,
    aos quais são transcritos nesta função df_to_html(),
    permitindo assim com que o usuário customize as cores
    da tabela resultante, bem como o tamanho, alinhamento
    ou até mesmo a família de fontes. Para informações
    mais detalhadas, é recomendado o consumo da documentação
    do pacote pretty-html-table no PyPI ou no GitHub.

    Parâmetros
    ----------
    :param df:
        Objeto DataFrame do pandas a ser utilizado como 
        alvo na transformação para tabela HTML.
        [type: pd.DataFrame]

    :param color:
        Combinação de cores a ser utilizada na customização
        da tabela resultante. A documentação oficial do
        pacote pretty-html-table traz as opções possíveis.
        [type: string, default='blue_light']

    :param font_size:
        Informação sobre o tamanho da fonte a ser alocada
        na tabela resultante. A documentação oficial do
        pacote pretty-html-table traz as opções possíveis.
        [type: string, default='medium']

    :param font_family:
        Família da fonte a ser utilizada na tabela HTML
        resultante. É possível consumir referências sobre
        as famílias de fontes possíveis no SO para testes
        adicionais.
        [type: string, default='Century Gothic']

    :param text_align:
        Alinhamento da tabela resultante no corpo do e-mail.
        [type: 'left']
    """

    # Contruindo uma tabela HTML a partir de um DataFrame
    df_html = build_table(
        df,
        color=color,
        font_size=font_size,
        font_family=font_family,
        text_align=text_align
    )

    return df_html

# Enviando mensagens
def send_mail(username, password, server, mail_box, mail_to, subject, 
              body, zip_attachments=None, send=True):
    """
    Função encapsulada para o envio de e-mails utilizando uma única
    linha de código. Na prática, esta função se utiliza de funções
    desenvolvidas neste mesmo módulo como componentes válidos de
    construção dos objetos necessários para a formulação e envio
    de e-mail. De forma direta, esta função consolida os passos para
    criação de uma conta, criação de uma mensagem e opcionalmente
    anexando arquivos passados pelo usuário em um formato zip contendo
    os nomes e os arquivos a serem anexados.

    Parâmetros
    ----------
    :param username:
        Usuário de e-mail com permissões válidas de envio de
        e-mails a partir da caixa genérica (mail_box) fornecida.
        Eventualmente, este parâmetro pode ser preenchido com
        o usuário de domínio Windows utilizado na autenticação
        do sistema de envio de e-mails pela Microsoft.
        [type: string]

    :param password:
        Senha referente ao usuário "username" fornecido para
        a devida autenticação no envio de e-mails.
        [type: string]

    :param server:
        Servidor de gerenciamento de e-mails utilizado nas
        operações a serem realizadas pelo objeto de conta
        criado. Um exemplo prático do servidor associado ao
        outlook do office 365 é: "outlook.office365.com"
        [type: string]

    :param mail_box:
        Caixa de e-mail a ser utilizada nas operações a serem
        designadas, sejam estas de leitura ou envio de e-mails.
        Basicamente, este parâmetro é equivalente ao parâmetro
        "primary_smtp_address" da classe Account e é a partir
        dele que as ações de e-mail são vinculadas.
        [type: string]

    :param subject:
        Título da mensagem ser enviada por e-mail.
        [type: string]

    :param body:
        Corpo da mensagem a ser enviada por e-mail. Este 
        argumento é automaticamente transformado em uma 
        string HTML a partir da aplicação da classe HTMLBody()
        antes da consolidação na classe Message().
        [type: string]

    :param zip_attachments:
        De todos os argumentos documentados nesta função, este
        pode ser considerado inédito. De todas as formas pensadas
        para automatizar o processo sem que parte da intuição fosse
        perdida, pensou-se em solicitar ao usuário o fornecimento
        de um elemento zipado em Python que contenha basicamente
        duas principais listas, nesta ordem:

            * Lista com os nomes dos anexos (contando com extensão)
                Ex: ['base.csv', 'imagem.png', 'bloco.txt']

            * Lista com os arquivos propriamente ditos, sejam estes
            dados como uma referência completa do caminho local de
            armazenamento, ou então os conteúdos em bytes lidos
            em alguma anterior do código. DataFrames pandas também
            são arquivos válidos no processo de anexo.
                Ex: ['path/dir/file.csv', img_em_bytes, df_pandas]

        Assim, para que o envio encapsulado de e-mails com anexo
        seja feito de forma correto, o usuário deve preparar este
        elemento zipado considerando as duas listas acima na ordem
        correta (lista à esquerda contendo os nomes e lista à
        direita contendo os arquivos). Um exemplo de preparação
        deste elemento zipado pode ser dado por:

            NAMES = ['nome1.csv', 'nome2.png']
            FILES = ['caminho/nome1.csv', arquivo_em_bytes]
            zip_attachments = zip(NAMES, FILES)

    :param send:
        Flag booleano para o envio da mensagem após todas a criação
        e preparação da mesma. Por padrão, este flag é configurado
        como sendo True, bastando apenas a chamada externa da função
        para o envio do e-mail. Caso este flag seja configurado como
        False, haverá o retorno da mensagem preparada ao usuário.
        [type: bool, default=True]
    """

    # Instanciando elemento de conta utilizando credenciais fornecidas
    acc = connect_to_exchange(
        username=username,
        password=password,
        server=server,
        mail_box=mail_box
    )

    # Criando mensagem com a configuração solicitada
    m = create_message(
        account=acc,
        subject=subject,
        body=body,
        to_recipients=mail_to
    )

    # Verificando anexos
    if zip_attachments is not None:
        for name, file in zip_attachments:
            m = attach_file(
                message=m,
                file=file,
                attachment_name=name
            )

    # Enviando mensagem se aplicável
    if send:
        m.send_and_save()
    else:
        return m

        