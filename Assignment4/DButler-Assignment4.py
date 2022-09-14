'''
    DATA 602 - Assignment 4
    Blockchain & Crypto
	
    Donald Butler
    2022-04-02
    
    Version: 1.0
'''

import datetime as dt
import hashlib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import unittest
import uuid

def calc_hash(s):
    '''
    Calculates the hash of a given string

    Parameters
    ----------
    s : str
        string to be hashed.

    Returns
    -------
    str
        hash of the string.

    '''

    return hashlib.sha256(str(s).encode('utf-8')).hexdigest()

class PandasChain:
    '''
    Class representing a blockchain
    '''
    
    def __init__(self, name): 
        '''
        Constructor of the PandasChain class.

        Parameters
        ----------
        name : str
            name of the blockchain.

        Returns
        -------
        None.

        '''
        
        self.__name = name.upper()
        self.__chain = []
        self.__id = calc_hash(str(uuid.uuid4()) + self.__name + str(dt.datetime.now()))
        self.__seq_id = 0
        self.__prev_hash = None
        self.__current_block = Block(self.__seq_id, None)
        print(self.__name,'PandasChain created with ID',self.__id,'chain started.')
    
    def display_chain(self): 
        '''
        Displays the complete blockchain

        Returns
        -------
        None.

        '''
        
        for block in self.__chain:
            block.display_transactions()
        self.__current_block.display_transactions()
    
    def add_transaction(self, s, r, v): 
        '''
        Adds a transaction to the blockchain

        Parameters
        ----------
        s : str
            Sender of the coins.
        r : str
            Receiver of the coins.
        v : float
            Value of the coins transacted.

        Returns
        -------
        None.

        '''
        
        if self.__current_block.get_size() >= 10:
            self.__commit_block(self.__current_block)
        self.__current_block.add_transaction(s, r, v)
    
    def __commit_block(self,block): 
        '''
        Commits the current block to the chain and creates a new block

        Parameters
        ----------
        block : Block
            Current block to be committed to the chain.

        Returns
        -------
        None.

        '''

        ts = dt.datetime.now()
        merkle_hash = block.get_simple_merkle_root()
        block_hash = calc_hash(str(self.__prev_hash) + str(self.__id) + str(ts) + str(self.__seq_id) + str(np.random.randint(100)) + str(merkle_hash))
        block.set_block_hash(block_hash)
        block.set_status('COMMITTED')
        self.__chain.append(block)
        self.__seq_id += 1
        self.__prev_hash = block_hash
        self.__current_block = Block(self.__seq_id, self.__prev_hash)
        print('Block committed')
    
    def display_block_headers(self): 
        '''
        Displays the metadata for each block

        Returns
        -------
        None.

        '''

        for block in self.__chain:
            block.display_header()
        self.__current_block.display_header()
    
    def get_number_of_blocks(self): 
        '''
        Returns the number of blocks in the chain

        Returns
        -------
        int
            Number of blocks in the chain.

        '''

        return len(self.__chain) + 1
    
    def get_values(self):
        '''
        Returns a list of coin values in each transaction in the chain

        Returns
        -------
        value_list : list
            List of coin values transacted.

        '''
        
        value_list = []
        for block in self.__chain:
            value_list.append(block.get_values())
        value_list.append(self.__current_block.get_values())
        return value_list

class Block:
    '''
    Class representing a block of transactions in a blockchain.
    '''

    def __init__(self,seq_id,prev_hash): 
        '''
        Constructor for the Block class

        Parameters
        ----------
        seq_id : int
            Sequence number for the block.
        prev_hash : str
            hash of the previous block in the chain.

        Returns
        -------
        None.

        '''

        self.__seq_id = seq_id
        self.__prev_hash = prev_hash
        self.__col_names = ['Timestamp','Sender','Receiver','Value','TxHash']
        self.__transactions = pd.DataFrame(columns = self.__col_names)
        self.__status = 'UNCOMMITTED'
        self.__block_hash = None
        self.__merkle_tx_hash = None
        
    def display_header(self): 
        '''
        Displays the metadata for this block

        Returns
        -------
        None.

        '''
        print("{seq_id}, {status}, {block_hash}, {prev_hash}, {merkle}, {trans_count}".format( \
            seq_id = self.__seq_id, status = self.__status, block_hash = self.__block_hash, \
            prev_hash = self.__prev_hash, merkle = self.__merkle_tx_hash, trans_count = self.get_size()))
    
    def add_transaction(self, s, r, v): 
        '''
        Adds a transaction to the block

        Parameters
        ----------
        s : str
            Sender of the coins.
        r : str
            Receiver of the coins.
        v : float
            Value of the coins transacted.

        Returns
        -------
        None.

        '''

        ts = dt.datetime.now()
        tx_hash = calc_hash(str(ts) + str(s) + str(r) + str(v))
        new_transaction = pd.DataFrame(data=[{self.__col_names[0]:ts, self.__col_names[1]:s, self.__col_names[2]:r, self.__col_names[3]:v, self.__col_names[4]:tx_hash}])
        self.__transactions = self.__transactions.append(new_transaction)
        self.__merkle_tx_hash = calc_hash(self.__transactions['TxHash'].str.cat())
        
    def display_transactions(self): 
        '''
        Displays the transactions in the block

        Returns
        -------
        None.

        '''

        self.display_header()
        print(self.__transactions[['Timestamp','Sender','Receiver','Value']].to_string(index = False))
    
    def get_size(self): 
        '''
        Returns the number of transactions in the block

        Returns
        -------
        int
            Number of tranactions in the block.

        '''

        return self.__transactions.shape[0]
    
    def set_status(self, status):
        '''
        Sets the status of the block

        Parameters
        ----------
        status : str
            Sets the block status.

        Returns
        -------
        None.

        '''
        
        self.__status = status
    
    def set_block_hash(self, hash):
        '''
        Sets the block hash

        Parameters
        ----------
        hash : str
            calculated hash of the block.

        Returns
        -------
        None.

        '''

        self.__block_hash = hash
    
    def get_simple_merkle_root(self): 
        '''
        Returns the simple merkle root hash of the transactions in the block

        Returns
        -------
        str
            simple merkle root hash of the transactions in the block.

        '''

        return self.__merkle_tx_hash
    
    def get_values(self):
        '''
        Returns a list of coin values in the transactions of the block

        Returns
        -------
        list
            list of coin values in the transactions of the block.

        '''
        
        return self.__transactions['value'].tolist()

