from cryptography.fernet import Fernet, InvalidToken
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives.kdf.scrypt import Scrypt
from cryptography.hazmat.primitives import hashes
from getpass import getpass
import base64
import pyperclip
import secrets
import sys
import click
import os

SALT_LENGTH = 16

def get_identity_folder():
    return click.get_app_dir("PasswordStore")

def get_identity_path():
    return os.path.join(get_identity_folder(), "identity")

def get_identity():
    """
    Fetches identity from a file
    :return: bytes of the identity
    """
    try:
        with open(get_identity_path(), "rb") as f:
            return f.read()
    except FileNotFoundError:
        return None
    except PermissionError:
        print("ERROR: permission denied, cannot read the identity!", file=sys.stderr)
        sys.exit(1)


# https://cryptography.io/en/latest/fernet/#using-passwords-with-fernet
def get_fernet_key_from_password(password, salt):
    """
    Generates a key for use in Fernet from user specified string
    :param password: user specified password
    :param salt: random array of bytes to be added to the password
    :return: bytes containing a key for Fernet
    """
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000)
    key = base64.urlsafe_b64encode(kdf.derive(bytes(password, 'utf-8')))
    return key


def create_identity():
    """
    Handles creating a new identity for the user
    :return: None
    """
    # Ask for a password twice and make sure they match
    pass1 = getpass("Enter master password for your new identity: ")
    pass2 = getpass("Repeat master password for your new identity: ")
    if pass1 != pass2:
        print("ERROR: passwords differ, try again!", file=sys.stderr)
        sys.exit(1)

    # salt is not important since we would store it in clear text anyway
    password_key = get_fernet_key_from_password(pass1, bytes())
    # identity_salt is the secret component in password generation
    identity_salt = secrets.token_bytes(SALT_LENGTH)
    f = Fernet(password_key)
    # Encrypt identity salt using fernet key derived from password
    token = f.encrypt(identity_salt)
    # Store encrypted identity_salt
    try:
        try:
            os.makedirs(get_identity_folder())
        except FileExistsError:
            pass
        
        with open(get_identity_path(), "wb") as f:
            f.write(token)
    except PermissionError:
        print("ERROR: dont have the permission to write the identity!", file=sys.stderr)
        sys.exit(1)
    print("Identity created successfully! (stored at %s)" % get_identity_path())


def get_identity_salt(identity, password):
    """
    :param identity: bytes stored in the identity
    :param password: password used to encrypt this identity
    :return:
    """
    password_key = get_fernet_key_from_password(password, bytes())
    f = Fernet(password_key)
    identity_salt = None
    # Try to decrypt the identity_salt
    try:
        identity_salt = f.decrypt(identity)
    except InvalidToken:
        print("ERROR: wrong password!", file=sys.stderr)
        sys.exit(1)
    return identity_salt


def derive_password(identifier, identity_salt):
    """
    :param identifier: string containing password name
    :param identity_salt: encrypted property of the identity
    :return: string containing a password
    """
    kdf = Scrypt(
        salt=identity_salt,
        length=16,
        n=2**14,
        r=8,
        p=1,
    )

    result = base64.b85encode(kdf.derive(bytes(identifier, 'utf-8')))
    return result.decode("ascii")

@click.command()
def cli():
    identity = get_identity()
    if identity:
        password = getpass("Enter master password for your identity: ")
        identity_salt = get_identity_salt(identity, password)
        identifier = input("Password identifier: ")
        pyperclip.copy(derive_password(identifier, identity_salt))
        print("Password was copied into your clipboard")
    else:
        create_identity()


if __name__ == "__main__":
    cli()
