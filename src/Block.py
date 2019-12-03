from hashlib import sha256
import json
import string


class Transaction(object):
    def __init__(self):
        print("created a transaction")
        pass
class Block(object):
    def __init__(self, index : int, transactions, timestamp, previousHash):
        self.index = index #check. it might be from the index
        self.transactions = transactions
        self.timestamp = timestamp
        self.previousHash = previousHash
        self.nonce = 0
        #selfHash : str

    def computeHash(self):
        print(self.__dict__)
        blockJsonStr = json.dumps(self.__dict__, sort_keys= True)
        return sha256(blockJsonStr.encode()).hexdigest()

    def __str__(self):
        return str(self.__dict__)
