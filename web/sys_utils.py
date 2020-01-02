from flask import Flask, jsonify, request
from flask_restful import Api, Resource
from pymongo import MongoClient
import bcrypt

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
    