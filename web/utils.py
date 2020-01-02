# importing helper functions and other imports
from sys_utils import *

# resources

"""
    Resource Register takes input on a POST protocol and creates new accounts 
    Parameters:
        namepass: contains username and password of the user <JSON>
    Returns:
        retJson: contains status code and message <JSON>
"""
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

"""
    Resource Add takes input on a POST protocol and credits user account
    Parameters:
        namepass: contains username, password and amount <JSON>
    Returns:
        retJson: contains status code and message <JSON>
"""
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

"""
    Resource Check takes inputs on POST protocol and returns current balance for the user
    Parameters:
        namepass: contains username and password of the user <JSON>
    Returns:
        retJson: contains status code and message <JSON>
"""
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

"""
    Resource Transfer takes inputs on a POST protocol and transfers money from sender to receiver's account
    Parameters:
        namepass: contains username, password of the user and receiver's username <JSON>
    Returns:
        retJson: contains status code and message <JSON>
"""
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

"""
    Resource Takeloan takes inputs on a POST protocol and grants user a loan
    Parameters:
        namepass: contains username, password of the user and loan amount <JSON>
    Returns:
        retJson: contains status code and message <JSON>
"""
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

"""
    Resource Payloan takes inputs on a POST protocol and pays back a part of the loan
    Parameters:
        namepass: contains username, password of the user and loan amount <JSON>
    Returns:
        retJson: contains status code and message <JSON>
"""
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