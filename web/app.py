from flask import Flask, jsonify, request
from flask_restful import Api, Resource
from pymongo import MongoClient
import bcrypt

app = Flask(__name__)
api = Api(app)

client = MongoClient("mongodb://db:27017")
db = client.BankApi # database

users = db["users"] # collection

# helper functions
def userExists(username):
    if users.find({"username": username}).count() == 0:
        return False
    else:
        return True

def verifypw(username, password):
    hashed_pw = users.find({
        "username" : username
    })[0]["password"]

    if bcrypt.hashpw(password.encode('utf8'), hashed_pw) == hashed_pw:
        return True
    else:
        return False

def countTokens(username):
    num_tokens = users.find({
        "username" : username
    })[0]["tokens"]
    return num_tokens

def getcash(username):
    cash = users.find({
            "username" : username
        })[0]["cash"]
    return cash

def getdebt(username):
    debt = users.find({
            "username" : username
        })[0]["debt"]
    return debt

def makeJson(statuscode, message):
    retJson = {
        "statuscode" : statuscode,
        "message" : message
    }
    return retJson

def updatecash(username, amount):
    cash = getcash(username)
    cash = cash + amount
    users.update(
        {"username" : username},
        {
            "$set":{
                "cash": cash
            }
        }
    )

def updatedebt(username, amount):
    debt = getdebt(username)
    debt = debt + amount
    users.update(
        {"username" : username},
        {
            "$set":{
                "debt": debt
            }
        }
    )
    

# resources
class Register(Resource):
    def post(self):
        namepass = request.get_json()
        username = namepass["username"]
        password = namepass["password"]

        if userExists(username):
            retJson = makeJson(301, "User Already Exists")
            return jsonify(retJson)

        hashed_pw = bcrypt.hashpw(password.encode('utf8'), bcrypt.gensalt())

        users.insert({ 
            "username" : username,
            "password" : hashed_pw,
            "cash" : 0,
            "debt" : 0
        })
        
        retJson = makeJson(200, "Your account is now set up")
        return jsonify(retJson)


class Add(Resource):
    def post(self):
        namepassamt = request.get_json()
        username = namepassamt["username"]
        password = namepassamt["password"]
        amount = namepassamt["amount"]

        if not userExists(username):
            retJson = makeJson(301, "Invalid username")
            return jsonify(retJson)

        correct_pw = verifypw(username, password)
        if not correct_pw :
            retJson = makeJson(302, "Incorrect password")
            return jsonify(retJson)

        if amount < 0 :
            retJson=makeJson(304, "You have entered a negative amount. Please re-enter a positive amount")
            return jsonify(retJson)

        # charge $1 as a service fee
        updatecash(username, amount-1)
        updatecash("bank", 1)

        retJson = makeJson(200, "Amount added to your existing cash")
        return jsonify(retJson)

class Check(Resource):
    def post(self):
        namepass = request.get_json()
        username = namepass["username"]
        password = namepass["password"]

        if not userExists(username):
            retJson = makeJson(301, "Invalid username")
            return jsonify(retJson)

        correct_pw = verifypw(username, password)
        if not correct_pw :
            retJson = makeJson(302, "Incorrect password")
            return jsonify(retJson)

        retJson = users.find({
            "username" : username
        }, {
            "password" : 0,
            "_id" : 0
            }
        )[0]
        return jsonify(retJson)

class Transfer(Resource):
    def post(self):
        namepasstoamt = request.get_json()
        username = namepasstoamt["username"]
        password = namepasstoamt["password"]
        amount = namepasstoamt["amount"]
        to = namepasstoamt["to"]

        if not userExists(username):
            retJson = makeJson(301, "Invalid username")
            return jsonify(retJson)

        if not userExists(to):
            retJson = makeJson(301, "Invalid receiver username")
            return jsonify(retJson)

        correct_pw = verifypw(username, password)
        if not correct_pw :
            retJson = makeJson(302, "Incorrect password")
            return jsonify(retJson)

        if amount < 0 :
            retJson=makeJson(304, "You have entered a negative amount. Please re-enter a positive amount")
            return jsonify(retJson)

        cash = getcash(username)
        if cash < amount:
            retJson = makeJson(303, "Not enough cash to transfer")
            return jsonify(retJson)

        updatecash(username, -1*amount -1 )
        updatecash(to, amount)
        updatecash("bank" , 1)

        retJson = makeJson(200, "Money successfully transferred")
        return jsonify(retJson)

class TakeLoan(Resource):
    def post(self):
        namepassamt = request.get_json()
        username = namepassamt["username"]
        password = namepassamt["password"]
        amount = namepassamt["amount"]

        if not userExists(username):
            retJson = makeJson(301, "Invalid username")
            return jsonify(retJson)

        correct_pw = verifypw(username, password)
        if not correct_pw :
            retJson = makeJson(302, "Incorrect password")
            return jsonify(retJson)

        if amount < 0 :
            retJson=makeJson(304, "You have entered a negative amount. Please re-enter a positive amount")
            return jsonify(retJson)

        updatecash(username, amount)
        updatedebt(username, amount)
        updatecash("bank", -1*amount)

        retJson = makeJson(200, "Loan passed successfully")
        return jsonify(retJson)

class PayLoan(Resource):
    def post(self):
        namepassamt = request.get_json()
        username = namepassamt["username"]
        password = namepassamt["password"]
        amount = namepassamt["amount"]

        if not userExists(username):
            retJson = makeJson(301, "Invalid username")
            return jsonify(retJson)

        correct_pw = verifypw(username, password)
        if not correct_pw :
            retJson = makeJson(302, "Incorrect password")
            return jsonify(retJson)

        if amount < 0 :
            retJson=makeJson(304, "You have entered a negative amount. Please re-enter a positive amount")
            return jsonify(retJson)

        updatecash(username, -1*amount)
        updatedebt(username, -1*amount)
        updatecash("bank", amount)

        retJson = makeJson(200, "Loan payed successfully")
        return jsonify(retJson)

api.add_resource(Register, "/register")
api.add_resource(Add, "/add")
api.add_resource(Transfer, "/transfer")
api.add_resource(Check, "/check")
api.add_resource(TakeLoan, "/takeloan")
api.add_resource(PayLoan, "/payloan")

if __name__ == "__main__":
    app.run(host="0.0.0.0")
