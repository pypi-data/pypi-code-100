import os
import sys

PATH = os.path.join(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)), "src")
sys.path.append(PATH)


from winhye_common.utils import CookieRsa


def test_ras():
    obj = CookieRsa()
    # encrypt = obj.rsa_encrypt('text')
    decrypt = obj.rsa_decrypt("test")
    # print(encrypt)
    print(decrypt)


if __name__ == '__main__':
    test_ras()
