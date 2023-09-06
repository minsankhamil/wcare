import pymongo
from flask import current_app, g

def get_db():
    mongocon = current_app.config['MONGO_CON']
    dbclient = pymongo.MongoClient(mongocon)
    g.db = dbclient[current_app.config['DATABASE']]
    return g.db

def get_collection(colname):
    if 'db' not in g:
        get_db()
    return g.db[colname]

#semua kajian
def get_kajians(filter={}):
    collection = get_collection("kajian")
    return collection.find(filter)

#get data kajian by nrm pasien
def get_kajian_nrm(data):
    collection = get_collection("kajian")
    return collection.find(data)

#get 1 image
def get_kajian(filter={}):
    collection = get_collection("kajian")
    return collection.find_one(filter)

#tambah kajian baru
def insert_kajian(data):
    collection = get_collection("kajian")
    row = collection.insert_one(data)
    return row


#delete satu data kajian berdasarkan id
def delete_one_kajian(id):
    collection = get_collection("kajian")    
    return collection.delete_one({"_id":id})

def update_kajian(id, filter):
    collection = get_collection('kajian')

    #cursor ke data pasien sesuai dengan id
    x = collection.find_one({ '_id' : id })
    #query ke id pasien + update data
    #a = int(id)
    myquery = { '_id' : id }
    print(filter)
    newvalues = { '$set': filter }
    return collection.update_one(myquery, newvalues, upsert=False)

def update_id_pasien_kajian(old_id, new_id):
    collection = get_collection('kajian')

    return collection.update_many(
    {"id_pasien": old_id },
        {
            "$set": { "id_pasien" : new_id}
        }
    )