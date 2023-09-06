import os
from flask import(
    Blueprint, Response, current_app, request, flash, url_for, redirect, session)
import json

from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename
from wound.data_kajian.helper import update_id_pasien_kajian
from wound.image.helper import update_id_pasien_image
from wound.pasien.helper import  delete_one_pasien, get_pasien, insert_pasien, get_pasien_ns, update_id, update_pasien_new
from wound import utils
from wound import db
from flask import Flask, jsonify
from bson.objectid import ObjectId
from typing import List
import time

bp = Blueprint('pasien', __name__, url_prefix='/')

#akses semua pasien yang telah terverifikasi klinik
@bp.route('/pasien', methods =['GET'])
def get_pasiens():
    a = db.get_pasiens()
    a_serializable = [{'_id': str(patient['_id']), 'email':patient['email'], 'nama':patient['nama'], 'born_date':patient['born_date'], 'usia':patient['usia'], 'kelamin':patient['kelamin'], 'agama':patient['agama'], 'alamat':patient['alamat'], 'no_hp':patient['no_hp'], 'nik':patient['nik']} for patient in a]
    return Response(response = json.dumps(list(a_serializable)), mimetype="application/json", status=200)

#akses semua pasien yang belum terverifikasi klinik
@bp.route('/pasien_unverify', methods =['GET'])
def get_pasiens_unverify():
    a = db.get_pasiens_unverify()
    a_serializable = [{'_id': str(patient['_id']), 'email':patient['email'], 'nama':patient['nama'], 'born_date':patient['born_date'], 'usia':patient['usia'], 'kelamin':patient['kelamin'], 'agama':patient['agama'], 'alamat':patient['alamat'], 'no_hp':patient['no_hp'], 'nik':patient['nik']} for patient in a]
    print("pass")
    return Response(response = json.dumps(list(a_serializable)), mimetype="application/json", status=200)

#akses profil pasien yang terverifikasi/tidak tersertifikasi klinik berdasarkan id
@bp.route('/profile_pasien/<_id>', methods =['GET'])
def get_profile_patient(_id):
    a = db.get_profile_pasien(_id)
    a_serializable = [{'_id': str(patient['_id']), 'email':patient['email'], 'nama':patient['nama'], 'born_date':patient['born_date'], 'usia':patient['usia'], 'kelamin':patient['kelamin'], 'agama':patient['agama'], 'alamat':patient['alamat'], 'no_hp':patient['no_hp'], 'nik':patient['nik']} for patient in a]
    print("pass")
    return Response(response = json.dumps(list(a_serializable)), mimetype="application/json", status=200)

#search profil pasien yang terverifikasi/tidak tersertifikasi klinik berdasarkan nik
@bp.route('/search_pasien', methods =['GET'])
def search_pasien():
                
    nik : request.form['nik']
            
    print(nik)
    
    a = db.search_pasien(nik)

    if a == None:
        print("Pasien tidak ditemukan")
        flash("Pasien tidak ditemukan")
        return redirect(url_for('pendaftaran_pasien_berobat'))
    else:
        a_serializable = [{'_id': str(patient['_id']), 'email':patient['email'], 'nama':patient['nama'], 'born_date':patient['born_date'], 'usia':patient['usia'], 'kelamin':patient['kelamin'], 'agama':patient['agama'], 'alamat':patient['alamat'], 'no_hp':patient['no_hp'], 'nik':patient['nik']} for patient in a]
        print("Data pasien ditemukan")
        flash("Data pasien ditemukan")
        return Response(response = json.dumps(list(a_serializable)), mimetype="application/json", status=200)

#akses merubah pasien belum terverifikasi menjadi pasien terverifikasi
@bp.route('/accept_verif_pasien/<_id>', methods =['GET'])
def accept_unverify_patient(_id):
    a = db.verify_pasien(_id)
    print("pass")
    flash("Berhasil verifikasi pasien")
    return redirect(url_for('list_request_new_patient'))

