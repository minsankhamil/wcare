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

#tambah data pemeriksaan kesehatan
def insert_data_pemeriksaan_kesehatan(data):
    collection = get_collection("data_pemeriksaan_kesehatan")
    row = collection.insert_one(data)
    return row

def get_data_pemeriksaan_kesehatan(filter={}):
    collection = get_collection("data_pemeriksaan_kesehatan")
    return collection.find(filter)

def get_all_data_pemeriksaan_kesehatan_one_patient(nik):
    collection = get_collection("data_pemeriksaan_kesehatan")
    return collection.find({"nik": nik})

def get_detail_data_pemeriksaan_kesehatan_one_patient(_id):
    collection = get_collection("data_pemeriksaan_kesehatan")
    return collection.find_one({"_id": int(_id)})