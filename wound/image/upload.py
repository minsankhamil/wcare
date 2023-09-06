from uuid import uuid1
import numpy as np
import uuid
from flask import(
    Blueprint, Response, request, send_file)
import json
import datetime

from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename
from wound.image import helper
from wound.image.helper import get_images, get_imagess, image_list_by_id, insert_image, search_filename_from_id, update_id_pasien_image, update_id_perawat_image, update_image, get_image
from wound.pasien.helper import  get_pasien, insert_pasien, get_pasien_ns
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


bp = Blueprint('upload', __name__, url_prefix='/')

#upload gambar
@bp.route('/upload', methods =['POST'])
def post_image():
                 
    #next save the file
    
    file = request.files['image']
    id = request.form['id']
    id_pasien = request.form['id_pasien']   

    try:
        if file and utils.allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filename = utils.pad_timestamp(filename)
            path = os.path.join(current_app.instance_path, current_app.config['UPLOAD_DIR'])
            try:
                os.makedirs(path)
            except OSError:
                pass
            filepath = os.path.join(path, filename)
            file.save(filepath)
                       
            data = {"_id": id,
                    "id_pasien": id_pasien,
                    "id_perawat": request.form['id_perawat'],
                    "filename":filename,
                    "filepath":path,
                    "type":request.form['type'],
                    "category":request.form['category'],
                    "created_at" : time.strftime("%d/%m/%Y %H:%M:%S"),
                    "updated_at" : time.strftime("%d/%m/%Y %H:%M:%S"),
                    }
            insert_image(data)

            if id_pasien == "all":
                print("all")
            else:
                helper.update_image_user(id_pasien, id)
            
              

            print(filepath)
            current_app.logger.debug(filepath);         
        return Response(response = json.dumps({"message" : "true"}), mimetype="application/json", status=200)
        
    except Exception as ex:
        print (ex)
        return Response(response = json.dumps({"message" : "error encountered"}), mimetype="application/json", status=500)

#download all in folder
import zipfile
@bp.route('/download_files', methods=["GET"])
def download_all():
    path = os.path.join(current_app.instance_path, current_app.config['UPLOAD_DIR']).replace("uploads","")

    #lokasi folder
    folderLocation = os.path.join(current_app.instance_path, current_app.config['UPLOAD_DIR'])
    dir = os.path.join(path, "zip")
    namafile = "imagefiles.zip"
    fixedfilename = os.path.join(dir, namafile)

    print(fixedfilename)

    # zip all the files which are inside in the folder
    zf = zipfile.ZipFile(fixedfilename, "w")
    for dirname, subdirs, files in os.walk(folderLocation):
        zf.write(dirname)
        for filename in files:
            zf.write(os.path.join(dirname, filename))
    zf.close()

    dir = os.path.join(path, "zip")

    return send_from_directory( dir, "imagefiles.zip", as_attachment=True)


#download all from category
@bp.route('/download_files_category/<category>', methods=["GET"])
def download_category(category):
    filter = {}
    filter["category"] = category
    data = {"category" : category}
    cek = image_list_by_id(data)

       
    if cek == None: 
        return Response(response = json.dumps({"message" : "not found"}), mimetype="application/json", status=404)
    else:
        a = []
        for doc in cek:
            a.append(doc)

    #for i in a:
        #print(i["filename"])


    path = os.path.join(current_app.instance_path, current_app.config['UPLOAD_DIR']).replace("uploads","")

    #lokasi folder
    folderLocation = os.path.join(current_app.instance_path, current_app.config['UPLOAD_DIR'])
    dir = os.path.join(path, "zip")
    namafile = "imagefiles.zip"
    fixedfilename = os.path.join(dir, namafile)

    print(fixedfilename)

    # zip all the files which are inside in the folder
    zf = zipfile.ZipFile(fixedfilename, "w")
    for dirname, subdirs, files in os.walk(folderLocation):
        zf.write(dirname)
        for filename in files:
            for i in a:
                if filename == i["filename"]:
                    print(filename)
                    zf.write(os.path.join(dirname, filename))
    zf.close()

    dir = os.path.join(path, "zip")

    return send_from_directory( dir, "imagefiles.zip", as_attachment=True)


    # Delete the zip file if not needed
    os.remove("imagefiles.zip")

#download all from id pasien
@bp.route('/download_files_pasien/', methods=["GET"])
def download_pasien():
    id_pasien = request.args.get("nrm")
    filter = {}
    filter["id_pasien"] = id_pasien
    data = {"id_pasien" : id_pasien}
    cek = image_list_by_id(data)
    a = []
       
    if cek == None: 
        return Response(response = json.dumps({"message" : "not found"}), mimetype="application/json", status=404)
    else:
        
        for doc in cek:
            a.append(doc)

    #for i in a:
        #print(i["filename"])


    path = os.path.join(current_app.instance_path, current_app.config['UPLOAD_DIR']).replace("uploads","")

    #lokasi folder
    folderLocation = os.path.join(current_app.instance_path, current_app.config['UPLOAD_DIR'])
    dir = os.path.join(path, "zip")
    namafile = "imagefiles.zip"
    fixedfilename = os.path.join(dir, namafile)

    print(fixedfilename)

    # zip all the files which are inside in the folder
    zf = zipfile.ZipFile(fixedfilename, "w")
    for dirname, subdirs, files in os.walk(folderLocation):
        zf.write(dirname)
        for filename in files:
            for i in a:
                if filename == i["filename"]:
                    print(filename)
                    zf.write(os.path.join(dirname, filename))
    zf.close()

    dir = os.path.join(path, "zip")

    return send_from_directory( dir, "imagefiles.zip", as_attachment=True)



    # Delete the zip file if not needed
    os.remove("imagefiles.zip")




