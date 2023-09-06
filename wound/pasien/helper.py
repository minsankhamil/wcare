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

#data pasien query
#fungsi khusus untuk  mencari data yang berhubungan dengan pasien

def get_pasiens(filter={}):
    collection = get_collection("pasien")
    return collection.find({"verif": "1"})

def get_pasien_ns(data):
    collection = get_collection("pasien")
    return collection.find(data)

def get_pasien(filter={}):
    collection = get_collection("pasien")
    return collection.find_one(filter)

def insert_pasien(data):
    collection = get_collection("pasien")
    row = collection.insert_one(data)
    return row

def update_pasien(filter, update):
    collection = get_collection("pasien")    
    return collection.update_one(filter, update, upsert=False)

def delete_pasien(data):
    collection = get_collection("pasien")
    collection.delete_one(data)

def delete_one_pasien(id):
    collection = get_collection("kajian")  
    collection.delete_many({"id_pasien":id})
    

    collection = get_collection("image")  
    collection.delete_many({"id_pasien":id})

    collection = get_collection("pasien")    
    return collection.delete_one({"_id":id})

def update_pasien_new(id, filter):
    collection = get_collection('pasien')

    #cursor ke data pasien sesuai dengan id
    x = collection.find_one({ '_id' : id })
    #query ke id pasien + update data
    #a = int(id)
    myquery = { '_id' : id }
    print(filter)
    newvalues = { '$set': filter }
    return collection.update_one(myquery, newvalues, upsert=False)

def update_id(old_id, new_id):
    collection = get_collection('pasien')
    old_doc_id = old_id
    new_doc_id = new_id

    doc = collection.find_one({'_id': old_doc_id})

    if doc is not None:
        #  set a new _id on the document
        doc['_id'] = new_doc_id

        # insert the document, using the new _id
        collection.insert_one(doc)

    
        # remove the document with the old _id
        return collection.delete_one({'_id':old_doc_id})
