from Block import *
from Blockchain import *
from Node import *
import time
import json

def createTransactionsIntial(nTransactions):
    transactions = []
    for i in range(0,nTransactions):
        transactions.append(Transaction(i, i+10, time.time(), i + 20))
    return transactions

def __main__():
    t = Transaction(0, 10, time.time(), 20)
    tJson = """{"sender": 0, "receiver": 10, "timestamp": 1575457940.1777258, "amount": 20}"""
    t1Dict = json.loads(tJson)
    t1 = Transaction.decodeJson(t1Dict)
    print(type(t1))
    print(json.dumps(t, default= encodeDef))

    chain = Blockchain()
    node = Node(chain)

    for i in range(0, 3):   
        successhash = node.mine()
    t = createTransactionsIntial(1)
    print(str(json.dumps(t[0].__dict__, sort_keys=True)))
    #print(chain)
__main__()


