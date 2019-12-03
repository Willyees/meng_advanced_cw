from Block import *
import time

class Blockchain(object):
    def __init__(self):
        self.chain = []
        self.createGenesisBlock()
        self.difficulty = 0
        self.lastBlockIndex = self.lastBlock.index
        self.lastHash = self.lastBlock.computeHash()
        self.unconfirmed_transactions = []
        

    def getDifficulty(self):
        return self.difficulty

    def createGenesisBlock(self):
        genesisBlock = Block(0, [], time.time(), "0")
        self.chain.append(genesisBlock)

    def addNewTransactions(self, transactions):
        for transaction in transactions:
            self.unconfirmed_transactions.append(transaction)

    def getTransactions(self):
        #look in the pool and return transactions
        pass

    def addBlock(self, block : Block, hash):
        #verify previous hash is the same stored in the block
        previousHash = self.lastBlock
        if previousHash != block.previousHash:
            return False
        #verify hash was correctly calculated
        if not self.verifyHashBlock(block, hash):
            return False
        self.chain.append(block)
        #block.selfHash = hash
        self.lastBlockIndex += 1
        self.lastHash = hash
        return True
        

    def setDifficulty(self, difficulty):
        self.difficulty = difficulty 

    def verifyHashBlock(self, block : Block, hash):
        hashCalculated = block.computeHash()
        return hash.startswith("0" * self.difficulty) and hashCalculated == hash
   
    def provideNextBlock(self) -> Block:
        block = Block(self.lastBlockIndex + 1, self.unconfirmed_transactions, time.time(), self.lastHash)
        return block

    def printChain(self):
        for block in self.chain:
            print(block)
            
    @property
    def lastBlock(self) -> Block:
        return self.chain[-1]