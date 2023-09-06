from uuid import uuid1
import numpy as np
import uuid
from flask import(
    Blueprint, Response, request)
import json

from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename
from wound.data_kajian.helper import  delete_one_kajian, get_kajian, get_kajian_nrm, get_kajians, insert_kajian, update_id_pasien_kajian, update_kajian
from wound import utils
from flask import Flask, jsonify
from bson.objectid import ObjectId
from typing import List
import time
import functools, logging, os, json
from flask import(
    Blueprint, flash, g, redirect, render_template, request, session, url_for, current_app, Markup, send_from_directory
)

from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename
from bson.objectid import ObjectId


bp = Blueprint('datakajian', __name__, url_prefix='/')

#insert data kajian
@bp.route('/insert_kajian', methods =['POST'])
def post_kajian():
                 
    #next save the file
    id = uuid.uuid4().hex
    id_pasien = request.form['id_pasien']   

    try:
                              
        data = {    "_id" : id,
                    "id_pasien": id_pasien,
                    "id_perawat": request.form['id_perawat'],
                    "size":request.form['size'],
                    "edges":request.form['edges'],
                    "necrotic_type":request.form['necrotic_type'],
                    "necrotic_amount":request.form['necrotic_amount'],
                    "skincolor_surround":request.form['skincolor_surround'],
                    "granulation":request.form['granulation'],
                    "epithelization":request.form['epithelization'],
                    "raw_photo_id": request.form['raw_photo_id'],
                    "tepi_image_id": request.form['tepi_image_id'],
                    "diameter_image_id": request.form['diameter_image_id'],
                    "created_at" : time.strftime("%d/%m/%Y %H:%M:%S")
                    }
        insert_kajian(data)        
        return Response(response = json.dumps(data), mimetype="application/json", status=200)
        
    except Exception as ex:
        print (ex)
        return Response(response = json.dumps({"message" : "error encountered"}), mimetype="application/json", status=500)


#get all kajian data
@bp.route('/get_kajians', methods =['GET'])
def get_all_kajian():
    a = get_kajians()
    print(a)
    return Response(response = json.dumps(list(a)), mimetype="application/json", status=200)

#get 1 kajian berdasarkan id kajian
@bp.route('/get_kajian/<id>', methods =['GET'])
def get_one_kajian(id):
    try:
        filter = {}
        filter["_id"] = id
        cek = get_kajian(filter)

       
        if cek == None: 
            return Response(response = json.dumps({"message" : "not found"}), mimetype="application/json", status=404)
        else:
            print(cek)
            return Response(response = json.dumps(dict(cek)), mimetype="application/json", status=200)

    except Exception as ex:
        print("internal server error")
        return Response(response = json.dumps({"message" : "false"}), mimetype="application/json", status=500)


#delete 1 kajian berdasarkan id kajian
@bp.route('/delete_kajian/<id>', methods= ['DELETE'])
def delete_kajian(id):
    ide = id
    delete_one_kajian(ide)
    return Response(response = json.dumps({"message" : "1 kajian deleted"}), mimetype="application/json", status=200)


#get all kajian data berdasarkan nrm
@bp.route('/get_kajian/pasien/<nrm>', methods =['GET'])
def get_pasien_kajian(nrm):
    data = {"id_pasien" : nrm}
    cek = get_kajian_nrm(data)

    a = []
    for doc in cek:
        a.append(doc)
    return Response(response = json.dumps(a), mimetype="application/json", status=200)


#update data kajian
@bp.route('/kajian/update', methods =['POST'])
def update_data_kajian():

    id_perawat = request.form['id_kajian']
    jenis = request.form['jenis']
    isian = request.form['isian']

    filter = {}
    filter[jenis] = isian

    try:        
        update_kajian(id_perawat, filter)
        return Response(response = json.dumps({"message" : "berhasil"}), mimetype="application/json", status=200)
    
            
    except Exception as ex:
        print (ex)
        return Response(response = json.dumps({"message" : "false"}), mimetype="application/json", status=500)

@bp.route('kajian/pasien/new', methods=['POST'])
def coba_kajian_pasien():
    old_id = request.form['id_pasien']
    jenis = request.form['jenis']
    new_id = request.form['isian']

    try:
        update_id_pasien_kajian(old_id, new_id)
        return Response(response = json.dumps({"message" : "berhasil"}), mimetype="application/json", status=200)
    
            
    except Exception as ex:
        print (ex)
        return Response(response = json.dumps({"message" : "false"}), mimetype="application/json", status=500)

