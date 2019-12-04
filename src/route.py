from flask import Flask, request
import requests
from Blockchain import *
import main


app = Flask(__name__)
chain = Blockchain()
main.setTransactions(chain)

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
    required_fields = ["author", "content"]

    for field in required_fields:
        if not tx_data.get(field):
            return "Invalid transaction data", 404

        tx_data["timestamp"] = time.time()
        chain.addNewTransaction(tx_data)

        return "success", 201

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

# @app.route('/mine', methods=['GET'])
# def mine_unconfirmed_transactions():
#     result = blockchain.mine()
#     if not result:
#         return "No transactions to mine"
#     return "Block #{} is mined.".format(result)
app.run(port=8000)