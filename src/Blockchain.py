from Block import *
import time
from collections import deque
import itertools


class Blockchain(object):
    def __init__(self, difficulty=3, lastBlockIndex=0, lastHash="", genesis=True):
        self.chain = []
        self.difficulty = difficulty
        self.unconfirmed_transactions : list = list()
        self.lastBlockIndex = lastBlockIndex
        self.lastHash = lastHash
        #start the chain
        if genesis:
            self.createGenesisBlock()
            self.lastBlockIndex = self.lastBlock.index
            self.lastHash = self.lastBlock.computeHash()

            
    @classmethod
    def fromJson(cls, jsonDict):
        c = json.loads(jsonDict) #chain dictionary
        chain : list = list()
        for block in c["chain"]:
            chain.append(Block.decodeJson(block))
        
        transactions : list = list()
        for t in c["unconfirmed_transactions"]:
            transactions.append(Transaction.decodeJson(t))

        blockchain : Blockchain= cls(difficulty=c["difficulty"], lastBlockIndex=c["lastBlockIndex"],lastHash=c["lastHash"], genesis=False) #dont need to create genesis block
        blockchain.chain = chain
        blockchain.unconfirmed_transactions = transactions
        return blockchain
    
    def getDifficulty(self):
        return self.difficulty

    def createGenesisBlock(self):
        genesisBlock = Block(0, [], time.time(), "0" * self.difficulty)
        def findHash(difficulty, block : Block)  -> str:
            successfulHash = False
            hash : str 
            while not successfulHash:
                hash = block.computeHash()
                if hash.startswith("0" * difficulty):
                    successfulHash = True
                else:
                    block.nonce += 1
            print(block)
            return hash
        findHash(self.difficulty, genesisBlock)
        self.chain.append(genesisBlock)

    def addNewTransactions(self, transactions):
        for transaction in transactions:
            self.unconfirmed_transactions.append(transaction)

    def getTransactions(self):
        #look in the pool and return transactions
        pass

    def addBlock(self, block : Block, hash):
        #verify previous hash is the same stored in the block
        previousHash = self.lastHash
        if previousHash != block.previousHash:
            return False
        #verify hash was correctly calculated
        if not Blockchain.verifyHashBlock(block, hash, self.difficulty):
            return False
        self.chain.append(block)
        self.removeTransactions(1) #hardcoded
        #block.selfHash = hash
        self.lastBlockIndex += 1
        self.lastHash = hash
        return True

    def removeTransactions(self, nTransactions): #removing the first n transactions in the list
        del self.unconfirmed_transactions[0:nTransactions] #delete the transactions. better to later implement as a queue to pop O(1)

    def setDifficulty(self, difficulty):
        self.difficulty = difficulty 
    @classmethod
    def verifyHashBlock(cls, block : Block, hash, difficulty):
        hashCalculated = block.computeHash()
        return hash.startswith("0" * difficulty) and hashCalculated == hash
    
    @classmethod
    def verifyValidity(cls, blockchain):
        previousHash = "0" * blockchain.difficulty
        for block in blockchain.chain:
            if previousHash != block.previousHash:
                return False
            previousHash = block.computeHash()
            if not cls.verifyHashBlock(block, previousHash, blockchain.difficulty):
                return False
        return True

    def getLastBlock(self):
        return self.chain[-1]

    def provideNextBlock(self):
        if not self.unconfirmed_transactions:
            return None
        #passing 2 transactions. no tests at the moment
        transactionsToBlock = self.unconfirmed_transactions[0:1]
        #listTransStr = json.dumps([self.unconfirmed_transactions[2].__dict__])
        block = Block(self.lastBlockIndex + 1, transactionsToBlock, time.time(), self.lastHash)
        return block
    
   


    #make sure that the blockchain is not tampered
    #def verifyWholeChain
    
    def __str__(self):
        s = ""
        for block in self.chain:
            s = s + str(block) + "\n"
        return s

    @property
    def lastBlock(self) -> Block:
        return self.chain[-1]