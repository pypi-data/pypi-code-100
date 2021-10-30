import hashlib
import random 

nonce_limit = 1000000000

zeroes = random.randint(1, 100)

def mine(block_num, transaction_hash, previous_hash):
    for nonce in range(nonce_limit):
        base_text = str(block_num) + transaction_hash + previous_hash + str(nonce)
        hash_try = hashlib.sha256(base_text.encode()).hexdigest()
        if hash_try.startswith('0' * zeroes):
            print("Found hash with nonce: {}".format(nonce))
            return hash_try
    
    return None 





block_number = 24 
transactions = '761234fcc142'
previous_hash = "876de8756b967c87"

print(mine(block_number, transactions, previous_hash))
