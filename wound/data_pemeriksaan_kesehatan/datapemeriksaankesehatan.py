import os
from flask import(
    Blueprint, flash, redirect, Response, current_app, request, url_for)
import json

from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename
from wound.data_kajian.helper import update_id_pasien_kajian
from wound.image.helper import update_id_pasien_image
from wound.pasien.helper import  delete_one_pasien, get_pasien, insert_pasien, get_pasien_ns, update_id, update_pasien_new
from wound.inventaris.helper import get_inventaris, insert_inventaris
from wound.data_pemeriksaan_kesehatan.helper import insert_data_pemeriksaan_kesehatan, get_data_pemeriksaan_kesehatan, get_all_data_pemeriksaan_kesehatan_one_patient, get_detail_data_pemeriksaan_kesehatan_one_patient
from wound import utils
from wound import db
from flask import Flask, jsonify
from bson.objectid import ObjectId
from typing import List
import time

bp = Blueprint('datapemeriksaankesehatan', __name__, url_prefix='/')

#akses menambah inventaris baru
@bp.route('/add_data_pemeriksaan_kesehatan', methods =['POST'])
def post_data_pk():
    try:       
            a = list(get_data_pemeriksaan_kesehatan())
            data = {
                    "_id": 100000000 + len(a) + 1,
                    "tanggal": request.form['tanggal'],
                    "username": request.form['username'],
                    "nik": request.form['nik'],
                    "tekanan_darah": request.form['tekanan_darah'],
                    "nadi": request.form['nadi'],
                    "suhu": request.form['suhu'],
                    "gula_darah_sewaktu":request.form['gula_darah_sewaktu'],
                    "ABPI" : request.form['ABPI']
                    }
            
            insert_data_pemeriksaan_kesehatan(data) 
            print("Berhasil input data pemeriksaan kesehatan")       
            return Response(response = json.dumps(data), mimetype="application/json", status=200)
        
    except Exception as ex:
        print (ex)
        print("Gagal input data pemeriksaan kesehatan")  
        return Response(response = json.dumps({"message" : "error encountered"}), mimetype="application/json", status=500)
    

#akses semua data pemeriksaan kesehatan dari nik pasien
@bp.route('/all_data_pk_pasien/<nik>', methods =['GET'])
def all_data_pk(nik):
    a = get_all_data_pemeriksaan_kesehatan_one_patient(nik)
    a_serializable = [{'_id': str(data_pk['_id']), 'tanggal':data_pk['tanggal'], 'username':data_pk['username'], 'nik':data_pk['nik'], 'tekanan_darah':data_pk['tekanan_darah'], 'nadi':data_pk['nadi'], 'suhu':data_pk['suhu'], 'gula_darah_sewaktu':data_pk['gula_darah_sewaktu'], 'ABPI':data_pk['ABPI']} for data_pk in a]
    return Response(response = json.dumps(list(a_serializable)), mimetype="application/json", status=200)

#akses semua data pemeriksaan kesehatan dari nik pasien
@bp.route('/detail_data_pk_pasien/<_id>', methods =['GET'])
def detail_data_pk(_id):
    a = get_detail_data_pemeriksaan_kesehatan_one_patient(_id)
    print(a)
    a_serializable = [a]
    return Response(response = json.dumps(list(a_serializable)), mimetype="application/json", status=200)



