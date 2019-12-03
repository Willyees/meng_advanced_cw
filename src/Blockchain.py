from Block import *
import time

class Blockchain(object):
    def __init__(self):
        self.chain = []
        self.createGenesisBlock()
        self.difficulty = 0
        self.lastBlockIndex = 0
        
    def getLastBlock(self):
        self.last_block()
        return 0

    def createGenesisBlock(self):
        genesisBlock = Block(0, [], time.time())
        self.chain.append(genesisBlock)

    def getTransactions(self):
        #look in the pool and return transactions
        pass

    def addBlock(self):
        self.blockCount += 1
        #add block

    def setDifficulty(self, difficulty):
        self.difficulty = difficulty  

    @property
    def last_block(self):
        return self.chain[-1]

chain = Blockchain()
chain.getTransactions()
