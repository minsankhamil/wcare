import os
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
from wound import utils
from wound import db
from flask import Flask, jsonify
from bson.objectid import ObjectId
from typing import List
import time

bp = Blueprint('inventarisasi', __name__, url_prefix='/')

#akses list inventaris terdaftar
#@bp.route('/list_inventory', methods =['GET'])
def get_inventariss():
     a = db.get_semua_inventaris()
     print(a)
     print("pass")
     a_serializable = [{'_id': str(inventory['_id']), 'nama_inventaris':inventory['nama_inventaris'], 'tipe_inventaris':inventory['tipe_inventaris'], 'harga':inventory['harga']} for inventory in a]
     return Response(response = json.dumps(list(a_serializable)), mimetype="application/json", status=200)

#@bp.route('/details_inventaris/<_id>', methods =['GET'])
def get_details_inventaris(_id):
    a = db.get_details_inventaris(_id)
    print("pass")
    print(a)
    a_serializable = [{'_id': str(inventory['_id']), 'nama_inventaris':inventory['nama_inventaris'], 'tipe_inventaris':inventory['tipe_inventaris'], 'harga':inventory['harga'], 'keterangan':inventory['keterangan'], 'jumlah':inventory['jumlah']} for inventory in a]
    return Response(response = json.dumps(list(a_serializable)), mimetype="application/json", status=200)

@bp.route('/update_inventaris/<_id>', methods =['POST'])
def update_details_inventaris(_id):
    try:
        data = {
            "nama_inventaris": request.form['nama_inventaris'],
            "tipe_inventaris": request.form['tipe_inventaris'],
            "harga": request.form['harga'],
            "keterangan": request.form['keterangan'],
            "jumlah" : request.form['jumlah']     
        }

        db.update_details_inventaris(data, _id)
        flash("berhasil edit inventaris")
        return redirect(url_for('list_inventaris'))
    
    except Exception as ex:
        print(ex)
        flash("gagal edit inventaris")
        return redirect(url_for('list_inventaris'))


#akses menambah inventaris baru
@bp.route('/inventaris', methods =['POST'])
def addinventory():
    try:       
            data = {
                    "nama_inventaris": request.form['nama_inventaris'],
                    "tipe_inventaris": request.form['tipe_inventaris'],
                    "harga": request.form['harga'],
                    "keterangan":request.form['keterangan'],
                    "jumlah" : request.form['jumlah']
                    }
            
            cek = get_inventaris(data)
       
            if cek == None:
                row = insert_inventaris(data)
                print("berhasil input inventaris")
                flash("berhasil input inventaris")
                return redirect(url_for('inventaris'))
                
            else:
                #jika sudah ada data yang sama maka tidak bisa daftar lagi
                print("gagal input inventaris")
                flash("gagal input inventaris")
                return redirect(url_for('inventaris'))
                            
    except Exception as ex:
        print(ex)
        flash("gagal input inventaris")
        return redirect(url_for('inventaris'))

@bp.route('/delete_inventaris/<_id>')
def delete_inventaris(_id):
    a = db.delete_inventaris(_id)
    print("pass")
    flash("berhasil menghapus inventaris")
    return redirect(url_for('list_inventaris'))
