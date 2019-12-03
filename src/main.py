from Block import *
from Blockchain import *
from Node import *

def __main__():
    chain = Blockchain()
    node = Node(chain)
    block1 = chain.last_block
    successhash = node.findHash(1, block1)
    print(successhash)

__main__()


