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
    chain.unconfirmed_transactions = createTransactionsIntial(6)
    tJson = json.dumps(chain.unconfirmed_transactions, default=encodeDef)
    tJsonl = json.loads(tJson)
    transactions : list = list()
    for t in tJsonl:
        transactions.append(Transaction.decodeJson(t))
    pass




