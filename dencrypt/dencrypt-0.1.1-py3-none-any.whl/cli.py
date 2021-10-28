import argparse
import os
import glob
import random
from datetime import datetime

from dencrypt import (
    __version__,
    Crypt, Encrypt, Decrypt, EncryptFile, DecryptFile
)

"""Dencrypt CLI
Exemplos de uso:
    + Verificando Versão
        > dencrypt --version | > dencrypt -v

    + Gerando chaves
        - Pública RSA (2048), Privada RSA (2048) e Simétrica Fernet
            > dencrypt --keys | > dencrypt -k

        - Apenas Simétrica Fernet
            > dencrypt --keys --norsa | > dencrypt -k -nr

        - Apenas Pública/Privada RSA (Tamanho 1024)
            > dencrypt --keys --nofer -size 1024 | > dencrypt -k -nf -s 1024
        
        - Pública/Privada RSA (2048) e Simétrica Fernet escolhendo local para salvar
            > dencrypt --keys --location "C:/user/User/Desktop" | > dencrypt -l "C:/user/User/Desktop"
        
        - Pú./Pr. RSA (2048) e Sim. Fer. adicionando prefixo e sufixo e alterando 
          extensão nos nomes dos arquivos das chaves
            > dencrypt --keys --prefix "B1_" --sufix "_1B" --ext ".chave" 
            > dencrypt -k -px "B1_" -sx "_1B" -e ".chave"
            
            Exemplo de resultado padrão sem aplicar "-px", "-sx" e "-e"
                - privatekey.key
                - publickey.key
                - symmetrickey.key
            
            Exemplo de resultado aplicando "-px", "-sx" e "-e"
                - B1_privatekey_1B.chave
                - B1_publickey_1B.chave
                - B1_symmetrickey_1B.chave

    + Encriptando arquivos/conteúdo
        - Com chave Simétrica Fernet
            > dencrypt --encrypt --input "arquivo.jpg" --skey "symmetrickey.key"
                        -enc      -i                    -sk
            Será gerado um novo arquivo chamado "arquivo.jpg.dencrypt"

        - Com chave Pública RSA
            > dencrypt -enc -i "arquivo.jpg" --pkey "publickey.key"
                                              -pk
            Será gerado um novo arquivo chamado "arquivo.jpg.dencrypt"
            ! Esta encriptação é limitada ao seu tamanho. Caso a chave seja de 
              2048 bits (Padrão), suportará um conteúdo de no máximo 256 bytes

        - Texto
            > ... -i "Texto Secreto" -sk ... --forcetext 
                                              -ft
            Será gerado um novo arquivo chamado "Texto Secreto.dencrypt" com o texto 
              criptografado de conteúdo
            Porém como podemos observar, o nome do arquivo se mantém com o do conteúdo
              secreto, abaixo veja exemplos de como renomear o arquivo com `output`      
        
        - Utilizando `--ext` e `--output` para salvar arquivo com nome diferente
            ? DICA: `--output` possui alguns format strings
                %FILENAME = Retorna o nome completo do arquivo original - Ex: "arquivo.jpg"
                %FILEEXT  = Retorna apenas a extensão do arquivo original - Ex: ".jpg"
                %FILE     = Retorna o nome do arquivo original - Ex: "arquivo"
                %EXT"     = Retorna a extensão enviada através do `--ext` - Por padrão é ".dencrypt"
                %DATETIME = Retorna a data do momento, seguinto o formado: ddmmaaaahhmmss 
                %RAND"    = Retorna um número aleatório entre 100.000 e 999.999
            
            > ... --ext ".louco" --output "a"
                   -e             -o
            Será gerado um novo arquivo chamado "a.louco" em vez de "arquivo.jpg.dencrypt"
            
            > ... -e ".louco" -o "%FILENAME%EXT"  |  > ... -e ".teste" -o "%FILE_%DATETIME%EXT"
            Resultará em "arquivo.jpg.louco"      |  Resultará em "arquivo_281020210252.teste"
            
            > ... --ext ".abcabc" --output "%RAND%EXT"  |  > ... --ext ".abcabc"
            Resultará em "734582.abcabc"                |  Resultará em "arquivo.jpg.abcabc" 
        
        - Múltiplos arquivos
          > dencrypt --encrypt --allfiles --skey "symmetrickey.key"
                                -af
          Todos arquivos da pasta atual serão criptografados e salvos em uma 
          nova pasta (criada no mesmo diretório) chamada "dencrypt_encrypt_202110280323" 
          com a data atual no final
          O nome dos novos arquivos seguirá o formato "nome.ext.dencrypt", Ex: "imagem.jpg.dencrypt"
          ! Os arquivos originais ainda serão mantidos

          > ... --allfiles ... --extignore "jpg, png, py"
                                -eig
          Realizará o mesmo processo anterior, porém ignorando arquivos com as extensões informadas
          .jpg, .png e .py

        - Comandos persistentes
          --replace ou -r = Força a substituição de qualquer arquivo existente com o mesmo nome
          --force ou -f   = Ignora qualquer aviso, e avança automaticamente 

    + Decriptando arquivos/conteúdo
      - Funcionamento semelhante ao `--encrypt`, porém, agora deve ser passado via `--input`
        o arquivo já criptografado

      - Com chave Simétrica Fernet
        > dencrypt --decrypt --input "arquivo.jpg.dencrypt" --skey "symmetrickey.key"
                    -dec      -i                    -sk
        Será gerado um novo arquivo chamado "arquivo.jpg"

      - Com chave PRIVADA RSA
        > dencrypt -dec -i "arquivo.jpg.dencrypt" --pkey "privatekey.key"
                                                   -pk
        Será gerado um novo arquivo chamado "arquivo.jpg"

      ...
"""

