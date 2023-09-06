from uuid import uuid1
import numpy as np
import uuid
from flask import(
    Blueprint, Response, request)
import json
import datetime

from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename
from wound.logging.helper import delete_one_log, get_logs, get_log, insert_log, log_list_by_user
from wound.pasien.helper import  get_pasien, insert_pasien, get_pasien_ns
from wound import utils
from flask import Flask, jsonify
from bson.objectid import ObjectId
from bson import json_util, ObjectId
from typing import List
import time
import functools, logging, os, json
from flask import(
    Blueprint, flash, g, redirect, render_template, request, session, url_for, current_app, Markup, send_from_directory
)

from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename
from bson.objectid import ObjectId


bp = Blueprint('logactivity', __name__, url_prefix='/')

#get all images data
@bp.route('/get_logs', methods =['GET'])
def get_all_log():
    a = get_logs()
    hiya = list(a)
    hiya.reverse()
    #return Response(response = json.dumps(list(a)), mimetype="application/json", status=200)
    return render_template('user_log.html', navigation=hiya)

#menampilkan seluruh dokumen pada collection log_activity yang dimiliki satu user
@bp.route('/get_logs/<id_user>', methods =['GET'])
def get_user_logs(id_user):
                 
    filter ={}
    filter["id_perawat"] = id_user
    cek = log_list_by_user(filter)

    try:
        if cek == None: 
            return Response(response = json.dumps({"message" : "not found"}), mimetype="application/json", status=404)
        else:
            print(cek)
            return Response(response = json.dumps(list(cek)), mimetype="application/json", status=200)
        
    except Exception as ex:
        print (ex)
        return Response(response = json.dumps({"message" : "error encountered"}), mimetype="application/json", status=500)


#insert data logging
@bp.route('/insert_log', methods =['POST'])
def addLogging():
    try:        
            data = {"_id" : str(uuid.uuid4().hex),
                    "id_perawat" : request.form["id_perawat"],
                    "activity" : request.form["activity"],
                    "created_at" : time.strftime("%d/%m/%Y %H:%M:%S")
                    }

            cek = insert_log(data)
            return Response(response = json.dumps({"message" : "true"}), mimetype="application/json", status=200)
                         
                            
    except Exception as ex:
        print(ex)
        return Response(response = json.dumps({"message" : "exe"}), mimetype="application/json", status=500)


#delete 1 image berdasarkan id
@bp.route('/delete_log/<id>', methods= ['DELETE'])
def delete_image(id):
    filter = {}
    filter["_id"] = id
    cek = get_log(filter)
    delete_one_log(id)
    return Response(response = json.dumps(dict(cek)), mimetype="application/json", status=200)