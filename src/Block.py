from hashlib import sha256
import json


class Transaction(object):
    def __init__(self):
        print("created a transaction")
        pass
class Block(object):
    def __init__(self, index, transactions, timestamp):
        self.index = [] #check. it might be from the index
        self.transactions = transactions
        self.timestamp = timestamp
        self.nonce = 0
        selfHash : str

    def computeHash(self):
        print(self.__dict__)
        blockJsonStr = json.dumps(self.__dict__, sort_keys= True)
        return sha256(blockJsonStr.encode()).hexdigest()
