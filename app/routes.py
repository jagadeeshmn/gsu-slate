from flask import request, flash, jsonify
from app import app, db
from werkzeug.security import generate_password_hash, check_password_hash
from app.models import Applicant, Application, Program
from flask_api import status
from datetime import datetime
from sqlalchemy import func

def hash_password(password):
    return generate_password_hash(password)

def check_password(password,password_hash):
    return check_password_hash(password,password_hash)

@app.route('/')
@app.route('/index')
def index():
    return "Hello world"

@app.route('/login',methods=['POST'])
def login():
    try:
        applicant = Applicant.query.filter_by(email = request.json['email']).first()
        if applicant is None or not check_password(applicant.password,request.json['password']):
            return jsonify({'status': status.HTTP_200_OK,'message':'Invalid Credentials'})
        else:
            return jsonify({'status': status.HTTP_200_OK,'message':'Login successful'})
    except:
        return jsonify({'status': status.HTTP_500_INTERNAL_SERVER_ERROR,'message':'Unable to login'})

@app.route('/register',methods=['POST'])
def register():
    try:
        applicant = Applicant.query.filter_by(email = request.json['email']).first()
        if applicant is None:
            password = hash_password(request.json['password'])
            applicant = Applicant(email=request.json['email'],fname=request.json['fname'],lname=request.json['lname'],password=password)
            db.session.add(applicant)
            db.session.commit()
            return jsonify({'status': status.HTTP_201_CREATED,'message':'Congratulations, you are now a registered user'})
        else:
            return jsonify({'status': status.HTTP_200_OK,'message':'Please use a different email'})
    except:
        return jsonify({'status': status.HTTP_500_INTERNAL_SERVER_ERROR,'message':'Unable to register'})

@app.route('/edit_profile',methods=['POST'])
def edit_profile():
    try:
        applicant = Applicant.query.filter_by(email = request.json['email']).first()
        if applicant is not None:
            password = hash_password(request.json['password'])
            
            applicant.fname = request.json['fname']
            applicant.lname = request.json['lname']
            applicant.password = password
            applicant.address1 = request.json['address1']
            applicant.address2 = request.json['address2']
            applicant.city = request.json['city']
            applicant.state = request.json['state']
            applicant.zip = int(request.json['zip'])
            applicant.GREQ = int(request.json['GREQ'])
            applicant.GREV = int(request.json['GREV'])
            applicant.GREA = float(request.json['GREA'])
            applicant.TOEFL = int(request.json['TOEFL'])

            db.session.add(applicant)
            db.session.commit()

            return jsonify({'status': status.HTTP_201_CREATED,'message':'Your profile updated successfully'})
        else:
            return jsonify({'status': status.HTTP_200_OK,'message':'Applicant Not found'})
    except:
        return jsonify({'status': status.HTTP_500_INTERNAL_SERVER_ERROR,'message':'Unable to Edit Profile'})

@app.route('/apply',methods=['POST'])
def apply():
    try:
        applicant = Applicant.query.filter_by(email = request.json['email']).first()
        if applicant is not None:
            application = Application.query.filter_by(email = request.json['email']).first()
            if application is None:
                program = Program.query.filter_by(program = request.json['program']).first()
                application = Application(
                    email = applicant.email,
                    university = request.json['university'] or 'GSU',
                    dname = request.json['dname'],
                    program = program.program,
                    dateOfApp = request.json['dateOfApp'] or datetime.utcnow(),
                    termOfAdmission = request.json['termOfAdmission'],
                    yearOfAdmission = request.json['yearOfAdmission'],
                    admissionStatus = request.json['admissionStatus'],
                    dataSentToPaws = request.json['dataSentToPaws'] or 'NO',
                    applicant_email = applicant.email,
                    applicant_program = program.program
                )

                db.session.add(application)
                db.session.commit()

                return jsonify({'status': status.HTTP_201_CREATED,'message':'Your application sent successfully'})
            else:
                return jsonify({'status': status.HTTP_200_OK,'message':'Looks like you have already applied.'})
        else:
            return jsonify({'status':status.HTTP_200_OK,'message':'Applicant not found'})
    except Exception as e:
        return jsonify({'status':status.HTTP_500_INTERNAL_SERVER_ERROR,'message':str(e)})
        # return jsonify({'status':status.HTTP_500_INTERNAL_SERVER_ERROR,'message':'Unable to apply'})
@app.route('/getappl',methods=['GET'])        
def getappl():       
    try:
        return_data = []
        applications = db.session.query(Applicant,Application).filter(Applicant.email == Application.email).filter(Application.admissionStatus == 'ACCEPT',Application.university == 'GSU').add_columns(Application.email,Applicant.fname,Applicant.lname,Application.dateOfApp).all()
        if applications is not None:
            for application in applications:
                application_data = {}
                application_data['email'] = application[2]
                application_data['fname'] = application[3]
                application_data['lname'] = application[4]
                application_data['dateOfApp'] = application[5]
                return_data.append(application_data)
            return jsonify({'status':status.HTTP_200_OK,'data':return_data})
    except Exception as e:
        return jsonify({'status':status.HTTP_500_INTERNAL_SERVER_ERROR,'message':str(e)})
        # return jsonify({'status':status.HTTP_500_INTERNAL_SERVER_ERROR,'message':'Unable to get applications'})
@app.route('/getstats',methods=['POST'])        
def getstats():       
    try:
        university = request.json['university']
        termOfAdmission= request.json['termOfAdmission']
        yearOfAdmission=request.json['yearOfAdmission']
        return_data = []
        statistics = db.session.query(Application.dname,Application.program,Application.admissionStatus, func.count(Application.admissionStatus).label('Count of Status')).filter(Application.university == university, Application.termOfAdmission == termOfAdmission , Application.yearOfAdmission == yearOfAdmission).group_by(Application.dname,Application.program,Application.admissionStatus).all()
        if statistics is not None:
            for s in statistics:
                s_data = {}
                s_data['department'] = s[0]
                s_data['program'] = s[1]
                s_data['status'] = s[2]
                s_data['count'] = s[3]
                return_data.append(s_data)
            return jsonify({'status':status.HTTP_200_OK,'data':return_data})
    except Exception as e:
        return jsonify({'status':status.HTTP_500_INTERNAL_SERVER_ERROR,'message':str(e)})
        # return jsonify({'status':status.HTTP_500_INTERNAL_SERVER_ERROR,'message':'Unable to get applications'})
