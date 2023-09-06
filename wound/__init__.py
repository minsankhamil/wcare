import os

from flask import(
    Blueprint, Response, redirect, request, session, g)
from flask import Flask, jsonify, render_template, url_for
#from wound.pasien.pasien import bp, get_pasiens
from wound.user import db, user
from . import submission
from wound.pasien import pasien
from wound.image import upload
from wound.data_kajian import datakajian
from wound.logging import logactivity
from wound.inventaris import inventarisasi
from wound.layanan import layanans
from wound.data_pemeriksaan_kesehatan import datapemeriksaankesehatan

def create_app(test_config=None):
    #create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_pyfile('settings.cfg', silent=True)
    app.secret_key = os.urandom(24)
    #print(app.config)
    #mongocon = app.config['MONGO_CON']
    #print("MONGO_CON:" + mongocon)
    
    #ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    db.init_app(app)
    #app.register_blueprint(submission.bp)    
    app.register_blueprint(user.bp)
    app.register_blueprint(pasien.bp)
    app.register_blueprint(upload.bp)
    app.register_blueprint(datakajian.bp)
    app.register_blueprint(logactivity.bp)
    app.register_blueprint(inventarisasi.bp)
    app.register_blueprint(layanans.bp)
    app.register_blueprint(datapemeriksaankesehatan.bp)

    #Login
    #Route login
    @app.route('/login_apps')
    def login():
        if 'user_info' in session:
            return render_template('Dashboard.html')
        return render_template('Login.html')

    ####routing
    @app.route('/home')
    @app.route('/')
    def home():
        if 'user_info' in session:
            return render_template('Dashboard.html')
        return render_template('Login.html')
    
    #Akun Pasien
    #Route page pengelolaan akun
    @app.route('/manage_accounts')
    def manage_accounts():
        if 'user_info' in session:
            return render_template('ManageAccount.html')
        return render_template('Login.html')
    
    #Route page tambah pasien baru oleh klinik
    @app.route('/add_new_patient')
    def add_new_patient():
        if 'user_info' in session:
            return render_template('RegNewPatient.html')
        return render_template('Login.html')
    
    #Route page daftar pasien terverifikasi klinik
    @app.route('/list_patient')
    def list_patient():
        if 'user_info' in session:
            response = pasien.get_pasiens()
            return render_template('ListVerifyPatient.html', data = response.get_json())
        return render_template('Login.html')
    
    #Route page daftar pemohon pasien baru yang mendaftar melalui apps pasien
    @app.route('/list_request_new_patient')
    def list_request_new_patient():
        if 'user_info' in session:
            response = pasien.get_pasiens_unverify()
            return render_template('ListRequestNewPatient.html', data = response.get_json())
        return render_template('Login.html')
    
    #Route page profil pasien terverifikasi
    @app.route('/profil_pasien/<_id>')
    def profil_pasien(_id):
        if 'user_info' in session:
            response = pasien.get_profile_patient(_id)
            return render_template('ProfilePatient.html',  data = response.get_json())
        return render_template('Login.html')
    
    #Route page data pemohon pasien baru yang mendaftar melalui apps pasien
    @app.route('/profil_req_new_pasien/<_id>')
    def profil_pemohon_pasien_baru(_id):
        if 'user_info' in session:
            response = pasien.get_profile_patient(_id)
            return render_template('ProfileRequestNewPatient.html',  data = response.get_json())
        return render_template('Login.html')     
    
    #Route page pengelolaan pendaftaran berobat
    @app.route('/manage_pasien_berobat')
    def manage_pasien_berobat():
        if 'user_info' in session:
            #response = pasien.get_profile_patient()
            return render_template('ManageRegTreatment.html')#,  data = response.get_json())
        return render_template('Login.html')
    
    #Route page pendaftaran berobat offline
    @app.route('/pendaftaran_pasien_berobat_offline')
    def pendaftaran_pasien_berobat_offline():
        if 'user_info' in session:
            response = pasien.get_pasiens()
            return render_template('TreatmentRegOffline.html', data = response.get_json())
        return render_template('Login.html')
    
    #Route page list pasien daftar berobat online
    @app.route('/list_pasien_daftar_berobat_online')
    def list_pasien_daftar_berobat_online():
        if 'user_info' in session:
            return render_template('ListPatientRegTreatmentOnline.html')
        return render_template('Login.html')


    #Akun Staff Klinik
    #Route page daftar staff klinik
    @app.route('/add_new_staff')
    def add_new_staff():
        if 'user_info' in session:
            return render_template('RegNewStaff.html')
        return render_template('Login.html') 
    
    @app.route('/list_staff')
    def list_staff():
        if 'user_info' in session:
            response = user.get_users()
            return render_template('ListStaff.html', data = response.get_json())
        return render_template('Login.html') 
    
    @app.route('/profil_staff/<_id>')
    def profile_staff(_id):
        if 'user_info' in session:
            response = user.get_profile_staff(_id)
            return render_template('ProfileUser.html', data = response.get_json())
        return render_template('Login.html')
    
    #Inventaris
    #Route page daftar inventaris
    @app.route('/list_inventaris')
    def list_inventaris():
        if 'user_info' in session:
            response = inventarisasi.get_inventariss()
            return render_template('ListInventories.html', data = response.get_json())
        return render_template('Login.html')
    
    #Route page tambah inventaris baru
    @app.route('/add_inventaris')
    def inventaris():
        if 'user_info' in session:
            return render_template('AddInventory.html')
        return render_template('Login.html')
    
    #Route page detail inventaris
    @app.route('/detail_inventaris/<_id>')
    def detail_inventaris(_id):
        if 'user_info' in session:
            response = inventarisasi.get_details_inventaris(_id)
            return render_template('DetailInventory.html', data = response.get_json())
        return render_template('Login.html')
    
    #Route page edit inventaris
    @app.route('/edit_inventaris/<_id>')
    def edit_inventaris(_id):
        if 'user_info' in session:
            response = inventarisasi.get_details_inventaris(_id)
            return render_template('EditInventaris.html', data = response.get_json())
        return render_template('Login.html')



    #Layanan
    #Route page tambah layanan baru
    @app.route('/add_layanan')
    def layanan():
        if 'user_info' in session:
            return render_template('Services.html')
        return render_template('Login.html')
    
    #Route page daftar layanan
    @app.route('/list_layanan')
    def list_layanan():
        if 'user_info' in session:
            response = layanans.get_layanans()
            return render_template('ListServices.html', data = response.get_json())
        return render_template('Login.html')
    
    #Route page detail layanan
    @app.route('/detail_layanan/<_id>')
    def detail_layanan(_id):
        if 'user_info' in session:
            response = layanans.get_details_layanan(_id)
            return render_template('DetailService.html', data = response.get_json())
        return render_template('Login.html')
    
    #Route page edit layanan
    @app.route('/edit_layanan/<_id>')
    def edit_layanan(_id):
        if 'user_info' in session:
            response = layanans.get_details_layanan(_id)
            return render_template('EditService.html', data = response.get_json())
        return render_template('Login.html')
    

    #Pemeriksaan Kesehatan
    #Route page daftar pasien yang telah melakukan pemeriksaan kesehatan
    @app.route('/list_patient_medical_check')
    def list_patient_medical_check():
        if 'user_info' in session:
            response = pasien.get_pasiens()
            return render_template('MedicalCheck1.html', data = response.get_json())
        return render_template('Login.html')
    
    #Route page list hasil pemeriksaan kesehatan pasien berdasar nik
    @app.route('/list_medical_check_data/<nik>')
    def list_medical_check_data(nik):
        if 'user_info' in session:
            response = datapemeriksaankesehatan.all_data_pk(nik)
            print(response.get_json())
            return render_template('MedicalCheck2.html', data = response.get_json())
        return render_template('Login.html')
    
    #Route page detail hasil pemeriksaan kesehatan
    @app.route('/detail_medical_check_data/<_id>')
    def detail_medical_check_data(_id):
        if 'user_info' in session:
            response = datapemeriksaankesehatan.detail_data_pk(_id)
            print(response.get_json())
            return render_template('MedicalCheck3.html', data = response.get_json())
        return render_template('Login.html')
    


    #Data Kajian Pasien
    #Route page semua data kajian pasien
    @app.route('/data_kajian_luka')
    def data_kajian_pasien():
        if 'user_info' in session:
            response = pasien.get_pasiens()
            return render_template('KajianDataPatient.html', data = response.get_json())
        return render_template('Login.html')
    
    @app.route('/profil_data_kajian/<_id>')
    def profil_data_kajian(_id):
        if 'user_info' in session:
            response = pasien.get_profile_patient(_id)
            return render_template('DetailKajianData.html', data = response.get_json())
        return render_template('Login.html')
    
    @app.route('/List_Data_Kajian_Luka_Pasien')
    def list_data_kajian_luka_pasien():
        if 'user_info' in session:
            return render_template('ListKajianData.html')
        return render_template('Login.html')
        
    
    #Route page detail layanan
    #@app.route('/detail_layanan/<_id>')
    #def detail_layanan(_id):
        #response = inventarisasi.get_details_layanan(_id)
        #return render_template('DetailInventory.html', data = response.get_json())
    


    @app.route('/kuota_berobat')
    def kuota():
        if 'user_info' in session:
            return render_template('Quota.html')
        return render_template('Login.html')
    
    @app.route('/kelola_antrian_berobat')
    def antrian():
        if 'user_info' in session:
            return render_template('Queue.html')
        return render_template('Login.html')
    
    
    
    @app.route('/tagihan')
    def tagihan():
        if 'user_info' in session:
            return render_template('Bill.html')
        return render_template('Login.html')
    
    
    #@app.route('/test', methods = ["POST"])
    #def post_user():
        #return "testing"

    @app.errorhandler(404)
    def page_not_found(e):
        #note that we set the 404 status explicitly
        return render_template('404.html'), 404

    return app 

    
