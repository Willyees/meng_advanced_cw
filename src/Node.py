from Block import *
from Blockchain import *

class Node(object):
    nonce = 0
    def __init__(self, blockchain : Blockchain):
        self.blockchain = blockchain
        pass

    def findHash(self, difficulty, block : Block)  -> str:
        successfulHash = False
        hash : str 
        while not successfulHash:
            hash = block.computeHash()
            if hash.startswith("0" * difficulty):
                successfulHash = True
            else:
                block.nonce += 1
        return hash

    def getNextBlock(self):
        #get a block with transactions
        pass

    def mine(self):
        #get next block to mine from blockchain
        block = self.blockchain.provideNextBlock()
        if block == None:
            print("No transactions available")
            return None
        hash = self.findHash(self.blockchain.getDifficulty(), block)
        self.blockchain.addBlock(block, hash)
        return hash


