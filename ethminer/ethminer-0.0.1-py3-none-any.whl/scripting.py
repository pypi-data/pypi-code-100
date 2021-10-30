from ether_scan import ether_base
import time 


class Script:
    blocks = []

    global_connection = None
    
    def connect_chain(self):
        ether_base.infura_url_setter()
        connection_status = ether_base.connection()
        if connection_status == False:
            self.global_connection = False
            return False 
        else:
            self.global_connection = True
            return True 

    def get_top_block(self):
        if not self.global_connection == True:
            return "Error - No Connection to Chain"
        latest_block = ether_base.get_latest_block()
        self.blocks.append(latest_block)
        return latest_block 

    def get_multiple_blocks(self):
        if not self.global_connection == True:
            return "Error - No Connection to Chain"
        num = int(input('Please type in the number of latest blocks you would like to see: '))
        blocks = ether_base.get_multiple_blocks(num)

        for block in blocks:
            self.blocks.append(block)

    def view_blocks(self):
        if not self.global_connection == True:
            return "Error - No Connection to Chain"
        return self.blocks

    def mine(self, block_num, from_account_hash, transaction_hash, previous_hash, difficulty):
        nonce_limit = self.web3.eth.getTransactionCount(from_account_hash)
        for nonce in range(nonce_limit):
            base_text = str(block_num) + str(transaction_hash) + str(previous_hash) + str(nonce)
            hash_try = haslib.sha256(base_text.encode()).hexdigest()
            if hash_try.startswith('0' * difficulty):
                print('Found hash with nonce: {}'.format(nonce))
                return hash_try

        return None     

                    
                    




                
        
        
