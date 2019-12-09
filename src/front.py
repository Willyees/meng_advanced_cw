import datetime
import json
import requests
from flask import render_template, redirect, request



BLOCKCHAIN_ADDRESS = "http://127.0.0.1:8000"
posts = []

def fetchPosts():
    getChainAddress = "{}/chain".format(BLOCKCHAIN_ADDRESS)
    response = requests.get(getChainAddress)
    if response.status_code == 200:
        content = []
        chain = json.loads(response.content)
        for block in chain["chain"]:
            for transaction in block["transactions"]:
                transaction["index"] = block["index"]
                transaction["hash"] = block["previousHash"]
                content.append(transaction)
        global posts
        posts = sorted(content, key=lambda k : k['timestamp'], reverse=True)

@app.route('/submit', methods=['POST'])
def submitTextArea():
   """
   create transaction with a form
   """ 
   postAmount = request.form["amount"]
   sender = request.form["author"]

   postObject = {
       'sender' : sender, 'amount' : postAmount
   }

   #submit a transaction
   newTransactionaddress = "{}/newTransaction".format(BLOCKCHAIN_ADDRESS)
   requests.post(newTransactionAddress, json=postObject, headers={'Content-type': 'application/json'})

   return redirect('/')

app.run(port=8000)