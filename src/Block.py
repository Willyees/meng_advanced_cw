from hashlib import sha256
import json
import string


class Transaction(object):
    def __init__(self, sender, receiver, timestamp, amount):
        self.sender = sender
        self.receiver = receiver
        self.timestamp = timestamp
        self.amount = amount
    
    @classmethod
    def decodeJson(cls, dct):
        return cls(dct["sender"], dct["receiver"], dct["timestamp"], dct["amount"])

    def getJson(self):
        return json.dumps(self.__dict__, sort_keys = True)

    
    def __str__(self):
        return str(self.__dict__)

class Block(object):
    def __init__(self, index : int, transactions, timestamp, previousHash, nonce=0):
        self.index = index #check. it might be from the index
        self.transactions : list = transactions
        self.timestamp = timestamp
        self.previousHash = previousHash
        self.nonce = nonce
        #selfHash : str

    @classmethod
    def decodeJson(cls, dct):
        transactions = list()
        transactionsdir : dict = dct["transactions"]
        if len(transactionsdir) == 0:
            pass
        for t in transactionsdir:
            transactions.append(Transaction.decodeJson(t))
        return cls(dct["index"], transactions, dct["timestamp"], dct["previousHash"], dct["nonce"])      

    def computeHash(self):
        blockJsonStr = json.dumps(self.__dict__, default= encodeDef, sort_keys= True)
        return sha256(blockJsonStr.encode()).hexdigest()

    def __str__(self):
        return str(self.__dict__)

def encodeDef(o):
    if isinstance(o, Transaction):
        return o.__dict__
    if isinstance(o, Block):
        return o.__dict__
    else:
        typeName = o.__class__.__name__
        raise TypeError(f"Object of type '{type_name}' is not JSON serializable!")
