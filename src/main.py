from Block import *
from Blockchain import *
from Node import *
import time
import json

def __main__():
    t = Transaction(0, 10, time.time(), 20)
    print(json.dumps(t, default= encodeDef))

    chain = Blockchain()
    node = Node(chain)
    for i in range(0,6):
        chain.unconfirmed_transactions.append(Transaction(i, i+10, time.time(), i + 20))
    for i in range(0, 3):   
        successhash = node.mine()

    print(chain)
__main__()


