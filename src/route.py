from flask import Flask, request
import requests
from Blockchain import *
from Node import *
from main import createTransactionsIntial

#transaction example
#{"sender": 0, "receiver": 10, "timestamp": 1575457940.1777258, "amount": 20}

#block example


app = Flask(__name__)
node = Node(Blockchain())
peers = set()
transactionsIntial = createTransactionsIntial(6)
transactionsNodeAddress = ""

for t in transactionsIntial:
    node.blockchain.unconfirmed_transactions.append(t)

# @app.route('/new-ttransaction')
# def new_transaction_parameters():
#     sender = request.args.get("sender") #if not exists returns None
#     receiver = request.args.get("receiver")
#     timestamp = request.args.get("timestamp")
#     amount = request.args.get("amount")
#     transaction = Transaction(sender, receiver, timestamp, amount) #http://127.0.0.1:8000/new-ttransaction?sender=0&receiver=1&timestamp=1575419338.4732528&amount=15
#     chain.addNewTransactions([transaction])
#   
#    return "Got your transaction: " + str(transaction.__dict__)

@app.route('/new-transaction', methods = ['POST'])
def new_transaction():
    tx_data : Requests = request.get_json()#using transaction with json format. Have to transform in Transaction obj
    required_fields = ["sender", "receiver", "amount"]
    for field in required_fields:
        if tx_data.get(field) == None:
            return "Invalid transaction data", 404

    if transactionsNodeAddress != "": #means that this node is connected to the network and will not be storing transactions by itself
    #send the info to the main node storing transactions (pool)
        requests.post(transactionsNodeAddress + "/new-transaction", data=json.dumps(tx_data), headers=request.headers)
        return "This node is not the designated node to be a transaction pool"
    r = request
    tx_data["timestamp"] = time.time()
    transaction = Transaction.decodeJson(tx_data)
    node.blockchain.addNewTransactions([transaction])

    return "success" + str(transaction), 200

@app.route('/chain', methods=['GET'])
def getChain():
    chainData = []
    for block in node.blockchain.chain:
        chainData.append(block.__dict__)
    return json.dumps({"length" : len(node.blockchain.chain), 
        "chain" : chainData, "peers" : list(peers)}, default=encodeDef)

@app.route('/unconfirmed-transactions', methods=['GET'])
def showUnconfTransactions():
    p = json.dumps(node.blockchain.unconfirmed_transactions, default=encodeDef)
    return p


#todo decide which chain to keep in case longer valid chain is found
#def consensus():

@app.route('/add-block', methods=['POST'])
def addBlock():
    blockJson = request.get_json()
    blockStr = json.loads(str(blockJson).replace("'", "\""))
    block = Block.decodeJson(blockStr)
    #block = Block(blockJson["index"], blockJson["transactions"], blockJson["timestamp"], blockJson["previousHash"])
    hash = blockJson["hash"] #have to pass also the hash from the node
    if not node.blockchain.addBlock(block, hash):
        print("Block was not added to the chain")
        return "Block was not added to the chain", 400
    print("block was added to chain")
    return "Success, block added to the chain", 201

@app.route('/contact-peers')
def contact_peers():
    propagateNewBlock()

#adding a single node. Not multiple as it was before
@app.route('/add-node', methods=['POST'])
def registerNewNode():
    nodesJson = request.get_json()["address"]
    
    #endpoint= request.remote_addr
    #urlr = request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
    response = requests.get('http://127.0.0.1:8000/chain')
    if not nodesJson:
        return "Invalid data", 400
    peers.add(nodesJson)
    dct = node.blockchain.__dict__.copy()
    dct["peers"] = list(peers)
    chainJson = json.dumps(dct, sort_keys=True, default=encodeDef) 
    return chainJson, 200 #plus return the chain to the newly added node #return getChain()


#other nodes that want to register with main blockchain node
@app.route('/register-with', methods=['POST'])
def registerNodeWith():
    clientAddress = request.get_json()["address"]
    if not clientAddress:
        return "Empty host address", 400
    #request to register with the host
    data = {"address" : request.host_url.rstrip('/')}
    print("****")
    print(data)
    header = {'Content-Type': "application/json"}
    response : Response = requests.post(clientAddress + "/add-node", data=json.dumps(data), headers=header)

    #get the chain from the reponse in case it was successful
    if response.status_code == 200:
        chainHostJson = response.json() #not only the chain in needed, aslo difficulty etc
        chainHostStr : str = str(chainHostJson)
        #print(chainHostStr)
        blockchain = Blockchain.fromJson(chainHostStr.replace("'", "\""))
        global node
        global peers
        peers.update(response.json()['peers'])
        node.blockchain = blockchain
        global transactionsNodeAddress
        transactionsNodeAddress = clientAddress
        peers.update([clientAddress]) #store the pool as peer
        #print("**ASD" + clientAddress)
        #peers.update(response.json()['peers']) #dont need to update the nodes because this function is only called from nodes and not the main blockchain
        return "Success", 200
    else:
        return response.content, response.status_code #problem in adding the node to the host

#call after every block is mined
def propagateNewBlock(hash):
    for peer in peers:
        url = "{}/add-block".format(peer)
        headers = {'Content-Type': "application/json"}
        print("contacting other peers to propagate")
        dct = node.blockchain.getLastBlock().__dict__.copy()
        dct["hash"] = hash
        requests.post(url, data=json.dumps(dct, sort_keys=True, default=encodeDef), headers=headers)

# @app.route('/while')
# def longwait():
#     init = time.time()
#     while time.time() < (init + 20.0):
#         pass

@app.route('/mine', methods=['GET'])
def mine_unconfirmed_transactions():
    setUnconfTransactions()
    hash = node.mine()
    if not hash:
        return "No transactions to mine"
    propagateNewBlock(hash)
    return "Block #{} is mined.".format(hash)
    

#https://scotch.io/bar-talk/processing-incoming-request-data-in-flask
#mention to postman and how to use it

#get the unconfirmed transactions from the pool node. If this is the pool node, dont do anything
def setUnconfTransactions():
    if transactionsNodeAddress != "":
        response = requests.get('{}/unconfirmed-transactions'.format(transactionsNodeAddress))
        transactionsJson = response.json()
        # transactions = json.loads(transactionsJson) #should be a dict type
        # print(type(transactions))
        # global chain
        node.blockchain.unconfirmed_transactions.clear() #clear from all previous transactions. Not the best move
        for t in transactionsJson:
            node.blockchain.unconfirmed_transactions.append(Transaction.decodeJson(t))
    return showUnconfTransactions(), 200

#debug show the peers connected
@app.route('/peers', methods=['GET'])
def show_peers_connected():
    return str(peers)

@app.route('/test')
def test():
    return setUnconfTransactions()
app.run(port=8000)