#akses merubah pasien belum terverifikasi menjadi pasien terblokir
@bp.route('/block_verif_pasien/<_id>', methods =['GET'])
def block_unverify_patient(_id):
    a = db.block_pasien(_id)
    print("pass")
    flash("Berhasil blokir pasien")
    return redirect(url_for('list_request_new_patient'))


#add pasien baru lewat apps klinik
@bp.route('/pasien', methods =['POST'])
def addpasien():
    try:       
            data = {
                    "email": request.form['email'],
                    "password": request.form['passw'],
                    "nik": request.form['nik'],
                    "nama":request.form['nama'],
                    "kelamin": request.form['kelamin'],
                    "agama":request.form['agama'],
                    "born_date":request.form['born_date'],
                    "usia":request.form['usia'],
                    "alamat": request.form['alamat'],
                    "no_hp": request.form['no_hp'],
                    "created_at" : time.strftime("%d/%m/%Y %H:%M:%S"),
                    "updated_at" : time.strftime("%d/%m/%Y %H:%M:%S"),
                    "list_image_id": [],
                    "verif": '1'
                    }
            
            cek = get_pasien(data)
       
            if cek == None:
                row = insert_pasien(data)
                print("Berhasil input pasien baru")
                flash("Berhasil input pasien baru")
                return redirect(url_for('add_new_patient'))
            
            else:
                #jika sudah ada data yang sama maka tidak bisa daftar lagi
                print("Gagal input pasien baru")
                flash("Gagal input pasien baru")
                return redirect(url_for('add_new_patient'))
                           
    except Exception as ex:
        print(ex)
        return Response(response = json.dumps({"message" : "exe"}), mimetype="application/json", status=500)


#add pasien baru lewat apps pasien
@bp.route('/pasien_app', methods =['POST'])
def addpasien_app():
    try:      
            data = {
                    "email": request.form['email'],
                    "password": request.form['passw'],
                    "nik": request.form['nik'],
                    "nama":request.form['nama'],
                    "kelamin": request.form['kelamin'],
                    "agama":request.form['agama'],
                    "born_date":request.form['born_date'],
                    "usia":request.form['usia'],
                    "alamat": request.form['alamat'],
                    "no_hp": request.form['no_hp'],
                    "created_at" : time.strftime("%d/%m/%Y %H:%M:%S"),
                    "updated_at" : time.strftime("%d/%m/%Y %H:%M:%S"),
                    "list_image_id": [],
                    "verif": '0'
                    }
            
            cek = get_pasien(data)
       
            if cek == None:
                row = insert_pasien(data)
                print("pendaftaran berhasil. menunggu untuk dikonfirmasi klinik")
                return Response(response = json.dumps({"message" : "true"}), mimetype="application/json", status=200)
                
            else:
                #jika sudah ada data yang sama maka tidak bisa daftar lagi
                return Response(response = json.dumps({"message" : "false"}), mimetype="application/json", status=404)                    
                            
    except Exception as ex:
        print(ex)
        return Response(response = json.dumps({"message" : "exe"}), mimetype="application/json", status=500)


#mendapatkan data pasien berdasarkan id/nrm
@bp.route('/pasien/<nrm>', methods =['GET'])
def cek_data_pasien(nrm):
    try:
        filter = {}
        filter["_id"] = nrm
        cek = get_pasien(filter)

       
        if cek == None: 
            return Response(response = json.dumps({"message" : "not found"}), mimetype="application/json", status=404)
        else:
            print(cek)
            return Response(response = json.dumps(dict(cek)), mimetype="application/json", status=200)

    except Exception as ex:
        print("internal server error")
        return Response(response = json.dumps({"message" : "false"}), mimetype="application/json", status=500)

#delete 1 pasien berdasarkan id
@bp.route('/pasien/<id>', methods= ['DELETE'])
def delete_pasien(id):
    ide = id
    filter = {}
    filter["_id"] = ide
    cek = get_pasien(filter)
    delete_one_pasien(ide)
    return Response(response = json.dumps(dict(cek)), mimetype="application/json", status=200)

