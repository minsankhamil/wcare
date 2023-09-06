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

"""
Helper function to query all user on system 
"""
def get_users(filter={}):
    collection = get_collection("user")
    return collection.find(filter)

def get_user(data):
    collection = get_collection("user")
    return collection.find_one(data)

def get_nama_user(filter={}, filter2={}):
    collection = get_collection("user")
    return collection.find({"$or":[ filter, filter2]})
    
def insert_user(data):
    collection = get_collection("user")
    row = collection.insert_one(data)
    return row

def get_profile_user(_id):
    collection = get_collection("user")
    return collection.find({ "_id" : int(_id) })


def update_user(id_perawat, filter):
    collection = get_collection('user')

    #cursor ke data pasien sesuai dengan id
    x = collection.find_one({ '_id' : id_perawat })
    #query ke id pasien + update data
    a = int(id_perawat)
    myquery = { '_id' : a }
    print(filter)
    newvalues = { '$set': filter }
    return collection.update_one(myquery, newvalues, upsert=False)   

def delete_user(data):
    collection = get_collection("user")
    collection.delete_one(data)

#data pasien query
#fungsi khusus untuk  mencari data yang berhubungan dengan pasien

def get_pasiens(filter={}):
    collection = get_collection("pasien")
    return collection.find({"verif": "1"})

def get_pasiens_unverify(filter={}):
    collection = get_collection("pasien")
    return collection.find({"verif": "0"})

def get_profile_pasien(_id):
    collection = get_collection("pasien")
    return collection.find({ "_id" : ObjectId(_id) })

def search_pasien(data):
    collection = get_collection("pasien")
    return collection.find_one(data)

def verify_pasien(_id):
    collection = get_collection("pasien")
    return collection.update_one({ "_id" : ObjectId(_id) }, { "$set": { "verif": "1" }})

def block_pasien(_id):
    collection = get_collection("pasien")
    return collection.update_one({ "_id" : ObjectId(_id) }, { "$set": { "verif": "-1" }})

def get_pasien_ns(data):
    collection = get_collection("pasien")
    return collection.find(data)

def get_pasien_login(data):
    collection = get_collection("pasien")
    return collection.find_one(data, { "verif" : "0" })

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



#fungsi khusus untuk  mencari data yang berhubungan dengan inventaris
def get_semua_inventaris(filter={}):
    collection = get_collection("inventaris")
    return collection.find(filter)

def get_details_inventaris(_id):
    collection = get_collection("inventaris")
    return collection.find({ "_id" : ObjectId(_id) })

def delete_inventaris(_id):
    collection = get_collection("inventaris")
    return collection.delete_one({ "_id" : ObjectId(_id) })

def update_details_inventaris(data, _id):
    collection = get_collection("inventaris")
    return collection.update_one({"_id": ObjectId(_id)}, {"$set": data})

#fungsi khusus untuk  mencari data yang berhubungan dengan layanan
def get_semua_layanan(filter={}):
    collection = get_collection("layanan")
    return collection.find(filter)

def get_details_layanan(_id):
    collection = get_collection("layanan")
    return collection.find({ "_id" : ObjectId(_id) })

def delete_layanan(_id):
    collection = get_collection("layanan")
    return collection.delete_one({ "_id" : ObjectId(_id) })

def update_details_layanan(data, _id):
    collection = get_collection("layanan")
    return collection.update_one({"_id": ObjectId(_id)}, {"$set": data})




"""get bill category"""

def get_bill_category(cat):
    collection = get_collection("bill")
    row = collection.find_one(cat)
    return row

def close_db(e=None):
    db = g.pop(current_app.config['DATABASE'], None)
    
    if db is not None:
        db.close() 

def init_db():
    """clear the existing data and create new tables."""    
    db = get_db()    
    db.client.drop_database(current_app.config['DATABASE'])
    
@click.command('init-db')
@with_appcontext
def init_db_command():    
    init_db()
    click.echo('Initialized the database.')

def init_app(app):
    "app.teardown_appcontext(close_db)"
    app.cli.add_command(init_db_command)