#upload gambar svg
@bp.route('/upload_svg', methods =['POST'])
def post_svg():
                 
    #next save the file
    
    paths= request.form['paths']
    print(paths)
    id = str(uuid.uuid4().hex)
    id_pasien = request.form['id_pasien']   

    try:
        output_str = paths.replace(', ', ' ').replace('[', '').replace(']', '').replace(","," ")
        canvas ='<svg width="1080" height="1441" viewBox="0 0 1080 1441" fill="none" xmlns="http://www.w3.org/2000/svg">'
        path ='<path d="' + output_str + '" stroke="black" stroke-width="10"/>'
        close = '</svg>'
        svg = canvas + path + close


        path = os.path.join(current_app.instance_path, current_app.config['UPLOAD_DIR'])
        try:
            os.makedirs(path)
        except OSError:
            pass
        

        date = str(datetime.datetime.now().replace(microsecond=0)).replace("-","").replace(" ","_").replace(':', "")

        filename = id_pasien + "_tepi_" + date + ".svg"
        filepath = os.path.join(path, filename)

        svg_file = open(filepath, "w")
 
        #write string to file
        svg_file.write(svg)
 
        #close file
        svg_file.close()
                       
        data = {"_id": id,
                    "id_pasien": id_pasien,
                    "id_perawat": request.form['id_perawat'],
                    "filename":filename,
                    "filepath":path,
                    "type":"Vector",
                    "category":request.form['category'],
                    "created_at" : time.strftime("%d/%m/%Y %H:%M:%S"),
                    "updated_at" : time.strftime("%d/%m/%Y %H:%M:%S"),
                    }
        insert_image(data)
        helper.update_image_user(id_pasien, id)  
        
        print(filepath)
        current_app.logger.debug(filepath);
      
        return Response(response = json.dumps({"message" : "true"}), mimetype="application/json", status=200)
        
    except Exception as ex:
        print (ex)
        return Response(response = json.dumps({"message" : "error encountered"}), mimetype="application/json", status=500)


#upload gambar svg
@bp.route('/upload_svg_3', methods =['POST'])
def post_svg_3():
                 
    #next save the file
    
    paths= request.form['paths']
    paths2 = request.form ['paths2']
    paths3 = request.form['paths3']
    print(paths)
    id = str(uuid.uuid4().hex)
    id_pasien = request.form['id_pasien']   

    try:
        
        paths = paths.replace(', ', ' ').replace('[', '').replace(']', '').replace(","," ")
        paths2 = paths2.replace(', ', ' ').replace('[', '').replace(']', '').replace(","," ")
        paths3 = paths3.replace(', ', ' ').replace('[', '').replace(']', '').replace(","," ")
        canvas ='<svg width="1080" height="1441" viewBox="0 0 1080 1441" fill="none" xmlns="http://www.w3.org/2000/svg">'
        path1 ='<path d="' + paths + '" stroke="black" stroke-width="10"/>'
        path2 ='<path d="' + paths2 + '" stroke="black" stroke-width="10"/>'
        path3 ='<path d="' + paths3 + '" stroke="black" stroke-width="10"/>'

        close = '</svg>'

        svg = canvas + path1 + path2 + path3 + close


        path = os.path.join(current_app.instance_path, current_app.config['UPLOAD_DIR'])
        try:
            os.makedirs(path)
        except OSError:
            pass
        

        date = str(datetime.datetime.now().replace(microsecond=0)).replace("-","").replace(" ","_").replace(':', "")

        filename = id_pasien + "_diameter_" + date + ".svg"
        filepath = os.path.join(path, filename)

        svg_file = open(filepath, "w")
 
        #write string to file
        svg_file.write(svg)
 
        #close file
        svg_file.close()
                       
        data = {"_id": id,
                    "id_pasien": id_pasien,
                    "id_perawat": request.form['id_perawat'],
                    "filename":filename,
                    "filepath":path,
                    "type":"Vector",
                    "category":request.form['category'],
                    "created_at" : time.strftime("%d/%m/%Y %H:%M:%S"),
                    "updated_at" : time.strftime("%d/%m/%Y %H:%M:%S"),
                    }
        insert_image(data)
        helper.update_image_user(id_pasien, id)  
        
        print(filepath)
        current_app.logger.debug(filepath);
      
        return Response(response = json.dumps({"message" : "true"}), mimetype="application/json", status=200)
        
    except Exception as ex:
        print (ex)
        return Response(response = json.dumps({"message" : "error encountered"}), mimetype="application/json", status=500)


