import os
import os
from flask import(
    Blueprint, flash, Response, current_app, request, redirect, url_for)
import json

from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename
from wound.data_kajian.helper import update_id_pasien_kajian
from wound.image.helper import update_id_pasien_image
from wound.pasien.helper import  delete_one_pasien, get_pasien, insert_pasien, get_pasien_ns, update_id, update_pasien_new
from wound.inventaris.helper import get_inventaris, insert_inventaris
from wound.layanan.helper import get_layanan, insert_layanan
from wound import utils
from wound import db
from flask import Flask, jsonify
from bson.objectid import ObjectId
from typing import List
import time

bp = Blueprint('layanans', __name__, url_prefix='/')

#akses list layanan terdaftar
#@bp.route('/list_services', methods =['GET'])
def get_layanans():
    
     a = db.get_semua_layanan()
     print(a)
     print("pass")
     a_serializable = [{'_id': str(service['_id']), 'nama_layanan':service['nama_layanan'], 'harga':service['harga'], 'harga':service['harga']} for service in a]
     return Response(response = json.dumps(list(a_serializable)), mimetype="application/json", status=200)

#akses detail layanan
#@bp.route('/details_layanan/<_id>', methods =['GET'])
def get_details_layanan(_id):
    a = db.get_details_layanan(_id)
    print("pass")
    print(a)
    a_serializable = [{'_id': str(service['_id']), 'nama_layanan':service['nama_layanan'], 'harga':service['harga'], 'keterangan':service['keterangan']} for service in a]
    return Response(response = json.dumps(list(a_serializable)), mimetype="application/json", status=200)

@bp.route('/update_layanan/<_id>', methods =['POST'])
def update_details_layanan(_id):
     try:
        data = {
                "nama_layanan": request.form['nama_layanan'],
                "harga": request.form['harga'],
                "keterangan": request.form['keterangan'],    
                }
        
        db.update_details_layanan(data, _id)
        flash("berhasil edit layanan")
        return redirect(url_for('list_layanan'))
     
     except Exception as ex:
        print(ex)
        flash("gagal edit layanan")
        return redirect(url_for('list_inventaris'))


#akses menambah layanan baru
@bp.route('/layanan', methods =['POST'])
def addservice():
    try:       
            data = {
                    "nama_layanan": request.form['nama_layanan'],
                    "keterangan": request.form['keterangan'],
                    "harga":request.form['harga'],
                    }
            
            cek = get_layanan(data)
       
            if cek == None:
                row = insert_layanan(data)
                print("Berhasil input layanan")
                flash("Berhasil input layanan")
                return redirect(url_for('layanan'))
            else:
                print("Gagal input layanan")
                flash("Gagal input layanan")
                return redirect(url_for('layanan'))
                        
    except Exception as ex:
        print("Gagal input layanan")
        flash("Gagal input layanan")
        return redirect(url_for('layanan'))
    
@bp.route('/delete_layanan/<_id>')
def delete_layanan(_id):
    a = db.delete_layanan(_id)
    print("pass")
    flash("berhasil menghapus inventaris")
    return redirect(url_for('list_layanan'))