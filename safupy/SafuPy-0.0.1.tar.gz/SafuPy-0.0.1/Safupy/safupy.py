from cryptography.hazmat.primitives.kdf.scrypt import Scrypt
import base64
from cryptography.fernet import Fernet


class Safu:
    """
    Creates a Safu object, which takes 2 required arguments, password and salt.
    You can also specify length (int) – The desired length of the derived key
    in bytes, n (int) – CPU/Memory cost parameter.
    It must be larger than 1 and be a power of 2,
    r (int) – Block size parameter, p (int) – Parallelization parameter.
    """

    def __init__(
        self,
        salt: bytes,
        password: str,
        length: int = 32,
        n: int = 2 ** 14,
        r: int = 8,
        p: int = 1,
    ):
        self.salt = salt
        self.password = password
        self.length = length
        self.n = n
        self.r = r
        self.p = p

    def encryptdata(self, data):
        """
        Takes one required argument (data to encrypt). Returns encryped data as token.
        """

        kdf = Scrypt(salt=self.salt, length=self.length, n=self.n, r=self.r, p=self.p)
        frenkey = base64.urlsafe_b64encode(kdf.derive(bytes(self.password, "utf-8")))
        f = Fernet(frenkey)
        token = f.encrypt(bytes(data, "utf-8"))
        return token

    def decryptdata(self, token):
        """
        Takes one required argument (token to decrypt). Returns data as cleartext of given token.
        """

        kdf = Scrypt(salt=self.salt, length=self.length, n=self.n, r=self.r, p=self.p)
        frenkey = base64.urlsafe_b64encode(kdf.derive(bytes(self.password, "utf-8")))
        f = Fernet(frenkey)
        return f.decrypt(token).decode('utf-8')

    def hashpw(self):
        """
        Returns password's salted hash.
        """

        kdf = Scrypt(salt=self.salt, length=self.length, n=self.n, r=self.r, p=self.p)
        key = kdf.derive(bytes(self.password, "utf-8"))
        return key

    def cmphash(self, key):
        """
        Takes one required argument (password hash). Returns True if password is correct, False if incorrect.
        """
        kdf = Scrypt(salt=self.salt, length=self.length, n=self.n, r=self.r, p=self.p)
        try:
            kdf.verify(bytes(self.password, "utf-8"), key)
        except:
            return False
        else:
            return True
