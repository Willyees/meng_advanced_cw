from hashlib import sha256
import json
import string


class Transaction(object):
    def __init__(self, sender, receiver, timestamp, amount):
        self.sender = sender
        self.receiver = receiver
        self.timestamp = timestamp
        self.amount = amount
        print("created a transaction")
    
    def getJson(self):
        return json.dumps(self.__dict__, sort_keys = True)

class Block(object):
    def __init__(self, index : int, transactions, timestamp, previousHash):
        self.index = index #check. it might be from the index
        self.transactions = transactions
        self.timestamp = timestamp
        self.previousHash = previousHash
        self.nonce = 0
        #selfHash : str

    def computeHash(self):
        blockJsonStr = json.dumps(self.__dict__, default= encodeDef, sort_keys= True)
        return sha256(blockJsonStr.encode()).hexdigest()

    def __str__(self):
        return str(self.__dict__)

def encodeDef(o):
    if isinstance(o, Transaction):
        return o.__dict__
    else:
        typeName = o.__class__.__name__
        raise TypeError(f"Object of type '{type_name}' is not JSON serializable!")