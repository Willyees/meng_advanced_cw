from flask import Flask, request
import requests
from Blockchain import *
from main import createTransactionsIntial

#transaction example
#{"sender": 0, "receiver": 10, "timestamp": 1575457940.1777258, "amount": 20}

#block example


app = Flask(__name__)
chain = Blockchain()
peers = set()
transactionsIntial = createTransactionsIntial(6)
for t in transactionsIntial:
    chain.unconfirmed_transactions.append(t)

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
    tx_data = request.get_json()#using transaction with json format. Have to transform in Transaction obj
    required_fields = ["sender", "receiver", "amount"]

    for field in required_fields:
        if tx_data.get(field) == None:
            return "Invalid transaction data", 404

    tx_data["timestamp"] = time.time()
    
    transaction = Transaction.decodeJson(tx_data)
    chain.addNewTransactions([transaction])

    return "success" + str(transaction), 201

@app.route('/chain', methods=['GET'])
def getChain():
    chainData = []
    for block in chain.chain:
        chainData.append(block.__dict__)
    return json.dumps({"length" : len(chain.chain), 
        "chain" : chainData}, default=encodeDef)

@app.route('/unconfirmed-transactions', methods=['GET'])
def getUnconfTransactions():
    return json.dumps(chain.unconfirmed_transactions, default=encodeDef)


#todo decide which chain to keep in case longer valid chain is found
#def consensus():

@app.route('/add-block', methods=['POST'])
def addBlock():
    blockJson = request.get_json()
    block = json.loads(blockJson)
    #block = Block(blockJson["index"], blockJson["transactions"], blockJson["timestamp"], blockJson["previousHash"])
    hash = blockJson["hash"] #have to pass also the hash from the node
    if not chain.verifyHashBlock(block, hash):
        return "Block was not added to the chain", 400
    provideNewBlock()
    return "Success, block added to the chain", 201

@app.route('/contact-peers')
def contact_peers():
    provideNewBlock()

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
    global chain 
    chainJson = json.dumps(chain.__dict__, sort_keys=True, default=encodeDef) 
    print(chainJson)
    return chainJson, 200 #plus return the chain to the newly added node #return getChain()


#other nodes that want to register with main blockchain node
@app.route('/register-with', methods=['POST'])
def registerNodeWith():
    hostAddress = request.get_json()["address"]
    if not hostAddress:
        return "Empty host address", 400
    #request to register with the host
    data = {"address" : request.host_url}
    header = {'Content-Type': "application/json"}
    response : Response = requests.post(hostAddress + "/add-node", data=json.dumps(data), headers=header)

    #get the chain from the reponse in case it was successful
    if response.status_code == 200:
        chainHostJson = response.json()#['chain'] #not only the chain in needed, aslo difficulty etc
        chainHostStr : str = str(chainHostJson)
        print(chainHostStr)
        blockchain = Blockchain.fromJson(chainHostStr.replace("'", "\""))
        global chain
        print(blockchain)
        chain = blockchain
        print(chain)
        #peers.update(response.json()['peers']) #dont need to update the nodes because this function is only called from nodes and not the main blockchain
        return "Success", 200
    else:
        return response.content, response.status_code #problem in adding the node to the host


#call after every block is mined
def provideNewBlock():
    for peer in peers:
        url = "http://{}/add-block".format(peer)
        requests.post(url, data=json.dumps(block.__dict__, sort_keys=True))
# @app.route('/mine', methods=['GET'])
# def mine_unconfirmed_transactions():
#     result = blockchain.mine()
#     if not result:
#         return "No transactions to mine"
#     return "Block #{} is mined.".format(result)

#https://scotch.io/bar-talk/processing-incoming-request-data-in-flask
#mention to postman and how to use it

#debug show the peers connected
@app.route('/peers', methods=['GET'])
def show_peers_connected():
    return str(peers)

app.run(port=8000)