# importing the libraries

from flask import Flask, jsonify, request
from flask_restful import Api, Resource
from pymongo import MongoClient
import bcrypt

# setting up the database
client = MongoClient("mongodb://db:27017")
db = client.BankApi # database

users = db["users"] # collection

# helper functions

"""
    Checks whether a user already exists in the database 
       
    Parameters:
        username: the unique identification name for the user <str>
    Returns:
        True/False <boolean>
"""
def userExists(username):
    if users.find({"username": username}).count() == 0:
        return False
    else:
        return True

"""
    Verifies password provided by the user against the one already present in the database
       
    Parameters:
        username: the unique identification name for the user <str>
        password : password given at the time of calling the API <str>
    Returns:
        True/False <boolean>
"""
def verifypw(username, password):
    hashed_pw = users.find({
        "username" : username
    })[0]["password"]

    if bcrypt.hashpw(password.encode('utf8'), hashed_pw) == hashed_pw:
        return True
    else:
        return False

"""
    Returns the number of tookens available to the user at the time for API call
       
    Parameters:
        username: the unique identification name for the user <str>
        password : password given at the time of calling the API <str>
    Returns:
        num_tokens: the number of tokens currently available <int>
"""
def countTokens(username):
    num_tokens = users.find({
        "username" : username
    })[0]["tokens"]
    return num_tokens

"""
    Return the current balance in user's account
    Parameters:
        username: the unique identification name for the user <str>
    Returns:
        cash: balance  of the user <int>
"""
def getcash(username):
    cash = users.find({
            "username" : username
        })[0]["cash"]
    return cash

"""
    Return the current debt the user owns to the bank
    Parameters:
        username: the unique identification name for the user <str>
    Returns:
        debt: debt owned <int>
"""
def getdebt(username):
    debt = users.find({
            "username" : username
        })[0]["debt"]
    return debt

"""
    Creates a JSON for consisting of message and the statuscode
    Parameters:
        statuscode: status code to include in the JSON <int>
        message: message to be included in the JSON <str>
    Returns:
        none
"""
def makeJson(statuscode, message):
    retJson = {
        "statuscode" : statuscode,
        "message" : message
    }
    return retJson

"""
    Updates the account balance for the user based on the trasaction
    Parameters:
        username: the unique identification name for the user <str>
        amount : the amount of money to add or subtravt to the existing balance <int>
    Returns:
        none
"""
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

"""
    Updates the account debt for the user based on the trasaction
    Parameters:
        username: the unique identification name for the user <str>
        amount : the amount of money to add or subtravt to the existing debt <int>
    Returns:
        none
"""
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
    