#get all images data
@bp.route('/get_images', methods =['GET'])
def get_all_images():
    a = get_images()
    print(a)
    return Response(response = json.dumps(list(a)), mimetype="application/json", status=200)

#get 1 image berdasarkan id
@bp.route('/get_image/<id>', methods =['GET'])
def get_one_image(id):
    try:
        filter = {}
        filter["_id"] = id
        cek = get_image(filter)

       
        if cek == None: 
            return Response(response = json.dumps({"message" : "not found"}), mimetype="application/json", status=404)
        else:
            print(cek)
            return Response(response = json.dumps(dict(cek)), mimetype="application/json", status=200)

    except Exception as ex:
        print("internal server error")
        return Response(response = json.dumps({"message" : "false"}), mimetype="application/json", status=500)


#delete 1 image berdasarkan id
@bp.route('/delete_image/<id>', methods= ['DELETE'])
def delete_image(id):
    ide = id
    filename = search_filename_from_id(ide)
    filter = {}
    filter["_id"] = ide
    cek = get_image(filter)
    path = os.path.join(current_app.instance_path, current_app.config['UPLOAD_DIR'])
    try:
        os.makedirs(path)
    except OSError:
        pass
    filepath = os.path.join(path, filename)
    os.remove(filepath)
    helper.delete_one_image(ide)
    return Response(response = json.dumps(dict(cek)), mimetype="application/json", status=200)

  
#download gambar tapi via image id
@bp.route('/get_image/<id>', methods =['GET'])
def show_image(id):
    filename = search_filename_from_id(id)
    path = os.path.join(current_app.instance_path, current_app.config['UPLOAD_DIR'])
    return send_from_directory(path, filename, as_attachment=True)

#return image url via id
@bp.route('/get_image_url/<id>', methods = ['GET'])
def image_url(id):
    path = "https://jft.web.id/woundapi/instance/uploads/"
    filename = search_filename_from_id(id)
    img_url = path + filename
    return Response(response = json.dumps({"image_url" : img_url}), mimetype="application/json", status=200)

#return image url list via id pasien
@bp.route('/pasien_image_list/<id_pasien>', methods = ['GET'])
def image_url_list(id_pasien):
    img_url = []
    list = helper.pasien_image_list(id_pasien)
    path = "https://jft.web.id/woundapi/instance/uploads/"

    for i in list:
        filename = search_filename_from_id(i)
        img_url.append(path + filename)

    return Response(response = json.dumps({"image_url" : img_url}), mimetype="application/json", status=200)

#return image list via id pasien
#mendapatkan data pasien berdasarkan perawat yang mengurus
@bp.route('image/find/<id_pasien>')
def image_list_id(id_pasien):
    try:
        filter = {}
        filter["id_pasien"] = id_pasien
        data = {"id_pasien" : id_pasien}
        cek = image_list_by_id(data)

       
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


#delete all collection
@bp.route('/delete_coll', methods= ['DELETE'])
def delete_all_collection():
    
    x = helper.delete_all_coll()
    return Response(response = json.dumps(x), mimetype="application/json", status=200)

@bp.route('upload/pasien/new', methods=['POST'])
def coba_image_pasien():
    old_id = request.form['id_pasien']
    jenis = request.form['jenis']
    new_id = request.form['isian']

    try:
        update_id_pasien_image(old_id, new_id)
        return Response(response = json.dumps({"message" : "berhasil"}), mimetype="application/json", status=200)
    
            
    except Exception as ex:
        print (ex)
        return Response(response = json.dumps({"message" : "false"}), mimetype="application/json", status=500)

@bp.route('upload/perawat/new', methods=['POST'])
def coba_image_perawat():
    old_id = request.form['id_pasien']
    jenis = request.form['jenis']
    new_id = request.form['isian']

    try:
        update_id_perawat_image(old_id, new_id)
        return Response(response = json.dumps({"message" : "berhasil"}), mimetype="application/json", status=200)
    
            
    except Exception as ex:
        print (ex)
        return Response(response = json.dumps({"message" : "false"}), mimetype="application/json", status=500)


@bp.route('image/update/anotasi', methods=['POST'])
def anotasi_update():
    file = request.files['image']
    id_image = request.form['id_image']
    

    try:
        if file and utils.allowed_file(file.filename):
                filename = secure_filename(file.filename)
                filename = utils.pad_timestamp(filename)
                path = os.path.join(current_app.instance_path, current_app.config['UPLOAD_DIR'])
                try:
                    os.makedirs(path)
                except OSError:
                    pass
                filepath = os.path.join(path, filename)
                file.save(filepath)
                        
                filter ={}
                filter['filename'] = filename
                helper.update_filename_byid(id_image,filter)
                              

                print(filepath)
                current_app.logger.debug(filepath);         
                return Response(response = json.dumps({"message" : "true"}), mimetype="application/json", status=200)
    except Exception as ex:
            print (ex)
            return Response(response = json.dumps({"message" : "error encountered"}), mimetype="application/json", status=500)       
        