#mendapatkan data pasien berdasarkan perawat yang mengurus
@bp.route('pasien/find/perawat/<id_perawat>')
def cek_data_perawat_pasien(id_perawat):
    try:
        filter = {}
        filter["id_perawat"] = int(id_perawat)
        data = {"id_perawat" : int(id_perawat)}
        cek = get_pasien_ns(data)

       
        if cek == None: 
            return Response(response = json.dumps({"message" : "not found"}), mimetype="application/json", status=404)
        else:
            a = []
            for doc in cek:
                a.append(doc)

            print(a)
            return Response(response = json.dumps(a), mimetype="application/json", status=200)

    except Exception as ex:
        print(ex)
        print("internal server error")
        return Response(response = json.dumps({"message" : "false"}), mimetype="application/json", status=500)

#update data user
@bp.route('/pasien/update', methods =['POST'])
def update_data_pasien():

    id_perawat = request.form['id_pasien']
    jenis = request.form['jenis']
    isian = request.form['isian']

    if jenis == "_id":
        try:
            update_id(id_perawat,isian)
            update_id_pasien_kajian(id_perawat,isian)
            update_id_pasien_image(id_perawat,isian)
            return Response(response = json.dumps({"message" : "berhasil"}), mimetype="application/json", status=200)
        except Exception as ex:
            print(ex)
            return Response(response = json.dumps({"message" : "false"}), mimetype="application/json", status=500)
    else:
        filter = {}
        filter[jenis] = isian

        try:        
            update_pasien_new(id_perawat, filter)
            return Response(response = json.dumps({"message" : "berhasil"}), mimetype="application/json", status=200)
        
                
        except Exception as ex:
            print (ex)
            return Response(response = json.dumps({"message" : "false"}), mimetype="application/json", status=500)


#upload gambar
@bp.route('/pasien/profile_img', methods =['POST'])
def post_pasien_image():
                 
    #next save the file
    
    file = request.files['image']
    id_perawat = request.form['id_pasien']

    filter = {}
    filter["_id"] = id_perawat
    cek = get_pasien(filter)

    

    try:
        if file and utils.allowed_file(file.filename):

            
            filename = secure_filename(file.filename)
            filename = utils.pad_timestamp(filename)
            path = os.path.join(current_app.instance_path, current_app.config['UPLOAD_DIR']).replace("uploads","")
            fixed_path = os.path.join(path, "userImage")

            try:
                if cek["profile_image_url"] != None:
                    old_filename = cek["profile_image_url"].replace("https://jft.web.id/woundapi/instance/userImage/", "")
                    old_filepath = os.path.join(fixed_path, old_filename)
                    os.remove(old_filepath)
                else :
                    pass
            except Exception as ex:
                print (ex)

            filter = {}
            filter["profile_image_url"] = "https://jft.web.id/woundapi/instance/userImage/" + filename

            try:
                os.makedirs(fixed_path)
            except OSError:
                pass
            filepath = os.path.join(fixed_path, filename)
            file.save(filepath)
                       
            filter = {}
            filter["profile_image_url"] = "https://jft.web.id/woundapi/instance/userImage/" + filename

            update_pasien_new(id_perawat, filter)           
              

            print(filepath)
            current_app.logger.debug(filepath);         
        return Response(response = json.dumps({"message" : "true"}), mimetype="application/json", status=200)
        
    except Exception as ex:
        print (ex)
        return Response(response = json.dumps({"message" : "error encountered"}), mimetype="application/json", status=500)
    
#login pasien
@bp.route('/login_pasien', methods=['POST'])
def login_pasien():
    try:
        data = { 
                "email" : request.form['email'], 
                "password" : request.form['passw'],
                "verif" : '1'
                }
        
        a = db.get_pasien_login(data)
        
        if a == None:
             print("Pasien tidak ditemukan")
             return Response(response = json.dumps({"message" : "failed"}), mimetype="application/json", status=400)
        else:
             print("Berhasil login")
             return Response(response = json.dumps({"message" : "success"}), mimetype="application/json", status=200)
        
    except Exception as ex:
        print (ex)
        return Response(response = json.dumps({"message" : "exe"}), mimetype="application/json", status=500)

