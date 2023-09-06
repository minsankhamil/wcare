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

def get_images(filter={}):
    collection = get_collection("image")
    return collection.find(filter)

def get_imagess(data):
    collection = get_collection("image")
    return collection.find(data)


#get 1 image
def get_image(filter={}):
    collection = get_collection("image")
    return collection.find_one(filter)

def insert_image(data):
    collection = get_collection("image")
    row = collection.insert_one(data)
    return row
    
def update_image(id, update):
    collection = get_collection("image")
    myquery = { "id" : id }
    newvalues = { "$set": { "update": update } }
    return collection.update_one(myquery, newvalues, upsert=False)

#nambahin id gambar ke list image
def update_image_user(id_pasien, data):
    collection = get_collection("pasien")

    #cursor ke data pasien sesuai dengan id
    x = collection.find_one({ "_id" : id_pasien })

    #ambil data list yang udah ada dari pasien sesuai dengan id
    List = x["list_image_id"]
    
    #masukin data baru ke List
    List.append(data)

    #query ke id pasien + update data
    myquery = { "_id" : id_pasien }
    newvalues = { "$set": { "list_image_id": List } }
    return collection.update_one(myquery, newvalues, upsert=False)

#dapetin list image yang udah dipunya pasien
def pasien_image_list(id_pasien):
    collection = get_collection("pasien")

    #cursor ke data pasien sesuai dengan id
    x = collection.find_one({ "_id" : id_pasien })

    #ambil data list yang udah ada dari pasien sesuai dengan id
    List = x["list_image_id"]    

    return List

#nyari filename dari id_image
def search_filename_from_id(id):
    collection = get_collection("image")

    #cursor ke data image sesuai dengan id
    x = collection.find_one({"_id" : id})

    #masukin filename ke variabel baru
    filename = x["filename"]

    return filename

#nyari filename dari id_image
def search_filename_from_id(id):
    collection = get_collection("image")

    #cursor ke data image sesuai dengan id
    x = collection.find_one({"_id" : id})

    #masukin filename ke variabel baru
    filename = x["filename"]

    return filename

def delete_one_image(id):
    collection = get_collection("image")    
    return collection.delete_one({"_id":id})

def delete_all_coll():
    collection = get_collection("image")
    collection.delete_many({})

    collection = get_collection("user")
    collection.delete_many({})

    collection = get_collection("pasien")
    collection.delete_many({})  

    collection = get_collection("kajian") 
    x = collection.delete_many({})   

    list = { "jumlah" : x.deleted_count }   

    return list


#cari list images dr id pasien
def image_list_by_id(data):
    collection = get_collection("image")
    return collection.find(data)

def update_id_pasien_image(old_id, new_id):
    collection = get_collection('image')

    return collection.update_many(
    {"id_pasien": old_id },
        {
            "$set": { "id_pasien" : new_id}
        }
    )

def update_id_perawat_image(old_id, new_id):
    collection = get_collection('image')

    return collection.update_many(
    {"id_perawat": old_id },
        {
            "$set": { "id_perawat" : new_id}
        }
    )

def update_filename_byid(id_image, filter):
    collection = get_collection('image')

    #cursor ke data pasien sesuai dengan id
    x = collection.find_one({ '_id' : id_image })
    myquery = { '_id' : id_image }
    print(filter)
    newvalues = { '$set': filter }
    return collection.update_one(myquery, newvalues, upsert=False) 