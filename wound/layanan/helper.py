import click
import pymongo
from flask import current_app, g
from flask.cli import with_appcontext

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

def get_layanan(filter={}):
    collection = get_collection("layanan")
    return collection.find_one(filter)

def insert_layanan(data):
    collection = get_collection("layanan")
    row = collection.insert_one(data)
    return row