class TestAssignment4(unittest.TestCase):
    def test_chain(self):
        block = Block(1,"test")
        self.assertEqual(block.get_size(),0)
        block.add_transaction("Bob","Alice",50)
        self.assertEqual(block.get_size(),1)
        pandas_chain = PandasChain('testnet')
        self.assertEqual(pandas_chain.get_number_of_blocks(),1)
        pandas_chain.add_transaction("Bob","Alice",50)
        pandas_chain.add_transaction("Bob","Alice",51)
        pandas_chain.add_transaction("Bob","Alice",52)
        pandas_chain.add_transaction("Bob","Alice",53)
        pandas_chain.add_transaction("Bob","Alice",53)
        pandas_chain.add_transaction("Bob","Alice",53)
        pandas_chain.add_transaction("Bob","Alice",53)
        pandas_chain.add_transaction("Bob","Alice",53)
        pandas_chain.add_transaction("Bob","Alice",53)
        pandas_chain.add_transaction("Bob","Alice",53)
        pandas_chain.add_transaction("Bob","Alice",53)
        self.assertEqual(pandas_chain.get_number_of_blocks(),2)
        pandas_chain.add_transaction("Bob","Alice",50)
        pandas_chain.add_transaction("Bob","Alice",51)
        pandas_chain.add_transaction("Bob","Alice",52)
        pandas_chain.add_transaction("Bob","Alice",53)
        pandas_chain.add_transaction("Bob","Alice",53)
        pandas_chain.add_transaction("Bob","Alice",53)
        pandas_chain.add_transaction("Bob","Alice",53)
        pandas_chain.add_transaction("Bob","Alice",53)
        pandas_chain.add_transaction("Bob","Alice",53)
        pandas_chain.add_transaction("Bob","Alice",53)
        pandas_chain.add_transaction("Bob","Alice",53)
        self.assertEqual(pandas_chain.get_number_of_blocks(),3)

if __name__ == '__main__':
    unittest.main()

   
pc = PandasChain('donald')

pc.add_transaction("Bob","Alice",50)
pc.add_transaction("Bob","Alice",51)
pc.add_transaction("Bob","Alice",52)
pc.add_transaction("Bob","Alice",53)
pc.add_transaction("Bob","Alice",53)
pc.add_transaction("Bob","Alice",53)
pc.add_transaction("Bob","Alice",53)
pc.add_transaction("Bob","Alice",53)
pc.add_transaction("Bob","Alice",53)
pc.add_transaction("Bob","Alice",53)
pc.add_transaction("Bob","Alice",53)

pc.add_transaction("Bob","Alice",50)
pc.add_transaction("Bob","Alice",51)
pc.add_transaction("Bob","Alice",52)
pc.add_transaction("Bob","Alice",53)
pc.add_transaction("Bob","Alice",53)
pc.add_transaction("Bob","Alice",53)
pc.add_transaction("Bob","Alice",53)
pc.add_transaction("Bob","Alice",53)
pc.add_transaction("Bob","Alice",53)
pc.add_transaction("Bob","Alice",53)
pc.add_transaction("Bob","Alice",53)

pc.add_transaction("Bob","Alice",50)
pc.add_transaction("Bob","Alice",51)
pc.add_transaction("Bob","Alice",52)
pc.add_transaction("Bob","Alice",53)
pc.add_transaction("Bob","Alice",53)
pc.add_transaction("Bob","Alice",53)
pc.add_transaction("Bob","Alice",53)

pc.display_chain()
