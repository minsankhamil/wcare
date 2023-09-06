import click
import pymongo
from flask import current_app, g
from flask.cli import with_appcontext
from bson import ObjectId

def get_db():
    mongocon = current_app.config['MONGO_CON']
    dbclient = pymongo.MongoClient(mongocon)
    g.db = dbclient[current_app.config['DATABASE']]
    return g.db

def get_collection(colname):
    if 'db' not in g:
        get_db()
    return g.db[colname]

#fungsi khusus untuk  mencari data yang berhubungan dengan inventaris

def get_inventaris(filter={}):
    collection = get_collection("inventaris")
    return collection.find_one(filter)

def insert_inventaris(data):
    collection = get_collection("inventaris")
    row = collection.insert_one(data)
    return row
    