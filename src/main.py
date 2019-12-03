from Block import *
from Blockchain import *
from Node import *

def __main__():
    chain = Blockchain()
    node = Node(chain)
    successhash = node.mine()
    print(chain.provideNextBlock())

__main__()


