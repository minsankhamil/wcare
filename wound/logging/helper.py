from typing import Collection
import click
import pymongo
from flask import current_app, g
from flask.cli import with_appcontext
import gridfs

def get_db():
    mongocon = current_app.config['MONGO_CON']
    dbclient = pymongo.MongoClient(mongocon)
    g.db = dbclient[current_app.config['DATABASE']]
    return g.db

def get_collection(colname):
    if 'db' not in g:
        get_db()
    return g.db[colname]


#data pasien query
#fungsi khusus untuk  mencari data yang berhubungan dengan pasien

def get_logs(filter={}):
    collection = get_collection("logging")
    return collection.find(filter)

#get 1 image
def get_log(filter={}):
    collection = get_collection("logging")
    return collection.find_one(filter)

def insert_log(data):
    collection = get_collection("logging")
    row = collection.insert_one(data)
    return row
    

#delete log
def delete_one_log(id):
    collection = get_collection("logging")    
    return collection.delete_one({"_id":id})


#cari list images dr id pasien
def log_list_by_user(data):
    collection = get_collection("logging")
    return collection.find(data)