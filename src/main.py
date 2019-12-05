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
    chain = Blockchain()
    node = Node(chain)
    chain.unconfirmed_transactions.append(createTransactionsIntial(6))
    for i in range(0, 3):   
        successhash = node.mine()
    print(chain.__dict__)
    print(type(json.dumps(chain.__dict__, default=encodeDef)))
    #print(chain)
__main__()


