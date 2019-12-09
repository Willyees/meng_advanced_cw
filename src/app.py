from flask import Flask, request, render_template
import requests
import json
import grequests

CONNECTED_NODE_ADDRESS = "http://127.0.0.1:8000"
peers = set({'http://127.0.0.1:8000'})
app = Flask("__name__")

@app.route('/', methods=['GET'])
def index():
    return render_template('home.html',node_addess = CONNECTED_NODE_ADDRESS)

@app.route('/mine', methods=['GET'])
def mine():
    for p in peers:
        response =requests.get("{}/mine".format(p))
        z = response.content
    #should be using grequest because now it waits that each node mines their block
    # rs = (grequests.get(u) for u in peers)
    # r = grequests.map(rs)
    pass
    return response.content, response.status_code

@app.route('/set-peers', methods=['GET'])
def getPeers():
    response = requests.get("{}/peers".format(CONNECTED_NODE_ADDRESS))
    d1 = response.content
    d = list(response.content)
    s = set()
    # for z in d1:
    #     s.update(z)
    # for k in d:
    #     pass
    responseJson = response.json()
    for p in responseJson:
        peers.update([p])
    return "Ok"

@app.route('/submit', methods=['POST'])
def submit():
    keys = ["sender","receiver","amount"]
    if not all(needed in request.form for needed in keys):
        return "Missing argument in the post request. Needed sender, receiver, amount"
    sender = request.form["sender"]
    receiver = request.form["receiver"]
    amount = request.form["amount"]
    dct = {"sender":sender, "receiver":receiver, "amount":amount}
    #send request to the main node holding the transactions
    nodeAddress = "{}/new-transaction".format(CONNECTED_NODE_ADDRESS)
    print(dct)
    requests.post(nodeAddress, data=json.dumps(dct), headers= {'Content-type': 'application/json'})
    return "Success", 200

app.run(port=5000)