__version__ = '0.1.1'
__author__ = 'Vitor Gabriel <edvitor13@hotmail.com>'
__date__ = '2021-10-25'
__lang__ = 'pt-br'

"""Dencrypt

Módulo criado com o objetivo de gerar de forma rápida
a criptografia de textos e arquivos.

Utiliza como base as criptografias: 
    - RSA (Assimétrica)
      - Encrypt (Chave Pública)/Decrypt (Chave Privada)
      - Lento; Uso recomendado em conteúdo com tamanho máximo de 256 bytes
    
    - Fernet (Simétrica)
      - EncryptFile (Chave Única)/DecryptFile (Chave Única)
      - Rápido; Uso recomendado para arquivos
"""

from .core import Crypt, Encrypt, Decrypt, EncryptFile, DecryptFile
