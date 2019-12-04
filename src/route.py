from flask import Flask, request
import requests
from Blockchain import *
import main

#transaction example
#{"sender": 0, "receiver": 10, "timestamp": 1575457940.1777258, "amount": 20}

#block example


app = Flask(__name__)
chain = Blockchain()
peers = []
transactionsIntial = main.createTransactionsIntial(6)
chain.unconfirmed_transactions.append(transactionsIntial)

@app.route('/new-ttransaction')
def new_transaction_parameters():
    sender = request.args.get("sender") #if not exists returns None
    receiver = request.args.get("receiver")
    timestamp = request.args.get("timestamp")
    amount = request.args.get("amount")
    transaction = Transaction(sender, receiver, timestamp, amount) #http://127.0.0.1:8000/new-ttransaction?sender=0&receiver=1&timestamp=1575419338.4732528&amount=15
    chain.addNewTransactions([transaction])
    
    return "Got your transaction: " + str(transaction.__dict__)

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
def get_chain():
    chainData = []
    for block in chain.chain:
        chainData.append(chain.__dict__)
        return json.dumps({"length" : len(chain.chain), 
        "chain" : chainData}, default=encodeDef)

@app.route('/unconfirmed-transactions')
def getUnconfTransactions():
    return json.dumps(chain.unconfirmed_transactions, default=encodeDef)

@app.route('/add-node', methods=['POST'])
def registerNewNode():
    nodesJson = request.get_json()
    if not nodesJson:
        return "Invalid data", 400
        for node in nodesJson:
            peers.add(node)
        return "Success", 201
#todo decide which chain to keep in case longer valid chain is found
#def consensus():

@app.route('/add-block', methods=['POST'])
def addBlock():
    blockJson = request.get_json()
    block = json.loads(blockJson)
    #block = Block(blockJson["index"], blockJson["transactions"], blockJson["timestamp"], blockJson["previousHash"])
    hash = blockJson["hash"]
    if not chain.verifyHashBlock(block, hash):
        return "Block was not added to the chain", 400
    provideNewBlock()
    return "Success, block added to the chain", 201

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
app.run(port=8000)

#https://scotch.io/bar-talk/processing-incoming-request-data-in-flask
#mention to postman and how to use it