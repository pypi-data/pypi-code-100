import cryptocode

def encrypt(text, key):
    str_encoded = cryptocode.encrypt(text, key)
    return str_encoded

def decrypt(encrypted_text, key):
    str_decoded = cryptocode.decrypt(encrypted_text, key)
    return str_decoded