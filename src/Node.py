from Block import *

class Node(object):
    nonce = 0
    def __init__(self, blockchain):
        self.blockchain = blockchain
        pass

    def findHash(self, difficulty, block : Block)  -> str:
        successfulHash = False
        hash : str 
        while not successfulHash:
            hash : str= block.computeHash()
            if hash.startswith("0" * difficulty):
                successfulHash = True
            else:
                block.nonce += 1
        return hash

    def getNextBlock(self):
        #get a block with transactions
        pass