def cli():

    """
    Comandos
    """
    parser = argparse.ArgumentParser(description = 'CLI - Para testes do DENcrypt')

    # Version
    parser.add_argument(
        "-v", "--version", help="retorna a versão do dencrypt", action="store_true")

    # Keys
    parser.add_argument(
        "-k", "--keys", help="criará chaves RSA e Fernet", action="store_true")

    parser.add_argument(
        "-nr", "--norsa", help="não irá criar chaves RSA [TRUE]", action="store_true")

    parser.add_argument(
        "-nf", "--nofer", help="não irá criar chave Fernet [TRUE]", action="store_true")

    parser.add_argument(
        "-s", "--size", help="tamanho das chaves RSA [2048]", 
        default=2048, type=int)

    parser.add_argument(
        "-l", "--location", help="local para salvar as chaves", 
        default="", type=str)

    parser.add_argument(
        "-px", "--prefix", help="prefixo do nome do arquivo da chave", 
        default="", type=str)
    
    parser.add_argument(
        "-sx", "--sufix", help="sufixo no nome do arquivo da chave", 
        default="", type=str)

    # Encrypt
    parser.add_argument(
        "-enc", "--encrypt", help="gera um novo arquivo criptografado", action="store_true")

    # Decrypt
    parser.add_argument(
        "-dec", "--decrypt", help="gera um novo arquivo criptografado", action="store_true")

    # Global
    parser.add_argument(
        "-i", "--input", default=None, type=str,
        help="nome do arquivo que deve ser criptografado/decriptografado")

    parser.add_argument(
        "-o", "--output", default=None, type=str,
        help="nome do arquivo que deve ser criptografado/decriptografado")

    parser.add_argument(
        "-sk", "--skey", default=None, type=str,
        help="chave simétrica que será utilizada para criptografar/descriptografar o arquivo")

    parser.add_argument(
        "-pk", "--pkey", default=None, type=str,
        help="chave pública/privada que será utilizada para criptografar/descriptografar o conteúdo")

    parser.add_argument(
        "-e", "--ext", help="extensão do arquivo que será salvo", 
        default=None, type=str)

    parser.add_argument(
        "-r", "--replace", action="store_true", 
        help="se deve substituir arquivo já existente com mesmo nome"
    )

    parser.add_argument(
        "-eig", "--extignore", default="dencrypt", type=str,
        help=(
            "extensões que devem ser ignoradas - separando por vírgula\n"
            'ex: "jpg, png, mp4"'
        )
    )

    parser.add_argument(
        "-af", "--allfiles", action="store_true", 
        help="se deve realizar criptografia/descriptografia em todos arquivos do diretório"
    )

    parser.add_argument(
        "-b64", "--base64", action="store_true", 
        help="se deve salvar o conteúdo criptografado em base64"
    )

    parser.add_argument(
        "-f", "--force", action="store_true", 
        help="ignora qualquer pergunta de segurança"
    )

    parser.add_argument(
        "-ft", "--forcetext", action="store_true", 
        help="força que o --input seja reconhecido como texto (caso tenha mesmo nome de algum arquivo)"
    )

    parser.add_argument(
        "-sw", "--show", action="store_true", 
        help="exibe o conteúdo criptografado/descriptografado no terminal"
    )

    
    # Iniciando
    args = parser.parse_args()

    # Version
    if (args.version):
        print(__version__)

    # Keys
    elif (args.keys):
        NOT_RSA_AND_FER = args.norsa and args.nofer
        RSA_AND_FER = not args.norsa and not args.nofer
        RSA_OK = args.norsa
        FER_OK = args.nofer

        replace = args.replace
        ext = ".key" if (args.ext is None) else args.ext

        if (NOT_RSA_AND_FER):
            print("-- ERRO: Ao menos uma das chaves deve ser criada --")
        
        elif (RSA_AND_FER):
            try:
                Crypt().save_all_keys(
                    args.prefix, args.sufix, ext, 
                    True, replace, args.location
                )
            except Exception as e:
                print(f"ERRO: {e}")

        elif (RSA_OK):
            try:
                Crypt().save_symkey(
                    args.prefix, args.sufix, ext, 
                    True, replace, args.location
                )
            except Exception as e:
                print(f"ERRO: {e}")
        
        elif (FER_OK):
            try:
                Crypt().save_keys(
                    args.prefix, args.sufix, ext, 
                    True, replace, args.location
                )
            except Exception as e:
                print(f"ERRO: {e}")
        
        else:
            print("-- COMANDO INVÁLIDO --")

    # Encrypt
    elif (args.encrypt):
        
        actual_datetime = datetime.now().strftime("%d%m%Y%H%M%S")

        # Args
        input_ = args.input
        replace = args.replace
        ext = ".dencrypt" if (args.ext is None) else args.ext
        extignore = args.extignore.split(",") # ex: "mp4, .png,jpg "
        extignore = list(map(
            lambda e: 
            f".{e.strip()}" if not e.strip().startswith(".") else e.strip(),
            extignore
        )) # ex: [".mp4", ".png", ".jpg"]

        # OUTPUT
        try:
            filename, file_ext = os.path.splitext(
                os.path.basename(input_))
            original_filename = f"{filename}{file_ext}"
        except:
            filename, file_ext = ("", "")
            original_filename = ""

        if (args.output is None):
            out = f"{input_}{ext}"
        else:
            out = args.output
        
        out = out.replace("%FILENAME", original_filename)
        out = out.replace("%FILEEXT", file_ext)
        out = out.replace("%FILE", filename)
        out = out.replace("%EXT", ext)
        out = out.replace("%DATETIME", actual_datetime)
        out = out.replace("%RAND", str(random.randint(100000, 999999)))

        # Iniciando
        if (input_ is None and args.allfiles is False):
            print(f"-- Informe algum arquivo ou texto via '--input' --")
            print(f'   Ex: --encrypt -i "imagem 1.jpg" -sk symmetrickey.key')
            print(f'   Ex: --encrypt --input "video.mp4" --skey symmetrickey.key')

        elif (args.skey is None and args.pkey is None):
            print(f"-- Informe uma chave --")
            print(f'   Ex: --encrypt -i "imagem 1.jpg" -sk symmetrickey.key')
            print(f'   Ex: --encrypt --input "arquivo_pequeno.txt" --pkey publickey.key')
        
        elif (args.skey is not None and args.pkey is not None):
            print(f"-- Informe APENAS uma chave --")
            print(f'   INCORRETO: -sk symmetrickey.key -pk publickey.key')
            print(f'   CORRETO: -sk symmetrickey.key')
        
        elif (args.allfiles is True):
            
            input_ = "" if input_ is None else os.path.dirname(input_)
            files = glob.glob(f"{os.path.join(input_, '*.*')}")
            
            for t in extignore:
                files = list(
                    filter(
                        lambda e: not e.lower().endswith(t.lower()), files
                    )
                )

            if (len(files) == 0):
                print("-- NENHUM ARQUIVO ENCONTRADO --")
            
            else:
                print()
                print("-" * 10)
                for i, file in enumerate(files, 1):
                    print(f"{i}. {file}")
                print("-" * 10)
                
                if (args.force is False):
                    q = input(
                        "DESEJA GERAR A VERSÃO CRIPTOGRAFADA " 
                        "DESSES ARQUIVOS [s/N]? "
                    ).lower()
                else:
                    q = "s"

                if (q in ["s", "sim", "y", "yes"]):
                    path = os.path.join(input_, f"dencrypt_encrypt_{actual_datetime}")
                    os.mkdir(path) # Criando pasta

                    errors = 0
                    success = 0
                    print()
                    print("-" * 10)
                    for i, file in enumerate(files, 1):
                        filename, fileext = os.path.splitext(
                            os.path.basename(file))
                        
                        final_filename = os.path.join(
                            path, f"{filename}{fileext}{ext}")

                        try:
                            if (args.pkey is None):
                                encr = EncryptFile(file, args.skey)
                            else:
                                encr = Encrypt(input_, args.pkey)

                            if encr.save(
                                final_filename, b64=args.base64, replace_file=replace
                            ):
                                success += 1
                                print(f"{i}. {file} [OK]")
                            else:
                                errors += 1
                                print(f"{i}. {file} [FAIL]")
                
                        except Exception as e:
                            errors += 1
                            print(f"{i}. {file} [FAIL] {e}")
                    print("-" * 10)
                    print(f"FINALIZADO: {success}/{len(files)} - {errors} errors")
                    print()
        else:
            try:
                if (args.forcetext is True):
                    input_ = input_.encode()

                if (args.pkey is None):
                    encr = EncryptFile(input_, args.skey)
                else:
                    encr = Encrypt(input_, args.pkey)

                if encr.save(
                    out, b64=args.base64, replace_file=replace
                ):
                    print(f"Arquivo '{out}' salvo com sucesso!")
                    if (args.show):
                        print("SHOW: ")
                        print(encr.get())
                        print()
                else:
                    print(f"Falha ao salvar '{out}'")
    
            except Exception as e:
                print(f"ERRO: {e}")
    
    # Decrypt
    elif (args.decrypt):
        
        actual_datetime = datetime.now().strftime("%d%m%Y%H%M%S")

        # Args
        input_ = args.input
        replace = args.replace
        ext = ".dencrypt" if (args.ext is None) else args.ext
        extignore = "" if args.extignore == "dencrypt" else args.extignore
        extignore = extignore.split(",") # ex: "mp4, .png,jpg "
        extignore = list(map(
            lambda e: 
            f".{e.strip()}" if not e.strip().startswith(".") else e.strip(),
            extignore
        )) # ex: [".mp4", ".png", ".jpg"]

        # OUTPUT
        try:
            filename, file_ext = os.path.splitext(
                os.path.basename(input_))
            original_filename = f"{filename}{file_ext}"
        except:
            filename, file_ext = ("", "")
            original_filename = ""

        if (args.output is None):
            out = f"{input_.replace(ext, '')}"
        else:
            out = args.output
        
        out = out.replace("%FILENAME", original_filename)
        out = out.replace("%FILEEXT", file_ext)
        out = out.replace("%FILE", filename)
        out = out.replace("%EXT", ext)
        out = out.replace("%DATETIME", actual_datetime)
        out = out.replace("%RAND", str(random.randint(100000, 999999)))

        # Iniciando
        if (input_ is None and args.allfiles is False):
            print(f"-- Informe algum arquivo ou texto via '--input' --")
            print(f'   Ex: --decrypt -i "imagem 1.jpg.dencrypt" -sk symmetrickey.key')
            print(f'   Ex: --decrypt --input "video.mp4.dencrypt" --skey symmetrickey.key')

        elif (args.skey is None and args.pkey is None):
            print(f"-- Informe uma chave --")
            print(f'   Ex: --decrypt -i "imagem 1.jpg.dencrypt" -sk symmetrickey.key')
            print(f'   Ex: --decrypt --input "arquivo_pequeno.txt.dencrypt" --pkey publickey.key')
        
        elif (args.skey is not None and args.pkey is not None):
            print(f"-- Informe APENAS uma chave --")
            print(f'   INCORRETO: -sk symmetrickey.key -pk publickey.key')
            print(f'   CORRETO: -sk symmetrickey.key')
        
        elif (args.allfiles is True):
            
            input_ = "" if input_ is None else os.path.dirname(input_)
            files = glob.glob(f"{os.path.join(input_, '*.*')}")
            
            for t in extignore:
                files = list(
                    filter(
                        lambda e: not e.lower().endswith(t.lower()), files
                    )
                )

            if (len(files) == 0):
                print("-- NENHUM ARQUIVO ENCONTRADO --")
            
            else:
                print()
                print("-" * 10)
                for i, file in enumerate(files, 1):
                    print(f"{i}. {file}")
                print("-" * 10)
                
                if (args.force is False):
                    q = input(
                        "DESEJA GERAR A VERSÃO DESCRIPTOGRAFADA " 
                        "DESSES ARQUIVOS [s/N]? "
                    ).lower()
                else:
                    q = "s"

                if (q in ["s", "sim", "y", "yes"]):
                    path = os.path.join(input_, f"dencrypt_decrypt_{actual_datetime}")
                    os.mkdir(path) # Criando pasta

                    errors = 0
                    success = 0
                    print()
                    print("-" * 10)
                    for i, file in enumerate(files, 1):
                        filename, fileext = os.path.splitext(
                            os.path.basename(file.replace(ext, '')))
                        
                        final_filename = os.path.join(
                            path, f"{filename}{fileext}")

                        try:
                            if (args.pkey is None):
                                decr = DecryptFile(file, args.skey)
                            else:
                                decr = Decrypt(input_, args.pkey)

                            if decr.save(
                                final_filename, b64=args.base64, replace_file=replace
                            ):
                                success += 1
                                print(f"{i}. {file} [OK]")
                            else:
                                errors += 1
                                print(f"{i}. {file} [FAIL]")
                
                        except Exception as e:
                            errors += 1
                            print(f"{i}. {file} [FAIL] {e}")
                    print("-" * 10)
                    print(f"FINALIZADO: {success}/{len(files)} - {errors} errors")
                    print()
        else:
            try:
                if (args.forcetext is True):
                    input_ = input_.encode()

                if (args.pkey is None):
                    decr = DecryptFile(input_, args.skey)
                else:
                    decr = Decrypt(input_, args.pkey)

                if decr.save(
                    out, b64=args.base64, replace_file=replace
                ):
                    print(f"Arquivo '{out}' salvo com sucesso!")
                    if (args.show):
                        print("SHOW: ")
                        print(decr.get())
                        print()
                else:
                    print(f"Falha ao salvar '{out}'")
    
            except Exception as e:
                print(f"ERRO: {e}")

def main():
    try:
        import rsa
        import cryptography

        DEPENDENCIES_OK = True
    except:
        DEPENDENCIES_OK = False

    if (DEPENDENCIES_OK):
        cli()
    else:
        print("Falha ao carregar as dependências: RSA & Cryptography")
        print("Instale:")
        print("  - pip install rsa")
        print("  - pip install cryptography")
